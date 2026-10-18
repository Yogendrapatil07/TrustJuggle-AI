import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-trustjuggle-secret-key-change-in-prod-8877")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session & Security Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Risk Engine Configuration (4 Neutral Bands)
    # 0-29: Low (Normal activity)
    # 30-59: Moderate (Monitor and collect evidence)
    # 60-79: High (Request additional verification)
    # 80-100: Very High (Prioritize verification and review)
    RISK_THRESHOLD_LOW = 0.0
    RISK_THRESHOLD_MODERATE = 30.0
    RISK_THRESHOLD_HIGH = 60.0
    RISK_THRESHOLD_VERY_HIGH = 80.0

    # Explainable Scoring Weights (Transparent rule-based model)
    WEIGHT_DEVICE_MISMATCH = 25.0
    WEIGHT_LOCATION_VELOCITY_ANOMALY = 30.0
    WEIGHT_DEVICE_CHURN = 20.0
    WEIGHT_UNUSUAL_HOURS = 15.0
    WEIGHT_NETWORK_INCONSISTENCY = 10.0

    # Telemetry Ingestion & Verification Settings
    TELEMETRY_API_KEY = os.getenv("TELEMETRY_API_KEY", "tj-telemetry-demo-key-2026")
    VERIFICATION_CHALLENGE_EXPIRY_HOURS = 24
    VERIFICATION_MAX_ATTEMPTS = 3

    # Device & Session Intelligence Settings
    MAX_CONCURRENT_SESSIONS = int(os.getenv("MAX_CONCURRENT_SESSIONS", "2"))
    DEVICE_CHURN_THRESHOLD_HOURS = int(os.getenv("DEVICE_CHURN_THRESHOLD_HOURS", "72"))
    PRIVATE_ARTIFACTS_DIR = BASE_DIR / "instance" / "private_artifacts"
    PASSWORD_RESET_TIMEOUT_MINUTES = 30

    # Identity & KYC Verification Providers
    IDENTITY_PROVIDER_MODE = os.getenv("IDENTITY_PROVIDER_MODE", "demo")  # 'demo' or 'live'
    IDENTITY_PROVIDER_NAME = "Simulated UIDAI / DigiLocker Verification Gateway"
    LIVENESS_PROVIDER_MODE = os.getenv("LIVENESS_PROVIDER_MODE", "demo")
    SMS_PROVIDER_MODE = os.getenv("SMS_PROVIDER_MODE", "demo")

    # Application Branding
    APP_NAME = "TrustJuggle AI"
    APP_TAGLINE = "One Account. One Verified Rider. Smarter Trust."
    SIMULATED_PLATFORM_NOTICE = (
        "Simulated Platform Environment: All delivery events and rider profiles "
        "are securely managed test records."
    )


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'trustjuggle.db'}"
    )


class TestingConfig(Config):
    """Testing configuration with in-memory SQLite and CSRF disabled."""

    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
