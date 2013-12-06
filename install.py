#!/usr/bin/env python3

import sys
import os
import errno
import shutil
import subprocess
import logging

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EXTERNAL = os.path.join(BASE_DIR, 'external')
VIM_DIR  = os.path.join(BASE_DIR, 'src', 'vim')

solarized_repo = r'git://github.com/altercation/solarized.git'
solarized_root = os.path.join(EXTERNAL, 'solarized')

pathogen_repo = r'git://github.com/tpope/vim-pathogen'
pathogen_root = os.path.join(EXTERNAL, 'pathogen')

def git_clone(repo, root):
    git = '/usr/bin/git'
    if not os.path.exists(root):
        cmd = [ git, 'clone', repo, root ]
        logging.info( ' '.join(cmd) )
        cwd = './'
    else:
        cmd = [ git, 'pull' ]
        cwd = root
        logging.info( 'from {}: {}'.format(cwd, ' '.join(cmd)) )
    subprocess.check_call(cmd, cwd=cwd)

def setup_pathogen():
    git_clone(pathogen_repo, pathogen_root)
    src = os.path.join(pathogen_root, 'autoload', 'pathogen.vim')
    dest = os.path.join(VIM_DIR, 'autoload', 'pathogen.vim')
    install(src, dest)

def setup_solarized():
    git_clone(solarized_repo, solarized_root)
    solarized_colors_dir = 'vim-colors-solarized'
    src = os.path.join(solarized_root, solarized_colors_dir)
    dest = os.path.join(VIM_DIR, 'bundle', solarized_colors_dir)
    install(src, dest)

def main():
    logging.basicConfig(level=logging.INFO)

    setup_pathogen()
    setup_solarized()

    tolink = [
             ('bashrc',    '~/.bashrc'),
             ('vimrc',     '~/.vimrc'),
             ('vim',       '~/.vim'),
             ('screenrc',  '~/.screenrc'),
             ('config',    '~/.config'),
             ('tmux.conf', '~/.tmux.conf'),
            ]

    src_folder = os.path.abspath(os.path.join(BASE_DIR, 'src'))
    tolink = [ (os.path.join(src_folder, first), os.path.expanduser(second)) for first,second in tolink ]
    tolink.append( ( os.path.join(solarized_root, 'xresources', 'solarized'),
        os.path.expanduser('~/.Xresources') ) )

    for src,dest in tolink:
        install( src, dest )

def user_says_yes(query):
    answer = input(query)
    return answer.lower() == 'y'

def install( src, dest ):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    if os.path.exists(dest) and user_says_yes('Overwrite {} (Y/n)? '.format(dest) ):
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

