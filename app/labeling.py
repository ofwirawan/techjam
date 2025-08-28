from .prefilter import prefilter_signals

GENERIC_RANT_TERMS = {"scam", "fraud", "worst ever", "never again", "avoid at all costs"}
OOD_TERMS_BY_TYPE = {
    "restaurant": {"loan", "crypto", "insurance", "car rental"},
    "hotel": {"car polish", "plumber", "data recovery"}
}

def lf_ad(text): 
    s = prefilter_signals(text)
    return 1 if (s["has_url"] or s["has_phone"] or s["has_coupon"]) else -1

def lf_rant_unvisited(text):
    low_specificity = any(word in (text or "").lower() for word in GENERIC_RANT_TERMS)
    very_vague = len((text or "").split()) < 12
    return 1 if (low_specificity and very_vague) else -1

def lf_irrelevant(text, place_type):
    return 1 if any(k in (text or "").lower() for k in OOD_TERMS_BY_TYPE.get(place_type, set())) else -1
