# 🌐 CodePhoenix Frontend

Interface web para o GitHub Security Scanner com detecção inteligente de tipos de dados.

## 🚀 **Como Executar**

### Método 1: Script Automático (Recomendado)
```bash
# No diretório do projeto
./run_frontend.sh
```

### Método 2: Manual
```bash
# Ative o ambiente virtual
source venv/bin/activate

# Instale dependências (se necessário)
pip install -r requirements.txt

# Inicie o servidor
python server.py
```

### Método 3: Teste Rápido (Simulação)
```bash
# Abra diretamente o arquivo HTML
open frontend/index.html
# ou
cd frontend && python -m http.server 8080
```

## 🌐 **Acesso**

Depois de iniciar o servidor:
- **Frontend**: http://localhost:8080
- **API**: http://localhost:8080/api/scan

## 📝 **Como Usar**

### 1. **Configurar Token**
- Acesse: https://github.com/settings/tokens
- Crie um token com permissão `public_repo`
- Cole no campo "GitHub Token"

### 2. **Definir Termos de Busca**
```
@google.com,github.com
```

### 3. **Configurar Opções Avançadas** (Opcional)
- Resultados por página: 30
- Páginas: 5
- Intervalo: 2 segundos
- Filtros de data (opcional)

### 4. **Executar Scanner**
- Clique em "Iniciar Scanner"
- Acompanhe o progresso na barra
- Resultados aparecerão automaticamente

## 🛠️ **Recursos do Frontend**

### 🎯 **Detecção Inteligente**
- **📧 Emails**: `user@company.com`
- **🌐 URLs**: `https://api.company.com`
- **🔑 Tokens**: `ghp_abc123...`
- **🗝️ API Keys**: `sk-abc123...`
- **☁️ AWS**: `AKIA...`
- **🗄️ Database**: `mongodb://...`

### 📊 **Interface**
- Design responsivo com TailwindCSS
- Tema escuro estilo GitHub
- Validação em tempo real
- Barra de progresso
- Resultados organizados por tipo

### ⚙️ **Funcionalidades**
- **Configuração persistente**: Salva preferências no localStorage
- **Validação de token**: Verifica formato do GitHub token
- **Progresso em tempo real**: Mostra status da execução
- **Resultados estruturados**: Agrupa por termo de busca
- **Links diretos**: Acesso rápido aos repositórios encontrados

## 🔄 **Como Funciona**

### Fluxo de Dados
1. **Frontend** coleta configurações do usuário
2. **Envia** via POST para `/api/scan`
3. **Servidor** cria .env temporário
4. **Executa** `github_scan.py` em background
5. **Frontend** faz polling em `/api/results`
6. **Exibe** resultados formatados

### Arquitetura
```
Frontend (HTML/CSS/JS)
       ↓
Server.py (HTTP Server)
       ↓
simple_scanner.py (Bridge)
       ↓
github_scan.py (Scanner)
       ↓
GitHub API
```

## 🔧 **Desenvolvimento**

### Estrutura de Arquivos
```
frontend/
├── index.html          # Interface principal
└── app.js              # Lógica JavaScript

server.py                 # Servidor HTTP
simple_scanner.py         # Bridge frontend-backend
run_frontend.sh           # Script de inicialização
```

### Personalização
- **Cores**: Editue `tailwind.config` em `index.html`
- **API**: Modifique endpoints em `server.py`
- **UI**: Ajuste componentes em `index.html`
- **Lógica**: Altere comportamento em `app.js`

## 🐛 **Troubleshooting**

### Problema: "Erro na comunicação com o servidor"
**Solução**: Verifique se o servidor está rodando:
```bash
# Verificar se a porta 8080 está livre
lsof -i :8080

# Reiniciar servidor
./run_frontend.sh
```

### Problema: "Token inválido"
**Solução**: 
- Verifique se o token começa com `ghp_`
- Confirme permissões no GitHub
- Teste o token no terminal primeiro

### Problema: "Nenhum resultado encontrado"
**Solução**:
- Teste os mesmos termos no `github_scan.py` direto
- Verifique se não é um problema de rate limiting
- Tente termos mais comuns (ex: `@gmail.com`)

### Problema: "Frontend não conecta com Python"
**Solução**: Use modo simulação:
```bash
# Abrir apenas o HTML (modo demo)
open frontend/index.html
```

## 🚀 **Modo de Produção**

Para usar em produção, considere:

1. **Servidor WSGI**: Use Gunicorn ou uWSGI
2. **Proxy Reverso**: Nginx na frente
3. **HTTPS**: Certificados SSL
4. **Autenticação**: Sistema de login
5. **Rate Limiting**: Controle de uso

```bash
# Exemplo com Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8080 server:app
```

## 💫 **Próximos Passos**

- [ ] WebSocket para resultados em tempo real
- [ ] Exportação de resultados (CSV, JSON)
- [ ] Histórico de scans
- [ ] Dashboard com métricas
- [ ] Integração com outras APIs (GitLab, Bitbucket)
- [ ] Sistema de alertas
- [ ] API REST completa

---

**CodePhoenix Frontend** - Interface moderna para segurança em repositórios 🛡️

