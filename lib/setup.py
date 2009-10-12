from distutils.core import setup, Extension
try:
    import py2exe
except:
    pass

import sys
import glob
import os
import shutil

cmd = sys.argv[1]

data = [
    '*.txt',
    os.path.join("data","gfx","*"),
    os.path.join("data","intro","*"),
    os.path.join("data","levels","*"),
    os.path.join("data","menu","*"),
    os.path.join("data","sounds","*"),
    os.path.join("data","themes","default","*"),
    ]

src = [
    '*.py',
    '*.c',
    '*.h',
    '*.i',
    ]

if cmd in ('sdist'):
    f = open("MANIFEST.in","w")
    for l in data: f.write("include "+l+"\n")
    for l in src: f.write("include "+l+"\n")
    f.close()


if cmd in ('sdist','build'):
    setup(
        name='zanthor',
        version='1.0',
        description='Zanthor',
        author='Phil Hassey',
        author_email='philhassey@yahoo.com',
        url='http://www.imitationpickles.org/pyweek2/',
        )

if cmd in ('py2exe',):
    setup(
        options={'py2exe':{
            'dist_dir':'dist',
            'dll_excludes':['_dotblas.pyd','_numpy.pyd']
            }},
        windows=[{
            'script':'main.py',
            #'icon_resources':[(1,'icon.ico')],
            }],
        )

if cmd in ('build',):
    for fname in glob.glob("build/lib*/*.so"):
        shutil.copy(fname,os.path.basename(fname))

    for fname in glob.glob("build/lib*/*.pyd"):
        shutil.copy(fname,os.path.basename(fname))

if cmd in ('py2exe',):
    for gname in data:
        for fname in glob.glob(gname):
            dname = os.path.join('dist',os.path.dirname(os.path.dirname(os.path.dirname(fname))))
            try:
                os.mkdir(dname)
            except:
                'mkdir failed: '+dname
                
            dname = os.path.join('dist',os.path.dirname(os.path.dirname(fname)))
            try:
                os.mkdir(dname)
            except:
                'mkdir failed: '+dname


            dname = os.path.join('dist',os.path.dirname(fname))
            try:
                os.mkdir(dname)
            except:
                'mkdir failed: '+dname
            shutil.copy(fname,dname)

