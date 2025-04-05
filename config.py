# config.py
import os
from dotenv import load_dotenv

# Carga variables de entorno desde un archivo .env
load_dotenv()

class Config:
    # Clave secreta para la aplicación Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/dashcom"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Credenciales de API
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

    # Configuración de Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Validación de variables críticas
    @staticmethod
    def validate():
        required_vars = ["TELEGRAM_BOT_TOKEN", "OPENAI_API_KEY", "ADMIN_CHAT_ID"]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"La variable de entorno {var} no está configurada.")
