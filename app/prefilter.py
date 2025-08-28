import re

URL_RE = re.compile(r'(https?://|www\.)\S+', re.I)
PHONE_RE = re.compile(r'(\+\d{1,3}[-\s]?)?\d{3}[-\s]?\d{3,4}[-\s]?\d{3,4}')
COUPON_RE = re.compile(r'(use code|promo|discount|whatsapp|telegram|dm\s*me)', re.I)
REPEAT_PUNCT_RE = re.compile(r'([!?])\1{2,}')
EMOJI_RE = re.compile(r'[\U00010000-\U0010ffff]')

def prefilter_signals(text: str) -> dict:
    t = text or ""
    return {
        "has_url": bool(URL_RE.search(t)),
        "has_phone": bool(PHONE_RE.search(t)),
        "has_coupon": bool(COUPON_RE.search(t)),
        "too_short": len(t.strip()) < 8,
        "too_long": len(t) > 2000,
        "emoji_heavy": len(EMOJI_RE.findall(t)) > 10,
        "repeat_punct": bool(REPEAT_PUNCT_RE.search(t)),
        "all_caps": t.isupper() and len(t) > 12,
    }

def obvious_ad_or_spam(signals: dict) -> bool:
    return signals.get("has_url") or signals.get("has_phone") or signals.get("has_coupon")
