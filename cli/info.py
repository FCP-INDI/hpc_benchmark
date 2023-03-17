"""This file contains defines parameters for CPAC that we use to fill
settings in setup.py"""

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 1
_version_minor = 0
_version_micro = 0
_version_extra = ''

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 4 - Beta",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

description = 'High Performance Computing Benchmark'

long_description = """
==========================================
High Performance Computing (HPC) Benchmark
==========================================

Open source package that allows user to monitor command line runs. 
Metrics monitored include log time, CPU percentage, memory usage,
and processor for each run. Metrics are output into CSV file and can 
be plotted.
This was designed to understand the metrics of a run before allocating nodes
and memory onto a high performance computing cluster.

Documentation
-------------
User documentation can be found here: https://github.com/FCP-INDI/hpc_benchmark
"""

NAME = 'hpc_benchmark'
MAINTAINER = "C-PAC developers"
MAINTAINER_EMAIL = "CNL@childmind.org"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/FCP-INDI/hpc_benchmark"
DOWNLOAD_URL = "https://github.com/FCP-INDI/hpc_benchmark"
LICENSE = "LGPL-3.0-or-later"
AUTHOR = "Amy Gutierrez"
AUTHOR_EMAIL = "amy.gutierrez@childmind.org"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
ISRELEASE = _version_extra == ''
VERSION = __version__
PYTHON_REQUIRES = ">= 3.5"
REQUIREMENTS = [
    "packaging>=21.3",
    "numpy>=1.16.4",
    "pandas>=0.23.4",
    "plotly>=3.5.0",
    "psutil>=5.4.6",
]