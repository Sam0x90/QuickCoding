import json
import csv

with open('feed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_keys = set()
for row in data:
    all_keys.update(row.keys())

fieldnames = sorted(all_keys)

with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for row in data:
        if isinstance(row.get('screenshots'), list):
            row['screenshots'] = ', '.join(row['screenshots'])
        writer.writerow(row)
