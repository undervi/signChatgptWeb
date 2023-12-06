# blog/urls.py
from django.urls import path
from board import views

app_name = 'board'
urlpatterns = [
    path('', views.board_list, name='list'),
    path('detail/<int:board_id>/', views.board_detail, name='detail'),
    path('delete/', views.board_delete, name='delte'),
    path('write/',views.board_write, name='write'),
    path('comment/wrtie/', views.comment_write, name='comment-write'),
    # 글 수정
]
