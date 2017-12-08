#Solstice API Demo Script
#This version changes the display name of a list of Pods using the /config api URL
#The list of pod IP addresses, name, and other info is stored in a text file named "myIPs.txt". You must make this file.
#The "before" and "after" versions are printed to the console. 

#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import necessary packages:
import sys
import requests
import random
from random import choice
podnum = 0

#set value relationships required to properly read all the Boolean results:
true=1
false=0


#Say Hello
print "###################################################"
print "#  Solstice API Multiple Name Change Demo Script  #"
print "###################################################"

#Check that we're running Python 2.7
print 'You are using Python version '+str(sys.version_info[0])+'.'+str(sys.version_info[1])

#Quit if it's not a 2.x version of Python
if sys.version_info[0] != 2:
	print "Must be using Python 2 not Python 3"
	print "Exiting Program"
	quit()

#Pull in the text file with the IP addresses and build array named "IParray"
with open("myIPs.txt", "r") as f:
    IParray = f.readlines()
#Strip whitespace characters like `\n` from the end of each line
IParray = [x.strip() for x in IParray] 

for i in IParray:
	#print i
	x=0
	params=i.split(",")
	for j in params:
		if x==0:
			print x,"URL:",j
			myurl = j
		elif x==1:
			print x,"Other Info:",j
			myPODname = j
		elif x==2:
			print x,"Time Zone:",j
			mytimezone = j
		else:
			print x,"Tag:",j		
		x +=1
	print "......."

	#create URLs using that IP addresses
	print myurl

	#Convert Time Zone to valid entry
	if mytimezone == "Eastern":
			mytimezone = "America/New_York"
	elif mytimezone == "Central":
			mytimezone = "America/Chicago"
	elif mytimezone == "Mountain":
			mytimezone = "America/Denver"
	elif mytimezone == "Pacific":
			mytimezone = "America/Los_Angeles"
	elif mytimezone == "Alaska":
			mytimezone = "America/Anchorage"
	elif mytimezone == "Hawaii":
			mytimezone = "Pacific/Honolulu"

	#Define SDS and Time Server IP's
	mysdsone = "10.10.10.1"
	mysdstwo = "10.10.10.2"
	mytimeserver = "10.10.10.3"

	#Define Wi-Fi Information - Security protocol of the Pod wireless network (Pod-only).  0=open, 1=WEP, 2=WPA, 3=WPA2, 4=EAP
	myssid = "AccessPoint"
	wifipass = "CPasswordAP"
	securityprot = "3"

	#If you're supplying an Admin password, type it in here and uncomment the URLs that use passwords.  Otherwise, leave it blank as "" 
	old_admin_password = "oldadmin"
	new_admin_password = "newadmin"

	print "Target Device:", myurl
	print "............."

	#Create the two target URLs for the device
	#mystatsurl = 'http://'+myurl+'/api/stats'
	#myconfigurl = 'http://'+myurl+'/api/config'

	#Create the two target URLs for the device with supplied admin password

	mystatsurl = 'http://'+myurl+'/api/stats?password='+old_admin_password
	myconfigurl = 'http://'+myurl+'/api/config?password='+old_admin_password

	#GET the stats url
	rs=requests.get(mystatsurl)

	#GET the config url
	rc=requests.get(myconfigurl)

	#The GET returns a string that we want to use as a dictionary of key:value pairs, so convert results using eval()
	rstats=eval(rs.text)
	rconfig=eval(rc.text)

	#m_displayName: current device display name from the /api/stats URL
	#Returns string
	print "Current Display Name from Stats:", rstats.get('m_displayInformation',{}).get('m_displayName')

	#m_displayName: current device display name from the /api/config URL 
	#Returns string
	print "Current Display Name from Config:", rconfig.get('m_displayInformation',{}).get('m_displayName')
	print "............."
	
	#develop a new name 
	#num = str(podnum)	
	#newname = "Pod Number "+num
	#print newname
	#podnum +=1
	
	#POST the new display name to the /api/config URL 
	r=requests.post(myconfigurl, json={'password':old_admin_password,'m_displayInformation':{'m_displayName':myPODname},"m_generalCuration":{"language":"en_US","showSplashScreen":false,"localConfigEnabled":false,"browserConfigEnabled":false,"autoConnectOnClientLaunch":true},"m_authenticationCuration":{"screenKeyEnabled":true,"moderatorApprovalDisabled":false},"m_networkCuration":{"connectionShowFlags":2648,"discoveryBroadcastEnabled":true,"maximumConnections":10,"maximumLicensedConnections":4294967295,"maximumImageSize":1048576,"maximumPublished":40,"maximumAirPlayUsers":4,"publishToNameServer":true,"sdsHostName":mysdsone,"sdsHostName2":mysdstwo,"remoteViewMode":0,"firewallMode":0,"postTypeDesktopSupported":true,"postTypeApplicationWindowSupported":true,"postTypeMediaFilesSupported":true,"postTypeAirPlaySupported":false,"postTypeAndroidMirroringSupported":true,"bonjourProxyEnabled":false,"wifiMode":1,"wifiConfig":{"ssid":myssid,"security":securityprot,"identity":"","eap":0,"phase2":0,"password":wifipass,"dhcp":true,"staticIP":"","gateway":"","prefixLength":24,"dns1":"","dns2":""},"apConfig":{"SSID":"","SecurityMode":0,"PSK":""},"ethernetEnabled":true,"ethernet":{"dhcp":true,"staticIP":"","gateway":"","prefixLength":24,"dns1":"","dns2":""},"httpProxyServerSettings":{"enabled":false,"ip":"","port":0,"username":"","password":""},"httpsProxyServerSettings":{"enabled":false,"ip":"","port":0,"username":"","password":""},"bulletinEnabled":false,"bulletinText":""},"m_licenseCuration":{"licenseStatus":2,"trustFlags":0,"fulfillmentType":"","enabled":false,"fulfillmentId":"","entitlementId":"","productId":"","suiteId":"","expirationDate":"","featureLine":"","numDaysToExpiration":0,"maxUsers":"Unlimited","licensing_maxPosts":0,"licensing_maxPostsIsConfigurable":true,"licensing_atMaxPostsReplace":false,"licensing_maxUsers":0,"licensing_maxUsersIsConfigurable":true,"licensing_remoteViewEnabled":true,"licensing_remoteViewIsConfigurable":true,"licensing_runtimeAccessControls":true},"m_userGroupCuration":{"adminPassword":new_admin_password,"presenterPasswordLength":0,"presenterPassword":"","passwordValidationEnabled":false},"m_systemCuration":{"autoDateTime":true,"ntpServer":mytimeserver,"timeZone":mytimezone,"l24HourTime":false,"resolution":"Not Supported"}})
	print "Changing Name to: ",myPODname
	print "............."
	
	#create new URLs with new password
	mystatsurl = 'http://'+myurl+'/api/stats?password='+new_admin_password
	myconfigurl = 'http://'+myurl+'/api/config?password='+new_admin_password
	
	#Repeat the GET and formatting seen above
	rs=requests.get(mystatsurl)
	rc=requests.get(myconfigurl)
	rstats=eval(rs.text)
	rconfig=eval(rc.text)

	#Display the new display name, as read from both /api/stats and /api/config
	print "New Display Name from Stats:", rstats.get('m_displayInformation',{}).get('m_displayName')
	print "New Display Name from Config:", rconfig.get('m_displayInformation',{}).get('m_displayName')
	if (rstats.get('m_displayInformation',{}).get('m_displayName')==rconfig.get('m_displayInformation',{}).get('m_displayName') == myPODname):
		print "Name Change Success!"
	else:
		print "Name Change Failure"
	print "............."

#Shut it down (on your own terms, if running the program directly) 
end = raw_input("Press any key to exit")
#done
