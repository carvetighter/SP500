# SP500 Moving Average (SMA) Analysis

This analysis pulls data for the SP500 (since inception) and conducts a moving average analysis to indicate when to get in and out of the market.  The goal of this analysis is to "get out of the way" of the long downward trends and stay in as long as the market is going up.

# Requirements
- SQL Server Database locally (install prior to running script)
- internet connection (to get the SP500)
- Anaconda Python distribuiton

# Running the python script
1. download / pull the repo
2. create sp_500_init.py file
3. create the environment from the environment file
4. activate the environment
5. run the script

## Create the Environment
```conda env create -f env_sp500.yml```

## Activate Environment
Windows -> ```activate sp_500```\
Linux -> ```conda activate sP_500```

## Run Script
```python sp_500_init.py```

## Example sp_500_init.py file
Below is an example of the init file you will need to create.  This file will define the user name and password for the SQL Server locally.  Replace ```<sql_server_user_name>``` and ```<password>``` with the user name and password for the SQL Server.

```
'''
This is the initial file which is not tracked in git.
Calls the main method in sp_500_main.py
'''

from sp_500_class import main_class

if __name__ == '__main__':
    list_sql_up = [r'<sql_server_user_name>', r'<password>']
    main_class(list_sql_up)
```