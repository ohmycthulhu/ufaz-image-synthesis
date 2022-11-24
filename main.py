from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


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
    gluPerspective(40,1,4,20)


def lookat():
    # look point to the model
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5,5,5,0,0,0,0,1,0)


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


def drawCube(size):
    #draw cube
    glPushMatrix()
    glutSolidCube(size)
    glPopMatrix()

def drawCone(radius, height, slices, stacks):
    #draw Cone
    glTranslatef(0,1,0)
    glPushMatrix()
    glRotatef(-90,1,0,0)
    glutSolidCone(radius, height, slices, stacks)
    glPopMatrix()


def drawChimney(size):
    #draw Chimney
    glTranslatef(.75,.5,-.75)
    glPushMatrix()
    glScalef(1,3,1)
    glutSolidCube(size)
    glPopMatrix()


def drawCar():

    glTranslatef(0,-1,3.5)
    glPushMatrix()

    #Car body
    glPushMatrix()
    glScalef(2,.5,1)
    glutSolidCube(.5)
    glPopMatrix()
    glTranslatef(0,0,.25)
    glPushMatrix()
    glTranslatef(-.4,-.2,0)

    #wheel
    glutSolidTorus(.05,.1,8,8)
    glTranslatef(.8,0,0)
    glutSolidTorus(.05,.1,8,8)
    glPopMatrix()
    glTranslatef(0,0,-.5)
    glPushMatrix()
    glTranslatef(-.4,-.2,0)
    glutSolidTorus(.05,.1,8,8)
    glTranslatef(.8,0,0)
    glutSolidTorus(.05,.1,8,8)
    glPopMatrix()
    glPopMatrix()


def display():
    background()
    perspective()
    lookat()
    light()
    depth()
    drawCube(2)
    drawCone(1.5,1,16,8)
    drawChimney(0.25)
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

# Begin event loop
glutMainLoop()