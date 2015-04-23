from distutils.core import setup

setup(
    name='murray_desai_platereader',
    version='0.1',
    packages=[''],
    url='https://github.com/btweinstein/murray_desai_platereader',
    license='',
    author='Bryan Weinstein',
    author_email='bweinstein@seas.harvard.edu',
    description='Used by the murray and desai labs at Harvard to analyze plate reader data',
    install_requires = ['numpy', 'pandas', 'matplotlib', 'seaborn',
                        'skimage']
)
