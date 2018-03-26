######################################
#             DomainMap              #
#  Code by Jonathan Tessarolo - 2018 #
######################################

import argparse 								# Import for Argument parsing
from argparse import RawTextHelpFormatter		# Import for Argument parsing
import whois									# Import for WhoIs Information
import socket									# Import for IP Address Information
import requests									# Import for URL opening
from bs4 import BeautifulSoup 					# Import for page title interpretation

def argumentParsing():
 parser = argparse.ArgumentParser(description="""
 This script reads line by line of an input file populated with
 domain names and brings back the following information:
 
  - Domain Owner
  - IP Address
  - Destination URL
  - Page Title""", formatter_class=RawTextHelpFormatter)

 # Required arguments
 parser.add_argument("input_file", help="Path of input file")
 parser.add_argument("output_file", help="Path of output file")
 
 # Optional arguments
 parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
 
 global args
 args = parser.parse_args()
 
 if args.verbose:
  print("Verbosity increased...")

def openInputFile(file):

 global inputFile, inputFileLines

 try:
  inputFile = open(file, "r")
 except:
  print("[ERROR] Failed to open input file")
  
 try:
  inputFileLines = inputFile.read().splitlines()
 except:
  print("[ERROR] Failed to read lines of input file")
 
def createOutputFile(file):

 global outputFile
 
 try: 
  outputFile = open(file, "w")
 except:
  print("[ERROR] Failed to open output file")
  
 outputFile.write("Target Domain;Owner;IP Address;Destination URL;Page Title\n")

def findWhoIs(domain):
 try:
  w = whois.whois('' + domain + '')
 except:
  return "Failed to find WhoIs information of " + domain + ""
 
 if w.owner:
  return w.owner
 else:
  return "Error while retrieving WhoIs information"
  
def findIPAddress(domain):
 try:
  ipaddress = socket.gethostbyname(domain)
 except:
  return "Error while retrieving IP address"

 return ipaddress
 
def findHTMLData(domain):
 try:
  response = requests.get("http://" + domain)
 except:
  finalURL = "Error while retrieving webpage"
  pageTitle = "Error while retrieving HTTP page title"
  return finalURL, pageTitle
  
 try:
  html = BeautifulSoup(response.content, "html5lib")
 except:
  finalURL = response.url
  pageTitle = "Error while retrieving HTTP page title"
  return finalURL, pageTitle
 
 finalURL = response.url
 
 try:
  pageTitle = html.title.string.strip()
 except:
  pageTitle = "Error while retrieving HTTP page title"
  
 return(finalURL, pageTitle)
 
def gatherInformation():

 global inputFile, inputFileLines

 totalLines = len(inputFileLines)
 currentLine = 1
 
 print("\n[IN PROGRESS] Gathering information of " + str(totalLines) + " domains...\n")
 for line in inputFileLines:
  print(" [" + str(currentLine) + "/" + str(totalLines) + "] - " + line)
  targetDomain = line
  Owner = findWhoIs(line)
  ipAddress = findIPAddress(line)
  destinationURL, pageTitle = findHTMLData(line)
  currentLine = currentLine + 1
  writeToOutputFile("" + targetDomain + ";" + Owner + ";" + ipAddress + ";" + destinationURL + ";" + pageTitle + "" + "\n")
 print("\n[SUCCESS] Information gathering finished\n")
 
def writeToOutputFile(data):
 outputFile.write(data)
  
def closeFiles():
 inputFile.close()
 outputFile.close() 

argumentParsing()
openInputFile(args.input_file)
createOutputFile(args.output_file)
gatherInformation()
closeFiles()