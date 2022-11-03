'''
Runs the server in browser

author: Jay White
'''

import sys
import argparse
import flask_methods

# handles args
def args():
    """Function responsible for reading in and returning arguments"""
    parser = argparse.ArgumentParser(
        description="Ancient Greek Model", allow_abbrev=False)
    parser.add_argument('port', type=int,
        help='the port at which the servers should listen')

    return parser.parse_args()

def main():
    """Main method"""
    # calling args (error handles) and gets arguments
    arguments = args()
    port = arguments.port

    try:
        flask_methods.app.run(host="0.0.0.0", port = port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()