#!/usr/bin/env python3
"""
Bridge script para conectar o frontend ao scanner Python
"""

import json
import sys
import os
import tempfile
from pathlib import Path

# Adiciona o diretório pai ao path para importar o scanner
sys.path.append(str(Path(__file__).parent))

from github_scan import main as run_scanner, reload_env_config

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

def run_scan_with_config(config_data):
    """Executa o scanner com a configuração fornecida"""
    try:
        # Parse da configuração JSON
        config = json.loads(config_data)
        
        # Validação básica
        required_fields = ['GITHUB_TOKEN', 'SEARCH_TERM']
        for field in required_fields:
            if not config.get(field):
                return {'error': f'Campo obrigatório ausente: {field}'}
        
        # Cria .env temporário
        temp_env_path = create_temp_env(config)
        
        try:
            # Backup do .env original se existir
            original_env = '.env'
            backup_env = None
            
            if os.path.exists(original_env):
                backup_env = original_env + '.backup'
                os.rename(original_env, backup_env)
            
            # Copia o .env temporário
            os.rename(temp_env_path, original_env)
            
            # Executa o scanner
            print(json.dumps({'status': 'starting', 'message': 'Iniciando scanner...'}))
            run_scanner()
            
            return {'status': 'completed', 'message': 'Scanner concluído com sucesso'}
            
        finally:
            # Restaura o .env original
            if os.path.exists(original_env):
                os.remove(original_env)
            
            if backup_env and os.path.exists(backup_env):
                os.rename(backup_env, original_env)
            
            # Remove arquivo temporário se ainda existir
            if os.path.exists(temp_env_path):
                os.remove(temp_env_path)
    
    except json.JSONDecodeError:
        return {'error': 'Configuração JSON inválida'}
    except Exception as e:
        return {'error': f'Erro durante o scanner: {str(e)}'}

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Configuração não fornecida'}))
        sys.exit(1)
    
    config_data = sys.argv[1]
    result = run_scan_with_config(config_data)
    
    print(json.dumps(result))

if __name__ == '__main__':
    main()

