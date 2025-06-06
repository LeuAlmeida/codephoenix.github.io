#!/usr/bin/env python3
"""
Script para testar diferentes filtros de data na API do GitHub
"""

import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def test_date_filter(term, date_filter=None):
    """Testa diferentes filtros de data"""
    base_query = f'"{term}" in:file'
    
    if date_filter:
        query = f'{base_query} {date_filter}'
    else:
        query = base_query
    
    print(f"\n🔍 Testando: {query}")
    
    encoded_query = urllib.parse.quote(query)
    url = f'https://api.github.com/search/code?q={encoded_query}&per_page=5'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        total_count = data.get('total_count', 0)
        items = data.get('items', [])
        
        print(f"📊 Status: {response.status_code}")
        print(f"📈 Total encontrado: {total_count}")
        
        if items:
            print("📝 Primeiros resultados:")
            for i, item in enumerate(items[:3], 1):
                repo = item['repository']['full_name']
                # Pegar data do último commit do repositório
                repo_data = item['repository']
                created_at = repo_data.get('created_at', 'N/A')
                updated_at = repo_data.get('updated_at', 'N/A')
                
                print(f"   {i}. {repo}")
                print(f"      Criado: {created_at}")
                print(f"      Atualizado: {updated_at}")
        else:
            print("❌ Nenhum resultado encontrado")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")

def main():
    term = "@google.com"
    
    print("🧪 Teste de Filtros de Data do GitHub API")
    print("="*50)
    
    test_date_filter(term)
    
    date_filters = [
        "created:2020-01-01..2025-12-31",
        "created:>2020-01-01",
        "created:>=2020-01-01",
        "created:2022-01-01..*",
        "pushed:2020-01-01..2025-12-31",
        "pushed:>2020-01-01",
        "updated:2020-01-01..2025-12-31",
        "updated:>2020-01-01"
    ]
    
    for date_filter in date_filters:
        test_date_filter(term, date_filter)
        print("-" * 30)

if __name__ == "__main__":
    main()

