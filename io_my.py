import urllib.request as rq
from csv import reader, writer
def download(key, gid=[0], format="csv", outputfile="data/tablesheet"):
	url_format = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=%s&gid=%i"
	ret = []
	if (len(gid) > 1):
		ret = []
		for id in range(len(gid)):
			filename = outputfile + "_" +  str(id) + ".xls"
			rq.urlretrieve(url_format % (key, format, gid[id-1]), filename)

			with open(filename, 'r', encoding="UTF-8", newline='') as read_obj:
				# pass the file object to reader() to get the reader object
				csv_reader = reader(read_obj)
				# Pass reader object to list() to get a list of lists
				ls = list(csv_reader)
				ret = ret + ls


		with open(outputfile + ".xls", 'w+', encoding="UTF-8",newline='') as write_obj:
			writer_ = writer(write_obj)
			writer_.writerows(ret)
	else:
		filename = outputfile + ".xls"
		rq.urlretrieve(url_format % (key, format, gid[0]), filename)

		with open(filename, 'r', encoding="UTF-8",newline='') as read_obj:
			# pass the file object to reader() to get the reader object
			csv_reader = reader(read_obj)
			# Pass reader object to list() to get a list of lists
			ret = list(csv_reader)
		return ret

def get_sheet_ids(key, api_key):
	ret = rq.urlopen("https://docs.googleapis.com/v4/spreadsheets/d/%s/key=%s?&fields=sheets.properties" % (key,api_key))
	return ret
