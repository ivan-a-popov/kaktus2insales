# Module for kak2c

import log_setup
import requests
import json
import time

def get_token():
    try:
        file = open('temp/token_info')
    except FileNotFoundError:
        return get_new_token('Token file not found. ')
    else:
        token_info = json.load(file)
        file.close()
        token = token_info['access_token']
        url = 'https://app.kak2c.ru/api/lite/account_info'
        headers = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=headers)
        return token if r.ok else get_new_token('Token expired. ')


def get_new_token(reason):
    url = 'https://app.kak2c.ru/api/lite/auth'
    try:
        file = open('files/kak2c_info')
    except FileNotFoundError:
        log_setup.logger.critical('No auth file found.  Exiting...')
        raise
    else:
        log_setup.logger.info(reason+'Getting new token...')
        body = file.read()
        file.close()
        r = requests.post(url, data=body)
        log_setup.logger.debug(r)
        token_info = r.json()
        with open('temp/token_info', 'w+') as file:
            json.dump(token_info, file)
        return token_info['access_token']

def get_products(token, page=0):
    tic = time.perf_counter()
    log_setup.logger.debug('Getting products from kak2c, page '+str(page))
    url = 'https://app.kak2c.ru/api/lite/products?page='+str(page)
    headers = {'Authorization': 'Bearer '+token}
    r = requests.get(url, headers=headers)
    if not r.ok:
        log_setup.logger.error('Failed to get data from kak2c. Exiting.')
        return False
    else:
        toc = time.perf_counter()
        log_setup.logger.debug(f"Done. {toc - tic:0.4f} seconds spent.")
        return r.json()

def get_items():
    token = get_token()
    data = get_products(token)
    if data:
        products = data['products']
        total = data['recordsTotal']
        if total > 100:
            for i in range(0, total//100):
                page = get_products(token, i+1)
                products += page['products']
        variants = []
        for product in products:
            item = (product['variants'])
            for each in item:
                variants.append(each)
        with open('temp/kaktus_items', 'w+') as file:
            json.dump(variants, file, indent=4)
        return variants
    else:
        return False

def get_stocks():
    items = get_items()
    if items:
        stocks = {}
        for item in items:
            stocks[item['id']] = item['stock'][0]['stockTotal']
        with open('temp/stocks', 'w+') as file:
            json.dump(stocks, file)
        return stocks
    else:
        return False
