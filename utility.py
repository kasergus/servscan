# импорт библиотек
import os
import argparse
import requests
import json

# объявление констант во избежание магических цифр
NUMBER_OF_IP_SEGMENTS = 4

# объявление функций
def do_ping_sweep(ip, num_of_host, count=5, time_to_wait=1):
    ip_parts = ip.split('.')
    if len(ip_parts) != NUMBER_OF_IP_SEGMENTS or not all(list(map(lambda x: x.isnumeric(), ip_parts))):
        # тут выполнеятся проверка на правильность данных
        # (правильно ли записаны сегменты ip адреса 
        #  и нет ли в нём иных символов кроме цифр)
        print("[#] Error: wrong ip address!")
        return
    network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2]
    scanned_ip = network_ip + '.' + str(int(ip_parts[3]) + num_of_host)
    response = os.popen(f"ping -c {count} -W {time_to_wait} {scanned_ip}").readlines()
    result = ''.join(response)
    if (result.split(' ')[0] == 'PING'):  # проверка на ошибку от команды ping
        print(f"[#] Result of scanning {scanned_ip}:\n{result}", end = '\n\n')
    else:
        print("[#] Error: bad command syntax!")

def send_http_request(target, method, headers=None, payload=None):
    headers_dict = dict()

    if headers:
        for header in headers:
            header_name = header.split(':')[0]
            header_value = header.split(':')[1:]
            headers_dict[header_name] = ':'.join(header_value)

    if method == 'GET':
        response = requests.get(target, params=payload, headers=headers_dict)
    elif method == 'POST':
        response = requests.post(target, params=payload, headers=headers_dict)

    print(f"[#] Response status code: {response.status_code}")
    print(f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}")
    print(f"[#] Response content:\n{response.text}")


# создание и парсинг аргументов

# создание основного парсера и субпарсера задач программы
parser = argparse.ArgumentParser(description="Proxy Server with scanning function")
taskparser = parser.add_subparsers(dest='task', help="Choose task to do")

# парсер отправки http запроса
send_parser = taskparser.add_parser('sendhttp', help="Program will send http request")
send_parser.add_argument('-m', '--method', type=str, required=True, choices=['GET', 'POST'], help="Method of http request (GET or POST)")
send_parser.add_argument('-t', '--target', type=str, required=True, help="The link to witch request will send")
send_parser.add_argument('-hd', '--headers', nargs='+', help="Headers of request")

# парсер сканирования хостов в локальной сети
scan_parser = taskparser.add_parser('scan', help="Program will scan host in local network")
scan_parser.add_argument('-i', '--ip', required=True, type=str, help="Ip address which will scan")
scan_parser.add_argument('-n', '--num_of_host', type=int, default=0, help="Number of host, which will scan")
scan_parser.add_argument('-c', '--count', type=int, default=5, help="Number of times the request will be sent")
scan_parser.add_argument('-t', '--time_to_wait', type=int, default=1, help="Time (in seconds) to wait for response")

args = parser.parse_args()


# анализ аргументов и выполение программы
if not args.task:
    print("[#] Error: No tasks has been selected!")
    parser.print_help()
elif args.task == 'sendhttp':
    send_http_request(args.target, args.method, headers=args.headers)
elif args.task == 'scan':
    do_ping_sweep(args.ip, args.num_of_host, args.count, args.time_to_wait)