from SqlMethods import SqlMethods
list_conn = [r'Frosty-SB-02\FROSTY SB 02', r'localhost\SQLEXPRESS', r'suM~=EqNV\D1', r'Finance']

sql_conn = SqlMethods(list_conn)
sql_conn.bool_is_connected


string_query_00 = '''
    select top 10 *
    from sp500.data
    '''
string_query_01 = '''
    select top 10 *
    from sp500.analysis
    '''
list_data_00 = sql_conn.query_select(string_query_00)
if list_data_00[0]:
    print(list_data_00[1])

list_data_01 = sql_conn.query_select(string_query_01)
if list_data_01[0]:
    print(list_data_01)