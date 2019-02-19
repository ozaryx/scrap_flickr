import os
import re
import requests
from bs4 import BeautifulSoup as BS

URL = r'https://www.flickr.com/search/?text={}'

# search = r'mustang+gt'
print('''Введите ключевые слова для поиска изображений на Flickr.
Ключевые слова разделяются знаком '+'. Например, sunflower+carrot''')
search = input('Поиск: ')
url = URL.format(search)

proxies = {
    'http': 'http://localhost:3128',
    'https': 'http://localhost:3128',
}

print('Ищем изображения...')
resp = requests.get(url)
# resp = requests.get(url, proxies=proxies)
# try:
#     resp = requests.get(url)
# except requests.exceptions.ProxyError:
#     print('error', '')

if resp.status_code != 200:
    print('error', resp.status_code)

doc = BS(resp.text, 'html.parser')

# <div class="view photo-list-photo-view requiredToShowOnServer awake"
# style="transform: translate(551px, 359px); width: 249px; height: 166px;
# background-image: url(&quot;//c1.staticflickr.com/3/2222/2118049999_a05f4e8501.jpg&quot;);"
# id="yui_3_16_0_1_1550066883577_1181">
# </div>

foto_divs = doc.find_all(
    'div', class_='view photo-list-photo-view requiredToShowOnServer awake')

regexp = r'<.*(//.*\.jpg).*>'
regexp = re.compile(regexp)

url_list = []
for elem in foto_divs[:5]:
    matches = regexp.findall(str(elem))
    url_list += matches

print('Сохраняем изображения на диск...')
for url in url_list:
    resp = requests.get('https:{}'.format(url))
    if resp.status_code != 200:
        print('error', resp.status_code)
        continue
    img_name = url.rpartition('/')[-1]
    with open(img_name, 'wb') as f:
        print('\tСохраняем файл: {}'.format(img_name))
        f.write(resp.content)

print('Сохраненные файлы:')
for elem in os.listdir():
    if os.path.isfile(elem):
        if elem.endswith('.jpg'):
            print('\t{}'.format(elem))
