from src.libs import *

ROOT = Path(__name__).parent.parent

DATA = ROOT / Path("data")
LOGS = ROOT / Path("logs")
DIRS = []
DIRS.append(DATA)
DIRS.append(LOGS)
# DIRS.append()
for a_dir in DIRS:
    a_dir.mkdir(exist_ok=True)

SEATS_DATASET = DATA / Path("seats.pkl")
CLUSTERS = DATA / Path("clusters.csv")
CENTROIDS = DATA / Path("centroids.txt")

LOG_FILE = LOGS / Path("example.log")
N_CLUSTERS = 12

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# logging.basicConfig(filename=str(LOG_FILE), encoding='utf-8', level=logging.INFO)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
