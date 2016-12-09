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

class GitPackage:
    def __init__(self, src, name):
        self.src = src
        self.name = name

    def install_or_update(self, dst):
        dst = os.path.expanduser(dst)
        logging.info('Installing {} to {}...'.format(self.name, dst))
        if os.path.exists(dst):
            logging.info('{} already installed.'.format(self.name))
            logging.info('Updating {}...'.format(self.name))
            with ChdirContextManager(dst):
                subprocess.call(['git', 'pull'])
            logging.info('Update complete: {}'.format(self.name))
        else:
            logging.info('Cloning {}...'.format(self.name))
            subprocess.check_call(['git', 'clone',
                self.src, dst])
            logging.info('Cloning complete: {}'.format(self.name))
        logging.info('{} pull complete.'.format(self.name))

VundleGithub = GitPackage(
    'https://github.com/gmarik/Vundle.vim.git',
    'Vundle')

SolarizedGithub = GitPackage(
    'https://github.com/altercation/solarized.git',
    'Solarized')

GnomeTerminalSolarized = GitPackage(
    'https://github.com/Anthony25/gnome-terminal-colors-solarized.git',
    'GnomeTerminalSolarized')

def ask_about_initial_setup():
    print('Setup:')
    print('\tsudo apt install build-essential cmake python-dev python3-dev tmux')
    print('\tCreate a new Gnome Terminal profile called \'Solarized\'')
    if not user_says_y('Continue?'):
        sys.exit(1)

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Install config files to home directory (with soft links)')
    parser.add_argument('--force', '-f', action='store_true', default=False,
            help='Don\'t ask about overwriting files, just do.')
    parser.add_argument('--skip_ycm', action='store_true', default=False,
            help='Skip building YouCompleteMe')
    parser.add_argument('--iknow', action='store_true', default=False,
            help='Runs the script instead of giving the warning')

    args = parser.parse_args()
    if not args.iknow:
        logging.error('Makefile with Ansible is now preferred.')
        logging.error('Re-run with --iknow to try this outdated script anyway.')
        return 1
    if not args.force:
        ask_about_initial_setup()

    tolink = [
             ('bashrc',    '~/.bashrc'),
             ('vimrc',     '~/.vimrc'),
             ('vim',       '~/.vim'),
             ('screenrc',  '~/.screenrc'),
             #('config',    '~/.config'),
             ('tmux.conf', '~/.tmux.conf'),
             #('dir_colors','~/.dir_colors'),
            ]

    src_folder = os.path.abspath(os.path.join(BASE_DIR, 'src'))
    tolink = [ (os.path.join(src_folder, first), os.path.expanduser(second)) for first,second in tolink ]
    extralinks = [(os.path.expanduser('~/.bashrc'), os.path.expanduser('~/.bash_profile'))]
    tolink = tolink + extralinks
    for src,dest in tolink:
        install( src, dest, args )
    VundleGithub.install_or_update('~/.vim/bundle/Vundle.vim')
    solarized = os.path.join(BASE_DIR, 'solarized')
    SolarizedGithub.install_or_update(solarized)
    gnomesolarized = os.path.join(BASE_DIR, 'GnomeTerminalSolarized')
    GnomeTerminalSolarized.install_or_update(gnomesolarized)
    with ChdirContextManager(gnomesolarized):
        subprocess.check_call(['./install.sh',
                               '--scheme', 'dark',
                               '--install-dircolors',
                               '--profile', 'Solarized'])

    logging.info('File installation complete')
    logging.info('Updating vim plugins')
    logging.info('Calling: vim +PluginInstall +qall')
    subprocess.check_call('vim +PluginInstall +qall'.split())
    if not args.skip_ycm:
        with ChdirContextManager(os.path.expanduser('~/.vim/bundle/YouCompleteMe')):
            subprocess.check_call(
                    './install.py --clang-completer --racer-completer'.split())

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

class ChdirContextManager:
    def __init__(self, dst):
        self.original = os.getcwd()
        self.dst = dst

    def __enter__(self):
        os.chdir(self.dst)

    def __exit__(self, *args):
        os.chdir(self.original)

if __name__ == '__main__':
    main()

