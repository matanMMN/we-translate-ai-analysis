import Celery
from meditranslate.app.configurations import config

celery = Celery(
    config.CELERY_WORKER_NAME,
    backend= config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL
)
celery.conf.task_routes = {
    "wetranslateai.app.tasks.task_test.task_test": {
        'queue':'queue_test'
    }
}
celery.conf.update(task_track_started=True)
