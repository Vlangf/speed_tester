from speed import SpeedChecker
from browsermobproxy import Server
from selenium import webdriver
import json


def set_proxy_and_driver():
    server = Server("~/browsermob-proxy/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    driver = webdriver.Chrome(chrome_options=chrome_options)

    return server, proxy, driver


def test_urls_opening_speed():
    result_dict = {}

    with open('urls.json', 'r') as file:
        urls = json.load(file)['urls']

    for each in urls:
        server, proxy, driver = set_proxy_and_driver()
        time = SpeedChecker().with_time_limit(each, proxy, driver, server)
        url = each
        result_dict[url] = time

    print(result_dict)

    for each in urls:
        server, proxy, driver = set_proxy_and_driver()
        time = SpeedChecker().with_loadEventEnd(each, driver)
        url = each
        result_dict[url] = time

    print(result_dict)


test_urls_opening_speed()
