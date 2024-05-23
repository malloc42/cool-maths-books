import os
import urllib
import pandas as pd

MAIN_DIR = os.getcwd()

if "database.xlsx" not in os.listdir():
	pd.DataFrame(columns=["S.No.","FileName","Book","Author(s)","Link (PDF)","Edn, Vol","Year","Publisher"]).to_excel("database.xlsx", index=False)

db = pd.read_excel("database.xlsx").set_index("S.No.")

os.chdir("Books")

for file in sorted(os.listdir()):
	if (file.endswith(".pdf")) and (file not in db.FileName.values):
		book = ": ".join(file.split(" - ")[:-1])

		from_authors = file.split(" - ")[-1]
		authors = from_authors.split(" (")[0].split(", ")

		from_years = " (".join(from_authors.split(" (")[1:])
		year = int(from_years.split(", ")[0])

		from_pub = from_years.split(", ")[1]
		pub = ")".join(from_pub.split(")")[:-1])

		edvol = from_pub.split(")")[-1].strip()[:-4].replace(" Edition", "").replace(" V", ", V")

		fsize = os.path.getsize(file)

		if fsize/(2**20) < 25:
			site = "GitHub"
			url = "https://raw.githubusercontent.com/malloc42/cool-maths-books/main/Books/" + urllib.parse.quote(file)
		else:
			site = "Drive"
			url = "https://drive.google.com/file/d/UID_GOES_HERE/view"

		db.loc[len(db)+1] = [file, book, ", ".join(authors), f"[{site}]({url})", edvol if edvol else "N/A", year, pub]

os.chdir(MAIN_DIR)

db.sort_values(by="Book", inplace=True)
db.index = pd.Series(list(range(1, len(db)+1)), name="S.No.")
db.fillna("N/A", inplace=True)
db.to_excel("database.xlsx")

table = db.drop(["FileName"], axis=1).to_markdown()

# read contents of README.md
with open("README.md", "r") as f:
	file = f.read().split("<!-- table below -->")[0]

# update readme.md
with open("README.md", "w") as f:
	f.write(file+"<!-- table below -->\n\n"+table)
