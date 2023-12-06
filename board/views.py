from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from board import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 데코레이터
def user_id_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if "user_id" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            # 세션에 user_id가 없는 경우, 게시글 목록 페이지로 리다이렉트
            return redirect("/board/")  

    return _wrapped_view


# 목록
def board_list(request):
    # 게시판 리스트 가져오기 (is_deleted가 True인 것 제외)
    posts = models.Board.objects.select_related("user").exclude(is_deleted=True).all()

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


# 상세
def board_detail(request, board_id):
    post = get_object_or_404(models.Board, board_id=board_id)
    return render(request, "board/detail.html", {"post": post})


# 삭제
def board_delete(request, board_id):
    post = get_object_or_404(models.Board, board_id=board_id)
    
    if str(request.session.get("user_id", None)) == post.user.user_id:
        post.is_deleted = True
        post.save()
        data = {"message": "게시글을 삭제하였습니다.", "icon": "success"}
    else:
        data = {"message": "작성자만 삭제할 수 있습니다.", "icon": "error"}
         
    return JsonResponse(data)


@user_id_required
# 작성
def board_write(request):
    if request.method == "POST":
        # 유저 정보 불러오기
        session_user_id = request.session.get("user_id", None)
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
        return render(request, "board/write.html")