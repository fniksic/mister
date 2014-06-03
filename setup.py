from distutils.core import setup

setup(
    name = 'mister',
    version = '0.1',
    description = 'Parser library for the MIST specification format.',
    author = 'Filip Niksic',
    author_email = 'fniksic@mpi-sws.org',
    maintainer = 'Filip Niksic',
    maintainer_email = 'fniksic@mpi-sws.org',
    url = 'http://plv.mpi-sws.org/',
    package_dir = {'mister': 'src/mister'},
    packages = ['mister'],
    requires = ['ply']
)