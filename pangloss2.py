import sys
import csv
import math

def words(fileobj):
    for line in fileobj:
        for word in line.split():
            yield word

python = { '=' : 127029 ,  '#' : 75374 ,  'def' : 39952 ,  'the' : 37945 ,  'if' : 32369 ,  'in' : 22803 ,  'return' : 20984 ,  'a' : 20375 ,  'is' : 19248 ,  'for' : 18792 ,  'to' : 17378 ,  '->' : 16634 ,  'of' : 13981 ,  'and' : 13727 ,  'not' : 12204 ,  'import' : 11129 ,  'class' : 10772 ,  'LETTER' : 10544 ,  '+' : 10253 ,  '==' : 10017 ,  "'" : 9692 ,  'LATIN' : 7854 ,  'from' : 7832 ,  '"""' : 7749 ,  'with' : 7340 ,  'be' : 7093 ,  'else:' : 6495 ,  'or' : 6469 ,  '%' : 6417 ,  'None,' : 6384 ,  '1' : 6244 ,  'as' : 6021 ,  ':' : 5902 ,  'that' : 5860 ,  'try:' : 5660 ,  'SMALL' : 5169 ,  'raise' : 5036 ,  'print' : 4991 ,  '-' : 4809 ,  'CAPITAL' : 4679 ,  'pass' : 4628 ,  'this' : 4487 ,  'None' : 4392 ,  'except' : 4289 ,  '0' : 4265 ,  'an' : 4237 ,  'are' : 4200 ,  '>>>' : 3819 ,  'The' : 3798 ,  'it' : 3781 ,  'by' : 3751 ,  'WITH' : 3750 ,  'file' : 3560 ,  'on' : 3404 ,  'name' : 3375 ,  '*' : 3287 ,  'i' : 3142 ,  'x' : 2965 ,  'None:' : 2896 ,  '[]' : 2855 ,  'line' : 2841 ,  'elif' : 2808 ,  'which' : 2555 ,  's' : 2517 ,  'This' : 2507 ,  'test' : 2499 ,  '2' : 2392 ,  'value' : 2364 ,  'c' : 2350 ,  'will' : 2284 ,  'we' : 2272 ,  '"' : 2249 ,  '|' : 2246 ,  'b' : 2210 ,  'should' : 2208 ,  'If' : 2198 ,  '...' : 2189 ,  "'\\n'" : 2140 ,  'can' : 2139 ,  '>' : 2100 ,  '!=' : 2091 ,  '<' : 2076 ,  'all' : 2048 ,  'string' : 2045 ,  '0,' : 2041 ,  'data' : 2023 ,  '1,' : 2018 ,  'module' : 1982 ,  'result' : 1969 ,  '{' : 1924 ,  'list' : 1908 ,  'A' : 1854 ,  'while' : 1845 ,  'object' : 1830 ,  '0)' : 1824 ,  '1)' : 1820 ,  '}' : 1808 ,  'have' : 1788 ,  '\\' : 1727 ,  'when' : 1721 }

scala = { '=' : 90622 ,  '*' : 82814 ,  '{' : 56096 ,  '}' : 53650 ,  'val' : 48675 ,  '//' : 23499 ,  'def' : 23403 ,  '=>' : 21614 ,  'of' : 17675 ,  'new' : 16470 ,  'import' : 16065 ,  '*/' : 15631 ,  'for' : 14945 ,  'in' : 13963 ,  'case' : 12784 ,  '/**' : 12667 ,  'with' : 12597 ,  'this' : 12563 ,  'if' : 12416 ,  'under' : 9918 ,  'or' : 9629 ,  '+' : 9111 ,  'file' : 8644 ,  'override' : 8636 ,  '===' : 8378 ,  'License' : 7366 ,  'not' : 7319 ,  'private' : 6450 ,  'may' : 5598 ,  '==' : 5563 ,  'on' : 5488 ,  'class' : 5364 ,  'See' : 5104 ,  '::' : 5089 ,  'You' : 4951 ,  'Apache' : 4913 ,  'License.' : 4910 ,  'else' : 4789 ,  '|' : 4664 ,  'extends' : 4500 ,  '@param' : 4497 ,  'var' : 4455 ,  'Unit' : 4237 ,  '-' : 3982 ,  'use' : 3875 ,  'as' : 3851 ,  'should' : 3725 ,  'one' : 3529 ,  'at' : 3519 ,  '->' : 3467 ,  '1' : 3393 ,  'data' : 3345 ,  '"' : 3208 ,  'more' : 3179 ,  '/*' : 2918 ,  'This' : 2835 ,  'you' : 2808 ,  'String,' : 2792 ,  'required' : 2766 ,  'either' : 2741 ,  'copy' : 2686 ,  'specific' : 2612 ,  'package' : 2607 ,  'work' : 2601 ,  '2.0' : 2586 ,  '0' : 2580 ,  '+=' : 2563 ,  'except' : 2515 ,  'OR' : 2506 ,  'object' : 2500 ,  '(the' : 2479 ,  'obtain' : 2477 ,  'ANY' : 2466 ,  'language' : 2465 ,  'Version' : 2464 ,  'OF' : 2461 ,  'WITHOUT' : 2460 ,  'writing,' : 2459 ,  'Unless' : 2458 ,  'express' : 2458 ,  '"AS' : 2456 ,  'Licensed' : 2455 ,  'Software' : 2455 ,  '(ASF)' : 2455 ,  'license' : 2455 }



javascript = { '=' : 97582 ,  '{' : 71715 ,  '}' : 42792 ,  'var' : 40475 ,  '*' : 36627 ,  'if' : 30302 ,  '//' : 29291 ,  'return' : 22334 ,  'function' : 21499 ,  'the' : 17250 ,  '+' : 14450 ,  '===' : 11115 ,  'to' : 10506 ,  '});' : 9570 ,  'a' : 8828 ,  '};' : 8479 ,  '&&' : 8176 ,  'new' : 7205 ,  'is' : 6891 ,  'of' : 6867 ,  '||' : 6692 ,  'else' : 6457 ,  'for' : 6451 ,  '},' : 6407 ,  '*/' : 6166 ,  ':' : 5310 ,  '@param' : 5013 ,  '/**' : 4877 ,  'The' : 4650 ,  'in' : 4594 ,  '})' : 4373 ,  'and' : 4365 ,  '0;' : 4290 ,  'i' : 4269 ,  '-' : 4245 ,  '<' : 4209 ,  '!==' : 4051 ,  '?' : 4020 ,  ',' : 3543 ,  'function()' : 3530 ,  'module.exports' : 3251 ,  '+=' : 3149 ,  'not' : 3115 ,  '()' : 3084 ,  'case' : 3009 ,  'const' : 3005 ,  'that' : 2973 ,  'be' : 2962 ,  "'use" : 2945 ,  "strict';" : 2860 ,  'false;' : 2770 ,  '@returns' : 2626 ,  "'" : 2622 ,  'throw' : 2524 ,  'with' : 2520 ,  'true;' : 2481 ,  'an' : 2445 ,  'value' : 2427 ,  'this' : 2408 ,  '0,' : 2383 ,  'node' : 2349 ,  'or' : 2318 ,  '=>' : 2130 ,  'true' : 2101 ,  '0)' : 2059 ,  '==' : 1971 ,  'as' : 1863 ,  '>' : 1819 ,  'it' : 1797 ,  '(var' : 1794 ,  'false' : 1776 ,  '[' : 1738 ,  'are' : 1717 ,  'on' : 1701 ,  'object' : 1684 ,  '(typeof' : 1680 ,  'result' : 1642 ,  'from' : 1640 ,  'Returns' : 1549 ,  'null;' : 1518 ,  'we' : 1495 ,  'return;' : 1429 ,  'array' : 1412 ,  '0' : 1411 ,  '&' : 1388 ,  'true,' : 1381 ,  'cb)' : 1379 ,  'should' : 1346 ,  '[];' : 1297 ,  'path' : 1289 ,  'false,' : 1286 ,  'while' : 1273 ,  '(t)' : 1265 ,  'by' : 1256 ,  'options' : 1252 ,  'assert' : 1250 ,  'type:' : 1234 ,  'i++)' : 1224 ,  'null' : 1221 ,  'break;' : 1206 }

cplusplus = { '//' : 199606 ,  '=' : 124262 ,  '{' : 111007 ,  '}' : 88909 ,  'if' : 64362 ,  'the' : 51906 ,  'return' : 43217 ,  'void' : 37224 ,  'a' : 30266 ,  'to' : 27065 ,  'for' : 26911 ,  'const' : 24195 ,  'of' : 23185 ,  'case' : 22367 ,  'int' : 22043 ,  'is' : 21940 ,  '///' : 21211 ,  'CHECK:' : 21120 ,  '};' : 19450 ,  'struct' : 18760 ,  '<<' : 17860 ,  ':' : 16274 ,  '&&' : 16014 ,  '==' : 14989 ,  'in' : 12586 ,  '-' : 12579 ,  'bool' : 12567 ,  '|' : 11372 ,  '#pragma' : 11244 ,  'omp' : 11176 ,  'class' : 10844 ,  'be' : 10631 ,  'else' : 10245 ,  'and' : 9703 ,  'we' : 9492 ,  'template' : 9186 ,  'this' : 9093 ,  'not' : 8940 ,  '0;' : 8822 ,  'type' : 8759 ,  'that' : 8609 ,  'i' : 8592 ,  'an' : 8338 ,  '!=' : 8153 ,  '"' : 7998 ,  'break;' : 7894 ,  '%s' : 7870 ,  'i32' : 7804 ,  'static' : 7480 ,  'RUN:' : 7463 ,  'false;' : 7426 ,  '||' : 7402 ,  'true;' : 6999 ,  '<' : 6903 ,  'unsigned' : 6832 ,  '#include' : 6637 ,  'with' : 6401 ,  'A' : 6377 ,  '{}' : 6091 ,  'or' : 5921 ,  'call' : 5876 ,  'If' : 5820 ,  '+' : 5814 ,  'function' : 5757 ,  'T>' : 5603 ,  'are' : 5538 ,  'char' : 5196 ,  'return;' : 5176 ,  'it' : 5008 ,  'as' : 4992 ,  '(const' : 4839 ,  '0,' : 4756 ,  'auto' : 4615 ,  'This' : 4606 ,  'have' : 4539 ,  'x' : 4503 ,  'virtual' : 4421 ,  'QualType' : 4402 ,  'parallel' : 4196 ,  'The' : 4084 ,  'from' : 4052 ,  '0' : 3957 ,  'nullptr;' : 3866 ,  'I' : 3840 ,  '?' : 3834 ,  '+=' : 3792 ,  'new' : 3734 ,  'T' : 3715 ,  'define' : 3615 ,  '(int' : 3597 ,  'on' : 3348 ,  'typedef' : 3336 ,  'by' : 3225 ,  'using' : 3136 ,  '++i)' : 3085 ,  'FIXME:' : 3045 ,  '\\' : 3041 ,  'B' : 3030 ,  'here}}' : 3000 ,  'no' : 2971 }

java = { '*' : 1210449 ,  '{' : 528948 ,  '}' : 514962 ,  '=' : 502280 ,  'public' : 275248 ,  'if' : 250458 ,  '//' : 247750 ,  '+' : 246653 ,  'of' : 202305 ,  'new' : 168476 ,  '*/' : 161688 ,  'return' : 154957 ,  'import' : 146907 ,  'this' : 139987 ,  'for' : 129919 ,  'in' : 127396 ,  '/**' : 120508 ,  'int' : 116504 ,  'or' : 106119 ,  'static' : 98077 ,  'void' : 94196 ,  'long' : 92680 ,  '-' : 91282 ,  'private' : 89295 ,  'final' : 75071 ,  'String' : 70626 ,  'License' : 69417 ,  'file' : 68498 ,  '==' : 66954 ,  'as' : 61763 ,  'with' : 61703 ,  'throws' : 59790 ,  '"' : 58189 ,  'This' : 58094 ,  '@param' : 57635 ,  'version' : 54971 ,  '2' : 53643 ,  'not' : 53022 ,  'class' : 52927 ,  'Oracle' : 52747 ,  'Public' : 50763 ,  'General' : 50722 ,  'GNU' : 50546 ,  '!=' : 50292 ,  'you' : 48772 ,  'have' : 45625 ,  'null)' : 43881 ,  '/*' : 43251 ,  'under' : 42929 ,  'else' : 42409 ,  'OR' : 42040 ,  'copy' : 41799 ,  'throw' : 41101 ,  'code' : 40753 ,  'Software' : 39989 ,  'boolean' : 38913 ,  'and/or' : 34145 ,  'Free' : 33752 ,  'should' : 32797 ,  'See' : 31074 ,  'i' : 30391 ,  '0;' : 29606 ,  'null;' : 29416 ,  'on' : 29402 ,  '<' : 28757 ,  '@return' : 28212 ,  'more' : 28156 ,  'try' : 27776 ,  'value' : 27181 ,  'A' : 27036 ,  'any' : 26489 ,  'LICENSE' : 26334 ,  'its' : 26073 ,  'method' : 25543 ,  '&&' : 25201 ,  'ANY' : 23985 ,  'but' : 23840 ,  'case' : 23801 ,  'may' : 23670 ,  'catch' : 23583 ,  'You' : 23538 ,  'WITHOUT' : 23024 ,  '0,' : 22756 ,  ':' : 21751 ,  '@see' : 21701 }


ruby = { '#' : 16500 ,  'end' : 11966 ,  '=' : 10622 ,  'the' : 6374 ,  'def' : 5902 ,  'if' : 4075 ,  'to' : 3113 ,  'a' : 2810 ,  '=>' : 1978 ,  'is' : 1975 ,  'of' : 1921 ,  'do' : 1897 ,  'and' : 1699 ,  'for' : 1604 ,  '##' : 1434 ,  'in' : 1255 ,  'unless' : 1241 ,  'be' : 1238 ,  'require' : 1174 ,  'class' : 1150 ,  '<<' : 1140 ,  'else' : 1129 ,  '==' : 1128 ,  '}' : 1084 ,  'that' : 1039 ,  'true' : 1034 ,  'this' : 957 ,  'return' : 943 ,  '{' : 935 ,  'when' : 904 ,  'then' : 904 ,  '&&' : 902 ,  'gem' : 888 ,  'not' : 823 ,  'or' : 810 ,  'nil' : 761 ,  'raise' : 747 ,  'The' : 746 ,  'are' : 735 ,  '||' : 730 ,  'with' : 704 ,  'from' : 702 ,  'name' : 668 ,  'an' : 665 ,  '"' : 643 ,  ':nodoc:' : 615 ,  'module' : 614 ,  'will' : 580 ,  '<' : 571 ,  '[]' : 544 ,  'false,' : 542 ,  'as' : 537 ,  '||=' : 523 ,  'path' : 517 ,  'nil,' : 507 ,  'by' : 495 ,  'it' : 490 ,  'on' : 488 ,  'If' : 480 ,  'false' : 471 ,  'options' : 470 ,  'version' : 463 ,  ':' : 460 ,  '?' : 456 ,  'value' : 452 ,  'rescue' : 445 ,  'given' : 439 ,  'attr_reader' : 434 ,  'file' : 433 ,  'gems' : 432 ,  '+' : 427 ,  'you' : 427 ,  'spec' : 426 ,  'frozen_string_literal:' : 412 ,  'all' : 404 ,  'Returns' : 403 ,  'can' : 391 ,  'This' : 374 ,  '1' : 367 ,  'source' : 358 ,  '@return' : 354 ,  'command' : 331 ,  '-' : 329 ,  '\\' : 320 ,  '{}' : 303 ,  'begin' : 301 ,  'result' : 296 ,  'your' : 296 ,  'dependency' : 296 ,  'set' : 295 ,  'private' : 294 ,  'use' : 282 ,  'default' : 272 ,  'Bundler' : 270 ,  'used' : 264 ,  'new' : 264 ,  'elsif' : 263 ,  '=~' : 263 ,  '*' : 261 ,  'specs' : 260 }


perl = { '#' : 20217 ,  ';' : 13281 ,  '=' : 7507 ,  '{' : 6315 ,  '}' : 5833 ,  'LETTER' : 5626 ,  'my' : 5253 ,  'the' : 5172 ,  'CJK' : 5098 ,  'if' : 3953 ,  'LATIN' : 3229 ,  'to' : 3033 ,  'WITH' : 2987 ,  '=>' : 2438 ,  'SMALL' : 2250 ,  'is' : 2219 ,  'CAPITAL' : 2064 ,  'a' : 1945 ,  'and' : 1788 ,  'for' : 1766 ,  'of' : 1648 ,  'in' : 1543 ,  'print' : 1373 ,  '=~' : 1262 ,  'or' : 1115 ,  'sub' : 1083 ,  'MARK>' : 1035 ,  '(' : 1023 ,  ')' : 1016 ,  'use' : 974 ,  'that' : 951 ,  'KATAKANA' : 933 ,  'eq' : 883 ,  'be' : 869 ,  'unless' : 788 ,  '"' : 777 ,  'it' : 763 ,  'die' : 760 ,  'we' : 744 ,  'ACUTE' : 740 ,  'not' : 740 ,  'return' : 732 ,  'this' : 718 ,  'RADICAL' : 699 ,  'SOUND' : 696 ,  '##' : 685 ,  'U' : 684 ,  '.' : 679 ,  '-' : 668 ,  'AND' : 654 ,  '+' : 651 ,  'are' : 646 ,  'KANGXI' : 642 ,  '<LATIN' : 627 ,  'else' : 620 ,  '&&' : 606 ,  'ok' : 602 ,  ':' : 598 ,  'with' : 588 ,  'as' : 584 ,  'O' : 578 ,  ');' : 566 ,  '||' : 511 ,  '?' : 506 ,  'from' : 498 ,  'A' : 494 ,  'E' : 492 ,  'file' : 489 ,  'If' : 479 ,  'The' : 478 ,  'defined' : 470 ,  'VOICED' : 467 ,  'GRAVE' : 455 ,  'by' : 441 ,  'push' : 437 ,  'on' : 428 ,  'This' : 419 ,  'foreach' : 411 ,  'elsif' : 410 ,  'new' : 403 ,  '0;' : 403 ,  '1' : 403 ,  'will' : 402 ,  '*' : 400 ,  '1;' : 399 ,  '==' : 399 ,  'an' : 392 ,  'have' : 365 ,  '|' : 357 ,  'all' : 355 ,  'set' : 352 ,  'while' : 347 ,  '};' : 346 ,  '[' : 342 ,  'code' : 342 ,  'shift;' : 338 ,  '@_;' : 335 ,  'next' : 333 ,  '30FC' : 328 ,  'CARON' : 326 }

c = { '=' : 2676314 ,  '{' : 1368862 ,  '*' : 1254223 ,  '}' : 1051623 ,  'if' : 1022007 ,  '*/' : 854162 ,  '/*' : 807015 ,  'struct' : 703407 ,  'return' : 586933 ,  'int' : 542039 ,  'static' : 478685 ,  '0;' : 328241 ,  'for' : 229611 ,  '#include' : 227685 ,  '==' : 225465 ,  '&' : 223274 ,  '+' : 215075 ,  '0x00,' : 213429 ,  'void' : 211655 ,  'case' : 199378 ,  '#define' : 191776 ,  '},' : 187848 ,  'unsigned' : 181197 ,  'of' : 180900 ,  '-' : 178034 ,  '|' : 174062 ,  '0,' : 161034 ,  'else' : 158414 ,  '<' : 156471 ,  'break;' : 152386 ,  'goto' : 134425 ,  '};' : 129428 ,  'const' : 123385 ,  'in' : 121138 ,  '0)' : 115014 ,  'ret' : 112447 ,  '&&' : 107117 ,  '!=' : 104830 ,  'u32' : 98720 ,  '<<' : 96761 ,  'long' : 89361 ,  '|=' : 85573 ,  'char' : 84254 ,  'ret;' : 78141 ,  '||' : 76388 ,  '1;' : 73291 ,  'this' : 70846 ,  'u8' : 66476 ,  '1,' : 64523 ,  'on' : 63656 ,  '0);' : 62992 ,  'not' : 62199 ,  ':' : 61955 ,  'This' : 61835 ,  'i' : 61716 ,  'device' : 60665 ,  '>' : 60245 ,  'NULL;' : 59736 ,  '0' : 57635 ,  'or' : 56827 ,  '(i' : 55804 ,  'err' : 55224 ,  'with' : 53485 ,  '-EINVAL;' : 52526 ,  '\\' : 52301 ,  '+=' : 52252 ,  '?' : 47432 ,  '>>' : 47102 ,  'as' : 45980 ,  'return;' : 45190 ,  'NULL,' : 44293 ,  'err;' : 41835 ,  '#endif' : 41806 ,  'data' : 41289 ,  '"' : 40969 ,  '1' : 40800 ,  'i++)' : 40540 ,  'switch' : 40141 ,  '/**' : 39990 ,  'while' : 37648 ,  '>=' : 37432 ,  '&=' : 36354 ,  'i;' : 35563 ,  'flags);' : 34566 ,  '1);' : 34558 }


typescript = { '{' : 64204 ,  '}' : 49367 ,  '=' : 46513 ,  '//' : 27202 ,  'var' : 23998 ,  '////' : 14690 ,  'return' : 14608 ,  'function' : 13574 ,  'if' : 10678 ,  '=>' : 10547 ,  'export' : 8282 ,  'class' : 7461 ,  'const' : 7319 ,  'new' : 5238 ,  'of' : 5033 ,  '===' : 4939 ,  'extends' : 4572 ,  'x' : 4456 ,  '};' : 4248 ,  'case' : 4161 ,  'public' : 4046 ,  '+' : 4018 ,  'for' : 3891 ,  'string;' : 3661 ,  'type' : 3489 ,  '()' : 3469 ,  'let' : 3417 ,  'module' : 3297 ,  'number;' : 3209 ,  'in' : 3187 ,  '&&' : 3170 ,  ':' : 3070 ,  'error' : 3000 ,  '|' : 2984 ,  '*' : 2956 ,  'x:' : 2838 ,  'string' : 2586 ,  '},' : 2574 ,  'number' : 2471 ,  '||' : 2362 ,  'static' : 2344 ,  'true' : 2206 ,  'string,' : 2183 ,  '});' : 2182 ,  'x;' : 2182 ,  'else' : 2172 ,  '1;' : 2171 ,  'private' : 2171 ,  '////}' : 2171 ,  'declare' : 2105 ,  '0;' : 2086 ,  'y' : 1992 ,  '?' : 1934 ,  'y:' : 1920 ,  '<' : 1853 ,  'i' : 1801 ,  'as' : 1797 ,  'number,' : 1792 ,  '-' : 1769 ,  'import' : 1741 ,  'C' : 1732 ,  'not' : 1664 ,  'A' : 1633 ,  'with' : 1606 ,  'typeof' : 1601 ,  'this' : 1562 ,  'number)' : 1543 ,  '!==' : 1535 ,  'a:' : 1533 ,  '////var' : 1478 ,  'T;' : 1443 ,  '*/' : 1425 ,  'b' : 1419 ,  '&' : 1407 ,  'string):' : 1383 ,  'T)' : 1377 ,  'number):' : 1350 ,  '/>' : 1339 ,  'null;' : 1329 ,  '///' : 1315 ,  'this;' : 1298 ,  'any)' : 1295 ,  '/**' : 1292 ,  'ok' : 1292 ,  'kind:' : 1288 ,  'get' : 1260 ,  'void;' : 1243 ,  'text:' : 1224 ,  '1' : 1209 ,  'string)' : 1208 }


classifiers = [cplusplus, javascript, java, c, ruby, perl, typescript, python, scala]
classes = ["C++", "JavaScript", "Java", "C", "Ruby", "Perl", "TypeScript", "Python", "Scala"]

# Normalize classifiers

for i in range(0, len(classifiers)):
    total = reduce(lambda x,y: x+y, classifiers[i].values())
    for j in classifiers[i].keys():
        classifiers[i][j] = float(classifiers[i][j]) / total

# print classifiers

# Load up input file to be classified.

counts = {}
total = 0
with open('/dev/stdin', 'r') as f:
    wordgen = words(f)
    for word in wordgen:
        counts[word] = counts.get(word, 0) + 1
        total = total + 1

# Naive Bayes
# Bayes:
#  P(hypothesis_k true | evidence) = P(hypothesis_k true) * P(evidence | hypothesis_k true) / P(evidence)
#           posterior = prior * likelihood / evidence
# Naive Bayes:
#      ignore evidence as it is the same for all
#      => posterior ~ prior * likelihood
#
#      prior = #(hypothesis_k) / #(all hypotheses)
#      likelihood = P(evidence | hypothesis_k true)
#
#      assume independence of outcomes
#      now we just multiply prior * likelihood and find the argmax for k

# for multinomials:
#   argmax_k log prior + sum_i (evidence_i * log Pr(hypothesis_k[i]))

argmax = 0
max = float('-inf')

for i in xrange(0,len(classifiers)):
    val = 0

    counted = 0
    for word in sorted(counts, key=counts.get, reverse=True):
        c = classifiers[i].get(word, 0.0001)
        val = val + counts[word] * math.log(c)
        counted = counted + 1
    # val = val + math.log(prior[i])

    # val = val / math.sqrt(counted)
    if val > max:
        max = val
        argmax = i

print classes[argmax]

