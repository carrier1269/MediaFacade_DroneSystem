import PySimpleGUI as sg
import win32gui
import win32com.client
import cv2
import numpy as np
import mss

# 접을 수 있는 행 추가 함수
def add_row(layout, key):
    return [sg.pin(sg.Column(layout, key=key, visible=False))]

# 윈도우에 실행중인 모든 창의 Text, handle을 list로 반환.
def get_win_list():
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            hwnd_list.append((title, hwnd))
        return True
    output = []
    win32gui.EnumWindows(callback, output)
    return output

# window handle로 이미지 위치 및 크기 찾는 함수
def get_win_size(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return left, top, right, bottom


shell = win32com.client.Dispatch("WScript.Shell")
def set_foreground(hwnd):
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd) # window handle로 창 앞으로 가져오기:

# 이미지 캡쳐하기
def get_win_image(x1, y1, x2, y2):
    # img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_RGB2BGR) # PIL VER
    with mss.mss() as sct: # mss로 캡처 수정 - 2022.03.08
        pos = {"left":x1, "top":y1, "width":x2-x1, "height":y2-y1}
        img = np.array(sct.grab(pos))
    return img

win_list = get_win_list()
win_text = [list[0] for list in win_list]
hwnd = None
run = False
s_1 = (10, None)  # 1st column size
s_b = (6, None) # Button size
s_i = (3, None) # Input size

sg.theme("Dark2")

lay_main = [
    [sg.Text("윈도우", size=s_1), sg.Combo(values=win_text, key="WIN", readonly=True, expand_x=True, enable_events=True)],
    [sg.Button("시작", size=s_b, key="START", expand_x=True, metadata=False), sg.Button("정지", size=s_b, key="STOP", expand_x=True)],
    [sg.Image(filename="", key="IMG")],
]

window = sg.Window('드론 AI 딥러닝', lay_main, grab_anywhere=True)

while True:
    evt, val = window.read(timeout=250)

    if evt == sg.WIN_CLOSED:
        break
    elif evt == "WIN":
        selected_text = window["WIN"].get()
        selected_text_idx = win_text.index(selected_text)
        hwnd = win_list[selected_text_idx][1]
        print("윈도우가 선택되었습니다. {}".format(hwnd))
    
    elif evt == "START":
        run = False if hwnd == None else True
        set_foreground(hwnd)

    elif evt == "STOP":
        run = False
    
    if run:
        x1, y1, x2, y2 = get_win_size(hwnd) # 윈도우 핸들로 게임창의 위치를 찾는다.
        fullImage = get_win_image(x1, y1, x2, y2) # 게임창 전체를 캡쳐한다.
        window["IMG"].update(data=cv2.imencode(".png", fullImage)[1].tobytes()) # 이미지 업데이트
            
window.close()