
import argparse
import os
import sys
import hashlib
from database import *



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Add missing files to db')
	parser.add_argument('folder',  
		                help='folder to check')
	parser.add_argument('--sqlitedb', dest='sqlitedb', default=None,
		                help='db folder (absolute), by defautl is [folder].files.db')

	args = parser.parse_args()
	folder = os.path.abspath(args.folder)
	if not  os.path.isdir(folder):
		print ("the folder argument should be an existing folder")
		sys.exit(1)
	dbfile = args.sqlitedb
	if dbfile == None:
		dbfile = folder.rstrip(os.sep)
		f = dbfile.split(os.sep)[-1]
		dbfile = os.sep.join(dbfile.split(os.sep)[0:-1])
		dbfile += os.sep + f  + ".files.db"
	print ("DB file: ", dbfile)

	print ("create db")
	sqlite_dbfile = 'sqlite:///'+dbfile
	print ("db:", sqlite_dbfile)
	dbsession = get_dbsession(sqlite_dbfile)

	print( "Getting file list")
	file_names = get_files(folder)
	print ("found " , len(file_names) , " files")

	

	print ("adding them to the db")
	inserted = 0
	len_file_names = len(file_names)
	i = 0
	for f in file_names:
		i+=1
		sys.stdout.write("\r%.2f %%   " % (i * 100. /  len_file_names))
		sys.stdout.flush()
		inserted += insert_if_not_present(dbsession, f)
	print ("inserted", inserted , "files")





