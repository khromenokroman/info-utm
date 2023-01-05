import concurrent.futures
import threading

import requests
from bs4 import BeautifulSoup
import os
from time import sleep

def getInfoUTM(adress, find_year, find_month):

    try:
        link_key = f'http://{adress}:8080/api/info/list'
        link_adres = f'http://{adress}:8080/api/rsa'
        #print(link_adres)
        #print(link_key)
        answer_key = requests.get(link_key).text
        answer_adress = requests.get(link_adres).json()
        #print(answer_key)
        #print(answer_adress)
        soup = BeautifulSoup(answer_key,'lxml')
        block = soup.find_all('p')[0].text
        blockCR = block.split(':')
        #print(blockCR)
        fsrar_temp = blockCR[5].split('"')
        fsrar = fsrar_temp[1]

        rsa = blockCR[16][1:11]

        gost = blockCR[26][1:11]
        pars_data = gost.split('-')
        year = pars_data[0]
        month = pars_data[1]

        answer_adress = requests.get(link_adres).json()
        data = answer_adress['rows']
        #print(answer_adress)
        owner_id = 'Owner_ID'
        short_name = 'Short_Name'
        inn = 'INN'
        kpp = 'KPP'
        fact_address = 'Fact_Address'

        for i in data:
        #print(find_month)
            if i[owner_id] == fsrar and year == find_year and month == find_month:
            #if i[owner_id] == fsrar:
                print(f'Найден УТМ: {adress}')
                file = open('info_utm.txt', 'a', encoding='utf-8')
                file.write(f'\nОрганизация: {i[short_name]}\n'
                f'ИНН/КПП: {i[inn]}/{i[kpp]}\n'
                f'Адрес: {i[fact_address]}\n'
                f'Адрес(IP): {adress}\n'
                f'Сертификат: {fsrar}\n'
                f'RSA: {rsa}\n'
                f'GOST: {gost}\n')
                file.writelines('='*20)
                print(f'Организация: {i[short_name]}\n'
                f'ИНН/КПП: {i[inn]}/{i[kpp]}\n'
                f'Адрес: {i[fact_address]}\n'
                f'Адрес(IP): {adress}\n'
                f'Сертификат: {fsrar}\n'
                f'RSA: {rsa}\n'
                f'GOST: {gost}')
                print('='*20)
        file.close()
        sleep(4)
    except Exception as ex:
        pass
        #print(f'adress {adress} not found')
if __name__ == '__main__':
    try:
        os.remove('info_utm.txt')
    except:
        pass
    str_network = input('Введите сеть:')
    str_month = input('Введите месяц по которому нужно совершить отбор:')
    str_year = input('Введите год по которому нужно совершить отбор:')
    str_ip = str_network.split('.')
    adress_ip = f'{str_ip[0]}.{str_ip[1]}.{str_ip[2]}'
    #print(adress_ip)
    list_info_utm = []
    with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor:
        for i in range(2, 255):
            list_info_utm.append(executor.submit(getInfoUTM,f'{str_ip[0]}.{str_ip[1]}.{str_ip[2]}.{i}',str_year, str_month))



