from fastapi import APIRouter, Query
from psycopg2.extras import RealDictCursor

from fluxguard_api.database import (
    get_connection,
    release_connection,
)

from fluxguard_api.models import (
    FraudAlertResponse,
    FraudStatsResponse,
)


router = APIRouter(
    prefix="/fraud",
    tags=["Fraud Detection"],
)


@router.get(
    "/alerts",
    response_model=list[FraudAlertResponse],
)
def get_fraud_alerts(
    limit: int = Query(default=50, ge=1, le=500),
):
    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                fa.id,
                fa.event_id,
                fa.order_id,
                fa.customer_id,
                fa.risk_level,
                fa.fraud_score,
                fa.decision,
                fa.status,
                fa.created_at,

                t.amount,
                t.payment_method,
                t.billing_country,
                t.shipping_country,

                fp.rule_score,
                fp.ml_probability,
                fp.hybrid_score

            FROM fraud_alerts fa

            JOIN transactions t
                ON fa.event_id = t.event_id

            LEFT JOIN fraud_predictions fp
                ON fa.event_id = fp.event_id

            ORDER BY fa.created_at DESC

            LIMIT %s
            """,
            (limit,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        release_connection(connection)


@router.get(
    "/stats",
    response_model=FraudStatsResponse,
)
def get_fraud_stats():
    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_transactions,

                COUNT(*) FILTER (
                    WHERE final_decision = 'APPROVE'
                ) AS approved,

                COUNT(*) FILTER (
                    WHERE final_decision = 'REVIEW'
                ) AS review,

                COUNT(*) FILTER (
                    WHERE final_decision = 'BLOCK'
                ) AS blocked,

                ROUND(
                    AVG(hybrid_score)::numeric,
                    4
                ) AS average_risk_score

            FROM fraud_predictions
            """
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        release_connection(connection)