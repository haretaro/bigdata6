import re
import json

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
                    d['writer'] = row[7:-1]

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

def reader():
    for n in range(2008, 2016):
        r = parse('{}.txt'.format(n))
        for j in r:
            yield j

if __name__ == '__main__':
    data = list(reader())
    with open('output.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
