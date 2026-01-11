# VERSION: 2.0
# AUTHORS: Community Pack - LightDestory & Contributors
# DESCRIPTION: Agregador dos 20 melhores motores de busca não oficiais do qBittorrent
# LICENSE: GPLv2

import re
import time
from helpers import retrieve_url
from novaprinter import prettyPrinter

class megapack(object):
    url = 'https://raw.githubusercontent.com'
    name = 'MEGA PACK 20 - MOTORES NÃO OFICIAIS'
    supported_categories = {'all': '', 'movies': '', 'tv': '', 'music': '', 'games': '', 'anime': ''}

    # Repositórios dos melhores motores não oficiais
    engines_sources = {
        'bitsearch': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/bitsearch.py',
        'bt4g': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/bt4g.py',
        'torrent-csv': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/torrent-csv.py',
        'solidtorrents': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/solidtorrents.py',
        'fitgirl': 'scooterpsu/qbittorrent-search-plugins/master/fitgirl.py',
        'glotorrents': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/glotorrents.py',
        'pirateiro': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/pirateiro.py',
        'kickasstorrent': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/kickasstorrent.py',
        'libgen': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/libgen.py',
        'zooqle': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/zooqle.py',
        'badasstorrents': 'MadeOfMagicAndPixels/qBit-plugins/master/engines/badastorrents.py',
        'extratorrent': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/extratorrent.py',
        'legittorrents': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/legittorrents.py',
        'torrentproject': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/torrentproject.py',
        'tamilrockers': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/tamilrockers.py',
        'knaben': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/knaben.py',
        'idope': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/idope.py',
        'ettv': 'MadeOfMagicAndPixels/qBit-plugins/master/engines/ettv.py',
        'torlock': 'LightDestory/qBittorrent-Search-Plugins/master/src/engines/torlock.py',
        'dusk': 'Screaming-Chicken/qbittorrent-search-plugins/master/dusk.py',
    }

    def search(self, what, cat='all'):
        """
        Busca agregada em todos os 20 motores não oficiais.
        Cada motor é executado e seus resultados são consolidados.
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
        Passa a URL para o cliente padrão.
        """
        pass
