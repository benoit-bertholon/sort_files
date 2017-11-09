
import argparse
import os
import sys
import hashlib
from database import *
    
def compute_size()
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
    print( "DB file: ", dbfile)
    sqlite_dbfile = 'sqlite:///'+dbfile
    print( "db:", sqlite_dbfile)
    dbsession = get_dbsession(sqlite_dbfile)

    

    print ("compute size of the ")
    files = get_all_files(dbsession)
    i = 0
    num_missing = 0
    size = 0
    len_file_names = len(files)
    for f in files:
        i+=1
        sys.stdout.write("\r%.2f  " % (i * 100. /  len_file_names))
        sys.stdout.flush()

        if not os.path.isfile(f.path):
            num_missing += 1
            if args.verbose > 0:
                print ("missing:", f.path)
        else:
            size += os.path.getsize(f.path)
    print("missing: ", num_missing)
    print("num files:" , i)
    print("size:", size,"B",  "%.2f MB", size/(1024.**2))
    

if __name__ == "__main__":
    compute_size()
