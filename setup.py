from setuptools import setup

setup(
    name='nangis',
    version='0.0.1',
    packages=['nangis', 'nangis.dk', 'nangis.dk.db', 'nangis.dk.styles', 'nangis.dk.basemap', 'nangis.dk.factories',
              'nangis.demo', 'nangis.demo.data'],
    url='',
    license='MIT License',
    author='Marek Ostrowski',
    author_email='marek@hi.no',
    description='Areal integration with Voronoi diagrams',
    install_requires=[
        'matplotlib',
        'pandas',
        'numpy',
        'tatukgis_pdk'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
