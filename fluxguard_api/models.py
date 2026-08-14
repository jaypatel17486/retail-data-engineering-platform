from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    event_id: str
    order_id: str
    customer_id: str
    event_type: str

    amount: Decimal
    currency: str

    payment_method: Optional[str] = None

    billing_country: Optional[str] = None
    shipping_country: Optional[str] = None

    event_timestamp: datetime


class FraudAlertResponse(BaseModel):
    id: int

    event_id: str
    order_id: str
    customer_id: str

    risk_level: str
    fraud_score: Decimal
    decision: str
    status: str

    created_at: datetime

    amount: Decimal
    payment_method: Optional[str] = None

    billing_country: Optional[str] = None
    shipping_country: Optional[str] = None

    rule_score: Optional[int] = None
    ml_probability: Optional[Decimal] = None
    hybrid_score: Optional[Decimal] = None


class FraudStatsResponse(BaseModel):
    total_transactions: int
    approved: int
    review: int
    blocked: int
    average_risk_score: Optional[Decimal] = None