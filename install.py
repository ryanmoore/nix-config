#!/usr/bin/env python3

import sys
import os
import errno
import shutil
import subprocess
import logging
import argparse

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EXTERNAL = os.path.join(BASE_DIR, 'external')
VIM_DIR  = os.path.join(BASE_DIR, 'src', 'vim')

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Install config files to home directory (with soft links)')
    parser.add_argument('--force', '-f', action='store_true', default=False,
            help='Don\'t ask about overwriting files, just do.')

    args = parser.parse_args()
    tolink = [
             ('bashrc',    '~/.bashrc'),
             ('vimrc',     '~/.vimrc'),
             ('vim',       '~/.vim'),
             ('screenrc',  '~/.screenrc'),
             ('config',    '~/.config'),
             ('tmux.conf', '~/.tmux.conf'),
             ('dir_colors','~/.dir_colors'),
            ]

    src_folder = os.path.abspath(os.path.join(BASE_DIR, 'src'))
    tolink = [ (os.path.join(src_folder, first), os.path.expanduser(second)) for first,second in tolink ]
    tolink.append( ( os.path.join(solarized_root, 'xresources', 'solarized'),
        os.path.expanduser('~/.Xresources') ) )

    for src,dest in tolink:
        install( src, dest, args )

def user_says_yes(query):
    answer = input(query)
    return answer.lower() == 'y'

def install( src, dest, args ):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    if os.path.exists(dest):
        if args.force or user_says_yes( 'Overwrite {} (Y/n)? '.format(dest) ):
            logging.info('rm {}'.format(dest))
            try:
                os.remove(dest)
            except OSError as e:
                if e.errno == os.errno.EISDIR:
                    shutil.rmtree(dest)
                else:
                    raise
        else:
            logging.info('skipping {}'.format(dest))
            return
    logging.info('ln -s {} {}'.format(src, dest))
    os.symlink( src, dest )

if __name__ == '__main__':
    main()

