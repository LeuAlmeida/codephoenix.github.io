#!/usr/bin/env python3
"""
Script de teste para verificar a detecção de tipos de dados
"""

import sys
import os
sys.path.append('.')

from github_scan import detect_data_type, generate_search_queries

def test_data_detection():
    print("🧪 Teste de Detecção de Tipos de Dados")
    print("="*60)
    
    test_cases = [
        # Emails
        ("user@example.com", "email"),
        ("admin@company.org", "email"),
        ("test.user+tag@domain.co.uk", "email"),
        
        # URLs
        ("https://api.example.com/v1/users", "url"),
        ("http://localhost:3000/api", "url"),
        ("ftp://files.company.com/folder", "url"),
        ("api.company.com/v2/data", "url"),
        
        # GitHub Tokens
        ("ghp_1234567890abcdefghijklmnopqrstuv", "github_token"),
        ("gho_1234567890abcdefghijklmnopqrstuv", "github_token"),
        ("ghu_1234567890abcdefghijklmnopqrstuv", "github_token"),
        
        # API Keys
        ("sk-1234567890abcdefghijklmnopqrstuv", "api_key"),
        ("pk_test_1234567890abcdefghijklmnop", "api_key"),
        ("api_key_1234567890abcdefghijklmnop", "api_key"),
        ("1234567890abcdefghijklmnopqrstuvwxyz", "api_key"),
        
        # Bearer Tokens
        ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "bearer_token"),
        
        # AWS Keys
        ("AKIAIOSFODNN7EXAMPLE", "aws_key"),
        ("wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", "aws_secret"),
        
        # JWT Tokens
        ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c", "jwt_token"),
        
        # Database URLs
        ("mongodb://user:password@localhost:27017/database", "database_url"),
        ("mysql://root:password@localhost:3306/mydb", "database_url"),
        ("postgresql://user:pass@localhost/dbname", "database_url"),
        ("redis://localhost:6379/0", "database_url"),
        
        # Passwords
        ("mypassword123", "password"),
        ("secret_key_value", "password"),
        ("admin_passwd", "password"),
        
        # Generic
        ("some_random_text", "generic"),
        ("config_value", "generic"),
    ]
    
    print(f"\n📊 Testando {len(test_cases)} casos...\n")
    
    correct = 0
    total = len(test_cases)
    
    for term, expected_type in test_cases:
        detected_type = detect_data_type(term)
        status = "✅" if detected_type == expected_type else "❌"
        
        print(f"{status} {term:<50} | Esperado: {expected_type:<15} | Detectado: {detected_type}")
        
        if detected_type == expected_type:
            correct += 1
    
    accuracy = (correct / total) * 100
    print(f"\n📊 Resultado: {correct}/{total} corretos ({accuracy:.1f}% de precisão)")
    
    # Teste de geração de queries
    print("\n" + "="*60)
    print("🔍 Teste de Geração de Queries")
    print("="*60)
    
    sample_terms = [
        "user@example.com",
        "https://api.company.com",
        "ghp_1234567890abcdef",
        "AKIAIOSFODNN7EXAMPLE"
    ]
    
    for term in sample_terms:
        data_type = detect_data_type(term)
        queries = generate_search_queries(term, data_type)
        
        print(f"\n📝 Termo: {term}")
        print(f"🏷️  Tipo: {data_type}")
        print(f"🔍 Queries geradas ({len(queries)}):")
        for i, query in enumerate(queries, 1):
            print(f"   {i}. {query}")

if __name__ == "__main__":
    test_data_detection()

