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
         ("pypy pangloss2.py < test/paperinfo.php", "PHP")]

successes = 0
failures = 0
for (cmd, value) in tests:
    str = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    if (str != value):
        failures = failures + 1
        print "Failed : " + cmd + " -> " + str + " ( should be " + value + ")"
    else:
        successes = successes + 1

passrate = 100.0 * float(successes)/(successes + failures)
print passrate,
print "% tests passed."
