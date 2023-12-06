# blog/urls.py
from django.urls import path
from board import views

app_name = 'board'
urlpatterns = [
    path('', views.board_list, name='list'),
    path('detail/<int:board_id>/', views.board_detail, name='detail'), # 추가: 목록으로 가는 기능 (페이지 유지)
    path('delete/<int:board_id>/', views.board_delete, name='delte'),
    path('write/',views.board_write, name='write')
    # 글 수정
    # 댓글 달기
]
