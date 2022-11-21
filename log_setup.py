# Logging setup
# Change fh.setLevel from ERROR to DEBUG when tracing issues

import logging

# create logger
logger = logging.getLogger('kaktus2insales')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages (set to 'error' when ran in production)
fh = logging.FileHandler('files/kaktus2insales.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
