# 🔍 GitHub Security Scanner - Recursos Avançados

Este GitHub Scanner possui detecção inteligente de tipos de dados e estratégias de busca específicas para diferentes tipos de informações sensíveis.

## 🎯 Tipos de Dados Suportados

### 📧 **Emails**
- **Detecção**: Conteúdo com `@` e `.`
- **Estratégias de busca**:
  - Email completo com e sem aspas
  - Apenas o domínio
  - Username + domain separados
  - Padrões `mailto:` e `email:`
- **Exemplo**: `user@company.com`

### 🌐 **URLs**
- **Detecção**: Protocolos `http://`, `https://`, `ftp://` ou padrão `domain.com/path`
- **Estratégias de busca**:
  - URL completa
  - URL sem protocolo
  - Padrões `url:` e `href=`
- **Exemplo**: `https://api.company.com/v1/users`

### 🔑 **GitHub Tokens**
- **Detecção**: Prefixos `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`
- **Estratégias de busca**:
  - Token direto
  - Padrões `token:`, `key:`, `api_key:`
  - Headers de autorização
- **Exemplo**: `ghp_1234567890abcdefghijklmnopqrstuv`

### 🗝️ **API Keys**
- **Detecção**: Prefixos `sk-`, `pk_`, palavras-chave `api_key`, strings longas alfanuméricas
- **Estratégias de busca**:
  - Key direta
  - Vários padrões de nomeação
  - Headers de autorização
- **Exemplo**: `sk-1234567890abcdefghijklmnopqrstuv`

### 🎫 **Bearer Tokens**
- **Detecção**: Prefix `Bearer `
- **Estratégias de busca**:
  - Token completo
  - Padrões de autorização
- **Exemplo**: `Bearer eyJhbGciOiJIUzI1NiJ9...`

### ☁️ **AWS Credentials**

#### AWS Access Keys
- **Detecção**: Prefix `AKIA`
- **Estratégias de busca**:
  - Key direta
  - Padrões `AWS_ACCESS_KEY_ID`, `access_key`
- **Exemplo**: `AKIAIOSFODNN7EXAMPLE`

#### AWS Secret Keys
- **Detecção**: 40 caracteres alfanuméricos com `/`, `+`, `=`
- **Estratégias de busca**:
  - Secret direto
  - Padrões `AWS_SECRET_ACCESS_KEY`, `secret_key`
- **Exemplo**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

### 🎟️ **JWT Tokens**
- **Detecção**: Exatamente 2 pontos, string > 50 caracteres
- **Estratégias de busca**:
  - Token completo
  - Padrões `jwt:`, `token:`
- **Exemplo**: `eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.signature`

### 🗄️ **Database URLs**
- **Detecção**: Protocolos `mongodb://`, `mysql://`, `postgresql://`, `redis://`
- **Estratégias de busca**:
  - URL completa
  - Padrões `DATABASE_URL`, `connection_string`
- **Exemplo**: `mongodb://user:pass@localhost:27017/db`

### 🔐 **Passwords/Secrets**
- **Detecção**: Palavras-chave `password`, `passwd`, `pwd`, `secret`
- **Estratégias de busca**:
  - Valor direto
  - Vários padrões de nomeação
- **Exemplo**: `admin_password123`

### 📄 **Genérico**
- **Aplicação**: Qualquer termo que não se encaixe nos padrões acima
- **Estratégias de busca**:
  - Busca com e sem aspas

## 📊 **Estatísticas de Detecção**

- **Precisão**: 96.3% (26/27 casos de teste)
- **Tipos suportados**: 10 categorias diferentes
- **Estratégias por tipo**: 4-8 queries diferentes por categoria

## 🚀 **Como Usar**

### 1. Configuração Rápida
```bash
# Configure o arquivo .env
SEARCH_TERM=user@company.com,ghp_token,https://api.internal.com

# Execute o scanner
./run.sh
```

### 2. Exemplos Práticos

#### Buscar emails de uma empresa
```bash
SEARCH_TERM=@company.com,@internal.company.org
```

#### Buscar tokens do GitHub
```bash
SEARCH_TERM=ghp_,gho_,ghu_
```

#### Buscar credenciais AWS
```bash
SEARCH_TERM=AKIA,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY
```

#### Buscar URLs internas
```bash
SEARCH_TERM=internal.company.com,api.company.local,https://staging.company.com
```

#### Buscar strings de conexão de banco
```bash
SEARCH_TERM=mongodb://,mysql://,postgresql://,DATABASE_URL
```

### 3. Combinações Poderosas
```bash
# Auditoria de segurança completa
SEARCH_TERM=@company.com,ghp_,AKIA,mongodb://company,password123

# Busca de vazamentos de API
SEARCH_TERM=sk-,pk_,api_key,Bearer,Authorization

# URLs e endpoints sensíveis
SEARCH_TERM=api.company.com,internal.company.com,staging.company.com
```

## ⚡ **Recursos Avançados**

### 🔄 **Reload Automático**
- O arquivo `.env` é recarregado a cada execução
- Modifique configurações sem reiniciar

### 📊 **Rate Limiting Inteligente**
- Detecta limites da API do GitHub
- Pausa automática quando necessário
- Mostra informações de limite restante

### 🔍 **Debug Detalhado**
- Mostra tipo de dado detectado
- Lista todas as queries tentadas
- Informações de status detalhadas

### 💯 **Múltiplas Estratégias**
- Tenta diferentes abordagens para cada tipo
- Para na primeira que encontra resultados
- Maximiza chances de encontrar dados sensíveis

## 🛡️ **Boas Práticas de Segurança**

1. **Nunca comite o arquivo `.env`** - Está no `.gitignore`
2. **Use tokens com permissões mínimas** - Apenas `public_repo`
3. **Monitore rate limits** - Respeite os limites da API
4. **Documente achados** - Relate vazamentos de forma responsável
5. **Use éticamente** - Apenas em repositórios que você tem permissão

## 📝 **Exemplos de Saída**

```
🔍 Tipo detectado: EMAIL
🔍 Tentativa 1/6 - Query: "user@company.com" in:file
🌐 URL: https://api.github.com/search/code?q=%22user%40company.com%22...
📊 Status: 200
📈 Total encontrado: 42, Retornados nesta página: 30
📁 company/config - .env.example
🔗 https://github.com/company/config/blob/.../env.example
```

Este scanner é uma ferramenta poderosa para auditoria de segurança e detecção de vazamentos de dados sensíveis em repositórios GitHub. Use com responsabilidade! 🛡️

