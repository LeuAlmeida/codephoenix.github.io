#!/usr/bin/env python3
"""
Simple HTTP server para servir o frontend do CodePhoenix
"""

import http.server
import socketserver
import json
import subprocess
import os
import threading
import urllib.parse
from pathlib import Path

PORT = 8080
FRONTEND_DIR = Path(__file__).parent / 'frontend'

# Global variables to store scan state
scan_results = []
scan_status = {'status': 'idle', 'message': ''}
current_scan_process = None

class CodePhoenixHandler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/results':
            self.handle_results_request()
        elif self.path == '/api/status':
            self.handle_status_request()
        else:
            # Serve static files
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests para API calls"""
        if self.path == '/api/scan':
            self.handle_scan_request()
        else:
            self.send_error(404, "API endpoint not found")
    
    def handle_scan_request(self):
        """Handle scan requests do frontend"""
        try:
            # Lê o body da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            config = json.loads(post_data.decode('utf-8'))
            
            # Validação básica
            if not config.get('githubToken') or not config.get('searchTerms'):
                self.send_json_response({'error': 'Token ou termos de busca ausentes'}, 400)
                return
            
            # Prepara configuração para o bridge script
            bridge_config = {
                'GITHUB_TOKEN': config['githubToken'],
                'SEARCH_TERM': config['searchTerms'],
                'RESULTS_PER_PAGE': str(config.get('resultsPerPage', 30)),
                'PAGES': str(config.get('pages', 5)),
                'SLEEP_TIME': str(config.get('sleepTime', 2)),
                'START_DATE': config.get('startDate'),
                'END_DATE': config.get('endDate')
            }
            
            # Remove valores None
            bridge_config = {k: v for k, v in bridge_config.items() if v is not None}
            
            # Executa o scanner em thread separada
            def run_scanner():
                try:
                    # Chama o bridge script
                    result = subprocess.run([
                        'python3', 'frontend_bridge.py', 
                        json.dumps(bridge_config)
                    ], capture_output=True, text=True, cwd=Path(__file__).parent)
                    
                    if result.returncode == 0:
                        print("Scanner executado com sucesso")
                    else:
                        print(f"Erro no scanner: {result.stderr}")
                        
                except Exception as e:
                    print(f"Erro executando scanner: {e}")
            
            # Inicia scanner em background
            scanner_thread = threading.Thread(target=run_scanner)
            scanner_thread.daemon = True
            scanner_thread.start()
            
            # Resposta imediata
            self.send_json_response({
                'status': 'started',
                'message': 'Scanner iniciado com sucesso'
            })
            
        except json.JSONDecodeError:
            self.send_json_response({'error': 'JSON inválido'}, 400)
        except Exception as e:
            self.send_json_response({'error': f'Erro interno: {str(e)}'}, 500)
    
    def handle_results_request(self):
        """Handle requests para resultados do scan"""
        global scan_results, scan_status
        
        try:
            # Simula resultados para demonstração
            # Na implementação real, isso viria do arquivo de resultados
            if scan_status['status'] == 'completed':
                self.send_json_response({
                    'status': 'completed',
                    'results': scan_results
                })
            else:
                self.send_json_response({
                    'status': 'running',
                    'message': 'Scanner em execução...'
                })
        except Exception as e:
            self.send_json_response({'error': f'Erro ao obter resultados: {str(e)}'}, 500)
    
    def handle_status_request(self):
        """Handle requests para status do scan"""
        global scan_status
        
        try:
            self.send_json_response(scan_status)
        except Exception as e:
            self.send_json_response({'error': f'Erro ao obter status: {str(e)}'}, 500)
    
    def send_json_response(self, data, status=200):
        """Envia resposta JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    """Inicia o servidor"""
    
    # Verifica se o diretório frontend existe
    if not FRONTEND_DIR.exists():
        print(f"Erro: Diretório frontend não encontrado em {FRONTEND_DIR}")
        return
    
    # Cria o servidor
    with socketserver.TCPServer(("", PORT), CodePhoenixHandler) as httpd:
        print(f"🚀 CodePhoenix Server iniciado!")
        print(f"🌐 Frontend disponível em: http://localhost:{PORT}")
        print(f"📁 Servindo arquivos de: {FRONTEND_DIR}")
        print(f"📊 API endpoint: http://localhost:{PORT}/api/scan")
        print(f"\n⏹️  Pressione Ctrl+C para parar o servidor")
        print("="*50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛱 Servidor interrompido pelo usuário")
            print("👋 Obrigado por usar o CodePhoenix!")

if __name__ == "__main__":
    main()

