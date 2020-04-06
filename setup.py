from setuptools import setup, find_packages
from fetchmovie import VERSION

setup(
    name='fetchmovie',
    version=VERSION,
    include_package_data=True,
    package_data={
        '': ['README.md'],
        'fetchmovie': ['data/*.yaml'],
    },
    packages=find_packages(),
    author='lihe',
    author_email='imanux@sina.com',
    url='https://github.com/coghost/fetchmovie',
    description='movie searcher',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GPL',
    install_requires=[
        'icraw', 'iparse', 'lxml', 'click', 'urllib3', 'vto'
    ],
    entry_points={
        'console_scripts': ['fetchmovie=fetchmovie.app:run'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/coghost/fetchmovie/issues',
        'Source': 'https://github.com/coghost/fetchmovie',
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords=['movie', 'movie searcher', 'douban']
)
