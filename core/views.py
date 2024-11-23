from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import PingTask


def login_view(request):
    if request.user.is_authenticated:
        print("User is authenticated, redirecting to home.")
        return redirect('home')  # Перенаправление на главную страницу

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, 'core/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на домашнюю страницу
        else:
            messages.error(request, "Invalid login credentials.")
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')


@login_required
def ping_page(request):
    # Получаем все пинг задачи пользователя (можно добавить фильтрацию по пользователю)
    tasks = PingTask.objects.all()
    return render(request, 'core/ping_page.html', {'tasks': tasks})


def home(request):
    """
    Главная страница сайта. Если пользователь авторизован, перенаправляем на страницу пинга.
    Если не авторизован, показываем страницу с формой логина.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'core/home.html')  # Показываем главную страницу, если не авторизован
