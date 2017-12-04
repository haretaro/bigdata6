from bs4 import BeautifulSoup
import os
import pickle
import re
from reader import reader
from urllib.parse import urljoin

page_images = re.compile(r'http://portal.nifty.com/20[0-9]{2}/[0-9]{2}/[0-9]{2}/.+')

def extract_images(json):
    page_num = json['pagenum']
    if page_num is None:
        return json
    imgs = []
    for i in range(1, page_num+1):
        page = 'PAGE{}'.format(i)
        if page not in json.keys():
            continue
        html = json[page]
        soup = BeautifulSoup(html, 'html5lib')
        for img in soup.find_all('img'):
            if 'src' in img.attrs.keys():
                src = urljoin(json['baseurl'], img['src'])
                if page_images.match(src):
                    imgs.append(src)
    json['imgs'] = imgs
    json['imgnum'] = len(imgs)
    return json

def with_images(reader, cache='scraped.bin', verbose=False):
    if os.path.exists(cache):
        with open(cache, 'rb') as f:
            data = pickle.load(f)
        for j in data:
            yield j
        raise StopIteration()

    data = []
    for i, json in enumerate(reader):
        j = extract_images(json)
        data.append(j)
        if verbose:
            print('{}/8358'.format(i))
        yield(j)
    if not os.path.exists(cache):
        with open(cache, 'wb') as fo:
            pickle.dump(data, fo)

def show(r):
    j = scrape(next(r))
    print('page num', j['pagenum'])
    for src in j['imgs']:
        print(src)

if __name__ == '__main__':
    r = with_images(reader(), verbose=True)
    data = list(r)
    print(data[0])
