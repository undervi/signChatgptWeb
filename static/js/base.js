// csrf 토큰 가져오기
function getCSRFToken() {
    // Django에서는 'csrftoken'이라는 이름의 쿠키에 CSRF 토큰이 저장됩니다.
    const csrfCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('csrftoken='));
    if (csrfCookie) {
        return csrfCookie.split('=')[1];
    }
    return null;
}