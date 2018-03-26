from setuptools import setup, find_packages
from version import __VERSION__
import os
import io

def read_contents(fname='README.md'):
    """read contents of readme into setup.py long_description field
    """
    return io.open(os.path.join(os.path.dirname(__file__),
                                fname), encoding="utf-8").read()

setup(
    name='pyBusylight',
    version=__VERSION__,
    url='https://github.com/ericpulvino/pyBusylight',
    description='Python Library for Kuando Busylight device.',
    long_description=read_contents(),
    author='Eric Pulvino',
    author_email='ericpulvino@gmail.com',
    install_requires=[
        'setuptools',
        'pyusb'
    ],
    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    
        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',
    
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='kuando busylight',
    project_urls={
        'Documentation':'https://github.com/ericpulvino/pyBusylight/docs',
        'Source':'https://github.com/ericpulvino/pyBusylight',
        'Tracker':'https://github.com/ericpulvino/pyBusylight/issues'
    },
    packages=find_packages(),
    python_requires='>=2.7',
)
