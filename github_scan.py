import requests
import time
import os
from dotenv import load_dotenv
import datetime

load_dotenv(dotenv_path='.env', override=True, verbose=True)

def reload_env_config():
    """Força o recarregamento das variáveis de ambiente do arquivo .env"""
    print("Recarregando configurações do arquivo .env...")
    load_dotenv(dotenv_path='.env', override=True, verbose=False)
    
    global TOKEN, SEARCH_TERMS, RESULTS_PER_PAGE, PAGES, SLEEP_TIME, START_DATE, END_DATE, headers
    
    TOKEN = os.getenv('GITHUB_TOKEN')
    SEARCH_TERMS = [t.strip() for t in os.getenv('SEARCH_TERM', '').split(',') if t.strip()]
    RESULTS_PER_PAGE = int(os.getenv('RESULTS_PER_PAGE', '30'))
    PAGES = int(os.getenv('PAGES', '5'))
    SLEEP_TIME = int(os.getenv('SLEEP_TIME', '2'))
    START_DATE = os.getenv('START_DATE')
    END_DATE = os.getenv('END_DATE')
    
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    print(f"Configurações atualizadas: {len(SEARCH_TERMS)} termo(s) de busca")
    return TOKEN is not None

# === CONFIGURAÇÕES ===
TOKEN = os.getenv('GITHUB_TOKEN')
SEARCH_TERMS = [t.strip() for t in os.getenv('SEARCH_TERM', '').split(',') if t.strip()]
RESULTS_PER_PAGE = int(os.getenv('RESULTS_PER_PAGE', '30'))
PAGES = int(os.getenv('PAGES', '5'))
SLEEP_TIME = int(os.getenv('SLEEP_TIME', '2'))
START_DATE = os.getenv('START_DATE')
END_DATE = os.getenv('END_DATE')

if not TOKEN:
    print("❌ ERRO: Token do GitHub não configurado!")
    print("Configure seu token no arquivo .env")
    print("Obtenha um token em: https://github.com/settings/tokens")
    exit(1)

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def search_github(term, page, date_range=None):
    """Busca no GitHub com múltiplas estratégias para emails"""
    import urllib.parse
    
    queries = []
    
    if '@' in term:
        email_parts = term.split('@')
        username = email_parts[0]
        domain = email_parts[1]
        queries.append(f'"{term}" in:file')
        queries.append(f'{term} in:file')
        queries.append(f'"{domain}" in:file')
        queries.append(f'{username} {domain} in:file')
        
    else:
        queries.append(f'"{term}" in:file')
        queries.append(f'{term} in:file')
    
    if date_range:
        queries = [f'{q} created:{date_range}' for q in queries]
    
    for i, query in enumerate(queries):
        print(f"🔍 Tentativa {i+1}/{len(queries)} - Query: {query}")
        
        encoded_query = urllib.parse.quote(query)
        url = f'https://api.github.com/search/code?q={encoded_query}&page={page}&per_page={RESULTS_PER_PAGE}'
        
        print(f"🌐 URL: {url}")
        
        response = requests.get(url, headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total_count = data.get('total_count', 0)
            items = data.get('items', [])
            print(f"📈 Total encontrado: {total_count}, Retornados nesta página: {len(items)}")
            
            if items:  # Se encontrou resultados, retorna
                return items
            else:
                print(f"🚫 Nenhum resultado para esta query, tentando próxima...")
                
        elif response.status_code == 403:
            print(f"⚠️  Rate limit atingido. Aguarde um momento...")
            print(f"Detalhes: {response.headers.get('X-RateLimit-Remaining', 'N/A')} requests restantes")
            return []
        elif response.status_code == 422:
            print(f"⚠️  Query inválida, tentando próxima...")
            print(f"Detalhes: {response.text}")
            continue
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            continue
            
        # Pequena pausa entre tentativas
        time.sleep(0.5)
    
    print(f"🚫 Nenhuma das {len(queries)} estratégias de busca retornou resultados")
    return []

def main():
    if not reload_env_config():
        print("❌ Erro: Token não configurado após recarregar .env")
        exit(1)
    
    date_range = None
    if START_DATE and END_DATE:
        date_range = f'{START_DATE}..{END_DATE}'
    print(f"🔍 Buscando por: {', '.join(SEARCH_TERMS)}")
    
    if not SEARCH_TERMS:
        print("❌ Erro: Nenhum termo de busca configurado no arquivo .env")
        print("Configure a variável SEARCH_TERM no arquivo .env")
        exit(1)
    for term in SEARCH_TERMS:
        print(f"\n=== Termo: {term} ===")
        for page in range(1, PAGES + 1):
            print(f"\nPágina {page}")
            results = search_github(term, page, date_range)
            if not results:
                print("Sem resultados ou fim das páginas.")
                break
            for item in results:
                repo = item['repository']['full_name']
                file_path = item['path']
                html_url = item['html_url']
                print(f"📁 {repo} - {file_path}\n🔗 {html_url}\n")
            time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()

