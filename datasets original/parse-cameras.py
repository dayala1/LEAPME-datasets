import xmltodict
import os
import json

# This script is used to transform the cameras dataset into TAPON compatible json files with the desired properties
STORE_ROOT = "../records/cameras"
site_indexes = {}
with open('cameras.xml', 'rb') as fd:
	doc = xmltodict.parse(fd.read())
	products = doc["products"]["product"]
	for product in products:
		site = product["site"]
		if site not in site_indexes:
			site_indexes[site] = 0
		site_indexes[site] += 1
		record = {}
		for key, value in product.items():
			if(key not in ["site", "url"]):
				record[key]=value

		directory = os.path.join(STORE_ROOT, site)
		file = os.path.join(directory, str(site_indexes[site]) + ".json")
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open(file, "w") as fp:
			json.dump(record, fp, indent=4)