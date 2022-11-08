import sys
from math import *
from cv2 import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

windowWidth = 800
windowHeight = 600

Vertex = [] #Vertex, Vertex Normal, Texture Coordinate
VNomal = []
VTex = []

def draw(radius, stacks, slices):   #畫球體及計算U-V texture coordinates
    r = radius
    glColor3f(255, 255, 255)
    glBegin(GL_QUAD_STRIP)

    for i in range(stacks):
        sta0 = pi*(-0.5 + i/stacks) #degree -90 ~ 90
        z0   = sin(sta0)
        zr0  = cos(sta0)

        sta1 = pi*(-0.5 + (i+1)/stacks)
        z1  = sin(sta1)
        zr1 = cos(sta1)

        
        for j in range(slices):
            sli = 2*pi*(j)/slices   #degree 0 ~ 360
            x = cos(sli)
            y = sin(sli)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(r * x * zr0, r * y * zr0, r * z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(r * x * zr1, r * y * zr1, r * z1)

            Vnx = x * zr0
            Vny = y * zr0
            Vnz = z0
            Vx = r * Vnx
            Vy = r * Vny
            Vz = r * Vnz

            f_u = (Vx*0.802 + 1) / 2.0  #由於相機視角超過180度,
            f_v = (Vy*0.802 + 1) / 2.0  #將U-V texture coordinates大概調整到180度位置上

            if(len(Vertex) < 32*32):
                Vertex.append([round(Vx, 4), round(Vy, 4), round(Vz, 4)])
                VNomal.append([round(Vnx, 4), round(Vny, 4), round(Vnz, 4)])
                VTex.append([round(f_u, 4), round(f_v, 4), round(0.0, 4)])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)
    glFrustum(-float(windowWidth)/400, float(windowWidth)/400, -float(windowHeight)/400, float(windowHeight)/400, 5, 4000)
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [ 0.0,0.0,0.0,1.0 ])       #光線位置及設定
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [ 1.0,1.0,1.0,1.0 ])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [ 1.0,1.0,1.0, 1.0 ])
    glLightfv(GL_LIGHT0, GL_POSITION,  [ 0.0,1000.0,0.0,1.0 ])
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glPushMatrix()

    draw(1.0, 32, 32)   #僅有顯示空白球體，並未畫上Texture

    glPopMatrix()
    glDisable(GL_LIGHTING)
    glutSwapBuffers()

    print("Complete, press 'ESC' to save 'obj and mtl file' and exit")

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b':      #按鍵盤"Esc"鍵可離開，並保存obj、mtl檔
        obj_out = "./sphere.obj"
        mtl_out = "./sphere.mtl"

        img = cv2.imread("./FRONT.JPG")     #將前景圖進行左右翻轉，
        img = cv2.flip(img, 1)              #以利U-V texture coordinates方便計算
        cv2.imwrite("./FRONT_flip.JPG", img)

        with open(obj_out, 'w') as f:       #計算所有face(三角)順序，並輸出obj檔
            f.write("mtllib sphere.mtl\n\n")
            f.write("# OBJ file\n\n")
            for v in range(len(Vertex)):
                f.write("v {} {} {}\n".format(Vertex[v][0], Vertex[v][1], Vertex[v][2]))
            f.write("# {} vertices\n\n".format(len(Vertex)))
            for v in range(len(VNomal)):
                f.write("vn {} {} {}\n".format(VNomal[v][0], VNomal[v][1], VNomal[v][2]))
            f.write("# {} vertex normals\n\n".format(len(VNomal)))
            for v in range(len(VTex)):
                f.write("vt {} {} {}\n".format(VTex[v][0], VTex[v][1], VTex[v][2]))
            f.write("# {} texture coords\n\n".format(len(VTex)))

            f.write("o Object__0\ng Object__0\nusemtl Material__1\n".format(len(VNomal)))
            for j in range(1, 32):
                f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(1, 1, 1, j+33, j+33, j+33, j+32, j+32, j+32))
            f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(1, 1, 1, 33, 33, 33, 32*2, 32*2, 32*2))
            for i in range(1, 16):
                for j in range(1, 32):
                    f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*i+j, 32*i+j, 32*i+j, 32*(i+1)+j+1, 32*(i+1)+j+1, 32*(i+1)+j+1, 32*(i+1)+j, 32*(i+1)+j, 32*(i+1)+j))
                    f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*i+j, 32*i+j, 32*i+j, 32*i+j+1, 32*i+j+1, 32*i+j+1, 32*(i+1)+j+1, 32*(i+1)+j+1, 32*(i+1)+j+1))
                f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*(i+1), 32*(i+1), 32*(i+1), 32*(i+1)+1, 32*(i+1)+1, 32*(i+1)+1, 32*(i+2), 32*(i+2), 32*(i+2)))
                f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*(i+1), 32*(i+1), 32*(i+1), 32*i+1, 32*i+1, 32*i+1, 32*(i+1)+1, 32*(i+1)+1, 32*(i+1)+1))
          
            f.write("o Object__0\ng Object__0\nusemtl Material__2\n".format(len(VNomal)))
            for i in range(16, 31):
                for j in range(1, 32):
                    f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*i+j, 32*i+j, 32*i+j, 32*(i+1)+j+1, 32*(i+1)+j+1, 32*(i+1)+j+1, 32*(i+1)+j, 32*(i+1)+j, 32*(i+1)+j))
                    f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*i+j, 32*i+j, 32*i+j, 32*i+j+1, 32*i+j+1, 32*i+j+1, 32*(i+1)+j+1, 32*(i+1)+j+1, 32*(i+1)+j+1))
                f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*(i+1), 32*(i+1), 32*(i+1), 32*(i+1)+1, 32*(i+1)+1, 32*(i+1)+1, 32*(i+2), 32*(i+2), 32*(i+2)))
                f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*(i+1), 32*(i+1), 32*(i+1), 32*i+1, 32*i+1, 32*i+1, 32*(i+1)+1, 32*(i+1)+1, 32*(i+1)+1))
            for i in range(30):
                f.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(32*31+1, 32*31+1, 32*31+1, 32*31+i+2, 32*31+i+2, 32*31+i+2, 32*31+i+3, 32*31+i+3, 32*31+i+3))
            
        with open(mtl_out, 'w') as f:   #輸出mtl檔
            f.write("newmtl Material__1\n\tKa 0.2 0.2 0.2\n\tKd 0.9 0.9 0.9\n\tKs 1.0 1.0 1.0\n\tillum 2\n\tNs 25.6\n")
            f.write("\tmap_Kd ./FRONT_flip.JPG\n\n")

            f.write("newmtl Material__2\n\tKa 0.2 0.2 0.2\n\tKd 0.9 0.9 0.9\n\tKs 1.0 1.0 1.0\n\tillum 2\n\tNs 25.6\n")
            f.write("\tmap_Kd ./REAR.JPG\n")

        sys.exit()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'Final project')
glutReshapeWindow(windowWidth, windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()