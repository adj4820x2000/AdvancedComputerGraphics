import sys
from math import *
import numpy as np
from cv2 import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization

#輸入欲輸出的圖片長、寬
imageWidth = int(input("輸入圖片寬(Image Width):"))
imageHeight = int(input("輸入圖片長(Image Height):"))

if not(imageWidth > 0) or not(imageHeight > 0):   #預設值 寬:8000 長:6000
    imageWidth = 8000
    imageHeight = 6000
print(imageWidth, imageHeight)

windowWidth = int(imageWidth/10)    #將視窗長、寬設定在圖片的1/10
windowHeight = int(imageHeight/10)

BIGimg = np.zeros([imageHeight, imageWidth, 3], dtype = np.uint8)
Xstep = 0
Ystep = 0
XcropSize = 2*0.2
YcropSize = 2*0.2/windowWidth*windowHeight

model = pywavefront.Wavefront("./Dog.obj")    #讀取狗的模型檔，只有做狗的模型

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)

    global Xstep, Ystep
    #使用“perspective” projection方式做顯示
    #並且調整成視窗顯示的範圍
    glFrustum(-XcropSize*5+Xstep*XcropSize, -XcropSize*4+Xstep*XcropSize, YcropSize*4-Ystep*YcropSize, YcropSize*5-Ystep*YcropSize, 5, 4000)

    gluLookAt(0, 150, 500, 0, 150, 0, 0, 1, 0)   

    M = [[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0., 0., 0., 1.]]    #將模型旋轉
    RMinv1 = np.linalg.inv(M)
    MT = np.transpose(RMinv1)   #記得要轉置
    matmatList = [MT[i][j] for i in range(4) for j in range(4)]

    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    glLoadMatrixf(matmatList)   #畫上狗的模型，並旋轉
    visualization.draw(model)

    glPopMatrix()
    glDisable(GL_LIGHTING)

    #將被分成好幾塊的圖片，合併
    bufferRange = windowWidth * windowHeight * 3
    colorBuffer = (GLubyte * bufferRange)(0)   #預設1440000 == 800*600*3

    glReadPixels(0, 0, windowWidth, windowHeight, GL_BGR, GL_UNSIGNED_BYTE, colorBuffer)
    imgColorflip = np.frombuffer(colorBuffer, np.uint8).reshape(int(windowHeight), int(windowWidth), 3)
    imgColor = cv2.flip(imgColorflip, 0)
    BIGimg[Ystep*windowHeight:(Ystep+1)*windowHeight, Xstep*windowWidth:(Xstep+1)*windowWidth] = imgColor
 
    Xstep += 1      #紀錄視窗目前顯示位置
    if Xstep > 9:
        Xstep = 0
        Ystep += 1
        if Ystep > 9:
            Ystep = 0
            print("Render is complete, press 'ESC' to save 'BigImage' and exit")

    glutSwapBuffers()
    glutPostRedisplay()

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b':      #按鍵盤"Esc"鍵可離開
        imwrite('BigImage.jpg', BIGimg)  #離開及輸出圖片
        sys.exit()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'HW3')
glutReshapeWindow(windowWidth, windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()