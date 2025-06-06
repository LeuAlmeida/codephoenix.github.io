#!/usr/bin/env python3
"""
Bridge script para conectar o frontend ao scanner Python
"""

import json
import sys
import os
import tempfile
from pathlib import Path

# Add scanner package to path
sys.path.append(str(Path(__file__).parent.parent))

from core.github_scan import main as run_scanner, reload_env_config

def create_temp_env(config):
    """Cria um arquivo .env temporário com a configuração do frontend"""
    env_content = f"""# Configuração gerada pelo frontend
GITHUB_TOKEN={config['GITHUB_TOKEN']}
SEARCH_TERM={config['SEARCH_TERM']}
RESULTS_PER_PAGE={config['RESULTS_PER_PAGE']}
PAGES={config['PAGES']}
SLEEP_TIME={config['SLEEP_TIME']}
"""
    
    if config.get('START_DATE'):
        env_content += f"START_DATE={config['START_DATE']}\n"
    if config.get('END_DATE'):
        env_content += f"END_DATE={config['END_DATE']}\n"
    
    # Cria arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False)
    temp_file.write(env_content)
    temp_file.close()
    
    return temp_file.name

def main():
    """Executa o scanner com dados do frontend"""
    
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Configuração não fornecida'}))
        sys.exit(1)
    
    try:
        # Parse da configuração
        config = json.loads(sys.argv[1])
        
        # Cria arquivo .env temporário
        env_file = create_temp_env(config)
        
        # Backup do .env original
        if os.path.exists('.env'):
            os.rename('.env', '.env.backup')
        
        # Usa configuração temporária
        os.rename(env_file, '.env')
        
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