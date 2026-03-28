import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import os

def load_texture(filename):
    filepath = os.path.join("assets", filename)
    try:
        surface = pygame.image.load(filepath)
        w, h = surface.get_size()
        
        MAX_TEX_SIZE = 4096
        if w > MAX_TEX_SIZE or h > MAX_TEX_SIZE:
            ratio = min(MAX_TEX_SIZE / w, MAX_TEX_SIZE / h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            surface = pygame.transform.smoothscale(surface, (new_w, new_h))
            w, h = new_w, new_h
            print(f"[*] Đã tự động thu nhỏ '{filename}' xuống {w}x{h} để chống lỗi VRAM.")

        surface = surface.convert(24)
        data = pygame.image.tobytes(surface, "RGB", True)
        
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        
        # --- ĐÂY LÀ DÒNG FIX LỖI ACCESS VIOLATION CHO ẢNH KÍCH THƯỚC LẺ ---
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        
        return texid
    except Exception as e:
        print(f"LỖI TẢI ẢNH [{filename}]: {e}")
        return None

def draw_sphere(radius, slices=50):
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, slices, slices)
    gluDeleteQuadric(quad)