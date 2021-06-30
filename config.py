PROJECT_NAME = 'your-domain-skel'

#
# LOGGING CONFIG

LOG_FILE = '/var/log/{}.log'.format(PROJECT_NAME)

LOGGING = {
	'version':				1,
    'formatters': {
        'verbose': {
            'format': 		'%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': 		'%Y-%m-%d %H:%M:%S'
		},
        'simple': {
            'format': 		'[%(levelname)s] %(message)s',
		},
	},
	'handlers': {
		'file': {
			'class': 		'logging.FileHandler',
			'formatter': 	'verbose',
			'filename': 	LOG_FILE,
		},
		'default': {
			'class': 		'logging.StreamHandler',
			'formatter': 	'simple',
		},
	},
	'loggers': {
		'': {
			'handlers': [
				'file',
				'default',
			],
			'level':		'DEBUG',
		},		
	}
}

#
# CPANEL CONFIG

HOOK_SCRIPT_DIR = '/usr/local/cpanel/3rdparty/bin/{}'.format(PROJECT_NAME)
PYTHON_EXE = '/path/to/your/venv'


#
# DOMAIN SKEL CONFIG

DOMAIN_SKEL_SKELDIR = '/path/to/your/skel'
