import os
from distutils.core import setup
from Cython.Build import cythonize

# Cython's version of Extension class for extra parameters to work:
from Cython.Distutils import build_ext, Extension


#logging.basicConfig()
#log = logging.getLogger(__file__)

#setup(ext_modules=cythonize(ext))
#setup_args = {'name': 'module', 'license': 'MIT', 'author': 'Mars',
#    'cmdclass': {'build_ext': build_ext}
    #'packages': ['module'],
#    }

# Relative not absolute path, OFC.
if "SETUP_PATH" in os.environ:
    raw_path = os.environ['SETUP_PATH']
else:
    raw_path = 'src/'

# @TODO: Iterate over src directory using utils function, obvi.
ext1 = Extension(name="scheduler", sources=['scheduler.py'])
ext2 = Extension(name="kronos", sources=['kronos.py'])
sources=[ext1, ext2]

# ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)

# ext_modules=cythonize(ext, language_level="3"})
ext_modules=cythonize(sources,
    compiler_directives={'language_level' : "3"},
    build_dir='../../lib/c',
    annotate=False)

#for e in ext_modules:
#    e.cython_directives = {'language_level': "3"}

setup(
    #name = 'Zorobot',
    #cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
