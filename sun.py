from OpenGL.GL import *
from utils import load_texture, draw_sphere

class Sun:
    def __init__(self):
        self.radius = 3.0
        self.pos = (0, 0, 0)
        self.texture = load_texture("sun.jpg")
        self.spin_angle = 0.0

    def update(self, time_t):
        self.spin_angle = time_t * 10

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glRotatef(self.spin_angle, 0, 1, 0)
        
        glDisable(GL_LIGHTING) # Mặt trời tự phát sáng, không nhận ánh sáng
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor3f(1, 1, 1)
            
        draw_sphere(self.radius)
        glEnable(GL_LIGHTING)
        glPopMatrix()