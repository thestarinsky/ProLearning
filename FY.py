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
hwnd = wg.FindWindow(None,"江西省妇幼保健院")
l,t,r,b = wg.GetWindowRect(hwnd)
wg.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,r-l,b-t,0)
wg.SetForegroundWindow(hwnd)
wg.ShowWindow(hwnd,win32con.SW_NORMAL)

screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()
img.save("/dst_img/screenshot.jpg")

# 门诊挂号[75,351]

# 广告[385,102]

# 成人就诊[200,120]
# 提示框[136,436]
# 八一[351,192] 九龙湖[233,477]
# 提示框[184,378]
# 搜索框[159,159]
# 调用剪贴板进行输入
# 查询[379,163]
# 科室[310,230]
# 选择科室[158,324]
# 滚动条[120,216]
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


step_points = [[75,351],[385,102],[200,120],[136,436],[351,192],[184,378],[159,159]]
after_search= [[379,163],[310,230],[158,324],[115,190],[195,190],[275,190],[355,190]]
after_drag = [[115,190],[195,190],[275,190],[355,190]]
after_found = [[353,304],[100,237],[28,655],[200,721],[30,381],[30,553],[30,724]]
after_rollDown = [[30,167],[30,316],[30,485],[30,658],[202,714],[200,721]]
bar_handle = [120,216]
bar_dis_x = 180
step_deepth = 0
wait_between_steps = 0.5
def step_forward(points):
    for p in points:
        time.sleep(wait_between_steps)
        wp.SetCursorPos(p)
        wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN ,0,0,0,0)
    return
def setCopy(str):
    wcp.OpenClipboard()
    wcp.EmptyClipboard()
    wcp.SetClipboardData(win32con.CF_UNICODETEXT, str)
    wcp.CloseClipboard()
# 设置关键字
setCopy("HPV")
# 首页至科室选择页面
step_forward(step_points)
# 粘贴关键字
wp.keybd_event(0x11, 0, 0, 0)
wp.keybd_event(0x56, 0, 0, 0)
wp.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
wp.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(wait_between_steps)
# 根据查询结果到挂号（切换当前页面日期）
step_forward(after_search)
# 拖动滚动条至最右侧
wp.SetCursorPos(bar_handle)
wp.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 120, 216, 0, 0)
time.sleep(wait_between_steps)
wp.mouse_event(win32con.MOUSEEVENTF_MOVE,180, 0,0,0)
wp.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 300, 216, 0, 0)
# 切换日期
step_forward(after_drag)
# 找到指定目标后挂号
found = True
if found :
    # 挂号至填报疫情信息表
    step_forward(after_found)
    # 滚动疫情表至最下端
    wp.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1000)
    # 挂号完成
    step_forward(after_rollDown)



