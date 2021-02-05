"""
Counts all the characters in a file, assumes UTF-8 encoding, and
reports the frequency of each character as well as the Unicode
character name for that code point. Can accept an arbitrary number
of filles on the argument line and will report the aggregate across
each file. Can also accept input from stdin. If you want to mix
stdin with files pass the filename '-' on the argument line.
"""
import fileinput
import prettytable
from unicodedata import name

def count():
    chars = dict()
    for line in fileinput.input():
        for c in line:
            if c not in chars:
                chars[c] = 1
            else:
                chars[c] += 1

    table = prettytable.PrettyTable()
    table.field_names = ["Code point", "Character", "Name", "Count"]
    for char in sorted(chars.items(), key=lambda a: a[1], reverse=True):
        # 0 is the character, 1 is the count
        try:
            cname = name(char[0])
        except:
            cname = "not found"
        table.add_row([ord(char[0]), char[0], cname, char[1]])
    print(table)
