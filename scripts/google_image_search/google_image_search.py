#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import time
import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

TIMEOUT = 15


def get_image_urls(html):
    """Parse image URL from HTML content
    """
    soup = BeautifulSoup(html, 'html.parser')
    i = 0
    urls = []
    for a in soup.find_all('a', {'class': 'rg_l'}):
        i += 1
        href = a['href']
        m = re.match(r'.*?imgurl=(.*?)&.*', href)
        if m:
            urls.append(m.group(1))
    return urls


def google_image_search(q):
    """Google Image Search Web Driver
    """

    #  Assigning the user agent string for PhantomJS
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)

    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36")

    try:
        print("Create driver")
        # FIXME: Assume PhantomJS in PATH setting
        driver = webdriver.PhantomJS(desired_capabilities=dcap)

        # For testing
        #driver = webdriver.Firefox()

        driver.implicitly_wait(TIMEOUT)
        driver.set_page_load_timeout(TIMEOUT)

        print("Goto google.com")
        driver.get("https://www.google.co.th/search?q={0}&hl=en&tbm=isch&source=lnt&tbs=itp:face".format(q))

        """
        ### FIXME: Step-by-step
        driver.get('https://www.google.com/?hl=en')
        elem = driver.find_element_by_name('q')

        print("Enter name: {0}".format(n))
        elem.send_keys(n + '\n')

        print("Switch to Image search")
        elem = driver.find_element_by_link_text('Images')
        elem.click()
        print("Open Search tools")
        elem = driver.find_element_by_link_text('Search tools')
        elem.click()
        try:
            print("Wait for Type selection")
            elem = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Type"]')))
        except Exception as e:
            print(e)
        print("Click Type")
        elem = driver.find_element(By.XPATH, '//div[@aria-label="Type"]')
        elem.click()
        print("Click Face")
        elem = driver.find_element_by_link_text('Face')
        elem.click()
        print("Sleep 5s")
        """
        try:
            print("Wait for loading complete")
            wait = WebDriverWait(driver, 15)
            elem = wait.until(EC.invisibility_of_element_located((By.ID, "isr_cld")))
        except TimeoutException:
            print("Timeout")

        html = driver.page_source
        urls = get_image_urls(html)

        if len(urls) < args.count:
            print("Scroll to end (1)")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                print("Wait for loading complete")
                wait = WebDriverWait(driver, 15)
                elem = wait.until(EC.invisibility_of_element_located((By.ID, "isr_cld")))
            except TimeoutException:
                print("Timeout")

        html = driver.page_source
        urls = get_image_urls(html)

        while len(urls) < args.count:
            try:
                print("Wait for more button visible")
                wait = WebDriverWait(driver, 1)
                elem = wait.until(EC.element_to_be_clickable((By.ID, "smb")))
                #elem = driver.find_element(By.XPATH, '//input[@id="smb"]')
                print("Click more button")
                elem.click()
                try:
                    print("Wait for more button invisible")
                    wait = WebDriverWait(driver, 15)
                    elem = wait.until(EC.invisibility_of_element_located((By.ID, "smb")))
                except TimeoutException:
                    print("Timeout")
                print("Scroll to end (2)")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    print("Wait for loading complete")
                    wait = WebDriverWait(driver, 15)
                    elem = wait.until(EC.invisibility_of_element_located((By.ID, "isr_cld")))
                except TimeoutException:
                    print("Timeout")
                html = driver.page_source
                urls = get_image_urls(html)
            except TimeoutException:
                print("Timeout")
                break
            except Exception as e:
                print(e)
                break
        print("Total: {0}".format(len(urls)))
        driver.quit()
        return urls
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        raise
    return []


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Google Image Search (Face type)')
    parser.add_argument('input', help='Input file name')
    parser.add_argument('-c', '--count', type=int, default=10,
                        help='Number of image per name')
    parser.add_argument('-o', '--output', default='output-img.csv',
                        help='Output CSV file name')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Output without header at the first row')
    parser.add_argument('-r', '--retry', type=int, default=5,
                        help='Number of retry if errors')
    parser.set_defaults(header=True)

    args = parser.parse_args()

    print(args)

    df = pd.read_csv(args.input)
    out = open(args.output, 'wb')

    writer = csv.DictWriter(out, fieldnames=list(df.columns) + ['ref_id', 'image_url', 'image_order'])
    if args.header:
        writer.writeheader()

    try:
        _id = 0
        for i, r in df.iterrows():
            row = dict(r)
            print(row)
            ref_id = row['id']
            n = row['name']
            urls = []
            retry = 0
            while retry < args.retry:
                try:
                    urls = google_image_search(n)
                    break
                except:
                    retry += 1
                    time.sleep(retry)
                    print("Retry #{}".format(retry))
            for i, u in enumerate(urls):
                row['ref_id'] = ref_id
                row['id'] = _id
                row['image_url'] = u
                row['image_order'] = i
                writer.writerow(row)
                _id += 1
    finally:
        out.close()
