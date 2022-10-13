from importlib.metadata import entry_points
import os
from setuptools import setup

ver_file = os.path.join('hpc_benchmark', 'info.py')
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
            install_requires=REQUIREMENTS,
            python_requires=PYTHON_REQUIRES)

if __name__ == '__main__':
    setup(**opts,
          entry_points = {
              'console_scripts': ['hpc_benchmark=hpc_benchmark.command_line:main']
          }
    )