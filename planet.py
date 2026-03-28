import math
from OpenGL.GL import *
from utils import load_texture, draw_sphere

class Planet:
    def __init__(self, name, radius, distance, orbit_speed, spin_speed, texture_file):
        self.name = name
        self.radius = radius            # Độ lớn của hành tinh
        self.distance = distance        # Khoảng cách tới Mặt Trời
        self.orbit_speed = orbit_speed  # Tốc độ quay quanh Mặt trời (Năm)
        self.spin_speed = spin_speed    # Tốc độ tự quay quanh trục (Ngày)
        
        self.pos = (distance, 0, 0)
        self.texture = load_texture(texture_file)
        self.orbit_angle = 0.0
        self.spin_angle = 0.0

    def update(self, time_t):
        # Tính toán góc xoay quanh Mặt Trời
        self.orbit_angle = time_t * self.orbit_speed
        # Cập nhật tọa độ X, Y, Z trong không gian
        self.pos = (
            self.distance * math.cos(self.orbit_angle),
            0,
            self.distance * math.sin(self.orbit_angle)
        )
        # Tính góc tự quay quanh trục
        self.spin_angle = time_t * self.spin_speed

    def draw_orbit(self):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.2, 0.2, 0.2) # Quỹ đạo vẽ màu xám mờ
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
        
        # Lật bản đồ 90 độ để 2 Cực hướng lên trên
        glRotatef(-90, 1, 0, 0)

        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor3f(1, 1, 1) # Giữ nguyên màu thật của ảnh
            
        draw_sphere(self.radius)
        glPopMatrix()