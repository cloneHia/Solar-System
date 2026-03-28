import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Camera:
    def __init__(self):
        self.mode = "SYSTEM"
        self.yaw = 0.0
        self.pitch = 30.0
        self.distance = 40.0
        self.earth_distance = 3.0
        self.is_dragging = False

    def handle_mouse(self, event):
        if event.type == MOUSEWHEEL:
            if self.mode == "SYSTEM":
                self.distance -= event.y * 3.0 
                self.distance = max(10.0, min(150.0, self.distance)) 
            elif self.mode == "EARTH":
                self.earth_distance -= event.y * 0.3
                self.earth_distance = max(1.05, min(15.0, self.earth_distance))

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1: 
                self.is_dragging = True
                
                # [SỬA LỖI TUYỆT ĐỐI]: Xả bộ nhớ đệm của chuột trước khi kéo để không bị giật ngược về gốc!
                pygame.mouse.get_rel() 
                
                # Khóa chuột vào màn hình để xoay vô hạn
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
        
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1: 
                self.is_dragging = False
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            
        elif event.type == MOUSEMOTION and self.is_dragging:
            self.yaw -= event.rel[0] * 0.3
            self.pitch -= event.rel[1] * 0.3
            # Khóa góc ngước lên/xuống để không bị lộn ngược bản đồ
            if self.mode == "EARTH": 
                self.pitch = max(-89.9, min(89.9, self.pitch))

    def apply(self, earth_pos):
        glLoadIdentity()
        gluPerspective(45, 1280/720, 0.1, 500.0)

        if self.mode == "SYSTEM":
            cx = self.distance * math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw))
            cy = self.distance * math.sin(math.radians(self.pitch))
            cz = self.distance * math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
            gluLookAt(cx, cy, cz, 0, 0, 0, 0, 1, 0)
        else:
            tracking_dist = self.earth_distance
            cx = earth_pos[0] + tracking_dist * math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw))
            cy = earth_pos[1] + tracking_dist * math.sin(math.radians(self.pitch))
            cz = earth_pos[2] + tracking_dist * math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
            gluLookAt(cx, cy, cz, *earth_pos, 0, 1, 0)