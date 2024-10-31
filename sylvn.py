# python 3.12+

import subprocess
import os
import csv
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--inputdir", help="the svn directory to parse. (the directory containing the \".svn\" folder", required=True)
argparser.add_argument("-o", "--output", help="the name for the output csv file. default is \"dumps.csv\"", default="dumps.csv")
argparser.add_argument("--svn", help="svn path variable, or filepath to svn executable. default is \"svn\"", default="svn")

args = argparser.parse_args()

svnCmd = args.svn
walkStart = args.inputdir
outputFile = args.output

try:
	os.remove(outputFile)
	print("Cleaning up old CSV")
except OSError:
	pass

with open(outputFile, 'w', newline='', encoding='utf-8') as csvfile:
	outputWriter = csv.writer(csvfile)
	# Write column headers
	outputWriter.writerow(["path","isDirectory","lastChangedAuthor","lastChangedRev","lastChangedDate","textLastUpdated","checksum"])
	
	def parsefile(rootdir, fn, isdir):
		path = ""
		lca = ""
		lcr = ""
		lcd = ""
		tlu = ""
		chk = ""
		
		# absolute is a str
		absolute = os.path.join(rootdir, fn)
		print("Dumping "+absolute)
		
		# KNOWN ISSUE: If the target filename (or path to it) contains Japanese text characters,
		# And the user is on Windows (10) using an English locale,
		# The call to subprocess.run() will just fail :P
		#
		# Workaround: Set your system locale to Japanese
		
		# "universal_newlines=True" = "text=True" in the args passed to subprocess.run()
		result = subprocess.run(["svn", "info", absolute], shell=True, text=True, capture_output=True)
		
		if(result.stdout is not None):
			stdout = ""
			
			# commented-out because it slows down execution
			# and is only necessary if you change to "text=False" in the above call to subprocess.run()
			#if(type(result.stdout) is bytes):
			#	stdout = result.stdout.decode("UTF-8") # possible encoding issues?
			#else: # type(result.stdout) is str
			stdout = result.stdout
			
			#print(result.stdout) # debug
			lines = result.stdout.split("\n") # "\r\n"
			for line in lines:
				if line.startswith("Path: "):
					path = line[6:]
				if line.startswith("Last Changed Author: "):
					lca = line[21:]
				if line.startswith("Last Changed Rev: "):
					lcr = line[18:]
				if line.startswith("Last Changed Date: "):
					lcd = line[19:]
				if line.startswith("Text Last Updated: "):
					tlu = line[19:]
				if line.startswith("Checksum: "):
					chk = line[10:]
		outputWriter.writerow([absolute, isdir, lca, lcr, lcd, tlu, chk])
	
	
	for rootdir, dirnames, filenames in os.walk(walkStart):
		# Skip over .svn directory
		if ".svn" in dirnames:
			del dirnames[dirnames.index(".svn")]
		
		parsefile(rootdir, "", True)
		
		for dirn in dirnames:
			parsefile(rootdir, dirn, True)
		
		for fn in filenames:
			parsefile(rootdir, fn, False)
