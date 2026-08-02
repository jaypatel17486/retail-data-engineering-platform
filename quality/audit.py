from warehouse.loaders.database import get_connection


def write_audit_log(
    pipeline_name,
    status,
    rows_processed,
    rows_failed,
    duration_seconds,
    message,
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO warehouse.etl_audit
        (
            pipeline_name,
            status,
            rows_processed,
            rows_failed,
            duration_seconds,
            message
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            pipeline_name,
            status,
            rows_processed,
            rows_failed,
            duration_seconds,
            message,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()