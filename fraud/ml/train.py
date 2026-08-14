import os
import random

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# =========================================================
# CONFIGURATION
# =========================================================

DATASET_PATH = "fraud/ml/transactions.csv"

MODEL_DIR = "fraud/ml/models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fluxguard_fraud_model.pt"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

RANDOM_SEED = 42


# =========================================================
# REPRODUCIBILITY
# =========================================================

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)


# =========================================================
# MODEL
# =========================================================

class FraudModel(nn.Module):

    def __init__(self):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(4, 16),

            nn.ReLU(),

            nn.Linear(16, 8),

            nn.ReLU(),

            nn.Linear(8, 1),
        )

    def forward(self, x):

        return self.network(x)


# =========================================================
# LOAD DATA
# =========================================================

print("=" * 60)
print("FLUXGUARD PYTORCH FRAUD MODEL")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)


FEATURES = [
    "amount",
    "country_mismatch",
    "payment_failed",
    "suspected_fraud_failure",
]


X = df[FEATURES].values

y = df["is_fraud"].values


# =========================================================
# TRAIN / VALIDATION / TEST SPLIT
# =========================================================

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=RANDOM_SEED,
    stratify=y,
)


X_validation, X_test, y_validation, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=RANDOM_SEED,
    stratify=y_temp,
)


print(f"Training samples:   {len(X_train)}")
print(f"Validation samples: {len(X_validation)}")
print(f"Test samples:       {len(X_test)}")


# =========================================================
# FEATURE SCALING
# =========================================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_validation = scaler.transform(X_validation)

X_test = scaler.transform(X_test)


# =========================================================
# CONVERT TO TENSORS
# =========================================================

X_train_tensor = torch.tensor(
    X_train,
    dtype=torch.float32
)

y_train_tensor = torch.tensor(
    y_train,
    dtype=torch.float32
).reshape(-1, 1)


X_validation_tensor = torch.tensor(
    X_validation,
    dtype=torch.float32
)


# =========================================================
# MODEL SETUP
# =========================================================

model = FraudModel()


# Handle class imbalance
fraud_count = np.sum(y_train == 1)

normal_count = np.sum(y_train == 0)

positive_weight = normal_count / fraud_count


loss_function = nn.BCEWithLogitsLoss(
    pos_weight=torch.tensor(
        [positive_weight],
        dtype=torch.float32
    )
)


optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# =========================================================
# TRAIN
# =========================================================

EPOCHS = 30


for epoch in range(EPOCHS):

    model.train()

    optimizer.zero_grad()

    logits = model(
        X_train_tensor
    )

    loss = loss_function(
        logits,
        y_train_tensor
    )

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 5 == 0:

        print(
            f"Epoch "
            f"{epoch + 1:02d}/{EPOCHS} "
            f"Loss: {loss.item():.4f}"
        )


# =========================================================
# VALIDATION
# =========================================================

model.eval()


with torch.no_grad():

    validation_logits = model(
        X_validation_tensor
    )

    validation_probabilities = torch.sigmoid(
        validation_logits
    ).numpy().flatten()


# Initial threshold
THRESHOLD = 0.50


validation_predictions = (
    validation_probabilities >= THRESHOLD
).astype(int)


print()
print("Validation Results")
print("-" * 60)

print(
    f"F1: "
    f"{f1_score(y_validation, validation_predictions):.3f}"
)


# =========================================================
# FINAL TEST
# =========================================================

X_test_tensor = torch.tensor(
    X_test,
    dtype=torch.float32
)


with torch.no_grad():

    test_logits = model(
        X_test_tensor
    )

    probabilities = torch.sigmoid(
        test_logits
    ).numpy().flatten()


predictions = (
    probabilities >= THRESHOLD
).astype(int)


accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

auc = roc_auc_score(
    y_test,
    probabilities
)


print()
print("=" * 60)
print("TEST RESULTS")
print("=" * 60)

print(
    f"Accuracy:  {accuracy:.3f}"
)

print(
    f"Precision: {precision:.3f}"
)

print(
    f"Recall:    {recall:.3f}"
)

print(
    f"F1 Score:  {f1:.3f}"
)

print(
    f"ROC-AUC:   {auc:.3f}"
)


# =========================================================
# SAVE MODEL
# =========================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


torch.save(
    model.state_dict(),
    MODEL_PATH
)


joblib.dump(
    scaler,
    SCALER_PATH
)


print()
print(f"Model saved:  {MODEL_PATH}")
print(f"Scaler saved: {SCALER_PATH}")

print("=" * 60)