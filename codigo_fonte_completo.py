"""
═══════════════════════════════════════════════════════════════════════════
ANÁLISE DE DESEMPENHO EM RENDERIZAÇÃO 3D COM OPENGL
═══════════════════════════════════════════════════════════════════════════

Código Fonte Completo - Todos os Módulos

Autor: Carlos Neto
Disciplina: Processamento Digital de Imagens
Instituição: Universidade do Estado do Amazonas - UEA
Data: Outubro 2024

Este arquivo contém todo o código fonte utilizado no projeto de análise
de desempenho gráfico, organizado por módulo.

═══════════════════════════════════════════════════════════════════════════
ÍNDICE:
═══════════════════════════════════════════════════════════════════════════

1. MÓDULO: triangle_benchmark.py
   Benchmark básico de triângulos sem texturas ou iluminação

2. MÓDULO: lighting_benchmark.py
   Benchmark com diferentes tipos de iluminação

3. MÓDULO: texture_benchmark.py
   Benchmark com texturas de diferentes resoluções

4. MÓDULO: generate_graphs.py
   Gerador de gráficos e visualizações

5. MÓDULO: check_system.py
   Verificador de informações do sistema

6. MÓDULO: demo_quick.py
   Demonstração rápida para teste

7. MÓDULO: run_all_benchmarks.py
   Script mestre para executar todos os benchmarks

═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 1: triangle_benchmark.py
# ═══════════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 2: lighting_benchmark.py
# ═══════════════════════════════════════════════════════════════════════════

"""
Benchmark de renderização com iluminação
Testa impacto de luzes omnidirecionais e spot no desempenho
"""

# (Importações repetidas omitidas por brevidade - são as mesmas do módulo 1)

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
        
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Benchmark de Iluminação - OpenGL")
        
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)
        
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


# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 3: texture_benchmark.py
# ═══════════════════════════════════════════════════════════════════════════

"""
Benchmark de renderização com texturas
Compara desempenho com e sem texturas de diferentes resoluções
"""

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
        self.texture_ids = []
        
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Benchmark de Texturas - OpenGL")
        
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)
        
        self.create_textures()
    
    def create_textures(self):
        """Cria texturas procedurais de diferentes tamanhos"""
        sizes = [64, 128, 256]
        
        for size in sizes:
            # Criar imagem procedural (padrão xadrez)
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
            
            # Criar textura OpenGL
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, 
                        GL_RGB, GL_UNSIGNED_BYTE, image)
            
            self.texture_ids.append(texture_id)


# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 4: generate_graphs.py
# ═══════════════════════════════════════════════════════════════════════════

"""
Gerador de gráficos para análise de desempenho
Cria visualizações profissionais dos dados coletados
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import os

class GraphGenerator:
    def __init__(self):
        self.figures = []
        
    def load_json(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None
    
    def plot_basic_benchmark(self, data):
        """Gera gráfico de FPS vs Triângulos e uso de recursos"""
        if not data:
            return
        
        results = data['results']
        triangle_counts = [r['triangle_count'] for r in results]
        avg_fps = [r['avg_fps'] for r in results]
        avg_cpu = [r['avg_cpu'] for r in results]
        avg_gpu = [r.get('avg_gpu', 0) for r in results]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Gráfico FPS
        ax1.plot(triangle_counts, avg_fps, 'b-o', linewidth=2, markersize=8)
        ax1.set_xlabel('Número de Triângulos', fontsize=12)
        ax1.set_ylabel('FPS Médio', fontsize=12)
        ax1.set_title('Desempenho: FPS vs Quantidade de Triângulos', 
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        
        for x, y in zip(triangle_counts, avg_fps):
            ax1.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=9)
        
        # Gráfico CPU e GPU
        ax2.plot(triangle_counts, avg_cpu, 'r-o', label='CPU', linewidth=2, markersize=8)
        if any(avg_gpu):
            ax2.plot(triangle_counts, avg_gpu, 'g-s', label='GPU', linewidth=2, markersize=8)
        ax2.set_xlabel('Número de Triângulos', fontsize=12)
        ax2.set_ylabel('Utilização (%)', fontsize=12)
        ax2.set_title('Utilização de CPU e GPU', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xscale('log')
        
        plt.tight_layout()
        plt.savefig('grafico_fps_triangulos.png', dpi=300, bbox_inches='tight')
        self.figures.append('grafico_fps_triangulos.png')
        plt.close()
    
    def plot_lighting_comparison(self, data):
        """Gera gráfico comparativo de iluminação"""
        if not data:
            return
        
        results = data['results']
        light_types = {}
        
        for r in results:
            light = r['light_type']
            if light not in light_types:
                light_types[light] = {'counts': [], 'fps': [], 'cpu': [], 'gpu': []}
            light_types[light]['counts'].append(r['triangle_count'])
            light_types[light]['fps'].append(r['avg_fps'])
            light_types[light]['cpu'].append(r['avg_cpu'])
            light_types[light]['gpu'].append(r.get('avg_gpu', 0))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        colors = {'none': 'blue', 'omnidirectional': 'green', 
                 'spot': 'orange', 'multiple': 'red'}
        markers = {'none': 'o', 'omnidirectional': 's', 
                  'spot': '^', 'multiple': 'd'}
        
        # Gráfico FPS
        for light, values in light_types.items():
            ax1.plot(values['counts'], values['fps'], 
                    color=colors.get(light, 'black'), 
                    marker=markers.get(light, 'o'),
                    label=light.capitalize(), linewidth=2, markersize=8)
        
        ax1.set_xlabel('Número de Triângulos', fontsize=12)
        ax1.set_ylabel('FPS Médio', fontsize=12)
        ax1.set_title('Impacto da Iluminação no FPS', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico CPU/GPU
        has_gpu_data = any(any(values['gpu']) for values in light_types.values())
        
        if has_gpu_data:
            for light, values in light_types.items():
                if any(values['gpu']):
                    ax2.plot(values['counts'], values['gpu'], 
                            color=colors.get(light, 'black'),
                            marker=markers.get(light, 'o'),
                            label=light.capitalize(), linewidth=2, markersize=8)
            ax2.set_ylabel('Utilização GPU (%)', fontsize=12)
            ax2.set_title('Impacto da Iluminação na GPU', fontsize=14, fontweight='bold')
        else:
            for light, values in light_types.items():
                ax2.plot(values['counts'], values['cpu'], 
                        color=colors.get(light, 'black'),
                        marker=markers.get(light, 'o'),
                        label=light.capitalize(), linewidth=2, markersize=8)
            ax2.set_ylabel('Utilização CPU (%)', fontsize=12)
            ax2.set_title('Impacto da Iluminação na CPU', fontsize=14, fontweight='bold')
            ax2.text(0.5, 0.95, 'GPU não detectada (Apple Silicon)', 
                    transform=ax2.transAxes, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
                    fontsize=9)
        
        ax2.set_xlabel('Número de Triângulos', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('grafico_iluminacao.png', dpi=300, bbox_inches='tight')
        self.figures.append('grafico_iluminacao.png')
        plt.close()
    
    def generate_all_graphs(self):
        """Gera todos os gráficos"""
        print("\n=== Gerando Gráficos ===\n")
        
        basic_data = self.load_json('benchmark_sem_textura.json')
        lighting_data = self.load_json('benchmark_lighting.json')
        texture_data = self.load_json('benchmark_textura.json')
        
        self.plot_basic_benchmark(basic_data)
        self.plot_lighting_comparison(lighting_data)
        # ... outros gráficos ...
        
        print(f"\nTotal de {len(self.figures)} gráficos gerados!")
        return self.figures


# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 5: check_system.py
# ═══════════════════════════════════════════════════════════════════════════

"""
Script para verificar informações do sistema
Detecta CPU, GPU, memória e módulos Python instalados
"""

import sys
import platform
import psutil

def check_system_info():
    """Exibe informações completas do sistema"""
    print("="*60)
    print("INFORMAÇÕES DO SISTEMA")
    print("="*60)
    
    # Sistema Operacional
    print(f"\nSistema: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Máquina: {platform.machine()}")
    print(f"Processador: {platform.processor()}")
    
    # CPU
    print(f"\nCores físicos: {psutil.cpu_count(logical=False)}")
    print(f"Cores lógicos: {psutil.cpu_count(logical=True)}")
    
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        print(f"Frequência: {cpu_freq.current:.2f} MHz")
    
    # Memória
    mem = psutil.virtual_memory()
    print(f"\nRAM Total: {mem.total / (1024**3):.2f} GB")
    print(f"RAM Disponível: {mem.available / (1024**3):.2f} GB")
    print(f"RAM Usada: {mem.percent}%")
    
    # GPU
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"\nGPU {i}: {gpu.name}")
                print(f"Memória: {gpu.memoryTotal} MB")
        else:
            print("\nGPU: Não detectada via GPUtil")
            print("(Normal em Apple Silicon)")
    except ImportError:
        print("\nGPUtil não instalado")


# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 6: demo_quick.py
# ═══════════════════════════════════════════════════════════════════════════

"""
Demo rápido - Visualização de triângulo rotativo
Testa a instalação básica sem executar benchmarks completos
"""

def demo_quick():
    """Demonstração rápida de 5 segundos"""
    print("=== DEMO: Triângulo Rotativo ===")
    print("Renderizando por 5 segundos...")
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -5)
    
    rotation = 0
    clock = pygame.time.Clock()
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desenhar triângulo
        glPushMatrix()
        glRotatef(rotation, 0, 1, 0)
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 1, 0)
        glColor3f(0, 1, 0)
        glVertex3f(-1, -1, 0)
        glColor3f(0, 0, 1)
        glVertex3f(1, -1, 0)
        glEnd()
        glPopMatrix()
        
        pygame.display.flip()
        rotation += 2
        clock.tick(60)
        frame_count += 1
    
    elapsed = time.time() - start_time
    print(f"\nFrames: {frame_count}")
    print(f"FPS médio: {frame_count / elapsed:.2f}")
    pygame.quit()


# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 7: run_all_benchmarks.py
# ═══════════════════════════════════════════════════════════════════════════

"""
Script mestre para executar todos os benchmarks
Coordena a execução sequencial de todos os testes
"""

import subprocess
import sys

def run_all_benchmarks():
    """Executa todos os benchmarks em sequência"""
    print("="*60)
    print("EXECUTANDO TODOS OS BENCHMARKS")
    print("="*60)
    
    benchmarks = [
        ('triangle_benchmark.py', 'Benchmark Básico'),
        ('lighting_benchmark.py', 'Benchmark de Iluminação'),
        ('texture_benchmark.py', 'Benchmark de Texturas')
    ]
    
    for script, description in benchmarks:
        print(f"\n{description}...")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"Erro em {description}")
            return False
    
    # Gerar gráficos
    print("\nGerando gráficos...")
    subprocess.run([sys.executable, 'generate_graphs.py'])
    
    print("\n✓ Todos os benchmarks concluídos!")
    return True


# ═══════════════════════════════════════════════════════════════════════════
# FIM DO CÓDIGO FONTE
# ═══════════════════════════════════════════════════════════════════════════

"""
NOTA FINAL:
───────────

Este arquivo contém todo o código fonte do projeto organizado por módulos.
Cada seção representa um arquivo Python independente que pode ser executado
separadamente.

Para usar este código:
1. Copie cada módulo para seu próprio arquivo .py
2. Instale as dependências: pip install -r requirements.txt
3. Execute os scripts conforme necessário

Ou execute o script mestre run_all_benchmarks.py para rodar tudo.

Desenvolvido para a disciplina de Processamento Digital de Imagens - UEA
Autor: Carlos Neto
Outubro 2024
"""
