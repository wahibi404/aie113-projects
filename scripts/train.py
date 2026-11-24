"""Reproduce the instructor notebook's time split, model and threshold."""

import json
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tracks/fraud/data/creditcard.csv"
OUT = ROOT / "tracks/fraud/artifacts"
FEATURES = [f"V{i}" for i in range(1, 29)] + ["Amount", "hour"]
THRESHOLDS = [.01, .02, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99]


def main():
    df = pd.read_csv(DATA)
    assert len(df) == 284807 and int(df.Class.sum()) == 492
    df = df.sort_values("Time", kind="stable").reset_index(drop=True)
    df["hour"] = (df.Time // 3600) % 24
    n = len(df)
    train, valid, test = df.iloc[:int(n*.6)], df.iloc[int(n*.6):int(n*.8)], df.iloc[int(n*.8):]
    model = HistGradientBoostingClassifier(
        learning_rate=.05, max_iter=300, max_leaf_nodes=15,
        l2_regularization=1.0, early_stopping=False, random_state=42,
    )
    model.fit(train[FEATURES], train.Class)
    val_scores = model.predict_proba(valid[FEATURES])[:, 1]
    thresholds = [t for t in THRESHOLDS if (val_scores >= t).sum() and
                  ((val_scores >= t) & (valid.Class.to_numpy() == 1)).sum() /
                  (val_scores >= t).sum() >= .8]
    if not thresholds:
        raise RuntimeError("No validation threshold meets 80% precision")
    threshold = min(thresholds)
    scores = model.predict_proba(test[FEATURES])[:, 1]
    alerts = scores >= threshold
    caught = int((alerts & (test.Class.to_numpy() == 1)).sum())
    metrics = {"alerts": int(alerts.sum()), "frauds_caught": caught,
               "precision": caught / max(int(alerts.sum()), 1),
               "recall": caught / int(test.Class.sum()),
               "average_precision": float(average_precision_score(test.Class, scores))}
    info = {
        "model_version": "1.0.0", "scikit_learn_version": sklearn.__version__,
        "features": FEATURES, "threshold": threshold,
        "typical_values": {name: float(v) for name, v in
                           train.loc[train.Class == 0, FEATURES].median().items()},
        "data": {"rows": n, "frauds": int(df.Class.sum()),
                 "train_rows": len(train), "valid_rows": len(valid), "test_rows": len(test),
                 "test_frauds": int(test.Class.sum())},
        "test_metrics": metrics,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUT / "fraud_model.joblib")
    (OUT / "model_info.json").write_text(json.dumps(info, indent=2))
    print(json.dumps({"threshold": threshold, "test": metrics}, indent=2))


if __name__ == "__main__":
    main()
