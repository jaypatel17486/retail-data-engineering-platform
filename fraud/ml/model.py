import torch.nn as nn


class FraudModel(nn.Module):
    """
    FluxGuard neural network for transaction fraud classification.
    """

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