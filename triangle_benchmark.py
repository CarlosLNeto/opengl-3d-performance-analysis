"""
Benchmark de renderização de triângulos com OpenGL
Mede FPS, uso de CPU e GPU com diferentes quantidades de triângulos
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

class Triangle:
    def __init__(self, position=(0, 0, 0), color=(1, 0, 0), size=1.0):
        self.position = position
        self.color = color
        self.size = size
        self.rotation = 0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        glScalef(self.size, self.size, self.size)
        
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        glVertex3f(0, 1, 0)
        glVertex3f(-1, -1, 0)
        glVertex3f(1, -1, 0)
        glEnd()
        
        glPopMatrix()
        
    def update(self, delta_time):
        self.rotation += 50 * delta_time

class BenchmarkApp:
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
        pygame.display.set_caption("Benchmark de Triângulos - OpenGL")
        
        # Configuração OpenGL
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
            "cpu_freq": psutil.cpu_freq().max if psutil.cpu_freq() else "N/A",
            "ram": psutil.virtual_memory().total / (1024**3),
            "gpu_available": GPU_AVAILABLE,
            "gpu_count": 0,
            "gpu_info": []
        }
        
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                info["gpu_count"] = len(gpus)
                for gpu in gpus:
                    info["gpu_info"].append({
                        "name": gpu.name,
                        "memory_total": gpu.memoryTotal,
                        "driver": gpu.driver
                    })
            except:
                pass
                
        return info
    
    def add_triangles(self, count=1):
        for i in range(count):
            # Distribui triângulos em grid 3D
            grid_size = int(np.ceil(np.sqrt(len(self.triangles) + 1)))
            x = (i % grid_size - grid_size / 2) * 2
            y = ((i // grid_size) % grid_size - grid_size / 2) * 2
            z = (i // (grid_size * grid_size)) * 2
            
            color = (
                np.random.random(),
                np.random.random(),
                np.random.random()
            )
            
            triangle = Triangle(position=(x, y, z), color=color, size=0.5)
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
    
    def run_benchmark(self, triangle_counts=[1, 10, 50, 100, 500, 1000], duration_per_test=5):
        results = []
        
        for count in triangle_counts:
            print(f"\n=== Testando com {count} triângulos ===")
            
            # Limpa triângulos anteriores e adiciona novos
            self.triangles.clear()
            self.add_triangles(count)
            
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
    
    def save_results(self, results, filename="benchmark_results.json"):
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
    print("BENCHMARK DE TRIÂNGULOS - OPENGL")
    print("="*60)
    
    app = BenchmarkApp()
    
    # Configurações de teste
    triangle_counts = [1, 10, 50, 100, 200, 500, 1000, 2000]
    duration = 5  # segundos por teste
    
    print(f"\nExecutando benchmark com {len(triangle_counts)} configurações")
    print(f"Duração de cada teste: {duration} segundos")
    print("\nPressione Ctrl+C para cancelar\n")
    
    try:
        results = app.run_benchmark(triangle_counts, duration)
        app.save_results(results, "benchmark_sem_textura.json")
        
        print("\n" + "="*60)
        print("BENCHMARK CONCLUÍDO!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nBenchmark cancelado pelo usuário")
    finally:
        app.cleanup()

