import os

import joblib
import numpy as np
import torch

from fraud.ml.model import FraudModel


MODEL_PATH = "fraud/ml/models/fluxguard_fraud_model.pt"
SCALER_PATH = "fraud/ml/models/scaler.pkl"

FEATURE_NAMES = [
    "amount",
    "country_mismatch",
    "payment_failed",
    "suspected_fraud_failure",
]


class FraudPredictor:
    """
    Load the trained FluxGuard PyTorch model and perform
    fraud predictions for incoming payment events.
    """

    def __init__(self):

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}"
            )

        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(
                f"Scaler not found: {SCALER_PATH}"
            )

        self.model = FraudModel()

        state_dict = torch.load(
            MODEL_PATH,
            map_location="cpu",
            weights_only=True,
        )

        self.model.load_state_dict(state_dict)

        self.model.eval()

        self.scaler = joblib.load(
            SCALER_PATH
        )

    def build_features(self, event):
        """
        Convert a payment event into the exact features
        expected by the model.
        """

        amount = float(
            event.get("amount") or 0
        )

        billing_country = event.get(
            "billing_country"
        )

        shipping_country = event.get(
            "shipping_country"
        )

        country_mismatch = int(
            bool(billing_country)
            and bool(shipping_country)
            and billing_country != shipping_country
        )

        payment_failed = int(
            event.get("event_type")
            == "payment_failed"
        )

        suspected_fraud_failure = int(
            event.get("failure_reason")
            == "suspected_fraud"
        )

        return np.array(
            [[
                amount,
                country_mismatch,
                payment_failed,
                suspected_fraud_failure,
            ]],
            dtype=np.float32,
        )

    def predict(self, event):
        """
        Return fraud probability and ML risk classification.
        """

        features = self.build_features(event)

        scaled_features = self.scaler.transform(
            features
        )

        tensor = torch.tensor(
            scaled_features,
            dtype=torch.float32,
        )

        with torch.no_grad():

            logits = self.model(tensor)

            probability = torch.sigmoid(
                logits
            ).item()

        if probability >= 0.75:
            risk_level = "HIGH"

        elif probability >= 0.40:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

        return {
            "ml_fraud_probability": round(
                probability,
                4
            ),
            "ml_risk_level": risk_level,
            "ml_is_suspicious": probability >= 0.50,
        }


predictor = FraudPredictor()