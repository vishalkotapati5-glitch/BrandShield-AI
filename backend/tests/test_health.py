from sqlalchemy.exc import OperationalError

from app.db.session import get_db
from app.main import app


def test_health_ok(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_unknown_route_uses_error_envelope(client):
    r = client.get("/api/v1/does-not-exist")
    assert r.status_code == 404
    body = r.json()["error"]
    assert body["code"] == "http_404"
    assert "message" in body and "details" in body


def test_unhandled_error_does_not_leak_internals(client):
    class BrokenSession:
        def execute(self, *_a, **_k):
            raise OperationalError("SELECT 1", {}, Exception("secret-connection-string"))

        def close(self):
            pass

    app.dependency_overrides[get_db] = lambda: BrokenSession()
    try:
        r = client.get("/api/v1/health/db")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 500
    assert r.json()["error"]["code"] == "internal_error"
    assert "secret" not in r.text
