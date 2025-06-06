#!/usr/bin/env python3
"""
Script para comparar resultados com e sem filtro de data
"""

import requests
import os
from dotenv import load_dotenv
import urllib.parse
import time
from pathlib import Path

# Add scanner package to path
sys.path.append(str(Path(__file__).parent.parent))

from core.github_scan import reload_env_config

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)
TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def test_comparison(term):
    print(f"🧪 Comparando resultados para: {term}")
    print("="*60)
    
    query1 = f'"{term}" in:file'
    encoded_query1 = urllib.parse.quote(query1)
    url1 = f'https://api.github.com/search/code?q={encoded_query1}&per_page=3'
    
    print(f"\nSEM filtro de data:")
    print(f"Query: {query1}")
    
    response1 = requests.get(url1, headers=headers)
    if response1.status_code == 200:
        data1 = response1.json()
        total1 = data1.get('total_count', 0)
        items1 = data1.get('items', [])
        print(f"📈 Total: {total1} resultados")
        
        if items1:
            print("📝 Amostra de repositórios:")
            for item in items1[:3]:
                repo = item['repository']['full_name']
                created = item['repository'].get('created_at', 'N/A')[:10]
                pushed = item['repository'].get('pushed_at', 'N/A')[:10]
                print(f"   • {repo} (criado: {created}, último push: {pushed})")
    else:
        print(f"❌ Erro: {response1.status_code}")
    
    time.sleep(2)
    
    query2 = f'"{term}" in:file pushed:2020-01-01..2024-12-31'
    encoded_query2 = urllib.parse.quote(query2)
    url2 = f'https://api.github.com/search/code?q={encoded_query2}&per_page=3'
    
    print(f"\nCOM filtro de data (pushed 2020-2024):")
    print(f"Query: {query2}")
    
    response2 = requests.get(url2, headers=headers)
    if response2.status_code == 200:
        data2 = response2.json()
        total2 = data2.get('total_count', 0)
        items2 = data2.get('items', [])
        print(f"📈 Total: {total2} resultados")
        
        if items2:
            print("📝 Amostra de repositórios:")
            for item in items2[:3]:
                repo = item['repository']['full_name']
                created = item['repository'].get('created_at', 'N/A')[:10]
                pushed = item['repository'].get('pushed_at', 'N/A')[:10]
                print(f"   • {repo} (criado: {created}, último push: {pushed})")
        else:
            print("🚫 Nenhum resultado com filtro de data")
    else:
        print(f"❌ Erro: {response2.status_code} - {response2.text[:100]}")
    
    print(f"\n📊 Comparação:")
    if response1.status_code == 200 and response2.status_code == 200:
        reduction = ((total1 - total2) / total1 * 100) if total1 > 0 else 0
        print(f"   • Sem filtro: {total1} resultados")
        print(f"   • Com filtro: {total2} resultados")
        print(f"   • Redução: {reduction:.1f}%")
        
        if total2 == 0:
            print("⚠️  O filtro de data está muito restritivo - considere expandir o range")
        elif reduction > 90:
            print("⚠️  Filtro muito restritivo - a maioria dos repos é mais antiga")
        elif reduction > 50:
            print("✅ Filtro razoável - boa redução de ruído")
        else:
            print("📝 Filtro pouco restritivo - consider usar datas mais recentes")

if __name__ == "__main__":
    search_term = os.getenv('SEARCH_TERM', '@google.com')
    test_comparison(search_term) 