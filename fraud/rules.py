def calculate_fraud_score(event):
    """
    Calculate a rule-based fraud risk score for a payment event.

    Returns:
        fraud_score
        risk_level
        is_suspicious
        reasons
    """

    score = 0
    reasons = []

    amount = float(event.get("amount") or 0)

    # Rule 1: Large transaction
    if amount >= 1000:
        score += 30
        reasons.append("high_transaction_amount")

    # Rule 2: Very large transaction
    if amount >= 1800:
        score += 20
        reasons.append("very_high_transaction_amount")

    # Rule 3: Billing/shipping country mismatch
    billing_country = event.get("billing_country")
    shipping_country = event.get("shipping_country")

    if (
        billing_country
        and shipping_country
        and billing_country != shipping_country
    ):
        score += 25
        reasons.append("country_mismatch")

    # Rule 4: Failed payment
    if event.get("event_type") == "payment_failed":
        score += 15
        reasons.append("payment_failed")

    # Rule 5: Payment system already flagged suspected fraud
    if event.get("failure_reason") == "suspected_fraud":
        score += 30
        reasons.append("suspected_fraud_failure")

    # Never allow score above 100
    score = min(score, 100)

    # Determine risk level
    if score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "fraud_score": score,
        "risk_level": risk_level,
        "is_suspicious": score >= 60,
        "fraud_reasons": reasons,
    }