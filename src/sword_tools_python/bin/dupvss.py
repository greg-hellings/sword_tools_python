"""
A command line utility that takes one Sword module name, iterates all the verses in it,
and detects any duplicate verses in it, reporting them back to the caller along with
the count and the references where these duplicates are found. Only compares the stripped
bare text of the verses, not any markup or leading/trailing whitespaces.
"""
import argparse
import sys

from prettytable import PrettyTable

from .. import utils # pylint: disable=relative-beyond-top-level


def dupvss():
    """
    Entry point for the dupvss module
    """
    parser = argparse.ArgumentParser(
        description="Compares all the verses of "
        "a Sword module for duplicate verse text "
        "and reports where it may be found."
    )
    parser.add_argument("module", help="Installed module to test against")
    parser.add_argument("-v", action="count", default=0)
    args = parser.parse_args()

    mod = utils.get_mod(args.module)
    if mod is None:
        print("Unable to locate module, is it installed?", file=sys.stderr)
        sys.exit(1)
    verse_text = dict()
    print("Processing entries for", args.module)
    # Iterate verses to find every unique text
    for verse in utils.strip_verses(mod):
        verse = verse.strip()
        if verse in verse_text.keys():
            verse_text[verse].append(mod.getKey().getText())
        else:
            verse_text[verse] = [mod.getKey().getText()]
    # Create a list of tuples for each item
    dups = [
        (len(refs), text, ", ".join(refs))
        for text, refs in verse_text.items()
        if len(refs) > 1
    ]
    dups.sort(key=lambda a: a[0])
    table = PrettyTable()
    table.field_names = ["Count", "Text", "References"]
    for dup in dups:
        table.add_row(dup)
    print(table)
