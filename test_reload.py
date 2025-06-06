#!/usr/bin/env python3
"""
Script de teste para verificar se o reload do .env está funcionando
"""

import os
import time
from dotenv import load_dotenv

def test_reload():
    print("🧪 Teste de reload do arquivo .env")
    print("="*50)
    
    print("\n1️Primeira leitura:")
    load_dotenv(dotenv_path='.env', override=True, verbose=True)
    search_term_1 = os.getenv('SEARCH_TERM', 'Não definido')
    print(f"   SEARCH_TERM: {search_term_1}")
    
    print("\nAgora modifique o arquivo .env e pressione Enter para continuar...")
    input("   (Exemplo: mude SEARCH_TERM para outro valor)")
    
    print("\nSegunda leitura (com reload forçado):")
    load_dotenv(dotenv_path='.env', override=True, verbose=False)
    search_term_2 = os.getenv('SEARCH_TERM', 'Não definido')
    print(f"   SEARCH_TERM: {search_term_2}")
    
    print("\nResultado:")
    if search_term_1 != search_term_2:
        print("   SUCESSO: O arquivo .env foi recarregado corretamente!")
        print(f"  Valor anterior: {search_term_1}")
        print(f"  Valor atual: {search_term_2}")
    else:
        print("   Os valores são iguais (pode não ter sido modificado)")
        print(f"  Valor: {search_term_1}")

if __name__ == "__main__":
    test_reload()

