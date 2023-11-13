from celery import Celery

app = Celery(
    "app",
    broker="redis://localhost:6379/0",
    chdir='answer/audio',
    include=["app.tasks"],
)

app.conf.result_backend = "redis://localhost:6379/0"
