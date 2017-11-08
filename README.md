
Install
==========

clone the repository.

install python3 python3-sqlalchemy

Idea
=====

- Store the hashes of file from a directory in an sqlite database to find duplicate files.
- This project uses small simple scripts.
- Each script is stand alone.

Usage
=======

**store_hash**
-----------

The first script to run is the **store_hash.py** which create the database and scan a folder.
During the scan, the script computes the sha256 of all the files and store the path, the name and the hash in the database.


**remove_files_present.py**
--------------------

This script removes the files in a directory given in parameter.
For that, the script compare the hash and the name of each files in the directory with the values in the sqlite database.

**check_integrity.py**
------------------

This script computes the hash values of the files in the db to ensure that they have not changed.

**compute_size.py**
-----------

This script computes the sum of the size of the files in the db


**remove_from_db.py**
-------------

This script removes the files in the db if they are not present in the folder anymore.




