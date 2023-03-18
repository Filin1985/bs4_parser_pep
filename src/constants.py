from pathlib import Path


BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS_DIR = 'results'
DOWNLOADS_DIR = 'downloads'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEPS_URl = 'https://peps.python.org/'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

PRETTY_FORMAT = 'pretty'
FILE_FORMAT = 'file'
OUTPUT_CHOICES = {
    'pretty': 'pretty',
    'file': 'file'
}
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
