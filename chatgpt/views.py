from django.shortcuts import render
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.CHATGPT_API_KEY)




#chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    print(completion)
    result = completion.choices[0].message.content
    return result

#chatGPT에게 그림 요청 API
def imageGPT(prompt):
    response = client.images.generate(prompt=prompt,
    n=1,
    size="256x256")
    print(response)
    result = response.data[0].url
    return result

def index(request):
    return render(request, 'gpt/index.html')

def chat(request):
    #post로 받은 question
    prompt = request.POST.get('question')


    #type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
    type = request.POST.get('type')
    if type == 'image':
        result = imageGPT(prompt)
    else:
        result = chatGPT(prompt)

    context = {
        'type': type,
        'question': prompt,
        'result': result
    }

    return render(request, 'gpt/result.html', context) 


class ImagesResponse:
    def __init__(self, created, data):
        self.created = created
        self.data = data