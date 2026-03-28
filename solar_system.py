from planet import Planet

class SolarSystem:
    def __init__(self):
        # Tạo toàn bộ các hành tinh ở đây, quản lý bằng 1 danh sách (List)
        self.planets = [
            Planet("Mercury", 0.4, 6.0, 4.0, 10.0, "mercury.jpg"),
            Planet("Venus", 0.9, 10.0, 3.0, -5.0, "venus.jpg"),
            Planet("Mars", 0.5, 20.0, 1.5, 30.0, "mars.jpg"),
            Planet("Jupiter", 2.5, 30.0, 0.8, 70.0, "jupiter.jpg"),
            Planet("Saturn", 2.0, 40.0, 0.5, 65.0, "saturn.jpg"),
            Planet("Uranus", 1.5, 50.0, 0.3, 40.0, "uranus.jpg"),
            Planet("Neptune", 1.4, 60.0, 0.2, 45.0, "neptune.jpg")
        ]

    def update(self, time_t):
        # Cập nhật vị trí cho tất cả hành tinh
        for p in self.planets:
            p.update(time_t)

    def draw_orbits(self):
        # Vẽ đường quỹ đạo cho tất cả hành tinh
        for p in self.planets:
            p.draw_orbit()

    def draw(self):
        # Vẽ hình ảnh khối cầu của tất cả hành tinh lên không gian
        for p in self.planets:
            p.draw()