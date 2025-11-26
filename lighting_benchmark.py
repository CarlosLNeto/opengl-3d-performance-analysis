"""
Benchmark de renderização com iluminação
Testa impacto de luzes omnidirecionais e spot no desempenho
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time
import psutil
import json
import os
from datetime import datetime

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("GPUtil não disponível. Instale com: pip install gputil")

class TriangleLighting:
    def __init__(self, position=(0, 0, 0), size=1.0):
        self.position = position
        self.size = size
        self.rotation = 0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        glScalef(self.size, self.size, self.size)
        
        # Material properties
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.3, 0.3, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        
        glBegin(GL_TRIANGLES)
        glNormal3f(0, 0, 1)
        glVertex3f(0, 1, 0)
        glVertex3f(-1, -1, 0)
        glVertex3f(1, -1, 0)
        glEnd()
        
        glPopMatrix()
        
    def update(self, delta_time):
        self.rotation += 50 * delta_time

class LightingBenchmark:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.triangles = []
        self.fps_history = []
        self.cpu_history = []
        self.gpu_history = []
        self.frame_count = 0
        self.start_time = time.time()
        self.last_time = time.time()
        
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Benchmark de Iluminação - OpenGL")
        
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)
        
        # Informações do sistema
        self.system_info = self.get_system_info()
        
    def get_system_info(self):
        info = {
            "cpu": psutil.cpu_count(logical=False),
            "cpu_logical": psutil.cpu_count(logical=True),
            "gpu_available": GPU_AVAILABLE
        }
        return info
        
    def setup_lighting(self, light_type="none"):
        if light_type == "none":
            glDisable(GL_LIGHTING)
            return
        
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        
        if light_type == "omnidirectional":
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 5.0, 5.0, 1.0])
            glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
            glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            
        elif light_type == "spot":
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 5.0, 5.0, 1.0])
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, -1.0, -1.0])
            glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 30.0)
            glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 2.0)
            glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
            glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            
        elif light_type == "multiple":
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
            
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_POSITION, [-5.0, 5.0, 5.0, 1.0])
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 1.0, 0.0, 1.0])
            
            glEnable(GL_LIGHT2)
            glLightfv(GL_LIGHT2, GL_POSITION, [0.0, -5.0, 5.0, 1.0])
            glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])
    
    def add_triangles(self, count=1):
        for i in range(count):
            grid_size = int(np.ceil(np.sqrt(len(self.triangles) + 1)))
            x = (i % grid_size - grid_size / 2) * 2
            y = ((i // grid_size) % grid_size - grid_size / 2) * 2
            z = (i // (grid_size * grid_size)) * 2
            
            triangle = TriangleLighting(position=(x, y, z), size=0.5)
            self.triangles.append(triangle)
    
    def get_performance_metrics(self):
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0),
            "ram_percent": psutil.virtual_memory().percent,
            "gpu_usage": [],
            "gpu_memory": []
        }
        
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    metrics["gpu_usage"].append(gpu.load * 100)
                    metrics["gpu_memory"].append(gpu.memoryUtil * 100)
            except:
                pass
        
        return metrics
    
    def update(self, delta_time):
        for triangle in self.triangles:
            triangle.update(delta_time)
    
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        for triangle in self.triangles:
            triangle.draw()
        
        pygame.display.flip()
        self.frame_count += 1
    
    def calculate_fps(self):
        current_time = time.time()
        elapsed = current_time - self.last_time
        if elapsed > 0:
            fps = 1.0 / elapsed
            self.fps_history.append(fps)
            self.last_time = current_time
            return fps
        return 0
    
    def run_benchmark(self, triangle_counts=[100, 500, 1000], 
                     light_types=["none", "omnidirectional", "spot", "multiple"],
                     duration_per_test=5):
        results = []
        
        for light_type in light_types:
            for count in triangle_counts:
                print(f"\n=== Testando {count} triângulos com iluminação: {light_type} ===")
                
                # Limpa e configura
                self.triangles.clear()
                self.add_triangles(count)
                self.setup_lighting(light_type)
                
                # Resetar métricas
                self.fps_history.clear()
                self.cpu_history.clear()
                self.gpu_history.clear()
                self.frame_count = 0
                self.last_time = time.time()
                
                test_start = time.time()
                
                while time.time() - test_start < duration_per_test:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return results
                    
                    current_time = time.time()
                    delta_time = current_time - self.last_time
                    
                    self.update(delta_time)
                    self.render()
                    
                    fps = self.calculate_fps()
                    metrics = self.get_performance_metrics()
                    
                    self.cpu_history.append(metrics["cpu_percent"])
                    if metrics["gpu_usage"]:
                        self.gpu_history.append(metrics["gpu_usage"][0])
                
                # Calcula estatísticas
                avg_fps = np.mean(self.fps_history) if self.fps_history else 0
                min_fps = np.min(self.fps_history) if self.fps_history else 0
                max_fps = np.max(self.fps_history) if self.fps_history else 0
                avg_cpu = np.mean(self.cpu_history) if self.cpu_history else 0
                avg_gpu = np.mean(self.gpu_history) if self.gpu_history else 0
                
                result = {
                    "triangle_count": count,
                    "light_type": light_type,
                    "avg_fps": avg_fps,
                    "min_fps": min_fps,
                    "max_fps": max_fps,
                    "avg_cpu": avg_cpu,
                    "avg_gpu": avg_gpu,
                    "total_frames": self.frame_count
                }
                
                results.append(result)
                print(f"FPS médio: {avg_fps:.2f}")
                print(f"CPU médio: {avg_cpu:.2f}%")
                if avg_gpu > 0:
                    print(f"GPU médio: {avg_gpu:.2f}%")
        
        return results
    
    def save_results(self, results, filename="benchmark_lighting.json"):
        data = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self.system_info,
            "results": results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"\nResultados salvos em {filename}")
    
    def cleanup(self):
        pygame.quit()


if __name__ == "__main__":
    print("="*60)
    print("BENCHMARK DE ILUMINAÇÃO - OPENGL")
    print("="*60)
    
    app = LightingBenchmark()
    
    triangle_counts = [100, 500, 1000]
    light_types = ["none", "omnidirectional", "spot", "multiple"]
    duration = 5
    
    print(f"\nTestando {len(light_types)} tipos de iluminação")
    print(f"com {len(triangle_counts)} configurações de triângulos")
    print(f"Duração de cada teste: {duration} segundos\n")
    
    try:
        results = app.run_benchmark(triangle_counts, light_types, duration)
        app.save_results(results, "benchmark_lighting.json")
        
        print("\n" + "="*60)
        print("BENCHMARK CONCLUÍDO!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nBenchmark cancelado pelo usuário")
    finally:
        app.cleanup()
