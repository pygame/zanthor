
from setuptools import setup, find_packages

setup(
    name='zanthor',
    version="1.2.4",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Games/Entertainment :: Arcade',
        "Topic :: Games/Entertainment :: Real Time Strategy",
    ],
    license='GPL',
    author="Aaron, Phil, Rene, Tim",
    author_email="renesd@gmail.com",
    maintainer='Rene Dudfield',
    maintainer_email='renesd@gmail.com',
    description="Zanthor is a game where you play an evil robot castle which is powered by steam.  @zanthorgame #python #pygame",
    url="http://github.com/pygame/zanthor/",
    include_package_data=True,
    long_description='Zanthor is a game where you play an evil robot castle which is powered by steam.',
    package_dir={'zanthor': 'zanthor'},
    packages=find_packages(),
    install_requires=['pygame'],
    entry_points={
        'console_scripts': [
            'zanthor=zanthor.main:main',
        ],
    },
)
