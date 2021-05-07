#!/usr/bin/python3
import os
import pymysql
import sys
from tabulate import tabulate

def startup():
	"""Connect to MySQL Database """
	db = pymysql.connect(host = 'localhost', user = 'testuser', password = 'test123', database = 'DB_OS_ML')
	print("connected")
	cursor = db.cursor()
	return cursor

cursor = startup()

def show_Tables():
	sql = "SHOW TABLES"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		# print(tabulate(results, headers='firstrow', tablefmt='fancy_grid'))
	except:
		print ("Error: unable to fetch data")
	return results

def show_col(x):
	sql = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'DB_OS_ML\' AND TABLE_NAME = \''+ x + '\'';
	try:
	    cursor.execute(sql)
	    result = cursor.fetchall()
	    # print(tabulate(result, headers='firstrow', tablefmt='fancy_grid'))
	except:
	    print('error: unable to perform request')
	return result

class get_tables:
	def __init__(self, name):
		self.name = name
		self.table_names = []
		self.tables = show_Tables()
	def add_tables(self, table_name):
	    self.table_names.append(table_name)
	def auto_add(self):
		a = len(self.tables)
		for i in range(a):
			self.table_names.append(self.tables[i][0])

class table_cols:
	def __init__(self,name):
		self.name = name
		self.cols = []
	def add_cols(self, col_name):
		self.cols.append(col_name)

class db_table:
	def __init__(self,name):
		self.name = name
		self.cols = []
	def fill_cols(self):
		a = show_col(self.name)
		for i in range(len(a)):
			self.cols.append(a[i][0])
	def select(self,mod,w_clause):
		while 1:
			if isinstance(mod,list):
				result = []
				for i in range(len(mod)):
					if mod[i] in self.cols:
						# print(mod[i])
						temp_result = []
						sql = 'SELECT ' + mod[i] + ' FROM ' + self.name;
						try:
							cursor.execute(sql)
							results = cursor.fetchall()
						except:
							print('Error unable to execute request: ')
							print(sql)
					for n in range(len(results)):
							temp_result.append(results[n][0])
							result.append(results[n][0])
							col_length = len(temp_result)
					# print(col_length)
					# result.append(mod[i])

				break
			else:
					mod = mod.split(', ')
		return mod,self.remove_S(result,col_length,mod)

	def remove_S(self,result,col_length,mod):
		l_result = len(result)
		for j in range(len(mod)):
			mod[j] = []
			for i in range(j*col_length, (j+1)*col_length):
				mod[j].append(result[i])
		return mod

a = get_tables('db_os_tables')

a.auto_add()
loVars = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10']
loTabs = a.table_names
Table_LIST='Tables: ' + str(loTabs).rjust(50)

print('\b' + Table_LIST + '\n\n', flush = True)
for i in range(len(a.table_names)):
	loVars[i] = db_table(a.table_names[i])
	loVars[i].fill_cols()
	loTabs[i] = db_table(a.table_names[i])
	loTabs[i].fill_cols()

print(loTabs[0].cols)
query2 = loTabs[1].select(loTabs[1].cols,'none')
