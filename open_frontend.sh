#!/bin/bash

# Script para abrir o frontend do CodePhoenix sem servidor Python

echo "🌐 CodePhoenix Frontend - Modo Demonstração"
echo "="*50
echo ""
echo "📝 Esta versão funciona em modo demonstração/simulação"
echo "🛡️  Mostra como seria a interface com resultados simulados"
echo "🔍 Para usar o scanner real, execute: ./run.sh"
echo ""
echo "🚀 Abrindo frontend..."

# Verifica se o arquivo existe
if [ ! -f "frontend/index.html" ]; then
    echo "❌ Erro: frontend/index.html não encontrado!"
    exit 1
fi

# Abre o frontend no navegador padrão
if command -v open >/dev/null 2>&1; then
    # macOS
    open frontend/index.html
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open frontend/index.html
elif command -v start >/dev/null 2>&1; then
    # Windows
    start frontend/index.html
else
    echo "📝 Abra manualmente o arquivo: frontend/index.html"
fi

echo "✅ Frontend aberto no navegador!"
echo ""
echo "📝 Como usar:"
echo "  1. Preencha um token GitHub (qualquer token válido)"
echo "  2. Digite: @google.com,github.com"
echo "  3. Clique em 'Iniciar Scanner'"
echo "  4. Veja os resultados simulados!"
echo ""
echo "💫 Para scanner real com GitHub API:"
echo "  ./run.sh"

