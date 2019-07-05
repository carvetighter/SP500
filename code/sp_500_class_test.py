'''
this is the main method to test the Sp500 class
'''

from Sp500 import Sp500Data
from Sp500 import Sp500Analysis
from Sp500 import Sp500Visualizations

def main_class_test(m_list_user):
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

    #--------------------------------------------------------------------------------#
    # object declarations
    #--------------------------------------------------------------------------------#

    sp_data = Sp500Data(
        csd_list_sql_up = m_list_user,
        csd_bool_verbose = True)
    sp_analysis = Sp500Analysis(
        ca_list_sql_up = m_list_user,
        ca_bool_verbose = True)
    sp_visualizations = Sp500Visualizations(
        ca_list_sql_up = m_list_user,
        ca_bool_verbose = True)

    #--------------------------------------------------------------------------------#
    # time declarations
    #--------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------#
    # lists declarations
    #--------------------------------------------------------------------------------#

    list_errors = list()
    bool_return = False
    
    #--------------------------------------------------------------------------------#
    # variables declarations
    #--------------------------------------------------------------------------------#

    string_check_sql_db = '''
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        checking data from sql database\n
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        '''
    string_get_sp500_data = '''
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        getting sp500 data from stooq\n
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        '''
    string_analyze_data = '''
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        analyzing the data\n
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        '''
    string_plotting_data = '''
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        plotting data\n
        -------------------------------------------------------------\n
        -------------------------------------------------------------\n
        '''

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

    #--------------------------------------------------------------------------------#
    # get data and market status
    #--------------------------------------------------------------------------------#

    print('\n' + string_check_sql_db)
    tup_db_check = sp_data.check_sql_db()
    if tup_db_check[0]:
        print(string_get_sp500_data)
        tup_data_results = sp_data.data_wrapper()
    else:
        list_errors.append(sp_data.error_sql_db())
        tup_data_results(False, '')
    
    if not tup_data_results[0]:
        

    #--------------------------------------------------------------------------------#
    # conduct analysis
    #--------------------------------------------------------------------------------#

    print('\n' + string_analyze_data)
    # tup_anal_db_check = sp_analysis.check_sql_db()
    if tup_db_check[0]:
        print('\n' + string_analyze_data)
        tup_analysis_ = sp_analysis.analysis_wrapper()
    else:
        list_errors.append(sp_analysis.error_sql_db())
        tup_analysis_ = (False, '||'.join(list_errors))

    #--------------------------------------------------------------------------------#
    # create visualization
    #--------------------------------------------------------------------------------#

    print('\n' + string_plotting_data)

    # CreateVisualization(datetime_start, datetime_stop, m_list_user)

    return
