all:

.PHONY: test train

train: classifiers.csv

test:
	python glosser.py classifiers.csv classes.csv < test/coffee_webservice.rb
	python glosser.py classifiers.csv classes.csv < test/csrankings.js
	python glosser.py classifiers.csv classes.csv < test/csrankings.py
	python glosser.py classifiers.csv classes.csv < test/libhoard.cpp
	python glosser.py classifiers.csv classes.csv < test/hoardmanager.h
	python glosser.py classifiers.csv classes.csv < test/Scheduler.scala
	python glosser.py classifiers.csv classes.csv < test/student_eval.cgi
	python glosser.py classifiers.csv classes.csv < test/divbyzero.c
	python glosser.py classifiers.csv classes.csv < test/divbyzero.cpp
	python glosser.py classifiers.csv classes.csv < test/divbyzero.js
	python glosser.py classifiers.csv classes.csv < test/divbyzero.py
	python glosser.py classifiers.csv classes.csv < test/divbyzero.pl
	python glosser.py classifiers.csv classes.csv < test/divbyzero.rb
	python glosser.py classifiers.csv classes.csv < test/divbyzero.scala

classifiers.csv: python.csv javascript.csv cplusplus.csv typescript.csv ruby.csv perl.csv scala.csv c.csv
	cat python.csv javascript.csv cplusplus.csv typescript.csv ruby.csv perl.csv scala.csv c.csv > classifiers.csv

python.csv: train/python-files.txt.gz
	gzip -dc train/python-files.txt.gz     | python count-ascii.py 1 > python.csv

javascript.csv: train/javascript-files.txt.gz
	gzip -dc train/javascript-files.txt.gz | python count-ascii.py 2 > javascript.csv

cplusplus.csv: train/cplusplus-files.txt.gz
	gzip -dc train/cplusplus-files.txt.gz  | python count-ascii.py 3 > cplusplus.csv

typescript.csv: train/typescript-files.txt.gz
	gzip -dc train/typescript-files.txt.gz | python count-ascii.py 4 > typescript.csv

ruby.csv:  train/ruby-files.txt.gz
	gzip -dc train/ruby-files.txt.gz       | python count-ascii.py 5 > ruby.csv

perl.csv:  train/perl-files.txt.gz
	gzip -dc train/perl-files.txt.gz       | python count-ascii.py 6 > perl.csv

scala.csv:  train/scala-files.txt.gz
	gzip -dc train/scala-files.txt.gz       | python count-ascii.py 7 > scala.csv

c.csv:  train/c-files.txt.gz
	gzip -dc train/c-files.txt.gz       | python count-ascii.py 8 > c.csv

