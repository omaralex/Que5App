from django.urls import path
from . import views

urlpatterns = [
    path('create_user', views.create_user_view,name='create_user'),
    path('login_user', views.login_view,name='login_user'),
    path('get_all_users', views.get_all_users_view,name='get_all_users'),
    path('question_random', views.questions_random_view,name='question_random'),
    path('notifications', views.push_notifications_view,name='notifications'),
    path('register_token', views.register_token_view,name='register_token'),
    path('send_message', views.send_message_view,name='send_message'),
    path('get_all_message', views.get_all_message_view,name='get_all_message'),
    path('update_status_message', views.update_status_message_view,name='update_status_message')
]