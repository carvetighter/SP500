#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#  

import pymssql
import collections
from xml.dom import minidom

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Classes 
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

class SqlMethods(object):
    '''
    This class makes it easier to connect and work with a sql server.  The list of methods below are firther defined in
    in the methods themselves
    
    Requirements:
    package pymssql
    package collections
    packace xml.dom.minidom

    Methods:
    gen_connection()
           - creates connection to the database

    close()
            - closes the connection to the database
    
    gen_select_statement()
           - generates the sql select staement

    query_select()
            - queries the table
    
    get_num_columns()
            - returns the number of columns in a table
            - can be used to determine if table is wide or not
    
    get_table_columns()
            - returns the columns in a table
    
    table_exists()
            - tests if a table exists or not
    
    delete_table()
            - deletes the table in a database
    
    create_table()
            - creates a table in a database
    
    truncate_table()
            - delete all the contents in a table

    delete_records()
            - delete certain records of the table
    
    insert()
           - inserts values into a table in a database
    
    update()
          - update existing columns in a table
    
    get_wide_columns()
            - check the columns from the table

    Attributes:
    bool_is_connected
            - flag to determine if the connection is open or closed
                True -> connection is open
                False -> connection is closed
    '''

    def __init__(self, list_conn_param = []):
        '''      
        this method initialized the class; if a list is paassed and has all the paramaters a connection will be generated to
        the sql server
        
        Requirements:
        package pymssql
        
        Inputs:
        list_conn_param
        Type: list
        Desc: the paramaters to generate the connection to the sql server
        list_conn_param[0] -> type: string; user name
        list_conn_param[1] -> type: string; host or server
        list_conn_param[2] -> type: string; user password
        list_conn_param[3] -> type: string; database name
        
        Important Info:
        1. the paramaters must use r'xxxxx' as raw strings but is used in relational expressions,
            eg. m_string_user = r'user name'
        
        Objects and Properties:
        list_conn
        Type: list
        Desc: the connection paramaters
        _list_conn[0] -> type: boolean; True of a connection was generated; False if not
        _list_conn[1] -> type: pymssql connection; the connection object to the sql server

        bool_is_connected
        Type: boolean
        Desc: flag to help the user to determine if the connection is generated
        '''
        
        # objects for the class
        self._list_conn = list()
        self._dict_flags = {}
        self.bool_is_connected = False
        
        # test pamater list to generate the connection
        if len(list_conn_param) == 4 and isinstance(list_conn_param, collections.Sequence) and not isinstance(
            list_conn_param, str):
            self.gen_connection(m_string_user = list_conn_param[0],
                                              m_string_host = list_conn_param[1],
                                              m_string_pswd = list_conn_param[2],
                                              m_string_db_name = list_conn_param[3])

    def _update_flags(self, *args):
        '''
        '''
        self._dict_flags = {'bool_is_connected':self._list_conn[0]}

        for string_flag in args:
            if string_flag in self._dict_flags.keys():
                if string_flag == 'bool_is_connected':
                    self.bool_is_connected = self._dict_flags[string_flag]

    def _build_column_string(self, m_list = [], bool_insert = False):
        '''
        this method will create a string that represents the columns from m_list
        
        Requirements:
        None
        
        Inputs:
        m_list_values
        Type: list
        Desc: the list of columns or values to create the string
        
        bool_insert
        Type: boolean
        Desc: a flag to if this is used to insert to another statement
         
        Important Info:
        None
         
        Return:
        variable
        Type: string
        Desc: this string has the parentheses and just need to be appended to the sql statement string
                   error can be detected by testing for the empty string
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#    
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        str_return_string = ''

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#     

        # build column string
        for element in m_list:
            str_return_string += str(element) + ','

        # clean up the return string
        if bool_insert == True:
            str_return_string = '(' + str_return_string[:-1] + ')'
        else:
            str_return_string = str_return_string[:-1]
    
        return str_return_string

    def gen_connection(self, m_string_user, m_string_host, m_string_pswd, m_string_db_name):
        '''
        this creates a connect to the designated sql server (m_string_host) and database and returns that connection
        
        Requirements:
        package pymssql
        
        Inputs:
        m_string_user
        Type: string
        Desc: the designated user that will connect to the database
        
        m_string_host
        Type: string
        Desc: the host / sql server to connect to
        
        m_psm_string_pswdwd
        Type: string
        Desc: the password for the user
        
        m_string_db_name
        Type: string
        Desc: the database to connect to on the host / sql server
        
        Important Info:
        1. for the paramaters must use r'xxxxx' as raw strings but is used in relational expressions,
            eg. m_string_user = r'user name'
        2. this is just the connection and does not include the cursor that is needed or that will hold the data from the 
            server connection
        
        Return:
        list
        Type: list
        Desc: a two element list which will tell if there is a connection or not; will add this to the list_conn
        list_connection[0] -> type: boolean; if True the connection is good and connected to the server, if False did not 
                                                connect to the server
        list_connection[1] -> type: pymssql sql server connection object; if list_connection[0] is true then there this will be
                                                be populated with the sql connection; if false this will be empty string object
        '''

        #------------------------------------------------------------------------------------------------------------------------------------------------------#    
        # sequence declarations (list, set, tuple)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_connection = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#    
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        bool_connection = False
        sql_conn = ''

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # generate connection
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        try:
            sql_conn = pymssql.connect(m_string_host, m_string_user, m_string_pswd, m_string_db_name)
        except pymssql.OperationalError as oe:
            sql_conn = 'Operational Error raised|'
            sql_conn += str(oe.args)
        except pymssql.Error as e:
            sql_conn = 'General error raised|'
            sql_conn += str(e.args)
        else:
            bool_connection = True
        finally:
            list_connection.append(bool_connection)
            list_connection.append(sql_conn)

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return variables / objects
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        self._list_conn = list_connection
        self._update_flags('bool_is_connected')

    def close(self):
        '''
        this method closes the connetion if it exists
        
        Requirements:
        package pymssql
        
        Inputs:
        None
        
        Important Info:
        None
        
        Return:
        None
        Type: n/a
        Desc: n/a
        '''
        if self._list_conn[0] == True:
            self._list_conn[1].close()
            self._list_conn[0] = False
            self._update_flags('bool_is_connected')

    def gen_select_statement(self, m_string_init = '', m_string_select = '', m_string_from = '', m_string_where = '', 
                                               m_string_end = ''):
        '''
        this method generates the select query string from the server
        
        Requirements:
        None
        
        Inputs:
        m_string_init
        Type: string
        Desc: any text before the select statement
          
        m_string_select
        Type: string
        Desc: table to pull the data from
          
        m_string_from
        Type: string
        Desc: the tables select from the table or anything after the 'FROM' statement
          
        m_string_where
        Type: string
        Desc: any qualifiers to be able to select the data based on any columns
          
        m_string_end
        Type: string
        Desc: any text after the where statement
          
        Important Info:
        none
        
        Return:
        variable
        Type: string
        Desc: the select query string to get the data
        '''

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        str_return = ''
        
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#   

        # test for initial part of string
        if len(m_string_init) > 0:
            str_return += m_string_init

        # test if there is a select string
        if len(m_string_select) > 0:
            str_return += r' SELECT ' + m_string_select

        # test for from string
        if len(m_string_from) > 0:
            str_return += r' FROM ' + m_string_from

        # test for where string
        if len(m_string_where) > 0:
            str_return += r' WHERE ' + m_string_where

        # test for end string
        if len(m_string_end) > 0:
            str_return += ' ' + m_string_end

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        return str_return

    def get_table_columns(self, m_string_table):
        '''
        this method will return three lists the columns names and the data types in a database on a sql server in a pymssql
        format and the sql data types
        
        Requirements:
        package pymssql
        
        Inputs:
        m_string_table
        Type: string
        Desc: the name of the table to get the number of columns
          
        Important Info:
        ensure table names are in the format schema.table_name
        
        Return:
        object
        Type: list, if no connect return None
        Desc: a list which will indicate the columns and if there was an error
        list_return[0] -> type: bool; True if SQL query to return the columns executed, False if throws an error
        list_return[1] -> if list_return[0] == True; type:list; the columns from the table
                                     if list_return[0] == False; type:string; text describing the error
        list_return[2] -> type: bool; True if SQL query to return the columns data type, False if throws an error
        list_return[3] -> if list_return[2] == True; type:list; the columns data type for pymssql / python
                                     if list_return[2] == False; type:string; text describing the error
        list_return[4] -> if list_return[2] == True; type:list; the columns data type for sql
                                     if list_return[2] == False; empty
        list_return[5] -> if list_return[2] == True; type:list; the columns data type for sql declaration to create a table
                                     if list_return[2] == False; empty
        '''

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # objects declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # time declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_columns = list()
        list_data_type = list()
        list_col_dec = list()
        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        # schema and table name
        string_schema, string_table_name = m_string_table.split('.')
        
        # where clause
        string_query_col_where = "TABLE_NAME = N'" + string_table_name + "' and TABLE_SCHEMA = '" + \
                                                    string_schema + "'"
        # columns queries
        str_query_col = self.gen_select_statement(m_string_select = 'COLUMN_NAME', 
                                                                            m_string_from = 'INFORMATION_SCHEMA.COLUMNS',
                                                                           m_string_where = string_query_col_where,
                                                                           m_string_end = 'Order by ORDINAL_POSITION') 
        str_query_dt = self.gen_select_statement(m_string_select = 'DATA_TYPE', 
                                                                         m_string_from = 'INFORMATION_SCHEMA.COLUMNS', \
                                                                         m_string_where = string_query_col_where,
                                                                         m_string_end = 'Order by ORDINAL_POSITION') 
        str_query_sys_table_obj_id = self.gen_select_statement(m_string_select = 'object_id',
                                                                        m_string_from = 'sys.tables',
                                                                        m_string_where = "name = '" + string_table_name + "'")

        # flags
        bool_columns = False
        bool_data_type = False
        bool_dec_01 = False
        bool_dec_02 = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#   

        if self._list_conn[0] == True:
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            # generate cursors
            #------------------------------------------------------------------------------------------------------------------------------------------------------#

            sql_cursor_col = self._list_conn[1].cursor()
            sql_cursor_dt = self._list_conn[1].cursor()
            sql_cursor_sql_dec_01 = self._list_conn[1].cursor()
            sql_cursor_sql_dec_02 = self._list_conn[1].cursor()

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # run column name query
            #------------------------------------------------------------------------------------------------------------------------------------------------------#

            try:
                sql_cursor_col.execute(str_query_col)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                # get the columns from the cursor
                list_raw_col = sql_cursor_col.fetchall()

                # convert the information in the tuple to a list
                list_columns = [x[0] for x in list_raw_col]

                # change boolean
                bool_columns = True
            finally:
                # fill the return list
                list_return.append(bool_columns)
                if bool_columns == True:
                    list_return.append(list_columns)
                else:
                    list_reutrn.append(str_sql_error)

            # close cursor
            sql_cursor_col.close()

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # run data type query
            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            
            try:
                sql_cursor_dt.execute(str_query_dt)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                # get the columns from the cursor
                list_raw_dt = sql_cursor_dt.fetchall()

                # convert the information in the tuple to a list
                list_sql_data_type = [x[0] for x in list_raw_dt]

                # convert sql data type to python data type used in 
                # pymssql for insert into a table
                list_py_data_type = ['%s' for x in list_sql_data_type]

                # change boolean
                bool_data_type = True
            finally:
                # fill the return list
                list_return.append(bool_data_type)
                if bool_data_type == True:
                    list_return.append(list_py_data_type)
                    list_return.append(list_sql_data_type)
                else:
                    list_return.append(str_sql_error)
                    list_return.append('')

            # close cursor
            sql_cursor_dt.close()

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # run sql delcaration column query
            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            
            try:
                sql_cursor_sql_dec_01.execute(str_query_sys_table_obj_id)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                # get the columns from the cursor
                list_raw_dec_01 = sql_cursor_sql_dec_01.fetchall()

                # convert the information in the tuple to a list
                string_table_obj_id = str(list_raw_dec_01[0][0])

                # change boolean
                bool_dec_01 = True
            finally:
                # test if retrieved object id
                if bool_dec_01 == False:
                    string_table_obj_id = ''

            # delete cursor
            sql_cursor_sql_dec_01.close()

            if len(string_table_obj_id) > 0:
                # generate the sql statement for the column name and the max length
                string_col_name_max_len = self.gen_select_statement(m_string_select = 'name, max_length, precision, scale',
                                                                                m_string_from = 'sys.columns',
                                                                                m_string_where = "object_id = '" + string_table_obj_id + "'")
                list_col_name_max_len = list()

                try:
                    sql_cursor_sql_dec_02.execute(string_col_name_max_len)
                except pymssql.OperationalError:
                    str_sql_error = 'Operational error was raised'
                except pymssql.ProgrammingError:
                    str_sql_error = 'A program error was raised.'
                except pymssql.Error:
                    str_sql_error = 'General error raised.'
                else:
                    # get the columns from the cursor
                    list_raw_dec_02 = sql_cursor_sql_dec_02.fetchall()

                    # convert the information in the tuple to a list
                    for tup_temp in list_raw_dec_02:
                        list_col_name_max_len.append([x for x in tup_temp])

                    # change boolean
                    bool_dec_02 = True
                finally:
                    pass

            # close cursor
            sql_cursor_sql_dec_02.close()

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # search to create the sql declaration column list
            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            
            for list_index in range(0, len(list_sql_data_type)):
                # get the data type
                string_col_data_type = list_sql_data_type[list_index]

                # pull out the varchar
                if string_col_data_type == 'varchar' or string_col_data_type == 'nvarchar' or string_col_data_type == 'char' \
                    or string_col_data_type == 'nchar':
                    string_col_name = list_columns[list_index]
                    for list_col in list_col_name_max_len:
                        if list_col[0] == string_col_name:
                            string_max_len = str(list_col[1])
                            break
                    list_col_dec.append(list_columns[list_index] + ' ' + string_col_data_type + '(' + string_max_len + ')')
                elif string_col_data_type == 'decimal':
                    string_col_name = list_columns[list_index]
                    for list_col in list_col_name_max_len:
                        if list_col[0] == string_col_name:
                            string_precision = str(list_col[2])
                            string_scale = str(list_col[3])
                            break
                    list_col_dec.append(list_columns[list_index] + ' ' + string_col_data_type + '(' + string_precision + \
                                    ',' + string_scale + ')')
                else:
                    list_col_dec.append(list_columns[list_index] + ' ' + string_col_data_type) 

            list_return.append(list_col_dec)

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # return value
            #------------------------------------------------------------------------------------------------------------------------------------------------------#

            return list_return
        
        else:
        
            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # return value
            #------------------------------------------------------------------------------------------------------------------------------------------------------#

            return None

    def table_exists(self, m_string_table):
        '''
        this method tests if a sql table exists in the database
        
        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: table to test if exists
        need to use scheme
        example: scheme.table_name; dbo.TestTable or FlowParts.DataRaw
          
        Important Info:
        None
        
        Return:
        variable
        Type: boolean
        Desc: return True of the table exists else it will return False
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # objects declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # time declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
        list_sch_tn = m_string_table.split('.')
        string_where = "TABLE_NAME = N'" + list_sch_tn[1] + "' and TABLE_SCHEMA = N'" + list_sch_tn[0] + "'"
        str_query = self.gen_select_statement('if exists (', '*', 'INFORMATION_SCHEMA.TABLES', string_where, 
                                       ") select 1 else select 0")
        bool_test_table = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#     

        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()

            # run the query
            sql_cursor.execute(str_query)

            # test the result of the query
            if sql_cursor.fetchone()[0] == 1:
                bool_test_table = True

            # delete cursor
            sql_cursor.close()

        # return value
        return bool_test_table

    def delete_table(self, m_table_name):
        '''
        this method deletes a table from a sql database
        
        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: table to test if exists
          
        Important Info:
        None
        
        Return:
        variable
        Type: boolean
        Desc: returns True if the table is dropped, False if not
        '''

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        str_query = 'DROP TABLE ' + m_table_name
        bool_deleted = False
        str_sql_error = ''

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#    

        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()

            # execute query
            try:
                sql_cursor.execute(str_query)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error = str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                bool_deleted = True
                self._list_conn[1].commit()
            finally:
                pass
    
            # delete cursor
            sql_cursor.close()

        # return object
        return bool_deleted

    def truncate_table(self, m_string_table):
        '''
        this method trucates a the table passed
        
        Requirements:
        package pymssql
        
        Inputs:
        m_sql_conn
        Type: pymssql connection object
        Desc: this is the connection to the sql server
         
        m_table_name
        Type: string
        Desc: table to test if exists
          
        Important Info:
        this method assumes that the table exists
        
        Return:
        variable
        Type: boolean
        Desc: returns True of the table is truncated, False if the table was not truncated
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#        

        str_query = r'TRUNCATE TABLE ' + m_string_table
        bool_truncate_table = False
        str_sql_error = ''
                
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

        if self._list_conn[0] == True:
            # create cursor
            sql_cursor = self._list_conn[1].cursor()

            # run the query
            try:
                sql_cursor.execute(str_query)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                bool_truncate_table = True
                #self._list_conn[1].commit()
            finally:
                pass

            # delete cursor
            sql_cursor.close()

        # return value
        return bool_truncate_table

    def query_select(self, m_string_sql_query = ''):
        '''
        this method gets the sql select query from the database
        
        Requirements:
        package pymssql
        
        Inputs:
        m_string_sql_query
        Type: string
        Desc: the sql query generated by method gen_selec_statement()
          
        Important Info:
        none
        
        Return:
        object
        Type: list 
        Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
        list_retunr[0] -> type: bool; True if sql statement executed with no errors, False if not
        list_return[1] -> if list_return[0] == True; type:integer; the results from the query
                                     if list_return[0] == False; type:string; text describing the error
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()
        list_results = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        bool_query = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#    

        if self._list_conn[0] == True:
            # generate cursor
            sql_cursor = self._list_conn[1].cursor()

            # try the select query
            try:
                sql_cursor.execute(m_string_sql_query)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                # get the columns from the cursor
                list_raw = sql_cursor.fetchall()

                # convert the information in the tuple to a list
                for tuple_temp in list_raw:
                    list_results.append([x for x in tuple_temp])

                # change boolean
                bool_query = True
            finally:
                pass

            # delete cursor
            sql_cursor.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return.append(bool_query)
        if bool_query == True:
            list_return.append(list_results)
        else:
            list_return.append(str_sql_error)
        return list_return

    def insert(self, m_string_table, m_list_columns, m_list_values):
        '''
        this method inserts data into a table
        
        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: table to test if exists
          
        m_list_columns
        Type: list
        Desc: the string of column names seperated by comas
          
        m_list_values
        Type: list of tuples
        Desc: the list of values that will be inserted into the table in the form of tuples
          
        Important Info:
        below is an example of how the insert into the table will work
        table : persons -> m_table_name
        data types: (%d, %s, %s) -> m_str_data_type
        values: [(1, 'John Smith', 'John Doe'), (2, 'Jane Doe', 'Joe Dog'),(3, 'Mike T.', 'Sarah H.')] -> m_list_values
        
        only the %s and %d data types are supported for the execute() and executemany() methods
        anything other than an integer (%d, signed integer) needs to be a %s, type checking is condcuted
        internally
         
        cursor.executemany( 
        "INSERT INTO persons VALUES (%d, %s, %s)",
        [(1, 'John Smith', 'John Doe'),
        (2, 'Jane Doe', 'Joe Dog'),
        (3, 'Mike T.', 'Sarah H.')])
        
        To insert into a wide table use the below format
        INSERT INTO table_name(column_name_01, column_name_02, column_name_03, column_name_04)
        VALUES (value_01, value_02, value_03, value_04);
        
        Return:
        object
        Type: list
        Desc: a list which will indicate if the sql statement is executed with or without errors
        list_retunr[0] -> type: bool; True if executed without error, False if not
        list_return[1] -> type:string; empty if the table is created and the type of error if not created
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        str_sql_error = ''
        string_data_type = ''
        str_sql_insert = 'INSERT INTO ' + m_string_table 
        str_sql_columns = self._build_column_string(m_list_columns, True)

        bool_insert_into_table = False
        int_segement_limit = 100000
        str_sql_error = 'no sql connection'

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                  
        
        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()

            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            # create data type string
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    

            if isinstance(m_list_values[0], collections.Sequence) and not isinstance(m_list_values[0], str):
                int_record_len = len(m_list_values[0])
            else:
                int_record_len = len(m_list_values)

            for int_len in range(0, int_record_len):
                string_data_type += '%s,'
            string_data_type = '(' + string_data_type[:-1] + ')'
    
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            # build execute many statement
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    

            str_sql_statement = str_sql_insert + ' ' + str_sql_columns + ' VALUES ' + string_data_type

            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            # list of tuples for insert
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    

            if isinstance(m_list_values[0], collections.Sequence) and not isinstance(m_list_values[0], str):
                list_insert_many = [tuple(x) for x in m_list_values]
            else:
                list_insert_many = [tuple(m_list_values)]

            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            # break up insert into segment limits
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            
            int_segments = int(len(list_insert_many) / int_segement_limit)
            bool_insert_into_table = True
            str_sql_error = ''

            #------------------------------------------------------------------------------------------------------------------------------------------------------#    
            # loop to insert values in list of tuples
            #------------------------------------------------------------------------------------------------------------------------------------------------------#    

            for int_seg in range(0, int_segments + 1):
                # split variables
                list_insert = list()
                int_lower = int_seg * int_segement_limit
                int_upper = int_lower + int_segement_limit

                # list split logic
                if int_seg == 0 and len(list_insert_many) < int_segement_limit:
                    list_insert = list_insert_many
                    int_seg = int_segments + 1
                elif int_seg != int_segments:
                    list_insert = list_insert_many[int_lower:int_upper]
                else:
                    list_insert = list_insert_many[int_lower:]

                # execute statement
                try:
                    sql_cursor.executemany(str_sql_statement, list_insert)
                except pymssql.OperationalError as oe:
                    str_sql_error += ';Operational error was raised' + str(oe.args)
                    bool_insert_into_table = False
                except pymssql.ProgrammingError as pe:
                    str_sql_error += ';A program error was raised|' + str(pe.args)
                    bool_insert_into_table = False
                except pymssql.DatabaseError as dbe:
                    str_sql_error += ';Database error raised|' + str(dbe.args)
                    bool_insert_into_table = False
                except pymssql.DataError as de:
                    str_sql_error += ';Data error raised|' + str(de.args)
                    bool_insert_into_table = False
                except pymssql.IntegrityError as inte:
                    str_sql_error += ';Integrity error raised|' + str(inte.args)
                    bool_insert_into_table = False
                except pymssql.InterfaceError as ife:
                    str_sql_error += ';Interface error raised|' + str(ife.args)
                    bool_insert_into_table = False
                except pymssql.InternalError as ie:
                    str_sql_error += ';Internal error raised|' + str(ie.args)
                    bool_insert_into_table = False
                except pymssql.NotSupportedError as nse:
                    str_sql_error += ';Not supported error raised|' + str(nse.args)
                    bool_insert_into_table = False
                except pymssql.StandardError as se:
                    str_sql_error += ';Standard error raised|' + str(se.args)
                    bool_insert_into_table = False
                except pymssql.Error as e:
                    str_sql_error += ';General error raised|' + str(e.args)
                    bool_insert_into_table = False
                else:
                    self._list_conn[1].commit()
                finally:
                    pass

            # delete cursor
            sql_cursor.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # append return list
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return.append(bool_insert_into_table)
        list_return.append(str_sql_error)
        return list_return

    def create_table(self, m_string_table, m_list_columns, m_bool_wide_table = False, m_bool_compression = True):
        '''
        this method creates a table in a sql database
        
        Requirements:
        package pymssql
        
        Inputs:
        m_sql_connection
        Type: pymssql connection object
        Desc: this is the connection to the sql server
        
        m_table_name
        Type: string
        Desc: table to test if exists
          
        m_list_columns
        Type: list of strings
        Desc: the columns to create the table
                each entry must be in the format of 'column_name column_data_type'
                the name of the column is first, a space, then the data type of the column
                this must be in a format that the sql database can read
                example: 'str_OrderNumber varchar(60)' or 'in_LineNumber int' or 'date_CreationDate datetime'
          
        m_bool_wide_table
        Type: boolean
        Desc: flag to indicate if the table should be wide or narrow
          
        m_bool_compression
        Type: boolean
        Desc: flag to enable data compression for the table
          
        Important Info:
        we are assuing the database in the connection is created and the table does not exist
        this method does not check if the table does not exist
        
        a wide table increases the max columns from 1,064 to 30,000; make sure you take into account
        the XML required when adding or reading data from the table; the wide uses a version of a sparse
        matrix to account for data that is not in a column; MAKE SURE a precursor is added to a number 000 to make
        it a valid column name
        
        Return:
        object
        Type: list
        Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
        list_return[0] -> type: bool; True if table created, False if not
        list_return[1] -> type:string; empty if the table is created and the type of error if not created
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        str_create = 'CREATE TABLE ' + m_string_table + '('
        bool_created = False
        str_sql_error = 'no sql connection'

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#     

        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()
            str_sql_error = ''

            #------------------------------------------------------------------------------------------------------------------------------------------------------# 
            # create sql statement
            #------------------------------------------------------------------------------------------------------------------------------------------------------# 

            for col_var in m_list_columns:
                # account for wide or narrow table
                if m_bool_wide_table == True:
                    str_create += col_var + ' SPARSE,'
                else:
                    str_create += col_var + ','

            str_create = str_create[:-1]

            # close out statement
            if m_bool_wide_table == True:
                str_create += ', XML_Record XML COLUMN_SET FOR ALL_SPARSE_COLUMNS) '
            else:
                str_create += ') '

            # add table compression
            if m_bool_compression == True:
                str_create += 'WITH (DATA_COMPRESSION = PAGE)'

            #------------------------------------------------------------------------------------------------------------------------------------------------------# 
            # execute sql statement
            #------------------------------------------------------------------------------------------------------------------------------------------------------# 
            
            try:
                sql_cursor.execute(str_create)
            except pymssql.OperationalError as e:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(e.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                bool_created = True
                self._list_conn[1].commit()
            finally:
                pass

            # delete cursor
            sql_cursor.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return.append(bool_created)
        list_return.append(str_sql_error)
        return list_return

    def update(self, m_table_name, m_list_columns, m_list_values, m_string_where = ''):
        '''
        this method updates specific columns in a table
        
        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: table to test if exists
          
        m_list_columns
        Type: list
        Desc: the string of column names to update the values
          
        m_list_values
        Type: list
        Desc: the list of values to update the columns
          
        m_string_where
        type: string
        Desc: appended to 'where' to for where statement
        
        Important Info:
        the length of lists m_list_columns and m_list_values must be in the same length and order
        m_list_columns = ['string_column01', 'string_column02', ...]
        m_list_values = [value_01, value_02, ...]
        
        below is a generic example of how to update a table with values
        UPDATE string_table_name
        SET string_column01 = value_01, string_column02 = value_02, ...
        where condition;
        
        Return:
        object
        Type: list
        Desc: returns true or false and the reason if false
        list[0] type: boolean; True if no errors, False if there are errors
        list[1] type: string, the error explanation if false, if true string 'None'
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        string_sql_update = 'update ' + m_table_name + ' '
        string_sql_set = 'set '
        string_sql_where = 'where '
        string_error = 'no sql connection'
        bool_list_length_error = False
        bool_return = False

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # build sql strings
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()
            string_error = ''

            # build set string
            try:
                if len(m_list_columns) == len(m_list_values) and len(m_list_columns) != 0:
                    for int_index in range(0, len(m_list_columns)):
                        if type(m_list_values[int_index]) == str:
                            string_sql_set += str(m_list_columns[int_index]) + " = '" + str(m_list_values[int_index]) + "', "
                        else:
                            string_sql_set += str(m_list_columns[int_index]) + " = " + str(m_list_values[int_index]) + ", "

                    string_sql_set = string_sql_set[:-2]
                else:
                    raise Exception('column and value lists are not the same length')
            except Exception as e:
                string_error += str(e.args)
                bool_list_length_error = True
            else:
                pass
            finally:
                pass

            # build where string
            if len(m_string_where) > 0:
                string_sql_where += m_string_where
            else:
                string_sql_where = ''

            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
            #
            # execute sql statement
            #
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#    
    
            if bool_list_length_error == False:
                try:
                    sql_cursor.execute(string_sql_update + string_sql_set + ' ' + string_sql_where)
                except pymssql.OperationalError as oe:
                    string_error = 'Operational error was raised|'
                    string_error += str(oe.args)
                except pymssql.ProgrammingError as pe:
                    string_error = 'A program error was raised|'
                    string_error += str(pe.args)
                except pymssql.DatabaseError as dbe:
                    string_error = 'Database error raised|'
                    string_error += str(dbe.args)
                except pymssql.DataError as de:
                    string_error = 'Data error raised;'
                    string_error += str(de.args)
                except pymssql.IntegrityError as inte:
                    string_error = 'Integrity error raised;'
                    string_error += str(inte.args)
                except pymssql.InterfaceError as ife:
                    string_error = 'Interface error raised;'
                    string_error += str(ife.args)
                except pymssql.InternalError as ie:
                    string_error = 'Internal error raised;'
                    string_error += str(ie.args)
                except pymssql.NotSupportedError as nse:
                    string_error = 'Not supported error raised;'
                    string_error += str(nse.args)
                except pymssql.StandardError as se:
                    string_error = 'Standard error raised;'
                    string_error += str(se.args)
                except pymssql.Error as e:
                    string_error = 'General error raised;'
                    string_error += str(e.args)
                else:
                    string_error = ''
                    bool_return = True
                    #self._list_conn[1].commit()
                finally:
                    pass

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # variable / object cleanup
            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            sql_cursor.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        if bool_return & ~bool_list_length_error == True:
            bool_return = True
        else:
            bool_return = False

        list_return.append(bool_return)
        list_return.append(string_error)
        return list_return

    def delete_records(self, m_table_name, m_list_where):
        '''
        this method deletes records in the table based on the where clauses in the list
        
        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: table to test if exists
          
        m_list_where
        Type: list
        Desc: the list of where clauses that will identify the records to delete in the table
          
        Important Info:
        below is an example of how delete records in a table (sql)
        DELETE FROM Customers # this is the table name
        WHERE CustomerName='Alfreds Futterkiste' # this is the beginning of the where clauses
        AND ContactName='Maria Anders'
        
        the 'AND' / 'OR' needs to be included in the where clauses
        
        Return:
        object
        Type: list
        Desc: a list which will indicate if the sql statement is executed with or without errors
        list_retunr[0] -> type: bool; True if executed without error, False if not
        list_return[1] -> type:string; empty if the table is created and the type of error if not created
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        str_sql_error = 'no sql connection'
        str_sql_delete_records = 'DELETE FROM ' + m_table_name + ' WHERE '
        bool_insert_into_table = False
        
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#      

        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()
            str_sql_error = ''

            # add where clauses to sql statement
            for string_w in m_list_where:
                str_sql_delete_records += string_w

            # execute statement
            try:
                sql_cursor.execute(str_sql_delete_records)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            except pymssql.DatabaseError as dbe:
                str_sql_error = 'Database error raised|'
                str_sql_error += str(dbe.args)
            except pymssql.DataError as de:
                str_sql_error = 'Data error raised|'
                str_sql_error += str(de.args)
            except pymssql.IntegrityError as inte:
                str_sql_error = 'Integrity error raised|'
                str_sql_error += str(inte.args)
            except pymssql.InterfaceError as ife:
                str_sql_error = 'Interface error raised|'
                str_sql_error += str(ife.args)
            except pymssql.InternalError as ie:
                str_sql_error = 'Internal error raised|'
                str_sql_error += str(ie.args)
            except pymssql.NotSupportedError as nse:
                str_sql_error = 'Not supported error raised|'
                str_sql_error += str(nse.args)
            except pymssql.StandardError as se:
                str_sql_error = 'Standard error raised|'
                str_sql_error += str(se.args)
            else:
                bool_insert_into_table = True
                #self._list_conn[1].commit()
            finally:
                pass

            # delete cursor
            sql_cursor.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return.append(bool_insert_into_table)
        list_return.append(str_sql_error)
        return list_return

    def get_wide_columns(self, m_string_table):
        '''
        this method obtains all the columns in a wide table since the wide table is in XML; all the reocords in the table 
        need to be checked to determine the entire list of columns
        
        Requirements:
        package xml.dom.minidom
        
        Inputs:
        list_columns
        Type: list of strings
        Desc: the columns from the table to check
         
        list_check
        Type: list of strings
        Desc: the columns names to check in list_columns
          
        Important Info:
        None
         
        Return:
        object
        Type: list
        Desc: list of all the columns names as strings
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # lists
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
        string_sql_query = self.gen_select_statement(m_string_select = '*', m_string_from = m_string_table)

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # objects
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # initialize lists
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#    

        # check to ensure the table exists
        bool_table_exists = self.table_exists(m_string_table)

        # if the table exits
        if bool_table_exists == True:
            # get all the recoreds (xml)
            list_sql_query_results = self.query_select(string_sql_query)

            if list_sql_query_results[0] == True:
                for list_result in list_sql_query_results[1]:
                    # create xml record
                    string_record = '<record>' + list_result[0] + '</record>'
                    xml_parse = minidom.parseString(string_record)

                    # get the data nodes
                    xmlnodelist_xml_nodes = xml_parse.childNodes[0].childNodes

                    # loop through the nodes to get the names
                    list_node_names = list()
                    for xml_node in xmlnodelist_xml_nodes:
                        list_node_names.append(xml_node.nodeName)
                
                    #list_columns_temp = [x for x in list_node_names if x not in list_columns]
                    list_return.extend([x for x in list_node_names if x not in list_return])

        # return value
        return list_return

    def get_num_columns(self, m_table_name):
        '''
        this method will return the number of columns in a table in a database on a sql server
        
        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: the name of the table to get the number of columns
          
        Important Info:
        1. table name must include schema; e.g. schema.table_name
        2. can be used to determine if a table is a wide or narrow table; 
                if the table is narrow the number of columns is <= 1,024 
                if the table is wide the number of columns will be zero
        
        Return:
        object
        Type: list 
        Desc: the number of columns if a narrow table or zero if a wide table; otherwise and error is returned
        list_return[0] -> type: bool; True if sql statement executed with no errors, False if not
        list_return[1] -> if list_return[0] == True; type:integer; the number of columns in the table
                                 if list_return[0] == False; type:string; text describing the error
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        string_schema, string_table = m_table_name.split('.')
        str_query_num_col = self.gen_select_statement(m_string_select = 'COUNT(*)', 
                                                                                       m_string_from = 'INFORMATION_SCHEMA.COLUMNS', \
                                                                                       m_string_where = "table_name = N'" + string_table + "' and " + \
                                                                                                                      "table_schema = N'" + string_schema + "'") 
        str_query_wide = self.gen_select_statement(m_string_init = 'if exists (',
                                                                                 m_string_select =  '*', 
                                                                                 m_string_from = 'INFORMATION_SCHEMA.COLUMNS',
                                                                                 m_string_where = "TABLE_NAME = N'" + string_table + \
                                                                                                               "TABLE_SCHEMA = N'" + string_schema + "'" + 
                                                                                                               "' AND COLUMN_NAME = N'XML_Record'",
                                                                                 m_string_end = ') select 1 else select 0')
        bool_num_col = False
        bool_table_wide = False
        str_sql_error = 'no sql connection'

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#       

        # return list if no connection
        list_return = [bool_num_col, str_sql_error]

        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()
            str_sql_error = ''

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # testing for narrow table
            #------------------------------------------------------------------------------------------------------------------------------------------------------#

            # run query to get the number of columns in the table
            try:
                sql_cursor.execute(str_query_num_col)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                # get the number of columns
                int_return = sql_cursor.fetchone()[0]
                bool_num_col = True

            # delete cursor
            sql_cursor.close()

            #------------------------------------------------------------------------------------------------------------------------------------------------------#
            # testing for wide table
            #------------------------------------------------------------------------------------------------------------------------------------------------------#

            # cursor to test for wide table
            sql_cursor_wide = self._list_conn[1].cursor()
    
            # run query to test for wide table
            try:
                sql_cursor_wide.execute(str_query_wide)
            except pymssql.OperationalError as oe:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(oe.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                # set boolean
                bool_table_wide = True

                # test if the the table is wide
                if sql_cursor_wide.fetchone()[0] == 1:
                    int_return -= 1
    
            # fill the return list
            list_return = [bool_num_col]
            if bool_num_col == True:
                list_return.append(int_return)
            else:
                list_reutrn.append(str_sql_error)

            # delete cursor
            sql_cursor_wide.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        return list_return

    def alter_table(self, m_string_table, m_string_command = '', m_bool_add_column = False, 
                    m_bool_drop_column = False, m_bool_alter_column = False):
        '''
        This method alters the table with the combination of the boolean flags and the command string

        Requirements:
        package pymssql
        
        Inputs:
        m_table_name
        Type: string
        Desc: the name of the table to get the number of columns

        m_string_command
        Type: string
        Desc: the phrase with will accompany the flag
            if m_bool_add_column is True -> columns_name column_type
            if m_bool_drop_column is True -> columns_name
            if m_bool_alter_column is True -> columns_name column_type

        m_bool_add_column
        Type: boolean
        Desc: flag to add a column

        m_bool_drop_column
        Type: boolean
        Desc: flag to drop a column

        m_bool_alter_column
        Type: boolean
        Desc: flag to change a column
          
        Important Info:
        None
        
        Return:
        object
        Type: list 
        Desc: the return value to determine if the command executed correctly
        list_return[0] -> type: bool; True if sql statement executed with no errors, False if not
        list_return[1] -> if list_return[0] == True; type:string; empty string
                                 if list_return[0] == False; type:string; text describing the error
        '''
        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # sequence declarations (list, set, tuple, dictionary, counter)
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        list_return = list()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # variables declarations
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        if m_bool_add_column == True:
            string_sql = 'alter table ' + m_string_table + ' add ' + m_string_command
        elif m_bool_drop_column == True:
            string_sql = 'alter table ' + m_string_table + ' drop ' + m_string_command
        elif m_bool_alter_column == True:
            string_sql = 'alter table ' + m_string_table + ' alter column ' + m_string_command
        else:
            pass
        string_error = 'no sql connection'
        bool_alter_table = False
        
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #
        # Start
        #
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#            
        
        if self._list_conn[0] == True:
            # gen cursor
            sql_cursor = self._list_conn[1].cursor()
            string_error = ''

            #------------------------------------------------------------------------------------------------------------------------------------------------------# 
            # execute sql statement
            #------------------------------------------------------------------------------------------------------------------------------------------------------# 
            
            try:
                sql_cursor.execute(string_sql)
            except pymssql.OperationalError as e:
                str_sql_error = 'Operational error was raised|'
                str_sql_error += str(e.args)
            except pymssql.ProgrammingError as pe:
                str_sql_error = 'A program error was raised|'
                str_sql_error += str(pe.args)
            except pymssql.Error as e:
                str_sql_error = 'General error raised|'
                str_sql_error += str(e.args)
            else:
                bool_alter_table = True
                #self._list_conn[1].commit()
            finally:
                pass

            # delete cursor
            sql_cursor.close()

        #------------------------------------------------------------------------------------------------------------------------------------------------------#
        # return value
        #------------------------------------------------------------------------------------------------------------------------------------------------------#

        return [bool_alter_table, string_error]