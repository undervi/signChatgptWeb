// 알림창 선언
const Toast = Swal.mixin({
    toast: true,
    position: 'center',
    showConfirmButton: false,
    timer: 900,
    timerProgressBar: false,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

// csrf 토큰 가져오기
function getCSRFToken() {
    // Django에서는 'csrftoken'이라는 이름의 쿠키에 CSRF 토큰이 저장됩니다.
    const csrfCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('csrftoken='));
    if (csrfCookie) {
        return csrfCookie.split('=')[1];
    }
    return null;
}

// 글 삭제
function del_post(boardId, curPage) {
    Swal.fire({
        title: '정말 삭제하시겠습니까?',
        text: "삭제한 데이터는 복구할 수 없습니다!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: '삭제',
        cancelButtonText: '취소'
    }).then((result) => {
        if (result.isConfirmed) {
            // 실제 동작 수행
            axios.post('/board/delete/', {
                board_id: boardId
            }, {
                headers: {
                'X-CSRFToken': getCSRFToken()  // CSRF 토큰을 헤더에 추가
                }
            })
            .then(function (response){
                // 서버 응답 성공시 처리
                Swal.fire({
                    icon: response.data.icon,
                    title: response.data.message
                }).then((result) => {
                    // Toast 메시지가 닫힌 후에 실행
                    if (result.isConfirmed) { // 확인 버튼을 누르면
                        if (response.data.icon == 'success') {
                            window.location.href = '/board/?page=' + String(curPage); // 게시글 목록으로 이동 (기존 페이지 유지)
                        }
                    }
                });
            })
            .catch(function (error) {
                // 에러 발생시 처리
                Toast.fire({
                    icon: "error",
                    title: "에러가 발생했습니다. 다시 시도해 주세요."
                });
            })
        }
    });
}

// 댓글 삭제