from setuptools import setup, find_packages

setup(
    name='VarTools',
    version='0.1.0',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'convert_vartrace = vartools.traceconverter:convert_vartrace']},
    install_requires=['ply', 'future'],
    # pypi metadata
    author='Alexey Naydenov',
    author_email='alexey.naydenov@linux.com',
    description='Functions and scripts for working with VarTrace logs',
    license='GPL',
    keywords='log trace',
    url='http://alexey-naydenov.github.io/vartools/',
)
