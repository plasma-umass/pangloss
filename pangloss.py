#!/usr/bin/env python

# pangloss
# Language detector for files.
# Copyright (C) 2016-2018 by Emery Berger <http://emeryberger.com>
#
# This language detector works by examining source contents and
# only uses file extensions as a hint. Based on a learned model
# from corpora of programs.
#
# Usage:
#   pangloss filename.ext

# Currently supports the following languages:

classes = ["C++", "JavaScript", "Java", "C", "Ruby", "Perl", "TypeScript", "Python", "Scala", "PHP", "Objective-C"]

# Each extension corresponds to the classifier above.
# We incorporate extension info as a weak prior, below.
extensions = [[".cpp", ".hpp", ".hh", ".cc", ".cxx", ".hxx", ".C"],
              [".js"],
              [".java"],
              [".c",".h"],
              [".rb"],
              [".pl",".pm"],
              [".ts"],
              [".py"],
              [".scala"],
              [".php"],
              [".m"]]

extensionPrior = 1.1 # 10% more likely if it has the given suffix

import os
import sys
import csv
import math
from itertools import tee, islice
import collections

if len(sys.argv) < 2:
    print "pangloss determines the programming language a file is written in."
    print "Usage: pangloss filename"
    sys.exit(1)

fname = sys.argv[1]
ext   = os.path.splitext(fname)[1]

def oldwords(fileobj):
    for line in fileobj:
        for word in line.split():
            yield word

# Break into conjoined bigrams.
def oldwords2(fileobj):
    wprev = None
    for line in fileobj:
        for w in line.split():
            if wprev is not None:
                yield wprev+":"+w
            else:
                yield w
            wprev = w


def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break
  
def wordsn(fileobj,n,skip=0):
    frequencies = collections.Counter([])
    words = fileobj.read().split()
#    print words
#    print words[::skip+1]
    words = words + words[::skip+1]
#    words += words[::skip+1]
    return ngrams(words, n)
            
java = { ('}', 'public') : 1755116 ,  ('}', '}') : 1512514 ,  ('{', 'return') : 1201231 ,  ('=', 'new') : 1160039 ,  ('public', 'void') : 937358 ,  ('{', '}') : 586614 ,  ('{', 'if') : 570069 ,  ('public', 'static') : 502202 ,  ('}', 'else') : 458422 ,  ('static', 'final') : 418012 ,  ('null)', '{') : 397104 ,  ('}', 'package') : 380115 ,  ('{', '=') : 364740 ,  ('@Override', 'public') : 364445 ,  ('}', '@Override') : 360661 ,  ('}', 'return') : 358259 ,  ('}', 'private') : 329425 ,  ('public', '{') : 325356 ,  ('"', '+') : 316374 ,  (')', '{') : 315284 ,  ('public', 'class') : 299588 ,  ('else', '{') : 290227 ,  ('!=', 'null)') : 285136 ,  ('try', '{') : 280059 ,  ('}', 'if') : 277597 ,  ('}', 'catch') : 273511 ,  ('public', 'String') : 270237 ,  ('=', '0;') : 261204 ,  ('{', 'public') : 252735 ,  ('throw', 'new') : 248478 ,  ('private', 'static') : 242275 ,  ('==', 'null)') : 240799 ,  ('=', 'null;') : 235567 ,  ('final', '=') : 214808 ,  ('return', 'public') : 214220 ,  ('final', 'String') : 202831 ,  ('e)', '{') : 197175 ,  ('=', '=') : 194048 ,  ('{', 'throw') : 190158 ,  ('public', 'boolean') : 187109 ,  ('}', 'protected') : 182725 ,  ('{', 'private') : 175387 ,  ('final', 'int') : 172539 ,  ('else', 'if') : 169217 ,  ('+', '"') : 167411 ,  ('}', 'void') : 165084 ,  (');', '}') : 164577 ,  ('null;', '}') : 160751 ,  ('public', 'int') : 158668 ,  ('for', '(int') : 152377 ,  ('if', '(') : 149089 ,  ('return', 'new') : 148071 ,  ('if', 'null)') : 143454 ,  ('void', '{') : 143230 ,  ('{', 'String') : 141316 ,  ('i', '=') : 136321 ,  ('Exception', '{') : 134807 ,  ('return', 'null;') : 133145 ,  ('return', '}') : 129867 ,  ('throws', 'Exception') : 129831 ,  ('false;', '}') : 129419 ,  ('return', 'false;') : 128047 ,  ('{', 'final') : 127924 ,  ('private', 'final') : 127801 ,  ('true;', '}') : 123833 ,  ('!=', 'null') : 122072 ,  ('{', 'int') : 119797 ,  ('}', 'import') : 118601 ,  ('i', '<') : 114619 ,  ('protected', 'void') : 109929 ,  ('private', 'void') : 109608 ,  ('result', '=') : 108693 ,  ('{', 'try') : 107842 ,  ('0)', '{') : 107539 ,  ('IOException', '{') : 107026 ,  ('=', 'false;') : 104729 ,  ('public', 'final') : 104245 ,  ('if(targetEditPart', 'instanceof') : 103679 ,  ('private', 'String') : 103653 ,  ('}', 'if(targetEditPart') : 103412 ,  ('0;', 'i') : 101131 ,  ('=', 'true;') : 99256 ,  ('{', '{') : 97998 ,  ('return', 'true;') : 97833 ,  ('i++)', '{') : 96404 ,  ('(int', 'i') : 95738 ,  ('throws', 'IOException') : 94266 ,  ('=', '}') : 93898 ,  ('==', 'null') : 92355 ,  ('=', 'public') : 88722 ,  ('null', '&&') : 84067 ,  ('break;', 'case') : 83632 ,  ('@Test', 'public') : 81926 ,  ('catch', '{') : 81012 ,  ('private', 'private') : 79942 ,  ('import', 'java.util.List;') : 79853 ,  ('import', 'class') : 77587 ,  (')', ');') : 76489 ,  ('return;', '}') : 76482 ,  ('static', 'void') : 75838 ,  ('}', '{') : 74032 ,  ('{', 'for') : 73815 ,  ('}', '@Test') : 73383 ,  ('}', '=') : 71968 ,  ('=', 'static') : 70491 ,  ('java.util.List;', 'import') : 69393 ,  ('private', 'int') : 69176 ,  ('static', 'String') : 68327 ,  ('=', '{') : 68164 ,  ('@Override', 'protected') : 65655 ,  ('public', 'extends') : 65051 ,  ('{', '@Override') : 62024 ,  ('value)', '{') : 61666 ,  ('break;', '}') : 61113 ,  ('{', 'new') : 59059 ,  ('{', 'case') : 58245 ,  ('private', 'boolean') : 58226 ,  ('catch', '(Exception') : 57704 ,  ('}', '});') : 57403 ,  ('0,', '0,') : 57204 ,  ('}', 'String') : 56804 ,  ('{', '==') : 56200 ,  ('}', 'static') : 55261 ,  ('import', 'static') : 55201 ,  ('}', 'e)') : 53936 ,  ('public', 'throws') : 53647 ,  ('String', 'return') : 52802 ,  ('import', 'java.io.IOException;') : 52790 ,  ('java.io.IOException;', 'import') : 52613 ,  ('public', 'Object') : 51616 ,  (')', ')') : 51006 ,  ('java.util.ArrayList;', 'import') : 50876 ,  ('}', 'finally') : 50489 ,  ('finally', '{') : 49927 ,  ('=', 'if') : 49704 ,  ('import', 'java.util.ArrayList;') : 48239 ,  ('j', '=') : 48155 ,  ('final', 'static') : 47623 ,  ('=', '<') : 47418 ,  ('for', '=') : 47301 ,  ('static', 'class') : 46599 ,  ('==', '0)') : 46328 ,  ('=', '1;') : 46082 ,  ('}', 'int') : 45784 ,  ('result;', '}') : 45380 ,  ('>', '0)') : 44893 ,  ('}', 'final') : 44550 ,  ('public', 'abstract') : 44528 ,  ('null', ')') : 44488 ,  ('public', 'interface') : 44253 ,  ('return', 'result;') : 44168 ,  ('null', '||') : 43220 ,  ('return', '@Override') : 42651 ,  ('new', '}') : 42542 ,  ('import', 'java.util.Map;') : 42427 ,  ('}', 'boolean') : 42256 ,  ('(Exception', 'e)') : 42062 ,  ('final', 'long') : 41047 ,  ('static', 'int') : 40676 ,  ('}', '};') : 40427 ,  ('private', '=') : 38907 ,  ('=', '4;') : 38707 ,  ('<', '{') : 38518 ,  ('null', '?') : 38231 ,  ('java.util.Map;', 'import') : 35854 ,  ('i', 'i') : 35797 ,  ('0;', '}') : 35781 ,  ('if(targetEditPart', '{') : 35500 ,  ('{', 'if(targetEditPart') : 35214 ,  ('e);', '}') : 34812 ,  ('(int', '0;') : 34671 ,  (');', 'if') : 34579 ,  ('j', 'j') : 34260 ,  ('{', '!=') : 34155 ,  ('protected', 'String') : 33991 ,  ('new', 'public') : 33894 ,  ('for', ':') : 33888 ,  ('value', '=') : 33414 ,  ('{', 'boolean') : 33383 ,  ('return', 'private') : 33265 ,  ('}', 'for') : 33235 ,  ('null);', '}') : 32797 ,  ('catch', '(IOException') : 32540 ,  ('static', '=') : 32279 ,  ('}', 'break;') : 32092 ,  ('{', 'return;') : 31832 ,  ('static', 'boolean') : 31794 ,  ('value;', '}') : 31746 ,  ('+', '}') : 31612 ,  ('{', 'void') : 31435 ,  ('if', '0)') : 30531 ,  ('{', 'protected') : 30442 ,  ('4;', 'j') : 30406 ,  ('+', '+') : 30125 ,  ('}', 'try') : 29955 ,  ('=', 'final') : 29786 ,  ('null)', '=') : 29691 ,  ('ex)', '{') : 29453 ,  ('this;', '}') : 29442 ,  ('node)', '{') : 29398 }

perl = { ('=>', "'sub") : 23745 ,  ('{', 'my') : 19314 ,  ('=', 'shift;') : 8691 ,  ('=', '@_;') : 8658 ,  (')', '{') : 8256 ,  ('=>', '{') : 7596 ,  ("}',", "'sub") : 6676 ,  ('$self', '=') : 5813 ,  ('my', '$self') : 5661 ,  ('}', '}') : 4823 ,  ("'sub", 'my') : 4722 ,  ('{', '=') : 4482 ,  ('shift;', 'my') : 4418 ,  ('if', '(') : 4364 ,  ('}', 'else') : 4312 ,  ('{', 'return') : 4275 ,  ('else', '{') : 4269 ,  ('=', '{') : 3635 ,  (')', '=') : 3477 ,  ('$VAR1', '=') : 3298 ,  ('@_;', 'my') : 3268 ,  ('}', 'return') : 3129 ,  ('my', '(') : 2980 ,  ('my', 'shift;') : 2832 ,  ('};', '$VAR1') : 2813 ,  ('}', 'if') : 2551 ,  ("}'", '};') : 2529 ,  ('}', 'elsif') : 2479 ,  (');', '}') : 2428 ,  ('my', '($self,') : 2379 ,  ('}', "}',") : 2314 ,  ('{', 'if') : 2306 ,  ('}', 'my') : 2285 ,  ('sub', '{') : 1952 ,  (');', "}',") : 1949 ,  ('=>', '=>') : 1798 ,  ('@_;', 'return') : 1715 ,  ('=', '=') : 1690 ,  ('=', '0;') : 1684 ,  ('for', 'my') : 1647 ,  ('shift;', 'return') : 1407 ,  ('=', '(') : 1380 ,  ('foreach', 'my') : 1345 ,  ('=', '1;') : 1341 ,  ('return', 'if') : 1320 ,  ('=', '=>') : 1302 ,  ('shift;', '=') : 1292 ,  ('}', '=') : 1221 ,  ('map', '{') : 1216 ,  ('unless', 'defined') : 1209 ,  (');', 'my') : 1061 ,  ('my', '=') : 1045 ,  (')', ')') : 1013 ,  ('};', '{') : 989 ,  (');', 'return') : 987 ,  ('{', 'push') : 968 ,  ('(', '$self,') : 946 ,  ('{', "'sub") : 905 ,  ('$self', 'my') : 902 ,  ('@_;', '=') : 891 ,  ('{', '}') : 881 ,  ('elsif', '(') : 865 ,  ('$class', '=') : 858 ,  ('1;', '}') : 832 ,  ('(', ')') : 828 ,  ('return', 'unless') : 823 ,  ('if', 'defined') : 821 ,  ("}'", '=') : 819 ,  ('=', 'my') : 814 ,  ('my', '$class') : 812 ,  ('=', '{};') : 801 ,  ('{', 'require') : 779 ,  ('eval', '{') : 763 ,  ('=>', 'sub') : 732 ,  ('@_;', 'if') : 728 ,  ('=', 'sub') : 714 ,  ('(', '{') : 700 ,  ('=', 'shift') : 699 ,  ('return;', "}',") : 676 ,  (')', 'if') : 666 ,  ('return', '$self;') : 665 ,  ('($self)', '=') : 660 ,  ('my', '($self)') : 660 ,  ('=', "\\'\\';") : 658 ,  (');', '=>') : 655 ,  ('};', '}') : 652 ,  ("'new'", '=>') : 641 ,  ('new', '{') : 638 ,  ("'sub", 'new') : 636 ,  ('}', '=>') : 632 ,  ('grep', '{') : 627 ,  ('return', '1;') : 627 ,  ('my', '@_;') : 622 ,  ('=', 'map') : 617 ,  ('or', 'die') : 614 ,  ('$self;', "}',") : 609 ,  ('}', '{') : 606 ,  ('next', 'if') : 602 ,  ('"', '.') : 602 ,  (')', 'or') : 602 ,  ('(', 'my') : 601 ,  ('return;', '}') : 599 ,  ("'sub", 'return') : 591 ,  ('=', '}') : 587 ,  ('=', 'if') : 575 ,  ('()', '{') : 573 ,  ('=', 'delete') : 568 ,  (');', 'if') : 550 ,  ('};', "}',") : 547 ,  ('if', '(defined') : 542 ,  ('shift;', 'if') : 538 ,  ('unless', '(') : 537 ,  ('=>', '[') : 537 ,  ('{', 'next') : 527 ,  ('0;', 'my') : 525 ,  ('1', 'if') : 520 ,  ('$name', '=') : 520 ,  ('{', "}',") : 514 ,  ("}',", "'new'") : 514 ,  ('{};', '$VAR1') : 508 ,  ("'BEGIN", '{') : 508 ,  ("'BEGIN'", '=>') : 507 ,  ('(', 'defined') : 506 ,  ('=>', "'BEGIN") : 506 ,  ('0;', '}') : 502 ,  ('my', '$name') : 495 ,  ('{', 'local') : 494 ,  ('}', ')') : 491 ,  ('or', 'return;') : 490 ,  ('{', 'croak') : 486 ,  ('};', 'my') : 483 ,  ('=>', '1,') : 482 ,  ('1;', "}',") : 481 ,  (')', ');') : 481 ,  ('{', 'die') : 478 ,  ('{', '$_') : 476 ,  ('($self,', '@_;') : 472 ,  ('my', '{') : 471 ,  ('or', 'return') : 466 ,  ('}', ');') : 462 ,  ('=', 'defined') : 456 ,  ('}', 'return;') : 455 ,  ('return', 'undef;') : 452 ,  ('if', 'not') : 447 ,  ('next', 'unless') : 447 ,  ('return', '0;') : 443 ,  ('{', 'print') : 440 ,  ('return', '1') : 431 ,  ('name', '=>') : 431 ,  ('return', 'undef') : 423 ,  ('or', 'croak') : 416 ,  ('and', 'return') : 415 ,  ('while', '(') : 414 ,  ('1', ':') : 403 ,  ('=', '1') : 403 ,  ('(', '=') : 402 ,  ('return', '(') : 397 ,  ('$type', '=') : 396 ,  (')', '}') : 396 ,  ('do', '{') : 387 ,  (')', ':') : 385 ,  ('$data', '=') : 384 ,  ('if', '(my') : 382 ,  ("}',", "'BEGIN'") : 382 ,  (')', 'my') : 379 ,  ('=', '[') : 379 ,  ('$_', '}') : 377 ,  ('$value', '=') : 376 ,  ('?', '1') : 375 ,  ('else', '=') : 372 ,  ('=', 'return') : 372 ,  ('$data', '.=') : 372 ,  ('}', 'push') : 371 ,  ('return', '0') : 370 ,  ('no', 'strict') : 364 ,  ("'_new_instance'", '=>') : 360 ,  ('_new_instance', '{') : 360 ,  ("'sub", '_new_instance') : 360 ,  ("'has_dst_changes'", '=>') : 359 ,  ("'sub", 'has_dst_changes') : 359 ,  ('spans', '=>') : 359 ,  ("'sub", 'olson_version') : 358 ,  ('return', 'shift->_init(') : 358 ,  ('$spans', ');') : 358 ,  ('shift->_init(', '@_,') : 358 ,  ('=>', '$spans') : 358 ,  ('@_,', 'spans') : 358 ,  ("'sub", '_max_year') : 358 ,  ("'olson_version'", '=>') : 358 ,  (')', '(') : 358 ,  ("'_max_year'", '=>') : 358 ,  ('if', ')') : 357 ,  ('if', '{') : 356 ,  ('{', 'warn') : 355 ,  ('$VAR1', '$VAR1') : 353 ,  ('$_', '=') : 350 ,  ('=', 'undef;') : 349 ,  ('my', '$type') : 348 ,  ('for', '(') : 345 ,  ('=', '();') : 345 }



c = { '}:static' : 218828 ,  '{:struct' : 197046 ,  '=:0;' : 196930 ,  '*:*' : 162636 ,  '=:{' : 151832 ,  '/*:*' : 151079 ,  'static:int' : 150986 ,  '0x00,:0x00,' : 130730 ,  '}:/*' : 122819 ,  'return:0;' : 121885 ,  'static:void' : 115199 ,  '},:{' : 107871 ,  'ret:=' : 107363 ,  '*/:if' : 105322 ,  '0;:}' : 105037 ,  '}:}' : 98845 ,  '{:if' : 87991 ,  '*/:static' : 86938 ,  '}:else' : 86180 ,  'break;:case' : 77239 ,  '}:if' : 76105 ,  'unsigned:int' : 73040 ,  '{:/*' : 72105 ,  '};:static' : 71375 ,  'unsigned:long' : 65627 ,  'of:the' : 65616 ,  'static:struct' : 60434 ,  'else:{' : 58814 ,  'const:struct' : 57883 ,  '{:int' : 57876 ,  'static:const' : 56393 ,  '}:return' : 53583 ,  'err:=' : 49978 ,  '<:0)' : 48311 ,  'return:ret;' : 48283 ,  '(i:=' : 47022 ,  'for:(i' : 47005 ,  'i:<' : 44434 ,  '=:NULL;' : 43966 ,  '0):{' : 43033 ,  'return:-EINVAL;' : 42382 ,  '*:This' : 42070 ,  '0;:i' : 41079 ,  '*/:#define' : 40753 ,  'else:if' : 40464 ,  '=:1;' : 40373 ,  '/**:*' : 39273 ,  'break;:}' : 38525 ,  'in:the' : 37222 ,  'to:the' : 37047 ,  '{:case' : 36233 ,  '0,:0,' : 34590 ,  'ret;:}' : 33929 ,  '*/:/*' : 33109 ,  '{:return' : 32270 ,  'the:*' : 32003 ,  '0x00,:/*' : 30306 ,  '.name:=' : 30078 ,  'if:(ret)' : 29886 ,  'General:Public' : 29825 ,  'goto:out;' : 28835 ,  '{:unsigned' : 28358 ,  'GNU:General' : 28231 ,  '==:0)' : 28219 ,  'i++):{' : 28046 ,  '}:/**' : 27869 ,  'Public:License' : 26656 ,  'rc:=' : 26351 ,  '*/:0x00,' : 26099 ,  'if:(ret' : 26053 ,  '*:Copyright' : 26043 ,  'const:char' : 25912 ,  'the:GNU' : 24864 ,  'int:ret;' : 24230 ,  '*:the' : 23952 ,  'int:i;' : 23075 ,  '*/:{' : 22883 ,  '{:.name' : 22607 ,  '=:0,' : 22236 ,  '0):return' : 22206 ,  'return:err;' : 21668 ,  '},:/*' : 21208 ,  'This:program' : 21019 ,  'program:is' : 21004 ,  'for:the' : 20867 ,  '-EINVAL;:}' : 20573 ,  'return:-ENOMEM;' : 20469 ,  '=:(struct' : 20348 ,  'static:inline' : 20336 ,  '*/:#include' : 20181 ,  'break;:default:' : 19984 ,  'GFP_KERNEL);:if' : 19759 ,  '}:void' : 19677 ,  'to:be' : 19335 ,  'return;:}' : 18702 ,  '(1:<<' : 18555 ,  '0;:if' : 18156 ,  '*/:int' : 17998 ,  'by:the' : 17969 ,  'status:=' : 17695 }

cplusplus = { '}:}' : 26899 ,  '}://' : 26189 ,  '//://' : 22573 ,  '=:0;' : 22553 ,  '//:CHECK-NEXT:' : 21631 ,  '//:CHECK:' : 21006 ,  '{://' : 19971 ,  '):{' : 18634 ,  '{:return' : 16505 ,  '}:void' : 15873 ,  'std::cout:<<' : 15584 ,  '{:if' : 14189 ,  '}:else' : 13638 ,  '":<<' : 12759 ,  '<<:std::endl;' : 11954 ,  'i:=' : 11316 ,  'copy:at' : 11084 ,  'Software:License,' : 10945 ,  'Boost:Software' : 10912 ,  'or:copy' : 10872 ,  'Version:1.0.' : 10764 ,  'License,:Version' : 10645 ,  '#pragma:omp' : 10620 ,  'the:Boost' : 9895 ,  'LICENSE_1_0.txt:or' : 9806 ,  'of:the' : 9671 ,  'accompanying:file' : 9631 ,  '//:expected-error' : 9613 ,  'under:the' : 9554 ,  '(See:accompanying' : 9392 ,  '//:Copyright' : 9245 ,  'i:<' : 9244 ,  'else:{' : 8950 ,  '{:int' : 8698 ,  'to:the' : 8332 ,  'const:{' : 8291 ,  '1.0.:(See' : 8006 ,  'file:LICENSE_1_0.txt' : 7744 ,  '0;:i' : 7680 ,  'Distributed:under' : 7643 ,  '<<:"' : 7625 ,  '>::value),:0);' : 7514 ,  '//:RUN:' : 7439 ,  'return:false;' : 7076 ,  ');:}' : 6952 ,  'using:namespace' : 6831 ,  '}:return' : 6743 ,  '0;:}' : 6499 ,  '}:};' : 6383 ,  'break;:case' : 6166 ,  '{:typedef' : 6085 ,  'return:0;' : 5981 ,  'else:if' : 5950 ,  '}:if' : 5878 ,  'for:(int' : 5800 ,  '0);:BOOST_CHECK_INTEGRAL_CONSTANT((::boost::BOOST_TT_TRAIT_NAME<' : 5656 ,  '}:{' : 5610 ,  '}:int' : 5591 ,  '=:{' : 5493 ,  'return:true;' : 5422 ,  'int:main()' : 5368 ,  '//:Distributed' : 5339 ,  '=:false;' : 5305 ,  '};:struct' : 5230 ,  'main():{' : 5217 ,  'in:the' : 5210 ,  '{:}' : 5124 ,  '//:This' : 5100 ,  'at:http://www.boost.org/LICENSE_1_0.txt)' : 4934 ,  'Copyright:(c)' : 4888 ,  'template:<typename' : 4797 ,  'true;:}' : 4797 ,  'template:<class' : 4785 ,  '&:>::value),' : 4726 ,  'the://' : 4629 ,  '//:If' : 4627 ,  '=:true;' : 4615 ,  'RUN::%clang_cc1' : 4602 ,  'const:&,' : 4417 ,  'at://' : 4351 ,  '{:const' : 4278 ,  '//:The' : 4263 ,  'false;:}' : 4257 ,  'break;:}' : 4255 ,  '//:expected-note' : 4255 ,  'http://www.boost.org/LICENSE_1_0.txt)://' : 4006 ,  '=:new' : 3943 ,  '}:bool' : 3857 ,  'cout:<<' : 3842 ,  'subject:to' : 3838 ,  'omp:parallel' : 3835 ,  '};://' : 3791 ,  'modification:and' : 3741 ,  '=:1;' : 3736 ,  'is:a' : 3686 ,  '}:namespace' : 3665 ,  '}:///' : 3658 ,  'Use,:modification' : 3643 ,  'const:char' : 3558 ,  '//:http://www.boost.org/LICENSE_1_0.txt)' : 3523 }

java = { '*:*' : 158857 ,  '}:}' : 121993 ,  '/**:*' : 105900 ,  '=:new' : 94876 ,  'of:the' : 92008 ,  '{:return' : 85075 ,  '*/:public' : 72472 ,  'public:long' : 68378 ,  '}:/**' : 68314 ,  'in:the' : 67678 ,  '}:public' : 62930 ,  '+://' : 57535 ,  '*:@param' : 57478 ,  '{:if' : 54654 ,  'to:the' : 52857 ,  'public:void' : 51027 ,  'the:GNU' : 50541 ,  'GNU:General' : 50541 ,  'General:Public' : 50541 ,  'Public:License' : 50440 ,  '*:This' : 44345 ,  '}:else' : 43883 ,  'public:static' : 42357 ,  'null):{' : 40847 ,  '":+' : 40329 ,  'static:final' : 40097 ,  'under:the' : 35590 ,  'throw:new' : 35410 ,  'code:is' : 34078 ,  'This:code' : 33923 ,  'version:2' : 33742 ,  'the:Free' : 33729 ,  'License:version' : 33728 ,  'Free:Software' : 33728 ,  '/*:*' : 30691 ,  '=:0;' : 30440 ,  'private:static' : 30169 ,  '!=:null)' : 29659 ,  'See:the' : 29509 ,  'else:{' : 29493 ,  '{://' : 28643 ,  '*:@return' : 27839 ,  'try:{' : 27746 ,  'file:that' : 26458 ,  '}:return' : 26303 ,  'accompanied:this' : 26293 ,  'the:LICENSE' : 26292 ,  'LICENSE:file' : 26292 ,  '*:or' : 25934 ,  '}:if' : 25719 ,  'by:the' : 25690 ,  'will:be' : 25191 ,  '{:throw' : 24673 ,  'the:*' : 24620 ,  'with:this' : 24577 ,  '}:catch' : 24405 ,  '==:null)' : 24066 ,  'copy:of' : 23849 ,  'a:copy' : 23653 ,  'is:distributed' : 23006 ,  'additional:information' : 22855 ,  '}:/*' : 22842 ,  '}:private' : 22081 ,  '}://' : 22039 ,  '=:null;' : 22024 ,  'IOException:{' : 21626 ,  '*:@see' : 21557 ,  '@Override:public' : 21225 ,  'for:the' : 21212 ,  'or:*' : 20788 ,  'for:(int' : 20701 ,  'throws:IOException' : 20261 ,  '}:@Override' : 19334 ,  'that:*' : 19239 ,  'i:=' : 18608 ,  'the:License' : 18473 ,  'e):{' : 18212 ,  'as:*' : 18199 ,  'that:it' : 18040 ,  'final:int' : 17949 ,  'it:will' : 17896 ,  'it:*' : 17798 ,  'should:have' : 17615 ,  'any:*' : 17557 ,  'for:more' : 17494 ,  '*:You' : 17335 ,  'public:class' : 17309 ,  '*/:package' : 17289 ,  '*:Copyright' : 17280 ,  'DO:NOT' : 17211 ,  'if:you' : 17150 ,  '*:Please' : 17132 ,  'you:can' : 17118 ,  'terms:of' : 17111 ,  'write:to' : 17092 ,  'included:in' : 17080 ,  'All:rights' : 17071 ,  'rights:reserved.' : 17071 ,  'Software:Foundation.' : 17066 ,  'FOR:A' : 17056 }

javascript = { '{:var' : 10167 ,  '{:return' : 7987 ,  '{:if' : 7189 ,  '}:}' : 5861 ,  '}:else' : 5098 ,  '*:@param' : 4976 ,  '*:*' : 4961 ,  '/**:*' : 4351 ,  '=:function' : 4056 ,  '=:0;' : 3370 ,  '{://' : 3364 ,  'function():{' : 3353 ,  'else:{' : 3344 ,  '}://' : 3265 ,  'module.exports:=' : 3246 ,  '}:function' : 3218 ,  '=:new' : 3175 ,  '}:return' : 3066 ,  '}:if' : 3040 ,  "'use:strict';" : 2847 ,  '():{' : 2815 ,  '*/:function' : 2656 ,  '*:@returns' : 2624 ,  '}:var' : 2554 ,  '=:{' : 2508 ,  'else:if' : 1963 ,  '*://' : 1917 ,  '=:true;' : 1839 ,  'function:()' : 1820 ,  'i:<' : 1818 ,  'for:(var' : 1780 ,  'i:=' : 1763 ,  'of:the' : 1755 ,  '}:/**' : 1645 ,  '//:=>' : 1609 ,  '=:false;' : 1559 ,  'if:(typeof' : 1514 ,  "':+" : 1453 ,  '0;:i' : 1377 ,  '},:{' : 1355 ,  'throw:new' : 1313 ,  '(var:i' : 1304 ,  '}:};' : 1294 ,  '(t):{' : 1264 ,  'function:(t)' : 1251 ,  '});:}' : 1237 ,  '});:});' : 1199 ,  'assert:=' : 1195 ,  '{:throw' : 1177 ,  "strict';:var" : 1132 ,  '=:function()' : 1128 ,  '0):{' : 1125 ,  "=:require('assert');" : 1093 ,  '*/:var' : 1091 ,  'in:the' : 1075 ,  'return:false;' : 1072 ,  '=:[];' : 1068 ,  '}):})' : 1024 ,  'common:=' : 997 ,  'i++):{' : 978 ,  'return;:}' : 978 ,  '=:null;' : 976 ,  'Returns:the' : 942 ,  't.end():})' : 918 ,  '{:name:' : 910 ,  'var:assert' : 896 ,  '};:/**' : 893 ,  "};:'use" : 871 ,  'result:=' : 870 ,  '};:}' : 855 ,  '*:@private' : 843 ,  'cb):{' : 835 ,  'to:the' : 829 ,  'is:a' : 827 ,  'try:{' : 809 ,  "require('../common');:var" : 808 ,  'false;:}' : 804 ,  '*:@memberOf' : 797 ,  '}:});' : 792 ,  '*:@example' : 764 ,  '@example:*' : 764 ,  'var:common' : 761 ,  '//://' : 733 ,  '_:*' : 731 ,  'true;:}' : 728 ,  '@memberOf:_' : 725 ,  '*:@category' : 724 ,  '*:@since' : 722 ,  '{:type:' : 717 ,  '*:@static' : 708 ,  '@static:*' : 708 ,  '}:catch' : 697 ,  '}:module.exports' : 696 ,  "+:'" : 695 ,  '=:{};' : 693 ,  '};://' : 687 ,  'return:new' : 684 ,  'fs:=' : 682 ,  'if:the' : 682 ,  'path:=' : 674 }

ruby = { 'end:end' : 3243 ,  'end:def' : 2531 ,  '#:#' : 2157 ,  'end:#' : 1771 ,  '##:#' : 1426 ,  'end:##' : 900 ,  '#::nodoc:' : 615 ,  'of:the' : 565 ,  'to:the' : 470 ,  '#:The' : 452 ,  '#:frozen_string_literal:' : 412 ,  'frozen_string_literal::true' : 412 ,  'in:the' : 400 ,  '=:nil' : 399 ,  '#:def' : 364 ,  '#:@return' : 354 ,  '#:Returns' : 338 ,  '}:end' : 336 ,  '=:[]' : 329 ,  'the:#' : 297 ,  'the:given' : 277 ,  'end:if' : 262 ,  'for:the' : 258 ,  '#:@param' : 256 ,  'to:be' : 251 ,  'false,:false,' : 251 ,  '#:====' : 234 ,  'will:be' : 233 ,  'from:the' : 220 ,  '=:{}' : 205 ,  '#:If' : 202 ,  '=:true' : 200 ,  'end:private' : 198 ,  'is:not' : 198 ,  '###:#' : 189 ,  '<<:"' : 187 ,  'is:a' : 185 ,  'the:current' : 184 ,  'the:gem' : 184 ,  ':type:=>' : 184 ,  'module:Bundler' : 180 ,  'nil:end' : 180 ,  'true:require' : 178 ,  '":\\' : 175 ,  '#:the' : 172 ,  '#:This' : 171 ,  '=:nil)' : 170 ,  'with:the' : 170 ,  '#:A' : 165 ,  'a:new' : 163 ,  'if:the' : 159 ,  'true:if' : 158 ,  '=:false' : 158 ,  '=>:e' : 157 ,  'can:be' : 156 ,  'private:def' : 155 ,  'options:=' : 154 ,  'def:initialize' : 151 ,  'true:end' : 150 ,  'nil,:nil,' : 150 ,  'end:class' : 149 ,  ':banner:=>' : 146 ,  '#:*' : 146 ,  'out:<<' : 145 ,  '#:end' : 140 ,  'return:unless' : 135 ,  'for:this' : 134 ,  'as:a' : 133 ,  'true:module' : 132 ,  'value:end' : 131 ,  'Returns:the' : 131 ,  'to:a' : 129 ,  'Bundler:class' : 128 ,  'end:else' : 125 ,  'on:the' : 124 ,  'should:be' : 120 ,  'to:#' : 120 ,  'end:###' : 119 ,  'result:=' : 118 ,  'Parameters:#' : 118 ,  'list:of' : 116 ,  'name:of' : 115 ,  '=>::boolean,' : 114 ,  '====:Parameters' : 114 ,  '=:{})' : 108 ,  'false:end' : 107 ,  'This:is' : 107 ,  'end:alias_method' : 106 ,  'end:module' : 106 ,  'next:if' : 105 ,  '=:value' : 103 ,  'spec:=' : 102 ,  'return:if' : 102 ,  'end:require' : 101 ,  'a:gem' : 100 ,  '=:nil,' : 99 ,  '#:Set' : 99 ,  'path:=' : 98 ,  '=:if' : 96 ,  'do:|value,' : 95 }

perl = { "=>:'sub" : 23745 ,  '{:my' : 18520 ,  '=:shift;' : 8701 ,  '=:@_;' : 8625 ,  '):{' : 8325 ,  '$self:=' : 5828 ,  'my:$self' : 5668 ,  '}:}' : 4520 ,  'if:(' : 4345 ,  'else:{' : 4268 ,  'shift;:my' : 4228 ,  '}:else' : 4160 ,  '{:return' : 3913 ,  '$VAR1:=' : 3298 ,  '=:{' : 3268 ,  '{:#' : 3256 ,  '):=' : 2952 ,  '@_;:my' : 2940 ,  '}:#' : 2792 ,  '};:$VAR1' : 2791 ,  'my:(' : 2725 ,  '}:return' : 2649 ,  "}':};" : 2537 ,  'my:($self,' : 2379 ,  ');:}' : 2277 ,  '}:elsif' : 2275 ,  'sub:{' : 1962 ,  ");:}'," : 1805 ,  '{:if' : 1713 ,  '}:if' : 1698 ,  "}:}'," : 1656 ,  '=:0;' : 1632 ,  'for:my' : 1630 ,  '@_;:return' : 1565 ,  '}:my' : 1438 ,  'foreach:my' : 1336 ,  'shift;:return' : 1313 ,  '=:1;' : 1252 ,  'unless:defined' : 1215 ,  'map:{' : 1210 ,  'return:if' : 1203 ,  '(:$self,' : 946 ,  '):)' : 918 ,  ');:return' : 895 ,  '{:push' : 884 ,  ');:my' : 881 ,  'elsif:(' : 865 ,  '$class:=' : 854 ,  'my:$class' : 808 ,  'if:defined' : 799 ,  'return:unless' : 796 ,  '1;:}' : 792 ,  '=:(' : 774 ,  '=:{};' : 773 ,  'eval:{' : 770 ,  '@_;:#' : 770 ,  '{:require' : 729 ,  '=>:sub' : 727 ,  '=:shift' : 688 ,  '=:sub' : 685 ,  'return:$self;' : 668 ,  'my:($self)' : 662 ,  '($self):=' : 662 ,  "'new':=>" : 641 ,  'new:{' : 637 ,  "'sub:new" : 636 ,  'or:die' : 628 ,  'grep:{' : 622 ,  'of:the' : 620 ,  'return:1;' : 617 ,  ');:#' : 617 ,  '};:}' : 615 ,  "return;:}'," : 612 ,  "$self;:}'," : 605 ,  "=:\\'\\';" : 601 ,  'next:if' : 591 ,  '):or' : 585 ,  '(:my' : 583 ,  'return;:}' : 571 ,  '():{' : 569 ,  'in:the' : 568 ,  '#:If' : 568 ,  '":.' : 560 ,  '=:map' : 557 ,  '=>:[' : 540 ,  '=:delete' : 538 ,  'if:(defined' : 537 ,  '1:if' : 523 ,  'unless:(' : 522 ,  '@_;:if' : 521 ,  "}',:'new'" : 517 ,  '$name:=' : 517 ,  '):if' : 514 ,  '(:defined' : 508 ,  "'BEGIN':=>" : 507 ,  '{};:$VAR1' : 506 ,  "=>:'BEGIN" : 506 ,  "'BEGIN:{" : 505 ,  "};:}'," : 504 ,  '}:=' : 502 }

typescript = { '}:}' : 8156 ,  '{:return' : 7689 ,  '{:}' : 7209 ,  '}:function' : 4649 ,  '{:////' : 4045 ,  '}://' : 3266 ,  '=>:{' : 3144 ,  '{:var' : 3079 ,  '():=>' : 3036 ,  '{:const' : 2848 ,  '{://' : 2805 ,  '}:class' : 2775 ,  '}:export' : 2449 ,  '}:var' : 2379 ,  '{:if' : 2313 ,  'x:=' : 2151 ,  '=:new' : 2111 ,  '}:else' : 2002 ,  '=:{' : 1980 ,  '}:////' : 1943 ,  '////:}' : 1914 ,  '}:interface' : 1883 ,  'export:var' : 1753 ,  '//:error' : 1712 ,  '{:export' : 1690 ,  '=:0;' : 1582 ,  '}:if' : 1519 ,  'export:class' : 1507 ,  'y:=' : 1480 ,  '}:return' : 1461 ,  'else:{' : 1428 ,  'export:function' : 1405 ,  '},:{' : 1348 ,  'var:x' : 1300 ,  'C:{' : 1262 ,  '}:public' : 1214 ,  '//:@Filename:' : 1210 ,  '//:ok' : 1190 ,  'of:the' : 1176 ,  'string;:}' : 1160 ,  'export:interface' : 1142 ,  '=:1;' : 1126 ,  '///:<reference' : 1116 ,  'x;:}' : 1072 ,  '////:////' : 1062 ,  'T):=>' : 1061 ,  'any):{' : 1026 ,  'var:y' : 1023 ,  'a:=' : 1012 ,  'A:{' : 1000 ,  '}:module' : 971 ,  '{:x:' : 947 ,  '//:@filename:' : 917 ,  'return:x;' : 908 ,  'class:C' : 907 ,  '{:text:' : 901 ,  '{:let' : 898 ,  'i:=' : 885 ,  'declare:function' : 876 ,  'var:x:' : 863 ,  '};:var' : 856 ,  'number):{' : 814 ,  'for:(let' : 803 ,  '}:=' : 785 ,  '=:this;' : 785 ,  'i:<' : 751 ,  'number;:}' : 751 ,  'true://' : 750 ,  '};:return' : 734 ,  '}:private' : 730 ,  'b:=' : 729 ,  'i++):{' : 719 ,  '{:public' : 718 ,  'string):{' : 703 ,  'this;:};' : 699 ,  'number):=>' : 692 ,  'return:null;' : 685 ,  'else:if' : 676 ,  '////:var' : 657 ,  'boolean:{' : 656 ,  "path='fourslash.ts':/>" : 651 ,  "<reference:path='fourslash.ts'" : 650 ,  'null;:}' : 647 ,  'in:the' : 646 ,  'return:new' : 640 ,  'true;:}' : 631 ,  'Base:{' : 621 ,  '0;:i' : 616 ,  '}:const' : 610 ,  '}:for' : 603 ,  '{:foo:' : 603 ,  '//:Error' : 600 ,  'undefined;:}' : 597 ,  'for:(const' : 592 ,  'should:be' : 587 ,  'I:{' : 583 ,  '};:}' : 574 ,  'return:true;' : 573 ,  'void:{' : 572 ,  '{:a:' : 566 }

python = { '->:LATIN' : 5674 ,  'SMALL:LETTER' : 5112 ,  'CAPITAL:LETTER' : 4641 ,  'LATIN:SMALL' : 4121 ,  'of:the' : 3893 ,  'LATIN:CAPITAL' : 3733 ,  'if:not' : 3648 ,  '=:1' : 3019 ,  'is:not' : 2861 ,  '=:0' : 2765 ,  'None,:None,' : 2722 ,  '=:None' : 2719 ,  '=:[]' : 2639 ,  'in:the' : 2432 ,  '#:#' : 2154 ,  '#:LATIN' : 2149 ,  'to:the' : 2120 ,  'def:__init__(self,' : 1712 ,  'is:None:' : 1647 ,  'i:in' : 1632 ,  'for:i' : 1596 ,  'BOX:DRAWINGS' : 1556 ,  's:=' : 1501 ,  'is:a' : 1485 ,  '=:{' : 1416 ,  'for:the' : 1408 ,  'a:=' : 1354 ,  'x:=' : 1284 ,  'to:be' : 1270 ,  'not:None:' : 1226 ,  '=:2' : 1191 ,  'c:=' : 1188 ,  'b:=' : 1164 ,  'f:=' : 1108 ,  '#:The' : 1076 ,  'want:=' : 1064 ,  '=:{}' : 1057 ,  'if:__name__' : 1034 ,  '__name__:==' : 1034 ,  'list:of' : 959 ,  '#:BOX' : 948 ,  'can:be' : 917 ,  '=:True' : 911 ,  'will:be' : 909 ,  'not:in' : 874 ,  'result:=' : 862 ,  'is:the' : 861 ,  'of:a' : 847 ,  '#:This' : 847 ,  '=:[' : 845 ,  '=:3' : 844 ,  'd:=' : 827 ,  'from:the' : 818 ,  'on:the' : 816 ,  'with:the' : 810 ,  'LETTER:A' : 792 ,  'the:same' : 785 ,  'should:be' : 784 ,  'must:be' : 779 ,  'data:=' : 773 ,  'import:sys' : 770 ,  'if:the' : 769 ,  'LETTER:O' : 761 ,  'the:#' : 754 ,  'msg:=' : 753 ,  '#:the' : 752 ,  '=:False' : 751 ,  "'\\n':'" : 744 ,  'm:=' : 736 ,  'WITH:ACUTE' : 724 ,  'which:=' : 717 ,  'in:a' : 706 ,  '=:4' : 704 ,  '""":which' : 697 ,  '#:Test' : 693 ,  'and:the' : 679 ,  'i:=' : 677 ,  'it:is' : 665 ,  'that:the' : 654 ,  'LETTER:E' : 650 ,  'LETTER:U' : 650 ,  'pass:class' : 644 ,  'x:in' : 640 ,  'line:=' : 633 ,  'as:a' : 633 ,  '->:DIGIT' : 631 ,  'pass:def' : 628 ,  'to:a' : 621 ,  'This:is' : 616 ,  'else::return' : 613 ,  'with:a' : 612 ,  'by:the' : 612 ,  '[]:for' : 609 ,  '#:XXX' : 609 ,  '->:BOX' : 608 ,  'a:list' : 606 ,  'A:WITH' : 602 ,  'for:x' : 595 ,  "=:''" : 590 ,  'used:to' : 590 }

scala = { '}:}' : 23566 ,  '=:{' : 23025 ,  '{:val' : 20439 ,  '*:*' : 16856 ,  '=:new' : 15859 ,  'override:def' : 13583 ,  '{:case' : 11923 ,  '/**:*' : 11545 ,  '*/:def' : 10898 ,  '}:/**' : 10279 ,  'Int:=' : 9789 ,  'of:the' : 9208 ,  '{:def' : 8484 ,  'under:the' : 7436 ,  'the:License' : 7368 ,  'match:{' : 7087 ,  'Unit:=' : 6992 ,  '}:def' : 6952 ,  '*:@param' : 6784 ,  '}://' : 6663 ,  '=:0' : 5739 ,  '":+' : 5647 ,  '{://' : 5553 ,  'to:the' : 5539 ,  '}:else' : 5369 ,  '}:/*' : 5156 ,  'with:*' : 5142 ,  'See:the' : 5016 ,  'this:file' : 4942 ,  'private:def' : 4918 ,  'the:Apache' : 4912 ,  'the:License.' : 4912 ,  'else:{' : 4489 ,  'for:the' : 4291 ,  '_:=>' : 4276 ,  'in:the' : 4215 ,  '*:The' : 4213 ,  'case:_' : 4174 ,  '{:if' : 4035 ,  'Boolean:=' : 3838 ,  '=:if' : 3656 ,  '}:object' : 3558 ,  '*:the' : 3530 ,  'f;:}' : 3480 ,  '}:val' : 3430 ,  '*/:package' : 3298 ,  'String:=' : 3257 ,  '0:def' : 3243 ,  '}:override' : 3156 ,  '=>:val' : 3147 ,  'and:*' : 2939 ,  'case:class' : 2924 ,  '{:override' : 2846 ,  'object:Test' : 2754 ,  'of:this' : 2699 ,  'lazy:val' : 2695 ,  '/*:*' : 2674 ,  '*:See' : 2634 ,  '*:this' : 2623 ,  'may:not' : 2617 ,  'copy:of' : 2585 ,  ';:f;' : 2569 ,  'or:more' : 2566 ,  '{:;' : 2560 ,  'one:or' : 2535 ,  'on:an' : 2531 ,  'a:copy' : 2530 ,  'use:this' : 2524 ,  'file:to' : 2521 ,  'not:use' : 2515 ,  '**:**' : 2498 ,  'at:*' : 2497 ,  '2.0:*' : 2496 ,  'more:*' : 2486 ,  'work:for' : 2481 ,  'you:may' : 2477 ,  'required:by' : 2473 ,  'the:specific' : 2472 ,  '*:(the' : 2470 ,  'You:may' : 2468 ,  'to:in' : 2467 ,  'obtain:a' : 2466 ,  '*:Unless' : 2463 ,  'additional:information' : 2461 ,  'for:additional' : 2459 ,  'except:in' : 2459 ,  '*:distributed' : 2459 ,  '*:http://www.apache.org/licenses/LICENSE-2.0' : 2458 ,  'is:distributed' : 2458 ,  '*:limitations' : 2458 ,  'distributed:with' : 2457 ,  'information:regarding' : 2457 ,  'distributed:on' : 2457 ,  '*:Licensed' : 2456 ,  'under:one' : 2456 ,  'Apache:License,' : 2456 ,  'License,:Version' : 2456 ,  'Version:2.0' : 2456 ,  '(the:"License");' : 2456 ,  'file:except' : 2456 }

php = { 'var_dump(null),:var_dump(null),' : 372600 ,  'public:function' : 260353 ,  '}:public' : 214998 ,  '}:}' : 138802 ,  '{:return' : 115497 ,  '{:if' : 73271 ,  '=:new' : 69535 ,  '}:if' : 58457 ,  '}:<?php' : 52436 ,  "=>:'0'," : 50236 ,  '}:else' : 48696 ,  '}:return' : 44790 ,  '<?php:namespace' : 43537 ,  'else:{' : 42064 ,  'protected:function' : 40437 ,  ');:}' : 31881 ,  '}:protected' : 31276 ,  '=>:array(' : 30848 ,  "'id':=>" : 28506 ,  "=>:'1'," : 27674 ,  'throw:new' : 27386 ,  '=:array();' : 26156 ,  '{:throw' : 25465 ,  '{:protected' : 20477 ,  '{:public' : 20396 ,  'array:(' : 19341 ,  '=>:array' : 19020 ,  'null):{' : 18900 ,  "'contentobject_id':=>" : 18071 ,  '=:0;' : 15867 ,  '=>:[' : 14862 ,  'false;:}' : 14739 ,  '=:array(' : 14683 ,  '=>:true,' : 14501 ,  "'identifier':=>" : 14389 ,  "'contentclass_id':=>" : 14224 ,  "'placement':=>" : 13528 ,  '=:null;' : 13463 ,  '):{' : 13449 ,  '$this;:}' : 13442 ,  "'0',:'id'" : 13418 ,  'return:$this;' : 13391 ,  'static:function' : 13324 ,  "'published':=>" : 13277 ,  "'section_id':=>" : 13248 ,  "'frequency':=>" : 12817 ,  "'contentclass_attribute_id':=>" : 12814 ,  "'integer_value':=>" : 12814 ,  "'next_word_id':=>" : 12814 ,  "'prev_word_id':=>" : 12814 ,  "'word_id':=>" : 12814 ,  "'0',:'next_word_id'" : 12793 ,  "(:'contentclass_attribute_id'" : 12609 ,  'true;:}' : 12443 ,  "=>:''," : 12412 ,  'public:static' : 12382 ,  '}:private' : 12382 ,  '0):{' : 12296 ,  '}:function' : 12276 ,  'return:false;' : 12171 ,  "'1',:'word_id'" : 11899 ,  '=:null)' : 11824 ,  '=:false;' : 11757 ,  'private:function' : 11752 ,  '=:true;' : 11330 ,  '$result:=' : 11265 ,  "[],:''," : 11145 ,  'break;:case' : 10994 ,  "=:'';" : 10866 ,  '{:global' : 10797 ,  "'type':=>" : 10563 ,  '}:elseif' : 10434 ,  'if:(!' : 10145 ,  '{:foreach' : 9788 ,  "':." : 9703 ,  "=>:'16'," : 9376 ,  '$vendorDir:.' : 9284 ,  '=>:$vendorDir' : 9222 ,  "'16',:'contentobject_id'" : 9033 ,  '=>:null,' : 8938 ,  "=>:'body'," : 8912 ,  "'body',:'integer_value'" : 8885 ,  'false):{' : 8403 ,  'return:true;' : 8291 ,  '{:var_dump(var_dump(null),' : 8280 ,  'var_dump(var_dump(null),:var_dump(null),' : 8280 ,  'var_dump(null),:var_dump(null));' : 8280 ,  'var_dump(null));:}' : 8280 ,  'return:new' : 8252 ,  '}:catch' : 8064 ,  '$sql.=:"' : 8020 ,  "=>:'187'," : 7913 ,  '=>:false,' : 7892 ,  '=:[];' : 7856 ,  '=:[' : 7796 ,  'extends:\\PHPUnit_Framework_TestCase' : 7784 ,  '\\PHPUnit_Framework_TestCase:{' : 7784 ,  '=>:1,' : 7781 ,  '$data:=' : 7721 ,  '$params:=' : 7682 }

objc = { '}:}' : 4779 ,  '}:-' : 4564 ,  '}:else' : 3939 ,  '{:return' : 3459 ,  '{:if' : 2925 ,  'else:{' : 2737 ,  '0):{' : 2666 ,  '}:if' : 2501 ,  '-:(void)' : 2480 ,  '=:0;' : 2243 ,  'nil):{' : 2096 ,  'of:the' : 1978 ,  '/**:*' : 1775 ,  '/*:*' : 1653 ,  '}:return' : 1584 ,  '}:/**' : 1581 ,  '=:nil;' : 1508 ,  '*/:-' : 1385 ,  'else:if' : 1358 ,  '=:[self' : 1245 ,  '-:(id)' : 1220 ,  '==:nil)' : 1192 ,  '==:0)' : 1156 ,  '}:/*' : 1098 ,  '{:[self' : 1097 ,  '!=:nil)' : 1088 ,  '==:YES)' : 1049 ,  'nil;:}' : 1002 ,  'YES):{' : 983 ,  'in:the' : 973 ,  'return:nil;' : 935 ,  '*/:if' : 909 ,  '>:0)' : 887 ,  '[NSException:raise:' : 873 ,  '=:NO;' : 851 ,  '{:/*' : 843 ,  '=:YES;' : 819 ,  '}:@end' : 817 ,  'to:the' : 816 ,  'NO;:}' : 816 ,  '0;:}' : 800 ,  '==:NO)' : 799 ,  '{:NSString' : 781 ,  'return:NO;' : 775 ,  'NO):{' : 750 ,  'YES;:}' : 713 ,  'the:GNU' : 696 ,  'Free:Software' : 691 ,  'General:Public' : 685 ,  '-:(BOOL)' : 674 ,  'Public:License' : 667 ,  '{:[NSException' : 665 ,  '/>:*' : 659 ,  's:=' : 630 ,  'return:self;' : 628 ,  'return:[self' : 627 ,  'break;:case' : 620 ,  'break;:}' : 619 ,  '{:unsigned' : 617 ,  'self;:}' : 614 ,  'return:0;' : 607 ,  '!=:0)' : 588 ,  'the:*' : 585 ,  'return;:}' : 570 ,  '}:+' : 562 ,  'result:=' : 562 ,  'c:=' : 552 ,  '(i:=' : 528 ,  '*:Returns' : 527 ,  'for:(i' : 525 ,  'i:<' : 502 ,  'return:YES;' : 501 ,  '@end:@implementation' : 485 ,  'Software:Foundation,' : 476 ,  'the:Free' : 473 ,  'if:(nil' : 467 ,  'i++):{' : 457 ,  'by:the' : 444 ,  '*:The' : 444 ,  '{://' : 442 ,  '0;:i' : 440 ,  '=:[NSString' : 432 ,  'library:is' : 430 ,  '[buf:appendString:' : 426 ,  '*:If' : 423 ,  'This:library' : 422 ,  'GNU:Lesser' : 419 ,  'Lesser:General' : 419 ,  'is:not' : 408 ,  'to:be' : 407 ,  'e:=' : 401 ,  '+:(id)' : 399 ,  'const:char' : 397 ,  'raise::NSInvalidArgumentException' : 396 ,  'NSInvalidArgumentException:format:' : 393 ,  '*:the' : 393 ,  'nil:&&' : 389 ,  'for:the' : 388 ,  '=:[[NSString' : 386 ,  '[NSAutoreleasePool:new];' : 378 }

classifiers = [java, perl]
# classifiers = [cplusplus, javascript, java, c, ruby, perl, typescript, python, scala, php, objc]

# Normalize classifiers

for i in range(0, len(classifiers)):
    total = reduce(lambda x,y: x+y, classifiers[i].values())
    for j in classifiers[i].keys():
        classifiers[i][j] = float(classifiers[i][j]) / total

# Load up input file to be classified.

counts = {}
total = 0

with open(fname, 'r') as f:
    # Generate histogram of counts for each word.
    wordgen = wordsn(f,2,2)
    for word in wordgen:
        counts[word] = counts.get(word, 0) + 1
        total += 1

print counts

argmax = 0
max = float('-inf')

for i in xrange(0,len(classifiers)):

    # Naive Bayes.
    val = 1
    for word in counts:
        c       = classifiers[i].get(word, 0) # 0.0001)
        if c != 0:
            val     += math.log(counts[word] * c)

    # Incorporate a modest prior for the extension
    for thisext in extensions[i]:
        if ext == thisext:
            val /= extensionPrior
            break

    print val
    
    # New maximum?
    if val > max:
        max = val
        argmax = i

print classes[argmax],

