import requests
import os
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

baseUrl = 'http://akumu.ru/lineage2/L2EU/P388/L2EU-P388-D20221128-P-220706-221129-1/'

directories = []
failedFiles = []

def parseUrl(url):
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, features="html.parser")
        for (i, a) in enumerate(soup.find_all('a', href=True)):
            if i <= 6:
                continue
            href = a['href']
            full_url = urljoin(url, href)
            path = full_url.replace(baseUrl, '')
            if href[-1] == '/' and not directories.__contains__(path):
                directories.append(path)
                print(f'\nParsing {path}')
                parseUrl(full_url)
            elif not fileExists(f'files/{path}'):
                    loadFile(full_url)
                    
    except Exception as e:
        print(f'Failed to parse {url}. {str(e)}')
        pass
        

# TODO: Check file size ?
def fileExists(path):
    return os.path.isfile(path)

def loadFile(url):
    try:
        fileName = url.replace(baseUrl, '')
        os.makedirs(os.path.dirname(f'files/{fileName}'), exist_ok=True)
        with open(f'files/{fileName}', "wb") as f:
            print(f"\nDownloading {fileName}")
            file = requests.get(url, stream=True)
            contentLength = file.headers.get('content-length')
            if contentLength is None: # no content length header
                f.write(file.content)
            else:
                dl = 0
                contentLength = int(contentLength)
                for data in file.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / contentLength)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()
            f.close()
    except Exception as e:
        failedFiles.append(url)
        print(f'Failed to load {fileName}.\n{str(e)}')
        pass


parseUrl(baseUrl)