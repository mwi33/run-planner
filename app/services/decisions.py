from pydantic import BaseModel


class CamberInputs(BaseModel):
    inner: float
    middle: float
    outer: float
    target_spread: float = 10.0


def camber_spread_rule(inputs: CamberInputs) -> dict:
    spread = abs(inputs.inner - inputs.outer)
    if spread > inputs.target_spread:
        rec = "Reduce front negative camber one step; inner–outer spread too high."
    else:
        rec = "Camber spread within target; hold."
    return {
        "rule": "camber_spread_rule",
        "inputs": inputs.model_dump(),
        "recommendation": rec,
    }
