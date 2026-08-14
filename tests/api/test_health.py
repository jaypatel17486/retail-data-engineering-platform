from fluxguard_api.main import app


def test_app_exists():
    assert app is not None


def test_app_name():
    assert app.title == "FluxGuard API"


def test_routes_exist():
    schema = app.openapi()
    paths = schema["paths"]

    assert "/" in paths
    assert "/health" in paths
    assert "/api/v1/info" in paths

    assert "/api/v1/transactions" in paths
    assert "/api/v1/transactions/{order_id}" in paths

    assert "/api/v1/fraud/alerts" in paths
    assert "/api/v1/fraud/stats" in paths