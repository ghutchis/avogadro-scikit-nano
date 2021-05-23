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
from random import randrange
from sknano.generators import MWNTGenerator

# Some globals:
debug = True


def getOptions():
    userOptions = {}

    userOptions['n'] = {}
    userOptions['n']['type'] = 'integer'
    userOptions['n']['default'] = 2
    userOptions['n']['suffix'] = ' walls'
    userOptions['n']['label'] = 'Number of MWNT Walls'

    userOptions['min'] = {}
    userOptions['min']['label'] = 'Minimum Wall Diameter'
    userOptions['min']['type'] = 'float'
    userOptions['min']['default'] = 1.0
    userOptions['min']['suffix'] = ' Å'

    userOptions['length'] = {}
    userOptions['length']['label'] = 'Length'
    userOptions['length']['type'] = 'float'
    userOptions['length']['default'] = 1.0
    userOptions['length']['precision'] = 3
    userOptions['length']['suffix'] = ' nm'
    userOptions['length']['toolTip'] = 'Length of the Nanotube'

    opts = {'userOptions': userOptions}

    return opts


def generate(opts):
    l = float(opts['length'])
    m = int(opts['min'])
    n = int(opts['n'])

    swnt = MWNTGenerator(Nwalls=n, min_wall_diameter=m, Lz=l)
    # need a better random temporary name
    name = 'temp{}.xyz'.format(randrange(32768))
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
        print("Multi-Wall Nanotube...")
    if args['menu_path']:
        print("&Build|Insert")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
