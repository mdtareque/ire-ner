import httplib2
import urllib2
import os 
import BeautifulSoup

http = httplib2.Http(proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, 'proxy.iiit.ac.in', 8080))
status, response = http.request('http://web.informatik.uni-mannheim.de/DBpediaAsTables/DBpediaClasses.htm')

all_links=[]
soup = BeautifulSoup.BeautifulSoup(response)
for a in soup.findAll('a', href=True):
	if '.csv.gz' in a['href']:
		all_links.append(a['href'])

print all_links[0]
proxy_handler = urllib2.ProxyHandler({'http': 'http://proxy.iiit.ac.in:8080/'})

opener = urllib2.build_opener(proxy_handler)
for i in xrange(len(all_links)):
	txt=opener.open(all_links[0])
	with open(all_links[0].split("/")[-1],"w") as f:
		f.write(txt.read())
#opener.urlretrieve(all_links[0], "./"+all_links[0].split("/")[-1],proxy={'http': 'http://proxy.iiit.ac.in:8080'})
