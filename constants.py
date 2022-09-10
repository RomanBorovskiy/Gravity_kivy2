from pathlib import Path

BASE_DIR = Path.cwd()
TEMPLATES_DIR = BASE_DIR.joinpath('templates')

SPACE_SIZE = 10000
MAX_TRACE = 100000
MIN_SCALE = .1
MAX_SCALE = 10