"""
src/visualizer.py
------------------
Static high-resolution plot generation and dynamic web chart payload formatting.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score

from src.config import OUTPUT_DIR, NUMERIC_FEATURES, CATEGORICAL_FEATURES


def setup_plotting_theme():
    """Apply unified styling for generated figures."""
    sns.set_theme(style="whitegrid", palette="Set2")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.autolayout": True,
    })


def generate_all_eda_plots(df: pd.DataFrame, output_dir: Optional[Path] = None) -> list:
    """
    Generates and saves the 7 Exploratory Data Analysis plots.
    Returns list of saved file names.
    """
    out_dir = Path(output_dir or OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    setup_plotting_theme()
    saved_files = []

    # 1. Class balance
    plt.figure(figsize=(5, 4))
    ax = sns.countplot(data=df, x="Class", order=["Good", "Bad"], hue="Class", palette=["#10b981", "#ef4444"], legend=False)
    plt.title("Target Class Balance (Good vs Bad)")
    plt.xlabel("Class")
    plt.ylabel("Sample Count")
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                    ha="center", va="center", color="white", fontweight="bold", fontsize=11)
    file1 = out_dir / "01_class_balance.png"
    plt.savefig(file1, dpi=150)
    plt.close()
    saved_files.append("01_class_balance.png")

    # 2. Fruit balance
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(data=df, x="Fruit", order=df["Fruit"].value_counts().index, hue="Fruit", palette="Blues_r", legend=False)
    plt.title("Fruit Variety Distribution")
    plt.xlabel("Fruit Type")
    plt.ylabel("Sample Count")
    file2 = out_dir / "02_fruit_balance.png"
    plt.savefig(file2, dpi=150)
    plt.close()
    saved_files.append("02_fruit_balance.png")

    # 3. Fruit vs Class
    plt.figure(figsize=(7, 4))
    sns.countplot(data=df, x="Fruit", hue="Class", hue_order=["Good", "Bad"], palette=["#10b981", "#ef4444"])
    plt.title("Produce Freshness by Fruit Variety")
    plt.xlabel("Fruit Type")
    plt.ylabel("Count")
    plt.legend(title="Condition")
    file3 = out_dir / "03_fruit_vs_class.png"
    plt.savefig(file3, dpi=150)
    plt.close()
    saved_files.append("03_fruit_vs_class.png")

    # 4. Feature histograms
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for ax, col in zip(axes.flat, NUMERIC_FEATURES):
        sns.histplot(data=df, x=col, hue="Class", hue_order=["Good", "Bad"],
                     kde=True, ax=ax, element="step", palette=["#10b981", "#ef4444"])
        ax.set_title(f"{col} Distribution")
    file4 = out_dir / "04_feature_distributions.png"
    plt.savefig(file4, dpi=150)
    plt.close()
    saved_files.append("04_feature_distributions.png")

    # 5. Boxplots by class
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for ax, col in zip(axes.flat, NUMERIC_FEATURES):
        sns.boxplot(data=df, x="Class", y=col, order=["Good", "Bad"], hue="Class", ax=ax, palette=["#10b981", "#ef4444"], legend=False)
        ax.set_title(f"{col} Spread by Quality Class")
    file5 = out_dir / "05_boxplots_by_class.png"
    plt.savefig(file5, dpi=150)
    plt.close()
    saved_files.append("05_boxplots_by_class.png")

    # 6. Correlation heatmap
    plt.figure(figsize=(6, 5))
    corr = df[NUMERIC_FEATURES].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", linewidths=0.5)
    plt.title("Sensor Features Correlation Matrix")
    file6 = out_dir / "06_correlation_heatmap.png"
    plt.savefig(file6, dpi=150)
    plt.close()
    saved_files.append("06_correlation_heatmap.png")

    # 7. Pairplot
    pair = sns.pairplot(df, vars=NUMERIC_FEATURES, hue="Class", hue_order=["Good", "Bad"],
                        palette=["#10b981", "#ef4444"], diag_kind="kde",
                        plot_kws={"alpha": 0.5, "s": 15})
    file7 = out_dir / "07_pairplot.png"
    pair.savefig(file7, dpi=130)
    plt.close()
    saved_files.append("07_pairplot.png")

    return saved_files


def generate_model_evaluation_plots(
    best_name: str,
    pipeline: Any,
    label_encoder: Any,
    X_test: pd.DataFrame,
    y_test: np.ndarray,
    output_dir: Optional[Path] = None,
    all_pipelines: Optional[Dict[str, Any]] = None,
    cv_scores_dict: Optional[Dict[str, list]] = None,
    results_df: Optional[pd.DataFrame] = None
) -> list:
    """
    Generates comprehensive evaluation visualizations for all evaluated models:
    - Individual confusion matrices for every model
    - Multi-model ROC comparison curve
    - Multi-model Precision-Recall comparison curve
    - Multi-model metrics bar comparison
    - 5-fold cross validation stability boxplot
    - Best model artifacts (backward compatibility)
    """
    out_dir = Path(output_dir or OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    setup_plotting_theme()
    saved_files = []

    pipelines = all_pipelines or {best_name: pipeline}
    model_colors = {
        "Random Forest": "#10b981",
        "Decision Tree": "#06b6d4",
        "SVM (RBF)": "#8b5cf6",
        "KNN": "#f59e0b",
        "Logistic Regression": "#ef4444"
    }

    # 1. Individual Confusion Matrix for every model
    for name, pipe in pipelines.items():
        slug = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        y_pred = pipe.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
        plt.xlabel("Predicted Class")
        plt.ylabel("Actual Class")
        plt.title(f"Confusion Matrix — {name}")
        fname = f"eval_cm_{slug}.png"
        fpath = out_dir / fname
        plt.savefig(fpath, dpi=150)
        plt.close()
        saved_files.append(fname)

        if name == best_name:
            # Also save legacy best model file
            plt.figure(figsize=(5, 4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
            plt.xlabel("Predicted Class")
            plt.ylabel("Actual Class")
            plt.title(f"Confusion Matrix — {best_name}")
            plt.savefig(out_dir / "08_confusion_matrix_best_model.png", dpi=150)
            plt.close()
            saved_files.append("08_confusion_matrix_best_model.png")

    # 2. Multi-Model ROC Comparison Curve (All models on one high-res chart)
    plt.figure(figsize=(7, 5))
    has_any_roc = False
    for name, pipe in pipelines.items():
        if hasattr(pipe, "predict_proba"):
            y_proba = pipe.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            auc = roc_auc_score(y_test, y_proba)
            c = model_colors.get(name, "#6366f1")
            plt.plot(fpr, tpr, color=c, lw=2, label=f"{name} (AUC = {auc:.3f})")
            has_any_roc = True
        elif hasattr(pipe, "decision_function"):
            y_score = pipe.decision_function(X_test)
            fpr, tpr, _ = roc_curve(y_test, y_score)
            auc = roc_auc_score(y_test, y_score)
            c = model_colors.get(name, "#6366f1")
            plt.plot(fpr, tpr, color=c, lw=2, label=f"{name} (AUC = {auc:.3f})")
            has_any_roc = True

    if has_any_roc:
        plt.plot([0, 1], [0, 1], linestyle="--", color="grey", label="Random Classifier (0.50)")
        plt.xlabel("False Positive Rate (1 - Specificity)")
        plt.ylabel("True Positive Rate (Sensitivity)")
        plt.title("Multi-Model ROC Comparison — All 5 Architectures")
        plt.legend(loc="lower right", fontsize=9)
        plt.tight_layout()
        roc_file = out_dir / "eval_multi_roc_curves.png"
        plt.savefig(roc_file, dpi=150)
        plt.close()
        saved_files.append("eval_multi_roc_curves.png")

        # Also save legacy best model file
        best_pipe = pipelines.get(best_name, pipeline)
        if hasattr(best_pipe, "predict_proba"):
            y_proba_best = best_pipe.predict_proba(X_test)[:, 1]
            fpr_b, tpr_b, _ = roc_curve(y_test, y_proba_best)
            auc_b = roc_auc_score(y_test, y_proba_best)
            plt.figure(figsize=(5, 4))
            plt.plot(fpr_b, tpr_b, color="#6366f1", lw=2, label=f"{best_name} (AUC = {auc_b:.3f})")
            plt.plot([0, 1], [0, 1], linestyle="--", color="grey")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("Receiver Operating Characteristic (ROC)")
            plt.legend(loc="lower right")
            plt.tight_layout()
            plt.savefig(out_dir / "09_roc_curve_best_model.png", dpi=150)
            plt.close()
            saved_files.append("09_roc_curve_best_model.png")

    # 3. Multi-Model Metrics Bar Chart (Accuracy, Precision, Recall, F1)
    if results_df is not None and not results_df.empty:
        plt.figure(figsize=(9, 5))
        plot_df = results_df[["Model", "Accuracy", "Precision", "Recall", "F1"]].melt(
            id_vars="Model", var_name="Metric", value_name="Score"
        )
        ax = sns.barplot(data=plot_df, x="Model", y="Score", hue="Metric", palette="Set2")
        plt.title("Comparative Performance Across Key Metrics")
        plt.xlabel("Model Architecture")
        plt.ylabel("Score (0.0 to 1.0)")
        plt.ylim(0.85, 1.02)
        plt.xticks(rotation=15)
        plt.legend(loc="lower right", framealpha=0.9)
        plt.tight_layout()
        bar_file = out_dir / "eval_metrics_comparison_bar.png"
        plt.savefig(bar_file, dpi=150)
        plt.close()
        saved_files.append("eval_metrics_comparison_bar.png")

    # 4. 5-Fold Cross Validation Fold Stability Boxplot
    if cv_scores_dict:
        plt.figure(figsize=(8, 4.5))
        cv_data = []
        for model_k, scores in cv_scores_dict.items():
            for s in scores:
                cv_data.append({"Model": model_k, "CV Accuracy": s})
        cv_df = pd.DataFrame(cv_data)

        sns.boxplot(data=cv_df, x="Model", y="CV Accuracy", hue="Model", palette="Set2", legend=False)
        sns.stripplot(data=cv_df, x="Model", y="CV Accuracy", color="black", size=6, jitter=0.1, alpha=0.6)
        plt.title("5-Fold Cross Validation Stability & Variance")
        plt.xlabel("Model Architecture")
        plt.ylabel("CV Fold Accuracy")
        plt.xticks(rotation=15)
        plt.tight_layout()
        cv_file = out_dir / "eval_cv_boxplots.png"
        plt.savefig(cv_file, dpi=150)
        plt.close()
        saved_files.append("eval_cv_boxplots.png")

    # 5. Feature Importance (for trees)
    best_pipe = pipelines.get(best_name, pipeline)
    model_step = best_pipe.named_steps["model"]
    if hasattr(model_step, "feature_importances_"):
        cat_encoder = best_pipe.named_steps["preprocess"].named_transformers_["cat"]
        cat_features = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
        all_features = NUMERIC_FEATURES + cat_features
        importances = model_step.feature_importances_

        imp_df = pd.DataFrame({"feature": all_features, "importance": importances}) \
            .sort_values("importance", ascending=True)

        plt.figure(figsize=(7, 5))
        plt.barh(imp_df["feature"], imp_df["importance"], color="#3b82f6")
        plt.xlabel("Relative Importance Score")
        plt.title(f"Feature Importance — {best_name}")
        plt.tight_layout()
        file10 = out_dir / "10_feature_importance.png"
        plt.savefig(file10, dpi=150)
        plt.close()
        saved_files.append("10_feature_importance.png")

    return saved_files
