#fake Makefile for zanthor, to support the common
# ./configure;make;make install

PYTHON = python

#build: Setup setup.py
build: setup.py
	$(PYTHON) setup.py build

#install: Setup setup.py
install: setup.py
	$(PYTHON) setup.py install

#Setup:
#	$(PYTHON) configure.py

test check tests:
	$(PYTHON) run_tests.py

testall:
	python2.5 setup.py test
	python2.6 setup.py test
	python3.1 setup.py test
	make checkdocs

#docs:	install
#	cd docs/utils
#	$(PYTHON) makedocs.py

clean:
	rm -rf build dist MANIFEST .coverage
	rm -f lib/*~ src/*~ test/*~
	rm -rf bin develop-eggs eggs parts .installed.cfg zanthor.egg-info
	find . -name *.pyc -exec rm {} \;
	find . -name *.swp -exec rm {} \;
	$(PYTHON) setup.py clean

# push changes
push:
	#bzr push lp:zanthor
	svn commit

# commit changes
commit:
	#bzr commit
	svn commit

#upload to pypi
upload:
	make clean
	$(PYTHON) setup.py sdist upload --sign --identity="Rene Dudfield <renesd@gmail.com>" 

sdist:
	make clean
	make testall
	$(PYTHON) setup.py sdist

checkdocs:
	$(PYTHON) setup.py checkdocs -setuptools

showdocs:
	$(PYTHON) setup.py showdocs -setuptools

coverage:
	coverage run run_tests.py
	coverage report -m


