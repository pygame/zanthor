#  makes the files in the ../ directory.


export DIRNAME=toba_game_source_`date +%Y_%m_%d_%H_%M`

cd ../
echo "Making directory"
mkdir $DIRNAME

echo "Copying in game files."
rsync -a --exclude=.svn --exclude=*.pyc --exclude=*.swp --exclude=*.pyo --exclude=sfx --exclude=graphics trunk/ $DIRNAME/


#copy in pgu if it is there.
#echo "Copying in pgu"
#test -d /home/rene/dev/pygame/pgu/pgu/dist/pgu/pgu && rsync -a --exclude=.svn --exclude=*.pyc --exclude=*.swp --exclude=*.pyo /home/rene/dev/pygame/pgu/pgu/dist/pgu/pgu $DIRNAME/
#test -d /home/rene/dev/pygame/pgu/pgu/dist/pgu/data && rsync -a --exclude=.svn --exclude=*.pyc --exclude=*.swp --exclude=*.pyo /home/rene/dev/pygame/pgu/pgu/dist/pgu/data $DIRNAME/


echo "Making tar"
tar -cvf $DIRNAME.tar $DIRNAME

echo "Backing up tar."
cp -a $DIRNAME.tar $DIRNAME.tar.bak

echo "Compressing files. gzip..."
gzip -9 $DIRNAME.tar
echo "Compressing bzip2..."
mv $DIRNAME.tar.bak $DIRNAME.tar
bzip2 -9 $DIRNAME.tar
echo "Compressing zip..."
zip -9 -r $DIRNAME.zip $DIRNAME



