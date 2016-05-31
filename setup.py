from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.2.0'

install_requires = [
    'beautifulsoup4'
]


setup(name='flask-test-machine',
    version=version,
    description="Wrapper to the flask test client to easily test multiple step "
                "interactions",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='Flask Test PyTest',
    author='Alex J Bartlett',
    author_email='alex@sourceshaper.com',
    url='http://www.sourceshaper.com',
    license='Public Domain',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['flask-test-machine=flasktestmachine:main']
    }
)
