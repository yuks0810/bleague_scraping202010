import requests
from bs4 import BeautifulSoup

target_url = 'https://www.bleague.jp/schedule/?tab=1&year=2020&event=2'
r = requests.get(target_url)

soup = BeautifulSoup(r.text, 'lxml')

# for a in soup.find_all('a'):
#       print(a.get('href'))

print(soup)