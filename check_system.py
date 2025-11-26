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


if __name__ == "__main__":
    check_system_info()

