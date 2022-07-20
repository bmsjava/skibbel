#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime


# ------------------------ Задаём цвета для лога ----------------------- #
purple = '\033[95m'  
green = '\033[32m'
red = '\033[31m'
yellow = '\033[33m'
normal = '\033[0m'
# ---------------------------------------------------------------------- #


# ------------------- Цветной лог с датой и временем ------------------- #
def color_log(text: str, color: str) -> str:
    d = datetime.now()
    color_text = '{}[%Y-%m-%d %H:%M:%S] - {} {}'.format(color, str(text), normal)
    return print(d.strftime(color_text))
# ---------------------------------------------------------------------- #