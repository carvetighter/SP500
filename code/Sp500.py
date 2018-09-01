'''
Sp500 class file

File containtes four classes:
Sp500 base class -> used for containers and setup for child classes
Sp500 data collection class -> used to collect the data from yahoo finance and a local sql database
Sp500 analysis class -> conducts the analysis between the moving averages
Sp500 visualizations class -> conducts the visualizations of the analysis
'''

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone
from pandas_datareader import data
import fix_yahoo_finance
import numpy
import warnings
from matplotlib import pyplot
from matplotlib import style
import pandas
from SqlMethods import SqlMethods

# fix for is_list_like error
pandas.core.common.is_list_like = pandas.api.types.is_list_like

# ignore warnings
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
        ??
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

        #--------------------------------------------------------------------------#
        # sql db data attributes
        #--------------------------------------------------------------------------#

        self.dict_sp500_tables = {
            'sp500.data':{
                'col_dtype':['date', 'float', 'varchar(10)', 'varchar(500)', 'float', 'float', 'float', 'float', 'float',
                    'float', 'float'],
                'col_names':['date_date', 'float_close', 'string_in_market', 'string_trigger', 'float_50_sma',
                    'float_200_sma', 'float_delta_50_200', 'float_delta_hl', 'float_delta_div_hl', 'float_velocity',
                    'float_accel']},
            'sp500.analysis':{
                'col_dtype':['date', 'date', 'date', 'float', 'int', 'int', 'int', 'int', 'varchar(10)', 'float', 'float', 'float',
                    'float', 'float', 'varchar(50)'],
                'col_names':['date_analysis', 'date_start', 'date_stop', 'dollar_start', 'int_days_range',
                    'int_days_in_market', 'int_days_good', 'int_days_bad', 'string_in_market', 'float_ann_fee',
                    'dollar_gm_with_fee', 'dollar_man_fee', 'dollar_buy_hold', 'dollar_gm_no_fee',
                    'string_symbol']}}
        self.tup_sql_db_setup = (False, 'not checked')

        #--------------------------------------------------------------------------#
        # yahoo finance attributes
        #--------------------------------------------------------------------------#

        self.dt_yahoo_start = datetime(1970, 1, 1)
        self.dt_yahoo_stop = datetime.now()
        self.string_sym_sp500 = '^GSPC'
        self.bool_query_yahoo_finance = True

        #--------------------------------------------------------------------------#
        # data containers
        #--------------------------------------------------------------------------#

        self.df_raw_yahoo = None
        self.df_analysis = None
        self.df_db_data = None

        #--------------------------------------------------------------------------#
        # analysis attributes
        #--------------------------------------------------------------------------#

        datetime_start = datetime(1995, 1, 1)
        datetime_stop = datetime.now()
        float_money = 3000
        float_annual_fee = 0.02
        
        #--------------------------------------------------------------------------#
        # other attributes
        #--------------------------------------------------------------------------#

        self.bool_verbose = c_bool_verbose

    #--------------------------------------------------------------------------#
    # callable methods
    # 
    # methods that directly support callable methods should
    # be underneath method
    #--------------------------------------------------------------------------#

    def check_sql_db_setup(self):
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
        # lists declarations
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # variables declarations
        #--------------------------------------------------------------------------------#

        bool_return = False
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

        if self.sql_conn.bool_is_connected:
            for string_table in self.dict_sp500_tables:

                #--------------------------------------------------------------------------------#
                # set table boolean check and get table information
                #--------------------------------------------------------------------------------#

                bool_table_check = False
                dict_table = self.dict_sp500_tables.get(string_table, None)
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
                            list_errors.append(string_error_db_check_02.format(string_table))
                    else:
                        string_error_db_check_00 = 'table {0} error reteiving columns'
                        list_errors.append(string_error_db_check_00.format(string_table))
                else:
                    string_error_db_check_01 = 'table {0} does not exist'
                    list_errors.append(string_error_db_check_01.format(string_table))

                # add boolean to set for check
                set_bool_return.add(bool_table_check)
        else:
            list_errors.append('no connection to sql database')
            bool_return = False

        #--------------------------------------------------------------------------------#
        # for each table determine the return boolean
        #--------------------------------------------------------------------------------#

        if set_bool_return == {True}:
            bool_return = True

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return, '||'.join(list_errors)

    def create_sql_db_tables(self, m_string_sql_db_errors):
        '''
        this method creates the sql database tables based on the error string passed

        Requirements:
        package SqlMethods

        Inputs:
        m_string_sql_db_errors
        Type: string
        Desc: error string, each error is seperated by string double pipe, '||'

        Important Info:
        None

        Return:
        object
        Type: tuple
        Desc: 
        tuple[0] -> type: boolean; True of db is setup for the analysis, False if not
        tuple[1] -> type: string; if tuple[0] is True then empty string; if tuple[0] is
            False than any errors that are detected; errors are separated by double
            pipes '||';
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

        list_errors = m_string_sql_db_errors.split('||')

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

        series_db_errors = pandas.Series(data = list_errors)
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
                dict_table = self.dict_sp500_tables.get(string_table, None)

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

                    series_col_name = pandas.Series(dict_table.get('col_names'))
                    series_col_type = pandas.Series(dict_table.get('col_dtype'))
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
                    list_errors.append(string_error_crete_table_00.format(string_table))

                #--------------------------------------------------------------------------------#
                # create return set to test return boolean
                #--------------------------------------------------------------------------------#

                set_bool_return.add(bool_table)
        else:
            list_errors.append('no connection to sql database')
            set_bool_return.add(bool_table)

        #--------------------------------------------------------------------------------#
        # for each table determine the return boolean
        #--------------------------------------------------------------------------------#

        if set_bool_return == {True}:
            bool_return = True

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        return bool_return, '||'.join(list_errors)

    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def def_Methods(self, list_cluster_results, array_sparse_matrix):
        '''
        below is an example of a good method comment

        ---------------------------------------------------------------------------------------------------------------------------------------------------

        this method implements the evauluation criterea for the clusters of each clutering algorithms
        criterea:
               - 1/2 of the clusters for each result need to be:
                   - the average silhouette score of the cluster needs to be higher then the silhouette score of all the clusters
                     combined
                   - the standard deviation of the clusters need to be lower than the standard deviation of all the clusters
                     combined
               - silhouette value for the dataset must be greater than 0.5

        Requirements:
        package time
        package numpy
        package statistics
        package sklearn.metrics

        Inputs:
        list_cluster_results
        Type: list
        Desc: the list of parameters for the clustering object
        list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
                         or dense array
        list[x][1] -> type: string; the cluster ID with the parameters

        array_sparse_matrix
        Type: numpy array
        Desc: a sparse matrix of the samples used for clustering

        Important Info:
        None

        Return:
        object
        Type: list
        Desc: this of the clusters that meet the evaluation criterea
        list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
                        or dense array
        list[x][1] -> type: string; the cluster ID with the parameters
        list[x][2] -> type: float; silhouette average value for the entire set of data
        list[x][3] -> type: array; 1 dimensional array of silhouette values for each data sample
        list[x][4] -> type: list; list of lists, the cluster and the average silhoutte value for each cluster, the orders is sorted 
                            highest to lowest silhoutte value
                            list[x][4][x][0] -> int; cluster label
                            list[x][4][x][1] -> float; cluster silhoutte value
        list[x][5] -> type: list; a list that contains the cluster label and the number of samples in each cluster
                           list[x][5][x][0] -> int; cluster label
                           list[x][5][x][1] -> int; number of samples in cluster list[x][5][x][0]
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
        # sub-section comment
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # sectional comment
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # variable / object cleanup
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        pass

class Sp500Data(Sp500Base):
    '''
    ??

    Requirements:
    package SqlMethods
    package pandas

    Methods:
    ??

    Attributes:
    ??
    '''

    #--------------------------------------------------------------------------#
    # constructor
    #--------------------------------------------------------------------------#

    def __init__(self, c_list_sql_up, c_bool_verbose):
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
        1. ??

        Attributes:
        ??
        '''
        #--------------------------------------------------------------------------#
        # call parent constructor
        #--------------------------------------------------------------------------#

        super().__init__(
            c_list_sql_up = c_bool_verbose,
            c_bool_verbose = c_bool_verbose)


    #--------------------------------------------------------------------------#
    # callable methods
    #--------------------------------------------------------------------------#



    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def def_Methods(self, list_cluster_results, array_sparse_matrix):
        '''
        below is an example of a good method comment

        ---------------------------------------------------------------------------------------------------------------------------------------------------

        this method implements the evauluation criterea for the clusters of each clutering algorithms
        criterea:
               - 1/2 of the clusters for each result need to be:
                   - the average silhouette score of the cluster needs to be higher then the silhouette score of all the clusters
                     combined
                   - the standard deviation of the clusters need to be lower than the standard deviation of all the clusters
                     combined
               - silhouette value for the dataset must be greater than 0.5

        Requirements:
        package time
        package numpy
        package statistics
        package sklearn.metrics

        Inputs:
        list_cluster_results
        Type: list
        Desc: the list of parameters for the clustering object
        list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
                         or dense array
        list[x][1] -> type: string; the cluster ID with the parameters

        array_sparse_matrix
        Type: numpy array
        Desc: a sparse matrix of the samples used for clustering

        Important Info:
        None

        Return:
        object
        Type: list
        Desc: this of the clusters that meet the evaluation criterea
        list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
                        or dense array
        list[x][1] -> type: string; the cluster ID with the parameters
        list[x][2] -> type: float; silhouette average value for the entire set of data
        list[x][3] -> type: array; 1 dimensional array of silhouette values for each data sample
        list[x][4] -> type: list; list of lists, the cluster and the average silhoutte value for each cluster, the orders is sorted 
                            highest to lowest silhoutte value
                            list[x][4][x][0] -> int; cluster label
                            list[x][4][x][1] -> float; cluster silhoutte value
        list[x][5] -> type: list; a list that contains the cluster label and the number of samples in each cluster
                           list[x][5][x][0] -> int; cluster label
                           list[x][5][x][1] -> int; number of samples in cluster list[x][5][x][0]
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
        # sub-section comment
        #--------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # sectional comment
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        #--------------------------------------------------------------------------------#
        # variable / object cleanup
        #--------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------#
        # return value
        #--------------------------------------------------------------------------------#

        pass

class Sp500Analysis(Sp500Base):
    pass

class Sp500Visualizations(Sp500Base):
    pass
