#!/usr/bin/env python3

import feedparser
import os
import re
import requests
import time
import urllib

feed_url = 'http://fudder.de/index.html.rss'
feed_file = 'feed.rss'

def get_url(url, file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return f.read()
    print(f'fetching {url} ...')
    time.sleep(1)
    r = requests.get(url, allow_redirects=True)
    with open(file_name, 'w') as f:
        f.write(r.text)
    return r.text

feed_data = get_url(feed_url, feed_file)
feed = feedparser.parse(feed_data)
for entry in feed.entries:
    entry_id = re.sub('[^0-9a-zA-Z]+', '_', entry['id'])
    entry_url = entry['link']
    entry_file = f'entry_{entry_id}.html'
    entry_data = get_url(entry_url, entry_file)
    for line in entry_data.split('\n'):
        if 'gewinnen@fudder.de' in line:
            print(line)
