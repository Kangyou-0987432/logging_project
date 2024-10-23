from django.urls import path
from .views import home, test1, test2, dashboard, setup_logging, signup, login_view, logout_view, button_click_view, \
    get_handler_by_name
import logging

#  start logging
setup_logging()

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('button_click/', button_click_view, name='button_click'),
    path('test1/', test1, name='test1'),
    path('test2/', test2, name='test2'),
    path("dashboard/", dashboard, name="dashboard"),
]

user_action_logger = logging.getLogger('user_actions')

memory_handler = get_handler_by_name(user_action_logger, 'memory_handler')
if memory_handler:
    memory_handler.flush()
