let idNum = 0;
function addFile(){
    deepCopy();
}

function deepCopy()  {
    // 'test' node 선택 (제일 마지막 노드 선택)
    const spanElements = document.querySelectorAll('#sign-form > span');
    let lastId = 0;
    spanElements.forEach(function (spanElement) {
        const spanId = parseInt(spanElement.id.split('-')[2]);
        lastId = spanId > lastId ? spanId : lastId;
    });
    const fileModule = document.getElementById('file-module-' + String(lastId));

    // 노드 복사하기 (deep copy)
    const newNode = fileModule.cloneNode(true);

    // 복사된 Node id 변경하기
    idNum++;
    newNode.id = 'file-module-' + idNum;

    // 복사된 노드에 이벤트 추가
    const deleteButton = newNode.querySelector('.del-btn');
    deleteButton.setAttribute('onClick', "fileDel('" + newNode.id + "')");
    deleteButton.setAttribute('disabled', false);

    // 복사된 노드에 value 삭제
    const fileInput = newNode.querySelector('input');
    fileInput.value = '';

    // 복사한 노드 붙여넣기
    fileModule.after(newNode);
}


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

//첨부파일 삭제
function fileDel(spanId){
    if (spanId == 'file-module-0') {
        Toast.fire({
            icon: 'error',
            title: '첫번째 칸은 삭제할 수 없습니다.'
        });
        return;
    }

    var spanElement = document.getElementById(spanId);
    if (spanElement) {
        spanElement.remove();
    } else {
        console.log("Span element not found with ID", spanId);
    }
}

// form submit
document.getElementById('form-submit').addEventListener('click', function(event) {
    event.preventDefault();

    var inputField = document.querySelector('#file-module-0 input');
    var inputValue = inputField.value.trim();

    // 사진 미첨부
    if (inputValue == '') {
        Toast.fire({
            icon: 'error',
            title: '첫번째 사진은 필수입니다.'
        });
        return;
    }

    // 확장자 유효성 검사
    var is_valid = true;
    var imageElements = document.querySelectorAll('.img-file');

    imageElements.forEach(function (imageElement) {
        var extension = imageElement.value.split('.').pop().toLowerCase();
        var allowedExtensions = ['jpg', 'jpeg', 'png', ''];
        if (!allowedExtensions.includes(extension)) {
            Toast.fire({
                icon: 'error',
                title: 'jpg, jpeg, png 확장자로된 사진만 사용 가능합니다.'
            });
            is_valid = false;
            return;
        }
    });

    // 서버로 파일 전송
    if (is_valid) {
        document.getElementById('sign-form').submit();
    }
});