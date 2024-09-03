import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from config import Config

class Visualization:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.display = Config.SIMULATION_PARAMS['resolution']
        self.pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        # glTranslatef(0.0, 0.0, -5)
        glTranslatef(-1.0, -1.0, -2)  # Move the camera closer to the agents

        
        # Set point size for better visibility
        glPointSize(10)

    def draw_agents(self, agents):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
        glBegin(GL_POINTS)
        for agent in agents:
            glColor3f(*agent['color'])
            x, y = agent['position']
            x = (x / self.display[0]) * 2 - 1
            y = (y / self.display[1]) * 2 - 1

            glVertex3f(x, y, 0)
        glEnd()

        self.pygame.display.flip()  # Update the display