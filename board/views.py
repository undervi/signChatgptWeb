from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from board import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
import json
from django.conf import settings

kakao_login_url = settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['login_url']


# 게시글 목록
def board_list(request):
    # 게시판 리스트 가져오기 (is_deleted가 True인 것 제외)
    posts = models.Board.objects.select_related("user").exclude(is_deleted=True).order_by('-created_datetime').all()

    # 페이지 처리
    page = request.GET.get("page", 1) # 기본값 1
    paginator = Paginator(posts, 10) # 한 페이지에 보여질 게시물 수를 10개로 설정
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "board/list.html", {"posts": posts})


# 게시글 상세
def board_detail(request, board_id):
    post = get_object_or_404(models.Board, board_id=board_id)
    comments = models.Comment.objects.filter(board=post, is_deleted=False).select_related("user").order_by('created_datetime').all()
    return render(request, "board/detail.html", {"post": post, "comments": comments, "cur_page": request.GET.get("page", 1)})


# 게시글 삭제
@require_POST
def board_delete(request):
    json_data = json.loads(request.body.decode('utf-8'))
    board_id = json_data.get('board_id') 
    post = get_object_or_404(models.Board, board_id=board_id)
    
    if str(request.session.get("user_id", None)) == post.user.user_id:
        post.is_deleted = True
        post.save()
        data = {"message": "게시글을 삭제하였습니다.", "icon": "success"}
    else:
        data = {"message": "작성자만 삭제할 수 있습니다.", "icon": "error"}
         
    return JsonResponse(data)


# 게시글 작성
def board_write(request):
    if request.method == "POST":
        # 유저 정보 불러오기
        session_user_id = request.session.get("user_id", None)
        if session_user_id is None: # 로그인 페이지로
            return redirect(kakao_login_url)
        if models.Users.objects.filter(user_id=session_user_id).exists():
            user = models.Users.objects.get(user_id=session_user_id)
            
        # 게시글 작성 로직
        post = models.Board.objects.create(
            user = user,
            title = request.POST.get("title"),
            body = request.POST.get("body")
        )
        return redirect("/board/detail/" + str(post.board_id) + "/")
    else:
        # 게시글 작성 페이지로 이동
        context = {
            "cur_page": request.GET.get("page", 1),
            "type": "write"
        }
        return render(request, "board/write.html", context)
    
    
# 게시글 수정 - GET
def board_modify_get(request, board_id):
    post = models.Board.objects.get(board_id=board_id)
    context = {
        "cur_page": request.GET.get("page", 1),
        "post": post,
        "type": "modify"
    }
    return render(request, "board/write.html", context)


# 게시글 수정 - POST
@require_POST
def board_modify_post(request):
    json_data = json.loads(request.body.decode('utf-8'))
    board_id = json_data.get('board_id')
    post = get_object_or_404(models.Board, board_id=board_id)
    
    if str(request.session.get("user_id", None)) == post.user.user_id:
        post.title = json_data.get('title')
        post.body = json_data.get('body')
        post.save()
        data = {"message": "게시글을 수정하였습니다.", "icon": "success"}
    else:
        data = {"message": "작성자만 수정할 수 있습니다.", "icon": "error"}
 
    return JsonResponse(data)
    

# 댓글 작성   
@require_POST
def comment_write(request):
    # 유저 정보 불러오기
    session_user_id = request.session.get("user_id", None)
    if session_user_id is None: # 로그인 페이지로
        return redirect(kakao_login_url)
    if models.Users.objects.filter(user_id=session_user_id).exists():
        user = models.Users.objects.get(user_id=session_user_id)
    
    board_id = request.POST.get("board_id")
    cur_page = request.POST.get("cur_page", 1)
    
    # 댓글 작성 로직
    comment = models.Comment.objects.create(
        user = user,
        board = models.Board.objects.get(board_id=board_id),
        comment_content = request.POST.get("comment_content")
    )
    return redirect("/board/detail/" + str(board_id) + "/?page=" + cur_page)


# 댓글 삭제
@require_POST
def comment_delete(request):
    json_data = json.loads(request.body.decode('utf-8'))
    comment_id = json_data.get('comment_id') 
    comment = get_object_or_404(models.Comment, comment_id=comment_id)
    
    if str(request.session.get("user_id", None)) == comment.user.user_id:
        comment.is_deleted = True
        comment.save()
        data = {"message": "댓글을 삭제하였습니다.", "icon": "success"}
    else:
        data = {"message": "작성자만 삭제할 수 있습니다.", "icon": "error"}
         
    return JsonResponse(data)


