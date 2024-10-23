import json
import logging
import logging.config
import logging.handlers
import pathlib
import time

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

user_action_logger = logging.getLogger('user_actions')


def get_handler_by_name(logger, name):
    for handler in logger.handlers:
        if handler.get_name() == name:
            return handler
    return None


def setup_logging():
    print(f"Setting up logging... Time right now is {time.time()}")
    config_file = pathlib.Path("logging_config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    # print("Logging configuration loaded:", config)

    # Apply the logging configuration
    logging.config.dictConfig(config)

    memory_handler = get_handler_by_name(user_action_logger, "memory_handler")
    if memory_handler is not None:
        print("MemoryHandler is set up correctly.")


def home(request):
    user_action_logger.info(
        f'Home view bezocht door gebruiker: {request.user.username if request.user.is_authenticated else "gast"}')
    return render(request, 'logging_app/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            user_action_logger.info(f' someone created an account.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'logging_app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user_action_logger.info(f'{username} logged in successfully.')
                return redirect('home')
            else:
                user_action_logger.warning(f"Authenticatie mislukt voor gebruiker: {username}")
        else:
            user_action_logger.warning(f"Verkeerd wachtwoord ingevoerd door gebruiker: {request.POST.get('username')}")
    else:
        form = AuthenticationForm()

    return render(request, 'logging_app/login.html', {'form': form})


def logout_view(request):
    username = request.user.username if request.user.is_authenticated else "Unknown"
    logout(request)
    user_action_logger.info(f'{username} logged out.')
    return redirect('home')


def button_click_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            for _ in range(1_000):
                user_action_logger.debug(f'{request.user.username} clicked the button.')
            memory_handler = get_handler_by_name(user_action_logger, 'memory_handler')
            if memory_handler:
                memory_handler.flush()
        return redirect('home')


def test1(request):
    user_action_logger.info(
        f'test1 view bezocht door gebruiker: {request.user.username if request.user.is_authenticated else "gast"}')
    return render(request, 'logging_app/test1.html', {'user': request.user})


def test2(request):
    user_action_logger.info(
        f'test2 view bezocht door gebruiker: {request.user.username if request.user.is_authenticated else "gast"}')
    return render(request, 'logging_app/test2.html', {'user': request.user})


def read_log_file(filename):
    logs = {
        'info': [],
        'warning': [],
        'debug': []
    }
    try:
        with open(filename, 'r') as file:
            for line in file:
                if 'INFO' in line:
                    logs['info'].append(line.strip())
                elif 'WARNING' in line:
                    logs['warning'].append(line.strip())
                elif 'DEBUG' in line:
                    logs['debug'].append(line.strip())
    except FileNotFoundError:
        pass
    return logs


def dashboard(request):
    user_action_logger.info(
        f'dashboard view bezocht door gebruiker: {request.user.username if request.user.is_authenticated else "gast"}')
    logs = read_log_file('queuehandler.log')
    users = User.objects.values_list('username', flat=True)
    selected_user = request.GET.get('username')
    filtered_logs = {
        'info': [],
        'warning': [],
        'debug': []
    }
    if selected_user:
        for level, entries in logs.items():
            for entry in entries:
                if selected_user in entry:
                    filtered_logs[level].append(entry)
    else:
        filtered_logs = logs

    return render(request, 'logging_app/dashboard.html', {
        'user': request.user,
        'users': users,
        'logs': filtered_logs,
    })
