from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import sys
import win32gui as wg
for i in range(3):
    hwnd = wg.FindWindow(None,"江西省妇幼保健院")
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("screenshot{0}.jpg",str(i))