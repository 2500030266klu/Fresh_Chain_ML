"""
src/dataset_analyzer.py
------------------------
Pure, authentic statistical analysis and strict validation engine for produce
cold-chain telemetry datasets. Computes exact distributions, physical psychrometrics,
correlation matrices, and model performance on user-uploaded datasets.
"""

from typing import Dict, Any, Tuple, Optional
import io
import math
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from src.config import (
    DATA_PATH, NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET
)
from src.predictor import get_model_bundle, calculate_dew_point, calculate_vpd


# Canonical column mappings and aliases for tolerant matching
COLUMN_ALIASES = {
    "Fruit": ["fruit", "produce", "item", "fruit_name", "variety"],
    "Temp": ["temp", "temperature", "temp_c", "temperature_c", "temp (°c)", "temperature (°c)"],
    "Humidity (%)": ["humidity", "humidity (%)", "relative_humidity", "rh", "rh (%)", "humidity_pct"],
    "Light (Lux)": ["light", "light (lux)", "ambient_light", "lux", "light_lux", "illuminance"],
    "CO2 (ppm)": ["co2", "co2 (ppm)", "carbon_dioxide", "co2_ppm", "carbon_dioxide (ppm)"],
}

TARGET_ALIASES = ["class", "target", "label", "quality", "spoilage", "status", "condition"]


def normalize_and_validate_dataset(df: pd.DataFrame) -> Tuple[bool, str, Optional[pd.DataFrame]]:
    """
    Strict validation of uploaded dataset.
    Must contain valid produce cold-chain features. Rejects any non-matching dataset.
    """
    if df is None or df.empty:
        return False, "Uploaded dataset is empty or could not be parsed.", None

    if len(df) < 5:
        return False, "Dataset contains fewer than 5 records. Authentic analysis requires sufficient telemetry observations.", None

    # Map existing columns (case-insensitive check)
    col_map = {}
    lower_to_orig = {str(c).strip().lower(): c for c in df.columns}

    # Find matches for each canonical feature
    for canonical, aliases in COLUMN_ALIASES.items():
        matched = None
        # Check canonical first
        if canonical.lower() in lower_to_orig:
            matched = lower_to_orig[canonical.lower()]
        else:
            # Check aliases
            for alias in aliases:
                if alias.lower() in lower_to_orig:
                    matched = lower_to_orig[alias.lower()]
                    break
        if matched:
            col_map[matched] = canonical

    # Check for missing required features
    matched_canonicals = set(col_map.values())
    missing_required = set(COLUMN_ALIASES.keys()) - matched_canonicals
    if missing_required:
        return (
            False,
            f"Dataset Rejected: Invalid Cold-Chain Telemetry Schema. FreshIQ only accepts produce cold-chain datasets. "
            f"Missing required sensor feature(s): {', '.join(sorted(missing_required))}. "
            f"Required columns: Fruit, Temp, Humidity (%), Light (Lux), CO2 (ppm) [and optional Class].",
            None
        )

    # Check for target column
    target_matched = None
    if TARGET.lower() in lower_to_orig:
        target_matched = lower_to_orig[TARGET.lower()]
    else:
        for alias in TARGET_ALIASES:
            if alias.lower() in lower_to_orig:
                target_matched = lower_to_orig[alias.lower()]
                break
    if target_matched:
        col_map[target_matched] = TARGET

    # Rename to canonical
    clean_df = df.rename(columns=col_map)

    # Validate numeric sensor channels
    for num_col in NUMERIC_FEATURES:
        clean_df[num_col] = pd.to_numeric(clean_df[num_col], errors="coerce")
        # If more than 50% values are non-numeric, reject as invalid data
        if clean_df[num_col].isnull().mean() > 0.5:
            return (
                False,
                f"Dataset Rejected: Column '{num_col}' contains invalid non-numeric values. Must be numeric sensor readings.",
                None
            )

    # Fill any remaining minor sensor nulls with median to avoid downstream errors
    for num_col in NUMERIC_FEATURES:
        if clean_df[num_col].isnull().any():
            clean_df[num_col] = clean_df[num_col].fillna(clean_df[num_col].median())

    # Validate and standardize Fruit column
    clean_df["Fruit"] = clean_df["Fruit"].astype(str).str.strip().str.capitalize()
    if clean_df["Fruit"].nunique() < 1:
        return False, "Dataset Rejected: Fruit column contains no valid produce varietals.", None

    # Validate and standardize Class column if present
    if TARGET in clean_df.columns:
        # Standardize target values to 'Good' and 'Bad'
        def standardize_class(val):
            s = str(val).strip().lower()
            if s in ["good", "1", "1.0", "fresh", "acceptable", "pass"]:
                return "Good"
            elif s in ["bad", "0", "0.0", "spoiled", "spoil", "reject", "fail"]:
                return "Bad"
            return "Good" if "good" in s or "fresh" in s else "Bad"

        clean_df[TARGET] = clean_df[TARGET].apply(standardize_class)

    return True, "Dataset validated successfully.", clean_df


def compute_comprehensive_analysis(df: pd.DataFrame, source_name: str = "Default Cleaned Dataset") -> Dict[str, Any]:
    """
    Computes purely authentic, real, unhyped statistics, distributions,
    psychrometric physics, and model evaluations on the given DataFrame.
    """
    total_rows, total_cols = df.shape
    missing_vals = {col: int(df[col].isnull().sum()) for col in df.columns}
    duplicates = int(df.duplicated().sum())

    # Class distribution
    has_target = TARGET in df.columns
    class_counts = {}
    good_count = 0
    bad_count = 0
    freshness_rate = 0.0
    spoilage_rate = 0.0

    if has_target:
        counts = df[TARGET].value_counts().to_dict()
        class_counts = {str(k): int(v) for k, v in counts.items()}
        good_count = class_counts.get("Good", 0)
        bad_count = class_counts.get("Bad", 0)
        total = good_count + bad_count
        if total > 0:
            freshness_rate = round((good_count / total) * 100, 2)
            spoilage_rate = round((bad_count / total) * 100, 2)

    # Fruit distribution & Cross-tabulation
    fruit_counts = {str(k): int(v) for k, v in df["Fruit"].value_counts().to_dict().items()}
    fruit_class_matrix = {}
    if has_target:
        crosstab = pd.crosstab(df["Fruit"], df[TARGET])
        for fruit in crosstab.index:
            g = int(crosstab.loc[fruit, "Good"]) if "Good" in crosstab.columns else 0
            b = int(crosstab.loc[fruit, "Bad"]) if "Bad" in crosstab.columns else 0
            tot = g + b
            s_rate = round((b / tot) * 100, 2) if tot > 0 else 0.0
            fruit_class_matrix[fruit] = {
                "Good": g,
                "Bad": b,
                "Total": tot,
                "SpoilageRate": s_rate
            }
    else:
        for fruit, cnt in fruit_counts.items():
            fruit_class_matrix[fruit] = {"Good": 0, "Bad": 0, "Total": cnt, "SpoilageRate": 0.0}

    # Descriptive Statistics & Histograms for Numeric Channels
    numeric_stats = {}
    histograms = {}

    for col in NUMERIC_FEATURES:
        series = df[col].dropna()
        if len(series) > 0:
            mean_val = float(series.mean())
            std_val = float(series.std()) if len(series) > 1 else 0.0
            min_val = float(series.min())
            p25_val = float(series.quantile(0.25))
            med_val = float(series.median())
            p75_val = float(series.quantile(0.75))
            max_val = float(series.max())

            numeric_stats[col] = {
                "mean": round(mean_val, 2),
                "std": round(std_val, 2),
                "min": round(min_val, 2),
                "p25": round(p25_val, 2),
                "median": round(med_val, 2),
                "p75": round(p75_val, 2),
                "max": round(max_val, 2),
            }

            # Generate exact 10-bin histogram
            counts, bin_edges = np.histogram(series, bins=10)
            histograms[col] = {
                "bins": [round(float(b), 1) for b in bin_edges[:-1]],
                "labels": [f"{round(float(bin_edges[i]), 1)}-{round(float(bin_edges[i+1]), 1)}" for i in range(len(counts))],
                "counts": [int(c) for c in counts]
            }

    # Psychrometric Calculations (Dew Point & VPD) computed row-by-row
    dew_points = []
    vpds = []
    for _, row in df.iterrows():
        t = float(row["Temp"])
        rh = float(row["Humidity (%)"])
        dp = calculate_dew_point(t, rh)
        vpd = calculate_vpd(t, rh)
        dew_points.append(dp)
        vpds.append(vpd)

    df_calc = df.copy()
    df_calc["DewPoint"] = dew_points
    df_calc["VPD"] = vpds

    # Dew Point and VPD summaries
    dp_series = pd.Series(dew_points)
    vpd_series = pd.Series(vpds)

    physics_stats = {
        "dew_point": {
            "mean": round(float(dp_series.mean()), 2),
            "min": round(float(dp_series.min()), 2),
            "max": round(float(dp_series.max()), 2),
        },
        "vpd": {
            "mean": round(float(vpd_series.mean()), 3),
            "min": round(float(vpd_series.min()), 3),
            "max": round(float(vpd_series.max()), 3),
            "condensation_risk_count": int((df_calc["Temp"] - df_calc["DewPoint"] <= 1.0).sum()),
            "excess_transpiration_count": int((df_calc["VPD"] > 0.45).sum())
        }
    }

    # Pearson Correlation Matrix across all numeric channels including Dew Point & VPD
    corr_cols = NUMERIC_FEATURES + ["DewPoint", "VPD"]
    corr_df = df_calc[corr_cols].corr().round(3)
    correlation_matrix = corr_df.to_dict()

    # Means by Spoilage Class
    means_by_class = {}
    if has_target:
        class_grp = df_calc.groupby(TARGET)[corr_cols].mean().round(2)
        means_by_class = class_grp.to_dict()

    # Anomaly Detection via Isolation Forest
    iso_anomalies_count = 0
    try:
        X_iso = df[NUMERIC_FEATURES].values
        if len(X_iso) >= 10:
            iso = IsolationForest(contamination=0.015, random_state=42)
            preds = iso.fit_predict(X_iso)
            iso_anomalies_count = int((preds == -1).sum())
    except Exception:
        pass

    # Model Evaluation on the Uploaded Dataset
    model_eval = {
        "evaluated": False,
        "champion_name": "Random Forest",
        "accuracy": None,
        "precision": None,
        "recall": None,
        "f1": None,
        "confusion_matrix": None
    }

    try:
        bundle = get_model_bundle()
        pipeline = bundle["pipeline"]
        le = bundle["label_encoder"]
        model_name = bundle.get("model_name", "Random Forest")
        model_eval["champion_name"] = model_name

        if has_target:
            # Evaluate model against the uploaded ground truth
            X_eval = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
            y_eval_raw = df[TARGET].values
            y_eval = le.transform(y_eval_raw)

            y_pred = pipeline.predict(X_eval)
            acc = float(accuracy_score(y_eval, y_pred))
            prec = float(precision_score(y_eval, y_pred, average="weighted", zero_division=0))
            rec = float(recall_score(y_eval, y_pred, average="weighted", zero_division=0))
            f1 = float(f1_score(y_eval, y_pred, average="weighted", zero_division=0))
            cm = confusion_matrix(y_eval, y_pred).tolist()

            model_eval = {
                "evaluated": True,
                "champion_name": model_name,
                "accuracy": round(acc * 100, 2),
                "precision": round(prec * 100, 2),
                "recall": round(rec * 100, 2),
                "f1": round(f1 * 100, 2),
                "confusion_matrix": cm,
                "classes": list(le.classes_)
            }
        else:
            # Predict unlabelled dataset
            X_eval = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
            y_pred = pipeline.predict(X_eval)
            pred_labels = le.inverse_transform(y_pred)
            good_pred = int((pred_labels == "Good").sum())
            bad_pred = int((pred_labels == "Bad").sum())
            fresh_pct = round((good_pred / len(pred_labels)) * 100, 2) if len(pred_labels) > 0 else 0.0

            # Update class metrics to predicted
            has_target = True
            class_counts = {"Good": good_pred, "Bad": bad_pred}
            freshness_rate = fresh_pct
            spoilage_rate = round(100.0 - fresh_pct, 2)
            model_eval = {
                "evaluated": True,
                "is_predicted": True,
                "champion_name": model_name,
                "predicted_fresh_count": good_pred,
                "predicted_spoil_count": bad_pred,
                "predicted_freshness_rate": fresh_pct
            }
    except Exception as e:
        model_eval["error"] = str(e)

    # Sample bivariate scatter points (max 150 points for responsive rendering)
    scatter_df = df_calc.sample(n=min(150, len(df_calc)), random_state=42)
    scatter_points = []
    for _, r in scatter_df.iterrows():
        scatter_points.append({
            "temp": round(float(r["Temp"]), 2),
            "co2": round(float(r["CO2 (ppm)"]), 1),
            "humidity": round(float(r["Humidity (%)"]), 1),
            "light": round(float(r["Light (Lux)"]), 2),
            "fruit": str(r["Fruit"]),
            "class": str(r[TARGET]) if TARGET in r else "Good"
        })

    # Preview rows (first 25 rows)
    preview_rows = df.head(25).to_dict(orient="records")

    return {
        "success": True,
        "source_name": source_name,
        "total_rows": total_rows,
        "total_cols": total_cols,
        "columns": list(df.columns),
        "missing_values": missing_vals,
        "duplicate_rows": duplicates,
        "has_target": has_target,
        "class_counts": class_counts,
        "freshness_rate": freshness_rate,
        "spoilage_rate": spoilage_rate,
        "fruit_counts": fruit_counts,
        "fruit_class_matrix": fruit_class_matrix,
        "numeric_stats": numeric_stats,
        "histograms": histograms,
        "physics_stats": physics_stats,
        "correlation_matrix": correlation_matrix,
        "means_by_class": means_by_class,
        "iso_anomalies_count": iso_anomalies_count,
        "model_eval": model_eval,
        "scatter_points": scatter_points,
        "preview_rows": preview_rows
    }
