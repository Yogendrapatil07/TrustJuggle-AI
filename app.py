"""TrustJuggle AI — The Rented Account Risk Monitoring & Verification Platform.

Tagline: One Account. One Verified Rider. Smarter Trust.
Mandatory launch command: python app.py
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config
from models import db
from models.models import User

# Extensions
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name: str = None) -> Flask:
    """Application factory for TrustJuggle AI."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    selected_config = config.get(config_name, config["default"])
    app.config.from_object(selected_config)

    # Ensure instance and private artifacts directories exist
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)
    private_artifacts_path = Path(app.config.get("PRIVATE_ARTIFACTS_DIR", instance_path / "private_artifacts"))
    private_artifacts_path.mkdir(parents=True, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.rider import rider_bp
    from routes.admin import admin_bp
    from routes.verification import verification_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(rider_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(verification_bp)
    app.register_blueprint(api_bp)

    # Exempt machine-to-machine API routes from browser CSRF checks
    csrf.exempt(api_bp)

    # Server-side Session Invalidation & Concurrency Hook
    @app.before_request
    def validate_rider_session():
        from flask import request, session, redirect, url_for, flash
        from flask_login import current_user, logout_user
        from services.device_session_service import DeviceSessionService

        # Skip validation for static assets, public auth endpoints, and API
        if request.endpoint in [
            "static",
            "auth.login",
            "auth.logout",
            "auth.register",
            "auth.forgot_password",
            "auth.reset_password",
            "auth.landing",
            "auth.index",
        ] or request.path.startswith("/api/") or request.path.startswith("/static/"):
            return None

        if current_user.is_authenticated and current_user.is_rider and current_user.rider_profile:
            session_token = session.get("session_token")
            if session_token:
                is_valid, reason = DeviceSessionService.validate_session_token(
                    current_user.rider_profile.id, session_token
                )
                if not is_valid:
                    logout_user()
                    session.pop("session_token", None)
                    flash(f"Session ended: {reason}", "warning")
                    return redirect(url_for("auth.login"))


    # Global context processor
    @app.context_processor
    def inject_global_variables():
        return {
            "app_name": app.config.get("APP_NAME", "TrustJuggle AI"),
            "app_tagline": app.config.get(
                "APP_TAGLINE", "One Account. One Verified Rider. Smarter Trust."
            ),
            "simulated_notice": app.config.get(
                "SIMULATED_PLATFORM_NOTICE",
                "Simulated Platform Environment: All delivery events and rider profiles are test records.",
            ),
        }

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500

    # Initialize database tables safely
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("\n" + "=" * 68)
    print("  [TRUSTJUGGLE AI] -- RENTED ACCOUNT MONITORING & VERIFICATION")
    print("      One Account. One Verified Rider. Smarter Trust.")
    print("=" * 68)
    print(f"  * Local Server running at: http://{host}:{port}/")
    print("  * Demo Admin: admin@trustjuggle.local / Admin123!")
    print("  * Demo Rider: rider@trustjuggle.local / Rider123!")
    print("=" * 68 + "\n")

    app.run(host=host, port=port, debug=debug)
