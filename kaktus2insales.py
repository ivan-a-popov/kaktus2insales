# Main integration module
# put 'python3 <this file>' to crontab

import time
import log_setup
import insales
import kak2c

tic = time.perf_counter()
log_setup.logger.debug('Job started.')

index = insales.get_index()
if not index:
    log_setup.logger.error("Failed to get data from InSales. Exiting.")
    exit(1)
stocks = kak2c.get_stocks()
if not stocks:
    log_setup.logger.error("Failed to get data from kak2c. Exiting.")
    exit(1)

variants = []
for key, id in index.items():
    try:
        qty = stocks[key]
    except KeyError:
        log_setup.logger.warning("Barcode "+key+" not found in stocks.")
        continue
    else:
        variants.append({"id": id, "quantity": qty})

result = insales.update(variants)
if result:
    toc = time.perf_counter()
    log_setup.logger.debug(f"Job finished. {toc - tic:0.4f} seconds spent totally.")
    exit(0)
else:
    log_setup.logger.error("Update failed.")
    exit(1)
