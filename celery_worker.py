# celery_worker.py
from tasks import celery

if __name__ == "__main__":
    celery.worker_main()
