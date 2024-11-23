from celery import shared_task

@shared_task
def hit_socket_once(task_id):
    task = SocketTask.objects.get(id=task_id)
    try:
        response = requests.get(task.url)
        Log.objects.create(task=task, message=f"Success: {response.text}")
    except Exception as e:
        Log.objects.create(task=task, message=f"Error: {str(e)}")

@shared_task
def hit_socket_periodic(task_id):
    task = SocketTask.objects.get(id=task_id)
    if task.is_active:
        try:
            response = requests.get(task.url)
            Log.objects.create(task=task, message=f"Success: {response.text}")
        except Exception as e:
            Log.objects.create(task=task, message=f"Error: {str(e)}")
        # Планируем повторную задачу
        hit_socket_periodic.apply_async((task_id,), countdown=task.interval)
