#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#        

import DataPrep, SqlMethods
import pandas, fix_yahoo_finance, numpy, warnings
from pandas_datareader import data
from matplotlib import pyplot, style
from datetime import datetime, time, timedelta, timezone

# ignore warnings
warnings.simplefilter('ignore')

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Methods
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

def def_Methods(list_cluster_results, array_sparse_matrix):
    ###############################################################################################
    ###############################################################################################
    #
    # below is an example of a good method comment
    #
    # ---------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # this method implements the evauluation criterea for the clusters of each clutering algorithms
    # criterea:
    #        - 1/2 of the clusters for each result need to be:
    #            - the average silhouette score of the cluster needs to be higher then the silhouette score of all the clusters
    #              combined
    #            - the standard deviation of the clusters need to be lower than the standard deviation of all the clusters
    #              combined
    #        - silhouette value for the dataset must be greater than 0.5
    #
    # Requirements:
    # package time
    # package numpy
    # package statistics
    # package sklearn.metrics
    #
    # Inputs:
    # list_cluster_results
    # Type: list
    # Desc: the list of parameters for the clustering object
    # list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
    #                or dense array
    # list[x][1] -> type: string; the cluster ID with the parameters
    #
    # array_sparse_matrix
    # Type: numpy array
    # Desc: a sparse matrix of the samples used for clustering
    #    
    # Important Info:
    # None
    #
    # Return:
    # object
    # Type: list
    # Desc: this of the clusters that meet the evaluation criterea
    # list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
    #                or dense array
    # list[x][1] -> type: string; the cluster ID with the parameters
    # list[x][2] -> type: float; silhouette average value for the entire set of data
    # list[x][3] -> type: array; 1 dimensional array of silhouette values for each data sample
    # list[x][4] -> type: list; list of lists, the cluster and the average silhoutte value for each cluster, the orders is sorted 
    #                    highest to lowest silhoutte value
    #                    list[x][4][x][0] -> int; cluster label
    #                    list[x][4][x][1] -> float; cluster silhoutte value
    # list[x][5] -> type: list; a list that contains the cluster label and the number of samples in each cluster
    #                    list[x][5][x][0] -> int; cluster label
    #                    list[x][5][x][1] -> int; number of samples in cluster list[x][5][x][0]
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # objects declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # sub-section comment
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # sectional comment
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object cleanup
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # return value
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    return list_return

def Setup(m_sql_conn, list_sql_tables):
    ###############################################################################################
    ###############################################################################################
    #
    # this method setsup the sql database and conducts the checks necessary
    #
    # Requirements:
    # file SqlMethods
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql connection
    # Desc: connection to the local sql database on my D: drive
    #    
    # list_sql_tables
    # Type: list
    # Desc: the names of a sql tables as strings
    #
    # Important Info:
    # None
    #
    # Return:
    # n/a
    # Type: n/a
    # Desc: n/a
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # objects declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists / dictionary declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    list_sql_col_names_sp500_data = ['date_date', 'float_close', 'string_in_market', 'string_trigger', 'float_50_sma',
                                  'float_200_sma', 'float_delta_50_200', 'float_delta_hl', 'float_delta_div_hl', 'float_velocity', 
                                  'float_accel']
    list_sql_col_dt_sp500_data = ['date', 'float', 'varchar(10)', 'varchar(500)', 'float', 'float', 'float', 'float', 'float', 'float', 'float']
    list_sql_col_names_sp500_analysis = ['date_analysis', 'date_start', 'date_stop', 'dollar_start', 'int_days_range',
                                      'int_days_in_market', 'int_days_good', 'int_days_bad', 'string_in_market', 'float_ann_fee', 
                                      'dollar_gm_with_fee', 'dollar_man_fee', 'dollar_buy_hold', 'dollar_gm_no_fee', 'string_symbol']
    list_sql_col_dt_sp500_analysis = ['date', 'date', 'date', 'float', 'int', 'int', 'int', 'int', 'varchar(10)', 'float', 'float', 'float',
                                   'float', 'float', 'varchar(50)']

    dict_sql_table_col_dt = {'dbo.sp500_data':[list_sql_col_names_sp500_data, list_sql_col_dt_sp500_data],
                          'dbo.sp500_analysis':[list_sql_col_names_sp500_analysis, list_sql_col_dt_sp500_analysis]}

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # sub-section comment
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    for string_table in list_sql_tables:
        # test if table exists
        bool_sql_table_exists = SqlMethods.SqlTestTableExists(m_sql_conn, string_table)

        # if table does not exists make it
        if bool_sql_table_exists == False:
            # get column names and data types from dictionary
            list_sql_col_names, list_sql_col_dt = dict_sql_table_col_dt[string_table]
            
            # test to make sure the lists are the same length
            if len(list_sql_col_names) == len(list_sql_col_dt):
                # create list for columns
                list_sql_col_create = list()
                for int_index in range(0, len(list_sql_col_names)):
                    list_sql_col_create.append(list_sql_col_names[int_index] + ' ' + list_sql_col_dt[int_index])
                
                # create table
                list_sql_table_create_dummy = SqlMethods.SqlCreateTable(m_sql_conn, string_table, list_sql_col_create, False)
            else:
                raise Exception('list holding column names and data types are not the same length')
        else:
            pass
        pass
    pass

def ClacMetrics(m_dataframe_data):
    ###############################################################################################
    ###############################################################################################
    #
    # this method conducts the calculations for the initial load of the data
    #
    # Requirements:
    # package pandas, numpy
    #
    # Inputs:
    # dataframe_data
    # Type: pandas dataframe
    # Desc: holds the sp500 data, only the close
    #
    # Important Info:
    # None
    #
    # Return:
    # object
    # Type: pandas dataframe
    # Desc: the data with the new calculations
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # objects declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    list_dataframe_series_order = ['float_close', 'string_in_market', 'string_trigger', 'float_50_sma', 'float_200_sma', 
                                'float_delta_50_200', 'float_delta_hl', 'float_delta_div_hl', 'float_velocity', 'float_accel']
    list_nan= list()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#        
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # initialize empty lists
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #for int_index in range(0, m_dataframe_data.shape[0]):
    #    list_nan.append(numpy.nan)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # 50 and 200 sma 
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    rolling_50 = m_dataframe_data['float_close'].rolling(window = 50)
    rolling_50_sma = rolling_50.mean()
    rolling_200 = m_dataframe_data['float_close'].rolling(window = 200)
    rolling_200_sma = rolling_200.mean()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # 50 sma - 200 sma 
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    series_delta_50_200 = rolling_50_sma - rolling_200_sma

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # velocity and acceleration
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    list_velocity = [numpy.nan]
    list_acceleration = [numpy.nan, numpy.nan]
    for int_index in range(0, m_dataframe_data.shape[0]):
        if int_index >= 1:
            list_velocity.append(m_dataframe_data['float_close'].iloc[int_index] - m_dataframe_data['float_close'].iloc[int_index - 1])
        if int_index >= 2:
            list_acceleration.append(list_velocity[int_index] - list_velocity[int_index - 1])
    
    series_velocity = pandas.Series(list_velocity, name = 'velocity')
    series_acceleration = pandas.Series(list_acceleration, name = 'acceleration')

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # combine into dataframe
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    dataframe_return = pandas.DataFrame()
    dataframe_return['float_close'] = m_dataframe_data['float_close']
    dataframe_return['float_50_sma'] = rolling_50_sma.values
    dataframe_return['float_200_sma'] = rolling_200_sma.values
    dataframe_return['float_delta_50_200'] = series_delta_50_200.values
    dataframe_return['float_velocity'] = series_velocity.values
    dataframe_return['float_accel'] = series_acceleration.values
    dataframe_return['string_in_market'] = m_dataframe_data['string_in_market']
    dataframe_return['string_trigger'] = m_dataframe_data['string_trigger']
    dataframe_return['float_delta_hl'] = m_dataframe_data['float_delta_hl']
    dataframe_return['float_delta_div_hl'] = m_dataframe_data['float_delta_div_hl']

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # cleanup nan's
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #for string_series_name in dataframe_return:
    #    dataframe_return[string_series_name] = DataPrep.NanToUnknown(dataframe_return[string_series_name], 0.)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # return value; order series to fit the insert order
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    return dataframe_return[list_dataframe_series_order]

def CalcInOutMarket(m_dataframe_data, bool_initial_load):
    ###############################################################################################
    ###############################################################################################
    #
    # this method calculates if at a particular date the analysis dictates if in or out of the market
    #
    # Requirements:
    # package pandas
    # file SqlMethods
    #
    # Inputs:
    # m_dataframe_data
    # Type: pandas dataframe
    # Desc: the new data from yahoo of the s&p 500
    #
    # bool_initial_load
    # Type: boolean
    # Desc: flag to determine if the calculation is an initial load
    #
    # Important Info:
    # None
    #
    # Return:
    # object
    # Type: pandas dataframe
    # Desc: data with the market status calculated
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # objects declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if bool_initial_load == True:
        bool_in_market = True
        float_delta_high_low = m_dataframe_data['float_delta_50_200'].iloc[199]
        m_dataframe_data['float_delta_hl'].iloc[199] = float_delta_high_low
        m_dataframe_data['string_in_market'].iloc[199] = True
        int_index_start = 200
    else:
        bool_in_market = bool(m_dataframe_data['string_in_market'].iloc[0])
        float_delta_high_low = m_dataframe_data['float_delta_hl'].iloc[0]
        int_index_start = 1

    string_trigger_rule_01 = '50 sma < 200 sma'
    string_trigger_rule_02 = '50 sma / 200 sma within 5% of max low'

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # loop through the dataframe and determine if in or out of the market
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    for int_index in range(int_index_start, m_dataframe_data.shape[0]):
        # get metrics
        float_delta_high_low = m_dataframe_data['float_delta_hl'].iloc[int_index - 1]
        float_delta = m_dataframe_data['float_delta_50_200'].iloc[int_index]

        # rules
        if bool_in_market == True:
            # rule 01: if in the market and 50 sma - 200 sma < 0 get out of the market
            if float_delta < 0:
                bool_in_market = False
                float_delta_high_low = float_delta
                m_dataframe_data['string_trigger'].iloc[int_index] = string_trigger_rule_01
            else:
                if float_delta > float_delta_high_low:
                    float_delta_high_low = float_delta
        else:
            # rule 02: if out of the market and 50 sma - 200 sma / delta high low is 5% or less then get
            # into the market
            if float_delta / float_delta_high_low < 0.05:
                bool_in_market = True
                float_delta_high_low = float_delta
                m_dataframe_data['string_trigger'].iloc[int_index] = string_trigger_rule_02
            else:
                if float_delta < float_delta_high_low:
                    float_delta_high_low = float_delta
        
        # update dataframe
        m_dataframe_data['string_in_market'].iloc[int_index] = bool_in_market
        m_dataframe_data['float_delta_hl'].iloc[int_index] = float_delta_high_low
        m_dataframe_data['float_delta_div_hl'].iloc[int_index] = float_delta / float_delta_high_low

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # sectional comment
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object cleanup
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    list_float_series = ['float_50_sma', 'float_200_sma', 'float_delta_50_200', 'float_delta_hl', 'float_delta_div_hl', 
                      'float_velocity', 'float_accel']
    m_dataframe_data['string_trigger'] = DataPrep.NanToUnknown(m_dataframe_data['string_trigger'], 'None')
    m_dataframe_data['string_in_market'] = DataPrep.NanToUnknown(m_dataframe_data['string_in_market'], False)
    for string_series_name in list_float_series:
        m_dataframe_data[string_series_name] = DataPrep.NanToUnknown(m_dataframe_data[string_series_name], 0.0)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # return value
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    return m_dataframe_data

def GetDataMarketStatus(bool_initial_load = False, m_list_user = []):
    ################################################################################################
    ################################################################################################
    #
    # this method gets the data from yahoo finance, calcualtes the metrics, market status and adds it to the database
    # 
    # Requirements:
    # packge pandas, pandas_datareader, fix_yahoo_finance, numpy, datetime
    # file SqlMethods, DataPrep
    #
    # Inputs:
    # bool_initial_load
    # Type: boolean
    # Desc: the flag to determine to conduct the initial load
    #  
    # Inputs:
    # m_list_user
    # Type: list
    # Desc: a list of the user name and password for the local sql database
    # list[0] -> type: raw string; user name
    # list[1] -> type: raw string; password
    #  
    # Important Info:
    # None
    #
    # Return:
    # None
    # Type: None
    # Description: None
    ###############################################################################################
    ###############################################################################################

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # object declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    datetime_now = datetime.now()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    list_sql_table_names = ['sp500.data', 'sp500.analysis']
    list_sql_insert_dt = list()
    for int_index in range(0, 11):
        list_sql_insert_dt.append('%s')
    list_sql_insert_col = ['date_date', 'float_close', 'string_in_market', 'string_trigger', 'float_50_sma', 'float_200_sma', 
                        'float_delta_50_200', 'float_delta_hl', 'float_delta_div_hl', 'float_velocity', 'float_accel']

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    # yahoo finance query variables
    datetime_yahoo_start = datetime(1970, 1, 1)
    datetime_yahoo_stop = datetime.now()
    string_symbol_sp500 = '^GSPC'
    
    # sql database connection variables
    string_sql_host = r'localhost\SQLEXPRESS'
    string_sql_database = r'Finance'

    # flag for parse error
    bool_query_yahoo_finance = True

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # database connections
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('generating database connection')
    list_sql_conn = SqlMethods.SqlGenConnection(m_list_user[0], string_sql_host, m_list_user[1], string_sql_database)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # setup
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    if list_sql_conn[0] == True:
        print('checking database setup')
        Setup(list_sql_conn[1], list_sql_table_names)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # get data
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # get the newest date from the database
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if list_sql_conn[0] == True and bool_initial_load == False:
        # get the newest date from the database
        print('getting newest data from the database')
        string_sql_query_newest_date = SqlMethods.SqlGenSelectStatement(m_str_select = 'max(date_date)', 
                                                                        m_str_from = list_sql_table_names[0])
        list_sql_query_results_newest_date = SqlMethods.SqlQuerySelect(list_sql_conn[1], string_sql_query_newest_date)

        # check to make sure there are no errors
        if list_sql_query_results_newest_date[0] == True:
            if list_sql_query_results_newest_date[1][0][0] != None:
                string_db_newest_date = list_sql_query_results_newest_date[1][0][0]
                datetime_yahoo_start = datetime.strptime(string_db_newest_date, '%Y-%m-%d') + timedelta(days = 1)
        # if an error pull all the data from the beginning 01 Jan 1970

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # pull the data from yahoo
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('getting data from yahoo finance from %s to %s' %(datetime_yahoo_start.strftime('%d %b %Y'),
                                                         datetime_yahoo_stop.strftime('%d %b %Y')))

    int_query_count = 1
    while bool_query_yahoo_finance == True:
        try:
            dataframe_sp500_raw = data.get_data_yahoo(string_symbol_sp500, start = datetime_yahoo_start, 
                                                     stop = datetime_yahoo_stop)
        except Exception as e:
            print('in query %s of yahoo fiance a %s error occured' %(int_query_count, str(e.args)))
            int_query_count += 1
        else:
            bool_query_yahoo_finance = False
        finally:
            pass

    dataframe_sp500 = pandas.DataFrame(columns = list_sql_insert_col[1:])
    dataframe_sp500['float_close'] = dataframe_sp500_raw['Close']
    del dataframe_sp500_raw

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # conduct calculations
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#    
    
    if bool_initial_load == True and dataframe_sp500.shape[0] > 0:
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # claculate metrics
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        print('calculating metrics')
        dataframe_init_load = ClacMetrics(dataframe_sp500)

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # determine market status
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        print('calculating market status')
        dataframe_init_load =  CalcInOutMarket(dataframe_init_load, True)

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # insert into database
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        print('inserting values into the database')
        for int_index in range(0, dataframe_init_load.shape[0]):
            list_values = list(dataframe_init_load.iloc[int_index])
            list_values.insert(0, dataframe_init_load.index[int_index]._date_repr)
            list_dummy_insert = SqlMethods.SqlInsertIntoTable(list_sql_conn[1], list_sql_table_names[0], list_sql_insert_col,
                                                     list_sql_insert_dt, list_values)

    elif bool_initial_load == False and dataframe_sp500.shape[0] > 0:    
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # get data from database
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        # get start date
        print('getting the 200 records for calculation')
        datetime_begin = datetime.strptime(string_db_newest_date, '%Y-%m-%d') - timedelta(days = 200)
        string_date_begin = datetime_begin.strftime('%Y-%m-%d')
        #string_sql_query_where = "date_date <= '" + string_db_newest_date + "' and date_date >= '" + string_date_begin + "'"
        string_sql_query_where = "date_date <= '" + string_db_newest_date + "'"

        string_sql_query_200 = SqlMethods.SqlGenSelectStatement(m_str_select = 'top(200) *', 
                                                          m_str_from = list_sql_table_names[0], 
                                                          m_str_where = string_sql_query_where, 
                                                          m_str_end = 'order by date_date desc')

        dataframe_200 = pandas.read_sql(string_sql_query_200, list_sql_conn[1])
        dataframe_200 = dataframe_200.sort_values(by = ['date_date'], ascending = True)
        list_timestamp = list()
        for string_date in dataframe_200['date_date']:
            datetime_temp = datetime.strptime(string_date, '%Y-%m-%d')
            #list_timestamp.append(datetime_temp.timestamp())
            list_timestamp.append(datetime_temp)
        dataframe_200.index = list_timestamp
        dataframe_200 = dataframe_200.drop('date_date', axis = 1)
        dataframe_new = pandas.concat([dataframe_200, dataframe_sp500], axis = 0)

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # claculate metrics
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        print('calculating metrics')
        dataframe_new = ClacMetrics(dataframe_new.copy())
        dataframe_new = dataframe_new.ix[199:]

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # determine market status
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        print('calculating market status')
        dataframe_new = CalcInOutMarket(dataframe_new.copy(), False)
        dataframe_new = dataframe_new.ix[1:]
        # code here

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # insert into database
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        print('inserting values into the database')
        for int_index in range(0, dataframe_new.shape[0]):
            list_values = list(dataframe_new.iloc[int_index])
            list_values.insert(0, dataframe_new.index[int_index]._date_repr)
            list_dummy_insert = SqlMethods.SqlInsertIntoTable(list_sql_conn[1], list_sql_table_names[0], list_sql_insert_col,
                                                     list_sql_insert_dt, list_values)

    elif dataframe_sp500.shape[0] == 0:
        # no new records for the sp500
        print('no new records for SP500, analysis is up to date')
    
    else:
        pass

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object cleanup
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if list_sql_conn[0] == True:
        list_sql_conn[1].close()

def ConductAnalysis(datetime_oldest = datetime(1970, 1, 1), datetime_newest = datetime.now(), 
                    float_initial_investment = 1000., float_annual_fee = 0.02, m_list_user = []):
    ###############################################################################################
    ###############################################################################################
    #
    # this method implemetns the analysis of the market status
    #
    # Requirements:
    # file DataPrep, SqlMethods
    # package pandas, datetime, numpy
    #
    # Inputs:
    # datetime_oldest
    # Type: datetime
    # Desc: the start date of when to pull the data
    #
    # datetime_newest
    # Type: datetime
    # Desc: the stop date of the end date to pull the data
    #    
    # float_initial_investment
    # Type: float
    # Desc: the dollar amount of the initial investment
    #    
    # float_annual_fee
    # Type: float
    # Desc: the annual fee which will be calculated quarterly
    #    
    # m_list_user
    # Type: list
    # Desc: a list of the user name and password for the local sql database
    # list[0] -> type: raw string; user name
    # list[1] -> type: raw string; password
    #  
    # Important Info:
    # None
    #
    # Return:
    # n/a
    # Type: n/a
    # Desc: n/a
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # objects declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # date / time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    datetime_analysis = datetime.now()
    string_date_of_analysis = datetime_analysis.strftime('%Y-%m-%d')
    string_date_oldest = datetime_oldest.strftime('%Y-%m-%d')
    string_date_newest = datetime_newest.strftime('%Y-%m-%d')

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    list_sql_table_names = ['sp500.data', 'sp500.analysis']

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    # sql database conection variables
    string_sql_host = r'localhost\SQLEXPRESS'
    string_sql_database = r'Finance'

    # info variables
    string_symbol_sp500 = '^GSPC'

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # connect to the databse
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('connecting to database')
    list_sql_conn = SqlMethods.SqlGenConnection(m_list_user[0], string_sql_host, m_list_user[1], string_sql_database)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # get data from the database
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('pulling data from database')
    if list_sql_conn[0] == True:
        string_sql_query_where = "date_date >= '" + string_date_oldest + "' and date_date <= '" + string_date_newest + "'"
        string_sql_query_end = 'order by date_date'
        string_sql_query = SqlMethods.SqlGenSelectStatement(m_str_select = '*', m_str_from = list_sql_table_names[0],
                                                      m_str_where = string_sql_query_where, m_str_end = string_sql_query_end)
        dataframe_data = pandas.read_sql(string_sql_query, list_sql_conn[1])

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # begin calculations
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # basic numbers
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('begin calculations')
    if dataframe_data.shape[0] > 0:
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # day counts
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        print('conducting days calculations')
        # days pulled from database
        string_date_first = dataframe_data['date_date'].ix[0]
        string_date_last = dataframe_data['date_date'].ix[dataframe_data.shape[0] - 1]

        # days in range
        int_days_in_range = dataframe_data.shape[0]

        # market status
        string_market_status = dataframe_data['string_in_market'].ix[dataframe_data.shape[0] - 1]

        # days in the market
        array_in_market = dataframe_data['string_in_market'] == 'True'
        dataframe_in_market = dataframe_data.ix[array_in_market]
        int_days_in_market = dataframe_in_market.shape[0]

        # bad days
        array_trigger = dataframe_data['string_trigger'] != 'None'
        dataframe_trigger = dataframe_data.ix[array_trigger]
        
        # replace index to interate
        list_index_new = list()
        for int_index in range(0, len(dataframe_trigger.index)):
            list_index_new.append(int_index)
        dataframe_trigger.index = list_index_new
        
        int_days_bad = 0
        for int_index in range(0, dataframe_trigger.shape[0] - 1):
            # get the start market status
            if int_index == 0:
                string_status_start = dataframe_data['string_in_market'].ix[0]
            else:
                string_status_start = dataframe_trigger['string_in_market'].ix[int_index]
            
            # get the end market satus
            string_status_end = dataframe_trigger['string_in_market'].ix[int_index + 1]
            
            # calculate based on the a change of market status or not
            if string_status_start == 'True' and string_status_end == 'False':
                # get sp500 values
                float_sp500_start = dataframe_trigger['float_close'].ix[int_index]
                float_sp500_end = dataframe_trigger['float_close'].ix[int_index + 1]

                # get bad days
                if float_sp500_end < float_sp500_start:
                    string_date_bad_start = dataframe_trigger['date_date'].ix[int_index]
                    string_date_bad_end = dataframe_trigger['date_date'].ix[int_index + 1]
                    datetime_bad_start = datetime.strptime(string_date_bad_start, '%Y-%m-%d')
                    datetime_bad_end = datetime.strptime(string_date_bad_end, '%Y-%m-%d')
                    timedelta_bad = datetime_bad_end - datetime_bad_start
                    int_days_bad = int_days_bad + timedelta_bad.days

        # calculate good days
        int_days_good = int_days_in_market - int_days_bad

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # conduct amount calculations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        print('conducting amount calculations')
        # calculate dollar amounts
        float_man_fee = 0
        float_gm_with_fee = float_initial_investment
        float_gm_without_fee = float_initial_investment
        for int_index in range(1, dataframe_data.shape[0]):
            # get dates
            string_date_calc_start = dataframe_data['date_date'].ix[int_index - 1]
            string_date_calc_stop = dataframe_data['date_date'].ix[int_index]
            datetime_calc_start = datetime.strptime(string_date_calc_start, '%Y-%m-%d')
            datetime_calc_stop = datetime.strptime(string_date_calc_stop, '%Y-%m-%d')

            # get closes
            float_close_calc_start = dataframe_data['float_close'].ix[int_index - 1]
            float_close_calc_stop = dataframe_data['float_close'].ix[int_index]
            float_ratio_return = float_close_calc_stop / float_close_calc_start
            if int_index == 1:
                float_close_initial = float_close_calc_start
            if int_index == dataframe_data.shape[0] - 1:
                float_close_final = float_close_calc_stop

            # get market status
            string_ms_start = dataframe_data['string_in_market'].ix[int_index - 1]
            string_ms_stop = dataframe_data['string_in_market'].ix[int_index]

            # calc amounts
            if string_ms_start == 'True' and string_ms_stop == 'True':
                float_gm_with_fee = float_gm_with_fee * float_ratio_return
                float_gm_without_fee = float_gm_without_fee * float_ratio_return

            # calc fee
            # get start datetime
            if int_index == 1:
                datetime_quarter_start = datetime_calc_start

            # account for new year
            if datetime_quarter_start.year != datetime_calc_stop.year:
                datetime_quarter_start = datetime_calc_stop

            # calc diff in dates
            timedelta_fee = datetime_calc_stop - datetime_quarter_start

            # test for quarter
            if timedelta_fee.days == 90:
                # reset new quarter date
                datetime_quarter_start = datetime_calc_stop + timedelta(days = 1)

                # calculate management fee and reduce balance
                float_man_fee = float_man_fee + (float_gm_with_fee * float_annual_fee / 4)
                float_gm_with_fee = float_gm_with_fee * (1 - (float_annual_fee / 4))

        # buy a hold calculation
        float_buy_hold = float_initial_investment * (float_close_final / float_close_initial)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # insert results into database
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('inserting results of analysis into database')
    list_sql_insert_columns = ['date_analysis', 'date_start', 'date_stop', 'dollar_start', 'int_days_range', 
                            'int_days_in_market', 'int_days_good', 'int_days_bad', 'string_in_market', 'float_ann_fee',
                            'dollar_gm_with_fee', 'dollar_man_fee', 'dollar_buy_hold', 'dollar_gm_no_fee', 'string_symbol']
    list_sql_insert_values = [string_date_of_analysis, string_date_first, string_date_last, float_initial_investment,
                       int_days_in_range, int_days_in_market, int_days_good, int_days_bad, string_market_status, float_annual_fee,
                       float_gm_with_fee, float_man_fee, float_buy_hold, float_gm_without_fee, string_symbol_sp500]
    list_sql_insert_dt = list()
    for element in list_sql_insert_values:
        list_sql_insert_dt.append('%s')

    list_insert_dummy = SqlMethods.SqlInsertIntoTable(list_sql_conn[1], list_sql_table_names[1], list_sql_insert_columns,
                                                   list_sql_insert_dt, list_sql_insert_values)

def CreateVisualization(m_datetime_start = datetime(1970, 1, 1), m_datetime_stop = datetime.now(), m_list_user = []):
    ###############################################################################################
    ###############################################################################################
    #
    # this method visualizes the data and the analysis from the sp500
    #
    # Requirements:
    # package datetime, pandas, matplotlib.pyplot
    # file SqlMethods
    #
    # Inputs:
    # m_datetime_start
    # Type: datetime
    # Desc: the date of the start of the visualization (oldest date)
    #
    # m_datetime_stop
    # Type: datetime
    # Desc: the date to stop the analysis (newest date)
    #    
    # m_list_user
    # Type: list
    # Desc: a list of the user name and password for the local sql database
    # list[0] -> type: raw string; user name
    # list[1] -> type: raw string; password
    #  
    # Important Info:
    # None
    #
    # Return:
    # n/a
    # Type: n/a
    # Desc: n/a
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # objects declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    # pplot style
    style.use('ggplot')

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    string_date_oldest = m_datetime_start.strftime('%Y-%m-%d')
    string_date_newest = m_datetime_stop.strftime('%Y-%m-%d')

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    # list of lists
    # list_in_market[x][0] -> np array of strings; dates that are x values in the market
    # list_in_market[x][1] -> mp array of floats; y values which are the market closes
    list_in_market = list()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    # sql database connection variables
    string_sql_host = r'localhost\SQLEXPRESS'
    string_sql_database = r'Finance'

    # sql database tables
    string_sql_table_data = r'sp500.data'
    string_sql_table_analysis = r'sp500.analysis'

    # info variables
    string_symbol_sp500 = '^GSPC'

    # path variables
    string_path = 'C:\\Users\\Frosty SB 02\\Documents\\Development\\Projects.Active\\Finance\\sp_500_20170607\\'
    string_path += 'visualizations\\'
    string_file = 'sp500_visualization_'  + m_datetime_stop.strftime('%Y-%m-%d %H_%M_%S') + '.png'

    # plot variables
    x = 0
    y_sp500 = 0
    y_200_sma = 0
    y_50_sma = 0
    float_y_max = 0
    float_y_min = 0
    array_vertical_lines = 0

    # error booleans
    bool_error_geting_data = False

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # get data from database
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # establish connection
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    print('connecting to database')
    list_sql_conn = SqlMethods.SqlGenConnection(m_list_user[0], string_sql_host, m_list_user[1], string_sql_database)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # query data
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if list_sql_conn[0] == True:
        print('getting data in date range')
        string_sql_query_where = "date_date >= '" + string_date_oldest + "' and date_date <= '" + string_date_newest + "'"
        string_sql_query_end = 'order by date_date'
        string_sql_query = SqlMethods.SqlGenSelectStatement(m_str_select = '*', m_str_from = string_sql_table_data,
                                                      m_str_where = string_sql_query_where, m_str_end = string_sql_query_end)
        try:
            dataframe_data = pandas.read_sql(string_sql_query, list_sql_conn[1])
        except Exception as e:
            string_e_args = str(e.args)
            bool_error_geting_data = True
            string_print_error = 'There was an error getting the data from the database: ' + string_e_args
            string_print_error += '.  Research and come back "dumkopf"!'
            print(string_print_error)
        else:
            # get the data from the dataframes
            x = dataframe_data['date_date'].values
            for int_index in range(0, len(x)):
                x[int_index] = datetime.strptime(x[int_index], '%Y-%m-%d')
            y_sp500 = dataframe_data['float_close'].values
            y_200_sma = dataframe_data['float_200_sma'].values
            y_50_sma = dataframe_data['float_50_sma'].values

            # get the triggers on when in and out of the market
            array_trigger = dataframe_data['string_trigger'] != 'None'
            dataframe_triggers = dataframe_data[array_trigger]
            index_df_trigger_index = dataframe_triggers.index

            # check the first element of the data from the database to ensure it is in In the market
            if dataframe_triggers['string_in_market'].iloc[0] == 'False':
                int_start = 1
            else:
                int_start = 0

            # create a list of row numbers in the dataframe to plot the in market lines
            # if the first value in the data is not in the market in the trigger dataframe
            if int_start == 1:
                # get the index for the dataframe
                int_loc_01 = index_df_trigger_index[0]
                list_in_market.append([dataframe_data['date_date'].iloc[0:int_loc_01 + 1].values,
                                                        dataframe_data['float_close'].iloc[0:int_loc_01 + 1].values])

            # loop through the dataframe of triggers to get the values for the in market for the plot
            for int_index in range(int_start, len(index_df_trigger_index) - 1):
                # get the indexes from the dataframe_triggers for the dataframe_data
                int_loc_01 = index_df_trigger_index[int_index]
                int_loc_02 = index_df_trigger_index[int_index + 1]

                # compare the markets status
                string_market_status_01 = dataframe_triggers['string_in_market'].iloc[int_index]
                string_market_status_02 = dataframe_triggers['string_in_market'].iloc[int_index + 1]

                # check if the market is in
                if string_market_status_01 == 'True' and string_market_status_02 == 'False':
                    list_in_market.append([dataframe_data['date_date'].iloc[int_loc_01:int_loc_02 + 1].values,
                                                           dataframe_data['float_close'].iloc[int_loc_01:int_loc_02 + 1].values])

            # get the vertical lines for the charts
            array_df_trigger_false = dataframe_triggers['string_in_market'] == 'False'
            array_df_trigger_true = dataframe_triggers['string_in_market'] == 'True'
            list_vertical_lines_false = list(dataframe_triggers[array_df_trigger_false]['date_date'].values)
            list_vertical_lines_true = list(dataframe_triggers[array_df_trigger_true]['date_date'].values)
                    
            # check the last value, if true then add to the end of the dataframe
            if dataframe_triggers['string_in_market'].iloc[len(index_df_trigger_index) - 1] == 'True':
                # get the last two locations
                int_loc_01 = index_df_trigger_index[-1]
                int_loc_02 = dataframe_data.shape[0] - 1

                # add last element into the market
                list_in_market.append([dataframe_data['date_date'].iloc[int_loc_01:int_loc_02 + 1].values,
                                                        dataframe_data['float_close'].iloc[int_loc_01:int_loc_02 + 1].values])

            # get max and min y values
            float_y_max = max(dataframe_data['float_close']) + 50
            float_y_min = min(dataframe_data['float_close']) - 50

            # convert dates to a datetime element for plotting
            #for plot_in_market in list_in_market:
            #    for int_index in range(0, len(plot_in_market[0])):
            #        plot_in_market[0][int_index] = datetime.strptime(plot_in_market[0][int_index], '%Y-%m-%d')

            #for int_index in range(0, len(array_vertical_lines)):
            #    array_vertical_lines[int_index] = datetime.strptime(array_vertical_lines[int_index], '%Y-%m-%d')
        finally:
            pass

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # plot the data
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # create figures and axes
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if bool_error_geting_data == False and list_sql_conn[0] == True:
        # create the figure and the axes for the plots
        # plot 1 (upper) is the sp500 and in's and outs
        # plot 2 (lower) is the 200 and 50 sma's
        print('generateing visualization')
        fig, axes = pyplot.subplots(2, 1) # one figure with two plots (2 rows, 1 column)
        fig.set_size_inches(10., 7.)  #  10 inches width, 7 inches high

        #upper plot
        axes[0].plot(x, y_sp500, color = 'black', linewidth = 2, linestyle = '-', label = 'SP500')
        bool_label = True
        for plot_in_market in list_in_market:
            if bool_label == True:
                bool_label = False
                axes[0].plot(plot_in_market[0], plot_in_market[1], color = 'green', linewidth = 2.5, linestyle = '-', label = 'In Market')
            else:
                axes[0].plot(plot_in_market[0], plot_in_market[1], color = 'green', linewidth = 2.5, linestyle = '-')
        
        # upper plot elements
        axes[0].set(title = 'In / Out of Market', xlabel = 'date of close', ylabel = 'close')
        axes[0].set_ylim(float_y_min, float_y_max)
        axes[0].legend(loc = 'best')

        # lower plot
        axes[1].plot(x, y_200_sma, color = 'blue', linewidth = 2, linestyle = '-', label = '200 sma')
        axes[1].plot(x, y_50_sma, color = 'red', linewidth = 2, linestyle = '-', label = '50 sma')

        # plot vertical lines on both axes
        bool_label_01 = True
        for x_val in list_vertical_lines_false:
            if bool_label_01 == True:
                axes[0].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to get out')
                axes[1].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to get out')
                bool_label_01 = False
            else:
                axes[0].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--')
                axes[1].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--')

        bool_label_02 = True
        for x_val in list_vertical_lines_true:
            if bool_label_02 == True:
                axes[0].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to buy in')
                axes[1].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to buy in')
                bool_label_02 = False
            else:
                axes[0].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--')
                axes[1].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--')
        
        # lower plot elements
        axes[1].set(title = '200 & 50 sma', xlabel = 'date of close', ylabel = 'close')
        axes[1].set_ylim(float_y_min, float_y_max)
        axes[1].legend(loc = 'best')

        # plot elements
        pyplot.subplots_adjust(wspace = None, hspace = 0.4)
        pyplot.suptitle('SP500 Analysis')
        #pyplot.show()
        pyplot.savefig(string_path + string_file)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # close connection
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    if list_sql_conn[0] == True:
        list_sql_conn[1].close()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Main Method
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

def Main(m_list_user):
    ################################################################################################
    ################################################################################################
    #
    # this is the main method new change another
    # 
    # Requirements:
    # None
    #
    # Inputs:
    # m_list_user
    # Type: list
    # Desc: a list of the user name and password for the local sql database
    # list[0] -> type: raw string; user name
    # list[1] -> type: raw string; password
    #  
    # Important Info:
    # None
    #
    # Return:
    # None
    # Type: None
    # Description: None
    ###############################################################################################
    ###############################################################################################

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # object declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # time declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # lists declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # variables declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    datetime_start = datetime(1995, 1, 1)
    datetime_stop = datetime.now()
    float_money = 3000
    float_annual_fee = 0.02

    # control flags
    bool_get_data = True
    bool_conduct_analysis = True
    bool_generate_visulaization = True

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # get data and market status
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if bool_get_data == True:
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        print('getting data from yahoo')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')

        GetDataMarketStatus(m_list_user = m_list_user)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # get data and market status
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if bool_conduct_analysis == True:
        print('\n-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        print('analyzing data')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')

        ConductAnalysis(datetime_start, datetime_stop, float_money, float_annual_fee, m_list_user)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # create visualization
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    if bool_generate_visulaization == True:
        print('\n-------------------------------------------------------------')
        print('-------------------------------------------------------------')
        print('plotting data')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')

        CreateVisualization(datetime_start, datetime_stop, m_list_user)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # sectional comment
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object cleanup
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    pass

# call Start()
#if __name__ == '__main__':
#    Main()