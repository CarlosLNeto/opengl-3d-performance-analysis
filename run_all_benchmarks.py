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


if __name__ == "__main__":
    run_all_benchmarks()

