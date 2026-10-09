"""
run_app.py
-----------
Entry point launcher for the Fruit & Vegetable Spoilage Intelligence Web Platform.
Includes automatic virtual environment forwarding if launched from global Python.
"""

import sys
import os
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ----------------------------------------------------------------------
# Auto-detect .venv and re-execute if dependencies are missing in global Python
# ----------------------------------------------------------------------
try:
    import flask
except ImportError:
    project_root = Path(__file__).resolve().parent
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists() and sys.executable.lower() != str(venv_python).lower():
        print(f"[*] Switching to project virtual environment: {venv_python}")
        import subprocess
        sys.exit(subprocess.call([str(venv_python)] + sys.argv))
    else:
        print("[!] Flask is not installed in the current Python environment.")
        print("    Please run: pip install -r requirements.txt")
        sys.exit(1)





from app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

    print("\n" + "=" * 70)
    print("FRESHIQ - FRUIT & VEGETABLE SPOILAGE INTELLIGENCE PLATFORM")
    print("=" * 70)
    print(f" * Server running on: http://{host}:{port}")
    print(f" * Real-Time Predictor: http://{host}:{port}/")
    print(f" * Sensor Analytics:    http://{host}:{port}/eda")
    print(f" * Model Benchmarks:    http://{host}:{port}/models")
    print(f" * Batch CSV Inference: http://{host}:{port}/batch")
    print("=" * 70 + "\n")
    sys.stdout.flush()

    app.run(host=host, port=port, debug=debug)
