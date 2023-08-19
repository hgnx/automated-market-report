import os
import sys
import configparser

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Setup Wizard")

banner()

config_file                 = 'config.ini'  
info                        = configparser.RawConfigParser()
info.add_section('api')
info.add_section('info')

xfred                       = input("[+] Enter FRED API Key : ")
info.set('api', 'fred', xfred)
info.set('info', 'src', 'https://github.com/hgnx/automated-market-report')

with open(config_file, 'w') as setup:
    info.write(setup)

print("[+] Setup completed successfully")