"""
app/routes.py
--------------
Application routes and REST endpoints for UI navigation and model interactions.
"""

import os
import json
import io
from flask import (
    Blueprint, render_template, request, jsonify,
    send_file, current_app, Response, send_from_directory
)
import pandas as pd

from src.config import (
    OUTPUT_DIR, FEATURE_BOUNDS, FRUIT_PROFILES,
    PRESETS, METRICS_JSON_PATH, COMPARISON_CSV_PATH,
    LIFECYCLE_JSON_PATH
)
from src.data_loader import get_dataset_summary, get_preview_rows, load_data
from src.predictor import predict_single, predict_batch, get_model_bundle
from src.trainer import train_and_evaluate_all
from src.dataset_analyzer import normalize_and_validate_dataset, compute_comprehensive_analysis

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Real-Time Freshness & Spoilage Predictor Dashboard."""
    # Ensure model is ready
    bundle = get_model_bundle()
    model_name = bundle.get("model_name", "Random Forest")
    metrics = bundle.get("metrics", {})

    return render_template(
        "index.html",
        page_title="Real-Time Spoilage Intelligence",
        active_page="predictor",
        feature_bounds=FEATURE_BOUNDS,
        fruit_profiles=FRUIT_PROFILES,
        presets=PRESETS,
        best_model_name=model_name,
        best_f1=round(metrics.get("F1", 0.99) * 100, 2),
        best_acc=round(metrics.get("Accuracy", 0.99) * 100, 2),
    )


@main_bp.route("/eda")
def eda():
    """Dataset Exploratory Data Analysis & Visualizations."""
    df = load_data()
    analysis = compute_comprehensive_analysis(df, source_name="Default: Dataset_cleaned.csv")
    summary = get_dataset_summary(df)
    preview = get_preview_rows(df, limit=25)

    # Collect available generated plots in outputs/
    plot_names = [
        ("01_class_balance.png", "Target Class Balance", "Distribution of Good vs Bad produce samples in the dataset."),
        ("02_fruit_balance.png", "Fruit Variety Distribution", "Number of sensor log observations recorded for each produce type."),
        ("03_fruit_vs_class.png", "Fruit Quality vs Spoilage", "Proportion of Fresh vs Spoiled samples per fruit category."),
        ("04_feature_distributions.png", "Sensor Feature Distributions", "Histogram & KDE curves for Temp, Humidity, Light, and CO2."),
        ("05_boxplots_by_class.png", "Boxplots by Spoilage Class", "Spread, medians, and quartile outliers across Good and Bad states."),
        ("06_correlation_heatmap.png", "Feature Correlation Heatmap", "Pearson correlation matrix across all numeric sensor readings."),
        ("07_pairplot.png", "Multivariate Pairplot", "Bivariate scatter and density plots colored by Freshness label.")
    ]

    available_plots = []
    for filename, title, desc in plot_names:
        filepath = OUTPUT_DIR / filename
        available_plots.append({
            "filename": filename,
            "title": title,
            "description": desc,
            "exists": filepath.exists()
        })

    return render_template(
        "eda.html",
        page_title="Dataset & Sensor Analytics",
        active_page="eda",
        analysis=analysis,
        summary=summary,
        preview_rows=preview,
        plots=available_plots
    )


@main_bp.route("/models")
def models():
    """Model Comparison, Evaluation Metrics & Leaderboard."""
    # Read metrics summary or trigger training if not yet created
    if not METRICS_JSON_PATH.exists():
        train_and_evaluate_all()

    with open(METRICS_JSON_PATH, "r") as f:
        metrics_data = json.load(f)

    eval_plots = [
        ("eval_multi_roc_curves.png", "Multi-Model ROC Comparison", "Overlaid ROC curves comparing True Positive vs False Positive rates for all 8 algorithms."),
        ("eval_metrics_comparison_bar.png", "All-Model Metrics Benchmark", "Grouped comparison across Accuracy, Precision, Recall, and F1-score across all 8 architectures."),
        ("eval_cv_boxplots.png", "5-Fold Cross-Validation Stability", "Fold accuracy variance and dispersion distributions for every architecture."),
        ("10_feature_importance.png", "Feature Importance Ranking", "Sensor readings and fruit features ranked by diagnostic contribution."),
        ("eval_cm_random_forest.png", "Random Forest Confusion Matrix", "Classification confusion matrix for the Random Forest ensemble."),
        ("eval_cm_decision_tree.png", "Decision Tree Confusion Matrix", "True vs Predicted performance matrix for Decision Tree."),
        ("eval_cm_knn.png", "KNN Confusion Matrix", "K-Nearest Neighbors classification matrix on test sensor readings."),
        ("eval_cm_gradient_boosting.png", "Gradient Boosting Confusion Matrix", "Sequential residual tree boosting classification matrix."),
        ("eval_cm_svm_rbf.png", "SVM (RBF) Confusion Matrix", "Support Vector Classifier with Radial Basis Function kernel performance."),
        ("eval_cm_adaboost.png", "AdaBoost Confusion Matrix", "Adaptive boosting stump re-weighting matrix."),
        ("eval_cm_logistic_regression.png", "Logistic Regression Confusion Matrix", "Generalized linear baseline model confusion matrix."),
        ("eval_cm_ridge_classifier.png", "Ridge Classifier Confusion Matrix", "L2-regularized closed-form normal equations classifier.")
    ]

    available_eval_plots = []
    for filename, title, desc in eval_plots:
        filepath = OUTPUT_DIR / filename
        available_eval_plots.append({
            "filename": filename,
            "title": title,
            "description": desc,
            "exists": filepath.exists()
        })

    return render_template(
        "models.html",
        page_title="Model Benchmark Suite",
        active_page="models",
        metrics_data=metrics_data,
        models_detail=metrics_data.get("models_detail", {}),
        eval_plots=available_eval_plots
    )


@main_bp.route("/batch")
def batch():
    """Batch CSV Upload & Multi-Sample Inference."""
    return render_template(
        "batch.html",
        page_title="Batch Produce Inference",
        active_page="batch"
    )


@main_bp.route("/lifecycle")
def lifecycle():
    """The System Lifecycle Comprehensive Dashboard."""
    if not LIFECYCLE_JSON_PATH.exists():
        from src.trainer import compute_lifecycle_analytics
        compute_lifecycle_analytics()

    with open(LIFECYCLE_JSON_PATH, "r") as f:
        lifecycle_data = json.load(f)

    return render_template(
        "lifecycle.html",
        page_title="Lifecycle",
        active_page="lifecycle",
        lifecycle=lifecycle_data
    )


@main_bp.route("/api/lifecycle", methods=["GET"])
def api_lifecycle():
    """Returns lifecycle analytics and metrics as JSON."""
    if not LIFECYCLE_JSON_PATH.exists():
        from src.trainer import compute_lifecycle_analytics
        compute_lifecycle_analytics()

    with open(LIFECYCLE_JSON_PATH, "r") as f:
        data = json.load(f)
    return jsonify({"success": True, "data": data})


# ----------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------

@main_bp.route("/api/predict", methods=["POST"])
def api_predict():
    """Real-time JSON prediction API."""
    data = request.get_json(silent=True) or request.form
    try:
        temp = float(data.get("temp", 24.0))
        humidity = float(data.get("humidity", 93.0))
        light = float(data.get("light", 12.0))
        co2 = float(data.get("co2", 330.0))
        fruit = str(data.get("fruit", "Orange"))

        result = predict_single(temp, humidity, light, co2, fruit)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@main_bp.route("/api/batch-predict", methods=["POST"])
def api_batch_predict():
    """CSV Batch Prediction API."""
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No CSV file uploaded."}), 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"success": False, "error": "Only .csv files are supported."}), 400

    try:
        content = file.read()
        batch_result = predict_batch(content)
        # We don't send the full raw CSV in the JSON response, only the preview and stats
        return jsonify({
            "success": True,
            "total_records": batch_result["total_records"],
            "good_count": batch_result["good_count"],
            "bad_count": batch_result["bad_count"],
            "freshness_rate": batch_result["freshness_rate"],
            "avg_confidence": batch_result["avg_confidence"],
            "preview_data": batch_result["preview_data"],
            "csv_content": batch_result["csv_content"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@main_bp.route("/api/upload-dataset", methods=["POST"])
def api_upload_dataset():
    """Strictly validates uploaded dataset and computes real, unhyped analytics."""
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."}), 400

    file = request.files["file"]
    if not file.filename.lower().endswith(".csv"):
        return jsonify({
            "success": False,
            "error": "Dataset Rejected: Only CSV (.csv) produce cold-chain telemetry files are accepted."
        }), 400

    try:
        content = file.read()
        if not content or len(content.strip()) == 0:
            return jsonify({"success": False, "error": "Dataset Rejected: The uploaded CSV file is empty."}), 400

        df = pd.read_csv(io.BytesIO(content))
        is_valid, err_msg, clean_df = normalize_and_validate_dataset(df)
        if not is_valid:
            return jsonify({"success": False, "error": err_msg}), 400

        analysis = compute_comprehensive_analysis(clean_df, source_name=file.filename)
        return jsonify({
            "success": True,
            "analysis": analysis,
            "message": f"Verified authentic telemetry dataset. Analyzed {clean_df.shape[0]} observations across {clean_df['Fruit'].nunique()} produce varieties."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Dataset Rejected: Error parsing CSV telemetry file: {str(e)}"
        }), 400


@main_bp.route("/api/default-dataset", methods=["GET"])
def api_default_dataset():
    """Returns authentic comprehensive analytics for the default dataset."""
    try:
        df = load_data()
        analysis = compute_comprehensive_analysis(df, source_name="Default: Dataset_cleaned.csv (6,953 rows)")
        return jsonify({"success": True, "analysis": analysis})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route("/api/sample-csv", methods=["GET"])
def api_sample_csv():
    """Download a template CSV for testing batch predictions."""
    df = load_data()
    sample_df = df.sample(n=15, random_state=101)[["Fruit", "Temp", "Humidity (%)", "Light (Lux)", "CO2 (ppm)"]]
    
    buf = io.BytesIO()
    sample_df.to_csv(buf, index=False)
    buf.seek(0)

    return send_file(
        buf,
        mimetype="text/csv",
        as_attachment=True,
        download_name="sample_sensor_batch.csv"
    )


@main_bp.route("/api/retrain", methods=["POST"])
def api_retrain():
    """Triggers model training and regenerates all charts."""
    try:
        _, summary = train_and_evaluate_all(generate_plots=True)
        # Force cache reload
        get_model_bundle(force_reload=True)
        return jsonify({"success": True, "message": "Models retrained successfully!", "summary": summary})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main_bp.route("/outputs/<path:filename>")
def serve_output_file(filename):
    """Serves generated plots and files from outputs/."""
    return send_from_directory(str(OUTPUT_DIR), filename)
