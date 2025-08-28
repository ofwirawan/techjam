from sentence_transformers import SentenceTransformer, util

BIENC_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class RelevancyScorer:
    def __init__(self, bienc=BIENC_NAME, device=None):
        device = device or "cpu"
        self.model = SentenceTransformer(bienc, device=device)

    def bi_encoder_score(self, review_text: str, place_text: str) -> float:
        embs = self.model.encode([review_text, place_text], normalize_embeddings=True, convert_to_tensor=True)
        return float(util.cos_sim(embs[0], embs[1]).item())
