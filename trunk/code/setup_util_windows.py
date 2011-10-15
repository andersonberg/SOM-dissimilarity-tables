from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("config", ["config.pyx"], extra_compile_args=["-IC:\\Python27\\Lib\\site-packages\\numpy\\core\\include"])],
)

