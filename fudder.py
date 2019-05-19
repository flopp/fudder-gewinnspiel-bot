import datetime
import feedparser
import os
import re
import requests
import time

class Fudder:
    def __init__(self, user_name, password, data_dir):
        self._user_name = user_name
        self._password = password
        self._data_dir = data_dir
    
    def get_new_gewinnspiele(self):
        feed_data = self.get_feed()
        feed = feedparser.parse(feed_data)
        for entry in feed.entries:
            entry_id = re.sub('[^0-9a-zA-Z]+', '_', entry['id'])
            entry_url = entry['link']
            entry_file = os.path.join(self._data_dir, f'entry_{entry_id}.html')
            if os.path.exists(entry_file):
                continue
            entry_data = self.get_article(entry['link'], entry_file)
            for line in entry_data.split('\n'):
                if 'gewinnen@fudder.de' in line:
                    print(entry['title'])
                    print(entry['published'])
                    print(line)
                    break
    
    def get_cookie(self, force_request=False):
        login_url = 'https://fudder.de/mein-fudder'

        cookie_file = os.path.join(self._data_dir, 'cookie.txt')
        if (not force_request) and os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                return f.read()
    
        s = requests.Session()
        r = s.get(login_url)
        login = re.search(r'<form\s+name="(login[^"]+)"', r.text).group(1)
        csrf_token = re.search(r'name="' + login + r'Csrftoken"\s+value="([^"]+)"', r.text).group(1)
    
        payload = {
            login + 'EingabeLoginsetComplexloginLogin': self._user_name,
            login + 'EingabeLoginsetComplexloginPasswd': self._password,
            login + 'Currentsite': 'eingabe',
            login + 'Csrftoken': csrf_token,
            login + 'Fertig-next': '',
            'coreFormSubmitted': 'user/login'
        }
        s.headers.update({
            'x-requested-with': 'XMLHttpRequest'
        })
        r = s.post(login_url, data=payload)
        cookie = r.cookies['session_cookie']
        with open(cookie_file, 'w') as f:
            f.write(cookie)

        return cookie
    
    def get_feed(self):
        feed_url = 'http://fudder.de/index.html.rss'
        feed_file = os.path.join(self._data_dir, 'feed.rss')
        if os.path.exists(feed_file):
            now = datetime.datetime.now()
            feed_date = datetime.datetime.fromtimestamp(os.path.getmtime(feed_file))
            if (now - feed_date) < datetime.timedelta(minutes=30):
                with open(feed_file, 'r') as f:
                    return f.read()
        return self.get_url(feed_url, feed_file, force_download=True)

    def get_article(self, url, file_name):
        cookie = self.get_cookie()
        text = self.get_url(url, file_name, cookie=cookie)
        if not re.search(r'class="freemium', text):
            return text
        cookie = self.get_cookie(force_request=True)
        return self.get_url(url, file_name, cookie=cookie, force_download=True)

    def get_url(self, url, file_name, cookie=None, force_download=False):
        if (not force_download) and (file_name is not None) and os.path.exists(file_name):
            with open(file_name, 'r') as f:
                return f.read()
        print(f'fetching {url} ...')
        time.sleep(1)
        if cookie:
            r = requests.get(url, allow_redirects=True, cookies={'session_cookie': cookie})
        else:
            r = requests.get(url, allow_redirects=True)
        if file_name is not None:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'w') as f:
                f.write(r.text)
        return r.text
