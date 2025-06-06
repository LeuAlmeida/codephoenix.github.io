#!/bin/bash

# Script para executar o frontend do CodePhoenix

echo "🚀 Iniciando CodePhoenix Frontend..."
echo ""

# Verifica se o diretório frontend existe
if [ ! -d "frontend" ]; then
    echo "❌ Erro: Diretório frontend não encontrado!"
    echo "Execute este script do diretório raiz do projeto."
    exit 1
fi

# Ativa o ambiente virtual
echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

# Verifica dependências
echo "🔍 Verificando dependências..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "🌐 Iniciando servidor..."
echo "📝 Acesse: http://localhost:8080"
echo "⏹️  Pressione Ctrl+C para parar"
echo "="*50

# Inicia o servidor
python server.py

