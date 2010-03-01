#!/usr/bin/env python
import os

NAME = 'PyLibNIDAQmx'
AUTHOR = 'Pearu Peterson'
AUTHOR_EMAIL = 'pearu.peterson@gmail.com'
LICENSE = 'BSD'
URL = 'http://pylibnidaqmx.googlecode.com'
DOWNLOAD_URL = 'http://code.google.com/p/pylibnidaqmx/downloads/'
DESCRIPTION = 'PyLibNIDAQmx: a Python wrapper to libnidaqmx library'
LONG_DESCRIPTION = '''\
PyLibNIDAQmx? provides a package nidaqmx that wraps the libnidaqmx library to Python using ctypes.
'''
CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
License :: OSI Approved
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Software Development
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""
PLATFORMS = ['Linux']
MAJOR               = 0
MINOR               = 2
MICRO               = 0
ISRELEASED          = False
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)



version_file = 'nidaqmx/version.py'
def write_version_py(filename=version_file):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
short_version='%(version)s'
version='%(version)s'
release=%(isrelease)s

if not release:
    version += '.dev'
    import os
    svn_version_file = os.path.join(os.path.dirname(__file__),
                                   '__svn_version__.py')
    svn_entries_file = os.path.join(os.path.dirname(__file__),'.svn',
                                   'entries')
    if os.path.isfile(svn_version_file):
        import imp
        svn = imp.load_module('nidaqmx.__svn_version__',
                              open(svn_version_file),
                              svn_version_file,
                              ('.py','U',1))
        version += svn.version
    elif os.path.isfile(svn_entries_file):
        import subprocess
        try:
            svn_version = subprocess.Popen(["svnversion", os.path.dirname (__file__)], stdout=subprocess.PIPE).communicate()[0]
        except:
            pass
        else:
            version += svn_version.strip()

"""
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION, 'isrelease': str(ISRELEASED)})
    finally:
        a.close()

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None,parent_package,top_path)
    config.add_subpackage('nidaqmx')
    config.get_version('nidaqmx/version.py')
    return config

from distutils.core import Extension

if __name__=='__main__':
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')
    if os.path.exists(version_file): os.remove(version_file)
    write_version_py()

    from numpy.distutils.core import setup

    setup(
        name = NAME,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        download_url = DOWNLOAD_URL,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        classifiers = filter(None, CLASSIFIERS.split('\n')),
        platforms = PLATFORMS,
        configuration = configuration)
