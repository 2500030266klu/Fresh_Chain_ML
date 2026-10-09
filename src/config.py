"""
src/config.py
--------------
Central configuration for dataset paths, ML parameters, produce profiles,
and sensor thresholds.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATA_PATH = DATA_DIR / "Dataset_cleaned.csv"
MODEL_PATH = OUTPUT_DIR / "best_model.joblib"
COMPARISON_CSV_PATH = OUTPUT_DIR / "model_comparison.csv"
METRICS_JSON_PATH = OUTPUT_DIR / "metrics_summary.json"
LIFECYCLE_JSON_PATH = OUTPUT_DIR / "lifecycle_summary.json"

# Ensure outputs directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ML Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

NUMERIC_FEATURES = ["Temp", "Humidity (%)", "Light (Lux)", "CO2 (ppm)"]
CATEGORICAL_FEATURES = ["Fruit"]
TARGET = "Class"
CLASS_NAMES = ["Bad", "Good"]  # Bad=0, Good=1

# Feature Bounds (derived from dataset statistics for input validation & sliders)
FEATURE_BOUNDS = {
    "Temp": {"min": 20.0, "max": 28.0, "default": 23.5, "step": 0.5, "unit": "°C"},
    "Humidity (%)": {"min": 85.0, "max": 98.0, "default": 93.0, "step": 1.0, "unit": "%"},
    "Light (Lux)": {"min": 3.0, "max": 26.0, "default": 11.5, "step": 0.1, "unit": "Lux"},
    "CO2 (ppm)": {"min": 150.0, "max": 500.0, "default": 320.0, "step": 5.0, "unit": "ppm"},
}

# Produce Specific Profiles & Optimal Storage Guidelines
FRUIT_PROFILES = {
    "Orange": {
        "icon": "🍊",
        "description": "Citrus fruit susceptible to penicillium decay and weight loss in elevated temperatures.",
        "optimal_temp": (21.0, 23.0),
        "optimal_humidity": (90.0, 94.0),
        "max_light": 10.0,
        "max_co2": 330.0,
        "baseline_shelf_life_days": 21,
        "primary_pathogen": "Penicillium digitatum (Green Mold)",
        "respiration_rate": "Low-Moderate (12 mg CO2/kg·h)",
        "target_vpd_range": (0.15, 0.38),
        "haccp_standard": "Codex Alimentarius CXC 44-1995 (Class I Citrus)",
        "storage_tip": "Keep in cool, darkened chambers with controlled ventilation to prevent skin degradation."
    },
    "Pineapple": {
        "icon": "🍍",
        "description": "Tropical fruit vulnerable to internal browning and rapid sugar fermentation under light.",
        "optimal_temp": (22.0, 24.0),
        "optimal_humidity": (91.0, 95.0),
        "max_light": 11.0,
        "max_co2": 340.0,
        "baseline_shelf_life_days": 14,
        "primary_pathogen": "Ceratocystis paradoxa (Black Rot)",
        "respiration_rate": "Moderate (18 mg CO2/kg·h)",
        "target_vpd_range": (0.12, 0.35),
        "haccp_standard": "UNECE FFV-49 Cold-Chain Specification",
        "storage_tip": "Avoid direct light exposure; preserve high relative humidity to maintain crown vitality."
    },
    "Banana": {
        "icon": "🍌",
        "description": "Climacteric fruit that releases ethylene, accelerating spoilage and CO2 generation rapidly.",
        "optimal_temp": (23.0, 25.0),
        "optimal_humidity": (88.0, 92.0),
        "max_light": 18.0,
        "max_co2": 350.0,
        "baseline_shelf_life_days": 8,
        "primary_pathogen": "Colletotrichum musae (Anthracnose)",
        "respiration_rate": "High Climacteric (45-85 mg CO2/kg·h)",
        "target_vpd_range": (0.20, 0.42),
        "haccp_standard": "FAO/WHO Produce Standard 130-1981",
        "storage_tip": "Ensure continuous air flow to dispel accumulated ethylene and CO2 pockets."
    },
    "Tomato": {
        "icon": "🍅",
        "description": "Perishable produce prone to fungal rots and softening under excess moisture and warmth.",
        "optimal_temp": (22.0, 24.0),
        "optimal_humidity": (90.0, 93.0),
        "max_light": 12.0,
        "max_co2": 360.0,
        "baseline_shelf_life_days": 12,
        "primary_pathogen": "Botrytis cinerea (Grey Mold)",
        "respiration_rate": "Moderate-High (24 mg CO2/kg·h)",
        "target_vpd_range": (0.16, 0.40),
        "haccp_standard": "USDA Cold Handling Grade 1 Fresh",
        "storage_tip": "Maintain moderate light levels and prevent temperature spikes above 25°C."
    }
}

# Quick Test Presets for Instant UI Demonstrations
PRESETS = [
    {
        "id": "fresh_orange_cold",
        "label": "Optimal Cold Storage (Orange)",
        "badge": "Fresh Presumed",
        "fruit": "Orange",
        "temp": 22.0,
        "humidity": 94.0,
        "light": 6.8,
        "co2": 280.0,
        "description": "Ideal cold room conditions with low light and controlled CO2 levels."
    },
    {
        "id": "spoil_orange_ambient",
        "label": "Overheated Chamber (Orange)",
        "badge": "Spoil Alert",
        "fruit": "Orange",
        "temp": 25.0,
        "humidity": 95.0,
        "light": 16.5,
        "co2": 395.0,
        "description": "High temperature and strong light triggering rapid fruit rot."
    },
    {
        "id": "fresh_banana_optimal",
        "label": "Balanced Humidity (Banana)",
        "badge": "Fresh Presumed",
        "fruit": "Banana",
        "temp": 24.0,
        "humidity": 90.0,
        "light": 19.5,
        "co2": 305.0,
        "description": "Standard controlled ripening condition with active air turnover."
    },
    {
        "id": "spoil_tomato_ferment",
        "label": "High CO2 Fermentation (Tomato)",
        "badge": "Spoil Alert",
        "fruit": "Tomato",
        "temp": 25.5,
        "humidity": 95.0,
        "light": 15.2,
        "co2": 420.0,
        "description": "Accumulated respiratory gases indicating advanced tissue breakdown."
    }
]
