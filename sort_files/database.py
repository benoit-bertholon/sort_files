from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
import hashlib

Base = declarative_base()

def get_files(folder):
	list_files = []
	if os.path.isfile(folder) :
		list_files = [folder]
	if os.path.isdir(folder) and not os.path.islink(folder):
		list_files = sum([get_files(folder+os.sep+f) for f in os.listdir(folder)],[])
	return list_files

	

class File(Base):
    __tablename__ = 'files'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    file_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    path = Column(Text, nullable=False,index=True, unique=True)
    hash = Column(String(128), nullable=False,index=True)

def get_dbsession(sqlite_dbfile):
	print (sqlite_dbfile)
	engine = create_engine(sqlite_dbfile)
	# Bind the engine to the metadata of the Base class so that the
	# declaratives can be accessed through a DBSession instance
	Base.metadata.bind = engine
	Base.metadata.create_all(engine)
	 
	DBSession = sessionmaker(bind=engine)
	return DBSession()
Meg = 1024*1024*1024 

def compute_sha256(file_abs_path):
	m = hashlib.sha256()
	if os.path.islink(file_abs_path):
		value = bytes(os.readlink(file_abs_path), "utf-8")
		m.update(value)
	else:        
		with open(file_abs_path,'rb') as fichier:
			while True:
				data = fichier.read(Meg)
				if not data:
					break
				m.update(data)
	hash_ = m.hexdigest()
	return hash_

def get_files_with_same_hash_from_abs_path(dbsession, file_abs_path):
	hash = compute_sha256(file_abs_path)
	res = dbsession.query(File).filter(File.hash == hash).all()
	return res

def get_files_from_hash(dbsession, hashvalue):
	res = dbsession.query(File).filter(File.hash == hashvalue).all()
	return res

def get_all_files(dbsession):
	res = dbsession.query(File).all()
	return res

def  insert_if_not_present(dbsession, file_abs_path):
	if not os.path.isfile(file_abs_path) :
		raise Exception ("Expecting file")
	res = dbsession.query(File).filter(File.path == file_abs_path).all()
	if len(res) == 0:
		name = file_abs_path.split(os.sep)[-1]
		path = file_abs_path
		hash = compute_sha256(file_abs_path)
		new_file = File(name=name, path=path, hash=hash)
		dbsession.add(new_file)
		dbsession.commit()
		return 1
	return 0
