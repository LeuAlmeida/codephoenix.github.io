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

def detect_data_type(term):
    """Detecta o tipo de dado baseado no padrão do termo"""
    import re
    
    if '@' in term and '.' in term and not term.lower().startswith(('http', 'ftp')):
        return 'email'
    if any(term.lower().startswith(proto) for proto in ['http://', 'https://', 'ftp://', 'ftps://']):
        return 'url'
    if term.count('.') >= 1 and '/' in term and not '@' in term:
        return 'url'
    
    if term.upper().startswith('AKIA'):  # AWS Access Key
        return 'aws_key'
    if len(term) == 40 and re.match(r'^[A-Za-z0-9+/=]+$', term):  # AWS Secret Key pattern
        return 'aws_secret'
    
    if term.lower().startswith(('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_')):  # GitHub tokens
        return 'github_token'
    if term.lower().startswith(('sk-', 'pk_')):  # Stripe, OpenAI patterns
        return 'api_key'
    if term.lower().startswith('bearer '):
        return 'bearer_token'
    
    if term.count('.') == 2 and len(term) > 50:
        return 'jwt_token'
    
    if any(db in term.lower() for db in ['mongodb://', 'mysql://', 'postgresql://', 'redis://']):
        return 'database_url'
    
    if any(keyword in term.lower() for keyword in ['password', 'passwd', 'pwd']):
        return 'password'
    if 'secret' in term.lower() and not any(kw in term.lower() for kw in ['key', 'token', 'api']):
        return 'password'
    
    if any(keyword in term.lower() for keyword in ['api_key', 'apikey', 'token', 'key']) and len(term) > 10:
        return 'api_key'
    if re.match(r'^[A-Za-z0-9]{20,}$', term):
        return 'api_key'
    
    return 'generic'

def generate_search_queries(term, data_type):
    """Gera queries de busca específicas para cada tipo de dado"""
    queries = []
    
    if data_type == 'email':
        email_parts = term.split('@')
        username = email_parts[0]
        domain = email_parts[1]
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'"{domain}" in:file',
            f'{username} {domain} in:file',
            f'"mailto:{term}" in:file',
            f'email:"{term}" in:file'
        ])
    
    elif data_type == 'url':
        # Remove protocol for variations
        clean_url = term.replace('https://', '').replace('http://', '').replace('ftp://', '')
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'"{clean_url}" in:file',
            f'{clean_url} in:file',
            f'url:"{term}" in:file',
            f'href="{term}" in:file'
        ])
    
    elif data_type in ['api_key', 'github_token', 'bearer_token']:
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'token:"{term}" in:file',
            f'key:"{term}" in:file',
            f'api_key:"{term}" in:file',
            f'apikey:"{term}" in:file',
            f'Authorization:"{term}" in:file',
            f'Bearer {term} in:file'
        ])
    
    elif data_type == 'aws_key':
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'AWS_ACCESS_KEY_ID:"{term}" in:file',
            f'access_key:"{term}" in:file',
            f'aws_access_key:"{term}" in:file'
        ])
    
    elif data_type == 'aws_secret':
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'AWS_SECRET_ACCESS_KEY:"{term}" in:file',
            f'secret_key:"{term}" in:file',
            f'aws_secret:"{term}" in:file'
        ])
    
    elif data_type == 'jwt_token':
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'jwt:"{term}" in:file',
            f'token:"{term}" in:file'
        ])
    
    elif data_type == 'database_url':
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'DATABASE_URL:"{term}" in:file',
            f'connection_string:"{term}" in:file'
        ])
    
    elif data_type == 'password':
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file',
            f'password:"{term}" in:file',
            f'passwd:"{term}" in:file',
            f'pwd:"{term}" in:file'
        ])
    
    else:  # generic
        queries.extend([
            f'"{term}" in:file',
            f'{term} in:file'
        ])
    
    return queries

def search_github(term, page, date_range=None):
    """Busca no GitHub com estratégias inteligentes baseadas no tipo de dado"""
    import urllib.parse
    
    # Detecta o tipo de dado
    data_type = detect_data_type(term)
    print(f"🔍 Tipo detectado: {data_type.upper()}")
    
    # Gera queries específicas para o tipo
    queries = generate_search_queries(term, data_type)
    
    # Adiciona filtro de data se especificado
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

