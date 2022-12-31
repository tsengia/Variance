import pytest

def test_default_units(app_with_defaults, client):
    r = client.get("/api/units/")
    assert r.status_code == 200
    