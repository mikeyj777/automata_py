import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from config import Config

class Visualization:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        display = Config.SIMULATION_PARAMS['resolution']
        self.pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        
        # Set point size for better visibility
        glPointSize(10)

    def draw_agents(agents):
        glBegin(GL_POINTS)
        for agent in agents:
            glColor3f(*agent['color'])
            glVertex3f(*agent['position'])
        glEnd()