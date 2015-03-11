import csv
import sys


def main():
	print "Enter complete file path below:"
	path = raw_input().strip(' ')
	
	file = open(path, 'rU')
	file.seek(0)
	if ',' in file.readline():
		delim = ','
	elif ';' in file.readline():
		delim = ';'
	
	file.seek(0)
	DataCaptured = csv.reader(file, delimiter=delim, skipinitialspace=True)
	print "Below are the columns present in the file :\n"
	headerString = next(DataCaptured)
	headerDict = {}
	key = 0
	for header in headerString :
		key = key + 1
		headerDict [key] = header
	print 'Index\t\tHeader'
	print '-'*8+'\t'+'-'*8
	for key in headerDict:
		print key ,'\t:\t',	 headerDict [key]


	session = True
	while session :
		distinctDim = set()
		print "\nEnter the index of the header whose distinct values you want to see, enter 0 to quit"
		dimension = int(raw_input())
		if dimension == 0:
			session = False
		else:
			file.seek(0)
			for row in DataCaptured:
				distinctDim.add(row[dimension-1])
			print '\n'
			print headerDict[dimension]
			print '-'*20
			for a in distinctDim:
				print '\t',a
	
	file.close()
	
	
if __name__ == '__main__':
	main()


	
