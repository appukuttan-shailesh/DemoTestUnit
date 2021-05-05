try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='DemoTestUnit',
    version='1.2.0',
    author='Shailesh Appukuttan, Andrew Davison',
    author_email='shailesh.appukuttan@unic.cnrs-gif.fr',
    packages=['DemoTestUnit',
              'DemoTestUnit.tests',
              'DemoTestUnit.capabilities',
              'DemoTestUnit.scores',
              'DemoTestUnit.plots',],
    url='https://github.com/appukuttan-shailesh/DemoTestUnit',
    keywords=['electrophysiology', 'electrical',
              'testing', 'validation framework'],
    license='MIT',
    description='A SciUnit library for data-driven testing of neurons.',
    install_requires=['efel']
)
