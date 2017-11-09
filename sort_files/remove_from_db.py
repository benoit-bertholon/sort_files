
import argparse
import os
import sys
import hashlib
from database import *

def remove_from_db():
    

    parser = argparse.ArgumentParser(description='Check files entries in the db')
    parser.add_argument('--sqlitedb', dest='sqlitedb', default=None,
                        help='db file')
    parser.add_argument('--no-warning', dest='warning', default=True, action="store_false",
                        help='Do not print warning when file is not present and hash does not exist in the db')
    parser.add_argument('--remove', dest='remove', default=False, action="store_true",
                        help='remove the entries in the db')
    parser.add_argument('--ignore-name', dest='ignore_name', default=False, action="store_true",
                        help='only base the comparison on the hash')
    parser.add_argument("-v", "--verbose", dest='verbose', action="count", default=0,
                    help="increase output verbosity")
    args = parser.parse_args()
    dbfile = args.sqlitedb
    if dbfile == None:
        args.help()
        sys.exit(1)
    print "DB file: ", dbfile

    sqlite_dbfile = 'sqlite:///'+dbfile
    print "db:", sqlite_dbfile
    dbsession = get_dbsession(sqlite_dbfile)

    

    print ("removing  to the db")
    files = get_all_files(dbsession)
    i = 0
    len_file_names = len(files)
    for f in files:
        i+=1
        sys.stdout.write("\r%.2f   " % (i * 100. /  len_file_names))
        sys.stdout.flush()

        if not os.path.isfile(f.path):
            if args.verbose > 0:
                print (f.path, "not an existing file")
            same_files = get_files_from_hash(dbsession, f.hash)
            ihavethisfile = False
            for f2 in same_files:
                if os.path.isfile(f2.path) :
                    hash = compute_sha256(f2.path)
                    if f2.hash == hash:
                        ihavethisfile = True
                        if args.verbose > 1:
                            print "it is here" , f2.path
                        break
            if not ihavethisfile:
                print(f.path, "with hash",f.hash,"not present in db elsewhere")
            if args.remove:
                print("remove file entry", f.path)
                dbsession.delete(f)
                dbsession.commit()


if __name__ == "__main__":
    remove_from_db()
