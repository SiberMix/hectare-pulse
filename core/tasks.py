from celery import shared_task
import requests
from .models import PingTask
from django.utils import timezone

@shared_task
def ping_task(ping_task_id):
    # Получаем задачу из базы данных по ID
    ping_task = PingTask.objects.get(id=ping_task_id)
    ping_task.start_ping()  # Устанавливаем статус "in_progress"

    try:
        # Пингует сервер (можно использовать любой метод, например, requests или сокеты)
        response = requests.get(ping_task.url)

        # Если запрос успешный, обновляем статус на "completed"
        if response.status_code == 200:
            ping_task.complete_ping(f"Success: {response.status_code}")
        else:
            ping_task.fail_ping(f"Failed with status: {response.status_code}")
    except Exception as e:
        ping_task.fail_ping(str(e))

    return f"Ping to {ping_task.url} completed"
