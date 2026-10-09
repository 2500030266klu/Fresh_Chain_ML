"""
app/__init__.py
----------------
Flask Application Factory with model and asset readiness checks.
"""

import os
from flask import Flask
from src.config import PROJECT_ROOT, OUTPUT_DIR


def create_app() -> Flask:
    """
    Constructs and configures the Flask application.
    """
    app = Flask(
        __name__,
        template_folder=str(PROJECT_ROOT / "app" / "templates"),
        static_folder=str(PROJECT_ROOT / "app" / "static")
    )

    app.config["SECRET_KEY"] = "fruit-spoilage-ml-secret-key-2026"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True

    # Register Blueprint / Routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
