from setuptools import setup, find_packages


with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name="dopr",
    version="0.1.0",
    description="CLI Tool for my Digital Ocean Workspace",
    long_description=readme,
    author='Ayoub ED-DAFALI',
    author_email='ayoubensalem@gmail.com',
    packages=find_packages('src'),
    package_dir={'':'src'},
    setup_requires=[],
    install_requires=["python-digitalocean"],
    entry_points={
        'console_scripts': [
            'dopr=dopr.cli:main'],
    }
)
