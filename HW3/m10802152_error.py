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
windowWidth = int(input("輸入圖片寬(Image Width):"))
windowHeight = int(input("輸入圖片長(Image Height):"))

if not(windowWidth > 0) or not(windowHeight > 0):   #預設值 寬:8000 長:6000
    windowWidth = 8000
    windowHeight = 6000
print(windowWidth, windowHeight)

BIGimg = np.zeros([windowHeight, windowWidth, 3], dtype = np.uint8)
a = 4000.0

model = pywavefront.Wavefront("./Dog.obj")    #讀取狗的模型檔，只有做狗的模型

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)

    global a
    #使用“perspective” projection方式做顯示
    glFrustum(-float(windowWidth)/a,float(windowWidth)/a,-float(windowHeight)/a,float(windowHeight)/a, 5, 4000)
    gluLookAt(0, windowHeight/40, 500, 0, windowHeight/40, 0, 0, 1, 0)

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

    widthRange = int(windowWidth/10)
    heightRange = int(windowHeight/10)
    bufferRange = widthRange * heightRange * 3
    colorBuffer = (GLubyte * bufferRange)(0)   #預設1440000 == 800*600*3

    #將圖片分解後，再次合併
    for i in range(10):
        for j in range(10):
            glReadPixels(j*widthRange, i*heightRange, widthRange, heightRange, GL_BGR, GL_UNSIGNED_BYTE, colorBuffer)
            imgColorflip = np.frombuffer(colorBuffer, np.uint8).reshape(heightRange, widthRange, 3)
            imgColor = cv2.flip(imgColorflip, 0)
            imshow("Display",imgColor)
            BIGimg[(9-i)*heightRange:(10-i)*heightRange, j*widthRange:(j+1)*widthRange] = imgColor
            waitKey(10)
    print("Render is complete, press 'ESC' to exit")
    glutSwapBuffers()

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b':      #按鍵盤"Esc"鍵可離開
        imwrite('BigImag.jpg', BIGimg)  #離開及輸出圖片
        sys.exit()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'MidtermProject')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()