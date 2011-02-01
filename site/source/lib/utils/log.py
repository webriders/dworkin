import logging
from settings import DEBUG 

# create logger
logger = logging.getLogger("WR")
if DEBUG: 
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

# create console handler and set level to debug
ch = logging.StreamHandler()
#ch.setLevel(logging.ERROR)
# create formatter
formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(funcName)s: %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

#TODO: move logging to rotating file handler 
