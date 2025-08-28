# Review Guard – ML system for Google-style location review quality & relevancy

A production-minded reference implementation that:
- **Gauges review quality:** detects spam/ads, irrelevant content, and rants from likely non-visitors.
- **Assesses relevancy:** checks whether a review is truly about the specific place.
- **Enforces policies:** combines ML + rules into decisions (`allow`, `soft-flag`, `hard-block`) with reasons.

## Quick start

```bash
# 1) Create venv and install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Run API
uvicorn app.main:app --reload --port 8000
# Visit http://127.0.0.1:8000/docs for interactive Swagger UI
```

### Minimal usage (API)
`POST /evaluate`
```json
{
  "review_text": "Great flat white, friendly barista.",
  "place_context": {
    "place_id": "p123",
    "name": "Kopi Corner",
    "category": "restaurant",
    "tags": ["kopi", "kaya toast", "hawker"],
    "neighborhood": "Tiong Bahru, Singapore",
    "owner_desc": "Casual breakfast spot with local coffee.",
    "menu_or_services": ["kopi o", "half-boiled eggs", "toast"]
  }
}
```
**Response**
```json
{
  "action": "allow",
  "reasons": [],
  "scores": { "quality": {"spam_ad": 0.02, "irrelevant": 0.10, "rant_unvisited": 0.05}, "bi_score": 0.71 },
  "place_context": "Kopi Corner | restaurant | Tiong Bahru, Singapore | tags: kopi, kaya toast, hawker | menu/services: kopi o, half-boiled eggs, toast | about: Casual breakfast spot with local coffee."
}
```

## Layout
```
review-guard/
  app/                 # service, models, policy
  config/              # thresholds and settings
  data/                # toy samples
  docker/              # containerization
  models/              # place for fine-tuned weights (optional)
  scripts/             # training stubs
  tests/               # unit tests
```

## Notes
- The ML components load **placeholder weights** by default so the API runs out-of-the-box. Replace with your fine-tuned models under `models/`.
- Thresholds are in `config/thresholds.yaml`. Start conservative (high precision for blocks).
- See `scripts/train_*.py` for training stubs and guidance.
