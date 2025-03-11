from setuptools import setup, find_packages

setup(
    name='TUEvolution',
    version='0.1.0',
    description='SC4ME evolution simulation',
    author='Clemens Verhoosel',
    author_email='c.v.verhoosel@tue.nl',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pygame',
        'matplotlib',
        'toml',
        'pathlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
