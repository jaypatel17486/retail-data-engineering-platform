from fraud.rules import calculate_fraud_score
from fraud.ml.predict import predictor


def analyze_transaction(event):
    """
    Analyze a payment using both:
    1. Rule-based fraud detection
    2. PyTorch ML fraud detection

    Returns one unified FluxGuard fraud decision.
    """

    # -----------------------------------------------------
    # RULE ENGINE
    # -----------------------------------------------------

    rule_result = calculate_fraud_score(event)

    rule_score = rule_result["fraud_score"]
    rule_risk = rule_result["risk_level"]

    # -----------------------------------------------------
    # PYTORCH MODEL
    # -----------------------------------------------------

    ml_result = predictor.predict(event)

    ml_probability = ml_result["ml_fraud_probability"]
    ml_risk = ml_result["ml_risk_level"]

    # -----------------------------------------------------
    # HYBRID SCORE
    # -----------------------------------------------------

    # Convert rule score from 0-100 to 0-1
    normalized_rule_score = rule_score / 100

    # Give ML slightly more weight
    hybrid_score = (
        normalized_rule_score * 0.40
        + ml_probability * 0.60
    )

    hybrid_score = round(hybrid_score, 4)

    # -----------------------------------------------------
    # FINAL DECISION
    # -----------------------------------------------------

    if hybrid_score >= 0.75:
        final_decision = "BLOCK"
        final_risk = "HIGH"

    elif hybrid_score >= 0.40:
        final_decision = "REVIEW"
        final_risk = "MEDIUM"

    else:
        final_decision = "APPROVE"
        final_risk = "LOW"

    return {
        "order_id": event.get("order_id"),
        "customer_id": event.get("customer_id"),

        "rule_score": rule_score,
        "rule_risk": rule_risk,
        "rule_reasons": rule_result["fraud_reasons"],

        "ml_probability": ml_probability,
        "ml_risk": ml_risk,

        "hybrid_score": hybrid_score,

        "final_risk": final_risk,
        "final_decision": final_decision,
    }