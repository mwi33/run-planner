from flask import jsonify, request

from ..services.decisions import CamberInputs, camber_spread_rule
from . import api_bp


@api_bp.post("/run-plans/<int:rp_id>/decide/camber")
def decide_camber(rp_id: int):
    payload = request.get_json(force=True, silent=True) or {}
    try:
        inputs = CamberInputs(**payload)
    except Exception as e:
        return jsonify({"error": f"Invalid payload: {e}"}), 400
    result = camber_spread_rule(inputs)
    return jsonify(result), 200
