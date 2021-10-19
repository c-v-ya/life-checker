from pathlib import Path

import yaml

BAS_DIR = Path(__file__).parent.parent

config_path = BAS_DIR / 'config.yaml'
with config_path.open('r') as f:
    config = yaml.safe_load(f)

TARGETS_FILE = config.get('targets_file')
RESPONSE_TIMEOUT = config.get('response_timeout', 0)
LOGSTASH_ENDPOINTS = config.get('logstash_endpoints', [])
USE_TLS = config.get('use_tls', True)
LOG_DEAD = config.get('log_dead', True)
