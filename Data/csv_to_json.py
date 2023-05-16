import csv
import json

# Read in CSV file and save data as list of dictionaries
with open('instructions.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    my_data = [row for row in reader]

# Output exported JSON file using json.dump()
with open('output.json', mode='w', encoding='utf-8') as f:
    json.dump(my_data, f, indent=4, ensure_ascii=False)

