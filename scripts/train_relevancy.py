# scripts/train_relevancy.py
# Stub: outline for training the two-tower bi-encoder with hard negatives.
# - Create (review, correct_place_text) positives.
# - Sample hard negatives from nearby / same-category places.
# - Train SentenceTransformer model and save via .save() under models/
