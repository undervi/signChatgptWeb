# blog/urls.py
from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.board_list, name='list'),
    path('detail/<int:board_id>/', views.board_detail, name='detail'),
    path('delete/<int:board_id>/', views.board_delete, name='delte'),
    # 글 작성성
    # 글 수정
    # 댓글 달기
]
