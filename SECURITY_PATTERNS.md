# 🔒 Padrões de Segurança Comuns - Guia Rápido

Este guia contém padrões comuns de busca para diferentes tipos de auditoria de segurança.

## 🏢 **Auditoria Corporativa**

### Emails Corporativos
```bash
SEARCH_TERM=@company.com,@corp.company.com,@internal.company.com
```

### URLs Internas
```bash
SEARCH_TERM=internal.company.com,api.company.local,staging.company.com,dev.company.com
```

### Credenciais de Desenvolvimento
```bash
SEARCH_TERM=company_api_key,company_secret,dev_password,staging_token
```

## 🔑 **Tokens e Chaves de API**

### GitHub Tokens
```bash
SEARCH_TERM=ghp_,gho_,ghu_,ghs_,ghr_
```

### Principais Provedores de API
```bash
# OpenAI
SEARCH_TERM=sk-,openai_api_key,OPENAI_API_KEY

# Stripe
SEARCH_TERM=pk_,sk_live,sk_test,stripe_key

# AWS
SEARCH_TERM=AKIA,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

# Google Cloud
SEARCH_TERM=AIza,google_api_key,GOOGLE_APPLICATION_CREDENTIALS

# Firebase
SEARCH_TERM=firebase_api_key,FIREBASE_CONFIG
```

## 🗄️ **Banco de Dados**

### Strings de Conexão
```bash
SEARCH_TERM=mongodb://,mysql://,postgresql://,redis://,DATABASE_URL
```

### Credenciais de Banco
```bash
SEARCH_TERM=db_password,database_password,DB_PASS,mysql_password
```

## 📱 **Configurações de Aplicação**

### Secrets Comuns
```bash
SEARCH_TERM=SECRET_KEY,JWT_SECRET,APP_SECRET,ENCRYPTION_KEY
```

### Senhas de Admin
```bash
SEARCH_TERM=admin_password,root_password,default_password,password123
```

## 🌐 **APIs e Webhooks**

### Tokens de Webhook
```bash
SEARCH_TERM=webhook_secret,WEBHOOK_TOKEN,webhook_url
```

### APIs de Terceiros
```bash
# Slack
SEARCH_TERM=xoxb-,xoxp-,slack_token,SLACK_BOT_TOKEN

# Discord
SEARCH_TERM=discord_token,DISCORD_BOT_TOKEN

# Telegram
SEARCH_TERM=telegram_bot_token,TELEGRAM_TOKEN
```

## ☁️ **Cloud Providers**

### Microsoft Azure
```bash
SEARCH_TERM=azure_client_secret,AZURE_CLIENT_ID,azure_tenant_id
```

### Google Cloud Platform
```bash
SEARCH_TERM=gcp_service_account,google_cloud_key,GCP_PROJECT_ID
```

### DigitalOcean
```bash
SEARCH_TERM=digitalocean_token,DO_TOKEN,digitalocean_api_key
```

## 🛠️ **Ferramentas de Desenvolvimento**

### Docker e Containers
```bash
SEARCH_TERM=docker_password,DOCKER_TOKEN,registry_password
```

### CI/CD
```bash
SEARCH_TERM=TRAVIS_TOKEN,CIRCLE_TOKEN,jenkins_password,gitlab_token
```

## 💳 **Processamento de Pagamentos**

### PayPal
```bash
SEARCH_TERM=paypal_client_secret,PAYPAL_CLIENT_ID,paypal_api_key
```

### Square
```bash
SEARCH_TERM=square_access_token,SQUARE_APPLICATION_ID
```

## 🗺️ **Mapas e Localização**

### Google Maps
```bash
SEARCH_TERM=google_maps_key,GOOGLE_MAPS_API_KEY,maps_api_key
```

### Mapbox
```bash
SEARCH_TERM=mapbox_token,MAPBOX_ACCESS_TOKEN,mapbox_api_key
```

## 📊 **Analytics e Monitoramento**

### Google Analytics
```bash
SEARCH_TERM=google_analytics,GA_TRACKING_ID,analytics_key
```

### Sentry
```bash
SEARCH_TERM=sentry_dsn,SENTRY_DSN,sentry_auth_token
```

## 🚑 **Exemplos de Uso Prático**

### Auditoria Completa de uma Empresa
```bash
# Configure no .env
SEARCH_TERM=@company.com,company_api,company.internal,AKIA,sk-,password123
PAGES=10
SLEEP_TIME=3
```

### Busca Específica por Tokens
```bash
SEARCH_TERM=ghp_,sk-,AKIA,Bearer,jwt
PAGES=5
SLEEP_TIME=2
```

### Scan de URLs Sensíveis
```bash
SEARCH_TERM=internal.,staging.,dev.,localhost:,127.0.0.1
PAGES=3
SLEEP_TIME=2
```

## ⚠️ **Importante**

1. **Use apenas em repositórios que você tem permissão**
2. **Reporte vazamentos de forma responsável**
3. **Respeite os rate limits da API do GitHub**
4. **Nunca abuse destas informações**
5. **Mantenha seu token do GitHub seguro**

## 🛡️ **Dicas de Segurança**

- Comece com termos mais específicos (menos resultados, mais precisos)
- Use combinações de domínios + palavras-chave relacionadas
- Monitore repositórios da sua organização regularmente
- Configure alertas para detecção contínua
- Documente e remedie vazamentos encontrados

