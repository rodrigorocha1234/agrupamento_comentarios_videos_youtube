SECRET_KEY = "MyVeryStrongSecretKey"

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://superset:superset@postgres:5432/superset"

SQLALCHEMY_TRACK_MODIFICATIONS = False

TALISMAN_ENABLED = False
ENABLE_PROXY_FIX = True
WTF_CSRF_ENABLED = True

FEATURE_FLAGS = {
    "DASHBOARD_RBAC": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
}

MAPBOX_API_KEY = ""

# Redis + Celery
class CeleryConfig:
    broker_url = 'redis://redis:6379/0'
    result_backend = 'redis://redis:6379/0'
    worker_log_server = False

CELERY_CONFIG = CeleryConfig

# Dark mode

APP_NAME = "Superset"

# Trino support
SQLLAB_CTAS_NO_LIMIT = True