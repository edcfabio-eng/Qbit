#!/usr/bin/env python3
# Testador de arquivos Lua ROM - Remove os que estão offline

import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse

# Caminho dos arquivos
rom_folder = r"c:\Users\edcfa\Downloads\Compressed\3489700"

# Lista para armazenar resultados
results = {"online": [], "offline": []}

def extract_urls_from_lua(file_path):
    """Extrai URLs dos arquivos Lua"""
    urls = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Procura por padrões de URL
            url_patterns = [
                r'https?://[^\s\'"<>]+',
                r'"https?://[^"]+',
                r"'https?://[^']+",
            ]
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    match = match.strip('\'"')
                    if match.startswith(('http://', 'https://')):
                        urls.add(match)
    except Exception as e:
        pass
    return urls

def test_url(url, timeout=5):
    """Testa se uma URL está respondendo"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except:
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            return response.status_code < 400
        except:
            return False

def test_lua_file(file_path):
    """Testa um arquivo Lua extraindo e testando suas URLs"""
    urls = extract_urls_from_lua(file_path)
    
    if not urls:
        # Se não encontrar URLs, assume que está ok (pode ser um arquivo de dados)
        return True
    
    # Testa cada URL
    for url in urls:
        if test_url(url):
            return True
    
    return False

# Processar todos os arquivos Lua
lua_files = sorted(Path(rom_folder).glob("*.lua"))
total = len(lua_files)

print(f"Testando {total} arquivos Lua...\n")

for idx, lua_file in enumerate(lua_files, 1):
    file_name = lua_file.name
    print(f"[{idx}/{total}] Testando {file_name}...", end=" ", flush=True)
    
    if test_lua_file(str(lua_file)):
        print("✓ ONLINE")
        results["online"].append(file_name)
    else:
        print("✗ OFFLINE")
        results["offline"].append(file_name)

# Exibir resumo
print("\n" + "="*60)
print(f"RESUMO DOS TESTES")
print("="*60)
print(f"Total de arquivos: {total}")
print(f"Online: {len(results['online'])}")
print(f"Offline: {len(results['offline'])}")

if results["offline"]:
    print(f"\n📋 Arquivos OFFLINE que serão removidos:")
    for file in sorted(results["offline"]):
        print(f"  - {file}")
    
    # Remover arquivos offline
    print("\n🗑️  Removendo arquivos offline...")
    for file in results["offline"]:
        file_path = os.path.join(rom_folder, file)
        try:
            os.remove(file_path)
            print(f"  ✓ Removido: {file}")
        except Exception as e:
            print(f"  ✗ Erro ao remover {file}: {e}")

print("\n" + "="*60)
print("Processo concluído!")
print(f"Mantidos: {len(results['online'])} arquivos online")
print("="*60)
