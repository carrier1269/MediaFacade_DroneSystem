import speech_recognition as sr

# google translator 사용자화 라이브러리 호출
from my_lib import translate_lib

# kakao karlo model _ image generator 사용자화 라이브러리 호출
from my_lib import image_generator_lib

# API_key load
import os
from dotenv import load_dotenv

load_dotenv()

kakao_api_key =  os.environ.get('kakao_api_key')

# Google의 STT 기능을 구현한 함수입니다.
def my_stt() :
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("건물에 그리고싶은 원하는 그림을 말해줘! : ")
        audio = r.listen(source)
    
    mySpeech = r.recognize_google(audio, language='ko', show_all=True)
    try :
        return mySpeech
        
    except sr.UnknownValueError:
        print("Google 음성 인식이 오디오를 이해할 수 없습니다.")
    except sr.RequestError as e:
        print("Google 음성 인식 서비스에서 결과를 요청할 수 없습니다.; {0}".format(e))

while True :
    my_speech = my_stt()
    if my_speech == "종료" :
        break
    else :
        prompt = my_speech['alternative'][0]['transcript']

        prompt = '만화 그림체로' + prompt

        print(prompt)

        translated_prompt = translate_lib.en_to_kr(prompt)

        print(translated_prompt)
        
        AI_Image = image_generator_lib.image_generator_karlo(translated_prompt, kakao_api_key)

        AI_Image.save("generated_AI_Image/generated_img.png")