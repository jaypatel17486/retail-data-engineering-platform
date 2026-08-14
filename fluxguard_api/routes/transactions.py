from fastapi import APIRouter, HTTPException, Query
from psycopg2.extras import RealDictCursor

from fluxguard_api.database import (
    get_connection,
    release_connection,
)
from fluxguard_api.models import TransactionResponse


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.get(
    "",
    response_model=list[TransactionResponse],
)
def get_transactions(
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
                event_id,
                order_id,
                customer_id,
                event_type,
                amount,
                currency,
                payment_method,
                billing_country,
                shipping_country,
                event_timestamp
            FROM transactions
            ORDER BY event_timestamp DESC
            LIMIT %s
            """,
            (limit,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        release_connection(connection)


@router.get("/{order_id}")
def get_transaction(order_id: str):
    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                t.*,
                fp.rule_score,
                fp.rule_risk,
                fp.ml_probability,
                fp.ml_risk,
                fp.hybrid_score,
                fp.final_risk,
                fp.final_decision

            FROM transactions t

            LEFT JOIN fraud_predictions fp
                ON t.event_id = fp.event_id

            WHERE t.order_id = %s

            ORDER BY t.event_timestamp DESC

            LIMIT 1
            """,
            (order_id,),
        )

        transaction = cursor.fetchone()

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found",
            )

        return transaction

    finally:
        cursor.close()
        release_connection(connection)