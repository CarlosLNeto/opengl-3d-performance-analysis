#!/bin/bash

# Script de configuração e execução do projeto
# Análise de Desempenho em Renderização 3D

echo "============================================================"
echo "   ANÁLISE DE DESEMPENHO EM RENDERIZAÇÃO 3D COM OPENGL"
echo "============================================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✓ Ambiente virtual criado"
else
    echo "✓ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependências instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo ""
echo "============================================================"
echo "   VERIFICANDO SISTEMA"
echo "============================================================"
echo ""

# Verificar sistema
python check_system.py

echo ""
echo "============================================================"
echo "   OPÇÕES DISPONÍVEIS"
echo "============================================================"
echo ""
echo "1) Demo rápido (5 segundos) - Testar instalação"
echo "2) Executar todos os benchmarks (~ 15-20 minutos)"
echo "3) Executar benchmark básico apenas"
echo "4) Executar benchmark de iluminação"
echo "5) Executar benchmark de texturas"
echo "6) Gerar gráficos (requer dados existentes)"
echo "7) Compilar relatório LaTeX"
echo "0) Sair"
echo ""
read -p "Escolha uma opção: " choice

case $choice in
    1)
        echo ""
        echo "Executando demo rápido..."
        python demo_quick.py
        ;;
    2)
        echo ""
        echo "Executando todos os benchmarks..."
        echo "Isso pode levar 15-20 minutos."
        read -p "Deseja continuar? (s/n): " confirm
        if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
            python run_all_benchmarks.py
        fi
        ;;
    3)
        echo ""
        echo "Executando benchmark básico..."
        python triangle_benchmark.py
        ;;
    4)
        echo ""
        echo "Executando benchmark de iluminação..."
        python lighting_benchmark.py
        ;;
    5)
        echo ""
        echo "Executando benchmark de texturas..."
        python texture_benchmark.py
        ;;
    6)
        echo ""
        echo "Gerando gráficos..."
        python generate_graphs.py
        ;;
    7)
        echo ""
        echo "Compilando relatório LaTeX..."
        if command -v pdflatex &> /dev/null; then
            pdflatex -interaction=nonstopmode relatorio.tex
            pdflatex -interaction=nonstopmode relatorio.tex
            echo "✓ Relatório compilado: relatorio.pdf"
        else
            echo "❌ pdflatex não encontrado"
            echo "Instale uma distribuição LaTeX:"
            echo "  macOS: brew install --cask mactex"
            echo "  Linux: sudo apt install texlive-full"
        fi
        ;;
    0)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "   CONCLUÍDO!"
echo "============================================================"
echo ""
echo "Arquivos gerados estão no diretório atual."
echo "Para executar novamente: ./setup.sh"
echo ""
