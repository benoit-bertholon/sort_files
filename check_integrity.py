
import argparse
import os
import sys
import hashlib
from database import *
	

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='compare hash of the file and in the db')
	parser.add_argument('--sqlitedb', dest='sqlitedb', default=None,
		                help='db folder (absolute), by defautl is [folder].files.db')
	parser.add_argument("-v", "--verbose", dest='verbose', action="count", default=0,
                    help="increase output verbosity")
	args = parser.parse_args()
	args = parser.parse_args()
	dbfile = args.sqlitedb
	if dbfile == None:
		args.help()
		sys.exit(1)
	print "DB file: ", dbfile
	sqlite_dbfile = 'sqlite:///'+dbfile
	print "db:", sqlite_dbfile
	dbsession = get_dbsession(sqlite_dbfile)

	

	print "check files integrity"
	files = get_all_files(dbsession)
	i = 0
	num_bad = 0
	num_good = 0
	num_missing = 0
	len_file_names = len(files)
	for f in files:
		i+=1
		sys.stdout.write("\r%.2f   \t % 20s \t % 20s  \t % 20s " % (i * 100. /  len_file_names, "good:%d" % num_good, "bad:%d" % num_bad, "missing:%d"%num_missing))
		sys.stdout.flush()

	 	if not os.path.isfile(f.path):
			num_missing += 1
			if args.verbose > 0:
				print "missing:", f.path
		else:
			hash = compute_sha256(f.path)
			if hash == f.hash:
				num_good += 1
			else:
				num_bad += 1
				if args.verbose > 0:
					print "bad hash:", f.path

