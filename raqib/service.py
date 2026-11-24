"""Inference code matching the fraud track notebook's feature engineering."""

import json
import os
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class FraudService:
    def __init__(self, model, info):
        self.model = model
        self.info = info
        self.features = info["features"]
        self.threshold = float(info["threshold"])
        self.typical = info["typical_values"]

    @classmethod
    def load(cls):
        model_path = Path(os.getenv("RAQIB_MODEL_PATH", ROOT / "tracks/fraud/artifacts/fraud_model.joblib"))
        info_path = Path(os.getenv("RAQIB_INFO_PATH", ROOT / "tracks/fraud/artifacts/model_info.json"))
        with info_path.open() as file:
            info = json.load(file)
        return cls(joblib.load(model_path), info)

    def score(self, payment):
        values = dict(payment)
        values["hour"] = (values["Time"] // 3600) % 24
        row = pd.DataFrame([values])[self.features]
        score = float(self.model.predict_proba(row)[0, 1])
        variants = pd.concat([row] * len(self.features), ignore_index=True)
        for i, feature in enumerate(self.features):
            variants.loc[i, feature] = self.typical[feature]
        changed = self.model.predict_proba(variants)[:, 1]
        reasons = [
            {"feature": name, "value": float(row.iloc[0][name]),
             "typical": float(self.typical[name]), "score_if_typical": float(changed[i]),
             "drop": float(score - changed[i])}
            for i, name in enumerate(self.features)
        ]
        reasons.sort(key=lambda reason: reason["drop"], reverse=True)
        # The notebook has only allow/alert. A second human-review priority is a
        # business rule; 'block' here means queue for urgent human review.
        decision = "block" if score >= 0.9 else "review" if score >= self.threshold else "allow"
        return {"score": score, "decision": decision, "threshold": self.threshold,
                "model_version": self.info["model_version"], "reasons": reasons[:3]}
