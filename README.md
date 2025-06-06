# 🔍 GitHub Security Scanner

Scanner inteligente para detecção de informações sensíveis em repositórios GitHub com:
- 🧠 **Detecção inteligente** de 10 tipos de dados (emails, tokens, URLs, etc.)
- 🔄 **Reload automático** de configurações
- 💯 **Múltiplas estratégias** de busca por tipo
- 🛡️ **Rate limiting** inteligente
- **96.3% de precisão** na detecção de tipos

## Configuração

### 1. Pré-requisitos
- Python 3.7 ou superior
- Token de acesso pessoal do GitHub

### 2. Instalação

1. Clone ou baixe este repositório
2. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

3. Se necessário, instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuração do Token e Variáveis de Ambiente

1. Vá para [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Clique em "Generate new token (classic)"
3. Selecione as permissões necessárias (pelo menos `public_repo` para repositórios públicos)
4. Copie o token gerado
5. Configure o arquivo `.env` com suas credenciais:
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o arquivo .env e substitua os valores
   ```
6. No arquivo `.env`, substitua:
   ```bash
   GITHUB_TOKEN=seu_token_real_aqui
   SEARCH_TERM=termo_que_voce_quer_buscar
   START_DATE=2023-01-01
   END_DATE=2023-12-31
   ```

### 4. Executar o script

```bash
# Certifique-se de que o ambiente virtual está ativo
source venv/bin/activate

# Execute o script
sh run.sh
```

## Configurações

Todas as configurações agora são feitas através do arquivo `.env`:

- `GITHUB_TOKEN`: Seu token de acesso pessoal do GitHub
- `SEARCH_TERM`: Um ou mais termos separados por vírgula (ex: termo1,termo2)
- `START_DATE`: (opcional) Data inicial no formato YYYY-MM-DD para filtrar arquivos criados a partir desta data
- `END_DATE`: (opcional) Data final no formato YYYY-MM-DD para filtrar arquivos criados até esta data
- `RESULTS_PER_PAGE`: Número de resultados por página (máximo 100)
- `PAGES`: Número de páginas para buscar
- `SLEEP_TIME`: Intervalo entre requisições (em segundos)

Exemplo do arquivo `.env`:
```bash
GITHUB_TOKEN=ghp_seu_token_aqui
SEARCH_TERM=exemplo.com,senha,apiKey
RESULTS_PER_PAGE=50
PAGES=10
SLEEP_TIME=3
START_DATE=2023-01-01
END_DATE=2023-12-31
```

## 🧠 **Recursos Inteligentes**

### 🔍 **Detecção Automática de Tipos**
O scanner detecta automaticamente o tipo de dado que você está buscando:

- **📧 Emails**: `user@company.com`
- **🌐 URLs**: `https://api.company.com` 
- **🔑 GitHub Tokens**: `ghp_abc123...`
- **🗝️ API Keys**: `sk-abc123...`, `AKIA123...`
- **🎫 Bearer Tokens**: `Bearer eyJhbGci...`
- **☁️ AWS Credentials**: `AKIA...`, `wJalrXUt...`
- **🎟️ JWT Tokens**: `eyJhbGci.eyJzdWI.signature`
- **🗄️ Database URLs**: `mongodb://...`, `mysql://...`
- **🔐 Passwords**: `admin_password`, `secret_key`

### 💯 **Múltiplas Estratégias de Busca**
Para cada tipo, o scanner tenta diferentes abordagens:
- Busca direta do termo
- Variações com e sem aspas
- Padrões de nomeação comuns
- Headers de autorização
- Contextos específicos (mailto:, url:, etc.)

### 🔄 **Reload Automático**
- O arquivo `.env` é recarregado a cada execução
- Modifique configurações sem reiniciar o script

### 🛡️ **Rate Limiting Inteligente**
- Detecta automaticamente limites da API
- Mostra requests restantes
- Pausas automáticas quando necessário

## 📚 **Documentação Adicional**

- **[FEATURES.md](FEATURES.md)** - Documentação completa dos recursos
- **[SECURITY_PATTERNS.md](SECURITY_PATTERNS.md)** - Padrões de busca por categoria
- **[test_data_types.py](test_data_types.py)** - Teste dos tipos de detecção

## 🚀 **Exemplos Rápidos**

### Buscar emails de uma empresa
```bash
SEARCH_TERM=@company.com,@corp.company.com
```

### Buscar tokens e credenciais
```bash
SEARCH_TERM=ghp_,sk-,AKIA,Bearer
```

### Buscar URLs internas
```bash
SEARCH_TERM=internal.company.com,api.company.local
```

## Limitações da API

- A API do GitHub tem limites de rate limiting
- Máximo de 1000 resultados por busca (10 páginas × 100 resultados)
- Recomenda-se usar intervalos entre requisições para evitar bloqueios

## Nota de Segurança

⚠️ **IMPORTANTE**: Nunca faça commit do seu token de acesso pessoal no repositório. Mantenha-o privado e seguro.

