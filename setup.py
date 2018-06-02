from setuptools import setup, find_packages
from codecs import open
from os import path


BASE_DIR = path.abspath(path.dirname(__file__))

# Get the long description from the README.md file.
with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Import the version.
import shipment
version = shipment.__version__


setup(
    name='shipment',
    version=version,
    description='Ship logs to your ELK Stack',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roaldnefs/shipment',
    author='Roald Nefs',
    author_email='info@roaldnefs.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    license='MIT',
    keywords='elk logstash redis logging logger',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['redis'],
    extra_require={
        'test': [],
    },
)
