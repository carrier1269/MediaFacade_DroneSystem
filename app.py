from flask import Flask, render_template, Response
import threading
import cv2
from drone_opencv import window
import cv2
import win32gui

# run_AI_STT.py >> Libraries

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

app = Flask(__name__)

output_frame = None
lock = threading.Lock()

def capture_frames():
    global output_frame
    ESC_KEY = 27
    FRAME_RATE = 120
    SLEEP_TIME = 1 / FRAME_RATE

    capture = window.WindowCapture("drone_python", FRAME_RATE)

    while True:
        _, frame = capture.screenshot()
        with lock:
            output_frame = frame.copy()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global output_frame
    while True:
        with lock:
            if output_frame is None:
                continue

            flag, encoded_image = cv2.imencode('.jpg', output_frame)
            if not flag:
                continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/AI_gen_image', methods=['POST'])
def generator_image():
    # Google의 STT 기능을 구현한 함수입니다.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("건물에 그리고싶은 원하는 그림을 말해줘! : ")
        audio = r.listen(source)
        
    mySpeech = r.recognize_google(audio, language='ko', show_all=True)

    # javascript setinterval & clearinterval 구현
    # 음성 입력시 동작, 이미지 생성시 반복문 제거

    status = None
    while(status == None):
        try :
            prompt = mySpeech['alternative'][0]['transcript']

            print(prompt)

            prompt = '만화 그림체로 ' + prompt

            print(prompt)

            translated_prompt = translate_lib.en_to_kr(prompt)

            print(translated_prompt)
                    
            AI_Image = image_generator_lib.image_generator_karlo(translated_prompt, kakao_api_key)

            AI_Image.save("generated_AI_Image/generated_img.png")

            status = True

            return f'{prompt} 그림이 생성되었습니다.'
                
        except sr.UnknownValueError:
            print("Google 음성 인식이 오디오를 이해할 수 없습니다.")
        except sr.RequestError as e:
            print("Google 음성 인식 서비스에서 결과를 요청할 수 없습니다.; {0}".format(e))

    

if __name__ == '__main__':
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.start()
    app.run(host='0.0.0.0', port=5000)