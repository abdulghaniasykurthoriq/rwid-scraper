import requests
from bs4 import BeautifulSoup
import json
import glob
import pandas as pd

session = requests.Session()

def login():
    print('login....')
    datas = {
        'username':'user',
        'password':'user12345'
    }

    res = session.post('http://167.172.70.208:9999/login', data=datas)

#pindahin ke get_url aja ah wkwkwkw
#    f = open('res.html', 'w+')
#    f.write(res.text)
#    f.close()

    soup = BeautifulSoup(res.text, 'html5lib')

    #udah mau ke page 1 nih cie
   # soup = BeautifulSoup(open('res.html'), 'html5lib')

    page_item = soup.find_all('li', attrs={'class': 'page-item'})
    total_pages = len(page_item) - 2
    return total_pages



def get_urls(page):
    print('getting urls.....page{}'.format(page))

    params = {
        'page':page
    }
    res = session.get('http://167.172.70.208:9999', params=params)
    soup = BeautifulSoup(res.text, 'html5lib')
    titles = soup.find_all('h4', attrs={'class':'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)
    #print(urls)
    return urls

#    f = open('res.html', 'w+')
#    f.write(res.text)
#    f.close()


def get_detail(url):
    print('getting detail..... {} '.format(url))
    res = session.get('http://167.172.70.208:9999'+url)
#    f = open('res.html', 'w+')
#    f.write(res.text)
#    f.close()

    soup = BeautifulSoup(res.text, 'html5lib')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class':'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class':'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class':'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class':'card-text'}).text.strip().replace('Description: ', '')

    dict_data = {
        'title': title,
        'price': price,
        'stock': stock,
        'category': category,
        'description': description
    }
    with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)


def create_csv():
    files = sorted(glob.glob('./results/*.json'))

    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)

    print('csv generated.....')

def run():
    total_pages = login()

    options = int(input('input options number:\n1.collecting all urls\n2.get detail all products\n3.create csv\nSilahkan pilih yang mana :'))
    if options == 1:
        total_urls = []
        for i in range(total_pages):
            page = i + 1
            urls = get_urls(page)
            total_urls += urls          #total_urls = total_urls +urls
        with open('all_urls.json', 'w') as outfile:
            json.dump(total_urls, outfile)
    if options == 2:
        with open('all_urls.json') as json_file:
            all_urls = json.load(json_file)
        for url in all_urls:
            get_detail(url)
    if options == 3:
        create_csv()

if __name__ == '__main__':
    run()