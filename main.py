import os
import time
import platform
import threading

import requests

URL = f'https://{input("URL (without protocol) => ")}'

if os.name == 'nt' and platform.release() != 10:
    Red = ''
    Green = ''
    None_color = ''

else:
    Red = '\x1b[31m'
    Green = '\x1b[32m'
    None_color = '\x1b[0m'


def get_proxy_generator():
    with open('proxies.txt') as file:
        proxyes = [line.strip() for line in file.readlines() if line.strip()]

    for proxy in proxyes:
        yield proxy


def check_proxy(proxy):
    global valid, invalid
    proxyDict = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}"
    }

    try:
        requests.get(URL, proxies=proxyDict, timeout=5)
        valid += 1
        goods.append(proxy)

    except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout):
        invalid += 1

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Green}Valid: {valid}\n{Red}Invalid: {invalid}\n{None_color}")


if __name__ == '__main__':
    valid = 0
    invalid = 0
    goods = []

    generator = get_proxy_generator()
    count_threads = int(input("Count of threads => "))
    threads = []

    while True:
        try:
            for i in range(count_threads):
                thread = threading.Thread(target=check_proxy, args=(next(generator),))
                thread.start()
                threads.append(thread)
            time.sleep(1)
        except StopIteration:
            break

    for thread in threads:
        thread.join()

    with open("goods.txt", "w") as file:
        for good_proxy in goods:
            file.write(f"{good_proxy}\n")

    input("Enter to exit...")
