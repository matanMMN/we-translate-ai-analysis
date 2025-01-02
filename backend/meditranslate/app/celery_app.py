"""
Celery configuration module for WeTranslate-AI.
Handles task queue configuration and worker settings.
"""
from celery import Celery
from meditranslate.app.configurations.config import config

# Initialize Celery app with configuration from settings
celery = Celery(
    config.CELERY_WORKER_NAME,
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL,
)

# Configure Celery settings
celery.conf.update({
    # Enable task tracking for monitoring
    'task_track_started': True,
    
    # JSON serialization for task data
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'UTC',
    'enable_utc': True,
    # Worker settings for Kubernetes scalability
    'worker_concurrency': 4,  # Number of worker processes per container
    'task_time_limit': 600,   # 10 minute timeout for tasks
    'task_soft_time_limit': 540,  # Soft timeout 9 minutes
    
    # Task routing and queues for distributed processing
    'task_default_queue': 'default',
    'task_queues': {
        'default': {
            'exchange': 'default',
            'exchange_type': 'direct',
            'routing_key': 'default'
        },
        'pdf_processing': {
            'exchange': 'pdf_processing',
            'exchange_type': 'direct',
            'routing_key': 'pdf_processing',
            'queue_arguments': {'x-max-priority': 10}  # Priority queue for PDF processing
        }
    },
    
    # Settings for reliable message delivery in distributed environment
    'task_queue_ha_policy': 'all',  # High availability for RabbitMQ queues
    'broker_transport_options': {
        'visibility_timeout': 43200,  # 12 hours
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },
    'task_routes':{
        'process_pdf_file_task': {'queue': 'pdf_processing'}
    },
    'imports':(
        'meditranslate.src.files.tasks',  # Explicitly import tasks module
    ),
    # Retry settings
    'task_acks_late': True,  # Tasks acknowledged after completion
    'task_reject_on_worker_lost': True,  # Reject tasks if worker disconnects
    
    # Result backend settings
    'result_expires': 3600,  # Results expire after 1 hour
})

celery.conf.update(
    task_routes={
        'process_pdf_file_task': {'queue': 'pdf_processing'}
    },
)
