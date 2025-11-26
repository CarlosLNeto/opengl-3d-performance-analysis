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
    
    def plot_texture_comparison(self, data):
        """Gera gráfico comparativo de texturas"""
        if not data:
            return
        
        results = data['results']
        texture_types = {}
        
        for r in results:
            tex = r['texture_size']
            if tex not in texture_types:
                texture_types[tex] = {'counts': [], 'fps': [], 'cpu': [], 'gpu': []}
            texture_types[tex]['counts'].append(r['triangle_count'])
            texture_types[tex]['fps'].append(r['avg_fps'])
            texture_types[tex]['cpu'].append(r['avg_cpu'])
            texture_types[tex]['gpu'].append(r.get('avg_gpu', 0))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        colors = {'none': 'blue', '64x64': 'green', '128x128': 'orange', '256x256': 'red'}
        markers = {'none': 'o', '64x64': 's', '128x128': '^', '256x256': 'd'}
        labels = {'none': 'Sem Textura', '64x64': '64x64', '128x128': '128x128', '256x256': '256x256'}
        
        # Gráfico FPS
        for tex, values in sorted(texture_types.items(), key=lambda x: 0 if x[0] == 'none' else int(x[0].split('x')[0])):
            ax1.plot(values['counts'], values['fps'], 
                    color=colors.get(tex, 'black'), 
                    marker=markers.get(tex, 'o'),
                    label=labels.get(tex, tex), linewidth=2, markersize=8)
        
        ax1.set_xlabel('Número de Triângulos', fontsize=12)
        ax1.set_ylabel('FPS Médio', fontsize=12)
        ax1.set_title('Impacto das Texturas no FPS', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico CPU
        for tex, values in sorted(texture_types.items(), key=lambda x: 0 if x[0] == 'none' else int(x[0].split('x')[0])):
            ax2.plot(values['counts'], values['cpu'], 
                    color=colors.get(tex, 'black'),
                    marker=markers.get(tex, 'o'),
                    label=labels.get(tex, tex), linewidth=2, markersize=8)
        
        ax2.set_xlabel('Número de Triângulos', fontsize=12)
        ax2.set_ylabel('Utilização CPU (%)', fontsize=12)
        ax2.set_title('Impacto das Texturas na CPU', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('grafico_texturas.png', dpi=300, bbox_inches='tight')
        self.figures.append('grafico_texturas.png')
        plt.close()
    
    def plot_general_comparison(self, basic_data, lighting_data, texture_data):
        """Gera gráfico de comparação geral entre todos os cenários"""
        if not basic_data or not lighting_data or not texture_data:
            print("⚠️  Dados insuficientes para gráfico de comparação geral")
            return
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Dados do benchmark básico (1000 triângulos)
        basic_results = [r for r in basic_data['results'] if r['triangle_count'] == 1000]
        if basic_results:
            basic_fps = basic_results[0]['avg_fps']
            ax.bar(0, basic_fps, color='blue', label='Básico', width=0.6)
            ax.text(0, basic_fps + 5, f'{basic_fps:.1f}', ha='center', fontsize=10, fontweight='bold')
        
        # Dados de iluminação (1000 triângulos)
        x_pos = 1
        light_types_order = ['none', 'omnidirectional', 'spot', 'multiple']
        light_colors = {'none': 'lightblue', 'omnidirectional': 'lightgreen', 
                       'spot': 'lightyellow', 'multiple': 'lightcoral'}
        
        for light_type in light_types_order:
            light_results = [r for r in lighting_data['results'] 
                           if r['triangle_count'] == 1000 and r['light_type'] == light_type]
            if light_results:
                fps = light_results[0]['avg_fps']
                ax.bar(x_pos, fps, color=light_colors.get(light_type, 'gray'), 
                      label=f'Luz: {light_type}', width=0.6)
                ax.text(x_pos, fps + 5, f'{fps:.1f}', ha='center', fontsize=9)
                x_pos += 1
        
        # Dados de textura (1000 triângulos)
        texture_order = ['none', '64x64', '128x128', '256x256']
        texture_colors = {'none': 'lightblue', '64x64': 'lightgreen', 
                         '128x128': 'lightyellow', '256x256': 'lightcoral'}
        
        for tex_size in texture_order:
            tex_results = [r for r in texture_data['results'] 
                          if r['triangle_count'] == 1000 and r['texture_size'] == tex_size]
            if tex_results:
                fps = tex_results[0]['avg_fps']
                label = 'Sem Tex' if tex_size == 'none' else f'Tex: {tex_size}'
                ax.bar(x_pos, fps, color=texture_colors.get(tex_size, 'gray'), 
                      label=label, width=0.6)
                ax.text(x_pos, fps + 5, f'{fps:.1f}', ha='center', fontsize=9)
                x_pos += 1
        
        ax.set_ylabel('FPS Médio', fontsize=12)
        ax.set_title('Comparação Geral de Desempenho (1000 Triângulos)', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9, ncol=2)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticks([])
        
        # Adicionar linha de referência
        if basic_results:
            ax.axhline(y=basic_fps, color='r', linestyle='--', alpha=0.3, 
                      label=f'Baseline: {basic_fps:.1f} FPS')
        
        plt.tight_layout()
        plt.savefig('grafico_comparacao_geral.png', dpi=300, bbox_inches='tight')
        self.figures.append('grafico_comparacao_geral.png')
        plt.close()
    
    def generate_all_graphs(self):
        """Gera todos os gráficos"""
        print("\n=== Gerando Gráficos ===\n")
        
        basic_data = self.load_json('benchmark_sem_textura.json')
        lighting_data = self.load_json('benchmark_lighting.json')
        texture_data = self.load_json('benchmark_textura.json')
        
        if basic_data:
            print("📊 Gerando gráfico de benchmark básico...")
            self.plot_basic_benchmark(basic_data)
        else:
            print("⚠️  Dados de benchmark básico não encontrados")
        
        if lighting_data:
            print("📊 Gerando gráfico de iluminação...")
            self.plot_lighting_comparison(lighting_data)
        else:
            print("⚠️  Dados de benchmark de iluminação não encontrados")
        
        if texture_data:
            print("📊 Gerando gráfico de texturas...")
            self.plot_texture_comparison(texture_data)
        else:
            print("⚠️  Dados de benchmark de texturas não encontrados")
        
        if basic_data and lighting_data and texture_data:
            print("📊 Gerando gráfico de comparação geral...")
            self.plot_general_comparison(basic_data, lighting_data, texture_data)
        
        print(f"\n✅ Total de {len(self.figures)} gráficos gerados!")
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

