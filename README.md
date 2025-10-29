# OpenGL 3D Performance Analysis

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/CarlosLNeto/opengl-3d-performance-analysis)

A comprehensive performance analysis project for 3D rendering using OpenGL and Python. This project systematically benchmarks graphics performance across different scenarios: varying geometry complexity, lighting configurations, and texture resolutions.

Developed for the Digital Image Processing course at the State University of Amazonas (UEA).

## Overview

This project provides a complete suite for analyzing 3D rendering performance, measuring the impact of:
- **Geometry complexity** (1 to 2000 triangles)
- **Lighting models** (omnidirectional, spotlight, multiple sources)
- **Texture resolutions** (64x64, 128x128, 256x256 pixels)

All tests include detailed metrics: FPS (frames per second), CPU utilization, and GPU utilization.

## Key Features

- Three independent benchmark modules for comprehensive testing
- Real-time FPS tracking with statistical analysis (min, max, average)
- CPU and GPU utilization monitoring
- High-quality visualizations (300 DPI graphs) ready for academic publication
- Complete technical report (13 pages) with data tables and analysis
- Apple Silicon (M3) optimized and tested

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- OpenGL-capable GPU
- 4 GB RAM
- Display with graphics support

### Recommended
- Python 3.10+
- 8 GB RAM
- Dedicated GPU or Apple Silicon

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/CarlosLNeto/opengl-3d-performance-analysis.git
cd opengl-3d-performance-analysis

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Benchmarks

The complete source code is in `codigo_fonte_completo.py`. You can extract and run individual modules or use the provided setup script:

```bash
# Interactive setup (recommended)
./setup.sh

# Or run Python directly with the complete source
# (Extract individual modules as needed)
```

## Project Structure

```
opengl-3d-performance-analysis/
├── README.md                          # This file
├── relatorio.pdf                      # Technical report (13 pages, Portuguese)
├── relatorio.tex                      # LaTeX source code
├── codigo_fonte_completo.py           # Complete source code (all modules)
│
├── benchmark_sem_textura.json         # Basic benchmark results (8 tests)
├── benchmark_lighting.json            # Lighting benchmark results (12 tests)
├── benchmark_textura.json             # Texture benchmark results (16 tests)
├── summary.json                       # Consolidated summary
│
├── grafico_fps_triangulos.png         # FPS vs Triangles graph
├── grafico_iluminacao.png             # Lighting impact graph
├── grafico_texturas.png               # Texture impact graph
├── grafico_comparacao_geral.png       # General comparison graph
│
├── requirements.txt                   # Python dependencies
├── setup.sh                           # Interactive setup script
└── .gitignore                         # Git ignore rules
```

## Benchmarks

### 1. Basic Geometry Benchmark

Tests rendering performance with varying numbers of colored rotating triangles without textures or lighting.

**Configurations tested:** 1, 10, 50, 100, 200, 500, 1000, 2000 triangles  
**Duration:** 5 seconds per configuration  
**Metrics:** FPS (avg/min/max), CPU usage

### 2. Lighting Benchmark

Analyzes the impact of different lighting models on rendering performance.

**Types tested:**
- No lighting (baseline)
- Omnidirectional light (point light)
- Spotlight with cutoff angle
- Multiple lights (3 simultaneous sources)

**Configurations:** 100, 500, 1000 triangles per lighting type

### 3. Texture Benchmark

Evaluates performance impact of procedural textures at different resolutions.

**Resolutions tested:**
- No texture (baseline)
- 64x64 pixels
- 128x128 pixels
- 256x256 pixels

**Configurations:** 100, 500, 1000, 2000 triangles per texture resolution

## Results Summary

### Test System Specifications

- **Processor:** Apple M3 (8 cores: 4 performance + 4 efficiency)
- **GPU:** Apple M3 Integrated (10 cores)
- **Memory:** 16 GB Unified Memory
- **Architecture:** ARM64 (Apple Silicon)
- **OS:** macOS (Darwin 25.0.0)

### Performance Highlights

| Scenario | Triangles | Average FPS | CPU Usage |
|----------|-----------|-------------|-----------|
| Basic | 1 | 147.13 | 2.34% |
| Basic | 100 | 127.84 | 2.05% |
| Basic | 1000 | 120.58 | 1.74% |
| Basic | 2000 | 107.49 | 2.63% |
| Lighting (None) | 1000 | 443.59 | 1.52% |
| Lighting (Multiple) | 1000 | 102.21 | 2.77% |
| Texture (64x64) | 2000 | 473.61 | 3.39% |
| Texture (256x256) | 2000 | 375.24 | 3.75% |

### Key Findings

1. **Excellent Performance:** Apple M3 maintains high FPS even with complex scenes
2. **Low CPU Usage:** Consistent 1-4% CPU utilization indicates efficient GPU processing
3. **Lighting Impact:** Multiple light sources show expected performance degradation
4. **Texture Efficiency:** Surprisingly, textures improved FPS in many scenarios due to efficient cache and Unified Memory Architecture
5. **Smooth Degradation:** Performance scales predictably with scene complexity

## Technical Details

### Software Stack

- **Python:** 3.13.7
- **PyOpenGL:** 3.1.10 (OpenGL interface)
- **Pygame:** 2.6.1 (Window management)
- **NumPy:** 2.3.4 (Numerical processing)
- **Matplotlib:** 3.10.7 (Graph generation)
- **PSUtil:** 7.1.2 (System monitoring)

### Modules Included

The `codigo_fonte_completo.py` file contains seven complete modules:

1. **Triangle Benchmark** - Basic geometry performance testing
2. **Lighting Benchmark** - Lighting impact analysis
3. **Texture Benchmark** - Texture resolution performance testing
4. **Graph Generator** - Automatic visualization creation
5. **System Check** - Hardware detection and verification
6. **Quick Demo** - 5-second validation test
7. **Master Script** - Coordinated execution of all benchmarks

## Data Format

All benchmark data is stored in JSON format with the following structure:

```json
{
  "timestamp": "ISO 8601 datetime",
  "system_info": {
    "cpu": "physical cores",
    "cpu_logical": "logical cores",
    "cpu_freq": "max frequency in MHz",
    "ram": "total RAM in GB",
    "gpu_available": "boolean",
    "gpu_count": "number of GPUs",
    "gpu_info": []
  },
  "results": [
    {
      "triangle_count": "number",
      "avg_fps": "average FPS",
      "min_fps": "minimum FPS",
      "max_fps": "maximum FPS",
      "avg_cpu": "average CPU %",
      "avg_gpu": "average GPU %",
      "total_frames": "total frames rendered"
    }
  ]
}
```

Additional fields for specific benchmarks:
- **Lighting:** `light_type` ("none", "omnidirectional", "spot", "multiple")
- **Texture:** `use_texture` (boolean), `texture_size` ("64x64", "128x128", "256x256")

## GPU Detection on Apple Silicon

**Important Note:** The GPUtil library does not detect Apple Silicon GPUs as it was designed for NVIDIA hardware. This is expected behavior and does not indicate a problem.

### Verification of GPU Usage

Evidence that the GPU is being actively used:
1. Very low CPU usage (1-4%) during intensive rendering
2. High and consistent FPS across all tests
3. Ability to render thousands of triangles in real-time

### Alternative Monitoring for Apple Silicon

To monitor Apple GPU usage:

```bash
sudo powermetrics --samplers gpu_power -i 1000
```

This provides:
- GPU utilization percentage
- Active frequency
- Power consumption
- Renderer information

## Documentation

### Technical Report

The included `relatorio.pdf` (13 pages, in Portuguese) contains:

1. **Introduction** - Project context and objectives
2. **Methodology** - Detailed test procedures and configurations
3. **Results** - Three comprehensive data tables with 36 measurements
4. **Hardware Analysis** - CPU and GPU utilization patterns
5. **Discussion** - Technical analysis and Apple Silicon architecture details
6. **Conclusions** - Key findings and recommendations
7. **References** - Academic and technical resources

### Data Tables

The report includes detailed tables with all benchmark results:
- **Table 1:** Basic Benchmark (8 configurations)
- **Table 2:** Lighting Benchmark (12 configurations)
- **Table 3:** Texture Benchmark (16 configurations)

### Visualizations

Four high-quality graphs (300 DPI, publication-ready):
- FPS vs Triangle Count with resource utilization
- Lighting impact comparison across different types
- Texture resolution performance comparison
- General performance comparison across all scenarios

## Apple Silicon Architecture

This project demonstrates unique characteristics of Apple Silicon:

### Unified Memory Architecture
CPU and GPU share physical memory, eliminating copy overhead and reducing latency.

### Metal Backend
OpenGL executes over Apple's Metal API, leveraging low-level optimizations.

### Tile-Based Rendering
Reduces memory bandwidth requirements through efficient rendering architecture.

### Hardware Acceleration
Dedicated blocks for common graphics operations improve efficiency.

## Academic Context

This project was developed for the **Digital Image Processing** course at the **State University of Amazonas (UEA)** as part of the Computer Engineering curriculum.

### Educational Value

The project demonstrates:
- Scientific methodology in performance analysis
- Professional data visualization techniques
- Comprehensive technical documentation
- Reproducible research practices
- Real-world hardware benchmarking

### Citation

If you use this project in your research or studies:

```
Neto, Carlos. (2024). OpenGL 3D Performance Analysis: 
Comprehensive Benchmarking of Rendering Performance on Apple Silicon.
State University of Amazonas, Computer Engineering.
GitHub: https://github.com/CarlosLNeto/opengl-3d-performance-analysis
```

## Future Extensions

Potential areas for project expansion:

1. **Advanced Rendering Techniques**
   - Deferred shading implementation
   - Shadow mapping
   - Post-processing effects

2. **Cross-Platform Comparison**
   - NVIDIA GPU benchmarks
   - AMD GPU benchmarks
   - Intel integrated graphics comparison

3. **Additional Metrics**
   - Power consumption analysis
   - Memory bandwidth utilization
   - Thermal performance

4. **Complex Scenarios**
   - Real-time ray tracing
   - Complex 3D model rendering
   - Scene complexity analysis

## Contributing

Contributions are welcome! Areas where contributions would be valuable:

- Additional benchmark scenarios
- Cross-platform testing and optimization
- Documentation improvements
- Bug fixes and performance optimizations

Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Carlos Neto**  
Computer Engineering Student  
State University of Amazonas (UEA)

## Acknowledgments

- State University of Amazonas (UEA) - Digital Image Processing Course
- OpenGL and PyOpenGL developer communities
- Apple Metal documentation team
- Python scientific computing community (NumPy, Matplotlib)

## References

1. OpenGL Programming Guide - The Official Guide to Learning OpenGL
2. Real-Time Rendering, Akenine-Möller, Haines, and Hoffman
3. GPU Gems Series - NVIDIA Corporation
4. PyOpenGL Documentation - http://pyopengl.sourceforge.net/
5. Apple Metal Documentation - Performance Best Practices
6. Apple Silicon GPU Architecture - Technical Specifications

---

**Last Updated:** October 2024  
**Version:** 2.0  
**Status:** Complete and Production-Ready

## Objetivos

O projeto foi desenvolvido para responder às seguintes questões fundamentais:

1. **Análise de Desempenho Geométrico**
   - Qual a relação entre quantidade de triângulos e FPS (Frames Per Second)?
   - Como o desempenho degrada com o aumento da complexidade geométrica?

2. **Detecção e Utilização de Hardware**
   - O sistema possui GPU? Qual modelo?
   - A GPU está sendo utilizada durante a renderização?
   - É possível monitorar a utilização percentual da GPU?
   - O sistema possui múltiplas GPUs?

3. **Análise de Processador**
   - Qual o processador do sistema?
   - Como a utilização do processador varia durante a renderização?
   - Existe correlação entre complexidade da cena e uso de CPU?

4. **Impacto da Iluminação**
   - Como diferentes tipos de iluminação afetam o desempenho?
   - Qual o impacto de luzes omnidirecionais versus spotlights?
   - Múltiplas fontes de luz degradam significativamente o desempenho?

5. **Impacto de Texturas**
   - Texturas afetam o desempenho? Em que magnitude?
   - Diferentes resoluções de textura têm impactos distintos?
   - Existem otimizações específicas de hardware?

## Especificações do Sistema de Teste

### Hardware

- **Processador:** Apple M3 (8 cores: 4 performance + 4 efficiency)
- **Frequência:** 744 MHz - 4056 MHz (adaptativa)
- **Memória RAM:** 16 GB (Unified Memory Architecture)
- **GPU:** Apple M3 Integrada ao SoC
- **Arquitetura:** ARM64 (Apple Silicon)
- **Sistema Operacional:** macOS (Darwin 25.0.0)

### Software

- **Linguagem:** Python 3.13.7
- **OpenGL:** PyOpenGL 3.1.10
- **Gerenciamento de Janelas:** Pygame 2.6.1
- **Processamento Numérico:** NumPy 2.3.4
- **Visualização:** Matplotlib 3.10.7
- **Monitoramento:** PSUtil 7.1.2

## Metodologia

### Cenários de Teste

O projeto implementa três benchmarks independentes:

#### 1. Benchmark Básico
Renderização de triângulos coloridos sem texturas ou iluminação, servindo como baseline para comparações. Configurações testadas:
- Quantidades: 1, 10, 50, 100, 200, 500, 1000, 2000 triângulos
- Duração: 5 segundos por configuração
- Métricas: FPS, CPU, GPU (quando detectável)

#### 2. Benchmark de Iluminação
Análise do impacto de diferentes modelos de iluminação:
- Sem iluminação (baseline)
- Luz omnidirecional (point light)
- Spotlight com ângulo de corte
- Múltiplas fontes de luz (3 luzes simultâneas)

Testado com 100, 500 e 1000 triângulos em cada configuração.

#### 3. Benchmark de Texturas
Avaliação do impacto de texturas procedurais:
- Sem textura (baseline)
- Textura 64x64 pixels
- Textura 128x128 pixels
- Textura 256x256 pixels

Testado com 100, 500, 1000 e 2000 triângulos para cada resolução.

### Métricas Coletadas

Para cada configuração, o sistema registra:

- **FPS (Frames Per Second):** Médio, mínimo e máximo
- **Utilização de CPU:** Percentual médio durante o teste
- **Utilização de GPU:** Percentual médio (quando detectável)
- **Total de Frames:** Quantidade de quadros renderizados
- **Tempo de Execução:** Duração precisa do teste

## Estrutura de Arquivos

### Documentação

- **relatorio.pdf** (12 páginas) - Relatório técnico completo com análise científica
- **relatorio.tex** - Código fonte LaTeX do relatório
- **README.md** - Este arquivo

### Código Fonte

- **codigo_fonte_completo.py** (30 KB) - Implementação completa de todos os módulos
  - Triangle Benchmark - Benchmark básico
  - Lighting Benchmark - Benchmark de iluminação
  - Texture Benchmark - Benchmark de texturas
  - Graph Generator - Geração de gráficos
  - System Check - Verificação de hardware
  - Demo Quick - Demonstração rápida
  - Master Script - Coordenação de execução

### Dados dos Benchmarks (JSON)

- **benchmark_sem_textura.json** (2.5 KB) - Resultados do benchmark básico
- **benchmark_lighting.json** (3.9 KB) - Resultados do benchmark de iluminação
- **benchmark_textura.json** (5.7 KB) - Resultados do benchmark de texturas
- **summary.json** (1.5 KB) - Resumo consolidado dos testes

### Visualizações (PNG, 300 DPI)

- **grafico_fps_triangulos.png** (237 KB) - FPS vs Quantidade de Triângulos
- **grafico_iluminacao.png** (368 KB) - Impacto da Iluminação no Desempenho
- **grafico_texturas.png** (313 KB) - Impacto das Texturas no Desempenho
- **grafico_comparacao_geral.png** (194 KB) - Comparação Consolidada

### Configuração

- **requirements.txt** - Dependências Python
- **setup.sh** - Script de configuração automática
- **venv/** - Ambiente virtual Python

## Principais Resultados

### Desempenho Básico

O sistema Apple M3 demonstrou excelente capacidade de renderização:

- **1 triângulo:** 147.13 FPS
- **100 triângulos:** 127.84 FPS
- **1000 triângulos:** 120.58 FPS
- **2000 triângulos:** 107.49 FPS

A degradação de desempenho foi suave e previsível, mantendo FPS acima de 100 em todas as configurações testadas.

### Utilização de Recursos

- **CPU:** Utilização consistentemente baixa (1-4%), indicando processamento eficiente na GPU
- **GPU:** Não detectada via GPUtil (limitação da ferramenta com Apple Silicon)
- **Memória:** Estável durante todos os testes

### Impacto da Iluminação

Resultados contra-intuitivos foram observados:

- Iluminação simples frequentemente melhorou o FPS
- Exemplo: 100 triângulos sem luz (130.71 FPS) vs com spotlight (251.91 FPS)
- Múltiplas luzes causaram degradação esperada: 1000 triângulos com 3 luzes (102.21 FPS)

Fenômeno explicado por VSync e otimizações de pipeline do Metal backend.

### Impacto de Texturas

Resultados surpreendentes com melhoria de desempenho:

- 100 triângulos sem textura: 130.28 FPS
- 100 triângulos com textura 64x64: 364.41 FPS
- 2000 triângulos sem textura: 418.77 FPS
- 2000 triângulos com textura 64x64: 473.61 FPS

Atribuído ao cache de textura eficiente e Unified Memory Architecture do Apple Silicon.

## Detecção de GPU em Apple Silicon

### Limitação de Ferramentas

O GPUtil, ferramenta padrão para monitoramento de GPU, não detecta GPUs Apple Silicon pois foi desenvolvida especificamente para GPUs NVIDIA. Isto é um comportamento esperado e não indica ausência de GPU.

### Confirmação de Utilização

A GPU Apple M3 está sendo utilizada, como evidenciado por:

1. Baixa utilização de CPU (1-4%) durante renderização intensiva
2. FPS elevado consistente
3. Capacidade de processar milhares de triângulos em tempo real

### Monitoramento Alternativo

Para monitorar GPU Apple Silicon, utilize:

```bash
sudo powermetrics --samplers gpu_power -i 1000
```

Este comando fornece:
- Utilização percentual da GPU
- Frequência ativa
- Consumo de energia
- Informações do renderizador

## Arquitetura Apple Silicon

### Características Únicas

O desempenho excepcional observado deve-se a:

1. **Unified Memory Architecture:** CPU e GPU compartilham memória física, eliminando overhead de cópias
2. **Metal Backend:** OpenGL executa sobre Metal, aproveitando otimizações de baixo nível
3. **GPU Integrada Potente:** Desempenho comparável a GPUs dedicadas entry-level
4. **Tile-Based Rendering:** Arquitetura que reduz bandwidth de memória
5. **Hardware Acceleration:** Blocos dedicados para operações gráficas comuns

### Implicações para Desenvolvimento

- Excelente desempenho para aplicações gráficas sem GPU dedicada
- Consumo energético reduzido comparado a soluções discretas
- Ideal para desenvolvimento de aplicações 3D em tempo real

## Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Interface gráfica ativa

### Configuração Rápida

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # macOS/Linux

# Instalar dependências
pip install -r requirements.txt
```

### Execução dos Benchmarks

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar benchmarks (implementado em codigo_fonte_completo.py)
# Cada módulo pode ser extraído e executado independentemente
```

### Geração de Gráficos

Os gráficos são gerados automaticamente durante a execução dos benchmarks. Para regenerá-los:

```bash
# Extrair módulo generate_graphs do codigo_fonte_completo.py
# Executar com dados JSON existentes
```

### Compilação do Relatório

```bash
# Primeira compilação
pdflatex relatorio.tex

# Segunda compilação (referências)
pdflatex relatorio.tex
```

## Formato dos Dados JSON

### Estrutura Padrão

```json
{
  "timestamp": "ISO 8601 datetime",
  "system_info": {
    "cpu": "número de cores físicos",
    "cpu_logical": "número de cores lógicos",
    "cpu_freq": "frequência máxima em MHz",
    "ram": "memória total em GB",
    "gpu_available": "boolean",
    "gpu_count": "número",
    "gpu_info": []
  },
  "results": [
    {
      "triangle_count": "número",
      "avg_fps": "float",
      "min_fps": "float",
      "max_fps": "float",
      "avg_cpu": "percentual",
      "avg_gpu": "percentual",
      "total_frames": "número"
    }
  ]
}
```

### Campos Específicos

**Benchmark de Iluminação:**
- `light_type`: "none", "omnidirectional", "spot", ou "multiple"

**Benchmark de Texturas:**
- `use_texture`: boolean
- `texture_size`: "none", "64x64", "128x128", ou "256x256"

## Conclusões

Este estudo demonstrou que:

1. **Desempenho Excepcional:** O Apple M3 mantém FPS elevado mesmo com cargas complexas
2. **Eficiência Energética:** Baixa utilização de CPU indica processamento eficiente na GPU
3. **Otimizações Arquiteturais:** Unified Memory e Metal backend proporcionam vantagens significativas
4. **Resultados Contra-Intuitivos:** Iluminação e texturas podem melhorar FPS em alguns cenários
5. **Limitações de Detecção:** Ferramentas tradicionais não detectam GPUs Apple Silicon

## Trabalhos Futuros

Sugestões para extensão deste projeto:

1. Implementação de técnicas avançadas de renderização (deferred shading, shadow mapping)
2. Comparação com outros hardwares (GPUs NVIDIA/AMD, Intel)
3. Análise de consumo energético durante renderização
4. Teste com modelos 3D complexos e cenários realistas
5. Implementação de ray tracing em tempo real

## Referências

1. OpenGL Programming Guide - The Official Guide to Learning OpenGL
2. Real-Time Rendering, Akenine-Möller, Haines, and Hoffman
3. GPU Gems Series - NVIDIA Corporation
4. PyOpenGL Documentation - http://pyopengl.sourceforge.net/
5. Apple Metal Documentation - Performance Best Practices
6. Apple Silicon GPU Architecture - Technical Whitepaper

## Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Processamento Digital de Imagens da Universidade do Estado do Amazonas.

## Contato

Para questões sobre este projeto, entre em contato através dos canais oficiais da Universidade do Estado do Amazonas - UEA.

---

**Última atualização:** Outubro 2024  
**Versão do documento:** 2.0
