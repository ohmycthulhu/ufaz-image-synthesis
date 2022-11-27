from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import time


class Car:
    def __init__(self, x, y, z, speed, x_lims):
        self._x = x
        self._x_lims = x_lims
        self._y = y
        self._z = z
        self._speed = speed

    def move(self):
        self._x += self._speed

        if self._x < self._x_lims[0]:
            self._speed = abs(self._speed)
        if self._x > self._x_lims[1]:
            self._speed = -abs(self._speed)

    def draw(self):
        glPushMatrix()
        glTranslatef(self._x, self._y, self._z)  # Car position

        # Car body
        glPushMatrix()
        glScalef(2, .5, 1)
        glutSolidCube(.5)
        glPopMatrix()

        for z_mul in [-1, 1]:
            glPushMatrix()
            # Position the wheel to the left or right
            glTranslatef(0, 0, 0.25 * z_mul)

            for x_mul in [-1, 1]:
                # Position the wheel to the front or back
                glPushMatrix()
                glTranslatef(.4 * x_mul, -.2, 0)
                glutSolidTorus(.05, .1, 8, 8)
                glPopMatrix()

            glPopMatrix()

        # Draw the salon
        glPushMatrix()
        glTranslate(0, .25, 0)
        glScalef(1, .5, 1)
        glutSolidCube(.5)
        glPopMatrix()

        glPopMatrix()


car = Car(0, (.5+.1) / 2, 2.5, speed=0.1, x_lims=(-5, 5))


class Camera:
    def __init__(self, center, up, min_distance, max_distance, distance=None, angle=0.0):
        self._distance = distance if distance is not None else (max_distance + min_distance) / 2
        self._center = center
        self._up = up
        self._angle = angle
        self._max_distance = max_distance
        self._min_distance = min_distance

    def lookat(self, point):
        # Calculate the camera position based on the current rotation
        x, y, z = self._center
        x += self._distance * math.sin(self._angle)
        z += self._distance * math.cos(self._angle)

        gluLookAt(
            x,
            y,
            z,
            *point,
            *self._up
        )

    def rotate(self, d_angle):
        self._angle += d_angle

    def move(self, distance_change):
        new_distance = self._distance

        new_distance += distance_change

        self._distance = max(min(new_distance, self._max_distance), self._min_distance)


camera = Camera(
    center=(0, 5, 0),
    up=(0, 1, 0),
    min_distance=3, max_distance=15,
    angle=(math.pi / 4)
)


class Light:
    def __init__(self, intensity_ambient, intensity_diffuse, intensity_specular):
        self._intensity_ambient = intensity_ambient
        self._intensity_diffuse = intensity_diffuse
        self._intensity_specular = intensity_specular

    def _setup(self, position, id):
        glLightfv(id, GL_AMBIENT, GLfloat_4(*self._intensity_ambient))
        glLightfv(id, GL_DIFFUSE, GLfloat_4(*self._intensity_diffuse))
        glLightfv(id, GL_SPECULAR, GLfloat_4(*self._intensity_specular))
        glLightfv(id, GL_POSITION, GLfloat_4(*position))

        glEnable(id)


class PositionedLight(Light):
    def __init__(self, intensity_ambient, intensity_diffuse, intensity_specular, position):
        super().__init__(intensity_ambient, intensity_diffuse, intensity_specular)

        self._position = position

    def setup(self, id):
        self._setup(self._position, id)


class RotatingLight(Light):
    def __init__(self, intensity_ambient, intensity_diffuse, intensity_specular, center, distance, angle=0.0):
        super().__init__(intensity_ambient, intensity_diffuse, intensity_specular)

        self._center = center
        self._distance = distance
        self._angle = angle

    def setup(self, id):
        x, y, z, *rest = self._center
        x += self._distance * math.sin(self._angle)
        z += self._distance * math.cos(self._angle)
        self._setup((x, y, z, *rest), id)

    def rotate(self, angle):
        self._angle += angle


main_light = PositionedLight(
    position=(0.0, 6.0, 3.0, 0.0),
    intensity_ambient=(0.2, 0.2, 0.2, .0),
    intensity_diffuse=(0.8, 0.8, 0.8, .0),
    intensity_specular=(1.0, 1.0, 1.0, 1.0),
)

secondary_light = RotatingLight(
    center=(0.0, 2.0, 0.0, 1.0),
    distance=6,
    intensity_ambient=(0., 0., 0., 1.0),
    intensity_diffuse=(0.4, .4, .0, .5),
    intensity_specular=(.0, .0, .0, 1.0),
)


def terrain_height(x, z):
    # -2.5, 3, 5
    if math.fabs(x) < 6 and math.fabs(z) < 4:
        return 0
    return 1 * (math.sin((x + z) / 10 * math.pi)**2)


def generate_terrain(start=-20, end=20, steps=40):
    step = (end - start) / steps

    # Generate vertices
    # Vertices are generated as (1, 0, 9), (1, 9, 10) when each row contains 9 vertices
    vertices = []
    for z_i in range(steps):
        vertices.extend(
            (
                start + x_i * step,
                terrain_height(start + x_i * step, start + z_i * step),
                start + z_i * step,
            ) for x_i in range(steps)
        )

    # Generate polygons
    polygons = []
    for tz_i in range(steps - 1):
        base_offset = tz_i * steps
        next_offset = (tz_i + 1) * steps
        for tx_i in range(steps - 1):
            # Generate two triangles to complete rectangle
            polygons.append(
                (base_offset + tx_i + 1, next_offset + tx_i, base_offset + tx_i)
            )
            polygons.append(
                (base_offset + tx_i + 1, next_offset + tx_i + 1, next_offset + tx_i)
            )

    return vertices, polygons


TERRAIN_POINTS, TERRAIN_POLYGONS = generate_terrain()


def background():
    # Set the background color of the window to dark blue
    glClearColor(0.1, 0.1, 0.5, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def perspective():
    # establish the projection matrix (perspective)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    _,_,width,height = glGetDoublev(GL_VIEWPORT)
    gluPerspective(45, width / height, 4, 40)


def lookat():
    # look point to the model
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    camera.lookat((0, 0, 0))


def light():
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, GLfloat_4(0.2, 0.2, 0.2, 1.0))
    glEnable(GL_LIGHTING)

    main_light.setup(GL_LIGHT0)
    secondary_light.setup(GL_LIGHT1)


def depth():
    # Setup depth
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)


def fog():
    # Enable fog
    glEnable(GL_FOG)

    # Set white fog with distance of 15
    glFogf(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, (1, 1, 1))
    glFogf(GL_FOG_START, 1.0)
    glFogf(GL_FOG_END, 15)


def terrainMaterial():
    # Setup material for terrain
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0, 0.325, 0, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.1, 0.675, 0.1, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.5, 0.5, 1.0, 1.0))


def homeMaterial():
    # Setup material for home
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0.525, 0.125, 0.32, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.175, 0.575, 0.38, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.0, 0.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, GLfloat(10.0))


def carMaterial():
    # Setup material for car
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0.125, 0.125, 0.32, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.875, 0.875, 0.68, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.0, 1.0, 1.0, 0.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, GLfloat(25.0))


def terrain():
    terrainMaterial()

    # Draw all polygons using points from TERRAIN_POINTS
    for polygon in TERRAIN_POLYGONS:
        glBegin(GL_TRIANGLES)
        for point_index in polygon:
            point = TERRAIN_POINTS[point_index]
            glVertex3f(*point)
        glEnd()


def drawHouse():
    # Set material
    homeMaterial()

    glPushMatrix()

    # House's position
    glTranslate(0, 1, -0.5)

    glutSolidCube(2) # House body
    drawRoof(1.5, 1.25, 16, 8)
    drawChimney(0.25)

    glPopMatrix()


def drawRoof(radius, height, slices, stacks):
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
    carMaterial()
    car.draw()


def display():
    background()
    perspective()
    lookat()
    light()
    depth()
    fog()

    terrain()
    drawHouse()
    drawCar()

    glutSwapBuffers()


def idle_func():
    car.move()
    secondary_light.rotate(0.05)

    glutPostRedisplay()
    time.sleep(0.016)


def on_keydown(key, *args):
    # Change camera's viewpoint rotation, if user presses horizontal arrows
    if key == GLUT_KEY_RIGHT:
        camera.rotate(0.1)
    elif key == GLUT_KEY_LEFT:
        camera.rotate(-0.1)

    if key == GLUT_KEY_UP:
        camera.move(-0.1)
    elif key == GLUT_KEY_DOWN:
        camera.move(0.1)

    glutPostRedisplay()


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
