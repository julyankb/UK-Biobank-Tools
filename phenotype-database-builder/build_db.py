from __future__ import division
import sqlite3
import sys
import os
import gzip
import subprocess
import time
import scrape_ukb

start_time = time.time()

# USER INPUTS
database_dir = 'target directory'
database_name = 'UKBB.db'
data_file = 'ukb_phenofile.tab' # Tab-separated UKB phenotype file.

# GENERATE LIST OF COLUMNS
proc = subprocess.Popen(['head', '-1', data_file], stdout=subprocess.PIPE)
output = proc.stdout.read()
columns = [c for c in output.split('\t') if c[0] == 'f' and '\n' not in c]

# CREATE DATABASE IF NOT EXISTS, INITIALIZE CURSOR
conn = sqlite3.connect(database_dir + database_name)
c = conn.cursor()

# DEFINE FUNCTIONS
def create_tables():
        command = 'CREATE TABLE IF NOT EXISTS participants (rowid integer primary key autoincrement, eid, df, instnum, itemnum, value)'
        c.execute(command)
        command = 'CREATE TABLE IF NOT EXISTS dfdesc (df integer primary key, desc, category, type)'
        c.execute(command)
	
def insert_participant_data(line):
	data = line.split('\t')
	eid = int(data[0])
	for i in range(1, len(columns)):
		column = columns[i].split('.') # of the form [f, 21, 0, 0]
		print column
		df, instnum, itemnum, value = int(column[1]), int(column[2]), int(column[3]), data[i]
		if value == 'NA': # 1 Byte to store NULL, 2 Bytes to store NA.
			value = None
		c.execute("INSERT INTO participants VALUES (?,?,?,?,?,?)", (None, eid, df, instnum, itemnum, value))
	conn.commit()
	
def insert_dfdesc_data(line):
	data = line.split('\t')
	df, desc, category, df_type = int(data[0]), data[1], data[2], data[3]
	c.execute("INSERT INTO dfdesc VALUES (?,?,?,?)", (df, desc, category, df_type))
	conn.commit()	

def read_from_db(query):
	c.execute(query)
	for row in c.fetchall():
		 print row
# ---------------------------------------------------------------------------------------------------
# ALWAYS RUN
create_tables()
# ---------------------------------------------------------------------------------------------------
# INSERT INTO patients TABLE
run_below = 0
if run_below:
	with open(data_file) as infile:
		next(infile) #skip header
		for counter, line in enumerate(infile):
			insert_participant_data(line)
			print "Inserted participant %s \t f.eid = %s "%(counter, line.split('\t')[0])

# CREATE participants.df INDEX
run_below = 0
if run_below:
	print "Creating index on participants.df..."
        c.execute("CREATE INDEX IF NOT EXISTS df_index ON participants (df)")
	print "Process completed."

# CREATE INDEX ON participants.eid
run_below = 0
if run_below:
	print "Creating index on participants.eid..."
	c.execute("CREATE INDEX IF NOT EXISTS eid_index ON participants (eid)")
	print "Process completed."
# ---------------------------------------------------------------------------------------------------
# INSERT INTO dfdesc TABLE 
run_below = 0
if run_below:
	df_descriptions = scrape.df_descriptions
	for line in df_descriptions:
		#print line
		insert_dfdesc_data(line)
		print "Inserted df %s"%line.split('\t')[0]	
# ---------------------------------------------------------------------------------------------------
# PRINT TIME ELAPSED
print 'Time elapsed:', time.time() - start_time
