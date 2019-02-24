#!/usr/bin/env python3

import os
import sys

import requests
import pprint

# Globals

URL	 = None
ISGD_URL = 'http://is.gd/create.php'
SUB	 = None

data = {}
shorten = False
limit = 10
orderby = 'score'
titlelen = 60

# Functions

def usage(status=0):
        ''' Display usage information and exit with specified status '''
        print('''Usage: {} [options] URL_OR_SUBREDDIT

        -s          Shorten URLs using (default: False)
        -n LIMIT    Number of articles to display (default: 10)
        -o ORDERBY  Field to sort articles by (default: score)
        -t TITLELEN Truncate title to specified length (default: 60)
        '''.format(os.path.basename(sys.argv[0])))
        sys.exit(status)

def load_reddit_data(url=URL):
        ''' Load reddit data from specified URL into dictionary '''

        headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}
        response = requests.get(url, headers=headers)
        data = response.json()

        return data

def dump_reddit_data(data, limit=10, orderby='score', titlelen=60, shorten=False):
        ''' Dump reddit data based on specified attributes '''

        children = data['data']['children']
        reverse = False
        if orderby == 'score':
                reverse = True
        children = sorted(children, key=lambda c: c['data'][orderby], reverse=reverse)
        children = children[:limit]

        for index, child in enumerate(children, 1):
                if index != 1:
                        print()
                title = child['data']['title'][:titlelen]
                score = child['data']['score']
                url = child['data']['url']
                if shorten:
                        url = shorten_url(url)
                print('{:4}.\t{} (Score: {})'.format(index, title, score))
                print('\t{}'.format(url))

        pass

def shorten_url(url):
        ''' Shorten URL using yld.me '''
        response = requests.get(ISGD_URL, params={'format': 'json', 'url': url})
        j_data = response.json()
        return j_data['shorturl']

# Parse Command-line Options

args = sys.argv[1:]
if not args:
	      usage(1)

while len(args) and args[0].startswith('-') and len(args[0]) > 1:
        arg = args.pop(0)
        if arg == '-h':
                usage(0)
        elif arg == '-s':
                shorten = True
        elif arg == '-n':
                limit = int(args.pop(0))
        elif arg == '-o':
                orderby = args.pop(0)
        elif arg == '-t':
                titlelen = int(args.pop(0))
        else:
             	usage(1)

if not len(args):

        URL = 'https://www.reddit.com/r/linux/.json'
        SUB = 'linux'

elif '/' in args[0]:

        URL = args.pop(0)
        components = URL.split('/')

        if URL.endswith('/'):
                SUB = components[len(components)-2]
        else:
              	SUB = components[len(components)-1]

else:

      	SUB = args.pop(0)
        URL = 'https://www.reddit.com/r/{}/'.format(SUB)

if not URL.endswith('.json') and not URL.startswith('https://yld.me'):
        URL = URL + '.json'

# Main Execution

data = load_reddit_data(URL)
dump_reddit_data(data, limit, orderby, titlelen, shorten)
