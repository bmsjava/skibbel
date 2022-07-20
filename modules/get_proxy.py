#!/usr/bin/python3
# -*- coding: utf-8 -*-


import requests
import re
from typing import List
from multiprocessing import Pool

from color_log import color_log, yellow, green

color_log(f'Запущен поиск прокси ...', yellow)
url1 = 'https://api.pro'
r = requests.get(f'{url1}xyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=2250&country=all&simplified=true')
proxy_list = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
all_proxy = ['socks5://' + i for i in proxy_list]
r = requests.get(f'{url1}xyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=2350&country=all&simplified=true')
proxy_list = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
[all_proxy.append('socks4://' + i) for i in proxy_list]
good_proxy = []

def _get_proxy(proxy: str) -> List[str]:
    proxies = {
        'http':proxy,
        'https':proxy
    }
    try:
        r = requests.get('https://www.skibbel.com/', proxies = proxies, timeout = 2)
        good_proxy.append(proxy)
    except:
        pass
    return good_proxy


def get_good_proxy() -> List[str]:
    with Pool(100) as p:
        good_proxy_list = p.map(_get_proxy, all_proxy)
    good_proxy_list = [i1 for i in good_proxy_list for i1 in i if len(i1) != 0]
    color_log(f'Найдено {len(good_proxy_list)} прокси', green)
    return good_proxy_list
