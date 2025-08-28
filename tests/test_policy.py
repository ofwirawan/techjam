from app.policy import PolicyEngine

def test_policy_defaults():
    pe = PolicyEngine()
    q = {"spam_ad": 0.01, "irrelevant": 0.05, "rant_unvisited": 0.05}
    decision = pe.decide("Nice coffee and toast.", "Cafe | restaurant | tags: coffee", q, 0.75)
    assert decision.action == "allow"
