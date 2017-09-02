import requests
import pandas as pd
from bs4 import BeautifulSoup
resp_main = requests.get('http://www.comuni-italiani.it/cap/')
soup_resp_main = BeautifulSoup(resp_main.text, 'html.parser')
for city in soup_resp_main.select('table.tabwrap')[0].find_all('a'):
    resp_city = requests.get('http://www.comuni-italiani.it/cap/' + city['href'])
    soup_resp_city = BeautifulSoup(resp_city.text, 'html.parser')
    for village in soup_resp_city.select('table.tabwrap')[0].find_all('a'):
        print city.text + '  -->  ' + village.text
        village_url = 'http://www.comuni-italiani.it/' + village['href'].replace('../', '')
        try:
            resp_village = requests.get(village_url)
            soup_resp_village = BeautifulSoup(resp_village.text, 'html.parser')
            results = [[col.text for col in row.find_all('td')]
                       for row in soup_resp_village.select('table.tabwrap')[0].find_all('tr')]
            results_dict = [{
                'Url': village_url,
                'Region': results[1][1],
                'Province':  results[2][1],
                'Zone': results[3][1],
                'City': city.text,
                'Village': village.text,
                'Inhabitants': int(results[5][0][:results[5][0].index('(')].replace('.', '')),
                'Density': float(results[5][0][results[5][0].index('Kmq') + 5:results[5][0].index('Sup')].replace('.', '').replace(',', '.')),
                'Surface': float(results[5][0][results[5][0].index('Superficie: ') + 12:].replace('.', '').replace(',', '.').replace(' Kmq', '')),
                'Zip_Code': results[7][1],
                'Telephone_Code': results[8][1],
                'Istat_Code': results[9][1],
                'House_Code': results[10][1],
            }]
        except:
            results_dict = [{
                'Url': '/', 'Region': '/', 'Province': '/', 'Zone': '/', 'Village': '/', 'Inhabitants': '/', 'Density': '/', 'Surface': '/', 'Zip_Code': '/', 'Telephone_Code': '/', 'Istat_Code': '/', 'House_Code': '/',
            }]
        with open('Output.csv', 'a') as f:
            pd.DataFrame(results_dict).to_csv(f, header=False, index=False, encoding='utf-8')
