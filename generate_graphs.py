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


if __name__ == "__main__":
    print("="*60)
    print("GERADOR DE GRÁFICOS")
    print("="*60)
    
    generator = GraphGenerator()
    figures = generator.generate_all_graphs()
    
    print("\n" + "="*60)
    print("Gráficos criados:")
    for fig in figures:
        print(f"  • {fig}")
    print("="*60)

