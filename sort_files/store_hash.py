
import argparse
import os
import sys
import hashlib
from sort_files.database import *

def store_hash():
    

    parser = argparse.ArgumentParser(description='Add missing files to db')
    parser.add_argument('folder',  
                        help='folder to check')
    parser.add_argument("-v", '--verbose', dest='verbose', default=0, action="count",
                        help='verbosity level')
    parser.add_argument('--sqlitedb', dest='sqlitedb', default=None,
                        help='db folder (absolute), by defautl is [folder].files.db')

    args = parser.parse_args()
    print(args.verbose)
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
        if args.verbose != 0:
            sys.stdout.write("\r%.2f %%  %d/%d  %s " % (i * 100. /  len_file_names, i , len_file_names, f.encode("ascii", 'ignore')))
            sys.stdout.flush()
        else:
            sys.stdout.write("\r%.2f %%   " % (i * 100. /  len_file_names))
            sys.stdout.flush()
        try:
            inserted += insert_if_not_present(dbsession, f)
        except UnicodeEncodeError as unicode_error:
            print(unicode_error, f.encode("ascii", 'ignore'))
        except ExceptFile as file_error:
            print(file_error, f.encode("ascii", 'ignore'))
    print ("inserted", inserted , "files")



if __name__ == "__main__":
    store_hash()

