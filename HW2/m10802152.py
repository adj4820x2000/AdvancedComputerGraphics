import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

windowWidth = 800
windowHeight = 600

#定義需要使用到的變數，正確的分針、時針角度變數
Angle = 0
hourAngle = 0
minuteAngle = 0

allVertex=[[-25.0000,15.0000,1.0000],
[-15.0000,15.0000,1.0000],
[70.0000,110.0000,1.0000],
[-25.0000,25.0000,1.0000],
[-28.0610,20.0000,0.5000],
[-20.0000,11.9390,0.5000],
[84.7932,20.0000,0.5000],
[-20.0000,28.0610,0.5000],
[60.2126,-86.5632,0.0000],
[90.0000,-90.0000,0.0000],
[119.7874,-86.5632,0.0000],
[147.1424,-76.7753,0.0000],
[32.8576,-76.7753,0.0000],
[171.2812,-61.4200,0.0000],
[8.7188,-61.4201,0.0000],
[-11.4200,-41.2812,0.0000],
[191.4200,-41.2812,0.0000],
[206.7753,-17.1424,0.0000],
[216.5632,10.2126,0.0000],
[220.0000,40.0000,0.0000],
[216.5632,69.7874,0.0000],
[206.7753,97.1424,0.0000],
[191.4200,121.2812,0.0000],
[171.2812,141.4200,0.0000],
[147.1423,156.7753,0.0000],
[119.7874,166.5632,0.0000],
[90.0000,170.0000,0.0000],
[60.2126,166.5632,0.0000],
[32.8576,156.7753,0.0000],
[8.7188,141.4200,0.0000],
[-11.4201,121.2812,0.0000],
[-26.7753,97.1423,0.0000],
[-36.5632,69.7874,0.0000],
[-40.0000,40.0000,0.0000],
[-36.5632,10.2126,0.0000],
[-26.7753,-17.1424,0.0000]]

# 2 triangles，分針
minuteHand=[[0,1,2],[3,0,2]]

# 2 triangles，時針
hourHand=[[4,5,6],[7,4,6]]

# 26 triangles，時鐘
clockBody=[[8,9,10],
[8,10,11],
[12,8,11],
[12,11,13],
[14,12,13],
[15,14,13],
[15,13,16],
[15,16,17],
[15,17,18],
[15,18,19],
[15,19,20],
[15,20,21],
[15,21,22],
[15,22,23],
[15,23,24],
[15,24,25],
[15,25,26],
[15,26,27],
[15,27,28],
[15,28,29],
[15,29,30],
[15,30,31],
[15,31,32],
[15,32,33],
[15,33,34],
[15,34,35]]



def drawClock():
    glColor3f(1,1,1)
    glBegin(GL_TRIANGLES) 
    for fID in clockBody:
        glVertex3fv(allVertex[fID[0]])
        glVertex3fv(allVertex[fID[1]])
        glVertex3fv(allVertex[fID[2]])
    glEnd()


def drawhourHand():
    glColor3f(1,0,0)

    glTranslatef(90,40,0)		# 1.先將時針移到原點(0,0,0)
    glRotatef(hourAngle,0,0,1)	# 2.再進行旋轉
    glTranslatef(20,-20,0)		# 3.再移至時鐘中心(90,40,0)

    glBegin(GL_TRIANGLES) 
    for fID in hourHand:
        glVertex3fv(allVertex[fID[0]])
        glVertex3fv(allVertex[fID[1]])
        glVertex3fv(allVertex[fID[2]])
    glEnd()

def drawminuteHand():
    glColor3f(0,1,0)

    glTranslatef(-20,20,0)			# 1.先將分針移到原點(0,0,0)
    glRotatef(minuteAngle, 0, 0, 1) # 2.將分針旋轉至0分位置
    glRotatef(45, 0, 0, 1)			# 3.再進行旋轉
    glTranslatef(20,-20,0)			# 4.再跟時針重新疊合

    glBegin(GL_TRIANGLES) 
    for fID in minuteHand:
        glVertex3fv(allVertex[fID[0]])
        glVertex3fv(allVertex[fID[1]])
        glVertex3fv(allVertex[fID[2]])
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    global Angle, minuteAngle, hourAngle
    Angle = Angle - 1						#計算分針跟時針的合理移動角度
    if Angle % 12 == 0:						#速率約差60倍，以1度為單位
        hourAngle = hourAngle - 1			#由於時針旋轉時，分針會跟著轉，
    minuteAngle = Angle - hourAngle			#所以需將分針被時針移動的角度扣掉
    if Angle % 360 == 0:
        Angle = 0							#當分針或時針轉一圈，歸零
    if hourAngle % 360 == 0:				#避免出現錯誤
        hourAngle = 0

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)
    glOrtho(-float(windowWidth)/2.0,float(windowWidth)/2.0,-float(windowHeight)/2.0,float(windowHeight)/2.0,-windowHeight*10.0,windowHeight*10.0)
    glPushMatrix()
    drawClock()
    drawhourHand()
    drawminuteHand()
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
glutCreateWindow(b'Homework2')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()