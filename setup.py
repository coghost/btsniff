from setuptools import setup, find_packages
from btsniff import VERSION

setup(
    name='btsniff',
    version=VERSION,
    include_package_data=True,
    package_data={
        '': ['README.md'],
        'btsniff': ['data/*.yaml'],
    },
    packages=find_packages(),
    author='lihe',
    author_email='imanux@sina.com',
    url='https://github.com/coghost/btsniff',
    description='movie searcher',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GPL',
    install_requires=[
        'icraw', 'iparse', 'lxml', 'click', 'urllib3', 'vto'
    ],
    entry_points={
        'console_scripts': ['btsniff=btsniff.app:run'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/coghost/btsniff/issues',
        'Source': 'https://github.com/coghost/btsniff',
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords=['movie', 'movie searcher', 'douban']
)
