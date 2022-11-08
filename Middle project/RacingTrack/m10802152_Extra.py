import sys
from math import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization

windowWidth = 800
windowHeight = 600

step = 0
Car = pywavefront.Wavefront('./Chevrolet_Camaro_SS_Low.obj')    #讀車子、跑道模型檔
Track = pywavefront.Wavefront('./FullTrack.obj')

with open('./Path.xyz', 'r') as PathFile:   #讀車子行經的路徑
    lines = PathFile.readlines()

Path=[]
for i in range(len(lines)):
    line = lines[i]
    line = line.replace('\n', '')
    line = line.split(' ')
    line = list(map(float, line))
    Path.append(line)

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)

    global step
    step = step + 1     #紀錄目前行經到的位置

    if(step == len(Path)):  #當已行至路徑尾，讓車子從頭開始
        step=0              #使車子能一直繞跑道行駛

    if(step == 0):
        Tx = Path[step][0]-Path[len(Path)-1][0] #計算正在行經的點與前一點的
        Ty = Path[step][1]-Path[len(Path)-1][1] #X、Y、Z的變化量
        Tz = Path[step][2]-Path[len(Path)-1][2] #還有2D距離
        dist = sqrt(pow(Tx, 2) + pow(Ty,2))
    else:
        Tx = Path[step][0]-Path[step-1][0]
        Ty = Path[step][1]-Path[step-1][1]
        Tz = Path[step][2]-Path[step-1][2]
        dist = sqrt(pow(Tx, 2) + pow(Ty,2))

    theta = degrees(atan2(Ty, Tx))      #利用X、Y的變化量計算出方位角度    
    phi = degrees(atan2(Tz, dist))      #利用Z的變化量與2D距離算出傾斜角度
    
    #利用glFrustum函式，達到有現實畫面的樣子
    glFrustum(-float(windowWidth)/400, float(windowWidth)/400, -float(windowHeight)/400, float(windowHeight)/400, 5, 4000)
    #調整相機的觀看位置及角度，以達到相機放在車前的畫面
    gluLookAt(Path[step][0]+sin(radians(theta))*4, Path[step][1]-cos(radians(theta))*4, Path[step][2]+3,
               Path[step][0]+sin(radians(theta))*4+cos(radians(theta))*50, Path[step][1]-cos(radians(theta))*4+sin(radians(theta))*50, Path[step][2]+sin(radians(phi))*3,
               0, 0, 1)

    ###移動車子所用到的Matrix###
    M = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0., 0., 0., 1.]]    #1.將車子轉到正確方向
    RMinv1 = np.linalg.inv(M)

    M = [[1, 0, 0, 0], [0, 1, 0, -4], [0, 0, 1, 1.5], [0., 0., 0., 1.]] #2.將車子移到右車道及正確高度
    TM1 = np.array(M)

    #3.調整車子方位及傾斜角度
    w = np.array([-sin(radians(theta))*sin(radians(phi)), -cos(radians(theta))*sin(radians(phi)), cos(radians(phi))])
    w = w / np.linalg.norm(w)
    V = np.array([ sin(radians(theta))*cos(radians(phi)),  cos(radians(theta))*cos(radians(phi)), sin(radians(phi))])
    u = np.cross(V,w)
    u = u / np.linalg.norm(u)
    v = np.cross(w,u)
    M = [[u[0], v[0], w[0], 0],[u[1], v[1], w[1], 0], [u[2], v[2], w[2], 0], [0., 0., 0., 1.]]
    RMinv2 = np.linalg.inv(M)

    #4.將車子放到該行經的點
    M = [[1, 0, 0, Path[step][0]], [0, 1, 0, Path[step][1]], [0, 0, 1, Path[step][2]], [0., 0., 0., 1.]]
    TM2 = np.array(M)

    M = TM2.dot(RMinv2).dot(TM1).dot(RMinv1)    #將所有用到的Matrix相乘出最後的Matrix
    MT = np.transpose(M)                        #記得要轉置
    matmatList = [MT[i][j] for i in range(4) for j in range(4)]

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    visualization.draw(Track)   #畫上車子
    glLoadMatrixf(matmatList)   #再調整車子方向及位置
    visualization.draw(Car)     #最後畫上跑道

    glPopMatrix()
    glutSwapBuffers()
    glutPostRedisplay()  

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b':		#修正按鍵盤"Esc"鍵可離開
        sys.exit()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'MidtermProject')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()