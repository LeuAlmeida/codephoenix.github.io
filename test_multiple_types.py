#!/usr/bin/env python3
"""
Script para testar múltiplos tipos de dados em SEARCH_TERM
"""

from github_scan import detect_data_type, generate_search_queries

def test_multiple_types():
    print("🧪 Teste de Múltiplos Tipos de Dados")
    print("="*50)
    
    test_combinations = [
        "@company.com,api.company.com",
        "user@example.com,ghp_abc123456789",
        "AKIAIOSFODNN7EXAMPLE,ghp_token123,admin@company.org",
        "https://api.internal.com,mongodb://localhost:27017",
        "sk-abc123,Bearer eyJhbGci,jwt.token.here",
        "@google.com,yahoo.com.br",
        "@company.com,company.internal,ghp_,AKIA,password123"
    ]
    
    for combination in test_combinations:
        print(f"\n🔍 Testando: {combination}")
        print("-" * 40)
        
        terms = [t.strip() for t in combination.split(',')]
        
        for term in terms:
            data_type = detect_data_type(term)
            queries = generate_search_queries(term, data_type)
            
            print(f"\n  📝 {term}")
            print(f"  🏷️  Tipo: {data_type.upper()}")
            print(f"  🔍 Estratégias ({len(queries)}):")
            for i, query in enumerate(queries[:3], 1):
                print(f"     {i}. {query}")
            if len(queries) > 3:
                print(f"     ... +{len(queries)-3} estratégias adicionais")
        
        print("\n" + "="*50)

def show_benefits():
    print("\n💡 VANTAGENS de Usar Múltiplos Tipos:")
    print("\n1. 🎯 **Busca Abrangente**:")
    print("   - Cada tipo usa estratégias otimizadas")
    print("   - Maximiza chances de encontrar vazamentos")
    
    print("\n2. 🔄 **Processamento Sequencial**:")
    print("   - Processa um termo por vez")
    print("   - Respeita rate limits entre termos")
    
    print("\n3. 📊 **Relatório Organizado**:")
    print("   - Agrupa resultados por termo")
    print("   - Fácil de analisar e auditar")
    
    print("\n4. ⚡ **Inteligência Adaptativa**:")
    print("   - Detecta tipo automaticamente")
    print("   - Aplica melhores práticas para cada tipo")
    
    print("\n🚀 **Exemplos Práticos de Uso**:")
    print("\n🏢 Auditoria corporativa completa:")
    print('   SEARCH_TERM="@company.com,company.internal,company-api-key"')
    
    print("\n🔒 Caça a credenciais:")
    print('   SEARCH_TERM="ghp_,sk-,AKIA,Bearer,jwt"')
    
    print("\n🌐 URLs e endpoints:")
    print('   SEARCH_TERM="api.company.com,internal.company.com,localhost:3000"')
    
    print("\n📧 Emails e domínios:")
    print('   SEARCH_TERM="@company.com,@internal.company.com,company.local"')

if __name__ == "__main__":
    test_multiple_types()
    show_benefits()

