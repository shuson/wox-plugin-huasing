# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://bbs.huasing.org/sForum/'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):
  
    def request(self,url):
	#get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
	    proxies = {
		"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
		"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
	    }
	    return requests.get(url,proxies = proxies)
	return requests.get(url)
			
    def query(self, param):
	r = self.request(URL + "zsbbs.php")
	r.encoding = 'utf-8'
	bs = BeautifulSoup(r.content, 'html.parser')
	posts = bs.find_all('div', 'fake-s')

	result = []
	for p in posts[2:]:
            meta = p.find_all('div')[1].string.split(',')
            title = p.find('div').contents[0]
            
            item = {
                'Title': u'{subject} [{replies}]'.format(subject=full2half(title), replies=meta[3]),
                'SubTitle': u'{forum} | {user} | {time}'.format(forum=meta[0], user=meta[9], time=meta[10].replace('\n', ' ')),
                'IcoPath': os.path.join('img', 'huasing.png'),
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [self.getLink(p['id'])]
                }
            }
            result.append(item)
        
	return result

    def getLink(self, str_id):
        return URL + 'bbs.php?B=' + str_id[2:].replace ("-", "_")
    
    def open_url(self, url):
	webbrowser.open(url)

if __name__ == '__main__':
    Main()
