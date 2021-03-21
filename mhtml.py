# -*- coding: utf-8 -*-
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import re, os


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def get_profile():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')  # 谷歌无头模式
    chromeOptions.add_argument('--disable-gpu')  # 禁用显卡
    chromeOptions.add_argument('window-size=1280,800')  # 指定浏览器分辨率
    chromeOptions.add_argument("--no-sandbox")
    return chromeOptions


def get_browser():
    browser = webdriver.Chrome(chrome_options=get_profile())
    return browser


def _get_page(initial_url):
    print(initial_url)
    browser = get_browser()
    browser.get(initial_url)

    html = browser.page_source
    if title := re.search("<title>(.*?)</title>", html, flags=re.S):
        title = title.group(1)
    if title != "404错误_C语言中文网" and title:
        title = validateTitle(title)
        # 执行 Chome 开发工具命令，得到mhtml内容
        res = browser.execute_cdp_cmd('Page.captureSnapshot', {})
        with open(os.path.join(r"D:\C语言中文网", '{}.mhtml'.format(title)), 'w', newline='') as f:
            f.write(res['data'])
    browser.close()

if __name__ == '__main__':
    with ThreadPoolExecutor(16) as executor:
        for i in range(100000):
            url = f"http://c.biancheng.net/view/{i}.html"
            executor.submit(_get_page,url)

