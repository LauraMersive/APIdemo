#Solstice API Demo Script!
#THIS ONLY WORKS WITH PYTHON 2.7.  If you are running 3.6, you will need different commands. 
#This version exposes every command available using GET through /stats or /config, even though some repeat information.
#All calls are exposed here, even those that are Pod or Software specific, so not every value will be populated in the results. 
#This script prints formatted results to console.

#import necessary packages:
import sys
from sys import version
import time
import datetime
import requests

#set value relationships required to properly read all the Boolean results:
true=1
false=0

#Say Hello
print('Solstice API GET Demo Script')
print "............................................................."

#Check that we're running Python 2.7
print 'You are using Python version '+str(sys.version_info[0])+'.'+str(sys.version_info[1])

#Quit if it's not a 2.x version of Python
if sys.version_info[0] != 2:
	print "Must be using Python 2 not Python 3"
	print "Exiting Program"
	quit()
	

#Get the Solstice Device's URL.  For example, http://192.168.3.127 
myurl = raw_input("Enter Target Device URL in http://xxx format: ")

#If you're testing this code against the same device over and over, enter the URL here, uncomment the line, and comment out the "input" line above.
#myurl = "http://192.168.3.227"

print "Target Device:", myurl

#Create the two target URLs for the device without admin password
mystatsurl = myurl+'/api/stats'
myconfigurl = myurl+'/api/config'

#Create the two target URLs for the device with supplied admin password (change the password to the real value)
#admin_password = "Pa$$w0rd"
#mystatsurl = myurl+'/api/stats?password='+admin_password
#myconfigurl = myurl+'/api/config?password='+admin_password

#GET the stats url
print "Getting Stats..."
rs=requests.get(mystatsurl)

#GET the config url
print "Getting Config..."
rc=requests.get(myconfigurl)

#The GET returns a string that we want to use as a dictionary of key:value pairs, so convert results using eval()
rstats=eval(rs.text)
rconfig=eval(rc.text)

print rconfig

##### Stats printed in the order shown in the API User Guide #####
print "--------STATS--------"

#m_displayId: unique identifier Solstice assigns to a single instance, independent of user factors
#Returns long string with numbers and letters
print "Display ID:", rstats.get('m_displayId')

#m_serverVersion: current software version
#Returns string in format x.x.x
print "Server Version:", rstats.get('m_serverVersion')

###m_displayInformation group key

#m_displayName: current device display name
#Returns string
print "Display Name:", rstats.get('m_displayInformation',{}).get('m_displayName')

#m_productName: name of software
#Returns "Solstice" in most cases
print "Product Name:", rstats.get('m_displayInformation',{}).get('m_productName')

#m_productVariant: POD ONLY parameter that returns generation and type of Pod
#Returns string like "Pod Gen2"
print "Product Variant:", rstats.get('m_displayInformation',{}).get('m_productVariant')

#m_productHardwareVersion: POD ONLY paramenter returns variant information in integer format
#Returns int 
hardwareversion = rstats.get('m_displayInformation',{}).get('m_productHardwareVersion')
print "Hardware Version:", hardwareversion

###m_statistics group key

#m_currentPostCount: total number of content pieces (posts) shared to the display.  This counts posts whether actively shared, in a stack, or in the 'On Deck' side panel.
#Returns int
print "Current Post Count:", rstats.get('m_statistics',{}).get('m_currentPostCount')

#m_currentBandwith: Yes, this is a typo.  I don't want to talk about it.  
#Returns int with units Mbps.  May be 0 if display is unused or if current content is inactive. 
print "Current Bandwidth:", rstats.get('m_statistics',{}).get('m_currentBandwith')

#m_connectedUsers: number of users currently connected to the display
#Returns int
print "Connected Users:", rstats.get('m_statistics',{}).get('m_connectedUsers')

#m_timeSinceLastConnectionInitialize: time (in ms) since a connection was last established.  Counts whether or not someone is currently connected.
#Returns int that might be long since we count in milliseconds
print "Time Since Last Init (ms)", rstats.get('m_statistics',{}).get('m_timeSinceLastConnectionInitialize')

#NOT A COMMAND - just converting the time above into hh:mm:ss to make it more human readable
millis=int(rstats.get('m_statistics',{}).get('m_timeSinceLastConnectionInitialize'))
seconds=(millis/1000)%60
seconds = int(seconds)
minutes=(millis/(1000*60))%60
minutes = int(minutes)
hours=(millis/(1000*60*60))
print "Time Since Last Init (hhhh:mm:ss):","%04d:%02d:%02d" % (hours, minutes, seconds)

#m_currentLiveSourceCount: number of current live sources such as an external video camera.  
#Returns int
print "Current Live Sources:", rstats.get('m_statistics',{}).get('m_currentLiveSourceCount')


##### Config printed in the order shown in the API User Guide #####
print "--------CONFIG--------"

#Duplicates information from /api/stats
#m_displayId: unique identifier Solstice assigns to a single instance, independent of user factors
#Returns long string with numbers and letters
print "Display ID:", rconfig.get('m_displayId')

#Duplicates information from /api/stats
#m_serverVersion: current software version
#Returns string in format x.x.x
print "Server Version:", rconfig.get('m_serverVersion')

#Duplicates information from /api/stats
#m_productName: name of software
#Returns "Solstice" in most cases
print "Product Name:", rconfig.get('m_productName')

#Duplicates information from /api/stats
#m_productVariant: POD ONLY parameter that returns generation and type of Pod
#Returns string like "Pod Gen2"
print "Product Variant:", rconfig.get('m_productVariant')

#Duplicates information from /api/stats
#m_productHardwareVersion: POD ONLY paramenter returns variant information in integer format
#Returns int 
print "Hardware Version:", rconfig.get('m_productHardwareVersion')

###m_displayInformation group key

#Duplicates information from /api/stats
#m_ipv4: get the current IP (v4) address assigned to device
#Returns string in IP address format, such as 192.168.3.127
print "IPv4 Address:", rconfig.get('m_displayInformation',{}).get('m_ipv4')

#Duplicates information from /api/stats
#m_displayName: current device display name
#Returns string
print "Display Name:", rconfig.get('m_displayInformation',{}).get('m_displayName')

#m_hostName: host device's current host name (deprecated).
#Returns string containing the OS and device identifier
print "Host Name:", rconfig.get('m_displayInformation',{}).get('m_hostName')

#m_port: base port that will be used for TCP/IP.  Solstice uses base, base+1, and base+2. 
#Returns int value of base port.  
print "Base Port:", rconfig.get('m_displayInformation',{}).get('m_port')

###m_generalCuration group key

#language: language setting for device. Current options are US English and Japanese
#Returns string like "en_US" or "xx"
print "Language:", rconfig.get('m_generalCuration',{}).get('language')

#showSplashScreen: show (1) or hide (0) splash screen background image when splash screen is up
#Returns boolean value
print "Splash Screen Visible:", rconfig.get('m_generalCuration',{}).get('showSplashScreen')

#localConfigEnabled: enable (1) or disable (0) the configuration panel visible to users on the Solstice host, accessible via USB keyboard/mouse
#Returns boolean value
print "Local Configuration Enabled:", rconfig.get('m_generalCuration',{}).get('localConfigEnabled')

#browserConfigEnabled:  enable (1) or disable (0) configuration through the browser, accessible at the bottom of the connection screen
#Returns boolean value
print "Browser Configuration Enabled:", rconfig.get('m_generalCuration',{}).get('browserConfigEnabled')

#autoConnectOnClientLaunch: enables (1) or disables (0) use of cookies to track if a user has already downloaded the client.
#Returns boolean value
print "Auto Client Launch Enabled:", rconfig.get('m_generalCuration',{}).get('autoConnectOnClientLaunch')

#hideOnLastClientDisconnect: WINDOWS ONLY - enable (1) or disable (0) hiding the Solstice window when no one is connected.
#Returns a boolean value
print "Hide if No Connections:", rconfig.get('m_generalCuration',{}).get('hideOnLastClientDisconnect')

#launchOnClientConnect: WINDOWS ONLY - enable (1) or disable (0) bringing Solstice to foreground when someone connects
#Returns boolean value 
print "Bring to Foreground on Connection:", rconfig.get('m_generalCuration',{}).get('launchOnClientConnect')

#launchOnSystemStart: WINDOWS ONLY - enable (1) or disable (0) launching Solstice when host computer boots
#Returns boolean value
print "Launch on Host Boot:", rconfig.get('m_generalCuration',{}).get('launchOnSystemStart')

#theme: WINDOWS ONLY - WINDOWS ONLY select a background color scheme using a value 1-6
#Returns an integer 0 thru 5
print "Theme Number:", rconfig.get('m_generalCuration',{}).get('theme')

#advancedRenderingEnabled: WINDOWS ONLY - enable (1) or disable (0) advanced rendering for better animations at the expense of host PC processing cycles
#Returns boolean value
print "Advanced Rendering Enabled:", rconfig.get('m_generalCuration',{}).get('advancedRenderingEnabled')

#windowMode: WINDOWS ONLY - whether Solstice is displayed as window app (0), fixed size (1) , or fullscreen (2)
#Returns int 0, 1, or 2
print "Window Mode:", rconfig.get('m_generalCuration',{}).get('autoConnectOnClientLaunch')

#NOT A COMMAND - just printing a useful value from values 0-2 above
winmode = rconfig.get('m_generalCuration',{}).get('autoConnectOnClientLaunch')
if winmode == 0:
	print "Window Mode: Window Application"
if winmode == 1:
	print "Window Mode: Fixed Size"
if winmode == 2:
	print "Window Mode: Fullscreen"

#windowLeft: WINDOWS ONLY - if winmode = 1, this is the left coordinate for the fixed window 
#Returns int
print "Window Left:", rconfig.get('m_generalCuration',{}).get('windowLeft')

#windowTop: WINDOWS ONLY - if winmode = 1, this is the top coordinate for the fixed window 
#Returns int
print "Window Top:", rconfig.get('m_generalCuration',{}).get('windowTop')

#windowWidth: WINDOWS ONLY - if winmode = 1, this is the fixed window width in pixels
#Returns int
print "Window Width:", rconfig.get('m_generalCuration',{}).get('windowWidth')
	
#windowHeight: WINDOWS ONLY - if winmode = 1, this is the fixed window height in pixels
#Returns int
print "Window Height:", rconfig.get('m_generalCuration',{}).get('windowHeight')

###m_authenticationCuration group key

#authenticationMode: Pre-3.0 ONLY - sets security on host to open (0), screen key (1), password (2), moderated (3), or select at runtime (4)
#Returns int 0-4
print "Authentication Mode:", rconfig.get('m_authenticationCuration',{}).get('authenticationMode')

#screenKeyEnabled: 3.0+ ONLY - enable (1) or disable (0) screen key
#Returns boolean value
print "Screen Key Enabled:", rconfig.get('m_authenticationCuration',{}).get('screenKeyEnabled')

#moderatorApprovalDisabled: 3.0+ ONLY - enable (1) or disable (0) moderator moderated
#Returns boolean value
print "Moderator Mode Enabled:", rconfig.get('m_authenticationCuration',{}).get('moderatorApprovalDisabled')

#sessionKey: shows current 4-character key needed to access host
#Returns string of 4 characters
print "Screen Key:", rconfig.get('m_authenticationCuration',{}).get('sessionKey')

###m_networkCuration group key

#connectionShowFlags: consolidated way to set/read display information.
'''
Bit 1: Display Name on splash screen
Bit 2: ?
Bit 3: IP Address on splash screen
Bit 4: Display name on presence bar
Bit 5: IP Address on presense bar
Bit 6: Screen key on splash screen
Bit 7: Screen key on presence bar
Bit 8: App instructions box
Bit 9: App instructions image
Bit 10: web instructions box
Bit 11: Web instructions image
Bit 12: SSID on splash screen
'''
#Returns as 12 bit string, or possibly just 32 "1" s.  
flags = rconfig.get('m_networkCuration',{}).get('connectionShowFlags')
print "Flags:","{0:b}".format(flags) 

#discoveryBroadcastEnabled: enable (1) or disable (0) UDP discovery broadcast
#Returns boolean value
print "Broadcast Enabled:", rconfig.get('m_networkCuration',{}).get('discoveryBroadcastEnabled')

#publishToNameServer: publish display information to Solstice Discovery Service (SDS)
#Returns boolean value
print "Publish to SDS:", rconfig.get('m_networkCuration',{}).get('publishToNameServer')

#maximumConnections: number of allowable simultaneous connections.  May not be set larger than license allows.
#Returns integer
print "Maximum Connections:", rconfig.get('m_networkCuration',{}).get('maximumConnections')

#maximumLicensedConnections: number of license allowable connections.
#Returns int.  If license allows for unlimited connections, 32 bits of "1"s will display (int: 4294967295)
print "Maximum Connections Allowed by License:", rconfig.get('m_networkCuration',{}).get('maximumLicensedConnections')

#maximumImageSize: max size of an image that will not get automatically resized
#Returns int in units "bytes"
#print "Maximum Image Size (B):", (rconfig.get('m_networkCuration',{}).get('maximumImageSize')
#Modified to return in kB:
print "Maximum Image Size (kB):", ((rconfig.get('m_networkCuration',{}).get('maximumImageSize'))/1000)

#maximumPublished: max number of posts allowed on the display
#Returns int
print "Maximum Number of Posts:", rconfig.get('m_networkCuration',{}).get('maximumPublished')

#maximumAirplayUsers: max number of simultaneous Airplay (iOS mirroring) users allowed
#Returns int
print "Maximum AirPlay Users:", rconfig.get('m_networkCuration',{}).get('maximumAirPlayUsers')

#sdsHostName: IP Address or Host name of device running SDS for this device
#Returns string
print "SDS Host 1:", rconfig.get('m_networkCuration',{}).get('sdsHostName')

#sdsHostName: IP Address or Host name of device running SDS for this device
#Returns string
print "SDS Host 2:", rconfig.get('m_networkCuration',{}).get('sdsHostName2')

#remoteViewMode: enable (1) or disable (0) browser look-in features
#Returns int
print "Browser Look-in Enabled:", rconfig.get('m_networkCuration',{}).get('remoteViewMode')

#firewallMode: enable (1) or disable (0) internet traffice between network interfaces in dual-network moderated
#Returns boolean value.  0 = All traffic blocked; 1 = allow ports 80/443
print "Firewall Mode Enabled:", rconfig.get('m_networkCuration',{}).get('firewallMode')

#postTypeDesktopSupported: enable (1) or disable (0) PC/desktop full screen sharing
#Returns bool
print "Full Screen Sharing Enabled:", rconfig.get('m_networkCuration',{}).get('postTypeDesktopSupported')

#postTypeApplicationWindowSupported: enable (1) or disable (0) app window sharing
#Returns bool
print "App Window Sharing Enabled:", rconfig.get('m_networkCuration',{}).get('postTypeDesktopSupported')

#postTypeMediaFilesSupported: enable (1) or disable (0) media file sharing
#Returns bool
print "Media File Sharing Enabled:", rconfig.get('m_networkCuration',{}).get('postTypeMediaFilesSupported')

#postTypeAirPlaySupported: enable (1) or disable (0) iOS mirroring via AirPlay
#Returns bool
print "AirPlay Posts Enabled:", rconfig.get('m_networkCuration',{}).get('postTypeAirPlaySupported')

#postTypeAndroidMirroringSupported: enable (1) or disable (0) Android mirroring
#Returns bool
print "Android Posts Enabled:", rconfig.get('m_networkCuration',{}).get('postTypeAndroidMirroringSupported')

#bonjourProxyEnabled: enable (1) or disable (0) the Solstice Bonjour Proxy feature
#Returns bool
print "Bonjour Proxy Enabled:", rconfig.get('m_networkCuration',{}).get('bonjourProxyEnabled')

#encryptClientServerCom: enable (1) or disable (0) network traffic encryption
#Returns bool
print "Network Encryption Enabled:", rconfig.get('m_networkCuration',{}).get('encryptClientServerCom')

#ethernetEnabled: POD ONLY - enable (1) or disable (0) ethernet network adapter
#returns bool
print "Ethernet Enabled:", rconfig.get('m_networkCuration',{}).get('ethernetEnabled')

#wifiMode: POD ONLY - set wireless adapter mode to off (0), attach to existing network (1), or WAP (2)
#returns int 0, 1, or 2
#print "WiFi Mode:", (rconfig.get('m_networkCuration',{}).get('wifiMode')
wifiMode = rconfig.get('m_networkCuration',{}).get('wifiMode')
if wifiMode == 0:
	print "WiFi Mode: Off"
if wifiMode == 1:
	print "WiFi Mode: Client Mode"
if wifiMode == 2:
	print "WiFi Mode: WAP"
	
#bulletinEnabled: enables (1) or disables (0) 
#returns bool
print "Bulletin Enabled:", rconfig.get('m_networkCuration',{}).get('bulletinEnabled')

#bulletinText: displays text of bulletin if enabled
#returns bool
print "Bulletin Text:", rconfig.get('m_networkCuration',{}).get('bulletinText')

##wifiConfig subgroup key

#ssid: POD ONLY - SSID of host wireless network when WiFi mode  = client
#Returns string
print "SSID:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('ssid')

#security: POD ONLY - security protocol of wireless network.  Options are open (0), WEP (1) , WPA (2), WPA2 (3) and EAP (4)
#Returns string
#print "Network Security:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('security')
nsec = rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('security')
if nsec == 0:
	print "Network Security: Open"
if nsec == 1:
	print "Network Security: WEP"
if nsec == 2:
	print "Network Security: WPA"
if nsec == 3:
	print "Network Security: WPA2"
if nsec == 4:
	print "Network Security: EAP"

#eap: POD ONLY - Mode of authentication if in EAP mode.  None (0), PEAP (1), TLS (2), TTLS (3), PWD (4), SIM (5), or SIM (6) 
#returns int 0-6
#print "EAP Security Mode:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('eap')
eapsec = rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('eap')
if eapsec == 0:
	print "EAP Security Mode: No EAP"
if eapsec == 1:
	print "EAP Security Mode: PEAP"
if eapsec == 2:
	print "EAP Security Mode: TLS"
if eapsec == 3:
	print "EAP Security Mode: TTLS"
if eapsec == 4:
	print "EAP Security Mode: PWD"
if eapsec == 5:
	print "EAP Security Mode: SIM"
if eapsec == 6:
	print "EAP Security Mode: SIM"

#phase2: POD ONLY - method of phase2 authentication.  None (0), PAP (1), MSCHAP (2), MSCHAPv2 (3), GTC (4).
#returns int 0-4
#print "Phase2 Authentication", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('phase2')
p2 = rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('phase2')
if p2 == 0:
	print "Phase2 Authentication: No Phase2"
if p2 == 1:
	print "Phase2 Authentication: PAP"
if p2 == 2:
	print "Phase2 Authentication: MSCHAP"
if p2 == 3:
	print "Phase2 Authentication: MSCHAPv2"
if p2 == 4:
	print "Phase2 Authentication: GTC"
	
#password: POD ONLY - Host network password
#returns string (GET returns "*" if set, not the actual password)
print "Host Network Password:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('password')

#dhcp: POD ONLY - enable (1) or disable (0) DHCP protocol on wireless interfaces
#returns bool
print "Wireless DHCP Enabled:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('dhcp')

#staticIP: POD ONLY - the static IP address assigned to a network device
#returns string
print "Wireless Static IP Address:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('staticIP')

#gateway: POD ONLY - address or name of gateway, if used
#returns string, commonly an IP address
print "Wireless Gateway Address:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('gateway')

#prefixLength:POD ONLY - prefix setting for wireless interfaces (commonly 24 for xxx.xxx.x.xxx style since the bitwise mask would need 24 bits)
#returns integer
print "Wireless Prefix Length:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('prefixLength')

#dns1: POD ONLY - First DNS for wireless interfaces (if set)
#returns string  
print "Wireless DNS1:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('dns1')

#dns2: POD ONLY - Second DNS for wireless interfaces (if set)
#returns string 
print "Wireless DNS2:", rconfig.get('m_networkCuration',{}).get('wifiConfig',{}).get('dns2')

##apConfig subgroup key

#SSID: POD ONLY - SSID for WAP
#returns string
print "WAP SSID:", rconfig.get('m_networkCuration',{}).get('apConfig',{}).get('SSID')

#SecurityMode: POD ONLY - security protocol when in WAP mode.  Open (0) or WPA2 (3). 
#Returns int 0 or 3
#print "WAP Security Mode:", rconfig.get('m_networkCuration',{}).get('apConfig',{}).get('SecurityMode')
wapsec = rconfig.get('m_networkCuration',{}).get('apConfig',{}).get('SecurityMode')
if wapsec == 0:
	print "WAP Security Mode: Open"
if wapsec == 3:
	print "WAP Security Mode: WPA2"

#PSK: POD ONLY - WAP authentication password
#returns string
print "WAP Password:", rconfig.get('m_networkCuration',{}).get('apConfig',{}).get('PSK')

##ethernet subgroup key 

#dhcp: POD ONLY - enable (1) or disable (0) DHCP protocol on wired interfaces.  Even if ethernet is disabled but the DHCP radio button is checked, this will return true. 
#returns bool
print "Wired DHCP Enabled:", rconfig.get('m_networkCuration',{}).get('ethernet',{}).get('dhcp')

#staticIP: POD ONLY - the static IP address assigned to a network device
#returns string
print "Wired Static IP Address:", rconfig.get('m_networkCuration',{}).get('ethernet',{}).get('staticIP')

#gateway: POD ONLY - address or name of gateway, if used
#returns string
print "Wired Gateway Address:", rconfig.get('m_networkCuration',{}).get('ethernet',{}).get('gateway')

#prefixLength:POD ONLY - prefix setting for wired interfaces (commonly 24 for xxx.xxx.x.xxx style since the bitwise mask would need 24 bits)
#returns integer
print "Wired Prefix Length:", rconfig.get('m_networkCuration',{}).get('ethernet',{}).get('prefixLength')

#dns1: POD ONLY - First DNS for wired interfaces (if set)
#returns string  
print "Wired DNS1:", rconfig.get('m_networkCuration',{}).get('ethernet',{}).get('dns1')

#dns2: POD ONLY - Second DNS for wired interfaces (if set)
#returns string 
print "Wired DNS2:", rconfig.get('m_networkCuration',{}).get('ethernet',{}).get('dns2')

##httpProxyServerSettings subgroup key

#enabled: enable (1) or disable (0) HTTP proxy
#returns bool
print "HTTP Enabled:", rconfig.get('m_networkCuration',{}).get('httpProxyServerSettings',{}).get('enabled')

#ip: IP address of HTTP proxy
#returns string
print "HTTP Proxy Server:", rconfig.get('m_networkCuration',{}).get('httpProxyServerSettings',{}).get('ip')

#port: HTTP proxy communication port. Will return "0" if HTTP proxy not enabled.
#returns int.  
print "HTTP Communication Port:", rconfig.get('m_networkCuration',{}).get('httpProxyServerSettings',{}).get('port')

#username: HTTP Proxy authentication username
#returns string
print "HTTP Username:", rconfig.get('m_networkCuration',{}).get('httpProxyServerSettings',{}).get('username')

#password: HTTP Proxy authentication password
#returns string
print "HTTP Password:", rconfig.get('m_networkCuration',{}).get('httpProxyServerSettings',{}).get('password')

##httpsProxyServerSettings subgroup key

#enabled: enable (1) or disable (0) HTTPS proxy
#returns bool
print "HTTPS Enabled:", rconfig.get('m_networkCuration',{}).get('httpsProxyServerSettings',{}).get('enabled')

#ip: IP address of HTTPS proxy
#returns string
print "HTTPS Proxy Server:", rconfig.get('m_networkCuration',{}).get('httpsProxyServerSettings',{}).get('ip')

#port: HTTP proxy communication port. Will return "0" if HTTP proxy not enabled.
#returns int.  
print "HTTPS Communication Port:", rconfig.get('m_networkCuration',{}).get('httpsProxyServerSettings',{}).get('port')

#username: HTTP Proxy authentication username
#returns string
print "HTTPS Username:", rconfig.get('m_networkCuration',{}).get('httpsProxyServerSettings',{}).get('username')

#password: HTTP Proxy authentication password
#returns string
print "HTTPS Password:", rconfig.get('m_networkCuration',{}).get('httpsProxyServerSettings',{}).get('password')

###m_licenseCuration group key

#licenseStatus: an integer representation of your license status 
#returns int
print "License Status:", rconfig.get('m_licenseCuration',{}).get('licenseStatus')

#trustFlags: 
#returns
print "Trust Flags:", rconfig.get('m_licenseCuration',{}).get('trustFlags')

#fulfillmentType: 
#returns
print "Fulfillment Type:", rconfig.get('m_licenseCuration',{}).get('fulfillmentType')

#enabled: 
#returns
print "Enabled:", rconfig.get('m_licenseCuration',{}).get('enabled')

#fulfillmentId
#returns
print "Fulfillment ID:", rconfig.get('m_licenseCuration',{}).get('fulfillmentId')

#entitlementId: 
#returns
print "Entitlement ID:", rconfig.get('m_licenseCuration',{}).get('entitlementId')

#productId: 
#returns
print "Product ID:", rconfig.get('m_licenseCuration',{}).get('productId')

#suiteId: 
#returns
print "Suite ID:", rconfig.get('m_licenseCuration',{}).get('suiteId')

#expirationDate: 
#returns
print "Expiration Date:", rconfig.get('m_licenseCuration',{}).get('expirationDate')

#featureLine: 
#returns
print "Feature Line:", rconfig.get('m_licenseCuration',{}).get('featureLine')

#numDaysToExpiration:
#returns
print "Days to Expiration:", rconfig.get('m_licenseCuration',{}).get('numDaysToExpiration')

#maxUsers:
#returns
print "Maximum Users:", rconfig.get('m_licenseCuration',{}).get('maxUsers')

#licensing_maxPosts
#returns 
print "Maximum Licensed Posts:", rconfig.get('m_licenseCuration',{}).get('licensing_maxPosts')

#licensing_maxPostsIsConfigurable
#returns 
print "Maximum Licensed Posts Configurable:", rconfig.get('m_licenseCuration',{}).get('licensing_maxPostsIsConfigurable')

#licensing_atMaxPostsReplace
#returns 
print "Maximum Licensed Posts Replace:", rconfig.get('m_licenseCuration',{}).get('licensing_atMaxPostsReplace')

#licensing_maxUsers
#returns 
print "Maximum Licensed Users:", rconfig.get('m_licenseCuration',{}).get('licensing_maxUsers')

#licensing_maxUsersIsConfigurable
#returns 
print "Maximum Licensed Users Configurable:", rconfig.get('m_licenseCuration',{}).get('licensing_maxUsersIsConfigurable')

#licensing_remoteViewEnabled
#returns 
print "License Remote View Enabled:", rconfig.get('m_licenseCuration',{}).get('licensing_remoteViewEnabled')

#licensing_remoteViewIsConfigurable
#returns 
print "License Remote View Enable Configurable:", rconfig.get('m_licenseCuration',{}).get('licensing_remoteViewIsConfigurable')

#licensing_runtimeAccessControls
#returns 
print "License Runtime Access Controls Enabled:", rconfig.get('m_licenseCuration',{}).get('licensing_runtimeAccessControls')

###m_userGroupCuration group key

#adminPassword: host admin password.  "get" will always return "<unknown>" whether or not an admin password is set.
#returns "<unknown>" 
print "Admin Password:", rconfig.get('m_userGroupCuration',{}).get('adminPassword')

#presenterPasswordLength: pre-3.0 only.  Returns length in characters of moderator password
#returns int.  Returns "0" if not set/enabled.
print "Presenter Password Length:", rconfig.get('m_userGroupCuration',{}).get('presenterPasswordLength')

#presenterPassword: pre-3.0 only.  Moderator password.  "get" will return "<unknown>" if password is set.  
#returns "<unknown>" if set or nothing if not. 
print "Presenter Password:", rconfig.get('m_userGroupCuration',{}).get('presenterPassword')

#passwordValidationEnabled: 3.0+ only.  Enables (1) or disables (0) admin password validation rules.  
#returns bool
print "Password Validation Enabled:", rconfig.get('m_userGroupCuration',{}).get('passwordValidationEnabled')

###m_systemCuration group key

#autoDateTime: POD ONLY - enable (1) or disable (0) use of standard NTP time server.  
#returns bool
print "Auto Date/Time Enabled:", rconfig.get('m_systemCuration',{}).get('autoDateTime')

#ntpServer: POD ONLY - address of non-standard NTP time server.  
#returns string
print "Non-default NTP Server:", rconfig.get('m_systemCuration',{}).get('ntpServer')

#dateTime: POD ONLY - time in ms since 1/1/1970
#returns 64-bit int
#print "Total Epoch Time:", rconfig.get('m_systemCuration',{}).get('dateTime')
#convert epoch time to datetime in mm/dd/yy 24hr:mm:ss format
totaltime = rconfig.get('m_systemCuration',{}).get('dateTime')

#since the software won't return a time, we can only show this value in date form for pods. 
if hardwareversion == 9999:
	print "Total Time:",totaltime
else:
	print "Current Date and Time:", datetime.datetime.fromtimestamp((totaltime/1000)).strftime('%c')
print "\n"

#Shut it down (on your own terms, if running the program directly) 
end = raw_input("Press any key to exit")
