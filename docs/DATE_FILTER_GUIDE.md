# 📅 Guia de Filtros de Data - GitHub Scanner

Este guia explica como os filtros de data funcionam no GitHub Scanner e como resolver problemas comuns.

## 🤔 **Como Funcionam os Filtros de Data**

### 📈 **Tipos de Filtros**

O GitHub Scanner usa filtros de data baseados na **atividade do repositório**, não na data dos arquivos:

1. **`pushed:YYYY-MM-DD..YYYY-MM-DD`** - Data do último push (recomendado)
2. **`created:YYYY-MM-DD..YYYY-MM-DD`** - Data de criação do repositório

### 🧠 **Fallback Inteligente**

O scanner possui um sistema inteligente que:

1. 🗾 **Testa o filtro**: Verifica se o filtro retorna resultados
2. ⚠️ **Detecta restrição**: Se retorna 0 resultados, o filtro é muito restritivo
3. 🔄 **Remove automaticamente**: Busca sem filtro para melhor cobertura
4. 📝 **Informa o usuário**: Mostra mensagem explicativa

## 📅 **Configuração de Datas**

### ✅ **Recomendações por Tipo de Busca**

#### 📧 **Emails Corporativos**
```bash
# Muitos emails corporativos estão em repos antigos
# Recomendação: SEM filtro ou range amplo
START_DATE=2008-01-01  # Início do GitHub
END_DATE=2024-12-31
```

#### 🔑 **Tokens/Credenciais**
```bash
# Tokens geralmente estão em projetos mais recentes
START_DATE=2020-01-01
END_DATE=2024-12-31
```

#### 🌐 **URLs/APIs**
```bash
# APIs modernas geralmente em projetos recentes
START_DATE=2018-01-01
END_DATE=2024-12-31
```

### 📊 **Exemplos Práticos**

#### Sem Restrição (Recomendado para emails)
```bash
# Comente ou remova as linhas de data
# START_DATE=
# END_DATE=
SEARCH_TERM=@company.com
```

#### Repositórios Ativos Recentemente
```bash
START_DATE=2020-01-01
END_DATE=2024-12-31
SEARCH_TERM=ghp_,sk-,AKIA
```

#### Range Conservador
```bash
START_DATE=2015-01-01
END_DATE=2024-12-31
SEARCH_TERM=api.company.com
```

## 🚑 **Solução de Problemas**

### ❌ **Problema: "0 resultados com filtro de data"**

**Causas comuns:**
- Data muito restritiva (ex: 2020+ para emails antigos)
- Termo de busca em repositórios muito antigos
- Filtro `created:` muito rígido

**Soluções:**
1. **Automática**: O scanner remove o filtro automaticamente
2. **Manual**: Comente as linhas START_DATE/END_DATE no .env
3. **Expandir range**: Use datas mais antigas (ex: 2008-01-01)

### ✅ **Problema: "Muitos resultados irrelevantes"**

**Solução:**
```bash
# Use filtro mais restritivo
START_DATE=2022-01-01  # Apenas repos muito recentes
END_DATE=2024-12-31
```

### 🔄 **Problema: "Fallback sempre ativa"**

**Solução:**
```bash
# Teste diferentes ranges:
# Muito restritivo:
START_DATE=2023-01-01

# Moderado:
START_DATE=2020-01-01

# Conservador:
START_DATE=2015-01-01

# Amplo:
START_DATE=2008-01-01
```

## 📊 **Estatísticas Práticas**

### 📈 **Dados Reais (exemplo @google.com)**

- **Sem filtro**: 125 resultados
- **pushed:2020+**: 0 resultados (🔄 fallback ativo)
- **pushed:2015+**: 0 resultados (🔄 fallback ativo)
- **pushed:2010+**: 0 resultados (🔄 fallback ativo)

**Conclusão**: Emails acadêmicos geralmente estão em repositórios mais antigos.

### 📉 **Dicas de Performance**

1. **Comece sem filtro** - Veja a distribuição temporal
2. **Use filtros progressivos** - Teste ranges diferentes
3. **Monitore o fallback** - Se sempre ativa, expanda o range
4. **Combine com outros filtros** - Use palavras-chave específicas

## 🎯 **Melhores Práticas**

### ✅ **Do's**
- Use o fallback inteligente (ativado por padrão)
- Teste diferentes ranges para seu caso
- Monitore mensagens de fallback
- Documente ranges que funcionam

### ❌ **Don'ts**
- Não use ranges muito restritivos (ex: apenas 2024)
- Não ignore mensagens de fallback
- Não assuma que "recente = melhor"
- Não use filtros para dados históricos

## 🚀 **Exemplos de Sucesso**

### 🏢 **Auditoria Corporativa**
```bash
# Emails corporativos (sem filtro)
SEARCH_TERM=@company.com,@corp.company.com
# START_DATE=  # Comentado - busca completa
# END_DATE=
```

### 🔒 **Credenciais Recentes**
```bash
# Tokens modernos (com filtro)
SEARCH_TERM=ghp_,sk-,Bearer
START_DATE=2020-01-01
END_DATE=2024-12-31
```

### 🌐 **URLs Internas**
```bash
# APIs e URLs (filtro moderado)
SEARCH_TERM=internal.company.com,api.company.com
START_DATE=2018-01-01
END_DATE=2024-12-31
```

---

## 📝 **Resumo**

O sistema de filtros de data do GitHub Scanner é **inteligente e adaptativo**:

- ⚙️ **Testa automaticamente** se o filtro é válido
- 🔄 **Faz fallback** quando muito restritivo
- 📝 **Informa o usuário** sobre a decisão tomada
- 💯 **Maximiza resultados** sem sacrificar funcionalidade

**Use este guia para otimizar suas buscas e entender o comportamento do scanner!**

