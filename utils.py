import logging
import logging.config
import sys
import os
import json
import config


__all__ = [
	'get_hook_input', 'get_script_name', 'get_logger', 'logger'
]


def get_hook_input():
	stdin = ''.join(sys.stdin.readlines())
	stdin = json.loads(stdin)
	return stdin['data']


def get_script_name():
	script_name = os.path.basename(sys.argv[0]).split('.')
	script_name.pop()
	return '.'.join(script_name)


def get_logger(name=None):
	if name is None:
		name = get_script_name()
	
	logging.config.dictConfig(config.LOGGING)

	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	
	return logger


logger = get_logger()
