# импорт библиотек
import os
import argparse
import requests
import http.server
import socketserver
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# объявление констант во избежание магических цифр
MAX_OF_HOSTS = 100
NUMBER_OF_IP_SEGMENTS = 4
PORT = 3000

# объявление класса сервера
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Текст ответа функции, в аргументы которой вписываются заголовки GET запроса
        raw_text = do_ping_sweep(self.headers.get('target'), int(self.headers.get('count', '0')))
        response_body = bytes(raw_text, 'utf-8')

        # объявление переменных во избежание магических цифр и строк
        status_code = 200
        content_type = "text/html"
        status_text = "scan mode"

        # отправка заголовков для корректного ответа сервера
        self.send_response(status_code, status_text)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(response_body)))
        self.end_headers()

        self.wfile.write(response_body)

    def do_POST(self):
        if self.headers.get('Header') and self.headers.get('Header-value'):
            # проверка на правильное указание пользовательского заголовка
            headers = self.headers.get('Header') + ':' + self.headers.get('Header-value')
            headers_list = list().append(headers)
            raw_text = send_http_request(self.headers.get('target'), self.headers.get('method'), headers=headers_list)
            raw_text = raw_text
        else:
            raw_text = send_http_request(self.headers.get('target'), self.headers.get('method'))

        # объявление переменных во избежание магических цифр и строк
        response_body = bytes(raw_text, 'utf-8')
        status_code = 200
        content_type = "text/html"
        status_text = "sendhttp mode"

        # отправка заголовков для корректного ответа сервера
        self.send_response(status_code, status_text)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(response_body)))
        self.end_headers()

        self.wfile.write(response_body)


# объявление функций 
# (в данном варианте утилиты как сервера функции не печатают значение, 
#  а возвращают его, дабы сервер смог отправить результат клиенту)
def do_ping_sweep(target, count):
    if (target):
        ip_parts = target.split('.')
    else:
        return f"[#] Error: no ip adderss"
    result = str()
    if len(ip_parts) != NUMBER_OF_IP_SEGMENTS or not all(list(map(lambda x: x.isnumeric(), ip_parts))):
        # тут выполнеятся проверка на правильность данных
        # (правильно ли записаны сегменты ip адреса 
        #  и нет ли в нём иных символов кроме цифр)
        return f"[#] Error: wrong ip address {target}"
    elif count <= 0 or count >= MAX_OF_HOSTS:
        return f"[#] Error: wrong count of hosts {count}, must be 0 < count < {MAX_OF_HOSTS}"
    network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2]
    for host in range(1, count+1):
        scanned_ip = network_ip + '.' + str(int(ip_parts[3]) + host)
        # здесь установлено ограничение в 3 пакета и 1 секунду, 
        # потому что 3 секунды это оптимальное время ожидания
        response = os.popen(f"ping -c 3 -W 1 {scanned_ip}").readlines()
        result = result + ''.join(response) + '\n\n'
    if (result.split(' ')[0] == 'PING'):  # проверка на ошибку от команды ping
        return f"[#] Results of scanning:\n\n{result}"
    else:
        return "[#] Error: bad command syntax!"

def send_http_request(target, method, headers=None, payload=None):
    headers_dict = dict()

    if headers:
        for header in headers:
            header_name = header.split(':')[0]
            header_value = header.split(':')[1:]
            headers_dict[header_name] = ':'.join(header_value)

    try:
        if method == 'GET':
            response = requests.get(target, params=payload, headers=headers_dict)
        elif method == 'POST':
            response = requests.post(target, params=payload, headers=headers_dict)
        else:
            return "[#] Error: you must write method! (GET|POST)"
    except requests.exceptions.ConnectionError:
        return "[#] Error: connection error. Check your target's name!"

    return f"[#] Response status code: {response.status_code}\n" + \
           f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}\n" + \
           f"[#] Response content:\n{response.text}"

# запуск сервера
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server at port: {PORT}")
    httpd.serve_forever()