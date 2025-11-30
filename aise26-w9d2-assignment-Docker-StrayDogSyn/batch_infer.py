import sys
import time
import pandas as pd
from models.train import ensure_model

def main():
    if len(sys.argv) != 3:
        print("Usage: python batch_infer.py <input_csv> <output_csv>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    start = time.perf_counter()
    model = ensure_model("models/baseline.joblib")
    df = pd.read_csv(input_path)
    scores = model.predict_proba(df[["x1", "x2"]].values)[:, 1]
    df["prediction"] = scores
    df.to_csv(output_path, index=False)
    elapsed = time.perf_counter() - start
    print(f"rows_processed={len(df)} time_seconds={elapsed:.4f}")

if __name__ == "__main__":
    main()