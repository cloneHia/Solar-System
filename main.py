import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import datetime
import time

from camera import Camera
from sun import Sun
from earth import Earth
from moon import Moon
from solar_system import SolarSystem
from galaxy import GalaxyBackground

class Engine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display = (1280, 720)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Google Earth - Flawless Time & Lighting")
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        
        self.sun = Sun()
        self.earth = Earth()
        self.moon = Moon()
        # Khởi tạo toàn bộ Hệ Mặt Trời từ class bên ngoài
        self.solar_system = SolarSystem()
        self.background = GalaxyBackground()
        self.camera = Camera()
        
        self.font = pygame.font.SysFont('Consolas', 22, bold=True)
        self.font_small = pygame.font.SysFont('Consolas', 16, bold=True)
        self.clock = pygame.time.Clock()
        self.time_t = 0.0
        self.show_orbits = True 
        self.is_wireframe = False
        
        now = datetime.datetime.now()
        self.tz_offset = -time.timezone // 3600
        self.sim_hour = now.hour
        self.sim_minute = now.minute
        self.sim_utc_time = datetime.datetime.utcnow()
        self.is_custom_time = False 

    def get_earth_screen_pos(self):
        mv_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        try:
            ex, ey, ez = self.earth.pos
            screen_x, screen_y, _ = gluProject(ex, ey, ez, mv_matrix, proj_matrix, viewport)
            return screen_x, viewport[3] - screen_y
        except: return None

    def jump_camera_to_timezone(self):
        # Phương trình gốc: Mỗi múi giờ tương ứng 15 độ. Dấu dương = Hướng Đông.
        self.camera.yaw = self.tz_offset * 15.0
        self.camera.pitch = 0

    def apply_custom_time(self):
        base_date = datetime.datetime.now()
        local_dt = base_date.replace(hour=self.sim_hour, minute=self.sim_minute, second=0)
        # Qui đổi mọi thứ về giờ UTC chuẩn quốc tế
        self.sim_utc_time = local_dt - datetime.timedelta(hours=self.tz_offset)
        self.is_custom_time = True
        self.jump_camera_to_timezone()

    def render_ui_text(self, text, x, y, color=(255, 255, 255), small=False):
        f = self.font_small if small else self.font
        surface = f.render(text, True, color)
        data = pygame.image.tobytes(surface, "RGBA", True)
        w, h = surface.get_size()
        glWindowPos2i(x, y)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def draw_btn(self, x, y, w, h, text):
        glColor3f(0.15, 0.15, 0.15)
        glBegin(GL_QUADS)
        glVertex2f(x, y); glVertex2f(x+w, y); glVertex2f(x+w, y+h); glVertex2f(x, y+h)
        glEnd()
        glColor3f(0.5, 0.8, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y); glVertex2f(x+w, y); glVertex2f(x+w, y+h); glVertex2f(x, y+h)
        glEnd()
        # Ép dùng font nhỏ và căn giữa nút 20x20
        self.render_ui_text(text, x + 6, 720 - y - h + 4, small=True)

    def render_ui_panel(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND) 
        glDisable(GL_CULL_FACE) 
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        
        # [SỬA LỖI MẤT NỀN XÁM]: Cấp cho thanh UI một "độ dày" Z từ -50 đến 50.
        # Nhờ vậy la bàn xoay nghiêng 3D thoải mái mà không bị đâm thủng màn hình!
        glOrtho(0, 1280, 720, 0, -50.0, 50.0)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # NỀN THANH CÔNG CỤ SIÊU NHỎ
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 680); glVertex2f(1280, 680)
        glVertex2f(1280, 720); glVertex2f(0, 720)
        glEnd()
        
        glColor3f(0.3, 0.3, 0.3)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glVertex2f(0, 680); glVertex2f(1280, 680)
        glEnd()
        
        # LA BÀN ĐỘNG THEO TRỤC VĨ ĐỘ (PITCH)
        cx, cy = 40, 700
        glPushMatrix()
        glTranslatef(cx, cy, 0)
        
        # 1. Nền xám SIÊU NHỎ (Bán kính 14) - CỐ ĐỊNH
        glColor3f(0.15, 0.15, 0.15)
        glBegin(GL_POLYGON)
        for i in range(36):
            a = math.radians(i * 10)
            glVertex2f(14*math.cos(a), 14*math.sin(a))
        glEnd()
        
        # 2. KIM CHỈ XOAY THEO VĨ ĐỘ (PITCH)
        glPushMatrix()
        # [SỬA LỖI NGU ĐẦN TẠI ĐÂY]: Dùng đúng self.camera.pitch (Vĩ độ)
        glRotatef(self.camera.pitch, 0, 0, 1) 
        
        # Kim Đỏ (Bắc) SIÊU NHỎ (Dài 12)
        glColor3f(1.0, 0.1, 0.1)
        glBegin(GL_TRIANGLES)
        glVertex2f(-3, 0); glVertex2f(3, 0); glVertex2f(0, -12)
        glEnd()
        
        # Kim Trắng (Nam) SIÊU NHỎ (Dài 12)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(-3, 0); glVertex2f(3, 0); glVertex2f(0, 12)
        glEnd()
        
        glPopMatrix() # Kết thúc xoay kim
        glPopMatrix() # Kết thúc cụm la bàn
        
        #  Bật chế độ trong suốt (Blend) TRƯỚC KHI vẽ nút bấm
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # 3. NÚT BẤM SIÊU NHỎ: 20x20 pixel
        self.draw_btn(120, 690, 20, 20, "-")
        self.draw_btn(220, 690, 20, 20, "+")
        
        self.draw_btn(320, 690, 20, 20, "-")
        self.draw_btn(400, 690, 20, 20, "+")
        
        # Nút BACK rộng 45px để quay lại Hệ Mặt Trời
        self.draw_btn(460, 690, 45, 20, "BACK")
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # 4. CHỮ HIỂN THỊ: Nằm gọn gàng trên 1 hàng duy nhất
        self.render_ui_text("TZ:", 90, 12, (150, 150, 150), small=True)
        tz_str = f"UTC+{self.tz_offset}" if self.tz_offset >= 0 else f"UTC{self.tz_offset}"
        self.render_ui_text(tz_str, 150, 12, (255, 200, 50), small=True)
        
        self.render_ui_text("HR:", 290, 12, (150, 150, 150), small=True)
        self.render_ui_text(f"{self.sim_hour:02d} h", 350, 12, (100, 255, 100), small=True)
        
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_CULL_FACE)

    def run(self):
        running = True
        while running:
            self.time_t += 0.005
            
            if not self.is_custom_time:
                now = datetime.datetime.now()
                self.sim_hour = now.hour
                self.sim_minute = now.minute
            
            for event in pygame.event.get():
                if event.type == QUIT: running = False
                
                elif event.type == KEYDOWN:
                    if event.key == K_o: self.show_orbits = not self.show_orbits
                    
                
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if event.button == 1: 
                        if mouse_y >= 680 and self.camera.mode == "EARTH":
                            # 1. NẾU BẤM NÚT BACK: Chỉ lùi Camera ra ngoài, KHÔNG cập nhật giờ!
                            if 460 <= mouse_x <= 505 and 690 <= mouse_y <= 710: 
                                self.camera.mode = "SYSTEM"
                                self.camera.pitch = 45.0
                                self.camera.yaw = 0.0
                                self.camera.distance = 100.0
                            
                            # 2. NẾU BẤM CÁC NÚT KHÁC (Chỉnh giờ, Múi giờ):
                            else:
                                if 120 <= mouse_x <= 140 and 690 <= mouse_y <= 710: self.tz_offset = max(-12, self.tz_offset - 1)
                                if 220 <= mouse_x <= 240 and 690 <= mouse_y <= 710: self.tz_offset = min(12, self.tz_offset + 1)
                                if 320 <= mouse_x <= 340 and 690 <= mouse_y <= 710: self.sim_hour = (self.sim_hour - 1) % 24
                                if 400 <= mouse_x <= 420 and 690 <= mouse_y <= 710: self.sim_hour = (self.sim_hour + 1) % 24
                                
                                # CHỈ gọi hàm đè góc pitch=0 khi đang chỉnh giờ trên Trái Đất
                                self.apply_custom_time()
                        else:
                            if self.camera.mode == "SYSTEM":
                                screen_pos = self.get_earth_screen_pos()
                                if screen_pos:
                                    dist = math.hypot(mouse_x - screen_pos[0], mouse_y - screen_pos[1])
                                    if dist < 30: 
                                        self.camera.mode = "EARTH"
                                        self.apply_custom_time()

                self.camera.handle_mouse(event)

            self.sun.update(self.time_t)
            self.earth.update(self.time_t, self.camera.mode)
            self.moon.update(self.time_t, self.earth.pos)
            # Cập nhật Hệ mặt trời
            self.solar_system.update(self.time_t)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            self.camera.apply(self.earth.pos)
            
            # [LÕI TOÁN HỌC ÁNH SÁNG CHUẨN XÁC]
            if self.camera.mode == "EARTH":
                # Lấy giờ UTC thực tính bằng số thập phân
                utc_hours = self.sim_utc_time.hour + self.sim_utc_time.minute / 60.0 + self.sim_utc_time.second / 3600.0
                
                # Phương trình Mặt trời: 12h trưa UTC -> Mặt trời chiếu góc 0.
                sun_yaw = (12.0 - utc_hours) * 15.0 
                sun_rad = math.radians(sun_yaw)
                
                # [QUAN TRỌNG NHẤT]: Tâm chiếu sáng phải neo vào tọa độ của Trái Đất (self.earth.pos)
                ex, ey, ez = self.earth.pos
                sun_x = ex + 1000.0 * math.sin(sun_rad)
                sun_z = ez + 1000.0 * math.cos(sun_rad)
                
                glLightfv(GL_LIGHT0, GL_POSITION, (sun_x, 0.0, sun_z, 1.0))
            else:
                glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))
            
            glDisable(GL_CULL_FACE)
            self.background.draw(self.camera.mode, self.earth.pos)
            glEnable(GL_CULL_FACE)
            
            if self.is_wireframe: glUseProgram(0)
            self.earth.draw()

            if self.camera.mode == "SYSTEM":
                # 1. Vẽ các đường quỹ đạo
                if self.show_orbits: 
                    self.earth.draw_orbit()
                    self.solar_system.draw_orbits()
                
                # 2. Vẽ Mặt Trời và Mặt Trăng
                self.sun.draw()
                self.moon.draw()
                
                # 3. Vẽ các hành tinh khác
                self.solar_system.draw()
            
            if self.camera.mode == "EARTH":
                self.render_ui_panel()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    app = Engine()
    app.run()