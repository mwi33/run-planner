import json


def test_decide_camber_endpoint(client):
    payload = {"inner": 90, "middle": 82, "outer": 79, "target_spread": 10}
    resp = client.post(
        "/api/run-plans/1/decide/camber", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["rule"] == "camber_spread_rule"
    assert "recommendation" in data
