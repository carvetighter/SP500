'''
<file doc string>
'''

'''
warnings
'''

import warnings
warnings.simplefilter('ignore')

'''
packages
'''

import json
import pandas
import pytz
import requests

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pathlib import Path
from datetime import datetime, timedelta
from enum import Flag, auto
from typing import Tuple, Dict, List

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

def _apply_rolling(window:pandas.Series) -> int:
    '''
    determine if the change is a buy or a sell

    :param pandas.Series window: winow of length 2 to determien a change
    :return: a buy or sell
    :rtype: string
    '''
    return_value = 0

    if len(window == 2):
        if window.iloc[0] - window.iloc[1] > 0.:
            return_value = 1
        elif window.iloc[0] - window.iloc[1] < 0.:
            return_value = 2
        else:
            pass
    else:
        pass

    return return_value

def _get_next_idx(index:pandas.Index, idx_key:pandas.Timestamp, step:int) -> pandas.Timestamp:
    '''
    finds the index key for the next (step) locations; not a collection just an index key

    :param pandas.Index index: index to use
    :param pandas.Timestamp idx_key: key to find
    :param int step: number of steps to find the next index key
    :return: desired index key
    :rtype: pandas.Timestamp
    '''
    return_value = idx_key

    try:
        loc_buy = index.get_loc(idx_key)
        return_value = index[loc_buy + step]
    except Exception as e:
        logger.error(f'could not find next index key for {idx_key} at step {step}')
    else:
        pass
    finally:
        pass

    return return_value

'''
callable functions
'''

def get_json_file(file_name:str) -> Dict[str, str]:
    '''
    get json file from location

    :param str file_name: path and file name for file
    :return: file content
    :rtype: dict
    '''
    # set-up
    file_data = ''

    # read file
    with open(file = file_name, mode = 'r') as file:
        file_data = file.read()
    
    return json.loads(file_data)

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
        logger.error(f'error reading data; no data in file; raw error -> {str(e)}')
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

def get_data_from_api(start:datetime, end:datetime, token:str) -> pandas.DataFrame:
    '''
    pull data from api

    :param datetime start: start date
    :param datetime end: end date
    :return: datafrom api
    :rtype: pandas.DataFrame
    '''
    # setup
    symbol = 'SPY'
    url = f'https://api.tiingo.com/tiingo/daily/{symbol}/prices/'
    params = {
        'startDate': start.strftime(DATETIME_CONV),
        'endDate': end.strftime(DATETIME_CONV)
    }
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }
    df_data = pandas.DataFrame()
    columns = ['open', 'high', 'low', 'close']

    # get data from api
    try:
        # get data
        response = requests.get(
            url = url,
            params = params,
            headers = header
        )
        data = response.json()

        # create dataframe
        if data:
            df_data = pandas.DataFrame(data = data)
            df_data.index = df_data['date'].apply(lambda x: pandas.to_datetime(x)).tolist()
            df_data = df_data[columns]
    except json.JSONDecodeError as jde:
        logger.error(f'{str(jde)}')
    except Exception as e:
        logger.error(f'unknown error -> {str(e)}')
    else:
        pass
    finally:
        pass

    # log info
    if df_data.empty:
        logger.error(f'no data from api')
    else:
        logger.info(f'received data from api')
        logger.info(f'# of records -> {len(df_data)}')
        logger.info(f'data received froom API start -> {df_data.index[0]} to {df_data.index[-1]}')
    
    return df_data

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

def changes(data:pandas.DataFrame) -> pandas.DataFrame:
    '''
    calculate when the buys and sells are for the data

    :param pandas.DataFrame data: data used to calculate buys and sells
    :return: data with buys and sells
    :rtype: pandas.DataFrame
    '''
    # set-up
    column = 'in_out'
    
    # calc change
    series_buy_sell = data[column].rolling(window = 2).apply(_apply_rolling, raw = False)
    series_buy_sell.iloc[0] = 0
    series_buy_sell = series_buy_sell.astype(int)

    # replace int w/ strings
    series_buy_sell[series_buy_sell == 0] = pandas.NA
    series_buy_sell[series_buy_sell == 1] = 'sell'
    series_buy_sell[series_buy_sell == 2] = 'buy'
    
    return data.assign(change = series_buy_sell)

def percent_change(data:pandas.DataFrame) -> pandas.DataFrame:
    '''
    calculate percent change daily

    :param data pandas.DataFrame: data to calc percent change
    :return: data with percent change calculate
    :rtyp: pandas.DataFrame
    '''
    series_perc_change = data['close'].pct_change()
    series_perc_change = series_perc_change + 1.
    return data.assign(perc_change = series_perc_change)

def calc_balances(data:pandas.DataFrame, start_balance:float) -> Tuple[pandas.DataFrame, List[pandas.Timestamp], List[pandas.Timestamp]]:
    '''
    calculate number of shares used and the buy and sell locations in the index

    :param pandas.DataFrame data: data to use for number of shares
    :return: data and buy and sell locations
        tuple[0] -> pandas.DataFrame; data with number of shares
        tuple[1] -> list; buy timestamps
        tuple[2] -> list; sell timestamps
    :rtype: tuple
    '''
    # set-up
    col_open = 'open'
    col_close = 'close'
    bool_first = True

    # initialize series
    series_num_shares = pandas.Series([0 for _ in range(0, len(data))])
    series_num_shares = series_num_shares.astype(int)
    series_num_shares.index = data.index
    series_balances = pandas.Series([0. for _ in range(0, len(data))])
    series_balances.index = data.index

    # get buys and sells
    buys = data['change'][data['change'] == 'buy'].index.tolist()
    sells = data['change'][data['change'] == 'sell'].index.tolist()
    if len(sells) < len(buys):
        sells.append(data.index[-1])

    # calc shares
    new_idx_buys, new_idx_sells = list(), list()
    prev_bal_idx = None
    for idx_buy, idx_sell in zip(buys, sells):
        # get new indexes
        new_idx_buy = _get_next_idx(
            index = data.index,
            idx_key = idx_buy,
            step = 1
        )
        new_idx_sell = _get_next_idx(
            index = data.index,
            idx_key = idx_sell,
            step = 1
        )

        # balance to use
        if bool_first:
            balance = start_balance
        else:
            balance = series_balances[prev_bal_idx]
        
        # add shares
        shares = int(balance / data.loc[new_idx_buy, col_open])
        series_num_shares.loc[new_idx_buy:new_idx_sell] = shares

        # add out balance
        if bool_first:
            series_balances[:new_idx_buy] = balance
        else:
            out_idx_start = _get_next_idx(
                index = data.index,
                idx_key = prev_bal_idx,
                step = 1
            )
            series_balances[out_idx_start:idx_buy] = balance

        # add in balance
        series_balances.loc[new_idx_buy:new_idx_sell] = data.loc[new_idx_buy:new_idx_sell, col_close] * shares
        prev_bal_idx = new_idx_sell

        # add to lists
        new_idx_buys.append(new_idx_buy)
        new_idx_sells.append(new_idx_sell)

        # set flag
        if bool_first:
            bool_first = False
    
    # calc sp500 balance on buy and hold
    series_filter_shares = series_num_shares[series_num_shares != 0]
    idx_first_buy = series_filter_shares.index[0]
    shares_first_buy = series_filter_shares.iloc[0]
    series_buy_hold_shares = pandas.Series(
        data = [shares_first_buy for _ in range(0, len(data))],
        index = data.index
    )
    series_buy_hold_shares[:idx_first_buy] = 0
    series_buy_hold_balance = series_buy_hold_shares * data[col_close]
    series_buy_hold_balance[series_buy_hold_balance == 0.] = start_balance

    # add new data
    dict_new_data = {
        'num_shares': series_num_shares,
        'balance': series_balances,
        'buy_hold_shares': series_buy_hold_shares,
        'buy_hold_balance': series_buy_hold_balance
    }
    data = data.assign(**dict_new_data)

    return data, new_idx_buys, new_idx_sells

def create_plots(data:pandas.DataFrame, buys:List[pandas.Timestamp], sells:List[pandas.Timestamp]):
    '''
    create plots for visualizations

    :param pandas.DataFrame data: data to plot
    :param list buys: buys to plot as verticle lines
    :param list sells: sells to plot as verticle lines
    :return: None
    '''
    # set-up
    fig:Figure = None
    axes:List[Axes] = None
    col_balance = 'balance'
    col_bh_balance = 'buy_hold_balance'
    col_50_ma = 'ema_50'
    col_200_ma = 'ema_200'

    # file
    directory = 'visualizations'
    file = data.index[-1].strftime(DATETIME_CONV) + '.png'
    path = Path('..', directory, file)

    # fig & axes (rows x columns)
    fig, axes = pyplot.subplots(2, 1, sharex = True)
    fig.set_size_inches(10., 7.)

    # plot balances
    x = data.index.tolist()
    axes[0].plot(
        x, data[col_balance], color = 'green', linewidth = 2.5, linestyle = '-',
        label = f'SMA Balance ${data[col_balance].iloc[-1]:,.0f}'
    )
    axes[0].plot(
        x, data[col_bh_balance], color = 'black', linewidth = 2.5, linestyle = '-',
        label = f'Buy & Hold Balance ${data[col_bh_balance].iloc[-1]:,.0f}'
    )
    axes[0].set(title = 'Balances', ylabel = 'Dollars')

    # plot sma values
    axes[1].plot(
        x, data[col_50_ma], color = 'blue', linewidth = 2.5, linestyle = '-',
        label = '50 MA'
    )
    axes[1].plot(
        x, data[col_200_ma], color = 'red', linewidth = 2.5, linestyle = '-',
        label = '200 MA'
    )
    axes[1].set(title = 'Moving Averages', ylabel = 'Dollars')

    # plot buys
    for buy_val in buys[:-1]:
        axes[0].axvline(buy_val, color = 'orangered', linewidth = 1, linestyle = '--')
        axes[1].axvline(buy_val, color = 'orangered', linewidth = 1, linestyle = '--')
    axes[0].axvline(buys[-1], color = 'orangered', linewidth = 1, linestyle = '--', 
            label = 'Buy')
    axes[1].axvline(buys[-1], color = 'orangered', linewidth = 1, linestyle = '--', 
        label = 'Buy')
    
    # plot sells
    if sells[-1].date() == datetime.now(tz = pytz.UTC).date():
        final_plot_index = -2
    else:
        final_plot_index = -1
    for sell_val in sells[:final_plot_index]:
        axes[0].axvline(sell_val, color = 'indigo', linewidth = 1, linestyle = '--')
        axes[1].axvline(sell_val, color = 'indigo', linewidth = 1, linestyle = '--')
    axes[0].axvline(sells[final_plot_index], color = 'indigo', linewidth = 1, linestyle = '--', 
            label = 'Sell')
    axes[1].axvline(sells[final_plot_index], color = 'indigo', linewidth = 1, linestyle = '--', 
        label = 'Sell')

    # additional plot elements
    axes[0].legend(loc = 'best')
    axes[1].legend(loc = 'best')
    pyplot.subplots_adjust(wspace = None, hspace = 0.4)
    pyplot.suptitle('SP500 Analysis')

    # save plot
    fig.savefig(str(path))

    return None

'''
main
'''

def main():
    '''
    main function for SP500 analysis
    '''
    # setup
    data_path_file = Path('..', 'data', 'data.parquet')
    results_path_file = Path('..', 'data', 'results.parquet')
    token_file_name = Path('.', 'sp_500_config.json')
    token_key_name = 'tiingo_key'
    start_balance = 10000.

    # get tokens
    logger.info('getting tokens')
    tokens = get_json_file(file_name = str(token_file_name))
    logger.info('finished getting tokens')

    # get data
    logger.info('start get data')
    df_file_data = get_data_file(path_file = str(data_path_file))
    dt_start, dt_end = get_query_dates(data = df_file_data)
    df_api_data = get_data_from_api(start = dt_start, end = dt_end, token = tokens.get(token_key_name, ''))
    df_data = pandas.concat([df_file_data, df_api_data])
    df_data = df_data.sort_index(ascending = True)
    logger.info('finished getting data')

    # save data
    logger.info('start save raw data')
    df_data.to_parquet(path = data_path_file)
    logger.info('finished save raw data')

    # conduct analysis of the data
    logger.info('start caclulations')
    df_data = percent_change(data = df_data)
    df_data = ema_calculations(data = df_data)
    df_data = in_out(data = df_data)
    df_data = changes(data = df_data)
    df_data, buys, sells = calc_balances(data = df_data, start_balance = start_balance)
    logger.info('finished caclulations')

    # save data
    logger.info('save results')
    df_data.to_parquet(path = str(results_path_file))
    logger.info('finished saving results')

    # create plots
    logger.info('creating plot')
    create_plots(data = df_data, buys = buys, sells = sells)
    logger.info('finished creating plot')

    # fig, ax = pyplot.subplots(1, 1)
    # x = [x for x in range(0, len(df_data))]
    # ax.plot(x, df_data['balance'], label = 'sma')
    # ax.plot(x, df_data['buy_hold_balance'], label = 'bh')
    # ax.legend(loc = 'best')
    # fig.savefig(r'c:\Code\Prod\Sp500\plot.png')

    # debug
    # print(df_data.info())
    # columns = ['in_out', 'perc_change', 'num_shares', 'balance']
    # filter_balace = df_data['balance'] == 0.
    # print(filter_balace.sum())
    # df_zero = df_data[filter_balace]
    # idx_first_zero = df_zero.index[0]
    # idx_int_first_zero = df_data.index.get_loc(idx_first_zero)
    # print(df_data[['balance', 'in_out']].iloc[idx_int_first_zero - 5:idx_int_first_zero + 5])
    # print(df_data.iloc[:10][columns], '\n')
    # print(df_data.iloc[195:205][columns], '\n')
    # print(df_data.iloc[-10:][columns], '\n')
    # print(df_data.iloc[-1]['balance'])
    # print(df_data['change'].dropna())

    

    return None

if __name__ == '__main__':
    main()
