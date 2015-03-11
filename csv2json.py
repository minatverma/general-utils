import csv
import json
import sys

csvfile = open(sys.argv[1], 'rU')
jsonfile = open(sys.argv[1][:-3]+'json', 'w')

headerString = csvfile.readline()
headerList = list()

for header in headerString.split(','):
    headerList.append(header.strip())

fieldnames = tuple(headerList)
# fieldnames = ('OrderIdentifier','AssignmentNumber','ResponseIdentifier','VendorName','QuestionNumber','CycleIdentifier','MultipriceSelectIdentifier','OptionIdentifier','ResponseText','CommentsText','ResponseLocationDescription','CommentsLocationDescription','PotentialScoreNumber','ActualScoreNumber')
reader = csv.DictReader( csvfile,fieldnames)
for row in reader:
    json.dump(row, jsonfile, encoding="utf-8")
    jsonfile.write('\n')
