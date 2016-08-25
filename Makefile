all:

.PHONY: test train

train: classifiers.csv

clean:
	rm python.csv javascript.csv cplusplus.csv typescript.csv ruby.csv perl.csv scala.csv c.csv java.csv

test:
	pypy pangloss2.py < test/coffee_webservice.rb
	pypy pangloss2.py < test/csrankings.js
	pypy pangloss2.py < test/csrankings.py
	pypy pangloss2.py < test/libhoard.cpp
	pypy pangloss2.py < test/hoardmanager.h
	pypy pangloss2.py < test/Scheduler.scala
	pypy pangloss2.py < test/student_eval.cgi
	pypy pangloss2.py < test/ProxyUriUtils.java
	pypy pangloss2.py < test/jquery-3.1.0.js
	pypy pangloss2.py < test/divbyzero.c
	pypy pangloss2.py < test/divbyzero.cpp
	pypy pangloss2.py < test/divbyzero.js
	pypy pangloss2.py < test/divbyzero.py
	pypy pangloss2.py < test/divbyzero.pl
	pypy pangloss2.py < test/divbyzero.rb
	pypy pangloss2.py < test/divbyzero.scala
	pypy pangloss2.py < test/divbyzero.java
	pypy pangloss2.py < test/hashjoin.java
	pypy pangloss2.py < test/paperinfo.php

classifiers.csv: python.csv javascript.csv cplusplus.csv typescript.csv ruby.csv perl.csv scala.csv c.csv java.csv
	cat python.csv javascript.csv cplusplus.csv typescript.csv ruby.csv perl.csv scala.csv c.csv java.csv > classifiers.csv

python.csv: train/python-files.txt.gz
	gzip -dc train/python-files.txt.gz     | pypy count-ascii.py 1 > python.csv

javascript.csv: train/javascript-files.txt.gz
	gzip -dc train/javascript-files.txt.gz | pypy count-ascii.py 2 > javascript.csv

cplusplus.csv: train/cplusplus-files.txt.gz
	gzip -dc train/cplusplus-files.txt.gz  | pypy count-ascii.py 3 > cplusplus.csv

typescript.csv: train/typescript-files.txt.gz
	gzip -dc train/typescript-files.txt.gz | pypy count-ascii.py 4 > typescript.csv

ruby.csv:  train/ruby-files.txt.gz
	gzip -dc train/ruby-files.txt.gz       | pypy count-ascii.py 5 > ruby.csv

perl.csv:  train/perl-files.txt.gz
	gzip -dc train/perl-files.txt.gz       | pypy count-ascii.py 6 > perl.csv

scala.csv:  train/scala-files.txt.gz
	gzip -dc train/scala-files.txt.gz      | pypy count-ascii.py 7 > scala.csv

c.csv:  train/c-files.txt.gz
	gzip -dc train/c-files.txt.gz          | pypy count-ascii.py 8 > c.csv

java.csv:  train/c-files.txt.gz
	gzip -dc train/java-files.txt.gz       | pypy count-ascii.py 9 > java.csv

