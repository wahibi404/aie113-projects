import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from raqib.api import app
from raqib.service import FraudService

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def payment():
    return {"Time": 154278.0, "Amount": 1504.93,
            **{f"V{i}": 0.0 for i in range(1, 29)}}


class FixedModel:
    def predict_proba(self, rows):
        return np.array([[1 - value, value] for value in rows["V1"].clip(0, 1)])


def test_threshold_boundaries(payment):
    service = FraudService(FixedModel(), {"features": ["V1"], "threshold": .4,
        "typical_values": {"V1": 0}, "model_version": "test"})
    for value, expected in [(0.399, "allow"), (.4, "review"), (.9, "block")]:
        payment["V1"] = value
        assert service.score(payment)["decision"] == expected


def test_http_validation_and_health(payment):
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.post("/score", json={**payment, "Amount": -1}).status_code == 422
    missing = dict(payment)
    del missing["V28"]
    assert client.post("/score", json=missing).status_code == 422
    assert client.post("/score", json={**payment, "unexpected": 1}).status_code == 422


def test_real_model_golden_and_behaviour():
    service = FraudService.load()
    info = json.loads((ROOT / "tracks/fraud/artifacts/model_info.json").read_text())
    assert info["data"]["rows"] == 284807
    assert info["data"]["frauds"] == 492
    df = pd.read_csv(ROOT / "tracks/fraud/data/creditcard.csv")
    df = df.sort_values("Time", kind="stable").reset_index(drop=True)
    test = df.iloc[int(len(df)*.8):]
    scores = service.model.predict_proba(test.assign(hour=(test.Time // 3600) % 24)[service.features])[:, 1]
    golden = np.array(json.loads((ROOT / "tests/golden_5000.json").read_text()))
    assert len(golden) == 5000
    np.testing.assert_allclose(scores[:5000], golden, rtol=0, atol=1e-8)
    alerts = scores >= service.threshold
    caught = int((alerts & (test.Class.to_numpy() == 1)).sum())
    assert caught == info["test_metrics"]["frauds_caught"]
    assert int(alerts.sum()) == info["test_metrics"]["alerts"]
    assert caught / int(test.Class.sum()) >= .70
    assert caught / int(alerts.sum()) >= .80
    sample = json.loads((ROOT / "tests/golden.json").read_text())
    result = service.score(sample["payment"])
    assert result["score"] == pytest.approx(sample["score"], abs=1e-10)
    assert result["reasons"][0]["feature"] == sample["top_reason"]
    assert result["reasons"][0]["drop"] > 0
    client = TestClient(app)
    assert client.post("/score", json=sample["payment"]).json()["score"] == pytest.approx(sample["score"])
    assert client.get("/ready").status_code == 200
