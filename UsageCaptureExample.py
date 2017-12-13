#
# UsageCaptureExample.py
#
# Solstice Usage Capture 
#
# An OpenControl Protocol Example.
#
# This application monitors a Solstice Pod deployment for a given amount of time and
# saves connection count information for each Pod to a comma-separated datafile that can easilly be imported
# into Excel or another tool to visualize usage statistics over time.
#
# Usage:   solsticeUsageCapture <Solstice Host File> <OutputFile (comma separated)> [-time] <time in seconds>
#
# The arguments are:
#
# <hostFile.txt>:  A textfile that contains, on each line, a display name and it's corresponding IPAddress.  This file 
#   contains the set of Solstice Hosts that will be monitored.
#
# <outputFile.txt>: The resulting output textfile.  This file will be written throughout the monitoring process and closed 
#   when the program terminates.  The format of this file is a CSV where each line contains the number of users connected
#   at the sample for each host.
#
# <Time (in seconds!) to monitor the program>
#
# This application uses the OpenControl protocol to establish a connection and download utilization information.
#
# (c) Mersive Technologies, 2016
#
# Author: Christopher Jaynes
# 	  CTO & Founder, Mersive
#

# --------------- LICENSE -MIT Open Source -----------------------------------------------
#Copyright (c) 2016 >Mersive
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions 
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# -------------------------------------------------------------------------------


import argparse	
import sys
import urllib
import time
import os

import urllib2

# Solstice OpenControl is based on JSON records, you can parse by hand or use existing libraries (like I do here)
# Make sure you take a look at the OpenControl protocol documentation to see what other capabilties it provides.
# You can download from here:
# https://mersive.com/solstice-opencontrol-api/
#
# 
import json


#
# I use the argparse library to quickly parse the command line for arguments and marshall them into each component
#
argumentParser = argparse.ArgumentParser(description='Solstice Usage Capture, Command Line Arguments.')
argumentParser.add_argument('HostFile', metavar='<hostfile.txt>', type=str, help='Solstice Host Text File: [Name] [IPAddr] [Port] per line')
argumentParser.add_argument('OutputFile', metavar='<outputFile.txt>', type=str, help='Output File for Usage Data')
argumentParser.add_argument('Time', metavar='<Time in Minutes>', type=int, help='Length of Capture in Minutes')

gHostConnectionInfo = []
gHostCount = 0

#
# This variable defines how often to poll user count for all hosts in the hostFile.txt file

gSampleIntervalInSeconds = 5

#
# OpenControl users several different URLs based on the type of information you are reading/writing (control, stats, config)
# This program will be reading statistics information (users connected), so we will be using the "stats" URL 
#
gSolstice_Stats_URL = "/api/stats"



#
#
# DEFINE loadHostFile.  A simple function to load a text file with hostname and IPAddr and load each line to the the
# gHostConnectionInfo array for processing later.
#
def loadHostFile(aHostFile):

	whiteSpaceRegEx = "\\s"

	#
	# First test if the file exists, then open and read until no more data exists.
	# 
	if (os.path.isfile(aHostFile)) :
		with open(aHostFile, 'r') as file:
			index = 0
			for line in file:
				gHostConnectionInfo.append(line.split())
				index = index+1

		return index
	else:
		print(aHostFile+" does not appear to exist or cannot be opened.")
		exit()
	

#
#
# DEFINE getUserCountFromHost.  Given an IPAddress, poll the number of users currently connected at that Solstice IPAddress.
#	If there is a problem (i.e. there is no Solstice host at that IPAddress, or it cannot be reached, set to zero.
#
def getUserCountFromHost( aIPAddr ):

	# This function users the url2lib for processing communicating to the socket and waiting on a response.  
	#
	# NOTE: This example assumes that the admin password is not set for all the endpoints.  If the admin password 
	# has been set.  The OpenControl protocol will use https and not http as shown below.  Additionally
 	# the urlStr would have to be appended with "?password=<your admin password>" so that the current admin password is
	# transmitted as an argument to the Solstice Host as part of the URL get request.

	urlStr = "http://"+aIPAddr+gSolstice_Stats_URL


	try:
		urlRequestResult = urllib2.urlopen( urlStr , timeout=1 )
	except urllib2.URLError, e:
		return(0)

	hostValuesStr = urlRequestResult.read()


	statsTopLevelRecord = json.loads( hostValuesStr );
	##
	## Parse out the Statistics SubRecord and Return User Count
	##
	if 'm_statistics' in statsTopLevelRecord:
		displayInformation = statsTopLevelRecord[ 'm_statistics' ]
		return( displayInformation['m_connectedUsers'] )
	else:
		return( 0 )



def main():


	# Parse command line arguments
	args = argumentParser.parse_args()

	#Load Host file into the gConnectionInfo structure that holds hostname/IP/Port
	gHostCount = loadHostFile( args.HostFile )





	# Start the timer and begin collecting usage information from all hosts.
	# At the end of each loop, append the result to the CSV output file.
	#
	timeStart = time.time()
	timeEnd = timeStart + (args.Time)


	#
	# Open output file.
	# and begin collecting data.
	#
	try:
		lOutputFile = open(args.OutputFile, "w")

		# Output HEADER Info
		lOutputFile.write("Time, ")
		for  gHostNumber in xrange(0,gHostCount):
			lOutputFile.write(gHostConnectionInfo[gHostNumber][0]+", ")
		lOutputFile.write("Total\n")


		while (time.time() < timeEnd):
			accumulatedUserCount = 0
			lOutputFile.write("%.0f" % (time.time() - timeStart))
			# Get number of users Connected for each display.
			for hostNumber in xrange(0,gHostCount):
				lNumUsers = getUserCountFromHost( gHostConnectionInfo[hostNumber][1]);
				accumulatedUserCount += lNumUsers
			
				lOutputFile.write(", "+str( lNumUsers ) )
			lOutputFile.write(", "+str(accumulatedUserCount)+"\n")
			lOutputFile.flush()
			time.sleep( gSampleIntervalInSeconds )

		close(lOutputFile)

	except IOError:
		print(args.OutputFile+" could not be opened.  Exiting.")
		exit()


main()



