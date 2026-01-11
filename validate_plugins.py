#!/usr/bin/env python3
# Validador e Testador de Plugins qBittorrent
# Remove plugins offline, com erro de sintaxe ou que não funcionam

import os
import re
import ast
import requests
from pathlib import Path

plugins_folder = r"C:\Users\edcfa\Downloads\Plugins  QbitTorrent"

results = {
    "valid": [],
    "syntax_error": [],
    "url_error": [],
    "no_search": [],
    "offline": []
}

def check_syntax(file_path):
    """Valida sintaxe Python do arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        return False

def extract_urls(file_path):
    """Extrai URLs dos plugins"""
    urls = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Procura por URLs em strings
            url_patterns = [
                r'https?://[^\s\'"<>]+',
            ]
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    match = match.strip('\'"')
                    if match.startswith(('http://', 'https://')):
                        # Remove trailing caracteres comuns
                        match = re.sub(r'[.,;:)}\]]+$', '', match)
                        urls.add(match)
    except:
        pass
    return urls

def has_search_method(file_path):
    """Verifica se o plugin tem o método search"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return 'def search' in content and 'class' in content
    except:
        return False

def test_url_fast(url, timeout=3):
    """Teste rápido de URL"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 500
    except:
        return False

def validate_plugin(file_path):
    """Valida um plugin qBittorrent"""
    file_name = os.path.basename(file_path)
    
    # 1. Verificar sintaxe Python
    if not check_syntax(file_path):
        return "syntax_error", "Erro de sintaxe Python"
    
    # 2. Verificar se tem método search
    if not has_search_method(file_path):
        return "no_search", "Faltam componentes obrigatórios"
    
    # 3. Extrair e testar URLs
    urls = extract_urls(file_path)
    if urls:
        online_count = 0
        for url in urls:
            if test_url_fast(url):
                online_count += 1
                break
        
        if online_count == 0:
            return "offline", "Todos os servidores offline"
    
    return "valid", "OK"

# Processar plugins
py_files = sorted([f for f in Path(plugins_folder).glob("*.py") if f.name != "helpers.py"])
total = len(py_files)

print(f"\n{'='*70}")
print(f"VALIDANDO {total} PLUGINS QBITTORRENT")
print(f"{'='*70}\n")

for idx, py_file in enumerate(py_files, 1):
    file_name = py_file.name
    status, msg = validate_plugin(str(py_file))
    
    status_symbol = {
        "valid": "✓",
        "syntax_error": "✗",
        "url_error": "⚠",
        "no_search": "⚠",
        "offline": "✗"
    }.get(status, "?")
    
    print(f"[{idx:2d}/{total}] {status_symbol} {file_name:35s} - {msg}")
    results[status].append(file_name)

# Resumo
print(f"\n{'='*70}")
print("RESUMO")
print(f"{'='*70}")
print(f"✓ Válidos e online:        {len(results['valid']):3d}")
print(f"✗ Erro de sintaxe:         {len(results['syntax_error']):3d}")
print(f"✗ Offline:                 {len(results['offline']):3d}")
print(f"⚠ Sem método search:       {len(results['no_search']):3d}")
print(f"⚠ Erro em URL:             {len(results['url_error']):3d}")

# Remover plugins ruins
to_remove = results['syntax_error'] + results['offline'] + results['no_search']

if to_remove:
    print(f"\n{'='*70}")
    print(f"REMOVENDO {len(to_remove)} PLUGINS COM PROBLEMAS")
    print(f"{'='*70}\n")
    
    for file in to_remove:
        file_path = os.path.join(plugins_folder, file)
        try:
            os.remove(file_path)
            print(f"  🗑️  Removido: {file}")
        except Exception as e:
            print(f"  ✗ Erro: {file} - {e}")

# Salvar lista dos válidos
print(f"\n{'='*70}")
print("SALVANDO LISTA DOS PLUGINS VÁLIDOS")
print(f"{'='*70}\n")

valid_list_path = r"C:\Users\edcfa\Downloads\Plugins  QbitTorrent\VALID_PLUGINS.txt"
with open(valid_list_path, 'w', encoding='utf-8') as f:
    f.write(f"PLUGINS VÁLIDOS - {len(results['valid'])} arquivos\n")
    f.write("="*70 + "\n\n")
    for plugin in sorted(results['valid']):
        f.write(f"  ✓ {plugin}\n")
    f.write("\n" + "="*70 + "\n")
    f.write(f"\nObs: Estes plugins foram validados e estão online.\n")
    f.write(f"Removidos: {len(to_remove)} plugins com problemas\n")

print(f"✓ Lista salva em: {valid_list_path}")
print(f"\n{'='*70}")
print(f"PROCESSAMENTO CONCLUÍDO!")
print(f"Mantidos: {len(results['valid'])} plugins válidos")
print(f"{'='*70}\n")
