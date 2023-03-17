from importlib.metadata import entry_points
import os
from setuptools import setup, find_packages

ver_file = os.path.join('cli', 'info.py')
os.path.realpath
with open(ver_file) as f:
    exec(f.read())
    
opts = dict(name=NAME,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            classifiers=CLASSIFIERS,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            platforms=PLATFORMS,
            version=VERSION,
            packages=find_packages(),
            install_requires=REQUIREMENTS,
            python_requires=PYTHON_REQUIRES)

if __name__ == '__main__':
    setup(entry_points = {
              'console_scripts': [
                  'hpc_benchmark = cli.main:main',
                  ]
          },
          **opts
    )