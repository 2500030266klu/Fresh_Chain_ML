"""
2_train_models.py
------------------
Supervised ML pipeline for Fruit & Vegetable Spoilage dataset:
preprocessing -> train/test split -> 5 models -> 5-fold CV -> evaluation ->
saves best model to disk -> runs example inference.

Refactored to systematically use the modular src package.
"""

import pandas as pd
from src.config import MODEL_PATH, OUTPUT_DIR
from src.trainer import train_and_evaluate_all
from src.predictor import predict_single


def main():
    print("=" * 70)
    print("EXECUTING FULL MACHINE LEARNING PIPELINE")
    print("=" * 70)

    results_df, summary = train_and_evaluate_all(generate_plots=True)

    print("\n" + "=" * 70)
    print("MODEL BENCHMARK RESULTS (sorted by F1-Score)")
    print("=" * 70)
    print(results_df.round(4).to_string(index=False))

    best_name = summary["best_model_name"]
    print("\n" + "=" * 70)
    print(f"CHAMPION MODEL SELECTED: {best_name}")
    print("=" * 70)
    best_m = summary["best_metrics"]
    print(f"  Test Accuracy : {best_m['Accuracy']:.4f}")
    print(f"  Test Precision: {best_m['Precision']:.4f}")
    print(f"  Test Recall   : {best_m['Recall']:.4f}")
    print(f"  Test F1-Score : {best_m['F1']:.4f}")
    print(f"  5-Fold CV Acc : {best_m['CV Accuracy (mean)']:.4f} +/- {best_m['CV Accuracy (std)']:.4f}")
    if best_m.get("ROC_AUC"):
        print(f"  ROC-AUC       : {best_m['ROC_AUC']:.4f}")

    print("\n" + "=" * 70)
    print(f"Artifacts saved to '{OUTPUT_DIR}/'")
    print(f"Best model bundle saved to: '{MODEL_PATH}'")
    print("=" * 70)

    # Example single prediction test
    print("\n" + "=" * 70)
    print("TESTING INFERENCE ENGINE ON NEW SAMPLE")
    print("=" * 70)
    test_sample = {
        "fruit": "Tomato",
        "temp": 25.0,
        "humidity": 90.0,
        "light": 14.2,
        "co2": 340.0
    }
    prediction_result = predict_single(**test_sample)
    print(f"Input sample: {test_sample}")
    print(f"Inferred Status: {prediction_result['status']} ({prediction_result['prediction']})")
    print(f"Confidence: {prediction_result['confidence']}%")
    print(f"Action Advice: {prediction_result['action_advice']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
