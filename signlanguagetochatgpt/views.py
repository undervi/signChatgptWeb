from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
import mlflow
import mlflow.keras
from chatgpt.views import chatGPT, imageGPT
logger = logging.getLogger('mylogger')
from .models import ChatResult, Result

def getChatResult(self, id):
        query = "SELECT * FROM signlanguagetochatgpt_chatresult WHERE id = {0}".format(id)
        logger.info(">>>>>>>> getChatResult SQL : "+query)
        chatResult = self.t_exec(query)

def index(request):
    return render(request, 'languagechat/index.html')

def chat(request):
    if request.method == 'POST' and request.FILES['files']:

        results=[]
        files = request.FILES.getlist('files')
        chatGptPrompt = ""
        for idx,file in enumerate(files, start=0):
            # logger.error('file', file)
            # class names 준비
            class_names = list(string.ascii_lowercase)
            class_names = np.array(class_names)


            # mlflow 로딩
            mlflow_uri="http://mlflow.carpediem.so/"
            mlflow.set_tracking_uri(mlflow_uri)
            model_uri = "models:/Sign_Signal_17/production"
            model = mlflow.keras.load_model(model_uri)


            # history 저장을 위해 객체에 담아서 DB에 저장
            # 이때 파일시스템에 저장도 된다.
            result = Result()
            result.image = file
            result.pub_date = timezone.datetime.now()
            result.save()


            # 흑백으로 읽기
            img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)
            # 크기 조정
            img = cv2.resize(img, (28, 28))
            # input shape 맞추기
            test_sign = img.reshape(1, 28, 28, 1)
            # 스케일링
            test_sign = test_sign / 255.

            # 예측 
            pred = model.predict(test_sign)
            pred_1 = pred.argmax(axis=1)

            result_str = class_names[pred_1][0]


            #결과를 DB에 저장
            result.result = result_str
            result.save()
            results.append(result)

            #result.result의 결과를 하나씩 chatGptPrompt에 추가
            chatGptPrompt += result.result
        
        #질문을 DB에 저장
        chatResult = ChatResult()
        chatResult.prompt = chatGptPrompt
        chatResult.pub_date = timezone.datetime.now()
        chatResult.save()


        #저장된 질문을 DB에서 가져오기
        selectedChatResult = ChatResult.objects.get(id=chatResult.id)

        #chatGptPrompt를 chatGPT에게 전달한다.
        #type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
        type = request.POST.get('type')
        if type == 'image':
            content = imageGPT(selectedChatResult.prompt)
        else:
            content = chatGPT(selectedChatResult.prompt)
        selectedChatResult.content = content
        selectedChatResult.save()
        
     
        context = {
            'type': type,
            'question': selectedChatResult.prompt,
            'result': selectedChatResult.content
        }

    return render(request, 'languagechat/result.html', context)  