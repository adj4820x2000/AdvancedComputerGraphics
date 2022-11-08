import sys
from math import *
import numpy as np
from cv2 import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization

mouseLeftPressed = 0
mouseRightPressed = 0
clickPt = np.array([0,0])

transfMatrix = np.eye(4,dtype=float)    #預設位置
transfZoom = 60

lightAmbient = [ 0.7, 0.7, 0.7, 1.0 ]   #光線位置及設定
lightDiffuse = [ 1.0, 1.0, 1.0, 1.0 ]
lightSpecular = [ 1.0, 1.0, 1.0, 1.0 ]
lightPosition = [ 0, 0, 1000, 1.0 ]

windowWidth = 800
windowHeight = 600

Sphere = pywavefront.Wavefront('./sphere.obj')  #讀取已將前後景的圖貼上球體的模型

def display():
    PJT = 60000

    global transfMatrix
    transfMatrixT = np.transpose(transfMatrix)  #轉置旋轉矩陣
    matmatList = [transfMatrixT[i][j] for i in range(4) for j in range(4)]

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

    glViewport(0, 0, int(windowWidth/2.0), windowHeight)    #左鏡頭
    glFrustum(-float(windowWidth)/PJT, float(windowWidth)/PJT, -float(windowHeight)/PJT, float(windowHeight)/PJT, 1, 5000)
    gluLookAt(-transfZoom/10, 0, transfZoom, 0, 0, 0, 0, 1, 0)  #左鏡頭，向左移動一點產生視差

    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    
    glLoadMatrixf(matmatList)   #左鏡頭旋轉球體
    visualization.draw(Sphere)  #左鏡頭顯示球體

    glPopMatrix()
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

    glViewport(int(windowWidth/2.0), 0, int(windowWidth/2.0), windowHeight)  #右鏡頭
    glFrustum(-float(windowWidth)/PJT, float(windowWidth)/PJT, -float(windowHeight)/PJT, float(windowHeight)/PJT, 1, 5000)
    gluLookAt(transfZoom/10, 0, transfZoom, 0, 0, 0, 0, 1, 0)   #右鏡頭，向右移動一點產生視差

    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    
    glLoadMatrixf(matmatList)   #右鏡頭旋轉球體
    visualization.draw(Sphere)  #右鏡頭顯示球體

    glPopMatrix()
    glDisable(GL_LIGHTING)
    glutSwapBuffers()

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    global  transfMatrix, transfZoom
    if key == b'\x1b':      #按鍵盤"Esc"鍵可離開
        sys.exit()
    if key == b'f':         #按鍵盤"f"鍵，還原到預設位置
        transfZoom=60
        transfMatrix = np.eye(4,dtype=float)
        display()

def MouseFunc(button, state, x, y):     
    global mouseLeftPressed, mouseRightPressed, clickPt, transfZoom
    if state == 1:
        if button == 0:
            mouseLeftPressed = 0
    else:
        if button == 0:     #點擊滑鼠左鍵並移動，旋轉球體
            mouseLeftPressed = 1
        clickPt = np.array([x,y])

        if button==3:       #滑鼠滾輪前滑，放大球體
            if transfZoom > 2:
                transfZoom += -1
                display()
        if button==4:       #滑鼠滾輪後滑，縮小球體
            transfZoom += 1
            display()
    
def MouseMotion(x, y):  #計算旋轉矩陣
    global mouseLeftPressed, mouseRightPressed, clickPt, transfMatrix
    if mouseLeftPressed==1:
        dR = np.array( [ x-clickPt[0] , y-clickPt[1] ] )
        dxyz = np.array( [ transfMatrix[0][3] , transfMatrix[1][3], transfMatrix[2][3]] )
        rRatio = 100.0
        Tinv= np.array([ [ 1.0, 0.0, 0.0, -dxyz[0] ],\
                         [ 0.0, 1.0, 0.0, -dxyz[1] ],\
                         [ 0.0, 0.0, 1.0, -dxyz[2] ],\
                         [ 0.0, 0.0, 0.0,     1.0  ] ])
        T= np.array([ [ 1.0, 0.0, 0.0, dxyz[0] ],\
                      [ 0.0, 1.0, 0.0, dxyz[1] ],\
                      [ 0.0, 0.0, 1.0, dxyz[2] ],\
                      [ 0.0, 0.0, 0.0,    1.0  ] ])
        Rx = np.array([ [ 1.0, 0.0, 0.0, 0.0 ],\
                        [ 0.0, cos(dR[1]/rRatio), -sin(dR[1]/rRatio), 0.0 ],\
                        [ 0.0, sin(dR[1]/rRatio), cos(dR[1]/rRatio), 0.0 ],\
                        [ 0.0, 0.0, 0.0, 1.0 ] ])
        Ry = np.array([ [ cos(dR[0]/rRatio), 0.0, sin(dR[0]/rRatio), 0.0 ],\
                        [ 0.0, 1.0, 0.0, 0.0 ],\
                        [ -sin(dR[0]/rRatio), 0.0, cos(dR[0]/rRatio), 0.0 ],\
                        [ 0.0, 0.0, 0.0, 1.0 ] ])
        transfMatrix = Tinv.dot(transfMatrix)
        transfMatrix = Rx.dot(transfMatrix)
        transfMatrix = Ry.dot(transfMatrix)
        transfMatrix = T.dot(transfMatrix)
        display()
    clickPt = np.array([x,y])

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'Final project')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(MouseFunc)
glutMotionFunc(MouseMotion)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightAmbient)
glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
glutMainLoop()