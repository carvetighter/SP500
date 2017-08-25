###############################################################################################
###############################################################################################
#
# This import file <DataVisAndEval.py> contains methods that evaluate and visualize cluster results using the 
# silhouette coeficient
#
# Requirements:
# package time
# package numpy
# package statistics
# package matplotlib.pyplot
# package matplotlib.cm
# package sklearn.metrics
#
# Methods included:
# EvaluateClusters()
#	- specific method for customer parts buying behavior model
#	- takes the cluster results and evaluates each cluster
#	- returns a list of cluster results
#
#	SaveClustEval()
#	- saves the cluster evaluations to a database
#	- saves cluster id, average of all sihloutte values, cluster label, cluster sihlouette value 
# 
#	VisualizeResults()
#	- visualized the sihlouette values from the evaluation
#	- creates a chart and saves that chart in a specified location
# 
# Important Info:
# None
###############################################################################################
###############################################################################################

# package import
import SqlMethods
import time, numpy, statistics
from matplotlib import pyplot, cm
from sklearn.metrics import silhouette_samples, silhouette_score

def EvaluateClusters(list_cluster_results, array_sparse_matrix):
    ###############################################################################################
    ###############################################################################################
    #
    # this method implements the evauluation criterea for the clusters of each clutering algorithms
	# criterea:
	#		- 1/2 of the clusters for each result need to be:
	#			- the average silhouette score of the cluster needs to be higher then the silhouette score of all the clusters
	#			  combined
	#			- the standard deviation of the clusters need to be lower than the standard deviation of all the clusters
	#			  combined
	#		- silhouette value for the dataset must be greater than 0.5
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
	# list[x][0] -> type: array; 1 dimensional array of cluster results by sample in the order of the sample row passed 
	#							as indicated by the sparse or dense array
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
	# list[x][0] -> type: array; 1 dimensional array of cluster results by sample in the order of the sample row passed 
	#							as indicated by the sparse or dense array
	# list[x][1] -> type: string; the cluster ID with the parameters
	# list[x][2] -> type: float; silhouette average value for the entire set of data
	# list[x][3] -> type: array; 1 dimensional array of silhouette values for each data sample
	# list[x][4] -> type: list; list of lists, the cluster and the average silhoutte value for each cluster, the orders is sorted 
	#					highest to lowest silhoutte value
	#					list[x][4][x][0] -> int; cluster label
	#					list[x][4][x][1] -> float; cluster silhoutte value
	# list[x][5] -> type: list; a list that contains the cluster label and the number of samples in each cluster
	#					list[x][5][x][0] -> int; cluster label
	#					list[x][5][x][1] -> int; number of samples in cluster list[x][5][x][0]
    ###############################################################################################
    ###############################################################################################	

	# time start
	time_start = time.perf_counter()

	# lists
	list_cluster_sihl_metrics = list()
	list_cluster_sihl_avg_values = list()
	list_positive_evals = list()
	list_id = list_cluster_results[0][1].split(sep = '|')

	# dictionaries
	dict_dist_posit = {'Aggl': 2, 'Dbs': 3}

	# get distance metric
	if list_id[0] == 'BatchKm' or list_id[0] == 'Spec':
		string_distance = 'euclidean'
	else:
		string_distance = list_id[dict_dist_posit[list_id[0]]]

	# loop through cluster results
	for cluster_result in list_cluster_results:
		# get number of clusters
		arrray_clusters_count = numpy.bincount(cluster_result[0])

		# check that there is more than one label in the cluster results
		int_non_zero_clust = 0
		for clust_count in arrray_clusters_count:
			if clust_count > 0:
				int_non_zero_clust += 1
	
		# number of potential clusters
		int_num_clusters = len(arrray_clusters_count)

		if int_num_clusters > 1 and int_non_zero_clust > 1:
			# calculate the average silhouette for the clusters
			# this gives a perspective into the desity and seperation
			# of the formed clusters
			silhouette_avg = silhouette_score(array_sparse_matrix, cluster_result[0], metric = string_distance)

			# compute the silhouette samples fore each cluster
			sample_silhouette_values = silhouette_samples(array_sparse_matrix, cluster_result[0], metric = string_distance)
			silhouette_std = statistics.stdev(sample_silhouette_values)

			# list, number of samples in the cluster
			list_count_cluster_samples = list()
			
			# get silhouette metrics for cluster
			for cluster in range(0, int_num_clusters):
				# get the silhouette values for only cluster (0 -> int_num_clusters - 1)
				cluster_silh_values = sample_silhouette_values[cluster_result[0] == cluster]

				# calculate the average and std deviation of each cluster
				if len(cluster_silh_values) > 1:
					cluster_silh_avg = statistics.mean(cluster_silh_values)
					cluster_silh_stdv = statistics.stdev(cluster_silh_values)
				else:
					cluster_silh_avg = -1
					cluster_silh_stdv = 1

				# the list of average sihlouette values by cluster
				list_cluster_sihl_avg_values.append([cluster, cluster_silh_avg])

				# count of samples in each cluster
				list_count_cluster_samples.append([cluster, len(cluster_silh_values)])

				# if the std deviation a cluster samples is less then the standard devation of all the clusters combined
				# and if the mean is greater than the mean of all the clusters combined
				# and the overall average is positive
				if cluster_silh_avg >= silhouette_avg and cluster_silh_stdv <= silhouette_std:
					list_cluster_sihl_metrics.append(cluster)

				# reset list
				cluster_silh_values = list()

			# if 1/2 of the clusters meet have a greater avarage and a lower standard deviation then add cluster to list
			#if len(list_cluster_sihl_metrics) >= int(int_num_clusters * 0.5) and silhouette_avg > 0.5:

			# sort the average silhoutte values of each cluster
			# sorting by the second element of the sublist
			list_cluster_sihl_avg_values = sorted(list_cluster_sihl_avg_values, key = lambda x: x[1])

			# add cluster to the return list
			list_temp = list()
			for k in cluster_result:
				list_temp.append(k)
			list_temp.append(silhouette_avg)
			list_temp.append(sample_silhouette_values)
			list_temp.append(list_cluster_sihl_avg_values)
			list_temp.append(list_count_cluster_samples)
			list_positive_evals.append(list_temp)

			# reset variables
			list_cluster_sihl_metrics = list()
			list_cluster_sihl_avg_values = list()
	
	# return positive cluster results
	time_total = time.perf_counter() - time_start
	print('%s clustering results evaluated positive for %s clustering process' %(len(list_positive_evals), list_id[0]))
	print('Evaluation time (HH:MM:SS): ', time.strftime('%H:%M:%S', time.gmtime(time_total)))
	return list_positive_evals

def SaveClustEval(m_list_cluster_alg_evaluations, m_sql_connection, m_string_sql_table_name, 
				  m_bool_truncate_table = True):
    ###############################################################################################
    ###############################################################################################
    #
    # this method will save the cluster information in the database to assist in the analysis and evaluation of each
	# cluster algorithm; 
    #
    # Requirements:
	# file SqlMethods
    #
    # Inputs:
    # list_cluster_evaluations
    # Type: list
    # Desc: this of the clusters that meet the evaluation criterea
	# list[x][0] -> type: array; 1 dimensional array of cluster results by sample in the order of the sample row passed 
	#							as indicated by the sparse or dense array
	# list[x][1] -> type: string; the cluster ID with the parameters
	# list[x][2] -> type: float; silhouette average value for the entire set of data
	# list[x][3] -> type: array; 1 dimensional array of silhouette values for each data sample
	# list[x][4] -> type: list; list of lists, the cluster and the average silhoutte value for each cluster, the orders is sorted 
	#					highest to lowest silhoutte value
	#					list[x][4][x][0] -> int; cluster label
	#					list[x][4][x][1] -> float; cluster silhoutte value
	# list[x][5] -> type: list; a list that contains the cluster label and the number of samples in each cluster
	#					list[x][5][x][0] -> int; cluster label
	#					list[x][5][x][1] -> int; number of samples in cluster list[x][5][x][0]
	#
    # m_sql_connection
    # Type: object, sql connection
    # Desc: the connection to the database
    #  
    # m_string_sql_table_name
    # Type: string
    # Desc: the name of the sql table to add the cluster evaluations to
    #    
	# m_bool_truncate_table
    # Type: boolean
    # Desc: flag whether to truncate destination table
    #   
    # Important Info:
	# for inserting data into a sql table using pymssql
	# only the %s and %d data types are supported for the execute() and executemany() methods
	# anything other than an integer (%d, signed integer) needs to be a %s, type checking is condcuted
	# internally
    #
    # Return:
    # None
	# Type: n/a
	# Desc: n/a
    ###############################################################################################
    ###############################################################################################	
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------#
	# variable / object declarations
	#------------------------------------------------------------------------------------------------------------------------------------------------------#

	# lists
	list_sql_table_columns = ['string_cluster_alg_id', 'float_avg_sihl_all_clusters', 'int_cluster_label', 'float_silhl_cluster', 
											   'float_sihl_sample', 'int_sample_count']
	list_sql_table_columns_data_type = [' varchar(100)', ' float', ' int', ' float', ' float', ' int']
	list_sql_insert_data_type = ['%s', '%s', '%d', '%s', '%s', '%d']

	# variables
	
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
	#
	# Start
	#
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#	

	#------------------------------------------------------------------------------------------------------------------------------------------------------#
	# destination table checks
	#------------------------------------------------------------------------------------------------------------------------------------------------------#

	# check if the table exists
	bool_sql_table_exists = SqlMethods.SqlTestTableExists(m_sql_connection, m_string_sql_table_name)

	# checking for consistancy of the table
	if bool_sql_table_exists == True:
		list_sql_dest_table_columns = SqlMethods.SqlGetTableColumns(m_sql_connection, m_string_sql_table_name)
		list_num_columns = SqlMethods.SqlGetNumTableColumns(m_sql_connection, m_string_sql_table_name)

		if list_sql_dest_table_columns[0] == True:
			bool_columns_good = SqlMethods.SqlCheckColumns(list_sql_dest_table_columns[1], list_sql_table_columns)
		else:
			bool_columns_good = False

		if list_num_columns[0] == True:
			if len(list_sql_table_columns) == list_num_columns[1] and bool_columns_good == True:
				bool_create_table = False
	else:
		# column list to create table
		list_create_columns = list()
		for int_index in range(0, len(list_sql_table_columns)):
			list_create_columns.append(list_sql_table_columns[int_index] + list_sql_table_columns_data_type[int_index])

		# create table
		list_bool_table_created = SqlMethods.SqlCreateTable(m_sql_connection, m_string_sql_table_name, list_create_columns,
												 False)

	# truncate table if flagged
	if m_bool_truncate_table == True:
		# trunacte table
		list_bool_trunc_dummy = SqlMethods.SqlTruncateTable(m_sql_connection, m_string_sql_table_name)

		# if an error delete the table and create a new one
		if list_bool_trunc_dummy[0] == False:
			list_bool_del_dummy = SqlMethods.SqlDeleteTable(m_sql_connection, m_string_sql_table_name)
			list_bool_create_dummy = SqlMethods.SqlCreateTable(m_sql_connection, m_string_sql_table_name, 
														list_create_columns, False)

	#------------------------------------------------------------------------------------------------------------------------------------------------------#
	# add cluster evaluations that passed the criterea to the destination table
	#------------------------------------------------------------------------------------------------------------------------------------------------------#

	# add values to the table
	# adds one cluster algorithm evaluation at a time
	for clust_alg_eval in m_list_cluster_alg_evaluations:
		# list to hold the inserts into the database
		list_eval_insert = list()

		# loop through each cluster in the algorithm
		for cluster_label in clust_alg_eval[4]:
			array_sihl_samples = clust_alg_eval[3][clust_alg_eval[0] == cluster_label[0]]

			# loop throgh each record of the cluster in the algorithm
			for int_index_01 in range(0, len(array_sihl_samples)):
				sample_sihl_value = array_sihl_samples[int_index_01]
				list_num_samples = [x[1] for x in clust_alg_eval[5] if x[0] == cluster_label[0]]

				# create insert list
				list_value = [clust_alg_eval[1]]
				list_value.append(float(clust_alg_eval[2]))
				list_value.append(int(cluster_label[0]))
				list_value.append(float(cluster_label[1])) 
				list_value.append(float(sample_sihl_value))
				list_value.append(int(list_num_samples[0]))

				# append insert list
				list_eval_insert.append(tuple(list_value))

		# insert into the database
		# inserts one algorithm evaluation at a time
		list_insert_result = SqlMethods.SqlInsertIntoTable(m_sql_connection[1], m_string_sql_table_name, 
													 list_sql_table_columns, list_sql_insert_data_type, list_eval_insert, 
													 True)
		
		if list_insert_result[0] == True:
			print('inserted algorithm %s' %list_eval_insert[0][0])
		else:
			print('there were problems inserting %s into the destination table' %list_eval_insert[0][0])

def VisualizeResults(list_cluster_evaluations, string_path = 'C:\\', bool_show = False):
    ###############################################################################################
    ###############################################################################################
    #
    # this method visualizes the silhouette values of each sample and the average silhouette value of each cluster
	# algorithm variation
    #
    # Requirements:
    # package numpy
	# package matplotlib.pyplot
	# package matplotlib.cm
    #
    # Inputs:
    # list_cluster_evaluations
    # Type: list
    # Desc: this of the clusters that meet the evaluation criterea
	# list[x][0] -> type: array; of cluster results by sample in the order of the sample row passed as indicated by the sparse
	#				or dense array
	# list[x][1] -> type: string; the cluster ID with the parameters
	# list[x][2] -> type: float; silhouette average value for the entire set of data
	# list[x][3] -> type: array; 1 dimensional array of silhouette values for each data sample
	# list[x][4] -> type: list; list of lists, the cluster and the average silhoutte value for each cluster, the orders is sorted 
	#					highest to lowest silhoutte value
	#					list[x][4][x][0] -> int; cluster label
	#					list[x][4][x][1] -> float; cluster silhoutte value
	# list[x][5] -> type: list; a list that contains the cluster label and the number of samples in each cluster
	#					list[x][5][x][0] -> int; cluster label
	#					list[x][5][x][1] -> int; number of samples in cluster list[x][5][0]
	#
    # string_path
    # Type: string; default = 'C:\\'
    # Desc: the path to store the images from the silhouette plots
	#
    # bool_show
    # Type: boolean; default = False
    # Desc: the flag to indicate and show or same the file
	#
    # Important Info:
    # None
    #
    # Return:
    # None
    # Type: None
    # Desc: None
    ###############################################################################################
    ###############################################################################################	

	# lists
	# calculate the x-ticks list for each plot
	list_x_ticks = [x / 10 for x in range(-10, 11, 2)]  

	# loop through the cluster algorithms
	for cluster_eval in list_cluster_evaluations:
		# get values
		cluster_labels = cluster_eval[0]
		cluster_id = cluster_eval[1]
		silhouette_avg = cluster_eval[2]
		sample_silhouette_values = cluster_eval[3]
		list_cluster_avg_sihl_values = cluster_eval[4]
		int_num_clusters = len(numpy.bincount(cluster_eval[0]))
		int_sample_total = len(cluster_labels)

		# create pyplot with one sublplot     
		fig_01, axes = pyplot.subplots(1, 1) # set by default to one figure, can have multiple plots in one figure
		# figure size [4, 8]
		#axes = fig_01.gca()
		fig_01.set_size_inches(4., 8.)

		# set the limit of the x-axis
		# the sihlouette measurements are from -1, 1
		axes.set_xlim(left = min(sample_silhouette_values), right = 1, emit = True)

		# set the limits of the y-axis
		# (int_num_clusters + 1) * 10 is for inserting a blank space betwen silhouette plots
		# to clearly demark them
		axes.set_ylim(0, int_sample_total + (int_num_clusters + 1) * 10)

		# show the number of clusters and the overall sihlouette score
		print('For %s clusters the average silhouette score is %s.' %(cluster_id, silhouette_avg))
		print('%s created %s clusters.' %(cluster_id, int_num_clusters))

		# display every cluster on the figure
		y_lower = 10
		float_cluster_color_counter = 0.
		for cluster_sorted in list_cluster_avg_sihl_values:
			# compile the silhouette scores for samples beloning to
			# cluster i, and sort them
			ith_cluster_silh_values = sample_silhouette_values[cluster_labels == cluster_sorted[0]]
			ith_cluster_silh_values.sort()

			# get the size of the samples in a cluster and calculate the y_upper value
			size_cluster_i = ith_cluster_silh_values.shape[0]
			y_upper = y_lower + size_cluster_i

			# set the color for the cluster and plot
			color = cm.spectral(float_cluster_color_counter / float(int_num_clusters))
			pyplot.fill_betweenx(numpy.arange(y_lower, y_upper), 0,
								ith_cluster_silh_values, facecolor = color,
								edgecolor = color, alpha = 0.7)

			# label the silhouette plots with their culster numbers at the middle
			#pyplot.text(-0.15, y_lower + 0.5 * size_cluster_i, str(cluster_sorted[0]) + ', ' + str(cluster_sorted[1]))
			pyplot.text(-0.15, y_lower + 0.5 * size_cluster_i, str(cluster_sorted[0]))

			# compute the new y_lower
			y_lower = y_upper + 10

			# increment cluster color counter
			float_cluster_color_counter += 1.

			# delete objects for memory manageemnt
			del ith_cluster_silh_values, size_cluster_i

		# set labels and title
		fig_01.suptitle('Silhouette plot by cluster')
		axes.set_title(cluster_id)
		axes.set_xlabel('The silhouette coefficient values')
		axes.set_ylabel('Cluster label')

		# plot the average silhouette score
		axes.axvline(x = silhouette_avg, color = 'red', linestyle = '--')

		# set the x and y ticks for each plot
		axes.set_yticks([]) # clears all the ticks
		axes.set_xticks(list_x_ticks)

		# set the limit of the x-axis
		# the sihlouette measurements are freom -1, 1
		axes.set_xlim(left = min(sample_silhouette_values), right = 1)

		# show the images or save them based on the flag bool_show
		if bool_show == True:
			# show the plot
			pyplot.show(block = False)
		else:
			# set file name
			list_clust_id = cluster_id.split('|')
			string_file = ''.join(word + '_' for word in list_clust_id)
			string_file = string_file[:-1]
			string_file = string_file + '.png'

			# save plot
			pyplot.savefig(string_path + string_file)