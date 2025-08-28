from .prefilter import prefilter_signals, obvious_ad_or_spam

class Decision:
    def __init__(self, action, reasons, scores):
        self.action = action                # "allow" | "soft-flag" | "hard-block"
        self.reasons = reasons              # ["ads", "irrelevant_low_sim", ...]
        self.scores = scores                # dict of model scores/signals

class PolicyEngine:
    def __init__(self,
                 th_ads_block=0.90,
                 th_irrelevant_flag=0.80,
                 th_rant_flag=0.85,
                 th_bienc_low=0.30):
        self.th_ads_block = th_ads_block
        self.th_irrelevant_flag = th_irrelevant_flag
        self.th_rant_flag = th_rant_flag
        self.th_bienc_low = th_bienc_low

    def decide(self, text, place_text, quality_scores, bi_score):
        reasons = []
        sig = prefilter_signals(text)

        # Ads/promo
        if obvious_ad_or_spam(sig) or quality_scores["spam_ad"] >= self.th_ads_block:
            reasons.append("ads_or_promo")
            return Decision("hard-block", reasons, {"quality": quality_scores, "bi_score": bi_score, **sig})

        # Irrelevant content
        if quality_scores["irrelevant"] >= self.th_irrelevant_flag or bi_score <= self.th_bienc_low:
            reasons.append("irrelevant_content" if quality_scores["irrelevant"] >= self.th_irrelevant_flag else "low_relevancy_similarity")
            return Decision("soft-flag", reasons, {"quality": quality_scores, "bi_score": bi_score, **sig})

        # Rant by likely non-visitor
        if quality_scores["rant_unvisited"] >= self.th_rant_flag:
            reasons.append("possible_rant_without_visit")
            return Decision("soft-flag", reasons, {"quality": quality_scores, "bi_score": bi_score, **sig})

        return Decision("allow", reasons, {"quality": quality_scores, "bi_score": bi_score, **sig})
