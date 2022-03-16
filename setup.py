"""
The setup file. To install as a developer (only do this in a venv):

python setup.py develop

Otherwise, just:

python setup.py install
"""

from setuptools import setup

setup(name='local_stats',
      version='0.0.1',
      license='Closed source idk',
      description='A python package for using local statistics to cluster " + \
          "significant signal in scientific images.',
      author='Richard Brearton',
      author_email='richardbrearton@gmail.com',
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: Implementation :: CPython',
      ]
      )
