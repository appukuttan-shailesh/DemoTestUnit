try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PackageName',
    version='0.1',
    author='Shailesh Appukuttan, Andrew Davison',
    author_email='shailesh.appukuttan@unic.cnrs-gif.fr',
    packages=['PackageName',
              'PackageName.tests',
              'PackageName.capabilities',
              'PackageName.scores',
              'PackageName.plots',],
    url='https://github.com/appukuttan-shailesh/PackageName',
    keywords=['electrophysiology', 'electrical',
              'testing', 'validation framework'],
    license='MIT',
    description='A SciUnit library for data-driven testing of neurons.',
    install_requires=['efel']
)
