#coding: utf-8
import re
import json
import os
import pickle

def normalize(writer_name):
    w = writer_name
    w = re.sub('\s|\(|\)|（|）', '', w)
    w = re.sub('\/|／|・|＋|、', '', w)
    w = w.replace('Ｔ','T')
    w = w.replace('齋藤','斎藤')
    w = w.replace('Ustream','USTREAM')
    w = w.replace('miooon', 'minoon')
    w = re.sub('^デイリーポータルＺ編集部$', '編集部', w)
    w = w.replace('デイリーポータルZ編集部', '')
    return w

def parse(filename):
    with open(filename, newline='\n') as f:
        for i, row in enumerate(f.readlines()):
            try:
                if row.startswith('CONTENT=BEGIN'):
                    d = {}
                    continue

                elif row.startswith('PUBDATE'):
                    d['date'] = row[8:-1]

                elif row.startswith('TITLE'):
                    d['title'] = row[6:-1]

                elif row.startswith('WRITER'):
                    d['writer'] = normalize(row[7:-1])

                elif row.startswith('BASEURL'):
                    d['baseurl'] = row[8:-1]

                elif row.startswith('PV'):
                    num = row[3:].replace(',','')
                    try:
                        num = int(num)
                    except ValueError:
                        num = None
                    d['pv'] = num

                elif row.startswith('PAGENUM'):
                    num = row[8:]
                    try:
                        num = int(num)
                    except ValueError:
                        num = None
                    d['pagenum'] = num

                elif row.startswith('PAGEURL'):
                    d[re.search('PAGEURL[0-9]+', row).group()] = re.search('http:.+$', row).group()

                elif row.startswith('PAGE'):
                    key = re.search('PAGE[0-9]+', row).group()
                    line = row[len(key)+1:]
                    d[key] = d.get(key, '') + line

                elif row.startswith('（ラジオ'):
                    d['type'] = 'radio'

                elif row.startswith('（デイリーポータルZテレビ'):
                    d['type'] = 'tv'

                elif row == '\n':
                    continue

                elif row.startswith('CONTENT=END'):
                    yield d

                else:
                    raise Exception('Cannot Parse {}'.format(row))

            except Exception as e:
                raise Exception(e, filename, i, row)

#記事の情報を一個ずつ返すジェネレータ
def reader():
    if os.path.exists('cache.bin'):
        with open('cache.bin', 'rb') as f:
            data = pickle.load(f)
        for j in data:
            yield j
        raise StopIteration()

    data = []
    for n in range(2008, 2016):
        r = parse('{}.txt'.format(n))
        for j in r:
            data.append(j)
            yield j
    if not os.path.exists('cache.bin'):
        with open('cache.bin', 'wb') as fo:
            pickle.dump(data, fo)

if __name__ == '__main__':
    data = list(reader())
    print(data[0])
