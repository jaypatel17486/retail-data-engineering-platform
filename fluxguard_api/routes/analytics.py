from fastapi import APIRouter, Query
from psycopg2.extras import RealDictCursor

from fluxguard_api.database import (
    get_connection,
    release_connection,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


# =========================================================
# OVERVIEW
# =========================================================

@router.get("/overview")
def get_overview():
    connection = get_connection()
    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_transactions,

                COALESCE(
                    SUM(amount) FILTER (
                        WHERE event_type = 'payment_completed'
                    ),
                    0
                ) AS total_revenue,

                COALESCE(
                    AVG(amount),
                    0
                ) AS average_transaction_value,

                COUNT(*) FILTER (
                    WHERE event_type = 'payment_completed'
                ) AS successful_payments,

                COUNT(*) FILTER (
                    WHERE event_type = 'payment_failed'
                ) AS failed_payments

            FROM transactions
            """
        )

        transaction_stats = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_predictions,

                COUNT(*) FILTER (
                    WHERE final_decision = 'APPROVE'
                ) AS approved,

                COUNT(*) FILTER (
                    WHERE final_decision = 'REVIEW'
                ) AS review,

                COUNT(*) FILTER (
                    WHERE final_decision = 'BLOCK'
                ) AS blocked

            FROM fraud_predictions
            """
        )

        fraud_stats = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS fraud_alerts
            FROM fraud_alerts
            """
        )

        alert_stats = cursor.fetchone()

        return {
            **transaction_stats,
            **fraud_stats,
            **alert_stats,
        }

    finally:
        cursor.close()
        release_connection(connection)


# =========================================================
# REVENUE
# =========================================================

@router.get("/revenue")
def get_revenue():
    connection = get_connection()
    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                DATE_TRUNC(
                    'hour',
                    event_timestamp
                ) AS hour,

                COUNT(*) AS transactions,

                COALESCE(
                    SUM(amount),
                    0
                ) AS revenue

            FROM transactions

            WHERE event_type = 'payment_completed'

            GROUP BY 1

            ORDER BY 1 DESC

            LIMIT 24
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        release_connection(connection)


# =========================================================
# PAYMENT ANALYTICS
# =========================================================

@router.get("/payments")
def get_payment_stats():
    connection = get_connection()
    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_payments,

                COUNT(*) FILTER (
                    WHERE event_type = 'payment_completed'
                ) AS successful,

                COUNT(*) FILTER (
                    WHERE event_type = 'payment_failed'
                ) AS failed

            FROM transactions
            """
        )

        result = cursor.fetchone()

        total = result["total_payments"] or 0
        successful = result["successful"] or 0
        failed = result["failed"] or 0

        success_rate = (
            successful / total * 100
            if total > 0
            else 0
        )

        failure_rate = (
            failed / total * 100
            if total > 0
            else 0
        )

        return {
            "total_payments": total,
            "successful": successful,
            "failed": failed,
            "success_rate": round(
                success_rate,
                2
            ),
            "failure_rate": round(
                failure_rate,
                2
            ),
        }

    finally:
        cursor.close()
        release_connection(connection)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

@router.get("/risk-distribution")
def get_risk_distribution():
    connection = get_connection()
    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                final_risk AS risk_level,
                COUNT(*) AS count

            FROM fraud_predictions

            GROUP BY final_risk

            ORDER BY final_risk
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        release_connection(connection)


# =========================================================
# RECENT ACTIVITY
# =========================================================

@router.get("/recent-activity")
def get_recent_activity(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    )
):
    connection = get_connection()
    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    try:
        cursor.execute(
            """
            SELECT
                t.event_id,
                t.order_id,
                t.customer_id,
                t.event_type,
                t.amount,
                t.payment_method,
                t.event_timestamp,

                fp.rule_score,
                fp.ml_probability,
                fp.hybrid_score,
                fp.final_risk,
                fp.final_decision

            FROM transactions t

            LEFT JOIN fraud_predictions fp
                ON t.event_id = fp.event_id

            ORDER BY t.event_timestamp DESC

            LIMIT %s
            """,
            (limit,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        release_connection(connection)