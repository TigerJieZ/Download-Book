# -*- coding: utf-8 -*-

import urllib2
import urlparse

class Downloader(object):

    def m_download(self,url, user_agent='Mr.Zhang', proxy=None, num_retries=2):
        headers = {'User-agent': user_agent}
        request = urllib2.Request(url, headers=headers)

        opener = urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.parser(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            html = opener.open(request).read()
        except urllib2.URLError as e:
            print('Download error:', e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.m_download(url, user_agent, proxy, num_retries - 1)
        return html