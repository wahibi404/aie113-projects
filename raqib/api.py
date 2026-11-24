"""HTTP entry point. Transaction fields are never logged."""

from functools import lru_cache
from math import isfinite
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, create_model

from raqib.service import FraudService

Payment = create_model(
    "Payment", __base__=BaseModel,
    __config__=ConfigDict(extra="forbid"),
    Time=(float, Field(ge=0)), Amount=(float, Field(ge=0)),
    **{f"V{i}": (float, ...) for i in range(1, 29)},
)


class Reason(BaseModel):
    feature: str
    value: float
    typical: float
    score_if_typical: float
    drop: float


class Result(BaseModel):
    score: float
    decision: Literal["allow", "review", "block"]
    threshold: float
    model_version: str
    reasons: list[Reason]


@lru_cache(maxsize=1)
def get_service() -> FraudService:
    try:
        return FraudService.load()
    except (OSError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=503, detail="Model unavailable") from exc


app = FastAPI(title="Raqib", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready(service: FraudService = Depends(get_service)):  # noqa: B008
    return {"status": "ready", "model_version": service.info["model_version"]}


@app.post("/score", response_model=Result)
def score(payment: Payment, service: FraudService = Depends(get_service)):  # noqa: B008
    values = payment.model_dump()
    if not all(isfinite(value) for value in values.values()):
        raise HTTPException(status_code=422, detail="All values must be finite")
    return service.score(values)
