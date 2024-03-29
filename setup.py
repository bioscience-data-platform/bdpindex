
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'docs/changes.rst')).read()
version = '0.0.3'

setup(
    name="bdp",
    version=version,
    url='http://github.com/mytardis/mytardis',
    license='MIT License',
    long_description=README + '\n\n' + CHANGES,
    author='Iman Yusuf',
    author_email='Iman.Yusuf@rmit.edu.au',
    packages=find_packages(),
    namespace_packages=['bdpindex'],
    install_requires=[
        'setuptools',
        'django==1.4.1',
        'django-registration',
        'django-extensions',
        'django-form-utils',
        'django-haystack',
        'django-bootstrap-form',
        'celery==2.5.5',           # Delayed tasks and queues
        'django-celery==2.5.5',
        'django-kombu',
        'django-mptt',
        'django-storages',
        'pysolr==2.1.0-beta',
        'pyoai==2.4.4'
        ],
    dependency_links = [
        'https://github.com/dahlia/wand/tarball/warning-bugfix#egg=Wand-0.1.10',
        'https://github.com/UQ-CMM-Mirage/django-celery/tarball/2.5#egg=django-celery-2.5.5',
        'https://github.com/defunkt/pystache/tarball/v0.5.2#egg=pystache-0.5.2'
    ],
)
