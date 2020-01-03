# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0',
    packages=find_packages(),
    package_data={
            'NepaliNewsScrapper': ['proxy.txt']
    },
    entry_points={'scrapy': ['settings = NepaliNewsScrapper.settings']}, install_requires=['scrapy', 'scrapy_proxies']
)