from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from kakao_login import models
from django.conf import settings

kakao_access_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['client_id'],
    "KAKAO_REDIRECT_URI": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['redirect_uri'],
    "KAKAO_CLIENT_SECRET_KEY": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['client_secret'], 
}

# 회원 정보 요청 함수
def request_user_info(access_token):
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    user_info_json = requests.get(kakao_profile_uri, headers=auth_headers).json()
    
    return user_info_json


def kakao_login(request):
    # 인카 코드 받기
    code = request.GET.get("code")
    
    # access token 요청
    client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
    client_secret = KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY']
    token_req = requests.post(f"{kakao_access_uri}?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}")
    access_token = token_req.json().get('access_token')
    
    # kakao 회원정보 요청
    user_info_json = request_user_info(access_token)
    if not user_info_json:
        error_message = {'message': '유저 정보를 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # 회원가입 및 로그인
    user_id = user_info_json.get('id')
    
    kakao_account = user_info_json.get('kakao_account')
    if not kakao_account:
        error_message = {'message': '카카오 계정을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    user_name = kakao_account.get('profile').get('nickname')
    profile_image_url = kakao_account.get('profile').get('profile_image_url')
    
    if not models.Users.objects.filter(user_id=user_id).exists():
        user = models.Users()
        user.user_id = user_id
        user.user_name = user_name
        user.profile_imeage_url = profile_image_url
        user.save()

    request.session['user_id'] = user_id
    request.session['user_name'] = user_name
    request.session['user_image'] = profile_image_url

    return redirect('/')


def logout(request):

    request.session['user_id'] = None
    request.session['user_name'] = None
    request.session['user_image'] = None
    
    return redirect('/')
