
import argparse
import os
import sys
import hashlib
from sort_files.database import *

def store_hash():
    

    parser = argparse.ArgumentParser(description='print file info from db')
    parser.add_argument("-v", '--verbose', dest='verbose', default=0, action="count",
                        help='verbosity level')
    parser.add_argument('--sqlitedb', dest='sqlitedb', default=None,
                        help='db folder (absolute), by defautl is [folder].files.db')

    args = parser.parse_args()
    print(args.verbose)
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

    files = get_all_files(dbsession)
    size = 0
    for f in files:
        print(f.path, f.hash)
        size += os.stat(f.path).st_size
    print("number of files: %d"%len(files))
    print("size: %f Mo" % (size/1024**2))
    


if __name__ == "__main__":
    store_hash()

