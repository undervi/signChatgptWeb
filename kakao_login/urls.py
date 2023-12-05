# blog/urls.py
from django.urls import path
from . import views

app_name = 'kakao_login'
urlpatterns = [
    path('oauth/', views.kakao_login, name='oauth'),
    path('logout/', views.logout, name='logout'),
]
