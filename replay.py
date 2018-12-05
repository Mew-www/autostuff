import os
import argparse
import json
import time
from windowsreplay import replay

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--filename', dest='filename', default='history.txt')
    argparser.add_argument('--delay', dest='delay', default=0, type=int)
    argparser.add_argument('--aggregate', dest='aggregate', default=False, type=bool)
    args = argparser.parse_args()

    configfile_path = os.path.join(os.path.join(os.path.realpath(__file__)), '..', args.filename)
    config = json.load(open(configfile_path, 'r'))
    if not args.aggregate:
        replay(config, args.delay)
    else:
        time.sleep(args.delay)
        for filename, delay in config:
            replay(json.load(open(filename, 'r')), delay)

