import os
import sys
import configparser

info                        = configparser.RawConfigParser()
info.read('config.ini')
try:
    src                     = info['info']['src']
except KeyError:
    os.system("cls" if os.name == "nt" else "clear")
    print("Run setup.py first")
    sys.exit(1)