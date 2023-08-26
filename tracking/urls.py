from django.urls import path
from tracking import views

urlpatterns = [
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('mainpage', views.mainpage_action, name='mainpage'),
    path('start-work', views.start_work, name='start_work'),
    path('end-work', views.end_work, name='end_work'),
]