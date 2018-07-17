###############################################################################################
###############################################################################################
#
# This import file <SqlMethods.py>covers the SQL methods that were created to make it easier to work with a 
# microsoft SQL server.
#
# Requirements:
# package pymssql
#
# Methods included:
# SqlGenConnection
#        - this method creates a connects to a sql server and specific database
#
# SqlGenSelectStatement
#        - generates the sql select staement
#
# SqlGetNumTableColumns
#        - returns the number of columns in a table
#
# SqlGetTableColumns
#        - returns the columns in a table
#
# SqlTestTableExists
#        - tests if a table exists or not
#
# SqlDeleteTable
#        - deletes the table in a database
#
# SqlCreateTable
#        - creates a table in a database
#
# SqlTruncateTable
#        - delete all the contents in a table
#
# SqlBuildColumnOrDataOrValueString
#        - is associated with the method SqlInsertIntoTable()
#        - builds the the column, data or value string for the insert statement
#
# SqlInsertIntoTable
#        - inserts values into a table in a database
#
# SqlUpdateTable
#       - update existing columns in a table
#
# SqlWideColumns
#        - check the columns from the table
#
# Important Info:
# None
###############################################################################################
###############################################################################################

# package import
import pymssql, collections
from xml.dom import minidom

def SqlGenConnection(m_user, m_host, m_pswd, m_db_name):
    ###############################################################################################
    ###############################################################################################
    #
    # this creates a connect to the designated sql server (m_host) and database and returns that connection
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_user
    # Type: string
    # Desc: the designated user that will connect to the database
    #
    # m_host
    # Type: string
    # Desc: the host / sql server to connect to
    #
    # m_pswd
    # Type: string
    # Desc: the password for the user
    #
    # m_db_name
    # Type: string
    # Desc: the database to connect to on the host / sql server
    #
    # Important Info:
    # this is just the connection and does not include the cursor that is needed or that will hold the data from the 
    # server connection
    #
    # Return:
    # list
    # Type: list
    # Desc: a two element list which will tell if there is a connection or not
    # list_connection[0] -> type: boolean; if True the connection is good and connected to the server, if False did not 
    #                                        connect to the server
    # list_connection[1] -> type: pymssql sql server connection object; if list_connection[0] is true then there this will be
    #                                        be populated with the sql connection; if false this will be empty string object
    ###############################################################################################
    ###############################################################################################

    # lists
    list_connection = list()

    # variables
    bool_connection = False
    sql_conn = ''

    # try to connect to the server
    try:
        sql_conn = pymssql.connect(m_host, m_user, m_pswd, m_db_name)
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

    return list_connection

def SqlGenSelectStatement(m_str_init = '', m_str_select = '', m_str_from = '', m_str_where = '', m_str_end = ''):
    ###############################################################################################
    ###############################################################################################
    #
    # this method generates the query string from the server
    #
    # Requirements:
    # None
    #
    # Inputs:
    # m_str_init
    # Type: string
    # Desc: any text before the select statement
    #  
    # m_str_select
    # Type: string
    # Desc: table to pull the data from
    #  
    # m_str_from
    # Type: string
    # Desc: the tables select from the table or anything after the 'FROM' statement
    #  
    # m_str_where
    # Type: string
    # Desc: any qualifiers to be able to select the data based on any columns
    #  
    # m_str_end
    # Type: string
    # Desc: any text after the where statement
    #  
    # Important Info:
    # none
    #
    # Return:
    # variable
    # Type: string
    # Desc: the query string to get the data
    ###############################################################################################
    ###############################################################################################

    # variables
    str_return = ''

    # test for initial part of string
    if len(m_str_init) > 0:
        str_return += m_str_init

    # test if there is a select string
    if len(m_str_select) > 0:
        str_return += r' SELECT ' + m_str_select

    # test for from string
    if len(m_str_from) > 0:
        str_return += r' FROM ' + m_str_from

    # test for where string
    if len(m_str_where) > 0:
        str_return += r' WHERE ' + m_str_where

    # test for end string
    if len(m_str_end) > 0:
        str_return += ' ' + m_str_end

    return str_return

def SqlQuerySelect(m_sql_connection, m_str_sql_query = ''):
    ###############################################################################################
    ###############################################################################################
    #
    # this method gets the sql query from the database
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_connection
    # Type: sql connection object
    # Desc: the connection to the sql database
    #
    # m_str_sql_query
    # Type: string
    # Desc: the sql query generated by method SqlGenSelectStatement()
    #  
    # Important Info:
    # none
    #
    # Return:
    # object
    # Type: list 
    # Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
    # list_retunr[0] -> type: bool; True if sql statement executed with no errors, False if not
    # list_return[1] -> if list_return[0] == True; type:integer; the results from the query
    #                             if list_return[0] == False; type:string; text describing the error
    ###############################################################################################
    ###############################################################################################

    # variables
    bool_query = False

    # lists
    list_return = list()
    list_results = list()
    
    # generate cursor
    sql_cursor = m_sql_connection.cursor()

    # try the select query
    # run query
    try:
        sql_cursor.execute(m_str_sql_query)
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
        # fill the return list
        list_return.append(bool_query)
        if bool_query == True:
            list_return.append(list_results)
        else:
            list_return.append(str_sql_error)

    # delete cursor
    sql_cursor.close()

    # return list
    return list_return

def SqlGetNumTableColumns(m_sql_conn, m_table_name):
    ###############################################################################################
    ###############################################################################################
    #
    # this method will return the number of columns in a table in a database on a sql server
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql.connection object
    # Desc: the connection to the database on the sql server
    #  
    # m_table_name
    # Type: string
    # Desc: the name of the table to get the number of columns
    #  
    # Important Info:
    # do not have the schema, such as 'dbo.' in front of the table name, it is not needed in this method
    #
    # Return:
    # object
    # Type: list 
    # Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
    # list_return[0] -> type: bool; True if sql statement executed with no errors, False if not
    # list_return[1] -> if list_return[0] == True; type:integer; the number of columns in the table
    #                             if list_return[0] == False; type:string; text describing the error
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_conn.cursor()
    
    # variables
    str_query_num_col = SqlGenSelectStatement(m_str_select = 'COUNT(*)', m_str_from = 'INFORMATION_SCHEMA.COLUMNS', \
                                                                              m_str_where = "table_name = '" + m_table_name + "'") 
    str_query_wide = SqlGenSelectStatement('if exists (', '*', 'INFORMATION_SCHEMA.COLUMNS', \
                                                                            "TABLE_NAME = N'" + m_table_name + "' AND COLUMN_NAME = N'SpecialPurposeColumns'", \
                                                                            ') select 1 else select 0')
    bool_num_col = False
    bool_table_wide = False
    str_sql_error = ''

    # lists
    list_return = list()

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

    # cursor to test for wide table
    sql_cursor_wide = m_sql_conn.cursor()
    
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
    list_return.append(bool_num_col)
    if bool_num_col == True:
        list_return.append(int_return)
    else:
        list_reutrn.append(str_sql_error)

    # delete cursor
    sql_cursor_wide.close()

    return list_return

def SqlGetTableColumns(m_sql_conn, m_table_name):
    ###############################################################################################
    ###############################################################################################
    #
    # this method will return three lists the columns names and the data types in a database on a sql server in a pymssql
    # format and the sql data types
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql.connection object
    # Desc: the connection to the database on the sql server
    #  
    # m_table_name
    # Type: string
    # Desc: the name of the table to get the number of columns
    #  
    # Important Info:
    # do not have the schema, such as 'dbo.' in front of the table name, it is not needed in this method
    #
    # Return:
    # object
    # Type: list 
    # Desc: a list which will indicate the columns and if there was an error
    # list_return[0] -> type: bool; True if SQL query to return the columns executed, False if throws an error
    # list_return[1] -> if list_return[0] == True; type:list; the columns from the table
    #                             if list_return[0] == False; type:string; text describing the error
    # list_return[2] -> type: bool; True if SQL query to return the columns data type, False if throws an error
    # list_return[3] -> if list_return[2] == True; type:list; the columns data type for pymssql / python
    #                             if list_return[2] == False; type:string; text describing the error
    # list_return[4] -> if list_return[2] == True; type:list; the columns data type for sql
    #                             if list_return[2] == False; empty
    # list_return[5] -> if list_return[2] == True; type:list; the columns data type for sql declaration to create a table
    #                             if list_return[2] == False; empty
    ###############################################################################################
    ###############################################################################################

    # objects
    # cast to cursor for intellisense in visual studio
    sql_cursor_col = m_sql_conn.cursor()
    sql_cursor_dt = m_sql_conn.cursor()
    sql_cursor_sql_dec_01 = m_sql_conn.cursor()
    sql_cursor_sql_dec_02 = m_sql_conn.cursor()
    
    # variables
    list_scheme_tablename = m_table_name.split('.')
    string_where = "TABLE_NAME = N'" + list_scheme_tablename[1] + "' and "
    string_where += "TABLE_SCHEMA = N'" + list_scheme_tablename[0] + "'"
    str_query_col = SqlGenSelectStatement(m_str_select = 'COLUMN_NAME', 
                                                                        m_str_from = 'INFORMATION_SCHEMA.COLUMNS',
                                                                       m_str_where = string_where,
                                                                       m_str_end = 'Order by ORDINAL_POSITION') 
    str_query_dt = SqlGenSelectStatement(m_str_select = 'DATA_TYPE', 
                                                                     m_str_from = 'INFORMATION_SCHEMA.COLUMNS', 
                                                                     m_str_where = string_where,
                                                                     m_str_end = 'Order by ORDINAL_POSITION') 
    str_query_sys_table_obj_id = SqlGenSelectStatement(m_str_select = 'object_id',
                                                                    m_str_from = 'sys.tables',
                                                                    m_str_where = "name = '" + m_table_name + "'")

    # flags
    bool_columns = False
    bool_data_type = False
    bool_dec_01 = False
    bool_dec_02 = False

    # lists
    list_columns = list()
    list_data_type = list()
    list_col_dec = list()
    list_return = list()

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

    # delete cursor
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
        list_py_data_type = SqlDataType(list_sql_data_type)

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
        list_raw_dec_01 = sql_cursor_dt.fetchall()

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
        string_col_name_max_len = SqlGenSelectStatement(m_str_select = 'name, max_length, precision, scale',
                                                                        m_str_from = 'sys.columns',
                                                                        m_str_where = "object_id = '" + string_table_obj_id + "'")
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
            list_raw_dec_02 = sql_cursor_dt.fetchall()

            # convert the information in the tuple to a list
            for tup_temp in list_raw_dec_02:
                list_col_name_max_len.append([x for x in tup_temp])

            # change boolean
            bool_dec_02 = True
        finally:
            pass

    # delete cursor
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

def SqlTestTableExists(m_sql_connection, m_table_name):
    ###############################################################################################
    ###############################################################################################
    #
    # this method tests if a sql table exists in the database
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_connection
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    # 
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    # need to use scheme
    # example: scheme.table_name; dbo.TestTable or FlowParts.DataRaw
    #  
    # Important Info:
    # None
    #
    # Return:
    # variable
    # Type: boolean
    # Desc: return True of the table exists else it will return False
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_connection.cursor()

    # variables
    list_sch_tn = m_table_name.split('.')
    string_where = "TABLE_NAME = N'" + list_sch_tn[1] + "' and TABLE_SCHEMA = N'" + list_sch_tn[0] + "'"
    str_query = SqlGenSelectStatement('if exists (', '*', 'INFORMATION_SCHEMA.TABLES', string_where, 
                                   ") select 1 else select 0")
    bool_test_table = False

    # run the query
    sql_cursor.execute(str_query)

    # test the result of the query
    if sql_cursor.fetchone()[0] == 1:
        bool_test_table = True

    # delete cursor
    sql_cursor.close()

    # return value
    return bool_test_table

def SqlDeleteTable(m_sql_connection, m_table_name):
    ###############################################################################################
    ###############################################################################################
    #
    # this method deletes a table from a sql database
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_connection
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    #
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    #  
    # Important Info:
    # None
    #
    # Return:
    # object
    # Type: list
    # Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
    # list_return[0] -> type: bool; True if table dropped, False if not
    # list_return[1] -> type:string; empty if the table is drpped and the type of error if not created
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_connection.cursor()

    # variables
    str_query = 'DROP TABLE ' + m_table_name
    bool_deleted = False
    str_sql_error = ''

    # lists
    list_return = list()

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
        m_sql_connection.commit()
    finally:
        list_return.append(bool_deleted)
        list_return.append(str_sql_error)
    
    # delete cursor
    sql_cursor.close()

    # return object
    return list_return

def SqlCreateTable(m_sql_connection, m_table_name, m_list_columns, m_bool_wide_table = True):
    ###############################################################################################
    ###############################################################################################
    #
    # this method creates a table in a sql database; 
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_connection
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    #
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    #  
    # m_list_columns
    # Type: list of strings
    # Desc: the columns to create the table
    #        each entry must be in the format of 'column_name column_data_type'
    #        the name of the column is first, a space, then the data type of the column
    #        this must be in a format that the sql database can read
    #        example: 'str_OrderNumber varchar(60)' or 'in_LineNumber int' or 'date_CreationDate datetime'
    #  
    # m_bool_wide_table
    # Type: boolean
    # Desc: flag to indicate if the table should be wide or narrow
    #  
    # Important Info:
    # we are assuing the database in the connection is created and the table does not exist
    # this method does not check if the table does not exist
    #
    # a wide table increases the max columns from 1,064 to 30,000; make sure you take into account
    # the XML required when adding or reading data from the table; the wide uses a version of a sparse
    # matrix to account for data that is not in a column; MAKE SURE a precursor is added to a number 000 to make
    # it a valid column name
    #
    # Return:
    # object
    # Type: list
    # Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
    # list_return[0] -> type: bool; True if table created, False if not
    # list_return[1] -> type:string; empty if the table is created and the type of error if not created
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_connection.cursor()

    # variables
    str_create = 'CREATE TABLE ' + m_table_name + '('
    bool_created = False
    str_sql_error = ''
    int_offset_counter = 0

    # lists
    list_return = list()

    # create sql statement
    for col_var in m_list_columns:
        # account for wide or narrow table
        if m_bool_wide_table == True:
            str_create += col_var + ' SPARSE,'
        else:
            str_create += col_var + ','

    str_create = str_create[:-1]

    # close out statement
    if m_bool_wide_table == True:
        str_create += ', SpecialPurposeColumns XML COLUMN_SET FOR ALL_SPARSE_COLUMNS)'
    else:
        str_create += ')'

    # execute sql statement
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
        m_sql_connection.commit()
    finally:
        # add information to the list
        list_return.append(bool_created)
        list_return.append(str_sql_error)

    # delete cursor
    sql_cursor.close()

    return list_return

def SqlTruncateTable(m_sql_conn, m_table_name):
    ###############################################################################################
    ###############################################################################################
    #
    # this method trucates a the table passed
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    # 
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    #  
    # Important Info:
    # this method assumes that the table exists
    #
    # Return:
    # object
    # Type: list
    # Desc: a list which will indicate if the table was dropped and if an effor occured what type of error
    # list_return[0] -> type: bool; True if table created, False if not
    # list_return[1] -> type:string; empty if the table is created and the type of error if not created
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_conn.cursor()
    list_return = list()

    # variables
    str_query = r'TRUNCATE TABLE ' + m_table_name
    bool_truncate_table = False
    str_sql_error = ''

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
        m_sql_conn.commit()
    finally:
        list_return.append(bool_truncate_table)
        list_return.append(str_sql_error)

    # delete cursor
    sql_cursor.close()

    # return value
    return list_return

def SqlBuildColumnOrDataOrValueString(m_list = [], m_list_data_types = [], m_string_vdc = '', bool_insert = False):
    ###############################################################################################
    ###############################################################################################
    #
    # this method will create a string that will be able to be inserted into a SQL INSERT statement for a column or 
    # values section of the sql statements
    #
    # Requirements:
    # None
    #
    # Inputs:
    # m_list_values
    # Type: list
    # Desc: the list of columns or values to create the string
    # 
    # m_list_data_types
    # Type: list
    # Desc: the list of for the values
    # 
    # m_string_vdc
    # Type: string
    # Desc: a string to indicate which part of the select statement to work on which has different criterea
    #    'values' -> work on the values section of the string
    # 'data type' -> work on the data type section of the statement
    # 'columns' -> work on the columns section of the statement
    #
    # bool_insert
    # Type: boolean
    # Desc: a flag to if this is used to insert to another statement
    # 
    # Important Info:
    # None
    # 
    # Return:
    # variable
    # Type: string
    # Desc: this string has the parentheses and just need to be appended to the sql statement string
    #                error can be detected by testing for the empty string
    ###############################################################################################
    ###############################################################################################

    # variables
    str_return_string = ''

    # check to make sure the lists are the same length
    if m_string_vdc == 'values':
        if len(m_list) == len(m_list_data_types):
            for index in range(0, len(m_list)):
                # get values
                str_data_type = m_list_data_types[index]
                str_value = str(m_list[index])

                # builds the value string
                if str_data_type == '%i' or str_data_type == '%f':
                    # if an integer or float do not put quotes around the value
                        str_return_string += str_value + ','
                else:
                    # if not an integer or float or byte put quotes around the value
                    str_return_string += "'" + str_value + "'" + ','
    elif m_string_vdc == 'columns':
        for index in range(0, len(m_list)):
            # get values
            str_value = str(m_list[index])
            str_return_string += str_value + ','
    elif m_string_vdc == 'data types':
        for data_type in m_list_data_types:
            str_return_string += data_type + ','
    else:
        pass

    # clean up the return string
    if bool_insert == True:
        str_return_string = '(' + str_return_string[:-1] + ')'
    else:
        str_return_string = str_return_string[:-1]
    
    return str_return_string

def SqlInsertIntoTable(m_sql_conn, m_table_name, m_list_columns, m_list_data_type, m_list_values,
                                    bool_exec_many = False):
    ###############################################################################################
    ###############################################################################################
    #
    # this method inserts data into a table
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    # 
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    #  
    # m_list_columns
    # Type: list
    # Desc: the string of column names seperated by comas
    #  
    # m_list_data_type
    # Type: list
    # Desc: the list data type which is associated with the list of columns and the list of values
    #  
    # m_list_values
    # Type: list of tuples
    # Desc: the list of values that will be inserted into the table in the form of tuples
    #  
    # bool_exec_many
    # Type: boolean
    # Desc: the flag to execute many sql inserts at a same time
    #  
    # Important Info:
    # below is an example of how the insert into the table will work
    # table : persons -> m_table_name
    # data types: (%d, %s, %s) -> m_str_data_type
    # values: [(1, 'John Smith', 'John Doe'), (2, 'Jane Doe', 'Joe Dog'),(3, 'Mike T.', 'Sarah H.')] -> m_list_values
    #
    # only the %s and %d data types are supported for the execute() and executemany() methods
    # anything other than an integer (%d, signed integer) needs to be a %s, type checking is condcuted
    # internally
    # 
    # cursor.executemany( 
    # "INSERT INTO persons VALUES (%d, %s, %s)",
    # [(1, 'John Smith', 'John Doe'),
    # (2, 'Jane Doe', 'Joe Dog'),
    # (3, 'Mike T.', 'Sarah H.')])
    #
    # To insert into a wide table use the below format
    # INSERT INTO table_name(column_name_01, column_name_02, column_name_03, column_name_04)
    # VALUES (value_01, value_02, value_03, value_04);
    #
    # Return:
    # object
    # Type: list
    # Desc: a list which will indicate if the sql statement is executed with or without errors
    # list_retunr[0] -> type: bool; True if executed without error, False if not
    # list_return[1] -> type:string; empty if the table is created and the type of error if not created
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_conn.cursor()

    # lists
    list_return = list()
    list_str_values = list()
    list_insert_many = list()

    # variables
    str_sql_error = ''
    bool_insert_into_table = False
    str_sql_insert = 'INSERT INTO ' + m_table_name 
    str_sql_columns = SqlBuildColumnOrDataOrValueString(m_list_columns, m_list_data_type, 'columns', True)
    str_sql_insert_values = SqlBuildColumnOrDataOrValueString(m_list_values, m_list_data_type, 'values', True)
    str_sql_data_types = SqlBuildColumnOrDataOrValueString(m_list_data_type, m_list_data_type, 'data types', True)
    
    # sql insert statement
    if bool_exec_many == True:
        # build execute many statement
        str_sql_statement = str_sql_insert + ' ' + str_sql_columns + ' VALUES ' + str_sql_data_types

        # list of tuples for insert
        if isinstance(m_list_values[0], collections.Sequence) and not isinstance(m_list_values[0], str):
            for record_insert in m_list_values:
                tuple_temp = tuple(record_insert)
                list_insert_many.append(tuple_temp)
        else:
                list_insert_many.append(tuple(m_list_values))
    else:
        # sql statement to insert one record
        str_sql_statement = str_sql_insert + ' ' + str_sql_columns + ' VALUES ' + str_sql_insert_values

    # execute statement
    try:
        if bool_exec_many == True:
            sql_cursor.executemany(str_sql_statement, list_insert_many)
        else:
            sql_cursor.execute(str_sql_statement)
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
        m_sql_conn.commit()
    finally:
        list_return.append(bool_insert_into_table)
        list_return.append(str_sql_error)

    # delete cursor
    sql_cursor.close()

    return list_return

def SqlUpdate(m_sql_conn, m_table_name, m_list_columns, m_list_col_data_type, m_list_values, m_list_where):
    ###############################################################################################
    ###############################################################################################
    #
    # this method updates specific columns in a table
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    # 
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    #  
    # m_list_columns
    # Type: list
    # Desc: the string of column names to update the values
    #  
    # m_list_col_data_type
    # Type: list
    # Desc: the data type of the column; %s or %d
    # %d -> signed integer
    # %s -> string
    # essentially everything else is a string unless it's and integer
    # if the entry needs quotes('' or "")  use %s else use %d
    #  
    # m_list_values
    # Type: list
    # Desc: the list of values to update the columns
    #  
    # m_list_where
    # type: list
    # Desc: list of where clauses
    #
    # Important Info:
    # the length of lists m_list_columns and m_list_values must be in the same length and order
    #
    # below is a generic example of how to update a table with values
    # UPDATE string_table_name
    # SET string_column01 = value_01, string_column02 = value_02, ...
    # where condition;
    #
    # Return:
    # object
    # Type: list
    # Desc: returns true or false and the reason if false
    # list[0] type: boolean; True if no errors, False if there are errors
    # list[1] type: string, the error explanation if false, if true string 'None'
    ###############################################################################################
    ###############################################################################################

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    # time variables

    # objects
    sql_cursor = m_sql_conn.cursor()

    # lists
    list_return = list()

    # variables
    string_sql_update = 'update ' + m_table_name + ' '
    string_sql_set = 'set '
    string_sql_where = 'where '
    string_error = ''
    bool_list_length_error = False
    bool_return = False

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # build sql strings
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    # build set string
    try:
        if len(m_list_columns) == len(m_list_values) and len(m_list_columns) != 0:
            for int_index in range(0, len(m_list_columns)):
                if m_list_col_data_type[int_index] == '%d':
                    string_sql_set += str(m_list_columns[int_index]) + " = " + str(m_list_values[int_index]) + ", "
                else:
                    string_sql_set += str(m_list_columns[int_index]) + " = '" + str(m_list_values[int_index]) + "', "

            string_sql_set = string_sql_set[:-2]
        else:
            raise Exception('column and value lists are not the same length')
    except Exception as e:
        string_error += e.args
        bool_list_length_error = True
    else:
        pass
    finally:
        pass

    # build where string
    if len(m_list_where) > 0:
        for string_w in m_list_where:
            string_sql_where += string_w + ', '

        string_sql_where = string_sql_where[:-2]

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
            string_error = 'None'
            bool_return = True
            m_sql_conn.commit()
        finally:
            list_return.append(bool_return)
            list_return.append(string_error)
    else:
        list_return.append(bool_return)
        list_return.append(string_error)

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object cleanup
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    sql_cursor.close()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # return value
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    return list_return

def SqlDeleteRecords(m_sql_conn, m_table_name, m_list_where):
    ###############################################################################################
    ###############################################################################################
    #
    # this method deletes records in the table based on the where clauses in the list
    #
    # Requirements:
    # package pymssql
    #
    # Inputs:
    # m_sql_conn
    # Type: pymssql connection object
    # Desc: this is the connection to the sql server
    # 
    # m_table_name
    # Type: string
    # Desc: table to test if exists
    #  
    # m_list_where
    # Type: list
    # Desc: the list of where clauses that will identify the records to delete in the table
    #  
    # Important Info:
    # below is an example of how delete records in a table (sql)
    # DELETE FROM Customers # this is the table name
    # WHERE CustomerName='Alfreds Futterkiste' # this is the beginning of the where clauses
    # AND ContactName='Maria Anders'
    #
    # the 'AND' / 'OR' needs to be included in the where clauses
    #
    # Return:
    # object
    # Type: list
    # Desc: a list which will indicate if the sql statement is executed with or without errors
    # list_retunr[0] -> type: bool; True if executed without error, False if not
    # list_return[1] -> type:string; empty if the table is created and the type of error if not created
    ###############################################################################################
    ###############################################################################################

    # objects
    sql_cursor = m_sql_conn.cursor()

    # lists
    list_return = list()

    # variables
    str_sql_error = ''
    str_sql_delete_records = 'DELETE FROM ' + m_table_name + ' WHERE '

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
        m_sql_conn.commit()
    finally:
        list_return.append(bool_insert_into_table)
        list_return.append(str_sql_error)

    # delete cursor
    sql_cursor.close()

    # return list
    return list_return

def SqlDataType(m_list_dt):

    ###############################################################################################
    ###############################################################################################
    #
    # this method converts the sql data type into a string that represents the sql data type that can be used with pymssql
    # to insert into a sql table using the method SqlInsertIntoTable
    #
    # Requirements:
    # None
    #
    # Inputs:
    # m_list_dt
    # Type: list
    # Desc: the list sql data types as strings
    #
    # Important Info:
    # %i -> integer
    # %f -> float, decimal
    # %s -> everything else
    #
    # Return:
    # object
    # Type: list
    # Desc: the data types as strings that are used with pymssql to insert into a table
    ###############################################################################################
    ###############################################################################################    

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variable / object declarations
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # lists / dictionaries
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    list_return = list()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#    
    # variables
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #
    # Start
    #
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # convert the sql data type to pymssql / python data type
    #------------------------------------------------------------------------------------------------------------------------------------------------------#        
    for data_type in m_list_dt:
        if data_type == 'float' or data_type == 'decimal' or data_type == 'money':
            list_return.append('%f')
        elif data_type == 'int':
            list_return.append('%i')
        else:
            list_return.append('%s')
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # return value
    #------------------------------------------------------------------------------------------------------------------------------------------------------#

    return list_return

def SqlWideColumns(m_sql_conn, m_string_table):
    ###############################################################################################
    ###############################################################################################
    #
    # this method obtains all the columns in a wide table since the wide table is in XML; all the reocords in the table 
    # need to be checked to determine the entire list of columns
    #
    # Requirements:
    # package xml.dom.minidom
    #
    # Inputs:
    # list_columns
    # Type: list of strings
    # Desc: the columns from the table to check
    # 
    # list_check
    # Type: list of strings
    # Desc: the columns names to check in list_columns
    #  
    # Important Info:
    # None
    # 
    # Return:
    # object
    # Type: list
    # Desc: list of all the columns names as strings
    ###############################################################################################
    ###############################################################################################
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # lists
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    list_return = list()

    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    # variables
    #------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    string_sql_query = SqlGenSelectStatement(m_str_select = '*', m_str_from = m_string_table)

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
    bool_table_exists = SqlTestTableExists(m_sql_conn, m_string_table)

    # if the table exits
    if bool_table_exists == True:
        # get all the recoreds (xml)
        list_sql_query_results = SqlQuerySelect(m_sql_conn, string_sql_query)

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
