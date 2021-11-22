import win32gui as wg
import win32con
import win32api as wp
import win32clipboard as wcp
import time
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import sys

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
hwnd = wg.FindWindow(None,"江西省妇幼保健院")
l,t,r,b = wg.GetWindowRect(hwnd)
wg.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,r-l,b-t,0)
wg.SetForegroundWindow(hwnd)
wg.ShowWindow(hwnd,win32con.SW_NORMAL)
window_img = ""

def click(p):    
    wp.SetCursorPos(p)
    time.sleep(wait_between_steps)
    wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0,0,0,0)

def step_forward(points,flag=True):    
    global state,state_index,hwnd,window_img
    for p in points:
        window_img = ""
        print("++++++++++++++切换新点+++++++++++++",p)
        if state[state_index]!=1 :
            wp.SetCursorPos(p)
            time.sleep(0.1)
            wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0,0,0,0)
            if flag:            
                # cv2.imshow("tmp",cv2.imread(window_img))
                # cv2.waitKey(0)
                print("~~~~~~~~~~~~找目标位置~~~~~~~~~~~~")
                nineAvailibleTmp = findPos(nineavai_img,0.90,True)
                if nineAvailibleTmp:
                    print("===========找到目标============")
                    return True
                # twoAvailibleTmp = findPos(twoavai_img,0.90,True)
                # if twoAvailibleTmp:
                #     return True
                # nineFullTmp = findPos(ninefull_img)
                # twoFullTmp = findPos(twofull_img)
                outWorkTmp = findPos(outWork_img)
                if state[state_index] == 0 :
                    # if nineFullTmp:
                    #     print("9无号")
                    #     state[state_index] += 0x02
                    # if twoFullTmp:
                    #     print("2无号")
                    #     state[state_index] += 0x04
                    if outWorkTmp:
                        print("无排班")
                        state[state_index] += 0x01
                    print("核查结束",state[state_index]) 
        print(state_index)           
        state_index+=1            
    return

# def step_forward(points,img,flag=True):
#     global state,state_index,hwnd
#     for p in points:
#         if flag:
#             img = screen.grabWindow(hwnd).toImage()
#             img.save("./dst_img/screenshot.jpg")
#             window_img  = "./dst_img/screenshot.jpg"
#             found = findPos(window_img,img,True)
#             if found:
#                 return True            
#         time.sleep(wait_between_steps)
#         wp.SetCursorPos(p)
#         wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0,0,0,0)
#     return

def findPos(dst_img="",val=0.97,c=False,h=40,w=360):
    global window_img
    wait_window_fresh = 0.5
    time.sleep(wait_window_fresh)
    if window_img == "":
        img = screen.grabWindow(hwnd).toImage()
        img.save("./dst_img/screenshot.png")
        window_img  = "./dst_img/screenshot.png"
    w_img = cv2.imread(window_img)
    w_img = cv2.cvtColor(w_img,cv2.COLOR_BGR2BGRA)
    d_img = cv2.imread(dst_img)
    d_img = cv2.cvtColor(d_img,cv2.COLOR_BGR2BGRA)
    res = cv2.matchTemplate(w_img,d_img,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
    print(max_val)
    if max_val>val:
        posX,posY = int(max_loc[0]+w),int(max_loc[1]+h)
        tmp_img = cv2.rectangle(w_img,(posX,posY),(posX+w,posY+h),(255,0,0),3)
        if c:
            click((posX,posY))    
        return True
    else:
        return False

# 日期[115,190] step 80
# 挂号[353,304] 后续需要根据opencv定位挂号按钮
# 选号[100,237]
# 勾选同意[28,655]
# 确定预约[200,721]
# 疫情表[30,381],[30,553],[30,724]
# 滚动后疫情表填写[30,167],[30,316],[30,485],[30,658]
# 提交按钮[202,714]
# 确定预约[200,721]
# 后退按钮[28,22]
# HPV疫苗门诊[240,270]        state_index=0

nineFull = False
twoFull = False


# 状态字：1、无排班；2、9无号；4、2无号；8、9未放号；16、2未放号；
state= [0,0,0,0,0,0,0,0,0,0,0]
state_index = 0
ninefull_img = "./jurdge/9full.png"
twofull_img = "./jurdge/2full.png"
outWork_img = "./jurdge/outWork.png"
nineavai_img= "./jurdge/9availible.png"
# twoavai_img= "./jurdge/2availible.png"
# nineavai_img= "./jurdge/test.png"
# twoavai_img= "./jurdge/test.png"
fenduan_img = "./jurdge/fenduan.png"
guahao_img = "./jurdge/guahao.png"
agree_img = "./jurdge/agree.png"
confirm_img = "./jurdge/confirm.png"


wait_between_steps = 0.5
# date_option = [[115,190],[195,190],[275,190],[355,190]]
date_option = [[115,190],[195,190],[275,190],[355,190]]
select_num=[[100,237]]
after_found = [[30,381],[30,553],[30,724]]
after_rollDown = [[30,167],[30,316],[30,485],[30,658],[202,714]]
bar_handle = [120,216]
bar_handle_back = [300,216]

while True:
    try:
        if step_forward(date_option):
            break
        wp.SetCursorPos(bar_handle)
        wp.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 120, 216, 0, 0)
        wp.mouse_event(win32con.MOUSEEVENTF_MOVE,150, 0,0,0)
        wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 300, 216, 0, 0)
        if step_forward(date_option):
            break
        # wp.SetCursorPos(bar_handle_back)
        # wp.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 120, 216, 0, 0)
        # wp.mouse_event(win32con.MOUSEEVENTF_MOVE,-150, 0,0,0)
        # wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 300, 216, 0, 0)
        step_forward([[28,22],[240,270]],False)
        state_index=0
    except KeyboardInterrupt:
        break
# 挂号至填报疫情信息表
while True:  
    window_img = ""
    time.sleep(wait_between_steps)  
    try:        
        fenduanTmp = findPos(fenduan_img,0.92)
        guahaoTmp = findPos(guahao_img,0.92)
        if fenduanTmp:
            step_forward(select_num,False)
            break
        if guahaoTmp:
            break
    except KeyboardInterrupt:
        break
img = screen.grabWindow(hwnd).toImage()
img.save("./dst_img/screenshot.jpg")
window_img  = "./dst_img/screenshot.jpg"
time.sleep(wait_between_steps)
window_img = ""
findPos(agree_img,0.93,True,18,18)
time.sleep(wait_between_steps)
window_img = ""
findPos(confirm_img,0.93,True,13,20)
time.sleep(wait_between_steps)
step_forward(after_found,False)
time.sleep(wait_between_steps)
# 滚动疫情表至最下端
wp.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1000)
# 挂号完成
time.sleep(wait_between_steps)
step_forward(after_rollDown,False)
window_img = ""
findPos(confirm_img,0.90,True,13,20)

