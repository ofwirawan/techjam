import torch, torch.nn as nn
from transformers import AutoModel, AutoTokenizer

MODEL_NAME = "xlm-roberta-base"

class QualityClassifier(nn.Module):
    def __init__(self, base=MODEL_NAME, n_heads=3):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(base)
        hid = self.encoder.config.hidden_size
        self.heads = nn.ModuleList([nn.Linear(hid, 1) for _ in range(n_heads)])

    def forward(self, input_ids, attention_mask):
        x = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:]
        outs = [torch.sigmoid(h(x)) for h in self.heads]
        return outs  # [spam_ad, irrelevant, rant_unvisited]

class QualityModel:
    def __init__(self, device="cpu", model_path=None):
        self.tok = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.net = QualityClassifier().to(device)
        self.device = device
        # Optional: load fine-tuned state_dict if provided
        if model_path:
            sd = torch.load(model_path, map_location=device)
            self.net.load_state_dict(sd)
        self.net.eval()

    @torch.no_grad()
    def predict(self, texts):
        batch = self.tok(texts, padding=True, truncation=True, max_length=256, return_tensors="pt").to(self.device)
        spam, irr, rant = self.net(**batch)
        spam, irr, rant = [t.squeeze(-1).cpu().numpy().tolist() for t in [spam, irr, rant]]
        return [{"spam_ad": a, "irrelevant": b, "rant_unvisited": c} for a,b,c in zip(spam, irr, rant)]
