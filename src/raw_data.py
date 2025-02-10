'''
raw data to pull data from polygon
'''

'''
package import
'''

import pandas
import requests
import json
import pytz

from typing import Optional, Union, List, Dict
from datetime import datetime, timezone, timedelta

'''
logger
'''

import logging
logger = logging.getLogger(__name__)

'''
classes
'''

class GetRawDataPolygon(object):
    '''
    pulls historical data from polygon API
    '''

    '''
    constructor
    '''
    
    def __init__(self):
        '''
        constructor for historial data from polygon

        :param str env: env to use for blob store
        '''
        # tokens
        self.__token = self._get_api_token()

        # api info
        self._url_template:str = 'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{timespan}/{start}/{stop}'
        self._auth_header = {
            'Authorization': f'Bearer {self.__token}'
        }

        # data
        self._candles = list()
        self._data:pandas.DataFrame = pandas.DataFrame()
        self._dst:pandas.DataFrame = pandas.DataFrame()

    '''
    properties
    '''

    @property
    def data(self) -> pandas.DataFrame:
        '''
        property to return Polygon data

        :return: api data
        :rtype: pandas.DataFrame
        '''
        return self._data

    '''
    callable functions
    '''

    def get_data(self, ticker:str, start:Union[int, str], stop:Union[int, str], \
        timespan:Optional[str] = 'day') -> pandas.DataFrame:
        '''
        entrypoint to pull data from Polygon API

        ::NOTE -> all times returned are milliseconds since epoch in UTC / Zulu time

        :param str ticker: ticker name to pull data
        :param int | str start: date to start; if passing milliseconds since epoch (int) it needs
            to be adjusted to eastern time; if passing a date string no adjustment is necessary
        :param int | str start: date to stop; if passing milliseconds since epoch (int) it needs
            to be adjusted to eastern time; if passing a date string no adjustment is necessary
        :param Optional[str] timespan: the time period for the agregation; will only use second,
            minute, day
        :return: data from Polygon API
        :rtype: pandas.DataFrame
        '''
        # hit api
        self._candles = self._hit_api(
            ticker = ticker,
            start = start,
            stop = stop,
            timespan = timespan
        )

        # gen dataframe
        self._data = self._generate_dataframe(data = self._candles)
        
        return self._data
    
    '''
    supportive functions
    '''

    def _get_api_token(self) -> str:
        '''
        get api token from config file

        :param: None
        :return: api token
        :rtype: str
        '''
        # setup
        file_name = 'sp_500_config.json'
        token_key = 'polygon_key'
        file_contents = None
        token = ''

        # get token
        try:
            with open(file = file_name, mode = 'r') as file:
                file_contents = file.read()
            
            if file_contents is not None:
                config_file = json.loads(file_contents)
                token = config_file.get(token_key, 'no token')
        except json.JSONDecodeError as jse:
            logger.error(f'error in decoding json file; raw error -> {str(jse)}')
        except Exception as e:
            logger.error(f'unkown error in getting config file; raw error -> {str(e)}')
        else:
            pass
        finally:
            pass

        return token

    def _hit_api(self, ticker:str, start:Union[int, str], stop:Union[int, str], \
        timespan:Optional[str] = 'day') -> List[Dict[str, Union[int, float]]]:
        '''
        pulls historical data from polygonio API

        :param str ticker: ticker name to pull data
        :param int | str start: date to start; if passing milliseconds since epoch (int) it needs
            to be adjusted to eastern time; if passing a date string no adjustment is necessary
        :param int | str start: date to stop; if passing milliseconds since epoch (int) it needs
            to be adjusted to eastern time; if passing a date string no adjustment is necessary
        :param Optional[str] timespan: the time period for the agregation; will only use second,
            minute, day
        :return: the results of the api
        :rtype: List[Dict[str, Union[int, float]]]
        '''
        # set-up
        url = self._url_template.format(
            ticker = ticker,
            timespan = timespan,
            start = start,
            stop = stop
        )
        ticker_data:List[Dict[str, Union[int, float]]] = list()

        # hit api
        try:
            # send data to api
            response:requests.Response = requests.get(
                url = url,
                params = {
                    'adjusted': 'false',
                    'sort': 'asc',
                    'limit': 50000
                },
                headers = self._auth_header
            )

            # unpack response
            dict_response:Dict = response.json()
            ticker_data = dict_response.get('results', list())
        except requests.ConnectTimeout as to:
            logger.error(f'timout; raw error -> {str(to)}')
        except requests.ConnectionError as ce:
            logger.error(f'connection error; raw error -> {str(ce)}')
        except requests.HTTPError as he:
            logger.error(f'http error; raw error -> {str(he)}')
        except json.JSONDecodeError as jde:
            logger.error(f'json decoder error; raw error -> {str(jde)}')
        except Exception as e:
            logger.error(f'error; raw error -> {str(e)}')
        else:
            pass
        finally:
            pass

        return ticker_data

    def _generate_dataframe(self, data:List[Dict[str, Union[int, float]]]) -> pandas.DataFrame:
        '''
        creates dataframe of the data from API

        :param data List[Dict[str, Union[int, float]]]: data from API
        :return: data in the form of a dataframe
        :rtype: pandas.DataFrame
        '''
        # set-up
        dict_data = dict()
        index = list()
        ohcl = ['o', 'h', 'l', 'c', 'v']
        columns = ['open', 'high', 'low', 'close', 'volume']
        df_data = pandas.DataFrame()

        # get values
        for sample in data:
            # get ohlc
            for ohlc_key in ohcl:
                value_list:list = dict_data.get(ohlc_key, list())
                value_list.append(sample.get(ohlc_key, 0.))
                dict_data[ohlc_key] = value_list
            
            # get timestamp
            index.append(sample.get('t', 0))
        
        # create dataframe
        try:
            df_data = pandas.DataFrame(
                data = dict_data,
                index = index
            )
            df_data.index = pandas.to_datetime(df_data.index, unit = 'ms', utc = True)
        except Exception as e:
            logger.error(f'error in creating dataframe; raw error -> {str(e)}')
        else:
            if df_data.empty:
                logger.error('no data in request from polygon API')
            else:
                df_data = df_data[ohcl]
                df_data.columns = columns
                df_data.sort_index(ascending = True)
        finally:
            pass

        return df_data
