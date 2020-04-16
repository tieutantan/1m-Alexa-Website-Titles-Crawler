import config
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.WARNING, filename=config.BUG_FILE)

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
        hearders = {'headers':config.USER_AGENT}
        response = requests.get(url, timeout=config.TIMEOUT, headers=hearders)
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
    with open(config.RESULT_FILE, 'a', encoding="utf-8") as f:
        f.writelines(str(string))