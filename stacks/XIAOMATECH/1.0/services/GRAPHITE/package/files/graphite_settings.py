SECRET_KEY = 'example'
TIME_ZONE = 'Asia/Shanghai'
DEFAULT_XFILES_FACTOR = 0
URL_PREFIX = '/'
LOG_DIR = '/var/log/graphite'
GRAPHITE_ROOT = '/opt/graphite'
CONF_DIR = '/etc/graphite'
DASHBOARD_CONF = '/etc/graphite/dashboard.conf'
GRAPHTEMPLATES_CONF = '/etc/graphite/graphTemplates.conf'
# STORAGE_DIR = '/opt/graphite/storage'
# STATIC_ROOT = '/opt/graphite/static'
# INDEX_FILE = '/opt/graphite/storage/index'
# CERES_DIR = '/opt/graphite/storage/ceres'
# WHISPER_DIR = '/opt/graphite/storage/whisper'
# RRD_DIR = '/opt/graphite/storage/rrd'
# MEMCACHE_HOSTS = ['10.10.10.10:11211', '10.10.10.11:11211', '10.10.10.12:11211']
STORAGE_FINDERS = (
    'graphite.graphouse.GraphouseFinder',
)
