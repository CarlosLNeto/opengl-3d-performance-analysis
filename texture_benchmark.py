"""
Benchmark de renderização com texturas
Compara desempenho com e sem texturas de diferentes resoluções
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

class TexturedTriangle:
    def __init__(self, position=(0, 0, 0), size=1.0, texture_id=None):
        self.position = position
        self.size = size
        self.rotation = 0
        self.texture_id = texture_id
        
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        glScalef(self.size, self.size, self.size)
        
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            glBegin(GL_TRIANGLES)
            glColor3f(1, 1, 1)
            glTexCoord2f(0.5, 1.0)
            glVertex3f(0, 1, 0)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1, -1, 0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1, -1, 0)
            glEnd()
            
            glDisable(GL_TEXTURE_2D)
        else:
            glBegin(GL_TRIANGLES)
            glColor3f(1, 0, 0)
            glVertex3f(0, 1, 0)
            glVertex3f(-1, -1, 0)
            glVertex3f(1, -1, 0)
            glEnd()
        
        glPopMatrix()
        
    def update(self, delta_time):
        self.rotation += 50 * delta_time

class TextureBenchmark:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.triangles = []
        self.texture_ids = {}
        self.fps_history = []
        self.cpu_history = []
        self.gpu_history = []
        self.frame_count = 0
        self.start_time = time.time()
        self.last_time = time.time()
        
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Benchmark de Texturas - OpenGL")
        
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)
        
        self.system_info = self.get_system_info()
        self.create_textures()
    
    def get_system_info(self):
        info = {
            "cpu": psutil.cpu_count(logical=False),
            "cpu_logical": psutil.cpu_count(logical=True),
            "gpu_available": GPU_AVAILABLE
        }
        return info
        
    def create_textures(self):
        sizes = [64, 128, 256]
        
        for size in sizes:
            image = np.zeros((size, size, 3), dtype=np.uint8)
            
            square_size = size // 8
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 0:
                        color = [255, 200, 100]
                    else:
                        color = [100, 150, 200]
                    
                    image[i*square_size:(i+1)*square_size, 
                          j*square_size:(j+1)*square_size] = color
            
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, 
                        GL_RGB, GL_UNSIGNED_BYTE, image)
            
            self.texture_ids[f"{size}x{size}"] = texture_id
    
    def add_triangles(self, count=1, texture_size=None):
        texture_id = None
        if texture_size and texture_size in self.texture_ids:
            texture_id = self.texture_ids[texture_size]
            
        for i in range(count):
            grid_size = int(np.ceil(np.sqrt(len(self.triangles) + 1)))
            x = (i % grid_size - grid_size / 2) * 2
            y = ((i // grid_size) % grid_size - grid_size / 2) * 2
            z = (i // (grid_size * grid_size)) * 2
            
            triangle = TexturedTriangle(position=(x, y, z), size=0.5, 
                                       texture_id=texture_id)
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
    
    def run_benchmark(self, triangle_counts=[100, 500, 1000, 2000], 
                     texture_sizes=[None, "64x64", "128x128", "256x256"],
                     duration_per_test=5):
        results = []
        
        for texture_size in texture_sizes:
            for count in triangle_counts:
                tex_label = texture_size if texture_size else "sem textura"
                print(f"\n=== Testando {count} triângulos com {tex_label} ===")
                
                self.triangles.clear()
                self.add_triangles(count, texture_size)
                
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
                
                avg_fps = np.mean(self.fps_history) if self.fps_history else 0
                min_fps = np.min(self.fps_history) if self.fps_history else 0
                max_fps = np.max(self.fps_history) if self.fps_history else 0
                avg_cpu = np.mean(self.cpu_history) if self.cpu_history else 0
                avg_gpu = np.mean(self.gpu_history) if self.gpu_history else 0
                
                result = {
                    "triangle_count": count,
                    "use_texture": texture_size is not None,
                    "texture_size": texture_size if texture_size else "none",
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
    
    def save_results(self, results, filename="benchmark_textura.json"):
        data = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self.system_info,
            "results": results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"\nResultados salvos em {filename}")
    
    def cleanup(self):
        for texture_id in self.texture_ids.values():
            glDeleteTextures([texture_id])
        pygame.quit()


if __name__ == "__main__":
    print("="*60)
    print("BENCHMARK DE TEXTURAS - OPENGL")
    print("="*60)
    
    app = TextureBenchmark()
    
    triangle_counts = [100, 500, 1000, 2000]
    texture_sizes = [None, "64x64", "128x128", "256x256"]
    duration = 5
    
    print(f"\nTestando {len(texture_sizes)} configurações de texturas")
    print(f"com {len(triangle_counts)} quantidades de triângulos")
    print(f"Duração de cada teste: {duration} segundos\n")
    
    try:
        results = app.run_benchmark(triangle_counts, texture_sizes, duration)
        app.save_results(results, "benchmark_textura.json")
        
        print("\n" + "="*60)
        print("BENCHMARK CONCLUÍDO!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nBenchmark cancelado pelo usuário")
    finally:
        app.cleanup()
