import urllib.request
import http.cookiejar
from getpass import getpass
import sys

def sendMessages(number,message):	 
	uname = "9877110677"
	password = "7589"
	message = "+".join(message.split(' '))
	 
	#Logging into the SMS Site
	url_for_wsms = 'http://site24.way2sms.com/Login1.action?'
	data_for_wsms = 'username='+uname+'&password='+password+'&Submit=Sign+in'

	data_for_wsms = data_for_wsms.encode('UTF-8')

	#For Cookies:
	cookie_jar = http.cookiejar.CookieJar()
	cookie_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

	cookie_opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
	 
	try:
	    user_open = cookie_opener.open(url_for_wsms, data_for_wsms)
	except IOError:
	    print("Error while logging in.")
	    sys.exit(1)

	ssionId = str(cookie_jar).split('~')[1].split(' ')[0]
	smsurl = 'http://site24.way2sms.com/smstoss.action?'
	smsdata = 'ssaction=ss&Token='+ssionId+'&mobile='+number+'&message='+message+'&msgLen=136'
	cookie_opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+ssionId)]

	smsdata = smsdata.encode('UTF-8')


	try:
	    sentpage = cookie_opener.open(smsurl,smsdata)
	except IOError:
	    print("Error while sending message")

	sys.exit(1)
	print("SMS has been sent.")

sendMessages("8556833932","this is test message")