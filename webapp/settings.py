import configparser


config = configparser.ConfigParser()
config.read('etc/base.conf')
config.read('etc/local.conf')

DEBUG = config.getboolean('general', 'debug')

# development server
HOST = config.get('server', 'host')
PORT = config.get('server', 'port')

# database
DB_HOST = config.get('database', 'host')
DB_PORT = config.get('database', 'port')
DB_NAME = config.get('database', 'name')

# cache
CACHE_HOST = config.get('cache', 'host')
CACHE_PORT = config.get('cache', 'port')

# paths
TEMPLATE_DIR = config.get('paths', 'templates')
STATIC_DIR = config.get('paths', 'static_dir')
STATIC_URL = config.get('paths', 'static_url')

MODULES_DIR = config.get('paths', 'modules_dir')