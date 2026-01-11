# VERSION: 1.0
# AUTHORS: Community Pack - ROM Edition
# DESCRIPTION: Agregador dos 10 melhores motores para buscar ROMs (Switch, PS2, PS3, etc)
# LICENSE: GPLv2

import re
import time
from helpers import retrieve_url
from novaprinter import prettyPrinter

class rompack(object):
    url = 'https://raw.githubusercontent.com'
    name = 'ROM PACK 10 - CONSOLES (Switch, PS2, PS3, Wii, etc)'
    supported_categories = {'all': '', 'games': ''}

    # 10 melhores motores para ROMs e isos de consoles
    engines_sources = {
        'bitsearch': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/bitsearch.py',
        'bt4g': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/bt4g.py',
        'solidtorrents': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/solidtorrents.py',
        'zooqle': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/zooqle.py',
        'torrentproject': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/torrentproject.py',
        'torlock': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/torlock.py',
        'kickasstorrent': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/kickasstorrent.py',
        'extratorrent': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/extratorrent.py',
        'pirateiro': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/pirateiro.py',
        'glotorrents': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/glotorrents.py',
    }

    def search(self, what, cat='all'):
        """
        Busca agregada nos 10 melhores motores para ROMs e ISOs de consoles.
        Otimizado para encontrar: Nintendo Switch, PS2, PS3, PS4, Wii, Xbox, etc.
        """
        for engine_name, engine_path in self.engines_sources.items():
            try:
                # Constrói a URL do motor
                engine_url = f"https://raw.githubusercontent.com/{engine_path}"
                
                # Tenta buscar do repositório
                engine_code = retrieve_url(engine_url)
                
                if engine_code:
                    # Executa o código do motor dinamicamente
                    try:
                        local_scope = {}
                        exec(engine_code, local_scope)
                        
                        # Obtém a classe principal do motor
                        for key, obj in local_scope.items():
                            if isinstance(obj, type) and hasattr(obj, 'search'):
                                engine_instance = obj()
                                
                                # Executa a busca do motor
                                if hasattr(engine_instance, 'search'):
                                    engine_instance.search(what, cat)
                                break
                    except Exception as e:
                        # Se um motor falhar, continua com o próximo
                        continue
                        
            except Exception as e:
                # Falha silenciosa - o motor pode estar indisponível
                continue

    def download_torrent(self, info):
        """
        Método necessário para o qBittorrent processar o download.
        """
        pass
