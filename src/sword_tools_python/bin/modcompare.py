import argparse
import sys

import Sword  # pylint: disable=import-error

from .. import utils


def modcompare(arglist=sys.argv):  # pylint: disable=dangerous-default-value
    """
    Compares two modules, verse by verse, and reports verses that differ between
    the two.
    """
    parser = argparse.ArgumentParser(
        description="Compares two SWORD modules, verse by"
        " verse, to certify that the contents of each are identical"
    )
    parser.add_argument("original", help="First module")
    parser.add_argument("test", help="Second module to compare against the first")
    args = parser.parse_args(arglist)

    original = utils.get_mod(args.original)
    test = utils.get_mod(args.test)

    if original is None or test is None:
        print(
            "Please double check that both modules are installed and accessible",
            file=sys.stderr,
        )
        sys.exit(1)

    key = Sword.VerseKey(original.createKey())
    test.setKey(key)
    book = key.getBook()

    while key.popError() == "\x00":
        if book != key.getBook():
            print("Checked up through ", key.getText())
            book = key.getBook()
        original_text = original.renderText().c_str()
        test_text = test.renderText().c_str()
        if original_text != test_text:
            print(f"Mismatch in {key.getText()}")
            print(f"Original text is*********:\n{original_text}")
            print(f"New text is*********:\n{test_text}")
        key.increment()
        original.setKey(key)
        test.setKey(key)

    print("Comparison ended at ", key.getText())
