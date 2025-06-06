#!/usr/bin/env python3
"""
Simplified scanner que pode ser chamado pelo frontend
"""

import json
import sys
import os
import tempfile
import subprocess
from pathlib import Path

def main():
    """Executa o scanner com dados do frontend"""
    
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Configuração não fornecida'}))
        sys.exit(1)
    
    try:
        # Parse da configuração
        config = json.loads(sys.argv[1])
        
        # Cria arquivo .env temporário
        env_content = f"""GITHUB_TOKEN={config['GITHUB_TOKEN']}
SEARCH_TERM={config['SEARCH_TERM']}
RESULTS_PER_PAGE={config.get('RESULTS_PER_PAGE', '30')}
PAGES={config.get('PAGES', '5')}
SLEEP_TIME={config.get('SLEEP_TIME', '2')}
"""
        
        if config.get('START_DATE'):
            env_content += f"START_DATE={config['START_DATE']}\n"
        if config.get('END_DATE'):
            env_content += f"END_DATE={config['END_DATE']}\n"
        
        # Salva configuração temporária
        with open('.env.temp', 'w') as f:
            f.write(env_content)
        
        # Backup do .env original
        if os.path.exists('.env'):
            os.rename('.env', '.env.backup')
        
        # Usa configuração temporária
        os.rename('.env.temp', '.env')
        
        try:
            # Executa o scanner original
            result = subprocess.run([
                'python', 'github_scan.py'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(json.dumps({
                    'status': 'success',
                    'message': 'Scanner executado com sucesso',
                    'output': result.stdout
                }))
            else:
                print(json.dumps({
                    'status': 'error',
                    'message': 'Erro no scanner',
                    'error': result.stderr
                }))
                
        finally:
            # Restaura .env original
            if os.path.exists('.env'):
                os.remove('.env')
            if os.path.exists('.env.backup'):
                os.rename('.env.backup', '.env')
                
    except json.JSONDecodeError:
        print(json.dumps({'error': 'JSON inválido'}))
    except subprocess.TimeoutExpired:
        print(json.dumps({'error': 'Scanner demorou muito para executar'}))
    except Exception as e:
        print(json.dumps({'error': str(e)}))

if __name__ == '__main__':
    main()

