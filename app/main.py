from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import yaml
import os

from .schemas import EvaluateRequest, EvaluateResponse
from .features import build_place_text
from .quality_model import QualityModel
from .relevancy_model import RelevancyScorer
from .policy import PolicyEngine

app = FastAPI(title="Review Guard", version="0.1.0")

# Load thresholds
TH_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "thresholds.yaml")
with open(TH_PATH, "r") as f:
    TH = yaml.safe_load(f)

policy = PolicyEngine(**TH)

# Lazy-load heavy models to speed import (optional micro-optimization)
_quality_model = None
_relevancy = None

def get_models():
    global _quality_model, _relevancy
    if _quality_model is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "quality.pt")
        _quality_model = QualityModel(device="cpu", model_path=model_path if os.path.exists(model_path) else None)
    if _relevancy is None:
        _relevancy = RelevancyScorer(device="cpu")
    return _quality_model, _relevancy

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    qm, rel = get_models()
    place_text = build_place_text(req.place_context)
    q = qm.predict([req.review_text])[0]
    bi = rel.bi_encoder_score(req.review_text, place_text)
    decision = policy.decide(req.review_text, place_text, q, bi)
    return EvaluateResponse(
        action=decision.action,
        reasons=decision.reasons,
        scores=decision.scores,
        place_context=place_text
    )
