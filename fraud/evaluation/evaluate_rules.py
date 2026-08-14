from streaming.events import generate_transaction
from fraud.rules import calculate_fraud_score


def evaluate_rules(num_transactions=1000):

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for _ in range(num_transactions):

        _, payment = generate_transaction()

        actual_fraud = payment["is_fraud"]

        result = calculate_fraud_score(payment)

        predicted_fraud = 1 if result["is_suspicious"] else 0

        # Actual fraud + predicted fraud
        if actual_fraud == 1 and predicted_fraud == 1:
            true_positive += 1

        # Legitimate + predicted legitimate
        elif actual_fraud == 0 and predicted_fraud == 0:
            true_negative += 1

        # Legitimate but predicted fraud
        elif actual_fraud == 0 and predicted_fraud == 1:
            false_positive += 1

        # Fraud but predicted legitimate
        elif actual_fraud == 1 and predicted_fraud == 0:
            false_negative += 1

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive > 0
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative > 0
        else 0
    )

    accuracy = (
        (true_positive + true_negative) / num_transactions
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0
    )

    print("=" * 60)
    print("FLUXGUARD RULE ENGINE EVALUATION")
    print("=" * 60)

    print(f"Transactions:   {num_transactions}")
    print()

    print("Confusion Matrix")
    print("-" * 60)

    print(f"True Positive:  {true_positive}")
    print(f"True Negative:  {true_negative}")
    print(f"False Positive: {false_positive}")
    print(f"False Negative: {false_negative}")

    print()
    print("Performance")
    print("-" * 60)

    print(f"Accuracy:  {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1 Score:  {f1:.3f}")

    print("=" * 60)


if __name__ == "__main__":
    evaluate_rules(1000)