# InSales module

import requests
from requests.auth import HTTPBasicAuth
import log_setup
import json
import time

def get_info():
    try:
        file = open('files/insales_info')
    except FileNotFoundError:
        log_setup.logger.critical('No InSales auth file found. Exiting.')
        raise
    else:
        info = json.load(file)
        login = info["login"]
        password = info["password"]
        url = info["url"]
        file.close()
        return {'url': url, 'basic': HTTPBasicAuth(login, password)}

def get_products(info):
    url = info['url'] + 'products/count.json'
    r = requests.get(url, auth=info['basic'])
    qty = r.json()['count']
    url = info['url']+'products.json?per_page='+str(qty)
    r = requests.get(url, auth=info['basic'])
    return r.json()

def get_index():
    info = get_info()
    tic = time.perf_counter()
    log_setup.logger.debug('Getting products from InSales...')
    products = get_products(info)
    toc = time.perf_counter()
    log_setup.logger.debug(f"Done. {toc - tic:0.4f} seconds spent.")
    tic = time.perf_counter()
    log_setup.logger.debug("Processing data and writing files...")

    variants = []
    for product in products:
        product_variants = (product["variants"])
        for variant in product_variants:
            variants.append(variant)

    with open('temp/insales_variants', 'w+') as file:
        json.dump(variants, file, indent=4)

    index = {}
    for variant in variants:
        if variant["barcode"]:
            index[variant["barcode"]] = variant["id"]

    with open('temp/index', 'w+') as file:
         json.dump(index, file)

    toc = time.perf_counter()
    log_setup.logger.debug(f"Done. {toc - tic:0.4f} seconds spent, "+str(len(index))+" items written to index.")
    return index

def update(variants):
    tic = time.perf_counter()
    log_setup.logger.debug('Updating qty in InSales...')
    info = get_info()
    url = info['url']+'products/variants_group_update.json'
    r = requests.put(url, auth=info['basic'], json={'variants': variants})
    if not r.ok:
        log_setup.logger.error(r)
        return False
    else:
        with open('temp/result', 'w+') as file:
            json.dump(r.json(), file, indent=4)
        toc = time.perf_counter()
        log_setup.logger.debug(f"Done. {toc - tic:0.4f} seconds spent.")
        return r
