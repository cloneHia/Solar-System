from OpenGL.GL import *
from utils import load_texture, draw_sphere

class GalaxyBackground:
    def __init__(self):
        self.radius = 200.0
        self.texture = load_texture("milky_way.jpg")

    def draw(self, camera_mode, earth_pos):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE) # Khóa Depth để nó luôn nằm ở lớp xa nhất
        
        # Đi theo Camera khi Zoom để không bao giờ bay ra ngoài rìa vũ trụ
        if camera_mode == "EARTH":
            glTranslatef(*earth_pos)
            
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor3f(1, 1, 1)
            
        draw_sphere(self.radius, slices=30)
        
        glDepthMask(GL_TRUE)
        glEnable(GL_LIGHTING)
        glPopMatrix()