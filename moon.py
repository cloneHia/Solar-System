import math
from OpenGL.GL import *
from utils import load_texture, draw_sphere

class Moon:
    def __init__(self):
        self.radius = 0.3
        self.distance = 2.5
        self.pos = (0, 0, 0)
        self.texture = load_texture("moon.png") # Khớp với đuôi .png của bạn
        self.orbit_angle = 0.0

    def update(self, time_t, earth_pos):
        self.orbit_angle = time_t * 13
        # Tính toán để luôn bám theo Trái Đất
        self.pos = (
            earth_pos[0] + self.distance * math.cos(self.orbit_angle),
            0,
            earth_pos[2] + self.distance * math.sin(self.orbit_angle)
        )

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glRotatef(self.orbit_angle, 0, 1, 0)
        
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor3f(1, 1, 1)
            
        draw_sphere(self.radius)
        glPopMatrix()