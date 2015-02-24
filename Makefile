MANAGE=./manage.py
APP=brownfield_django
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python jshint validate test flake8

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/phantomjs/bin/phantomjs:
	npm install phantomjs --prefix .

node_modules/qunit-phantomjs-runner:
	npm install qunit-phantomjs-runner --prefix .

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint media/js/ccnmtljs

qunit-phantomjs-runner: node_modules/qunit-phantomjs-runner/runner.js
	./node_modules/phantomjs/bin/phantomjs node_modules/qunit-phantomjs-runner/runner.js media/js/ccnmtljs/tests/qunit_html.html

casperjs: node_modules/casper/test.js
	./node_modules/casperjs/bin/casperjs test media/js/ccnmtljs/tests/casper-tests.js

phantomjs: node_modules/phantomjs/bin/phantomjs
	./node_modules/phantomjs/bin/phantomjs media/js/ccnmtljs/tests/phantom-tests.js

test: ./ve/bin/python
	$(MANAGE) jenkins

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=8

runserver: ./ve/bin/python validate
	$(MANAGE) runserver

migrate: ./ve/bin/python validate jenkins
	$(MANAGE) migrate

validate: ./ve/bin/python
	$(MANAGE) validate

shell: ./ve/bin/python
	$(MANAGE) shell_plus

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make validate
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make validate
	make test
	make migrate
	make flake8

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
