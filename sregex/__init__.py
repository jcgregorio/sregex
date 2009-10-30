"""
The sregex module implements Structural Regular Expressions.
Structural Regular Expressions were created by Rob Pike
and covered in this paper:

  http://doc.cat-v.org/bell_labs/structural_regexps/

Structural regular expressions work by describing the shape
of the whole string, not just the piece you want to match.
Each pattern is a list of operators to perform on a string, each time
constraining the range of text that matches the pattern. Examples
will make this much clearer. 

The first operator to consider is the x// operator, which means
e(x)tract. When applied to a string, all the substrings that match
the regular expression between // are passed on to the next operator
in the pattern.

Given the source string "Atom-Powered Robots Run Amok" and the 
pattern "x/A.../" the result would be ['Atom', 'Amok']. The sregex
module does that using the 'sres' function:

  >>> list(sres("Atom-Powered Robots Run Amok", "x/A.../"))
  ['Atom', 'Amok']

A pattern can contain mulitple operators, separated by 
whitespace, which are applied in order, each to the result of 
the previous match. 

  >>> list(sres("Atom-Powered Robots Run Amok", "x/A.../ x/.*m$/"))
  ['Atom']

There are four operators in total:

    x/regex/ - Matches all the text that matches the regular expression
    y/regex/ - Matches all the text that does not match the regular expression
    g/regex/ - If the regex finds a match in the string then the whole string is passed along.
    v/regex/ - If the regex does not find a match in the string then the whole string is passed along.


  >>> list(sres("Atom-Powered Robots Run Amok", "y/ /"))
  ['Atom-Powered', 'Robots', 'Run', 'Amok']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/( |-)/"))
  ['Atom', 'Powered', 'Robots', 'Run', 'Amok']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/ / x/R.*/"))
  ['Robots', 'Run']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/ / x/R./"))
  ['Ro', 'Ru']

  >>> sres("Atom-Powered Robots Run Amok", "y/( |-)/ v/^R/")
  ['Atom', 'Powered', 'Amok']

  >>> sres("Atom-Powered Robots Run Amok", "y/ / v/^R/ g/om/")
  ['Atom']

The module provides two other functions:

 sre(source, pattern) - Returns an interator for the index ranges that match the pattern.

    >>> list(sre("Atom-Powered Robots Run Amok", "y/ / v/^R/ g/om/"))
    [(0,4)]

 sub(source, pattern, repl) - Returns source with all the matches to pattern replaced with repl.

    >>> sub("Atom-Powered Robots Run Amok", "y/ / v/^R/ g/om/", "Coal")
    "Coal-Powered Robots Run Amok"

    The repl argument can also be a callable, in which case it is passed the 
    matching substring and is expected to return the substitute string.

    >>> sub("Atom-Powered Robots Run Amok", "x/A.../", lambda x: x.upper())
    "ATOM-Powered Robots Run AMOK"

"""
import re

CMD = re.compile(r"([xygv]/[^/]*/)")
VALIDCMD = re.compile(r"^\s*([xygv]/[^/]*/)(\s+([xygv]/[^/]*/))*\s*$")

class InvalidPatternError(Exception): pass

def ispattern(s):
    return (s == "") or (None != VALIDCMD.search(s))

def _makerange(range, match):
    return (match.span()[0] + range[0], match.span()[1] + range[0])

def sre(src, pattern):
    """ Returns an interator over tuples that contain 
    ranges of text in the supplied 'src' that match
    the structural regular expression given in pattern"""

    def start():
        yield (0, len(src))

    def from_g(f, pat):
        def nextf():    
            for range in f():
                s = src[slice(*range)]
                if re.search(pat, s):
                    yield range
        return nextf

    def from_v(f, pat):
        def nextf():    
            for range in f():
                s = src[slice(*range)]
                if not re.search(pat, s):
                    yield range
        return nextf

    def from_x(f, pat):
        def nextf():    
            for range in f():
                s = src[slice(*range)]
                for match in re.finditer(pat, s, re.DOTALL):
                    yield _makerange(range, match)
        return nextf

    def from_y(f, pat):
        def nextf():    
            for range in f():
                s = src[slice(*range)]
                begin = range[0]
                mend = range[1]
                amatch = False
                for match in re.finditer(pat, s, re.DOTALL):
                    amatch = True
                    (mbegin, mend) = _makerange(range, match)
                    if mbegin != begin:
                        yield (begin, mbegin)
                        begin = mend
                if mend != range[1] and amatch:
                    yield (mend, range[1])
        return nextf


    if not ispattern(pattern):
        raise InvalidPatternError(pattern)

    # f is a callable that returns an iterator. The iterator yields tuples of 
    # offsets into 'src'. We keep wrapping f's with new f's until we've built
    # the entire sre processing chain.
    wrapper = {
            'x': from_x,
            'y': from_y,
            'g': from_g,
            'v': from_v,
            }

    f = start
    for c in CMD.findall(pattern):
        f = wrapper[c[0]](f, c[2:-1])

    return f()

def sres(src, pattern):
    """ Returns an interator over strings in the supplied 'src' that match the
    structural regular expression given in pattern"""

    for range in sre(src, pattern):
        yield src[slice(*range)]

def sub(src, pattern, repl):
    """ Returns a modified copy of 'src' with all the ranges
    that match 'pattern' replaced with 'repl'. The replacement
    'repl' may be either a string, or a callable that takes
    the original text and returns the text to replace it with.
    """
    ranges = reversed(list(sre(src, pattern)))
    lsrc = list(src)
    for range in ranges:
        if callable(repl):
            lsrc[slice(*range)] = repl(src[slice(*range)])
        else:
            lsrc[slice(*range)] = repl

    return "".join(lsrc)

