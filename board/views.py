from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def board_list(request):
    # 게시판 리스트 가져오기
    posts = models.Board.objects.select_related('user').all()

    # 페이지 처리
    page = request.GET.get('page', 1) # 기본값 1
    paginator = Paginator(posts, 10) # 한 페이지에 보여질 게시물 수를 10개로 설정
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "list.html", {"posts": posts})


def board_detail(request, board_id):
    post = get_object_or_404(models.Board, board_id=board_id)
    return render(request, "detail.html", {"post": post})


def board_delete(request, board_id):
    post = get_object_or_404(models.Board, board_id=board_id)
    
    if str(request.session.get('user_id', None)) == post.user.user_id:
        post.delete()
        data = {"message": "게시글을 삭제하였습니다.", "icon": "success"}
    else:
        data = {"message": "작성자만 삭제할 수 있습니다.", "icon": "error"}
         
    return JsonResponse(data)