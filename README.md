# 🌿 FreshIQ — Fruit & Vegetable Spoilage Intelligence Platform

An end-to-end, production-grade Machine Learning and Environmental Telemetry system designed to predict produce spoilage and assess cold-chain storage safety. Built with a modular Python ML core (`src/`) and a modern, highly animated dark-glassmorphism Flask web platform (`app/`).

---

## 🌟 Key Highlights

- **99.7% Accuracy & F1-Score**: Evaluated across 5 supervised architectures (Random Forest, Decision Tree, SVM RBF, KNN, Logistic Regression) with 5-fold stratified cross-validation.
- **Microclimate Telemetry Simulation**: Real-time evaluation of Temperature (°C), Relative Humidity (%), Ambient Light (Lux), and Carbon Dioxide (CO2 ppm) across 4 perishable produce varieties (*Orange*, *Pineapple*, *Banana*, *Tomato*).
- **High-Throughput Batch Processing**: Drag-and-drop CSV batch inference engine with automatic column normalization and enriched CSV report export.
- **Dynamic Interactive Web Suite**: Animated SVG circular gauge, live diagnostics, storage protocol recommendations, interactive Chart.js visualizations, and model leaderboard.
- **RESTful API**: Clean JSON endpoints (`/api/predict`, `/api/batch-predict`, `/api/retrain`, `/api/sample-csv`) for edge integration.

---

## 🏗️ System Architecture

```
ML_Project/
├── data/
│   └── Dataset_cleaned.csv            # Cleaned sensor dataset (6,953 rows)
├── src/                               # Systematic ML Package
│   ├── __init__.py
│   ├── config.py                      # Global paths, bounds, presets, produce profiles
│   ├── data_loader.py                 # Data ingestion, schema validation & summary stats
│   ├── preprocessor.py                # StandardScaler + OneHotEncoder pipeline builder
│   ├── trainer.py                     # 5-Model training, 5-fold CV & benchmark exporter
│   ├── predictor.py                   # Real-time & batch inference service with caching
│   └── visualizer.py                  # High-res static plots & Chart.js payload generator
├── app/                               # Professional Flask Web Application
│   ├── __init__.py                    # Flask application factory
│   ├── routes.py                      # UI routes and REST API endpoints
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css              # Custom dark-glassmorphism design & animations
│   │   └── js/
│   │       └── app.js                 # Real-time reactivity, SVG gauge, batch upload & charts
│   └── templates/
│       ├── base.html                  # Responsive layout, nav header, particle glows
│       ├── index.html                 # Real-time Spoilage Simulator & Gauge Dashboard
│       ├── eda.html                   # Sensor Telemetry Profile & Figures Gallery
│       ├── models.html                # Model Leaderboard, Radar Chart & Diagnostics
│       └── batch.html                 # Drag-and-drop CSV batch predictor & exporter
├── outputs/                           # Generated models, benchmark CSVs and 10 plots
│   ├── best_model.joblib              # Serialized pipeline + label encoder bundle
│   ├── model_comparison.csv           # Benchmark comparison of all 5 algorithms
│   ├── metrics_summary.json           # Detailed metrics & classification report
│   └── *.png                          # 10 High-res statistical figures
├── 1_dataset_showcase.py              # CLI/PyCharm entrypoint for dataset exploration
├── 2_train_models.py                  # CLI/PyCharm entrypoint for training & evaluation
├── run_app.py                         # Web platform launcher (`python run_app.py`)
├── requirements.txt                   # Project dependencies
└── README.md                          # Documentation
```

---

## 🚀 Quick Start

### 1. Environment Setup

Clone or open the project folder in PyCharm or your terminal:

```bash
# Activate your virtual environment
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Web Application

Launch the Flask web server:

```bash
python run_app.py
```

Open your browser and navigate to:
- **Dashboard & Real-Time Predictor**: `http://127.0.0.1:5000/`
- **Exploratory Sensor Analytics**: `http://127.0.0.1:5000/eda`
- **Model Leaderboard & Radar**: `http://127.0.0.1:5000/models`
- **Batch CSV Classification**: `http://127.0.0.1:5000/batch`

### 3. Running Standalone ML Scripts (PyCharm or CLI)

Both standalone scripts have been refactored to systematically use the `src/` core:

- **Generate EDA Statistics & 7 Plots**:
  ```bash
  python 1_dataset_showcase.py
  ```
- **Train All 5 Models, Benchmark & Export Artifacts**:
  ```bash
  python 2_train_models.py
  ```

---

## 📊 Model Benchmark Results

Evaluated on an 80/20 stratified split with 5-fold stratified cross-validation on 6,953 sensor samples:

| Rank | Model Architecture | Accuracy | Precision | Recall | F1-Score | 5-Fold CV (Mean ± Std) | ROC-AUC |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Random Forest (Champion)** | **99.71%** | **99.87%** | **99.62%** | **99.74%** | **99.71% ± 0.09%** | **0.9999** |
| #2 | Decision Tree | 99.71% | 99.87% | 99.62% | 99.74% | 99.71% ± 0.09% | 0.9973 |
| #3 | K-Nearest Neighbors (KNN) | 99.71% | 99.87% | 99.62% | 99.74% | 99.71% ± 0.25% | 0.9972 |
| #4 | SVM (RBF Kernel) | 99.50% | 99.74% | 99.36% | 99.55% | 99.57% ± 0.25% | 0.9989 |
| #5 | Logistic Regression | 90.44% | 89.26% | 94.51% | 91.81% | 90.69% ± 0.44% | 0.9458 |

---

## 🔌 REST API Reference

### Real-Time Prediction: `POST /api/predict`
```json
// Request Payload:
{
  "temp": 24.5,
  "humidity": 93.0,
  "light": 12.5,
  "co2": 330.0,
  "fruit": "Orange"
}

// Response:
{
  "success": true,
  "data": {
    "status": "FRESH",
    "prediction": "Good",
    "confidence": 99.4,
    "probabilities": { "Good": 99.4, "Bad": 0.6 },
    "model_used": "Random Forest",
    "action_advice": "Produce assessed as FRESH & MARKETABLE...",
    "diagnostics": [...]
  }
}
```

### Batch CSV Inference: `POST /api/batch-predict`
Multipart form upload with field name `file`. Returns summary metrics, per-row predictions, and enriched CSV download content.

---

## 🛠️ Technology Stack

- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
- **Visualization**: Seaborn, Matplotlib, Chart.js
- **Web Backend**: Flask 3.1, Jinja2, Werkzeug
- **Frontend Architecture**: Bespoke CSS Design System, Dark Glassmorphism, Micro-Animations, Vanilla ES6+ JS
