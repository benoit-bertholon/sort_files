import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

install_requires = [
    'sqlalchemy',
]

setup_requires = []

setup(name='sort_files',
      version='0.1',
      description='set of scripts to sort and delete duplicates using sqlite DB',
      long_description=README + '\n\n',
      classifiers=[
          "Programming Language :: Python"],
      author='Benoit Bertholon',
      author_email='benoit@bertholon.info',
      url='https://benoit.bertholon.info',
      keywords='sort hash files duplicates database sqlite',
      packages=find_packages(),
      package_data={},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      setup_requires=setup_requires,
      entry_points={
          'console_scripts': ['store_hash = sort_files.store_hash:store_hash',
                              'remove_files_present = sort_files.remove_files_present:remove_files_present',
                              'remove_from_db = sort_files.remove_from_db:remove_from_db',
                              'check_integrity = sort_files.check_integrity:check_integrity',
                              'compute_size = sort_files.compute_size:compute_size',
                              ]
      }
      )

