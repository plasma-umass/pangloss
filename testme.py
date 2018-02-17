import subprocess

tests = [("./pangloss.py test/csrankings.js", "JavaScript"),
         ("./pangloss.py test/csrankings.ts", "TypeScript"),
         ("./pangloss.py test/csrankings.py", "Python"),
         ("./pangloss.py test/libhoard.cpp", "C++"),
         ("./pangloss.py test/hoardmanager.h", "C++"),
         ("./pangloss.py test/Scheduler.scala", "Scala"),
         ("./pangloss.py test/student_eval.cgi", "Perl"),
         ("./pangloss.py test/ProxyUriUtils.java", "Java"),
         ("./pangloss.py test/jquery-3.1.0.js", "JavaScript"),
         ("./pangloss.py test/divbyzero.c", "C"),
         ("./pangloss.py test/divbyzero.cpp", "C++"),
         ("./pangloss.py test/divbyzero.js", "JavaScript"),
         ("./pangloss.py test/divbyzero.py", "Python"),
         ("./pangloss.py test/divbyzero.pl", "Perl"),
         ("./pangloss.py test/divbyzero.rb", "Ruby"),
         ("./pangloss.py test/divbyzero.scala", "Scala"),
         ("./pangloss.py test/divbyzero.java", "Java"),
         ("./pangloss.py test/hashjoin.java", "Java"),
         ("./pangloss.py test/paperinfo.php", "PHP"),
         ("./pangloss.py test/bottles.c", "C"),
         ("./pangloss.py test/bottles.cpp", "C++"),
         ("./pangloss.py test/bottles.js", "JavaScript"),
         ("./pangloss.py test/bottles.php", "PHP"),
         ("./pangloss.py test/bottles.py", "Python"),
         ("./pangloss.py test/bottles.pl", "Perl"),
         ("./pangloss.py test/bottles.rb", "Ruby"),
         ("./pangloss.py test/bottles.scala", "Scala"),
         ("./pangloss.py test/bottles.m", "Objective-C"),
         ("./pangloss.py test/customrr.m", "Objective-C"),
         ("./pangloss.py test/bottles.java", "Java")]

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
