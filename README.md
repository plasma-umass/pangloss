pangloss: automatically detect the language a piece of code is written in

Training data:
* JavaScript sources from http://www.srl.inf.ethz.ch/js150.php
* C++ sources from Clang
* Scala sources from Apache Spark
* Ruby sources from the top 20 most downloaded gems on Rubygems.org
* Java sources from top projects (used to be OpenJDK, Hadoop, and Eclipse Core)
  - comments removed with:
      perl -0pe 's|//.*?\n|\n|g; s#/\*(.|\n)*?\*/##g;'
gunzip -dc java-files.txt.gz | perl -0pe 's|//.*?\n|\n|g; s#/\*(.|\n)*?\*/##g;' | head -n 50000000 > java-50MLOC.txt

* Perl sources from all modules included in Task::Kensho (https://metacpan.org/pod/Task::Kensho)
