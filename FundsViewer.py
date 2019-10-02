import argparse
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from time import time


def google_send(text):
    driver.switch_to.window(driver.window_handles[0])
    ele = driver.find_element_by_name('q')
    ele.clear()
    ele.send_keys(text)


def get_fund_site(fund_name):
    google_send(fund_name + '\n')
    t = re.findall('<a href="(.*?)"', driver.page_source)
    t = list(filter(lambda x: x.startswith('https:'), t))
    return t[1]


def argparser():
    """
    Command line arguments are specified here.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', action="store", default=0, type=int,
                        help='Starting integer of funds')
    return parser.parse_args()


if __name__ == '__main__':
    args = argparser().__dict__
    print(args)

    options = Options()
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    driver = webdriver.Chrome(options=options,
                              executable_path=r'.\chromedriver.exe')

    driver.get('https://www.google.com')

    funds = pd.read_csv('all')

    for i, fund_name in enumerate(funds['0'][args.get('start'):]):
        time_of_last_request = time()
        site = get_fund_site(fund_name)
        driver.execute_script("window.open('{}');".format(site))
        driver.switch_to.window(driver.window_handles[1])
        if i > 2:
            print('You have seen up to the {}th fund'.format(i-2))
        while len(driver.window_handles) > 3:
            pass
        sleep(max(0.0, time_of_last_request + 2 - time()))