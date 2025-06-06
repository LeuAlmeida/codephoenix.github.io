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

# Add scanner package to path
sys.path.append(str(Path(__file__).parent.parent))

from core.github_scan import main as run_scanner

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
        
        # Executa o scanner
        run_scanner()
        
        # Restaura .env original
        if os.path.exists('.env.backup'):
            os.remove('.env')
            os.rename('.env.backup', '.env')
        
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main() 