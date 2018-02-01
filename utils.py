from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen,HTTPError

def fetch_and_store_data(conn,date):

	#Flush Data
	conn.flushdb()

	#Remove hyphen to match format in url
	date = date.replace('-','')

	csv_file_name = "EQ{}.CSV".format(date)

	url = "http://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP".format(date)

	stock_data = []

	#Try catch block will be used to verify if actually data existed on that day
	try:
		response = urlopen(url)
	except HTTPError as e:
		return

	zipfile = ZipFile(BytesIO(response.read()))

	with zipfile.open(csv_file_name,'r') as csvfile:

		next(csvfile)

		for line in csvfile:
			row = line.decode('utf-8').split(',')
			conn.hmset(row[1], {'code': int(row[0]), 'name':row[1],'open': float(row[4]),
							'high': float(row[5]),'low': float(row[6]),'close': float(row[7])})
			conn.sadd('topset',row[1])
	return

def fetch_top_10_stocks(conn):

	stocks = []
	stock_keys = conn.sort("topset",start=0,num=10,desc=True,by='*->high')

	for code in stock_keys:
		stocks.append(conn.hgetall(code))

	return stocks

def match_key(conn,word):

	word = word.upper()
	stocks = []
	stock_keys = conn.keys(pattern='*{}*'.format(word))

	for code in stock_keys:
		stocks.append(conn.hgetall(code))

	return stocks
