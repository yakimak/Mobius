import math
import tkinter as tk
from tkinter import Canvas, Label, Scale, Button, Frame

class Point3D:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

class Triangle:
    def __init__(self, p1, p2, p3):
        self.points = [p1, p2, p3]
        self.center = Point3D(
            (p1.x + p2.x + p3.x)/3,
            (p1.y + p2.y + p3.y)/3,
            (p1.z + p2.z + p3.z)/3)

def create_mobius_strip(radius, twist, u_steps, v_steps):
    
    strips = []
    for i in range(u_steps):
        u1 = 2 * math.pi * i / u_steps
        u2 = 2 * math.pi * (i + 1) / u_steps
        
        for j in range(v_steps):
            v1 = -0.5 + j / v_steps
            v2 = -0.5 + (j + 1) / v_steps
            
            p1 = Point3D(
                (radius + v1 * math.cos(u1/2)) * math.cos(u1),
                (radius + v1 * math.cos(u1/2)) * math.sin(u1),
                twist * v1 * math.sin(u1/2)
            )
            p2 = Point3D(
                (radius + v2 * math.cos(u1/2)) * math.cos(u1),
                (radius + v2 * math.cos(u1/2)) * math.sin(u1),
                twist * v2 * math.sin(u1/2)
            )
            p3 = Point3D(
                (radius + v1 * math.cos(u2/2)) * math.cos(u2),
                (radius + v1 * math.cos(u2/2)) * math.sin(u2),
                twist * v1 * math.sin(u2/2)
            )
            p4 = Point3D(
                (radius + v2 * math.cos(u2/2)) * math.cos(u2),
                (radius + v2 * math.cos(u2/2)) * math.sin(u2),
                twist * v2 * math.sin(u2/2)
            )
            
            strips.append(Triangle(p1, p2, p3))
            strips.append(Triangle(p2, p4, p3))
    return strips

class Camera:
    def __init__(self, dist=5):
        self.dist = dist
        self.angle = 0
        self.light_pos = Point3D(5, 5, 5)
    
    def calculate_light_intensity(self, point):
        distanceqwadr = (point.x - self.light_pos.x)**2 + (point.y - self.light_pos.y)**2 + (point.z - self.light_pos.z)**2
        intensity = max(0, 1 - distanceqwadr / 100)
        return intensity
    
    def project(self, point):      
        x = point.x * math.cos(self.angle) - point.z * math.sin(self.angle)
        y = point.y
        z = point.x * math.sin(self.angle) + point.z * math.cos(self.angle)

        f = self.dist / (self.dist + z)
        return x * f, y * f

class MobiusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поверхность Мёбиуса")
        
        self.radius = 1.0
        self.twist = 0.5
        self.u_steps = 10
        self.v_steps = 5
        
        self.canvas = Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT)
        
        self.setup_controls()
        self.camera = Camera()
        self.update_strip()
        
        self.root.bind('<Left>', lambda e: self.rotate(-0.1))
        self.root.bind('<Right>', lambda e: self.rotate(0.1))
    
    def setup_controls(self):
        panel = Frame(self.root)
        panel.pack(side=tk.RIGHT, padx=10)
        
        controls = [ ("Радиус", 1.0, 3.0, 0.1, self.radius, self.set_radius),
                     ("Скручивание", 0.5, 2.0, 0.1, self.twist, self.set_twist),
                     ("Детализация по длине", 10, 100, 10, self.u_steps, self.set_u_steps),
                     ("Детализация по ширине", 5, 30, 1, self.v_steps, self.set_v_steps) ]
        
        for text, frm, to, step, val, cmd in controls:
            Label(panel, text=text).pack()
            Scale(panel, from_=frm, to=to, resolution=step, 
                  orient=tk.HORIZONTAL, command=cmd).pack()
        
        Button(panel, text="Обновить", command=self.update_strip).pack(pady=10)
    
    def set_radius(self, val): self.radius = float(val)
    def set_twist(self, val): self.twist = float(val)
    def set_u_steps(self, val): self.u_steps = int(float(val))
    def set_v_steps(self, val): self.v_steps = int(float(val))
    
    def update_strip(self):
        self.strip = create_mobius_strip(
            self.radius, self.twist, 
            self.u_steps, self.v_steps)
        self.draw()
    
    def rotate(self, angle):     
        self.camera.angle += angle
        self.draw()
    
    def draw(self):
        self.canvas.delete('all')
        sorted_strip = sorted(self.strip, key=lambda t: -t.center.z)
        
        for tri in sorted_strip:
            intensity = sum(
                self.camera.calculate_light_intensity(p) 
                for p in tri.points
            ) / 3
            
            color = f"#{int(0xA6 * intensity):02x}{int(0x89 * intensity):02x}{int(0xE1 * intensity):02x}"
            
            points = []
            for p in tri.points:
                x, y = self.camera.project(p)
                sx = 400 + x * 200
                sy = 300 - y * 200
                points.extend([sx, sy])
            
            self.canvas.create_polygon(
                points, 
                outline='black', 
                fill=color,
                width=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MobiusApp(root)
    root.mainloop()
