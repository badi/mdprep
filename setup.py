"""\
mdprep: a python library for preparing molecular dynamics simulations.
"""

DOCLINES = __doc__.split('\n')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os
import subprocess
import sys



################################################################################
setup_kws = dict()

dependencies = ['pyyaml', 'prody', 'mdtraj']
if 'setuptools' in sys.modules:
    setup_kws['install_requires'] = dependencies
else:
    setup_kws['requires'] = dependencies


################################################################################
VERSION = '0.1.0'
ISRELEASED = False
__version__ = VERSION
################################################################################


################################################################################
# Writing version control information to the module
################################################################################
# adapted from MDTraj setup.py

def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = 'Unknown'

    return GIT_REVISION


def write_version_py(filename='mdprep/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM MDPREP SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = 'Unknown'

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


def find_packages():
    """Find all python packages.
    Adapted from IPython's setupbase.py. Copyright IPython
    contributors, licensed under the BSD license.
    """
    packages = []
    for dir,subdirs,files in os.walk('mdprep'):
        package = dir.replace(os.path.sep, '.')
        if '__init__.py' not in files:
            # not a package
            continue
        packages.append(package)
    return packages

################################################################################
write_version_py()
setup(name='mdprep',
      author="Badi' Abdul-Wahid",
      author_email='abdulwahidc@gmail.com',
      description=DOCLINES[0],
      long_description="\n".join(DOCLINES),
      version=__version__,
      license='LGPLv2.1+',
      url='http://github.com/badi/mdprep',
      platforms=['Linux', 'Mac OS-X', 'Unix', 'Windows'],
      packages=find_packages(),
      **setup_kws)
