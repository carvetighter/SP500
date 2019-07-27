'''
Sp500 class file

File containtes four classes:
Sp500 base class -> used for containers and setup for child classes
Sp500 data collection class -> used to collect the data from yahoo finance and a local sql database
Sp500 analysis class -> conducts the analysis between the moving averages
Sp500 visualizations class -> conducts the visualizations of the analysis
'''

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

from datetime import datetime
# from datetime import time
from datetime import timedelta
# from datetime import timezone
import fix_yahoo_finance
import numpy
import os
from matplotlib import pyplot
from matplotlib import style
from SqlMethods import SqlMethods

# fix for is_list_like error
import pandas
pandas.core.common.is_list_like = pandas.api.types.is_list_like
from pandas_datareader import data
# import pandas_datareader

# ignore warnings
import warnings
warnings.simplefilter('ignore')

class Sp500Base(object):
    '''
    Base class for analysis; containes all the containers

    Requirements:
    package SqlMethods
    package pandas

    Methods:
    check_sql_db_setup()
        - checks if the table exists and the columns are the same as the dictionary
          in the constructor

    Attributes:
    ??
    '''

    #--------------------------------------------------------------------------#
    # constructor
    #--------------------------------------------------------------------------#

    def __init__(self, c_list_sql_up, c_bool_verbose):
        '''
        base class construtor

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        c_list_sql_up
        Type: list
        Desc: user and password for sql database
        c_list_sql_up[0] -> type: string; user name
        c_list_sql_up[1] -> type: string; password

        c_bool_verbose
        Type: boolean
        Desc: flag if verbose output desired

        Important Info:
        1. format for list to connec to sql db
            [r'<user name>', r'<sql server name>', r'<user password>', r'<database name>']

        Attributes:
        sql_conn
        Type: SqlMethods object
        Desc: connection to local sql express database on external drive

        dict_sp500_tables
        Type: dictionary
        Desc: the tables in the database segemented by category
            level 00 -> 'data' or 'analysis'
            level 01 -> 
                'table_name' -> string; format 'schema name. table name'
                'col_dtype' -> list; sql column data types to create table
                'col_names' -> list; column names
        '''
        #--------------------------------------------------------------------------#
        # sql db connection attributes
        #--------------------------------------------------------------------------#

        self.string_sql_db = r'Finance'
        self.string_sql_server = r'localhost\SQLEXPRESS'
        self.sql_conn = SqlMethods(
            [c_list_sql_up[0],
            self.string_sql_server,
            c_list_sql_up[1],
            self.string_sql_db])
        self.string_sym_sp500 = '^SPX'
        self.dt_sp500_start = datetime(1970, 1, 1)
        self.dt_sp500_stop = datetime.now()

        #--------------------------------------------------------------------------#
        # sql db data attributes
        #--------------------------------------------------------------------------#

        self.dict_sp500_tables = {
            'data':{
                'table_name':'sp500.data',
                'col_dtype':['date', 'float', 'varchar(10)', 'varchar(500)', 'float', 'float', 'float', 'float', 'float',
                    'float', 'float'],
                'col_names':['date_date', 'float_close', 'string_in_market', 'string_trigger', 'float_50_sma',
                    'float_200_sma', 'float_delta_50_200', 'float_delta_hl', 'float_delta_div_hl', 'float_velocity',
                    'float_accel']},
            'analysis':{
                'table_name':'sp500.analysis',
                'col_dtype':['date', 'date', 'date', 'float', 'int', 'int', 'int', 'int', 'varchar(10)', 'float', 'float', 'float',
                    'float', 'float', 'varchar(50)'],
                'col_names':['date_analysis', 'date_start', 'date_stop', 'dollar_start', 'int_days_range',
                    'int_days_in_market', 'int_days_good', 'int_days_bad', 'string_in_market', 'float_ann_fee',
                    'dollar_gm_with_fee', 'dollar_man_fee', 'dollar_buy_hold', 'dollar_gm_no_fee',
                    'string_symbol']}}
        self.tup_sql_db_setup = (False, 'not checked')
        self.bool_initial_load = False

        #--------------------------------------------------------------------------#
        # other attributes
        #--------------------------------------------------------------------------#

        self.bool_verbose = c_bool_verbose
        self.list_errors = list()

    #--------------------------------------------------------------------------#
    # callable methods
    #--------------------------------------------------------------------------#

    def check_sql_db(self):
        '''
        this method is a wrapper to check the sql database structure and
        setup for the analysis;
            - checks if the tables are in the database
            - checks if all the columns are in the appropriate table

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        none
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        object
        Type: tuple
        Desc: if the database is structured for the analysis and any errors that
            are detected; if tuple[0] is True the tables exists and the columns names are
            the same as the dictionary
        tuple[0] -> type: boolean; True of db is setup for the analysis, False if not
        tuple[1] -> type: string; if tuple[0] is True then empty string; if tuple[0] is
            False than any errors that are detected; errors are separated by double
            pipes '||'
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # iterator declarations
        #--------------------------------------------------------------------------------#

        tup_return = None

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        string_check_setup = 'checking sql setup for analysis'
        string_sql_good_setup = 'sql database is setup correctly'
        bool_create_tables = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # check the sql database structure
        #--------------------------------------------------------------------------------#

        if self.bool_verbose:
            print(string_check_setup)
        bool_db_check = self._check_sql_db_setup()
        if bool_db_check:
            if self.bool_verbose:
                print(string_sql_good_setup)
            tup_return = (bool_db_check, '')
        else:
            bool_create_tables = self._create_sql_db_tables()
            if bool_create_tables:
                string_errors = ''
            else:
                string_errors = '||'.join(self.list_errors)
            tup_return = (bool_create_tables, string_errors)
        self.tup_sql_db_setup = tup_return

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return tup_return

    def error_sql_db(self):
        '''
        this method prints the error message to the screen and returns the error

        Requirements:
        none

        Inputs:
        none
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: string
        Desc: error message if sql database is not set-up correctly
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        string_error_00 = 'sql database is not setup for analysis; check code'
        string_error_00 += ' and sql database for the proper setup'

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        if self.bool_verbose:
            print(string_error_00)
        
        #--------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------#

        return string_error_00
    
    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def _check_sql_db_setup(self):
        '''
        this method checks the sql database for the correct structure

        Requirements:
        package SqlMethods

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: method executes as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
        set_bool_return = set()

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # test for connection and begin looping through tables
        #--------------------------------------------------------------------------------#

        if self.sql_conn.bool_is_connected:
            for string_key in self.dict_sp500_tables:

                #--------------------------------------------------------------------------------#
                # set table boolean check and get table information
                #--------------------------------------------------------------------------------#

                bool_table_check = False
                dict_table = self.dict_sp500_tables.get(string_key, None)
                string_table = dict_table.get('table_name', None)
                bool_table_exists = self.sql_conn.table_exists(string_table)
                
                #--------------------------------------------------------------------------------#
                # begin table check
                #--------------------------------------------------------------------------------#

                if bool_table_exists:
                    list_table_columns = self.sql_conn.get_table_columns(string_table)
                    if list_table_columns[0]:
                        set_columns = set(list_table_columns[1])
                        set_dict_columns = set(dict_table.get('col_names'))
                        if set_columns == set_dict_columns:
                            bool_table_check = True
                        else:
                            string_error_db_check_02 = 'table {0} columns do not match'
                            self.list_errors.append(string_error_db_check_02.format(string_table))
                    else:
                        string_error_db_check_00 = 'table {0} error retrieving columns'
                        self.list_errors.append(string_error_db_check_00.format(string_table))
                else:
                    string_error_db_check_01 = 'table {0} does not exist'
                    self.list_errors.append(string_error_db_check_01.format(string_table))

                # add boolean to set for check
                set_bool_return.add(bool_table_check)
        else:
            self.list_errors.append('no connection to sql database')
            bool_return = False

        #--------------------------------------------------------------------------------#
        # for each table determine the return boolean
        #--------------------------------------------------------------------------------#

        if set_bool_return == {True}:
            bool_return = True

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _create_sql_db_tables(self):
        '''
        this method creates the sql database tables based on the error string passed

        Requirements:
        package SqlMethods

        Inputs:
        none
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: method executes as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # iterator declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
        bool_table = False
        list_errors = list()
        set_bool_return = set()

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # test for connection and begin looping through tables
        #--------------------------------------------------------------------------------#

        series_db_errors = pandas.Series(data = self.list_errors)
        series_tables = series_db_errors.apply(
            lambda x: x.split(' ')[1])
        set_tables = set(series_tables.values)
        if 'connection' in set_tables:
            set_tables.remove('connection')
        del series_tables, series_db_errors

        #--------------------------------------------------------------------------------#
        # loop through tables and create table
        #--------------------------------------------------------------------------------#

        if self.sql_conn.bool_is_connected:
            for string_table in set_tables:

                #--------------------------------------------------------------------------------#
                # get table dictionary
                #--------------------------------------------------------------------------------#

                bool_table = False
                for string_key in self.dict_sp500_tables:
                    dict_table = self.dict_sp500_tables.get(string_key, None)
                    if dict_table.get('table_name', None) == string_table:
                        dict_test_table = dict_table
                        break
                    else:
                        dict_test_table = None

                #--------------------------------------------------------------------------------#
                # test to ensure table is in dictionary
                #--------------------------------------------------------------------------------#

                if isinstance(dict_table, dict):
                    bool_table_dictionary = True
                else:
                    bool_table_dictionary = False

                #--------------------------------------------------------------------------------#
                # create tables
                #--------------------------------------------------------------------------------#

                if bool_table_dictionary:

                    #--------------------------------------------------------------------------------#
                    # create list to create columns
                    #--------------------------------------------------------------------------------#

                    series_col_name = pandas.Series(dict_test_table.get('col_names'))
                    series_col_type = pandas.Series(dict_test_table.get('col_dtype'))
                    series_create = series_col_name + ' ' + series_col_type
                    list_columns = list(series_create.values)
                    del series_col_name, series_col_type, series_create

                    #--------------------------------------------------------------------------------#
                    # create table
                    #--------------------------------------------------------------------------------#

                    list_create_table = self.sql_conn.create_table(
                        m_string_table = string_table,
                        m_list_columns = list_columns,
                        m_bool_wide_table = False,
                        m_bool_compression = True)

                    #--------------------------------------------------------------------------------#
                    # add errors and boolean for return tuple
                    #--------------------------------------------------------------------------------#

                    bool_table = list_create_table[0]
                    list_errors.append(list_create_table[1])
                else:
                    string_error_crete_table_00 = 'table {0} not in table dictionary'
                    self.list_errors.append(string_error_crete_table_00.format(string_table))

                #--------------------------------------------------------------------------------#
                # create return set to test return boolean
                #--------------------------------------------------------------------------------#

                set_bool_return.add(bool_table)
        else:
            self.list_errors.append('no connection to sql database')
            set_bool_return.add(bool_table)

        #--------------------------------------------------------------------------------#
        # for each table determine the return boolean
        #--------------------------------------------------------------------------------#

        if set_bool_return == {True}:
            bool_return = True

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _nan_to_unknown(self, m_pandas_series, m_replacement = '', bool_string = False):
        '''
        this method replaces all the nan values (which is a float in python / numpy)
        
        Requirements:
        package pandas
        
        Inputs:
        m_pandas_series
        Type: pandas series
        Desc: the data to clean
        
        m_replacement
        Type: variable / multiple
        Desc: the replacement value for numpy.nan
        
        bool_string
        Type: boolean
        Desc: flag to test series as a string or a float
        
        Important Info:
        None

        Return:
        object
        Type: pandas series
        Desc: the dataframe where each nan value is converted to a string 'Unknown'
        '''

        #--------------------------------------------------------------------------#
        # package import
        #--------------------------------------------------------------------------#

        #--------------------------------------------------------------------------#
        # variable / object declarations
        #--------------------------------------------------------------------------#

        # variables
        if m_replacement == '':
            m_replacement = 'Unknown'

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------#
        # replacing na / nan values with space
        #--------------------------------------------------------------------------#

        if m_pandas_series.hasnans is True and bool_string is False:
            series_nan = m_pandas_series.isnull()
            m_pandas_series.loc[series_nan.values] = m_replacement

        if bool_string is True:
            m_pandas_series.loc[m_pandas_series == 'nan'] = m_replacement

        #--------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------#

        return m_pandas_series

class Sp500Data(Sp500Base):
    '''
    This class connects to an external data source and pulls the sp500 data,
    conducts in / out calculations

    Requirements:
    package SqlMethods
    package pandas
    class Sp500Base()

    Methods:
    data_wrapper()

    Attributes:
    Sp500Base() attributes
    '''

    #--------------------------------------------------------------------------#
    # constructor
    #--------------------------------------------------------------------------#

    def __init__(self, csd_list_sql_up, csd_bool_verbose):
        '''
        class construtor

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        c_list_sql_up
        Type: list
        Desc: user and password for sql database
        c_list_sql_up[0] -> type: string; user name
        c_list_sql_up[1] -> type: string; password

        c_bool_verbose
        Type: boolean
        Desc: flag if verbose output desired

        Important Info:
        1. None

        Attributes:
        calss Sp500Base() attributes
        '''
        #--------------------------------------------------------------------------#
        # call parent constructor
        #--------------------------------------------------------------------------#

        Sp500Base.__init__(
            self,
            c_list_sql_up = csd_list_sql_up,
            c_bool_verbose = csd_bool_verbose)
        
        #--------------------------------------------------------------------------#
        # get data attributes
        #--------------------------------------------------------------------------#
        
        dict_table = self.dict_sp500_tables.get('data')
        self.bool_query_stooq_data = True
        self.string_table = dict_table.get('table_name')
        self.list_columns = dict_table.get('col_names')
        
        #--------------------------------------------------------------------------#
        # data containers
        #--------------------------------------------------------------------------#

        self.df_raw_stooq = None
        self.df_200_data = None
        self.df_metrics = None

    #--------------------------------------------------------------------------#
    # callable methods
    #--------------------------------------------------------------------------#

    def data_wrapper(self):
        '''
        this method is the wrapper to pull data from the database
        and stooq

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        
        Type: 
        Desc: 

        Important Info:
        None

        Return:
        object
        Type: tuple
        Desc: length = 2; 
        tuple[0] -> type: boolean; if wrapper method is successful
        tuple[1] -> type: string; if tuple[0] == True empty string; else
            string with errors
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # get max date
        #--------------------------------------------------------------------------------#

        if self.bool_verbose:
            print('getting date to start query for sp500')
        bool_max_date = self._get_max_date_from_db()

        #--------------------------------------------------------------------------------#
        # get data from yahoo finance
        #--------------------------------------------------------------------------------#

        if bool_max_date:
            if self.bool_verbose:
                print('get sp500 data')
            bool_sp500 = self._get_sp500_data()
        else:
            string_error_max_date = 'error in calculating the max date to pull data for sp500'
            self.list_errors.append(string_error_max_date)
            bool_sp500 = False,
            if self.bool_verbose:
                print(string_error_max_date)

        #--------------------------------------------------------------------------------#
        # get latest 200 records from sp500 database
        #--------------------------------------------------------------------------------#

        if bool_sp500:
            if self.bool_verbose:
                print('getting latest 200 records from database')
            bool_200 = self._get_200_from_db()
        else:
            string_error_sp500 = 'error in pulling sp500 data from stooq through pandas_datareader'
            self.list_errors.append(string_error_sp500)
            bool_200 = False
            if self.bool_verbose:
                print(string_error_sp500)

        #--------------------------------------------------------------------------------#
        # caclualte metrics
        #--------------------------------------------------------------------------------#

        if bool_200:
            if self.bool_verbose:
                print('calculating metrics')
            bool_calc = self._calc_metrics()
        else:
            string_error_200 = 'error in pulling 200 records from local sql db'
            self.list_errors.append(string_error_200)
            bool_calc = False
            if self.bool_verbose:
                print(string_error_200)

        #--------------------------------------------------------------------------------#
        # caclulate in or out of the market
        #--------------------------------------------------------------------------------#

        if bool_calc:
            if self.bool_verbose:
                print('calculating in out metrics')
            bool_inout = self._calc_inout_market()
        else:
            string_error_calc = 'error in caclulating metrics for market assessment'
            self.list_errors.append(string_error_calc)
            bool_inout = False
            if self.bool_verbose:
                print(string_error_calc)

        #--------------------------------------------------------------------------------#
        # insert results into sql database
        #--------------------------------------------------------------------------------#

        if bool_inout:
            if self.bool_verbose:
                print('inserting results into sql database')
            bool_insert_results = self._insert_results()
        else:
            string_error_inout = 'error in calculating in and out of market'
            self.list_errors.append(string_error_inout)
            bool_insert_results = False
            if self.bool_verbose:
                print(string_error_inout)

        #--------------------------------------------------------------------------------#
        # show insert results from database
        #--------------------------------------------------------------------------------#

        if bool_insert_results:
            print('successfull insert into sql databse')
        else:
            string_error_sql = 'error in inserting into sql database'
            self.list_errors.append(string_error_sql)
            if self.bool_verbose:
                print(string_error_sql)

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_insert_results

    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def _get_max_date_from_db(self):
        '''
        this method connects to the sql database and finds the most recent date
        to query yahoo finance

        Requirements:
        package SqlMethods

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: if method executed as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
        string_sql_query_get_max_date = '''
            select max(date_date)
            from {0}
            '''

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # configure query
        #--------------------------------------------------------------------------------#

        string_query = string_sql_query_get_max_date.format(self.string_table)

        #--------------------------------------------------------------------------------#
        # get max date
        #--------------------------------------------------------------------------------#

        list_max_date = self.sql_conn.query_select(string_query)
        if list_max_date[0]:
            string_date = list_max_date[1][0][0]
            bool_return = True
            if isinstance(string_date, str):
                self.dt_sp500_start = datetime.strptime(string_date, '%Y-%m-%d') + timedelta(days = 1)
            else:
                self.list_errors.append('data table is empty')
                self.bool_initial_load = True
        else:
            string_error_max_date_00 = 'error in querying data table; '
            string_error_max_date_00 += list_max_date[1]
            self.list_errors.append(string_error_max_date_00)

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _get_sp500_data(self):
        '''
        this method connets to stooq.com and pulls the sp500 data through pandas_datareader

        Requirements:
        package pandas
        package pandasdatareader

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: if method executed as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        int_query_count = 1
        string_error_data_00 = 'in query {0} of stooq error {1} occured'
        string_get_data = 'getting data for sp500 from {0} to {1}'
        bool_return = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # verbose string
        #--------------------------------------------------------------------------------#

        string_gd = string_get_data.format(
                self.dt_sp500_start.strftime('%d %b %Y'),
                self.dt_sp500_stop.strftime('%d %b %Y')
            )
        if self.bool_verbose:
            print(string_gd)

        #--------------------------------------------------------------------------------#
        # query sp500 data from stooq
        #--------------------------------------------------------------------------------#

        while self.bool_query_stooq_data:
            try:
                self.df_raw_stooq = data.get_data_stooq(
                    symbols = self.string_sym_sp500,
                    start = self.dt_sp500_start.strftime('%Y-%m-%d'),
                    end = self.dt_sp500_stop.strftime('%Y-%m-%d')
                )
            except Exception as e:
                string_error_00 = string_error_data_00.format(
                    int_query_count, str(e.args[0]))
                if self.bool_verbose:
                    print(string_error_00)
                int_query_count += 1
            else:
                self.bool_query_stooq_data = False
                bool_array = self.df_raw_stooq.index >= self.dt_sp500_start
                self.df_raw_stooq = self.df_raw_stooq[bool_array]
            finally:
                if int_query_count > 50:
                    self.bool_query_stooq_data = False

        #--------------------------------------------------------------------------------#
        # format dataframe
        #--------------------------------------------------------------------------------#

        if not self.bool_query_stooq_data:
            bool_return = True
        else:
            self.list_errors.append(string_error_00)

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _get_200_from_db(self):
        '''
        this method pulls the newest 200 records from the sql database

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: if method executed as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        dt_query_date = self.dt_sp500_start - timedelta(days = 201)
        string_query_date = dt_query_date.strftime('%Y-%m-%d')

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
        string_200_query_temp = '''
            select top(200) *
            from {0}
            where date_date <= '{1}'
            order by date_date desc'''

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # query database
        #--------------------------------------------------------------------------------#

        string_query = string_200_query_temp.format(
            self.string_table,
            string_query_date)
        list_data = self.sql_conn.query_select(string_query)

        #--------------------------------------------------------------------------------#
        # configure dataframe
        #--------------------------------------------------------------------------------#

        if list_data[0]:
            df_200 = pandas.DataFrame(
                data = list_data[1],
                columns = self.list_columns)
            df_200 = df_200.sort_values(
                by = ['date_date'],
                ascending = True)
            df_200.index = df_200['date_date'].apply(
                lambda x: datetime.strptime(x, '%Y-%m-%d'))
            df_200 = df_200.drop(
                labels = ['date_date'],
                axis = 1)
            self.df_200_data = df_200
            del df_200
            bool_return = True
        else:
            self.list_errors.append('error in query for newest 200 records of sp500')

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _calc_metrics(self):
        '''
        this method calculates the metrics to determine in and out criteria

        Requirements:
        package pandas
        package numpy

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: if method executed as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # test dataframes
        #--------------------------------------------------------------------------------#

        bool_db_data = isinstance(self.df_200_data, pandas.DataFrame)
        bool_raw_data = isinstance(self.df_raw_stooq, pandas.DataFrame)

        #--------------------------------------------------------------------------------#
        # conduct calculations
        #--------------------------------------------------------------------------------#

        if bool_db_data and bool_raw_data:

            #--------------------------------------------------------------------------------#
            # combine dataframes
            #--------------------------------------------------------------------------------#

            df_sp500 = pandas.DataFrame(columns = self.list_columns[1:])
            df_sp500['float_close'] = self.df_raw_stooq['Close']
            df_sp500.index = self.df_raw_stooq.index
            df_calc = pandas.concat([self.df_200_data, df_sp500], axis = 0)
            del df_sp500
            df_calc = df_calc.sort_index(axis = 0, ascending = True)

            #--------------------------------------------------------------------------------#
            # 50 and 200 sma
            #--------------------------------------------------------------------------------#

            rolling_50 = df_calc['float_close'].rolling(window = 50)
            series_rolling_50_sma = rolling_50.mean()
            rolling_200 = df_calc['float_close'].rolling(window = 200)
            series_rolling_200_sma = rolling_200.mean()
            del rolling_50, rolling_200

            #--------------------------------------------------------------------------------#
            # 50 - 200 sma
            #--------------------------------------------------------------------------------#

            series_delta_50_200 = series_rolling_50_sma - series_rolling_200_sma

            #--------------------------------------------------------------------------------#
            # velocity and acceleration
            #--------------------------------------------------------------------------------#

            list_velocity = [numpy.nan]
            list_acceleration = [numpy.nan, numpy.nan]
            for int_index in range(1, len(df_calc)):
                list_velocity.append(
                    df_calc['float_close'].iloc[int_index] - df_calc['float_close'].iloc[int_index - 1])
                if int_index >= 2:
                    list_acceleration.append(
                        list_velocity[int_index] - list_velocity[int_index - 1])
            series_velocity = pandas.Series(data = list_velocity, index = df_calc.index)
            series_acceleration = pandas.Series(data = list_acceleration, index = df_calc.index)
            del list_velocity, list_acceleration

            #--------------------------------------------------------------------------------#
            # combine into dataframe
            #--------------------------------------------------------------------------------#

            bool_return = True
            self.df_metrics = pandas.DataFrame(index = df_calc.index)
            self.df_metrics = self.df_metrics.assign(float_close = df_calc['float_close'])
            self.df_metrics = self.df_metrics.assign(float_50_sma = series_rolling_50_sma)
            self.df_metrics = self.df_metrics.assign(float_200_sma = series_rolling_200_sma)
            self.df_metrics = self.df_metrics.assign(float_delta_50_200 = series_delta_50_200)
            self.df_metrics = self.df_metrics.assign(float_velocity = series_velocity)
            self.df_metrics = self.df_metrics.assign(float_accel = series_acceleration)
            self.df_metrics = self.df_metrics.assign(string_in_market = df_calc['string_in_market'])
            self.df_metrics = self.df_metrics.assign(string_trigger = df_calc['string_trigger'])
            self.df_metrics = self.df_metrics.assign(float_delta_hl = df_calc['float_delta_hl'])
            self.df_metrics = self.df_metrics.assign(float_delta_div_hl = df_calc['float_delta_div_hl'])
            self.df_metrics = self.df_metrics[self.list_columns[1:]]
            del df_calc
        else:
            string_error_calc_00 = 'either the raw data from sp500 or database data is not present'
            self.list_errors.append(string_error_calc_00)
            if self.bool_verbose:
                print(string_error_calc_00)
                print('successful 200 records from locad db:', bool_db_data)
                print('sucessful raw data from stooq:', bool_raw_data)

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _calc_inout_market(self):
        '''
        this method calculates wether to be in or out of the market

        Requirements:
        package pandas
        package numpy

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: if method executed as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
        string_trigger_rule_01 = '50 sma < 200 sma'
        string_trigger_rule_02 = r'50 sma / 200 sma within 5% of max low'
        bool_df_metrics = isinstance(self.df_metrics, pandas.DataFrame)

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        if bool_df_metrics:
            #--------------------------------------------------------------------------------#
            # determine initial variables
            #--------------------------------------------------------------------------------#

            if self.bool_initial_load:
                bool_in_market = True
                float_delta_high_low = self.df_metrics['float_delta_50_200'].iloc[199]
                self.df_metrics['float_delta_hl'].iloc[199] = float_delta_high_low
                self.df_metrics['string_in_market'].iloc[199] = 'True'
                int_index_start = 200
            else:
                bool_in_market = bool(self.df_metrics['string_in_market'].iloc[0])
                float_delta_high_low = self.df_metrics['float_delta_hl'].iloc[0]
                int_index_start = 1

            #--------------------------------------------------------------------------------#
            # calculate in out of the market
            #--------------------------------------------------------------------------------#

            for int_index in range(int_index_start, len(self.df_metrics)):
                #--------------------------------------------------------------------------------#
                # get metrics
                #--------------------------------------------------------------------------------#

                float_delta_high_low = self.df_metrics['float_delta_hl'].iloc[int_index - 1]
                float_delta = self.df_metrics['float_delta_50_200'].iloc[int_index]

                #--------------------------------------------------------------------------------#
                # rules
                #--------------------------------------------------------------------------------#

                if bool_in_market:
                    #--------------------------------------------------------------------------------#
                    # rule 01: if in the market and 50 sma - 200 sma < 0
                    # get out of the market
                    #--------------------------------------------------------------------------------#

                    if float_delta < 0:
                        bool_in_market = False
                        float_delta_high_low = float_delta
                        self.df_metrics['string_trigger'].iloc[int_index] = string_trigger_rule_01
                    else:
                        if float_delta > float_delta_high_low:
                            float_delta_high_low = float_delta
                else:
                    #--------------------------------------------------------------------------------#
                    # rule 02: if out of the market and 50 sma - 200 sma / delta
                    # high low is 5% or less then get into the market
                    #--------------------------------------------------------------------------------#

                    if float_delta / float_delta_high_low < 0.05:
                        bool_in_market = True
                        float_delta_high_low = float_delta
                        self.df_metrics['string_trigger'].iloc[int_index] = string_trigger_rule_02
                    else:
                        if float_delta < float_delta_high_low:
                            float_delta_high_low = float_delta

                #--------------------------------------------------------------------------------#
                # update dataframe
                #--------------------------------------------------------------------------------#

                if bool_in_market:
                    string_in_market = 'True'
                else:
                    string_in_market = 'False'

                self.df_metrics['string_in_market'].iloc[int_index] = string_in_market
                self.df_metrics['float_delta_hl'].iloc[int_index] = float_delta_high_low
                self.df_metrics['float_delta_div_hl'].iloc[int_index] = float_delta / float_delta_high_low

            #--------------------------------------------------------------------------------#
            # cleanup of nan(s)
            #--------------------------------------------------------------------------------#

            list_float_series = ['float_50_sma', 'float_200_sma', 'float_delta_50_200', 'float_delta_hl',
                'float_delta_div_hl', 'float_velocity', 'float_accel']
            self.df_metrics['string_trigger'] = self._nan_to_unknown(
                self.df_metrics['string_trigger'],
                'None')
            self.df_metrics['string_in_market'] = self._nan_to_unknown(
                self.df_metrics['string_in_market'],
                'False')
            for string_series_name in list_float_series:
                self.df_metrics[string_series_name] = self._nan_to_unknown(
                    self.df_metrics[string_series_name],
                    0.0)

            #--------------------------------------------------------------------------------#
            # return boolean
            #--------------------------------------------------------------------------------#

            bool_return = True
        else:
            self.list_errors.append('the analysis data container is not a pandas DataFrame')

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

    def _insert_results(self):
        '''
        this method inserts results into sql database

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        none
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: if method executed as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # add date_date column to DataFrame
        #--------------------------------------------------------------------------------#

        if not self.bool_initial_load:
            self.df_metrics = self.df_metrics[200:]

        #--------------------------------------------------------------------------------#
        # add date_date column to DataFrame
        #--------------------------------------------------------------------------------#

        self.df_metrics = self.df_metrics.assign(
            date_date = self.df_metrics.index)
        self.df_metrics['date_date'] = self.df_metrics['date_date'].apply(
            lambda x: x.strftime('%Y-%m-%d'))
        self.df_metrics = self.df_metrics[self.list_columns]

        #--------------------------------------------------------------------------------#
        # get insert information for sql database
        #--------------------------------------------------------------------------------#

        list_insert_results = self.sql_conn.insert(
            m_string_table = self.string_table,
            m_list_columns = self.list_columns,
            m_list_values = self.df_metrics.values.tolist())

        if not list_insert_results[0]:
            self.list_errors.append(list_insert_results[1])
        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return list_insert_results[0]

class Sp500Analysis(Sp500Base):
    '''
    This class connects to an external data source and pulls the sp500 data,
    conducts in / out calculations

    Requirements:
    package SqlMethods
    package pandas
    class Sp500Base()

    Methods:
    data_wrapper()

    Attributes:
    Sp500Base() attributes
    '''

    #--------------------------------------------------------------------------#
    # constructor
    #--------------------------------------------------------------------------#

    def __init__(self, ca_list_sql_up, ca_bool_verbose):
        '''
        class construtor

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        c_list_sql_up
        Type: list
        Desc: user and password for sql database
        c_list_sql_up[0] -> type: string; user name
        c_list_sql_up[1] -> type: string; password

        c_bool_verbose
        Type: boolean
        Desc: flag if verbose output desired

        Important Info:
        1. None

        Attributes:
        Sp500Base() attributes
        '''
        #--------------------------------------------------------------------------#
        # call parent constructor
        #--------------------------------------------------------------------------#

        Sp500Base.__init__(
            self,
            c_list_sql_up = ca_list_sql_up,
            c_bool_verbose = ca_bool_verbose)

        #--------------------------------------------------------------------------#
        # data containers
        #--------------------------------------------------------------------------#

        self.df_analysis = None

        #--------------------------------------------------------------------------#
        # analysis attributes
        #--------------------------------------------------------------------------#

        self.datetime_start = datetime(1995, 1, 1)
        self.datetime_stop = datetime.now()
        self.float_money = 3000
        self.float_annual_fee = 0.02
        self.string_date_format = '%Y-%m-%d'
        self.string_date_start = self.datetime_start.strftime(self.string_date_format)
        self.string_date_stop = self.datetime_stop.strftime(self.string_date_format)
        self.string_table = self.dict_sp500_tables.get('analysis', dict()).get('table_name', '')

    #--------------------------------------------------------------------------#
    # callable methods
    #--------------------------------------------------------------------------#

    def analysis_wrapper(self):
        '''
        this method is the wrapper to conduct the analysis of the sp500
        data in the database and collected from stooq

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        
        Type: 
        Desc: 

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: method executes as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # get data from database
        #--------------------------------------------------------------------------------#

        bool_db_data = self._get_data_from_db()

        #--------------------------------------------------------------------------------#
        # conduct analysis of data
        #--------------------------------------------------------------------------------#

        if bool_db_data:
            bool_analysis = self._analysis()
        else:
            self.list_errors.append('analysis:error in getting data from database')
            bool_analysis = False

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_analysis

    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def _get_data_from_db(self):
        '''
        this method pulls data from the sql database for analysis

        Requirements:
        package pandas
        package SqlMethods

        Inputs:
        none
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: method executes as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
        string_sql_query_where = "date_date >= '" + self.string_date_start
        string_sql_query_where += "' and date_date <= '" + self.string_date_stop
        string_sql_query_where += "'"
        string_sql_query_end = 'order by date_date'
        string_sql_table = self.dict_sp500_tables.get('data')['table_name']

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # conduct sql query
        #--------------------------------------------------------------------------------#

        if self.sql_conn.bool_is_connected:
            string_sql_query = self.sql_conn.gen_select_statement(
                m_string_select = '*',
                m_string_from = string_sql_table,
                m_string_where = string_sql_query_where,
                m_string_end = string_sql_query_end)

            try:
                self.df_analysis = pandas.read_sql(
                    sql = string_sql_query,
                    con = self.sql_conn._list_conn[1])
            except Exception as e:
                self.list_errors.append('pandas.read_sql() error: ' + str(e.args))
            else:
                if isinstance(self.df_analysis, pandas.DataFrame) and \
                  not self.df_analysis.empty:
                    bool_return = True
                else:
                    self.list_errors.append(
                        'data from database is not in a dataframe or dataframe is empty')
            finally:
                pass
        else:
            self.list_errors.append('not connected to sql database')

        return bool_return

    def _analysis(self):
        '''
        this method conducts the analysis of the data pulled from the database

        Requirements:
        package pandas

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: method executes as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = True

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # start test
        #--------------------------------------------------------------------------------#

        print('begin calculations')
        if not self.df_analysis.empty:
            #--------------------------------------------------------------------------------#
            # day counts
            #--------------------------------------------------------------------------------#

            print('conducting days calculations')
            # days pulled from database
            string_date_first = self.df_analysis['date_date'].iloc[0]
            string_date_last = self.df_analysis['date_date'].iloc[len(self.df_analysis) - 1]
    
            # days in range
            int_days_in_range = len(self.df_analysis)
    
            # market status
            string_market_status = self.df_analysis['string_in_market'].iloc[len(self.df_analysis) - 1]
    
            # days in the market
            array_in_market = self.df_analysis['string_in_market'] == 'True'
            dataframe_in_market = self.df_analysis.ix[array_in_market]
            int_days_in_market = len(dataframe_in_market)
    
            # bad days
            array_trigger = self.df_analysis['string_trigger'] != 'None'
            dataframe_trigger = self.df_analysis.loc[array_trigger]
            
            # replace index to interate
            dataframe_trigger = dataframe_trigger.reset_index(drop = True)
            
            int_days_bad = 0
            for int_index in range(0, len(dataframe_trigger) - 1):
                # get the start market status
                string_status_start = dataframe_trigger['string_in_market'].iloc[int_index]
                
                # get the end market satus
                string_status_end = dataframe_trigger['string_in_market'].iloc[int_index + 1]
                
                # calculate based on the a change of market status or not
                if string_status_start == 'True' and string_status_end == 'False':
                    # get sp500 values
                    float_sp500_start = dataframe_trigger['float_close'].iloc[int_index]
                    float_sp500_end = dataframe_trigger['float_close'].iloc[int_index + 1]
    
                    # get bad days
                    if float_sp500_end < float_sp500_start:
                        string_date_bad_start = dataframe_trigger['date_date'].iloc[int_index]
                        string_date_bad_end = dataframe_trigger['date_date'].iloc[int_index + 1]
                        datetime_bad_start = datetime.strptime(string_date_bad_start, '%Y-%m-%d')
                        datetime_bad_end = datetime.strptime(string_date_bad_end, '%Y-%m-%d')
                        timedelta_bad = datetime_bad_end - datetime_bad_start
                        int_days_bad = int_days_bad + timedelta_bad.days
    
            # calculate good days
            int_days_good = int_days_in_market - int_days_bad
    
            #--------------------------------------------------------------------------------#
            # conduct amount calculations
            #--------------------------------------------------------------------------------#
    
            print('conducting amount calculations')
            # calculate dollar amounts
            float_man_fee = 0
            float_gm_with_fee = self.float_money
            float_gm_without_fee = self.float_money
            for int_index in range(1, len(self.df_analysis)):
                # get dates
                string_date_calc_start = self.df_analysis['date_date'].iloc[int_index - 1]
                string_date_calc_stop = self.df_analysis['date_date'].iloc[int_index]
                datetime_calc_start = datetime.strptime(string_date_calc_start, '%Y-%m-%d')
                datetime_calc_stop = datetime.strptime(string_date_calc_stop, '%Y-%m-%d')
    
                # get closes
                float_close_calc_start = self.df_analysis['float_close'].iloc[int_index - 1]
                float_close_calc_stop = self.df_analysis['float_close'].iloc[int_index]
                float_ratio_return = float_close_calc_stop / float_close_calc_start
                if int_index == 1:
                    float_close_initial = float_close_calc_start
                if int_index == self.df_analysis.shape[0] - 1:
                    float_close_final = float_close_calc_stop
    
                # get market status
                string_ms_start = self.df_analysis['string_in_market'].iloc[int_index - 1]
                string_ms_stop = self.df_analysis['string_in_market'].iloc[int_index]
    
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
                    float_man_fee = float_man_fee + (float_gm_with_fee * self.float_annual_fee / 4)
                    float_gm_with_fee = float_gm_with_fee * (1 - (self.float_annual_fee / 4))
    
            # buy a hold calculation
            float_buy_hold = self.float_money * (float_close_final / float_close_initial)

            #--------------------------------------------------------------------------------#
            # insert results into database
            #--------------------------------------------------------------------------------#
    
            print('inserting results of analysis into database')
            list_sql_insert_columns = ['date_analysis', 'date_start', 'date_stop', 'dollar_start', 'int_days_range',
                'int_days_in_market', 'int_days_good', 'int_days_bad', 'string_in_market', 'float_ann_fee',
                'dollar_gm_with_fee', 'dollar_man_fee', 'dollar_buy_hold', 'dollar_gm_no_fee', 'string_symbol']
            list_sql_insert_values = [self.string_date_stop, string_date_first, string_date_last, self.float_money,
                int_days_in_range, int_days_in_market, int_days_good, int_days_bad, string_market_status, 
                self.float_annual_fee, float_gm_with_fee, float_man_fee, float_buy_hold, float_gm_without_fee, 
                self. string_sym_sp500]
    
            list_insert_dummy = self.sql_conn.insert(
                m_string_table =  self.string_table,
                m_list_columns = list_sql_insert_columns,
                m_list_values = list_sql_insert_values)
            
            if list_insert_dummy[0] is False:
                self.list_errors.append('insert of analysis data failed into local database')
                bool_return = False
        else:
            self.list_errors.append('analysis dataframe is empty')
            bool_return = False

        #--------------------------------------------------------------------------------#
        # variable / object cleanup
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return

class Sp500Visualizations(Sp500Base):
    '''
    class documentation....
    '''

    def __init__(self, cv_list_sql_up, cv_bool_verbose):
        '''
        class construtor

        Requirements:
        package SqlMethods
        package pandas

        Inputs:
        c_list_sql_up
        Type: list
        Desc: user and password for sql database
        c_list_sql_up[0] -> type: string; user name
        c_list_sql_up[1] -> type: string; password

        c_bool_verbose
        Type: boolean
        Desc: flag if verbose output desired

        Important Info:
        1. None

        Attributes:
        Sp500Base() attributes
        '''
        
        #--------------------------------------------------------------------------#
        # call parent constructor
        #--------------------------------------------------------------------------#

        Sp500Base.__init__(
            self,
            c_list_sql_up = cv_list_sql_up,
            c_bool_verbose = cv_bool_verbose
        )
        
        #--------------------------------------------------------------------------#
        # pplot attributes
        #--------------------------------------------------------------------------#
        
        style.use('ggplot')
        
        #--------------------------------------------------------------------------#
        # time attributes
        #--------------------------------------------------------------------------#

        self.datetime_start = datetime(1995, 1, 1)
        self.datetime_stop = datetime.now()
        self.string_date_format = '%Y-%m-%d'
        self.string_date_start = self.datetime_start.strftime(self.string_date_format)
        self.string_date_stop = self.datetime_stop.strftime(self.string_date_format)

        #--------------------------------------------------------------------------#
        # data containers
        #--------------------------------------------------------------------------#

        self.df_vis_data = None

        #--------------------------------------------------------------------------#
        # sql query attributes
        #--------------------------------------------------------------------------#

        self.string_sql_query_where = "date_date >= '{date_start}' and date_date <= '{date_stop}'"
        self.string_sql_query = self.sql_conn.gen_select_statement(
            m_string_select='*',
            m_string_from=self.dict_sp500_tables.get('data', dict()).get('table_name', None),
            m_string_where=self.string_sql_query_where.format(
                date_start = self.string_date_start,
                date_stop = self.string_date_stop
            ),
            m_string_end='order by date_date'
        )

        #--------------------------------------------------------------------------#
        # visualization attributes
        #--------------------------------------------------------------------------#

        # path variables
        self.string_path = os.path.join(os.path.abspath('../'), 'visualizations')
        self.string_file = 'sp500_visualization_'  + self.datetime_stop.strftime('%Y-%m-%d %H_%M_%S') + '.png'
        
        # plot data
        self.dict_plot_data = {
            'x':None, # pandas.Series
            'y_sp500':None, # pandas.Series
            'y_200_sma':None, # pandas.Series
            'y_50_sma':None, # pandas.Series
            'y_max':None, # float
            'y_min':None, # float
            'vertical_lines_true':None, # list of datetime
            'vertical_lines_false':None, # list of datetime
            'in_market':None, # list of lists
        }

    #--------------------------------------------------------------------------#
    # callable methods
    #--------------------------------------------------------------------------#

    def visualization_wrapper(self):
        '''
        this method is the wrapper to visualize the data from the analysis

        Requirements:
        package ??

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: method executes as designed
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # sequence declarations
        #--------------------------------------------------------------------------------#

        set_bools = set()

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # get data from database
        #--------------------------------------------------------------------------------#

        print('retreiving data for visualization')
        bool_vis_data = self._get_vis_data()
        set_bools.add(bool_vis_data)

        #--------------------------------------------------------------------------------#
        # process the data
        #--------------------------------------------------------------------------------#

        if bool_vis_data:
            print('processing data for visualization')
            bool_process_vis_data = self._process_vis_data()
        else:
            bool_process_vis_data = False
            string_vis_process_error = 'data was not processed for visualization'
            self.list_errors.append(string_vis_process_error)
        set_bools.add(bool_process_vis_data)

        #--------------------------------------------------------------------------------#
        # create visualizations
        #--------------------------------------------------------------------------------#

        if bool_process_vis_data:
            print('generateing visualization')
            bool_create_plots = self._create_plots()
        else:
            bool_create_plots = False
        set_bools.add(bool_create_plots)

        #--------------------------------------------------------------------------------#
        # booleans
        #--------------------------------------------------------------------------------#

        if set_bools == {True}:
            bool_visualizations = True
        else:
            bool_visualizations = False
        
        if self.bool_verbose and not bool_visualizations:
            print('errors are as follows:')
            print('||'.join(self.list_errors))
            
        #--------------------------------------------------------------------------------#
        # return
        #--------------------------------------------------------------------------------#

        return bool_visualizations

    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def _get_vis_data(self):
        '''
        this method queries the data from the database

        Requirements:
        package pandas
        package SqlMethods

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        object
        Type: pandas.DataFrame
        Desc: data from the sql database which holds the transaction data
            columns -> ** see base class documentation
        '''

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_error_getting_data = False

        #--------------------------------------------------------------------------------#
        # query data
        #--------------------------------------------------------------------------------#

        try:
            self.df_vis_data = pandas.read_sql(self.string_sql_query, self.sql_conn._list_conn[1])
        except Exception as e:
            string_e_args = str(e.args)
            bool_error_getting_data = True
            string_print_error = 'There was an error getting the data from the database: ' + string_e_args
            string_print_error += '.  Research and come back "dumkopf"!'
            self.list_errors.append(string_print_error)
        else:
            dict_dtype = {
                'date_date':str,
                'float_close':numpy.float,
                'string_in_market':str,
                'string_trigger':str,
                'float_50_sma':numpy.float,
                'float_200_sma':numpy.float,
                'float_delta_50_200':numpy.float,
                'float_delta_hl':numpy.float,
                'float_delta_div_hl':numpy.float,
                'float_velocity':numpy.float,
                'float_accel':numpy.float
            }
            self.df_vis_data = self.df_vis_data.astype(dict_dtype)
        finally:
            pass
        
        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return not bool_error_getting_data

    def _process_vis_data(self):
        '''
        this method processes the data for the visualizations

        Requirements:
        package pandas
        package datetime

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        variable
        Type: boolean
        Desc: data for visualizations has been processed sucessfully
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        list_in_market = list()

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # check dataframe
        #--------------------------------------------------------------------------------#

        if isinstance(self.df_vis_data, pandas.DataFrame) and not self.df_vis_data.empty:
            bool_vis_proc_data = True
        else:
            bool_vis_proc_data = False

        #--------------------------------------------------------------------------------#
        # format x-values and get values
        #--------------------------------------------------------------------------------#
        
        if bool_vis_proc_data:
            self.dict_plot_data['x'] = self.df_vis_data['date_date'].apply(
                lambda x: datetime.strptime(x, '%Y-%m-%d')
            )
            self.dict_plot_data['y_sp500'] = self.df_vis_data['float_close']
            self.dict_plot_data['y_200_sma'] = self.df_vis_data['float_200_sma']
            self.dict_plot_data['y_50_sma'] = self.df_vis_data['float_50_sma']
            self.dict_plot_data['y_max'] = self.df_vis_data['float_close'].max() + 50
            self.dict_plot_data['y_min'] = self.df_vis_data['float_close'].min() - 50

            #--------------------------------------------------------------------------------#
            # get the triggers on when in and out of the market
            #--------------------------------------------------------------------------------#

            series_bool_trigger = self.df_vis_data['string_trigger'] != 'None'
            dataframe_triggers = self.df_vis_data[series_bool_trigger]
            index_df_trigger_index = dataframe_triggers.index

            #--------------------------------------------------------------------------------#
            # check the first element of the data from the database 
            # to ensure it is in In the market
            #--------------------------------------------------------------------------------#

            if dataframe_triggers['string_in_market'].iloc[0] == 'False':
                int_start = 1
            else:
                int_start = 0

            #--------------------------------------------------------------------------------#
            # create a list of row numbers in the dataframe to plot the in
            # market lines; if the first value in the data is not in the market
            # in the trigger dataframe get the index for the dataframe
            #--------------------------------------------------------------------------------#

            if int_start == 1:
                int_loc_01 = index_df_trigger_index[0]
                list_in_market.append([self.df_vis_data['date_date'].iloc[0:int_loc_01 + 1].values,
                                                        self.df_vis_data['float_close'].iloc[0:int_loc_01 + 1].values])

            #--------------------------------------------------------------------------------#
            # loop through the dataframe of triggers to get the values for
            # the in market for the plot
            #--------------------------------------------------------------------------------#

            for int_index in range(int_start, len(index_df_trigger_index) - 1):
                # get the indexes from the dataframe_triggers for the self.df_vis_data
                int_loc_01 = index_df_trigger_index[int_index]
                int_loc_02 = index_df_trigger_index[int_index + 1]

                # compare the markets status
                string_market_status_01 = dataframe_triggers['string_in_market'].iloc[int_index]
                string_market_status_02 = dataframe_triggers['string_in_market'].iloc[int_index + 1]

                # check if the market is in
                if string_market_status_01 == 'True' and string_market_status_02 == 'False':
                    list_in_market.append([self.df_vis_data['date_date'].iloc[int_loc_01:int_loc_02 + 1].values,
                                                            self.df_vis_data['float_close'].iloc[int_loc_01:int_loc_02 + 1].values])

            #--------------------------------------------------------------------------------#
            # get the vertical lines for the charts
            #--------------------------------------------------------------------------------#

            series_trigger_false = dataframe_triggers['string_in_market'] == 'False'
            series_trigger_true = dataframe_triggers['string_in_market'] == 'True'
            self.dict_plot_data['vertical_lines_false'] = list(dataframe_triggers[series_trigger_false]['date_date'].values)
            self.dict_plot_data['vertical_lines_true'] = list(dataframe_triggers[series_trigger_true]['date_date'].values)

            #--------------------------------------------------------------------------------#
            # check the last value, if true then add to the end of
            # the dataframe
            #--------------------------------------------------------------------------------#

            if dataframe_triggers['string_in_market'].iloc[len(index_df_trigger_index) - 1] == 'True':
                # get the last two locations
                int_loc_01 = index_df_trigger_index[-1]
                int_loc_02 = self.df_vis_data.shape[0] - 1

                # add last element into the market
                list_in_market.append([self.df_vis_data['date_date'].iloc[int_loc_01:int_loc_02 + 1].values,
                                                            self.df_vis_data['float_close'].iloc[int_loc_01:int_loc_02 + 1].values])
            
            self.dict_plot_data['in_market'] = list_in_market

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_vis_proc_data

    def _create_plots(self):
        '''
        this method creates the plots for the analysis saves the plot to a designated location

        Requirements:
        package matplotlib.pyplot
        package pandas
        package numpy
        package os

        Inputs:
        None
        Type: n/a
        Desc: n/a

        Important Info:
        None

        Return:
        None
        Type: n/a
        Desc: n/a
        '''

        #--------------------------------------------------------------------------------#
        # objects declarations
        #--------------------------------------------------------------------------------#

        fig, axes = pyplot.subplots(2, 1) # one figure with two plots (2 rows, 1 column)
        fig.set_size_inches(10., 7.)  #  10 inches width, 7 inches high

        #--------------------------------------------------------------------------------#
        # time declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # upper plot
        #--------------------------------------------------------------------------------#

        # sp500 only (black lines)
        axes[0].plot(self.dict_plot_data.get('x', pandas.Series()),
            self.dict_plot_data.get('y_sp500', pandas.Series()), color = 'black', linewidth = 2, linestyle = '-',
            label = 'SP500')

        # debug code
        list_to_plot = self.dict_plot_data.get('in_market', list())
        
        # when in the market (green lines)
        bool_label = True
        for plot_in_market in list_to_plot:
            if bool_label:
                bool_label = False
                axes[0].plot(plot_in_market[0], plot_in_market[1], color = 'green', linewidth = 2.5, linestyle = '-',
                    label = 'In Market')
            else:
                axes[0].plot(plot_in_market[0], plot_in_market[1], color = 'green', linewidth = 2.5, linestyle = '-')

        # upper plot elements
        axes[0].set(title = 'In / Out of Market', xlabel = 'date of close', ylabel = 'close')
        axes[0].set_ylim(self.dict_plot_data.get('y_min', None), self.dict_plot_data.get('y_max', None))
        axes[0].legend(loc = 'best')

        #--------------------------------------------------------------------------------#
        # lower plot; 200 day (blue) and 50 day (red) sma
        #--------------------------------------------------------------------------------#

        axes[1].plot(self.dict_plot_data.get('x', pandas.Series()),
            self.dict_plot_data.get('y_200_sma', pandas.Series()), color = 'blue', linewidth = 2, linestyle = '-',
            label = '200 sma')
        axes[1].plot(self.dict_plot_data.get('x', pandas.Series()),
            self.dict_plot_data.get('y_50_sma', pandas.Series()), color = 'red', linewidth = 2, linestyle = '-',
            label = '50 sma')

        # lower plot elements
        axes[1].set(title = '200 & 50 sma', xlabel = 'date of close', ylabel = 'close')
        axes[1].set_ylim(self.dict_plot_data.get('y_min', None), self.dict_plot_data.get('y_max', None))

        #--------------------------------------------------------------------------------#
        # veticle lines on both plots
        #--------------------------------------------------------------------------------#

        bool_label_01 = True
        for x_val in self.dict_plot_data.get('vertical_lines_false', list()):
            if bool_label_01:
                axes[0].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to get out')
                axes[1].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to get out')
                bool_label_01 = False
            else:
                axes[0].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--')
                axes[1].axvline(x_val, color = 'indigo', linewidth = 1, linestyle = '--')

        bool_label_02 = True
        for x_val in self.dict_plot_data.get('vertical_lines_true', list()):
            if bool_label_02:
                axes[0].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to buy in')
                axes[1].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--', 
                    label = 'Trigger to buy in')
                bool_label_02 = False
            else:
                axes[0].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--')
                axes[1].axvline(x_val, color = 'orangered', linewidth = 1, linestyle = '--')

        #--------------------------------------------------------------------------------#
        # plot elements
        #--------------------------------------------------------------------------------#

        axes[1].legend(loc = 'best')
        pyplot.subplots_adjust(wspace = None, hspace = 0.4)
        pyplot.suptitle('SP500 Analysis')
        pyplot.savefig(os.path.join(self.string_path,  self.string_file))

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return True
