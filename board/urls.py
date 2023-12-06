# blog/urls.py
from django.urls import path
from board import views

app_name = 'board'
urlpatterns = [
    path('', views.board_list, name='list'),
    path('detail/<int:board_id>/', views.board_detail, name='detail'),
    path('delete/', views.board_delete, name='delte'),
    path('write/', views.board_write, name='write'),
    path('modify/<int:board_id>/', views.board_modify_get, name='modify_get'),
    path('modify/', views.board_modify_post, name='modify_post'),
    path('comment/wrtie/', views.comment_write, name='comment-write'),
    path('comment/delete/', views.comment_delete, name='comment-delete'),
]
