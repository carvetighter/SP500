'''
this is the main method to test the Sp500 class
'''

from Sp500 import Sp500Data
from Sp500 import Sp500Analysis
from Sp500 import Sp500Visualizations

def main_class(m_list_user):
    '''
    this is the main method new change another
    
    Requirements:
    None
    
    Inputs:
    m_list_user
    Type: list
    Desc: a list of the user name and password for the local sql database
    list[0] -> type: raw string; user name
    list[1] -> type: raw string; password
     
    Important Info:
    None
    
    Return:
    None
    Type: None
    Description: None
    '''

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
        cv_list_sql_up = m_list_user,
        cv_bool_verbose = True)

    #--------------------------------------------------------------------------------#
    # time declarations
    #--------------------------------------------------------------------------------#

    #--------------------------------------------------------------------------------#
    # lists declarations
    #--------------------------------------------------------------------------------#

    list_errors = list()
    set_errors = set()
    
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
    bool_db_check = sp_data.check_sql_db()[0]
    if bool_db_check:
        print(string_get_sp500_data)
        bool_data_results = sp_data.data_wrapper()
        if not bool_data_results:
            list_errors.extend(sp_data.list_errors)
    else:
        list_errors.extend(sp_data.list_errors)
        bool_data_results = False
    set_errors.add(bool_db_check)
    set_errors.add(bool_data_results)

    #--------------------------------------------------------------------------------#
    # conduct analysis
    #--------------------------------------------------------------------------------#

    if bool_db_check and bool_data_results:
        print('\n' + string_analyze_data)
        bool_analysis = sp_analysis.analysis_wrapper()
        if not bool_analysis:
            list_errors.extend(sp_analysis.list_errors)
    else:
        bool_analysis = False
    set_errors.add(bool_analysis)

    #--------------------------------------------------------------------------------#
    # create visualization
    #--------------------------------------------------------------------------------#

    if bool_db_check and bool_data_results:
        print('\n' + string_plotting_data)
        bool_visualizations = sp_visualizations.visualization_wrapper()
        if not bool_visualizations:
            list_errors.extend(sp_visualizations.list_errors)
    else:
        bool_visualizations = False
    set_errors.add(bool_visualizations)

    #--------------------------------------------------------------------------------#
    # errors
    #--------------------------------------------------------------------------------#

    if set_errors != {True}:
        print('||'.join(list_errors))
    
    #--------------------------------------------------------------------------------#
    # return
    #--------------------------------------------------------------------------------#

    return
