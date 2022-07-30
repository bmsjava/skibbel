#!/usr/bin/python3
# -*- coding: utf-8 -*-


import requests
import re
import socket
from typing import List
from multiprocessing import Pool

from color_log import color_log, yellow, green

color_log(f'Запущен поиск прокси ...', yellow)
r = requests.get(f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=2000&country=all&ssl=all&anonymity=elite,anonymous')
proxy_list = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
all_proxy = ['socks5://' + i for i in proxy_list]
r = requests.get(f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=2000&country=all&ssl=all&anonymity=elite,anonymous')
proxy_list = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
[all_proxy.append('socks4://' + i) for i in proxy_list]
good_proxy = []

def _get_proxy(proxy: str) -> List[str]:
    port = re.search(r':(\d+)', proxy)
    if port != '80' and port != '8080' and port != '3128' and port != '1080' and port != '8123':
        proxies = {
            'http':proxy,
            'https':proxy
        }
        try:
            requests.get('https://www.skibbel.com/', proxies = proxies, timeout = 2)
            ip = re.search(r'(\d+\.\d+\.\d+\.\d+):\d+', proxy).group(1)
            try:
                sock = socket.socket()
                sock.settimeout(0.5)
                sock.connect((ip, 80))
                sock.close()
            except:
                good_proxy.append(proxy)
            else:
                pass
        except:
            pass
        return good_proxy


def get_good_proxy() -> List[str]:
    with Pool(100) as p:
        good_proxy_list = p.map(_get_proxy, all_proxy)
    good_proxy_list = [i1 for i in good_proxy_list for i1 in i if len(i1) != 0]
    color_log(f'Найдено {len(good_proxy_list)} прокси', green)
    return good_proxy_list
