"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys
import os
import tempfile

from sknano.generators import SWNTGenerator

def getOptions():
    userOptions = {}

    userOptions['n'] = {}
    userOptions['n']['type'] = 'integer'
    userOptions['n']['default'] = 1

    userOptions['m'] = {}
    userOptions['m']['type'] = 'integer'
    userOptions['m']['default'] = 1

    userOptions['Length'] = {}
    userOptions['Length']['type'] = 'float'
    userOptions['Length']['default'] = 1.0
    userOptions['Length']['precision'] = 3
    userOptions['Length']['suffix'] = ' nm'
    userOptions['Length']['toolTip'] = 'Length of the nanotube'

    opts = {'userOptions': userOptions}

    return opts


def generate(opts):
    l = float(opts['Length'])
    m = int(opts['m'])
    n = int(opts['n'])

    swnt = SWNTGenerator((m, n), Lz=l)
    # secure tempfile name ending in ".xyz" in a writable tmpdir
    fd, name = tempfile.mkstemp(".xyz")
    os.close(fd) # don't use the filehandle

    swnt.save(fname=name)

    with open(name) as f:
        xyzData = f.read()
    os.remove(name)

    return xyzData


def runCommand():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Append tube in xyz format (Avogadro will bond everything)
    result = {}
    result['append'] = True
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = generate(opts)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Single Walled Nanotube')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Single Wall Nanotube...")
    if args['menu_path']:
        print("&Build|Insert")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
