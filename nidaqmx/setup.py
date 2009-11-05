from os.path import join

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('nidaqmx',parent_package,top_path)
    config.make_svn_version_py()
    return config
