# agenda
# 1. dump dictionary `data` to a .json file
# 2. get file sizes and sort urls {>25mb => drive}
# 3. use `data` to create a summary table for repo page

# for file name & size analysis
import os

# json dumping (json use: not determined YET)
import json

MAIN_DIR = os.getcwd()

# /Books
os.chdir("Books")

# something `like` a library
data = {}

"""
# key: (int) index
# value: (dict) {
	"book": (str),
	"authors": (strs),
	"year": (str),
	"pub": (str),
	"edvol": (str),
	"href": {
			"name": (str),
			"url": (str)
			}
}
"""

# FORMAT (`.` => . is observed (atleast once) in every file name ):
# <TITLE - SUBTITLE(IF ANY)>` - `<AUTHOR(S) SEP. BY COMMAS>` (`YEAR, PUBLISHER(ALT)`)` <NTH EDITION, IF ANY> <VOL, IF ANY>`.PDF`

# examples
# w/ subtitle, w/o pub-alt
# Calculus - One-Variable Calculus with an Introduction to Linear Algebra - Tom M. Apostol (1967, Wiley) 2nd Edition Vol I
# w/o subtitle, w/ pub-alt
# Elementary Linear Algebra - Stephen Andrilli, David Hecker (2016, Elsevier (Academic Press)) 5th Edition.pdf

for file in sorted(os.listdir()):
	if file.endswith(".pdf"):
		# join the main and subtitle by ": "
		book = ": ".join(file.split(" - ")[:-1])
		
		# extract text starting from the author right next to the end of `<subtitle> - `
		from_authors = file.split(" - ")[-1]
		# `.split(" (")[0]` can be better visualised w/ Line 40/42
		# `.split(", ")` to store all authors in a list
		authors = from_authors.split(" (")[0].split(", ")
		# To store in <LAST>, <FIRST< MIDDLE(s)> form
		# authors = [a.split()[-1]+", "+" ".join(a.split()[:-1]) for a in authors]

		# work it out with examples
		from_years = " (".join(from_authors.split(" (")[1:])
		year = from_years.split(", ")[0]

		# work it out with example at line 42
		from_pub = from_years.split(", ")[1]
		pub = ")".join(from_pub.split(")")[:-1])

		# `[:-4]` to exclude extension `.pdf`
		edvol = from_pub.split(")")[-1].strip()[:-4].replace(" Edition", "").replace(" V", ", V")

		# Get file size in bytes
		fsize = os.path.getsize(file)
		# GitHub restricts web uploads to 25mb
		# The cap on CLI is 100mb but i'm unable to upload
		# (tried on both linux and win)
		# not really an issue, but worth mentioning
		# Those files (>100mb) will not be visible in the repo bc they're hosted on Drive
		if fsize/(2**20) < 25:
			site = "GitHub"
			url = f'https://raw.githubusercontent.com/malloc42/cool-maths-books/main/Books/{file.replace(" ","%20").replace(",", "%2c")}'
		else:
			site = "Drive"
			url = "https://drive.google.com/file/d/UID_GOES_HERE/view"	# To be added manually later, in the markdown file
			# This is not worth automating at the moment, doing so will be an overkill esp. with Drive
			# Also i'm not at all good at this :p.
			
			# Though it is stated in the markdown (no copyright intended), there are still
			# high chances of being struck by the DMCA on the Drive (or even GitHub)

		# Prepare for data dump
		data[len(data)] = {
			"book": book,
			"authors": ", ".join(authors),
			"year": year,
			"pub": pub,
			"edvol": edvol if edvol else "N/A",
			"href": {
						"site": site,
						"url": url
					}
		}

# Back to MAIN_DIR
os.chdir(MAIN_DIR)

# data dump
out_file = open("data.json", "w") 
json.dump(data, out_file, indent = 4) 
out_file.close()

# generate table
# https://www.markdownguide.org/extended-syntax/
# | s.no | book | author(s) | link (pdf only) | edition-vol | year | publisher |
# |:---:|:---|:---|:---:|:---:|:---:|:---|

table_rows = ["|S.No.|Book|Author(s)|Link (PDF)|Edn, Vol|Year|Publisher|",
			  "|:---:|:---|:---|:---:|:---:|:---:|:---|"]

for i in data:
	t = data[i]
	table_rows.append(f"|{i+1}|{t['book']}|{t['authors']}|[{t['href']['site']}]({t['href']['url']})|{t['edvol']}|{t['year']}|{t['pub']}|")

# table backup
with open("table.txt", "w") as f:
	f.write("\n".join(table_rows))

# read contents of readme.md
with open("README.md", "r") as f:
	file = f.read()

file = file.split("<!-- table below -->")[0]

# update readme.md
with open("README.md", "w") as f:
	f.write(file+"<!-- table below -->\n\n"+"\n".join(table_rows))
