The sregex module implements Structural Regular Expressions.
Structural Regular Expressions were created by Rob Pike
and covered in this paper:

> http://doc.cat-v.org/bell_labs/structural_regexps/

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
pattern "x/A.../" the result would be `['Atom', 'Amok']`. The sregex
module does that using the 'sres' function:

```
  >>> list(sres("Atom-Powered Robots Run Amok", "x/A.../"))
  ['Atom', 'Amok']
```

A pattern can contain mulitple operators, separated by
whitespace, which are applied in order, each to the result of
the previous match.

```
  >>> list(sres("Atom-Powered Robots Run Amok", "x/A.../ x/.*m$/"))
  ['Atom']
```

There are four operators in total:

> x/regex/ - Matches all the text that matches the regular expression

> y/regex/ - Matches all the text that does not match the regular expression

> g/regex/ - If the regex finds a match in the string then the whole string is passed along.

> v/regex/ - If the regex does not find a match in the string then the whole string is passed along.

```
  >>> list(sres("Atom-Powered Robots Run Amok", "y/ /"))
  ['Atom-Powered', 'Robots', 'Run', 'Amok']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/( |-)/"))
  ['Atom', 'Powered', 'Robots', 'Run', 'Amok']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/ / x/R.*/"))
  ['Robots', 'Run']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/ / x/R./"))
  ['Ro', 'Ru']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/( |-)/ v/^R/"))
  ['Atom', 'Powered', 'Amok']

  >>> list(sres("Atom-Powered Robots Run Amok", "y/( |-)/ v/^R/ g/om/"))
  ['Atom']
```

The module provides two other functions:

## sre(source, pattern) ##
Returns an interator for the index ranges that match the pattern.

```
    >>> list(sre("Atom-Powered Robots Run Amok", "y/ / v/^R/ g/om/"))
    [(0,4)]
```

## sub(source, pattern, repl) ##
Returns source with all the matches to pattern replaced with repl.

```
    >>> sub("Atom-Powered Robots Run Amok", "y/( |-)/ v/^R/ g/om/", "Coal")
    "Coal-Powered Robots Run Amok"
```

The repl argument can also be a callable, in which case it is passed the
matching substring and is expected to return the substitute string.

```
    >>> sub("Atom-Powered Robots Run Amok", "x/A.../", lambda x: x.upper())
    "ATOM-Powered Robots Run AMOK"
```

## Installation ##

```
 $ hg clone https://sregex.googlecode.com/hg/ sregex  
 $ cd sregex
 $ python setup.py install
```