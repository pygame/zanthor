import os

APP_NAME = "zanthor"
DESCRIPTION = open("README.md").read()

METADATA = {
    "name": APP_NAME,
    "version": "1.2.3",
    "license": "GPL",
    "description": "Zanthor is a game where you play an evil robot castle which is powered by steam.  @zanthorgame #python #pygame",
    "author": "zanthor.org",
    "author_email": "renesd@gmail.com",
    "url": "http://www.zanthor.org/",
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
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
        "Topic :: Software Development :: Libraries :: pygame",
        "Topic :: Games/Entertainment :: Real Time Strategy",
    ],
    "py2exe.target": "",
    #'py2exe.icon':'icon.ico', #64x64
    "py2exe.binary": APP_NAME,  # leave off the .exe, it will be added
    "py2app.target": APP_NAME,
    "py2app.icon": "icon.icns",  # 128x128
    #'cx_freeze.cmd':'~/src/cx_Freeze-3.0.3/FreezePython',
    "cx_freeze.cmd": "cxfreeze",
    "cx_freeze.target": "%s_linux" % APP_NAME,
    "cx_freeze.binary": APP_NAME,
}


cmdclass = {}
PACKAGEDATA = {
    "cmdclass": cmdclass,
    "package_dir": {
        "zanthor": "zanthor",
    },
    "packages": [
        "zanthor",
        "zanthor.pgu",
        "zanthor.pgu.gui",
    ],
    "scripts": ["scripts/zanthor"],
}

PACKAGEDATA.update(METADATA)


from distutils.core import setup
import sys
import glob
import os
import shutil

try:
    cmd = sys.argv[1]
except IndexError:
    print("Usage: setup.py install|sdist")
    raise SystemExit


# utility for adding subdirectories
def add_files(dest, generator):
    for dirpath, dirnames, filenames in generator:
        for name in "CVS", ".svn":
            if name in dirnames:
                dirnames.remove(name)

        for name in filenames:
            if "~" in name:
                continue
            suffix = os.path.splitext(name)[1]
            if suffix in (".pyc", ".pyo"):
                continue
            if name[0] == ".":
                continue
            filename = os.path.join(dirpath, name)
            dest.append(filename)


# define what is our data
_DATA_DIR = os.path.join("zanthor", "data")
data = []
add_files(data, os.walk(_DATA_DIR))


# data_dirs = [os.path.join(f2.replace(_DATA_DIR, 'data'), '*') for f2 in data]
data_dirs = [os.path.join(f2.replace(_DATA_DIR, "data")) for f2 in data]
PACKAGEDATA["package_data"] = {"zanthor": data_dirs}


data.extend(glob.glob("*.txt"))
data.extend(glob.glob("*.md"))
# data.append('MANIFEST.in')
# define what is our source
src = []
add_files(src, os.walk("zanthor"))
src.extend(glob.glob("*.py"))


# build the sdist target
if cmd not in "py2exe py2app cx_freeze".split():
    f = open("MANIFEST.in", "w")
    for l in data:
        f.write("include " + l + "\n")
    for l in src:
        f.write("include " + l + "\n")
    f.close()

    setup(**PACKAGEDATA)
