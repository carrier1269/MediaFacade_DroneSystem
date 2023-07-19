# drone_capstone

![image](https://github.com/carrier1269/drone_capstone/assets/58325946/c73fb1c6-7324-4cd1-a186-50eb5686a12c)
![image](https://github.com/carrier1269/drone_capstone/assets/58325946/13737a8e-9b5a-41a5-b2cf-6d66bde3c18c)
![image](https://github.com/carrier1269/drone_capstone/assets/58325946/15174fec-4cf8-4263-b328-ff226b99db21)

# Skills
## BashShell, Pixhawk4, HW(hardware), Python, Postman, Flask, Google-STT, Kakao karlo, Instance Segmentation, Mirroid

# Library
## bash_shell_auto // 한번에 프로그램을 관리할 수 있는 자동 프로그램 실행파일입니다.
### Auto_Flask.bat
### Auto_yolov5.bat

## drone_opencv // Mirroid 윈도우창을 실시간 캡쳐 및 송출하는 파일입니다.
### window.py

## my_lib // API를 사용하기 편리하게 사용자 라이브러리화 하였습니다.
### image_generator.py // kakao karlo api, 이미지 생성 모듈
### translate_lib.py // (prompt >> 영어 -> 한글) 전용 모듈

## yolov5 // latency를 최소화하기 위하여 yolov5 알고리즘을 사용하였습니다.
### segment/best.pt (segmentation model)
### segment/main_predict.py

## app.py (drone_cam.py + image_add.py + run_AI_STT.py) // my_lib폴더내의 라이브러리들을 상속받고 있습니다, Flask API 생성 파일입니다.
## craw.py // 데이터 크롤링