from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import time

camera_rot_angle = math.pi / 4
camera_distance = 5 * math.sqrt(2)
car_distance = 0
car_speed = 0.1


def background():
    # Set the background color of the window to black
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def perspective():
    # establish the projection matrix (perspective)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Get the viewport to use it in choosing the aspect ratio of gluPerspective
    # _,_,width,height = glGetDoublev(GL_VIEWPORT)
    width = 500
    height = 500
    gluPerspective(40, 1, 4, 20)


def lookat():
    # look point to the model
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        camera_distance * math.sin(camera_rot_angle),
        5,
        camera_distance * math.cos(camera_rot_angle),
        0, 0, 0,
        0, 1, 0
    )


def light():
    # Setup light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, GLfloat_4(0.2, 0.2, 0.1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_4(0.8, 0.8, 0.7, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, GLfloat_4(1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0.0, 2, 7.0, 0.0))

    # Setup light 1
    glLightfv(GL_LIGHT1, GL_AMBIENT, GLfloat_4(0.1, 0, 0, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_4(0.2, 0, 0, 0.5))
    glLightfv(GL_LIGHT1, GL_SPECULAR, GLfloat_4(0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(0.0, -7.0, 0.0))

    # Enable lighting
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, GLfloat_4(0.2, 0.2, 0.2, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def depth():
    # Setup depth
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)


def coneMaterial():
    # Setup material for cone
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0.125, 0.125, 0.32, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.875, 0.875, 0.68, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.0, 0.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, GLfloat(10.0))


def cubeMaterial():
    # Setup material for cone
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0.125, 0.125, 0.32, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.875, 0.875, 0.68, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.0, 1.0, 1.0, 0.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, GLfloat(25.0))


def drawHome():
    glPushMatrix()

    glTranslate(0, 0, -0.5)
    glutSolidCube(2)
    drawCone(1.5, 1, 16, 8)
    drawChimney(0.25)

    glPopMatrix()

def drawCube(size):
    glutSolidCube(size)


def drawCone(radius, height, slices, stacks):
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(radius, height, slices, stacks)
    glPopMatrix()


def drawChimney(size):
    glPushMatrix()
    glTranslatef(0.5, 1.5, -0.5)
    glScalef(1, 4, 1)
    glutSolidCube(size)
    glPopMatrix()


def drawCar():
    glPushMatrix()
    glTranslatef(car_distance, 0, 2.5)  # Car position

    # Car body
    glPushMatrix()
    glScalef(2, .5, 1)
    glutSolidCube(.5)
    glPopMatrix()

    # wheel
    glPushMatrix()
    glTranslatef(0, 0, .25)

    glPushMatrix()
    glTranslatef(-.4, -.2, 0)
    glutSolidTorus(.05, .1, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(.4, -.2, 0)
    glutSolidTorus(.05, .1, 8, 8)
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, -.25)

    glPushMatrix()
    glTranslatef(-.4, -.2, 0)
    glutSolidTorus(.05, .1, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(.4, -.2, 0)
    glutSolidTorus(.05, .1, 8, 8)
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()


def idle_func():
    global car_distance, car_speed

    car_distance += car_speed

    if car_distance > 5:
        car_speed = -abs(car_speed)
    elif car_distance < -5:
        car_speed = abs(car_speed)

    glutPostRedisplay()
    time.sleep(0.016)


def on_keydown(key, *args):
    global camera_rot_angle, camera_distance
    if key == GLUT_KEY_RIGHT:
        camera_rot_angle += 0.1
    elif key == GLUT_KEY_LEFT:
        camera_rot_angle -= 0.1

    new_distance = camera_distance

    if key == GLUT_KEY_UP:
        new_distance -= 0.1
    elif key == GLUT_KEY_DOWN:
        new_distance += 0.1

    camera_distance = max(min(new_distance, 10), 3)

    glutPostRedisplay()



def display():
    background()
    perspective()
    lookat()
    light()
    depth()
    drawHome()
    drawCar()
    coneMaterial()
    cubeMaterial()
    glutSwapBuffers()


# Initialize GLUT
glutInit()

# Initialize the window with double buffering and RGB colors
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

# Set the window size to 500x500 pixels
glutInitWindowSize(500, 500)

# Create the window and give it a title
glutCreateWindow("Drawing a 3D house and a car with lights")

glClearColor(0.0, 0.0, 0.0, 0.0)

# Set the initial window position to (50, 50)
glutInitWindowPosition(50, 50)

# Define display callback
glutDisplayFunc(display)
glutIdleFunc(idle_func)
glutSpecialFunc(on_keydown)

# Begin event loop
glutMainLoop()
