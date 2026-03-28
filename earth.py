import math
from OpenGL.GL import *
from utils import load_texture, draw_sphere
from shaders import create_earth_shader

class Earth:
    def __init__(self):
        self.radius = 1.0
        self.distance = 15.0
        self.pos = (self.distance, 0, 0)
        
        self.tex_day = load_texture("earth_day.png") 
        self.tex_night = load_texture("earth_night.jpg")
        self.shader = create_earth_shader()
        
        self.orbit_angle = 0.0
        self.spin_angle = 0.0
        
        # [CHỐT HẠ ĐỊA LÝ]: Ảnh bản đồ của bạn bị lệch 90 độ so với chuẩn chung. 
        # Tôi đã khóa cứng ở mức 90. Giờ đây UTC+7 sẽ trúng phóc Việt Nam!
        self.MAP_OFFSET =  0

    def update(self, time_t, camera_mode):
        if camera_mode == "SYSTEM":
            self.orbit_angle = time_t
            self.spin_angle = time_t * 30
            self.pos = (self.distance * math.cos(self.orbit_angle), 0, self.distance * math.sin(self.orbit_angle))
        else:
            # Ở chế độ Google Earth, Trái Đất đứng im tuyệt đối. Mọi việc chiếu sáng cứ để Mặt Trời lo!
            self.orbit_angle = 0.0
            self.pos = (self.distance, 0, 0)
            self.spin_angle = self.MAP_OFFSET 

    def draw_orbit(self):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            angle = 2.0 * math.pi * i / 100
            glVertex3f(self.distance * math.cos(angle), 0, self.distance * math.sin(angle))
        glEnd()
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glRotatef(self.spin_angle, 0, 1, 0)
        
        # Giữ cực Bắc luôn hướng lên trên
        glRotatef(-90, 1, 0, 0)

        if self.tex_day and self.tex_night:
            glUseProgram(self.shader)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.tex_day)
            glUniform1i(glGetUniformLocation(self.shader, "dayTex"), 0)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.tex_night)
            glUniform1i(glGetUniformLocation(self.shader, "nightTex"), 1)
            
            draw_sphere(self.radius)
            glUseProgram(0)
            glActiveTexture(GL_TEXTURE0)
        else:
            draw_sphere(self.radius)
        glPopMatrix()