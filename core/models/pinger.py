__all__ = ['PingTask']

from django.db import models
from django.utils import timezone


class PingTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # Задача в очереди
        ('in_progress', 'In Progress'),  # Задача в процессе
        ('completed', 'Completed'),  # Задача завершена
        ('failed', 'Failed'),  # Задача завершена с ошибкой
    ]

    url = models.URLField()  # URL сокет-сервера или другого ресурса, который пингуем
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Статус пинга
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания задачи
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления
    last_pinged = models.DateTimeField(null=True, blank=True)  # Время последнего пинга
    result = models.TextField(null=True, blank=True)  # Результат пинга (лог или ошибка)

    def __str__(self):
        return f"Ping to {self.url} ({self.status})"

    def start_ping(self):
        """Метод для начала пинга."""
        self.status = 'in_progress'
        self.save()

    def complete_ping(self, result):
        """Метод для завершения пинга с результатом."""
        self.status = 'completed'
        self.result = result
        self.last_pinged = timezone.now()
        self.save()

    def fail_ping(self, error_message):
        """Метод для обработки ошибки пинга."""
        self.status = 'failed'
        self.result = error_message
        self.last_pinged = timezone.now()
        self.save()
