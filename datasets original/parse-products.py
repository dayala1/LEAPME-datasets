import json
import os
import re

# This script is used to transform the headtvs, tvs and tvs datasets into TAPON compatible json files with the desired properties

with open("./tvs_labelled_entities.json", 'r', encoding="utf-8") as file:
	products = json.load(file)

sources = {}
mappings = {}
target_directory = '../records/datasets/products-tvs'
source_indexes = {}

for product in products:
	source = re.split(r'\d',product["id_warc"])[0]
	sources[source] = sources.get(source, 0)+1
	index = source_indexes.get(source, 1)
	source_indexes[source] = index + 1
	properties = {}
	dataset = {}
	for attribute in (product["list_atts"] + product["table_atts"]):
		parts = attribute.split(':', 1)
		if(len(parts) == 2):
			name, value = parts
			dataset[name] = value
	directory = os.path.join(target_directory, source)
	if not os.path.exists(directory):
		os.makedirs(directory)
	target_file = os.path.join(directory, str(index) + ".json")
	with open(target_file, "w") as fp:
				json.dump(dataset, fp, indent=4)
	for mapping in product["atts_map"]:
		source_attr, target_attr = mapping.split(':', 1)
		if(target_attr not in mappings):
			mappings[target_attr] = []
		if(source_attr not in mappings[target_attr]):
			mappings[target_attr].append(source_attr)

with open('../mappings/mappings-tvs.json', 'w') as file:
	json.dump(mappings, file, indent=4)