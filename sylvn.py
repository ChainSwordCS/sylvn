import subprocess
import os
import csv

svnCmd = "svn"
walkStart = "turtle_project"
outputFile = "dumps.csv"

try:
	os.remove(outputFile)
	print("Cleaning up old CSV")
except OSError:
	pass

with open(outputFile, 'w', newline='', encoding='utf-8') as csvfile:
	outputWriter = csv.writer(csvfile)
	# Write column headers
	outputWriter.writerow(["path","isDirectory","lastChangedAuthor","lastChangedRev","lastChangedDate","textLastUpdated","checksum"])
	
	for rootdir, dirnames, filenames in os.walk(walkStart):
		# Skip over .svn directory
		if ".svn" in dirnames:
			del dirnames[dirnames.index(".svn")]
		
		for dirn in dirnames:
			absolute = os.path.join(rootdir, dirn)
			print("Dumping "+absolute)
			result = subprocess.run(["svn", "info", absolute], capture_output=True)
			lines = result.stdout.decode("UTF-8").split("\r\n")
			path = ""
			lca = ""
			lcr = ""
			lcd = ""
			chk = ""
			for line in lines:
				if line.startswith("Path: "):
					path = line[6:]
				if line.startswith("Last Changed Author: "):
					lca = line[21:]
				if line.startswith("Last Changed Rev: "):
					lcr = line[18:]
				if line.startswith("Last Changed Date: "):
					lcd = line[19:]
				if line.startswith("Checksum: "):
					chk = line[10:]
			outputWriter.writerow([absolute, True, lca, lcr, lcd, "", chk])
		
		for fn in filenames:
			absolute = os.path.join(rootdir, fn)
			print("Dumping "+absolute)
			result = subprocess.run(["svn", "info", absolute], capture_output=True)
			lines = result.stdout.decode("UTF-8").split("\r\n")
			path = ""
			lca = ""
			lcr = ""
			lcd = ""
			tlu = ""
			chk = ""
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
			outputWriter.writerow([absolute, True, lca, lcr, lcd, tlu, chk])