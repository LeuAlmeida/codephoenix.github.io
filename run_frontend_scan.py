#!/usr/bin/env python3
"""
Script para executar o GitHub Scanner diretamente do frontend
Recebe parâmetros via linha de comando e salva resultados em JSON
"""

import json
import sys
import os
import argparse
from pathlib import Path
from github_scan import reload_env_config, main as run_scanner
import contextlib
import io

def create_env_from_params(token, search_terms, results_per_page=30, pages=5, sleep_time=2, start_date=None, end_date=None):
    """Cria arquivo .env temporário com os parâmetros fornecidos"""
    env_content = f"""GITHUB_TOKEN={token}
SEARCH_TERM={search_terms}
RESULTS_PER_PAGE={results_per_page}
PAGES={pages}
SLEEP_TIME={sleep_time}
"""
    
    if start_date:
        env_content += f"START_DATE={start_date}\n"
    if end_date:
        env_content += f"END_DATE={end_date}\n"
    
    return env_content

def backup_restore_env():
    """Context manager para backup e restore do .env"""
    class EnvBackup:
        def __init__(self):
            self.backup_path = '.env.backup_frontend'
            self.original_exists = os.path.exists('.env')
            
        def __enter__(self):
            if self.original_exists:
                # Faz backup do .env original
                with open('.env', 'r') as f:
                    content = f.read()
                with open(self.backup_path, 'w') as f:
                    f.write(content)
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Remove .env temporário
            if os.path.exists('.env'):
                os.remove('.env')
            
            # Restaura .env original
            if self.original_exists and os.path.exists(self.backup_path):
                os.rename(self.backup_path, '.env')
            elif os.path.exists(self.backup_path):
                os.remove(self.backup_path)
    
    return EnvBackup()

def run_scan_with_params(token, search_terms, results_per_page=30, pages=5, sleep_time=2, start_date=None, end_date=None):
    """Executa o scanner com parâmetros específicos"""
    
    try:
        # Cria arquivo .env temporário
        env_content = create_env_from_params(
            token, search_terms, results_per_page, pages, sleep_time, start_date, end_date
        )
        
        with backup_restore_env():
            # Escreve .env temporário
            with open('.env', 'w') as f:
                f.write(env_content)
            
            # Captura output do scanner
            output_buffer = io.StringIO()
            
            try:
                # Redireciona stdout para capturar output
                with contextlib.redirect_stdout(output_buffer):
                    run_scanner()
                
                output = output_buffer.getvalue()
                
                return {
                    'status': 'success',
                    'message': 'Scanner executado com sucesso',
                    'output': output,
                    'results_found': 'resultados encontrados' in output.lower(),
                    'total_results': output.count('📁') if '📁' in output else 0
                }
                
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Erro durante execução: {str(e)}',
                    'output': output_buffer.getvalue(),
                    'error': str(e)
                }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Erro na configuração: {str(e)}',
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='GitHub Scanner Frontend Interface')
    parser.add_argument('--token', required=True, help='GitHub Token')
    parser.add_argument('--search-terms', required=True, help='Search terms (comma separated)')
    parser.add_argument('--results-per-page', type=int, default=30, help='Results per page')
    parser.add_argument('--pages', type=int, default=5, help='Number of pages')
    parser.add_argument('--sleep-time', type=int, default=2, help='Sleep time between requests')
    parser.add_argument('--start-date', help='Start date filter (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date filter (YYYY-MM-DD)')
    parser.add_argument('--output-file', default='scan_results.json', help='Output JSON file')
    
    args = parser.parse_args()
    
    print("🚀 Iniciando GitHub Scanner...")
    print(f"🔍 Buscando por: {args.search_terms}")
    
    result = run_scan_with_params(
        token=args.token,
        search_terms=args.search_terms,
        results_per_page=args.results_per_page,
        pages=args.pages,
        sleep_time=args.sleep_time,
        start_date=args.start_date,
        end_date=args.end_date
    )
    
    # Salva resultado em JSON
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Resultados salvos em: {args.output_file}")
    
    # Output direto para o console também
    if result['status'] == 'success':
        print("✅ Scanner executado com sucesso!")
        if result.get('total_results', 0) > 0:
            print(f"📊 Total de resultados encontrados: {result['total_results']}")
        else:
            print("📭 Nenhum resultado encontrado")
    else:
        print("❌ Erro durante execução:")
        print(result['message'])
    
    return 0 if result['status'] == 'success' else 1

if __name__ == '__main__':
    sys.exit(main())

