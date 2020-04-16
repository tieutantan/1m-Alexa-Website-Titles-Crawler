import CoreModules.path as path

from multiprocessing.dummy import Pool as ThreadPool
import requests
from bs4 import BeautifulSoup
import sys
import os
import logging
import time

SOURCE_FILE = path.relative('top-1m.csv')
RESULT_FILE = path.relative('top-1m-result.csv')
BUG_FILE = path.relative('errors.log')

start_time = time.time()
os.system('cls||clear')

first_run = input('Frist run? (Y as default) ')
if first_run.lower() != 'n':
    path.remove(RESULT_FILE)
    path.remove(BUG_FILE)

test_mode = input('Test mode ? only run on 200 webs (Y as default) ')

threads_run = input('How many threads ? (50 as default) ')
if not threads_run:
    number_threads = int(50)
else:
    number_threads = int(threads_run.strip())

time.sleep(1)
print("Exe with " + str(number_threads) + " threads...")
time.sleep(3)

logging.basicConfig(level=logging.WARNING, filename=BUG_FILE)

def main():

    with open(SOURCE_FILE) as FileObj:

        list_rank = []
        list_url = []

        for index, item in enumerate(FileObj):

            rank = get_rank(item).strip()
            list_rank.append(rank)

            url = get_url(item).strip()
            list_url.append(url)

            if test_mode.lower() != 'n':
                if index > 200:
                    break

    pool = ThreadPool(number_threads)
    process = pool.starmap(get_info, zip(list_rank, list_url))

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

def get_info(rank, url):

    title = get_title(url)

    if title != None and title != '' and \
        title.__contains__("404 Page") == False and \
        title.__contains__("403 Page") == False and \
        title.__contains__("503 -") == False and \
        title.__contains__("Attention Required") == False:
        text = "{},{},{}\n".format(rank, url, title)
        store_result(text)
        print(rank + "- <3 - " + url)

def get_title(url):
    try:
        hearders = {'headers':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
        response = requests.get(url, timeout=10.05, headers=hearders)
        html = BeautifulSoup(response.text, "html.parser")
        return html.title.text
    except Exception as e:
        logging.exception("Oops: " + "Stop at: " + url)
        print("Stop at - " + url)

def get_url(string):
        output = string.split(',')
        return 'http://' + output[1]

def get_rank(string):
        output = string.split(',')
        return output[0]

def store_result(string):
    with open(RESULT_FILE, 'a', encoding="utf-8") as f:
        f.writelines(str(string))

if __name__ == '__main__':
    main()

    print("-------- %s seconds --------" % (time.time() - start_time))
    
    with open(BUG_FILE, 'a', encoding="utf-8") as f:
        f.writelines("\n\n")
        f.writelines(str("-------- %s seconds --------" % (time.time() - start_time)))