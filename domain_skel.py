#!/path/to/your/venv/bin/python
#
# Addon Domain Skeleton Hook
#
# When an addon domain is created, copy files from a domain skeleton directory.
#
# Events:
#	 Cpanel::Api2::AddonDomain::addaddondomain
#	 Cpanel::Api2::Subdomain::addsubdomain	
#
# Author:
#	 Keobi Web Hosting
#	 https://keobi.com


import json
import sys
import os
import subprocess
import click
import config
from utils import *


def format_result(is_failure=False, msg='Success'):
	print(json.dumps([int(is_failure), msg]))
	sys.exit(1 if is_failure else 0)


@click.command()
def command():
	# {
	#	"user": "<username>",
	#	"output":[
	#		{
	#			"reason": "The system successfully parked (aliased) the domain “<domain>” on top of the domain “<subdomain>”.",
	#			"result":1
	#		}
	#	],
	#	"args":{
	#		"ftp_is_optional": 1,
	#		"newdomain": "<domain>",
	#		"subdomain": "<subdomain>",
	#		"dir": "<relpath>"
	#	}
	# }
	
	input = get_hook_input()
	logger.debug('INPUT: {}'.format(input))
	
	if 'output' not in input or 'result' not in input['output'][0] or not input['output'][0]['result']:
		logger.error('Domain creation failed or the input is malformed')
		logger.debug('Input: {}'.format(input))
		format_result()
	
	args = input['args']
	domain = args['newdomain']
	
	logger.debug('Hook for new domain triggered: {}'.format(domain))
	
  # Using UAPI, get domain info
  # (this saves guesswork when choosing the domain's root directory
  #  since input["args"]["dir"] is relative to the home directory.)
	cmd_api_domain = [
		'uapi',
		'--user={}'.format(input['user']),
		'--output=json',
		'DomainInfo',
		'single_domain_data',
		'domain={}'.format(domain)
	]
	
	logger.debug('Running API command: {}'.format(' '.join(cmd_api_domain)))
	cmd = subprocess.run(cmd_api_domain, stdout=subprocess.PIPE)
	cmd_output = json.loads(cmd.stdout)	
	cmd_result = cmd_output['result']
	
	document_root = cmd_result['data']['documentroot']
	
	cmd_copy = 'cp {}/* {}'.format(config.DOMAIN_SKEL_SKELDIR, document_root)
	
	logger.debug('Running copy command: {}'.format(cmd_copy))
	cmd = subprocess.call(cmd_copy, shell=True)
	
	format_result()


if __name__ == '__main__':
	# Check for --describe
	if len(sys.argv) == 2 and sys.argv[1] == '--describe':
    # The --describe allows you to automate hook registration
    #
    # Based on the describe() method from here:
    # https://documentation.cpanel.net/display/DD/Guide+to+Standardized+Hooks+-+The+describe%28%29+Method
    
    hook_script = '{}/domain_skel.py'.format(config.HOOK_SCRIPT_DIR)
    
		print(json.dumps([
       {
        'category': 	    'Cpanel',
        'event':			    'Api2::AddonDomain::addaddondomain',
        'stage':			    'post',
        'hook':				    hook_script,
        'exectype':		    'script',
        'escalateprivs':	True, # Needed for Cpanel category since it runs as the cPanel user
      }, {
        'category': 	    'Cpanel',
        'event':			    'Api2::Subdomain::addsubdomain',
        'stage':			    'post',
        'hook':				    hook_script,
        'exectype':			  'script',
        'escalateprivs':	True, # Needed for Cpanel category since it runs as the cPanel user
      },
    ]))
    
		sys.exit(1)
	
  # Required for Click to work properly
  # Makes for some funkiness in input['output'], though
  # https://click.palletsprojects.com/en/8.0.x/unicode-support/
	os.environ['LC_ALL'] = 'en_US.UTF-8'
	os.environ['LANG'] = 'en_us.UTF-8'
	
	logger.debug('{} called'.format(get_script_name()))

	command()
