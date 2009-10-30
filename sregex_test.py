import unittest

from sregex import ispattern, sre, sres, sub, CMD, VALIDCMD

class Test(unittest.TestCase):
    def test_pattern_parsing(self):
        match = VALIDCMD.search("x/f/ y/../")
        self.assertEqual("x/f/", match.group(1))
        self.assertEqual("y/../", match.group(3))
        self.assertEqual(None, VALIDCMD.search(""))
        try:
            sres("", "not a valid pattern")
            self.fail("Invalid patterns should raise an exception")
        except:
            pass
        self.assertTrue(ispattern(""))
        self.assertTrue(ispattern("""y/".*"/ y/'.*'/ x/[a-zA-Z0-9]+/ g/n/ v/../ """))
        self.assertTrue(ispattern("y/\"\"\".*\"\"\"/"))


    def test_x(self):
        cases = [
        # source    pattern          result
        ("fred",   "",              ['fred']),
        ("fred f", "x/f/",          ['f', 'f']),
        ("fred f", "x/fred/ x/./",  ['f', 'r', 'e', 'd']),
        ("fred f", "x/\s/",         [' ']),
        ("fred f", "x/\s/ x/./",    [' ']),
        ("fred f", "x/bar/",        []),
        ("french fries", "x/fr../", ['fren', 'frie']),
        ("french fries", "x/fr../ x/ri?e/", ['re', 'rie']),

        ("fred",   "y/bar/",        []),
        ("fred",   "y/r/",          ['f', 'ed']),
        ("fred",   "y/f/",          ['red']),
        ("fred",   "y/d/",          ['fre']),
        ("fr\ned", "y/\n/",        ['fr', 'ed']),
        ("fr\ned", "y/\s/",        ['fr', 'ed']),

        ("french fries",   "y/r/ y/n/",        ['e', 'ch f']),

        ("fred",   "g/f/",           ['fred']),
        ("fred",   "g/./",           ['fred']),

        ("""fred:2\nbarney:3\nwilma:27""",        r"y/\n/ y/:/",                  ['fred', '2', 'barney', '3', 'wilma', '27']),
        ("""fred:2\nbarney:3\nwilma:27""",        r"y/\n/ g/barney/ y/:/",        ['barney', '3']),
        ("""fred:2\nbarney:3\nwilma:27""",        r"y/\n/ v/barney/ y/:/",        ['fred', '2', 'wilma', '27']),

        ("""struct foo A = {
"a": x,
"b": y,
"c": g,
"d": v, }
            """,        r'x/{.*}/ y/{/ y/}/ y/,/ y/.*:/ y/\s+/' ,        ['x', 'y', 'g', 'v']),
        ]                

        for (source, pattern, result) in cases:
            self.assertEqual(result, list(sres(source, pattern)), "Source: '%s' Pattern: %s Actual: %s Expected %s" % (source, pattern, str(list(sres(source, pattern))), str(result)))

    def test_sub(self):
        self.assertEqual("I am in denial. I won't deny.", sub("i am in denial. i won't deny.", r"y/\s/ v/../ x/i/", "I"))
        self.assertEqual("A bc D E fgh", sub("a bc d e fgh", r"y/\s/ v/../", lambda x: x.upper()))

unittest.main()


