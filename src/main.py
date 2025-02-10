'''
<file doc string>
'''

'''
packages
'''

import pandas
import pytz

from datetime import datetime, timedelta
from enum import Flag, auto
from typing import Tuple

from raw_data import GetRawDataPolygon
from support import set_up_logger

'''
constants
'''

DATETIME_CONV = '%Y-%m-%d'
LOG_DATETIME = '%Y%m%d%h%M%S'

'''
logger
'''

import logging
logger = logging.getLogger()
str_dt_now = datetime.now().strftime(LOG_DATETIME)
log_file = f'sp_500_{str_dt_now}.log'
log_path = '../logs'
set_up_logger(
    log_path = log_path,
    log_file = log_file,
    root_logger = logger
)

'''
analysis style
'''

class AnalysisStyle(Flag):
    '''
    custom type for analysis

    EMA_ONLY -> only use ema for determination
    EQUITY_EMA -> use equity value crossing EMA values
    '''
    EMA_ONLY = auto()
    EQUITY_EMA = auto()

'''
supportive functions
'''

'''
callable functions
'''

def get_data_file(path_file:str) -> pandas.DataFrame:
    '''
    get any existing data

    :param str path_file: path and file name of data
    :return: any data from the file
    :rtype: pandas.DataFrame
    '''
    # setup
    data = pandas.DataFrame()

    try:
        data = pandas.read_parquet(path = path_file)
    except Exception as e:
        logger.error(f'error reading data; raw error -> {str(e)}')
    else:
        data = data.sort_index(ascending = True)
        
        logger.info(f'# of records in data -> {len(data)}')
        logger.info(f'data file data from {data.index[0]} to {data.index[-1]}')
    finally:
        pass

    return data

def get_query_dates(data: pandas.DataFrame) -> Tuple[datetime, datetime]:
    '''
    get the start and end date for the data query

    :param pandas.DataFrame data: data from file
    :return: dates for query
    :rtype: tuple
        tuple[0] -> datetime; start date
        tuple[1] -> datetime; end date
    '''
    # setup
    dt_now = datetime.now(tz = pytz.UTC)

    if data.empty:
        dt_start = datetime(year = 1990, month = 1, day = 1, tzinfo = pytz.UTC)
    else:
        dt_start = data.index[-1] + timedelta(days = 1)

    return dt_start, dt_now

def get_data_from_api(start:datetime, end:datetime) -> pandas.DataFrame:
    '''
    pull data from api

    :param datetime start: start date
    :param datetime end: end date
    :return: datafrom api
    :rtype: pandas.DataFrame
    '''
    # setup
    raw_data = GetRawDataPolygon()
    symbol = 'SPY'

    # get data
    df_api_data:pandas.DataFrame = raw_data.get_data(
        ticker = symbol,
        start = start.strftime(DATETIME_CONV),
        stop = end.strftime(DATETIME_CONV)
    )

    if df_api_data.empty:
        logger.error(f'no data from api')
    else:
        logger.info(f'received data from api')
        logger.info(f'# of records -> {len(df_api_data)}')
        logger.info(f'data received froom API start -> {df_api_data.index[0]} to {df_api_data.index[-1]}')
    
    return df_api_data

def ema_calculations(data:pandas.DataFrame) -> pandas.DataFrame:
    '''
    calculate the 50 and 200 EMA

    :param pandas.DataFrame data: data for EMA calculations
    :return: data w/ EMA calculations
    :rtype: pandas.DataFrame
    '''
    # calc 200 and 50 day EMA
    ema_200 = data['close'].ewm(span = 200, adjust = False, min_periods = 200).mean()
    ema_50 = data['close'].ewm(span = 50, adjust = False, min_periods = 50).mean()
    data = data.assign(
        **{
            'ema_200': ema_200.tolist(),
            'ema_50': ema_50.tolist()
        }
    )

    return data

def in_out(data:pandas.DataFrame) -> pandas.DataFrame:
    '''
    conduct a base EMA analysis on the data

    :param pandas.DataFrmae data: data to be analyzed
    :return: data w/ in out flag
    :rtype: pandas.DataFrame
    '''
    series_in_out = data['ema_50'] >= data['ema_200']
    data = data.assign(in_out = series_in_out.tolist())

    return data

def calc_balances(data:pandas.DataFrame, start_balance:float) -> pandas.DataFrame:
    '''
    calculate the new balances and returns

    :param pandas.DataFrame data: data for calculation
    :param float start_balance: start balance
    :return: data w/ new columns
    :rtype: pandas.DataFrame
    '''
    # setup
    col_balance = 'balance'
    col_close = 'close'
    col_open = 'open'
    col_in_out = 'in_out'
    set_columns = set(data.columns)
    calc_balances, calc_idx = list(), list()

    # start row
    if col_balance in set_columns:
        existing_data = True
        filtered_data = data[data[col_balance].isnull()]
        start_row = filtered_data.index[0]
        start_loc = data.index.get_loc(key = start_row)
        balance = data[col_balance].iloc[start_loc - 1]
        prev_close = data[col_close].iloc[start_loc - 1]
    else:
        existing_data = False
        start_row = data.index[0]
        balance = start_balance
        prev_close = data[col_open].iloc[0]
    
    # iterate through rows
    for idx, row in data.loc[start_row:].iterrows():
        # get data
        current_close = row[col_close]
        gain_loss = current_close / prev_close

        # new balance if in
        if row[col_in_out]:
            new_balance = gain_loss * balance
        else:
            new_balance = balance
        
        # update lists
        calc_idx.append(idx)
        calc_balances.append(new_balance)
        
        # update
        prev_close = current_close
        balance = new_balance
    
    # create new data
    series_balance = pandas.Series(
        data = calc_balances,
        index = calc_idx,
        name = col_balance
    )

    # add to existing data
    if existing_data:
        series_balance = pandas.concat([data[col_balance], series_balance])
    data = data.assign(**{col_balance: series_balance.tolist()})

    # calc returns
    col_sp500_return = 'sp500_return'
    col_return = 'return'
    sp_500_start = data[col_close].iloc[0]
    balance_start = data[col_balance].iloc[0]
    series_sp500_return = data[col_close].apply(lambda x: (x / sp_500_start) - 1.)
    series_return = data[col_balance].apply(lambda x: (x / balance_start) - 1.)
    for column in [col_sp500_return, col_return]:
        if column in data.columns:
            data = data.drop(columns = [col_sp500_return])
    data = data.assign(
        **{
            col_sp500_return: series_sp500_return.tolist(),
            col_return: series_return.tolist()
        }
    )

    return data

'''
main
'''

def main():
    '''
    main function for SP500 analysis
    '''
    # setup
    data_path_file = '../data/data.parquet'
    start_balance = 10000.

    # get data
    logger.info('start get data')
    df_file_data = get_data_file(path_file = data_path_file)
    dt_start, dt_end = get_query_dates(data = df_file_data)
    df_api_data = get_data_from_api(start = dt_start, end = dt_end)
    df_data = pandas.concat([df_file_data, df_api_data])
    df_data = df_data.sort_index(ascending = True)
    logger.info('finished getting data')

    # save data
    logger.info('start save raw data')
    # df_data.to_parquet(path = data_path_file)
    logger.info('finished save raw data')

    # conduct analysis of the data
    logger.info('start caclulations')
    df_data = ema_calculations(data = df_data)
    df_data = in_out(data = df_data)
    df_data = calc_balances(data = df_data, start_balance = start_balance)
    logger.info('finished caclulations')

    # debug
    columns = ['in_out', 'balance', 'sp500_return', 'return']
    print(df_data.info())
    print(df_data.iloc[195:205][columns])
    print(df_data.iloc[-10:][columns])

    return None

if __name__ == '__main__':
    main()
