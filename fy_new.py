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
import os

wait_between_steps = 0.5
app = QApplication(sys.argv)
try:
    hwnd = wg.FindWindow(None,"江西省妇幼保健院")
except:
    print("window not found")
l,t,r,b = wg.GetWindowRect(hwnd)
wg.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,r-l,b-t,0)
wg.SetForegroundWindow(hwnd)
wg.ShowWindow(hwnd,win32con.SW_NORMAL)
screen = QApplication.primaryScreen()

step = 0
dst_img = []
for root, dirs, files in os.walk("./dst_img"):  
        for file in files:  
            if os.path.splitext(file)[1] == '.JPG' or os.path.splitext(file)[1] == '.jpg':  
                dst_img.append(os.path.join(root, file))
                try:
                    step = int(os.path.splitext(file)[0].split(".")[0])
                except:
                    pass
def setCopy(str):
    wcp.OpenClipboard()
    wcp.EmptyClipboard()
    wcp.SetClipboardData(win32con.CF_UNICODETEXT, str)
    wcp.CloseClipboard()

def findPos(window_img="",dst_img=""):
    w_img = cv2.imread(window_img)
    d_img = cv2.imread(dst_img)
    h,w = d_img.shape[:2]
    res = cv2.matchTemplate(w_img,d_img,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
    if max_val>0.90:
        posX,posY = int(max_loc[0]+0.5*w),int(max_loc[1]+0.5*h)
        step_forward([[posX,posY]])
        return True
    else:
        return False

def step_forward(points):
    for p in points:        
        wp.SetCursorPos(p)
        time.sleep(wait_between_steps)
        wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0,0,0,0)
    return

p_index = 0
while True:
    # 设置第一次比较    
    try:
        hint_hwnd = wg.FindWindow(None,"提示")        
    except:
        pass
    if hint_hwnd:
        l,t,r,b = wg.GetWindowRect(hint_hwnd)
        wg.SetWindowPos(hint_hwnd,win32con.HWND_TOPMOST,0,0,r-l,b-t,0)
        wg.SetForegroundWindow(hint_hwnd)
        wg.ShowWindow(hint_hwnd,win32con.SW_NORMAL)
        img = screen.grabWindow(hint_hwnd).toImage()
        img.save("./dst_img/screenshot.jpg")
        window_img  = "./dst_img/screenshot.jpg"
    else: 
        img = screen.grabWindow(hwnd).toImage()
        img.save("./dst_img/screenshot.jpg")
        window_img  = "./dst_img/screenshot.jpg"
    next = findPos(window_img,dst_img[p_index])
    # 如果没有找到，则刷新，并且步骤减1
    if not next:
        p_index+=1
        skip = findPos(window_img,dst_img[p_index])
        if not skip:
            p_index-=1
            i=0
            while i<5:
                if findPos(window_img,dst_img[p_index]):
                    break
                time.sleep(1)
                i+=1
            step_forward([[28,22]])
            while not next: 
                img = screen.grabWindow(hwnd).toImage()
                img.save("./dst_img/screenshot.jpg")
                window_img  = "./dst_img/screenshot.jpg"
                next = findPos(window_img,dst_img[p_index])
        else:p_index+=1            
    else:p_index+=1
# 如果找到则进行下一步

setCopy("HPV")
step_forward([[159,159]])
wp.keybd_event(0x11, 0, 0, 0)
wp.keybd_event(0x56, 0, 0, 0)
wp.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
wp.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(wait_between_steps)

