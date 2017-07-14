import sys, pandas, pandas_datareader
from yahoo_finance import Share
from bs4 import BeautifulSoup
from pandas_datareader import data
import fix_yahoo_finance
from datetime import datetime

def Main():
	datetime_start = datetime(2010, 1, 1)
	datetime_finish = datetime(2017, 5, 25)

	f_google = data.DataReader('F', 'google', datetime_start, datetime_finish)
	print('Ford on google, symbol "F", on 04 January 2010: %s' %f_google.loc['2010-01-04'])

	sp_500_yahoo = Share('^GSPC')
	print('Yahoo S&P 500: %s' %sp_500_yahoo.get_price())

	list_symbols = ['^GSPC']

	for string_symbol in list_symbols:
		try:
			sp500_yahoo_fix = data.get_data_yahoo(string_symbol, start = datetime_start, end = datetime_finish)
		except Exception as e:
			string_error = str(e.args)
			print('\nError for S&P 500 symbol %s on yahoo: %s' %(string_symbol, string_error))
		else:
			print('\nS&P 500 on yahoo, symbol %s, on 04 January 2010: %s' %(string_symbol, sp500_yahoo_fix.loc['2010-01-04']))
			print('\nS&P 500 on yahoo, symbol %s, on 25 May 2017: %s' %(string_symbol, sp500_yahoo_fix.loc['2017-05-25']))
		finally:
			pass

	# system info
	print('\npython version: %s' %sys.version)
	print('pandas version: %s' %pandas.__version__)
	print('pandas_datareader version: %s' %pandas_datareader.__version__)
	print('fix_yahoo_finance version: %s' %fix_yahoo_finance.__version__)

if __name__ == '__main__':
	Main()