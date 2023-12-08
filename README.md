# 수어 대화형 AI 웹 서비스

![](/static/image/image.png)
<a href="http://54.193.7.218/">수어 대화형 AI 웹 서비스로 이동</a>


### 0️⃣ 기간 : 2023.12.04 ~ 2023.12.07<br/>

### 1️⃣ 미션 : 수어 이미지를 번역하고 이를 chatgpt가 답변해주는 대화형 AI 웹 서비스 개발<br/>

### 2️⃣ 데이터 : 수어 이미지 데이터 제공
  
### 3️⃣ 목표 
    1) 이미지 분류를 통해서 수어를 알파벳으로 번역하는 AI 모델을 개발한다.
    2) AI 모델을 통해 번역된 문장을 chatgpt에게 질문하여 답변을 받는 서비스를 개발한다. 

### 4️⃣ 목차

1. [**서비스 소개**](#service)

2. [**기술스택**](#stacks)

3. [**기능 소개**](#func)

4. [**시연 영상**](#testing)

<br />

### 5️⃣ 이슈
1 ) 로컬이 실행이 안되는 오류
  - 원인: 장고는 기본적으로 8000번 포트를 사용하는데 해당 포트가 다른 프로세스에 의해 이미 사용하고 있어서 오류 발생
  - 해결방법 (윈도우 기준)
    ```
    # 실행중인 8000번 포트 프로세스 찾기
    $ netstat -ano | findStr 8000
    # 찾은 프로세스 ID를 통해 종료 시키기
    $ taskkill /f /pid "프로세스ID"
    ```
<br/>

2 ) 카카오 로그인 - 프로필 이미지 미동의 후 가입 시 constraint failed 오류
  - 원인: Users의 profile_imeage_url 필드에 NOT NULL 조건이 걸려있어서 오류 발생 (미지정시 기본으로 Null은 False가 된다.)
  - 해결방법

    ```
    # models.py 수정
    class Users(models.Model):
      user_id = models.CharField(primary_key=True, max_length=100)
      user_name = models.CharField(max_length=50)
      user_email = models.CharField(max_length=50, null=True, blank=True)
      gender = models.CharField(max_length=6,  null=True, blank=True)
      profile_imeage_url = models.CharField(max_length=100, null=True, blank=True)
    ```
<br />

3 ) AWS EC2 - CPU 사용률 100% 강제 종료 오류<br/>

![](/static/image/cpu100.png)<br/>

- 원인: 서버 실행 도중 접속자가 많이 몰려 CPU 사용률이 99.9%를 넘어서며 서버가 강제 종료되었다.
- 해결방법: 스토리지 용량 늘리기 (16GB -> 30GB)


  첫 번째, AWS EC2에서 용량을 늘려준다.
  - EC2 -> 인스턴스 -> 스토리지 -> 볼륨 용량 늘리기

  두 번째, 우분투에서 적용 
  - 볼륨에 확장해야 하는 파티션이 있는지 확인하려면 <code>lsblk</code> 명령을 사용해서 연결된 블록 디바이스에 대한 정보를 불러온다.

  - 리눅스 파티션 크기 조정 (xvda1 파티션의 크기를 조정함)</br>
  <code>$ sudo growpart /dev/xvda 1</code>

  - 이때, 블록 디바이스에 남은 공간이 없다는 오류가 발생한다면 임시 파일 시스템 tmpfs를 /tmp에 탑재하여 이를 방지한다.<br/>
  <code>$ sudo mount -o size=10M, rw, nodev, nosuid -t tmpfs tmpfs /tmp</code>

  - 조정 후 재부팅 하면 xvda1 파티션의 크기가 늘어남 -> <code>df -h</code> 로 확인

<br/>


<div id="service">
 
  ## 🌐 농인들을 위한 새로운 혁신, 수어 ChatGPT 대화 서비스

  >이 프로젝트는 수어 이미지를 인식하여 알파벳으로 번역하는 AI 모델과, 이를 기반으로 한 ChatGPT와의 통합을 통해 혁신적인 언어 서비스를 제공합니다. 손동작 이미지 분류 AI 모델을 활용하여 수어를 텍스트로 변환하고, 이렇게 번역된 텍스트를 ChatGPT에 전달하여 자연스러운 대화를 가능하게 합니다. 수어 커뮤니케이션과 인공지능의 만남으로 언어의 경계를 넘어, 소통의 장벽을 허물어보세요.🗣️✨
</div><br />

<div id="stacks">

  ## 🛠️ 기술 스택
  ### Tools
  ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
  ![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)
  ![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=MLflow&logoColor=white)
  ![VScode](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=VisualStudioCode&logoColor=white)
  ![AWS](https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
  ![Amazon EC2](https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
  
  ### Development
  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
  ![Django](https://img.shields.io/badge/django-003B57?style=for-the-badge&logo=Django&logoColor=white)
  ![sqlite](https://img.shields.io/badge/sqlite-4479A1?style=for-the-badge&logo=sqlite&logoColor=white)
  ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white)
  ![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=Keras&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white)
  ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=Axios&logoColor=white)
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white)
  
</div><br />

<div id="func">

  ## 🤖 기능 소개

  1. 수어 이미지 번역 
  - 손동작 이미지를 텍스트로 번역하여 의사소통의 장벽을 허물어줍니다.
  - Tensorflow Keras 딥러닝 모델 활용 (CNN)
  
  2. ChatGPT와의 대화
  - 번역된 문장은 ChatGPT API를 활용하여, 사용자에게 맞춤 대화를 제공합니다. 자동으로 생성된 답변은 사용자의 질문이나 입력에 유연하게 반응하여 자연스러운 대화를 이끌어냅니다.

  3. 자유 게시판
  - 회원가입한 사용자들은 게시판에 글 작성, 수정, 삭제, 댓글 작성, 삭제 등을 할 수 있습니다.
  - 본인의 글, 댓글만 수정/삭제 할 수 있습니다.
  - 비회원은 조회만 가능합니다.
  - 페이징 기능을 구현하였습니다.

</div><br />

<div id="testing">

  ## 🎥 시연 영상
  1. 카카오톡 로그인
  <video src="https://github.com/undervi/sign-chatgpt-web/assets/95211722/bc4350ae-6b3b-404e-b918-98494c6a90d4"></video><br/>
  
  2. ChatGPI에게 질문하기
  <video src="https://github.com/undervi/sign-chatgpt-web/assets/95211722/706f566b-b84e-4064-bc2e-2a91a3cc36f7"></video>
  <video src="https://github.com/undervi/sign-chatgpt-web/assets/95211722/7a98965e-fa0d-4009-aa94-6e4ef2d4d0c2"></video><br/>

  3. 수어로 ChatGPT에게 질문하기
  <video src="https://github.com/undervi/sign-chatgpt-web/assets/95211722/2629a635-4864-40c9-a85b-d7b87a94177f"></video>
  <video src="https://github.com/undervi/sign-chatgpt-web/assets/95211722/301a9b20-c172-4cb7-a16f-561d3d6934fa"></video><br/>

  4. 자유 게시판  
  <video src="https://github.com/undervi/sign-chatgpt-web/assets/95211722/f4486a30-d78d-4151-90a6-8bc267eca17d"></video>

</div>
