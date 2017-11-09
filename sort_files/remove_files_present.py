
import argparse
import os
import sys
import hashlib
from database import *

def remove_files_present():


    parser = argparse.ArgumentParser(description='remove file already present in db')
    parser.add_argument('folder',   
                        help='folder to check and remove')
    parser.add_argument('sqlitedb', 
                        help='db folder (absolute), by defautl is [folder].files.db')
    parser.add_argument('--dry-run', dest='dryrun', default=False, action="store_true",
                        help='do not remove files only print them')
    parser.add_argument('--with-name', dest='withname', default=True, action="store_true",
                        help='comparte the name as well')


    args = parser.parse_args()
    folder = os.path.abspath(args.folder)
    if not  os.path.isdir(folder):
        print ("the folder argument should be an existing folder")
        sys.exit(1)

    print ("connect db")
    sqlite_dbfile = 'sqlite:///'+args.sqlitedb
    dbsession = get_dbsession(sqlite_dbfile)

    print ("Getting file list")
    file_names = get_files(folder)
    print ("found " , len(file_names) , " files")

    print ("checking there presence in db")
    count = 0
    i = 0
    size = 0
    len_file_names = len(file_names)
    for f in file_names:
        i+=1
        sys.stdout.write("\r%.2f   " % (i * 100. /  len_file_names))
        sys.stdout.flush()
        files = get_files_with_same_hash_from_abs_path(dbsession, f)
        if len(files) > 0:
            if not f.split(os.sep)[-1] in [fi.name for fi in files]:
                print ("WARNING: name different", f.split(os.sep)[-1], files[0].name)
                if args.withname:
                    # ignore file if name is not the same 
                    continue
            file_inode = os.lstat(f).st_ino
            file_inodes = map(lambda x:os.lstat(x.path).st_ino, files)    
            assert file_inode not in file_inodes
            hash_file_to_remove = compute_sha256(f)
            hash_file_existing = compute_sha256(files[0].path)
            assert hash_file_to_remove == hash_file_existing
            print (f, ":" , hash_file_to_remove    )
            print (files[0].path, ":" , hash_file_existing)
            print ("present "+ f)
            count += 1
            size += os.stat(f).st_size
            if not args.dryrun:
                print ("remove", f)
                os.remove(f)
            else:
                print ("dry run not remove", f)
    print ("number of present:" ,count)
    print ("size of present: %.2f Mib" %( size/1024./1024))




if __name__ == "__main__":

    remove_files_present()


