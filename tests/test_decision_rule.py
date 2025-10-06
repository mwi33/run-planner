from app.services.decisions import CamberInputs, camber_spread_rule


def test_camber_rule_recommends_reduce():
    res = camber_spread_rule(CamberInputs(inner=95, middle=82, outer=70, target_spread=10))
    assert "Reduce" in res["recommendation"]


def test_camber_rule_recommends_hold():
    res = camber_spread_rule(CamberInputs(inner=90, middle=82, outer=82, target_spread=10))
    assert "hold" in res["recommendation"].lower()
