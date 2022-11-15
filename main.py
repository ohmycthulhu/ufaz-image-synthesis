from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class DrawAt:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __enter__(self):
        glPushMatrix()
        glTranslate(self._x, self._y, self._z)

    def __exit__(self, exc_type, exc_val, exc_tb):
        glPopMatrix()


class Object:
    def __init__(self, vertices, edges, mode=GL_TRIANGLES):
        self._vertices = vertices
        self._edges = edges
        self._mode = mode

    def draw(self, x, y, z):
        with DrawAt(x, y, z):
            for edge in self._edges:
                glBegin(self._mode)
                for vertex_index in edge:
                    glVertex3f(*self._vertices[vertex_index])
                glEnd()


def background():
    # Set the background color of the window to Gray
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
    gluPerspective(45, width / height, 1, 200)


def lookat():
    # and then the model view matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(9, 7, -8, -2.5, 3, 5, 0, 1, 0)


def light():
    # TODO: Change to the actual light
    # Setup light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, GLfloat_4(0.2, 0.2, 0.1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_4(0.8, 0.8, 0.7, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, GLfloat_4(1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0.0, 0, 7.0, 0.0))

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
    # Setup depth testing
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)


def display():
    background()
    perspective()
    lookat()

    cube = Object(
        vertices=[(-1, 0, 1), (-1, 2, 1), (-1, 0, 2), (-1, 2, 2)],
        edges=[(2, 1, 0), (2, 3, 1)],
    )

    cube.draw(0, 0, 0)
    # light()
    depth()
    glutSwapBuffers()


# Initialize GLUT
glutInit()

# Initialize the window with double buffering and RGB colors
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

# Set the window size to 500x500 pixels
glutInitWindowSize(500, 500)

# Create the window and give it a title
glutCreateWindow("Drawing a 3D cone and a sphere with lights")

glClearColor(0.0, 0.0, 0.0, 0.0)

# Set the initial window position to (50, 50)
glutInitWindowPosition(50, 50)

# Define display callback
glutDisplayFunc(display)

# Begin event loop
glutMainLoop()
