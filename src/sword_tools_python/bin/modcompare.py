from .. import utils
import argparse
import sys
import Sword


def modcompare(arglist=sys.argv):
    parser = argparse.ArgumentParser(description="Compares two SWORD modules, verse by"
            " verse, to certify that the contents of each are identical")
    parser.add_argument("original", help="First module")
    parser.add_argument("test", help="Second module to compare against the first")
    args = parser.parse_args()

    original = utils.get_mod(args.original)
    test = utils.get_mod(args.test)

    if original is None or test is None:
        print("Please double check that both modules are installed and accessible",
              file=sys.stderr)
        sys.exit(1)

    key = Sword.VerseKey(original.createKey())
    test.setKey(key)
    book = key.getBook()

    while key.popError() == '\x00':
        if book != key.getBook():
            print("Checked up through ", key.getText())
            book = key.getBook()
        oText = original.renderText().c_str()
        tText = test.renderText().c_str()
        if oText != tText:
            print(f"Mismatch in {key.getText()}")
            print(f"Original text is*********:\n{oText}")
            print(f"New text is*********:\n{tText}")
        key.increment()
        original.setKey(key)
        test.setKey(key)

    print("Comparison ended at ", key.getText())
