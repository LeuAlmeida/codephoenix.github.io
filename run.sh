#!/bin/bash
# Script para executar o GitHub Scanner

show_loading() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\\'
    local text="$2"
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf "\r%s [%c]" "$text" "$spinstr"
        local spinstr=$temp${spinstr%$temp}
        sleep $delay
    done
    printf "\r%s [✔]\n" "$text"
}

run_with_loading() {
    local command="$1"
    local message="$2"
    
    echo "$message"
    $command &
    local pid=$!
    show_loading $pid "$message"
    wait $pid
    return $?
}

echo "🚀 GitHub Scanner - Iniciando..."
echo ""

run_with_loading 'source venv/bin/activate' 'Ativando ambiente virtual...'
echo ""

run_with_loading 'pip install -r requirements.txt' 'erificando e instalando dependências...'
echo ""

if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copie o arquivo .env.example para .env e configure suas variáveis"
    exit 1
fi

run_with_loading 'python github_scan.py' '🔍 Executando GitHub Scanner...'
local_exit_code=$?

echo ""
if [ $local_exit_code -eq 0 ]; then
    echo "✅ Scanner executado com sucesso!"
else
    echo "❌ Erro durante a execução do scanner"
    echo "💡 Verifique se o token do GitHub está configurado corretamente no arquivo .env"
fi

echo "🏁 Processo finalizado!"

