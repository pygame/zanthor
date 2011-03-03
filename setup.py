import os

# usage: python setup.py command
#
# sdist - build a source dist
# py2exe - build an exe
# py2app - build an app
# cx_freeze - build a linux binary (not implemented)
#
# the goods are placed in the dist dir for you to .zip up or whatever...


APP_NAME = 'zanthor'
DESCRIPTION = open('README.txt').read()
CHANGES = open('CHANGES.txt').read()
TODO = open('TODO.txt').read()




METADATA = {
    'name':APP_NAME,
    'version':          '1.2.2',
    'license':          'GPL',
    'description':      'Zanthor is a game where you play an evil robot castle which is powered by steam.  @zanthorgame #python #pygame',
    'author':           'zanthor.org',
    'author_email':     'renesd@gmail.com',
    'url':              'http://www.zanthor.org/',
    'classifiers':      [
            'Development Status :: 4 - Beta',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Topic :: Software Development :: Libraries :: pygame',
            'Topic :: Games/Entertainment :: Real Time Strategy',
    ],


    'py2exe.target':'',
    #'py2exe.icon':'icon.ico', #64x64
    'py2exe.binary':APP_NAME, #leave off the .exe, it will be added
    
    'py2app.target':APP_NAME,
    'py2app.icon':'icon.icns', #128x128
    
    #'cx_freeze.cmd':'~/src/cx_Freeze-3.0.3/FreezePython',
    'cx_freeze.cmd':'cxfreeze',
    'cx_freeze.target':'%s_linux' % APP_NAME,
    'cx_freeze.binary':APP_NAME,
    }
    
files_to_remove = ['tk84.dll',
                    '_ssl.pyd',
                    'tcl84.dll',
                    os.path.join('numpy','core', '_dotblas.pyd'),
                    os.path.join('numpy', 'linalg', 'lapack_lite.pyd'),
]


directories_to_remove = [os.path.join('numpy', 'distutils'),
                         'distutils',
                         'tcl',
]


cmdclass = {}
PACKAGEDATA = {
    'cmdclass':    cmdclass,

    'package_dir': {'zanthor': 'zanthor',
                   },
    'packages': ['zanthor',
                 'zanthor.pgu',
                 'zanthor.pgu.gui',
                ],
    'scripts': ['scripts/zanthor'],
}

PACKAGEDATA.update(METADATA)


from distutils.core import setup, Extension
try:
    import py2exe
except:
    pass

import sys
import glob
import os
import shutil

try:
    cmd = sys.argv[1]
except IndexError:
    print 'Usage: setup.py install|py2exe|py2app|cx_freeze'
    raise SystemExit

# utility for adding subdirectories
def add_files(dest,generator):
    for dirpath, dirnames, filenames in generator:
        for name in 'CVS', '.svn':
            if name in dirnames:
                dirnames.remove(name)

        for name in filenames:
            if '~' in name: continue
            suffix = os.path.splitext(name)[1]
            if suffix in ('.pyc', '.pyo'): continue
            if name[0] == '.': continue
            filename = os.path.join(dirpath, name)
            dest.append(filename)

# define what is our data
_DATA_DIR = os.path.join('zanthor', 'data')
data = []
add_files(data,os.walk(_DATA_DIR))

if 0:
    data_dirs = [os.path.join(f2.replace(_DATA_DIR, 'data'), '*') for f2 in data]
    print data_dirs
else:
    data_dirs = ['data/gfx/caastles.png/*', 'data/gfx/background_illustration.png/*', 'data/gfx/heart.xcf.bz2/*', 'data/gfx/tileedit.ini/*', 'data/gfx/tiles.tga/*', 'data/gfx/background_equipment.png/*', 'data/gfx/hairs.tga/*', 'data/gfx/coal.png/*', 'data/gfx/background_bottom.png/*', 'data/gfx/hole2.png/*', 'data/gfx/tiles2.tga/*', 'data/gfx/hole.png/*', 'data/gfx/castle1.png/*', 'data/gfx/background_status_left.png/*', 'data/gfx/heart_pulse.png/*', 'data/gfx/castle1.tga/*', 'data/gfx/tileedit.py/*', 'data/gfx/hole4.png/*', 'data/gfx/heart.png/*', 'data/gfx/hole3.png/*', 'data/intro/ETHNOCEN.TTF/*', 'data/intro/soundtrack2.ogg/*', 'data/intro/grass.ogg/*', 'data/intro/dazzlesh.ttf/*', 'data/intro/read_me.html/*', 'data/intro/intro1.ogg/*', 'data/intro/mybkgr.png/*', 'data/intro/title.jpg/*', 'data/intro/soundtrack1.ogg/*', 'data/intro/zanthor.ogg/*', 'data/intro/WALSHES.TTF/*', 'data/intro/introbg.png/*', 'data/intro/soundtrack3.ogg/*', 'data/sounds/peasants1.ogg/*', 'data/sounds/cannon2.ogg/*', 'data/sounds/hitground.ogg/*', 'data/sounds/squish2.ogg/*', 'data/sounds/water.ogg/*', 'data/sounds/peasants2.ogg/*', 'data/sounds/peasants3.ogg/*', 'data/sounds/birds1.ogg/*', 'data/sounds/ouch2.ogg/*', 'data/sounds/upgrade.ogg/*', 'data/sounds/hitenemy.ogg/*', 'data/sounds/birds2.ogg/*', 'data/sounds/hitwall2.ogg/*', 'data/sounds/cannon3.ogg/*', 'data/sounds/engine-fast.ogg/*', 'data/sounds/cannon.ogg/*', 'data/sounds/coal.ogg/*', 'data/sounds/ouch1.ogg/*', 'data/sounds/squish1.ogg/*', 'data/sounds/engine-slow.ogg/*', 'data/sounds/destroyenemy.ogg/*', 'data/sounds/hitwall.ogg/*', 'data/sounds/release.ogg/*', 'data/themes/default/vslider.up.tga/*', 'data/themes/default/list.item.hover.png/*', 'data/themes/default/scroller.slide.v.tga/*', 'data/themes/default/scroller.slide.h.tga/*', 'data/themes/default/filebrowser.folder.png/*', 'data/themes/default/vslider.bar.hover.tga/*', 'data/themes/default/select.option.normal.png/*', 'data/themes/default/select.arrow.hover.tga/*', 'data/themes/default/vslider.bar.normal.tga/*', 'data/themes/default/checkbox.off.normal.tga/*', 'data/themes/default/select.selected.hover.tga/*', 'data/themes/default/rdot.hover.png/*', 'data/themes/default/list.item.down.png/*', 'data/themes/default/vdot.normal.png/*', 'data/themes/default/check.png/*', 'data/themes/default/box.normal.png/*', 'data/themes/default/box.hover.png/*', 'data/themes/default/menu.hover.tga/*', 'data/themes/default/hslider.right.tga/*', 'data/themes/default/list.png/*', 'data/themes/default/dialog.close.normal.tga/*', 'data/themes/default/desktop.png/*', 'data/themes/default/rdot.normal.png/*', 'data/themes/default/dialog.png/*', 'data/themes/default/slider.bar.hover.tga/*', 'data/themes/default/progressbar.bar.tga/*', 'data/themes/default/tool.down.tga/*', 'data/themes/default/notes.txt/*', 'data/themes/default/select.selected.down.tga/*', 'data/themes/default/x.png/*', 'data/themes/default/progressbar.tga/*', 'data/themes/default/right.png/*', 'data/themes/default/input.focus.png/*', 'data/themes/default/select.arrow.normal.tga/*', 'data/themes/default/menu.down.tga/*', 'data/themes/default/select.options.png/*', 'data/themes/default/sbox.normal.png/*', 'data/themes/default/hslider.bar.hover.tga/*', 'data/themes/default/list.item.normal.png/*', 'data/themes/default/button.hover.tga/*', 'data/themes/default/scroller.slide.bar.hover.tga/*', 'data/themes/default/hslider.bar.normal.tga/*', 'data/themes/default/select.arrow.png/*', 'data/themes/default/radio.png/*', 'data/themes/default/vbox.normal.png/*', 'data/themes/default/select.option.hover.png/*', 'data/themes/default/checkbox.on.normal.tga/*', 'data/themes/default/dialog.close.hover.tga/*', 'data/themes/default/box.xcf/*', 'data/themes/default/console.input.normal.png/*', 'data/themes/default/button.down.tga/*', 'data/themes/default/select.selected.normal.tga/*', 'data/themes/default/select.arrow.down.tga/*', 'data/themes/default/console.input.focus.png/*', 'data/themes/default/dot.normal.png/*', 'data/themes/default/checkbox.off.hover.tga/*', 'data/themes/default/hslider.tga/*', 'data/themes/default/radio.off.hover.tga/*', 'data/themes/default/down.png/*', 'data/themes/default/up.png/*', 'data/themes/default/vslider.down.tga/*', 'data/themes/default/hslider.left.tga/*', 'data/themes/default/tool.hover.tga/*', 'data/themes/default/dialog.bar.png/*', 'data/themes/default/menu.normal.tga/*', 'data/themes/default/vdot.down.png/*', 'data/themes/default/slider.tga/*', 'data/themes/default/vdot.hover.png/*', 'data/themes/default/dialog.close.down.tga/*', 'data/themes/default/radio.off.normal.tga/*', 'data/themes/default/generate.py/*', 'data/themes/default/rdot.down.png/*', 'data/themes/default/out.tga/*', 'data/themes/default/button.normal.tga/*', 'data/themes/default/listitem.hover.tga/*', 'data/themes/default/radio.on.hover.tga/*', 'data/themes/default/listitem.down.tga/*', 'data/themes/default/scroller.slide.bar.normal.tga/*', 'data/themes/default/listitem.normal.tga/*', 'data/themes/default/Vera.ttf/*', 'data/themes/default/idot.normal.png/*', 'data/themes/default/input.normal.png/*', 'data/themes/default/vslider.tga/*', 'data/themes/default/config.txt/*', 'data/themes/default/tool.normal.tga/*', 'data/themes/default/radio.on.normal.tga/*', 'data/themes/default/box.down.png/*', 'data/themes/default/left.png/*', 'data/themes/default/vsbox.normal.png/*', 'data/themes/default/dot.hover.png/*', 'data/themes/default/dot.xcf/*', 'data/themes/default/checkbox.on.hover.tga/*', 'data/themes/default/slider.bar.normal.tga/*', 'data/themes/default/console.png/*', 'data/themes/default/dot.down.png/*', 'data/themes/default/desktop.xcf/*', 'data/themes/gray/slider.png/*', 'data/themes/gray/radio.off.down.png/*', 'data/themes/gray/dialog.close.normal.png/*', 'data/themes/gray/filebrowser.folder.png/*', 'data/themes/gray/select.option.normal.png/*', 'data/themes/gray/checkbox.on.down.png/*', 'data/themes/gray/checkbox.off.normal.png/*', 'data/themes/gray/box.normal.png/*', 'data/themes/gray/list.png/*', 'data/themes/gray/desktop.png/*', 'data/themes/gray/dialog.png/*', 'data/themes/gray/input.focus.png/*', 'data/themes/gray/menu.option.hover.png/*', 'data/themes/gray/select.options.png/*', 'data/themes/gray/list.item.normal.png/*', 'data/themes/gray/tool.down.png/*', 'data/themes/gray/select.selected.normal.png/*', 'data/themes/gray/tool.normal.png/*', 'data/themes/gray/select.arrow.png/*', 'data/themes/gray/menu.normal.png/*', 'data/themes/gray/dialog.close.down.png/*', 'data/themes/gray/checkbox.off.down.png/*', 'data/themes/gray/slider.bar.normal.png/*', 'data/themes/gray/menu.option.normal.png/*', 'data/themes/gray/console.input.normal.png/*', 'data/themes/gray/console.input.focus.png/*', 'data/themes/gray/dialog.bar.png/*', 'data/themes/gray/radio.off.normal.png/*', 'data/themes/gray/button.down.png/*', 'data/themes/gray/Vera.ttf/*', 'data/themes/gray/checkbox.on.normal.png/*', 'data/themes/gray/radio.on.normal.png/*', 'data/themes/gray/input.normal.png/*', 'data/themes/gray/config.txt/*', 'data/themes/gray/radio.on.down.png/*', 'data/themes/gray/box.down.png/*', 'data/themes/gray/button.normal.png/*', 'data/themes/gray/menu.hover.png/*', 'data/themes/gray/select.arrow.down.png/*', 'data/themes/gray/console.png/*', 'data/themes/gray/select.arrow.normal.png/*', 'data/themes/gray/menu.down.png/*', 'data/themes/tools/icons48.draw.tga/*', 'data/themes/tools/icons48.bkgr.tga/*', 'data/themes/tools/icons48.tile.tga/*', 'data/themes/tools/icons48.code.tga/*', 'data/themes/tools/icons48.line.tga/*', 'data/themes/tools/icons48.fill.tga/*', 'data/themes/tools/icons48.pixel.tga/*', 'data/themes/tools/icons48.select.tga/*', 'data/themes/tools/config.txt/*', 'data/themes/tools/icons48.eraser.tga/*', 'data/levels/test.tga/*', 'data/levels/codes.tga/*', 'data/levels/tileedit.ini/*', 'data/levels/level1.tga/*', 'data/levels/tiles.tga/*', 'data/levels/level5.tga/*', 'data/levels/level7.tga/*', 'data/levels/level2.tga/*', 'data/levels/level4.tga/*', 'data/levels/level3.tga/*', 'data/levels/test2.tga/*', 'data/levels/test4.tga/*', 'data/levels/level6.tga/*', 'data/levels/leveledit.ini/*', 'data/levels/level8.tga/*', 'data/levels/leveledit.py/*', 'data/levels/test3.tga/*', 'data/menu/x.png/*', 'data/menu/read_me.html/*', 'data/menu/map.png/*', 'data/menu/vinque.ttf/*']


PACKAGEDATA['package_data'] = {'zanthor': data_dirs}
#PACKAGEDATA['package_data'] = {'zanthor': data}



data.extend(glob.glob('*.txt'))
data.append('MANIFEST.in')
# define what is our source
src = []
add_files(src,os.walk('zanthor'))
src.extend(glob.glob('*.py'))




# build the sdist target
if cmd not in "py2exe py2app cx_freeze".split():
    f = open("MANIFEST.in","w")
    for l in data: f.write("include "+l+"\n")
    for l in src: f.write("include "+l+"\n")
    f.close()
    
    setup(**PACKAGEDATA)

# build the py2exe target
if cmd in ('py2exe',):
    dist_dir = os.path.join('dist',METADATA['py2exe.target'])
    data_dir = dist_dir
    
    src = 'run_game.py'
    dest = METADATA['py2exe.binary']+'.py'
    shutil.copy(src,dest)
    
    setup(
        options={'py2exe':{
            'dist_dir':dist_dir,
            'dll_excludes':['_dotblas.pyd','_numpy.pyd', 'numpy.linalg.lapack_lite.pyd', 'numpy.core._dotblas.pyd'] + files_to_remove,
            'excludes':['matplotlib', 'tcl', 'OpenGL'],
            'ignores':['matplotlib', 'tcl', 'OpenGL'],
            'bundle_files':1,
            }},
#        windows=[{
       console=[{
            'script':dest,
            #'icon_resources':[(1,METADATA['py2exe.icon'])],
            }],
        )

# build the py2app target
if cmd == 'py2app':
    dist_dir = os.path.join('dist',METADATA['py2app.target']+'.app')
    data_dir = os.path.join(dist_dir,'Contents','Resources')
    from setuptools import setup

    src = 'run_game.py'
    dest = METADATA['py2app.target']+'.py'
    shutil.copy(src,dest)

    APP = [dest]
    DATA_FILES = []
    OPTIONS = {'argv_emulation': True, 
               #'iconfile':METADATA['py2app.icon']
              }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

# make the cx_freeze target
if cmd == 'cx_freeze':
    app_dist_dir = METADATA['cx_freeze.target'] + "_" + METADATA['version']
    dist_dir = os.path.join('dist', app_dist_dir)
    data_dir = dist_dir

    modules_exclude = "tcl,tk"
    cmd_args = (METADATA['cx_freeze.cmd'], dist_dir, METADATA['cx_freeze.binary'], modules_exclude)
    sys_cmd = '%s --install-dir=%s --target-name=%s --exclude-modules=%s run_game.py' % cmd_args
    print sys_cmd
    os.system(sys_cmd)

    import shutil
    if os.path.exists(os.path.join(data_dir, "tcl")): 
        shutil.rmtree( os.path.join(data_dir, "tcl") )
    if os.path.exists(os.path.join(data_dir, "tk")): 
        shutil.rmtree( os.path.join(data_dir, "tk") )



# recursively make a bunch of folders
def make_dirs(dname_):
    parts = list(os.path.split(dname_))
    dname = None
    while len(parts):
        if dname == None:
            dname = parts.pop(0)
        else:
            dname = os.path.join(dname,parts.pop(0))
        if not os.path.isdir(dname):
            os.mkdir(dname)

# copy data into the binaries 
if cmd in ('py2exe','cx_freeze','py2app'):
    dest = data_dir
    for fname in data:
        dname = os.path.join(dest,os.path.dirname(fname))
        make_dirs(dname)
        if not os.path.isdir(fname):
            #print (fname,dname)
            shutil.copy(fname,dname)

# make a tgz files.
if cmd == 'cx_freeze':
    sys_cmd = "cd dist; tar -vczf %s.tgz %s/" % (app_dist_dir,app_dist_dir)  
    os.system(sys_cmd)


# remove files from the zip.
if 0 and cmd in ('py2exe'):
    import shutil

    #shutil.rmtree( os.path.join('dist') )
    #shutil.rmtree( os.path.join('build') )


    os.system("unzip dist/library.zip -d dist\library")

    for fn in files_to_remove:
        os.remove( os.path.join('dist', 'library', fn) )


    for d in directories_to_remove:
        if os.path.exists( os.path.join('dist', 'library', d) ):
            shutil.rmtree( os.path.join('dist', 'library', d) )

    os.remove( os.path.join('dist', 'library.zip') )


    os.chdir("dist")
    os.chdir("library")

    os.system("zip -r -9 ..\library.zip .")

    os.chdir("..")
    os.chdir("..")

