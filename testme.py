import subprocess

tests = [("pypy pangloss2.py < test/csrankings.js", "JavaScript"),
         ("pypy pangloss2.py < test/csrankings.py", "Python"),
         ("pypy pangloss2.py < test/libhoard.cpp", "C++"),
         ("pypy pangloss2.py < test/hoardmanager.h", "C++"),
         ("pypy pangloss2.py < test/Scheduler.scala", "Scala"),
         ("pypy pangloss2.py < test/student_eval.cgi", "Perl"),
         ("pypy pangloss2.py < test/ProxyUriUtils.java", "Java"),
         ("pypy pangloss2.py < test/jquery-3.1.0.js", "JavaScript"),
         ("pypy pangloss2.py < test/divbyzero.c", "C"),
         ("pypy pangloss2.py < test/divbyzero.cpp", "C++"),
         ("pypy pangloss2.py < test/divbyzero.js", "JavaScript"),
         ("pypy pangloss2.py < test/divbyzero.py", "Python"),
         ("pypy pangloss2.py < test/divbyzero.pl", "Perl"),
         ("pypy pangloss2.py < test/divbyzero.rb", "Ruby"),
         ("pypy pangloss2.py < test/divbyzero.scala", "Scala"),
         ("pypy pangloss2.py < test/divbyzero.java", "Java"),
         ("pypy pangloss2.py < test/hashjoin.java", "Java"),
         ("pypy pangloss2.py < test/paperinfo.php", "PHP"),
         ("pypy pangloss2.py < test/bottles.c", "C"),
         ("pypy pangloss2.py < test/bottles.cpp", "C++"),
         ("pypy pangloss2.py < test/bottles.js", "JavaScript"),
         ("pypy pangloss2.py < test/bottles.php", "PHP"),
         ("pypy pangloss2.py < test/bottles.py", "Python"),
         ("pypy pangloss2.py < test/bottles.pl", "Perl"),
         ("pypy pangloss2.py < test/bottles.rb", "Ruby"),
         ("pypy pangloss2.py < test/bottles.scala", "Scala"),
         ("pypy pangloss2.py < test/bottles.m", "Objective-C"),
         ("pypy pangloss2.py < test/customrr.m", "Objective-C"),
         ("pypy pangloss2.py < test/bottles.java", "Java")]

successes = 0
failures = 0
for (cmd, value) in tests:
    string = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    if (string != value):
        failures = failures + 1
        print "Failed : " + cmd + " -> " + string + " ( should be " + value + ")"
    else:
        successes = successes + 1

passrate = 100.0 * float(successes)/(successes + failures)
print passrate,
print "% tests passed (" + str(successes) + "/" + str(successes+failures) + ")."
