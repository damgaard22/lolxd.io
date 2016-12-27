# -*- coding: utf-8 -*-
"""
    lolxd.riot
    ~~~~~~~~~~

    This module contacts the official League of Legends API.

    :copyright: (c) 2016 by Mads Damgaard and Carl Bordum Hansen.
    :license: MIT, see LICENSE for more details.
"""
from functools import lru_cache
import requests
import config


API_KEY = config.RIOT_API_KEY

platforms = {
    'br': 'BR1',
    'eune': 'EUN1',
    'euw': 'EUW1',
    'kr': 'KR',
    'lan': 'LA1',
    'las': 'LA2',
    'na': 'NA1',
    'oce': 'OC1',
    'ru': 'RU',
    'tr': 'TR1',
    'jp': 'JP1'
}


def base_request(query, proxy, **kwargs):
    """Make a request to the Riot API.

    :rtype: dict
    """
    params = {'api_key': API_KEY}
    for key, value in kwargs.items():
        params[key] = value
    url = f'https://{proxy}.api.pvp.net/{query}'
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


def api_request(region, version, query):
    """Make a request to the RIOT API at the URL '/api/lol/'.

    :rtype: dict
    """
    url = f'api/lol/{region}/{version}/{query}'
    return base_request(url, region)


def observer_mode_request(region, query):
    """Make a request to the Riot API at the URL '/observer-mode/rest/'.

    :rtype: dict
    """
    url = f'observer-mode/rest/{query}'
    return base_request(url, region)


@lru_cache()
def static_request(query, version):
    """Make a request to lol-static-data.

    :rtype: dict
    """
    return base_request(f'api/lol/static-data/euw/{version}/{query}', 'global')


def get_summoner_id(region, summoner_name, version='v1.4'):
    """Return the corresponding summoner ID.

    :rtype: int
    """
    query = f'summoner/by-name/{summoner_name}'
    r = api_request(region, version, query)
    return r[summoner_name.lower()]['id']


def get_ranked_stats(region, summoner_id, version='v1.3'):
    """Return the ranked stats of summoner_name.

    :rtype: dict
    """
    query = f'stats/by-summoner/{summoner_id}/ranked'
    return api_request(region, version, query)


def get_current_game(region, summoner_id):
    """Return all available information on current game.

    :rtype: dict
    """
    platform_id = platforms[region]
    query = f'consumer/getSpectatorGameInfo/{platform_id}/{summoner_id}'
    return observer_mode_request(region, query)


def get_item_name(item_id, version='v1.2'):
    """Return the name of an item.

    :rtype: str
    """
    return static_request(f'item/{item_id}', version)['name']


def get_champion_name(champion_id, version='v1.2'):
    """Return the name of a champion.

    :rtype: str
    """
    return static_request(f'champion/{champion_id}', version)['name']


def get_summoner_spell_name(spell_id, version='v1.2'):
    """Return the name of a summoner spell.

    :rtype: str
    """
    return static_request(f'summoner-spell/{spell_id}', version)['name']
