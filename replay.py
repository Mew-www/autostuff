import os
import argparse
from windowsreplay import replay_file

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--filename', dest='filename', default='history.txt')
    argparser.add_argument('--delay', dest='delay', default=0, type=int)
    args = argparser.parse_args()

    configfile_path = os.path.join(os.path.join(os.path.realpath(__file__)), '..', args.filename)

    replay_file(configfile_path, args.delay)
