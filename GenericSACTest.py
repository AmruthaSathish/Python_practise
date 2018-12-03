import requests
import time
import json
from HTMLParser import HTMLParser

def postsacdata(sacconfig) :
	print "Inside SAC"
	posturl_config = "http://192.168.43.1/goform/HandleSACConfiguration"
	
	postconfig = requests.post(posturl_config,data=sacconfig)
	sacstatus = (postconfig.content).strip()	
	if (postconfig.status_code == 200 ) :
		print sacstatus				
	else :
		print "Could not POst SAC . Configuration failed"	 
			
	return
def getscanresult() :
	parser = HTMLParser()
	url = "http://192.168.43.1/scanresult.asp"
	start = float(time.time())
	scanresults = requests.get(url)
	roundtrip = float(time.time()) - start
	print "Response Time %f"%roundtrip
	#scanresults = requests.get(geturl_scanlist,verify=False)
	if (scanresults.status_code == 200 ) :
		results = json.loads((scanresults.content).strip())
		scanlistvalues = results["Items"]
		indexval = 0
		print "Got Scan Results :"
		tempjoin = "" 
		for i in range(len(scanlistvalues)):     
			#print(newdict[indexval])    
			#print(newdict[indexval]) 
			tempjoin = ""   
			for key, value in (scanlistvalues[indexval]).iteritems() :
				#print key, parser.unescape(value)
				tempjoin += key +" : "+ parser.unescape(value)+"$\n"
			reverselist =  tempjoin.split('$')
			reverselist = reverselist[:-1]
			finallist = ""
			for i in reversed(reverselist):
  			  	finallist += i + " "
    	#print i
			print finallist
				#print key, parser.unescape(value)
			
			indexval += 1
		print "------------------------------------------------------------------------"
		#print "Got Scan Results : %s "%scanresults.content
		#parsescanresult(scanresults.content)
		#
	else :
		print "Couldn't get the scan resulst\n"
		#exit

def getconnectedstate() :
	geturl_status = "http://192.168.43.1/ConnectedStatus.asp"
	current_stat = requests.get(geturl_status)
	if ((current_stat.content).strip() == "") :
		return "No Connected State"
	return current_stat


def main() :
	sacconfig = {'SSID':"Te Fiti",'Passphrase':"12345678",'Security':"WPA-PSK"}
	connectedstatus = getconnectedstate()
	if (connectedstatus.status_code != 200) :
		print "Couldn't Connect to the server.Error Code %d\n" %connectedstatus.status_code
		exit()
	else :
		print "Status : %s"%connectedstatus.content

	getscanresult() 

	postsacdata(sacconfig)

if __name__ == "__main__":
	main()