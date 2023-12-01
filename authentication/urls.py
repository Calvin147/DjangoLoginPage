from django.contrib import admin
from django.urls import path, include
from . import views
from .views import update_task

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('update_task/<int:task_id>/', update_task, name='update_task'),
]