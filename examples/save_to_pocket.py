#!/usr/bin/env python
#
# vim: sw=4 ts=4 st=4
#
#  Copyright 2014 Felipe Borges <felipe10borges@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Add an Item to Pocket'''

__author__ = 'Felipe Borges'

import sys
sys.path.append("..")
import getopt

import pocket

USAGE = '''Usage: save_to_pocket [options] url

  This script adds an Item to Pocket.

  Options:

    -h --help: print this help
    --consumer_key : the Pocket API consumer key
    --access_token : the user's Pocket Access Token
	'''

def print_usage_and_exit():
	print (USAGE)
	sys.exit(2)

def main():
	try:
		shortflags = 'h'
		longflags = ['help', 'consumer_key=', 'access_token=']
		opts, args = getopt.gnu_getopt(sys.argv[1:], shortflags, longflags)
	except getopt.GetoptError:
		print_usage_and_exit()

	consumer_key = None
	access_token = None

	for o, a in opts:
		if o in ('-h', '--help'):
			print_usage_and_exit()
		if o in ('--consumer_key'):
			consumer_key = a
		if o in ('--access_token'):
			access_token = a

	url = ' '.join(args)
	if not url or not consumer_key or not access_token:
		print_usage_and_exit()

	api = pocket.Api(consumer_key = consumer_key, access_token = access_token)

	try:
		item = api.add(url)
		print ('Item \'%s\' added successfuly!' % item.normal_url)
	except Exception as e:
		print (e)
		sys.exit(2)

if __name__ == "__main__":
	main()
