function board_modify(boardId, curPage) {
    const title = document.getElementById("title").value;
    const body = document.getElementById("body").value;
    
    axios.post('/board/modify/', {
        board_id: boardId,
        title: title,
        body: body
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
                    window.location.href = '/board/detail/' + boardId + '/?page=' + String(curPage); // 게시글 목록으로 이동 (기존 페이지 유지)
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
    });
}