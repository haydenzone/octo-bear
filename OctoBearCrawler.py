import re
import urllib2
from time import time, sleep

class OctoBearCrawler:
    #html_code = "<a href='http://blah.com/'>haha</a> <a href='http://blah.com/'>haha</a><a href='/asdf' href=\"sfad\">"

    #url = 'http://www.python.org/'
    #url = 'http://www.chubbychipmunk.net/'
    #f = urllib2.urlopen(url)
    #html_code = str(f.read())
    #links = {url: False}
    
    def __init__(self, url):
        self.url = url
        self.f = urllib2.urlopen(url)
        self.links = {url: False}
    
    def has_false(self, d):
       return (len(list(filter(lambda x: not x, list(d.values())))) > 0)
       
    def crawl(self):
        while(self.has_false(self.links)): 
           #Find link
           cur_url = ""
           for key in self.links:
              if(not self.links[key]):
                 cur_url = key
                 break
           print("Searching %s"%cur_url)
           opener = urllib2.build_opener()
           #opener.addheaders = [('User-agent', 'Magic Browser')]

           hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
           for key in hdr:
              opener.addheaders = [(key, hdr[key])]
           
           #Do the web request

           #sleep(4)
           #Try 4 times with forbidden the quit
           parse = True
           for i in range(4):
              success = False
              error = ""
              try:
                 #f = urllib2.urlopen(cur_url)
                 self.f = opener.open(cur_url)
                 success = True
              except urllib2.HTTPError as e:
                 #continue
                 success = False
                 error = str(e)
              #print("Error ====> " + error)
              if success:
                 break
              if not success and i == 3:
                 print ("  Giving up...")
                 del(self.links[cur_url])
                 parse = False
                 break
              if not success and error != "HTTP Error 403: FORBIDDEN":
                 print("   HTTPError error: {0}".format(error))
                 del(self.links[cur_url])
                 parse = False
                 break
              if not success:
                 print("   Forbidden: trying again...")
                 sleep(3)
           if not parse:
              continue
           html_code = str(self.f.read())
           for match in re.finditer(r"href=['\"](.*?)['\"]", html_code):
              #print(match.group(1), end=' => ')
              link = match.group(1)
              if link[0] == "#":
                 continue
              if link[-4:] == ".css":
                 continue
              if link[-3:] == ".js":
                 continue
              if link[0] == '/':
                 link = url+link[1:]
              if link[0:7] != "http://":
                 link = url+link
              if link.find(url) == 0:
                 #store
                 if link not in self.links:
                    self.links[link] = False
           self.links[cur_url] = True #Mark as searched

           #print(link)
        print("=============================")
        print("Results")
        print("=============================")

        for key in self.links:
           print(key)
           if(not self.links[key]):
              print("   Error...")

    #>>>match.group(1) text = "He was carefully disguised but captured quickly by police."
    #>>> for m in re.finditer(r"\w+ly", text):
    #...     print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))
