import requests
import os
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = 'http://akumu.ru/lineage2/L2EU/P388/L2EU-P388-D20221128-P-220706-221129-1/'
directories = []
links = []


def parseUrl(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, features="html.parser")
    for (i, a) in enumerate(soup.find_all('a', href=True)):
        if i <= 6:
            continue
        href = a['href']
        full_url = urljoin(url, href)
        path = full_url.replace(base_url, '')
        if href[-1] == '/' and not directories.__contains__(href[:-1]):
            directories.append(href[:-1])
            parseUrl(full_url)
            print(f'Parsing {path}')
        else :
            loadFile(full_url)


def loadFile(url):
    fileName = url.replace(base_url, '')
    os.makedirs(os.path.dirname(f'files/{fileName}'), exist_ok=True)
    with open(f'files/{fileName}', "wb") as f:
        print(f"\nDownloading {fileName}")
        file = requests.get(url, stream=True)
        total_length = file.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(file.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in file.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()


parseUrl(base_url)