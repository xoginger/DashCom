# tasks.py
from celery import Celery
from config import Config
from models import db, Report
from datetime import datetime, timedelta

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
celery.conf.update({
    'broker_url': Config.CELERY_BROKER_URL,
    'result_backend': Config.CELERY_RESULT_BACKEND,
})

@celery.task
def daily_summary():
    from models import User
    summary = {}
    for user in User.query.all():
        reports = Report.query.filter(Report.user_id==user.id, Report.timestamp >= datetime.utcnow()-timedelta(days=1)).all()
        summary[user.name] = len(reports)
    print("Resumen diario:", summary)
    return summary
