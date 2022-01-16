from setuptools import setup, find_packages

setup(
    name='pandas-cli',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'prompt-toolkit',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'pandas-cli = pandas_cli.simple:main'
        ],
    },
)
