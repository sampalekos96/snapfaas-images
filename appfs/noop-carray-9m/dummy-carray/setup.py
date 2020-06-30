from distutils.core import setup, Extension

module1 = Extension('dummy_array', sources = ['dummy.c'])

setup (name = 'dummy_array', version = '1.0',
        description = 'This package allocates and frees an dummy array', 
        ext_modules = [module1])
