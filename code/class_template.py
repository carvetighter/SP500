'''
Class template
'''

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

import collections

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Classes
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

class ClassName(object):
    '''
    This class makes it easier to connect and work with a sql server.  The list of methods below are
    firther defined in the methods themselves

    Requirements:
    package pymssql
    package collections
    packace xml.dom.minidom

    Methods:
    gen_connection()
        creates connection to the database

    method_name()
        ....

    Attributes:
    bool_is_connected
        flag to determine if the connection is open or closed
            True -> connection is open
            False -> connection is closed
    '''

    #--------------------------------------------------------------------------#
    # constructor
    #--------------------------------------------------------------------------#

    def __init__(self, list_conn_param):
        '''
        this method initialized the class; if a list is paassed and has all the paramaters a connection will
        be generated to the sql server

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
        if len(list_conn_param) == 4 and isinstance(list_conn_param, collections.Sequence) and \
                not isinstance(list_conn_param, str):
            self.gen_connection(
                m_string_user = list_conn_param[0],
                m_string_host = list_conn_param[1],
                m_string_pswd = list_conn_param[2],
                m_string_db_name = list_conn_param[3])

    #--------------------------------------------------------------------------#
    # callable methods
    # 
    # methods that directly support callable methods should
    # be underneath method
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

    #--------------------------------------------------------------------------#
    # supportive methods
    #--------------------------------------------------------------------------#

    def _update_flags(self, *args):
        '''
        '''
        self._dict_flags = {'bool_is_connected':self._list_conn[0]}

        for string_flag in args:
            if string_flag in self._dict_flags.keys():
                if string_flag == 'bool_is_connected':
                    self.bool_is_connected = self._dict_flags[string_flag]
