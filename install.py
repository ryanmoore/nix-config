#!/usr/bin/python

import sys
import os
import errno
import shutil

user_dir = os.path.expanduser('~/')

files = {
        'bashrc':      os.path.join(user_dir, '.bashrc'),
        'vimrc':       os.path.join(user_dir, '.vimrc'),
        'vim':         os.path.join(user_dir, '.vim'),
        'screenrc':    os.path.join(user_dir, '.screenrc'),
        'config':      os.path.join(user_dir, '.config'),
        'Xdefaults':   os.path.join(user_dir, '.Xdefaults'),
        'DIR_COLORS':  'etc/DIR_COLORS',
        'bash.bashrc': 'etc/bash.bashrc',
        }

class UserObjectionException(Exception):
    pass

def main():
    if os.getuid() != 0:
        print 'Installation to some directories requires sudo. Please rerun with elevated permissions.'

    for src,dest in files.iteritems():
        print 'Installing %s'%( dest )

        try:
            DeleteExisting( dest )
        except UserObjectionException:
            continue
        except OSError as e:
            print 'Error: Failed to remove %s. Skipping.'%( dest )
            continue

        try:
            Install( src, dest )
        except OSError as e:
            print 'Error: Failed to install %s to %s. Skipping.'%( src, dest )
            continue

def DeleteExisting( target ):
    if os.path.exists( target ):
        response = raw_input( 'Overwrite %s? (y/n) '%( target ) )
        if response != 'y':
            raise UserObjectionException()

        try:
            shutil.rmtree( target )
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                os.remove( target )

        print '\trm -rf %s'%( target )

def Install( src, dest ):
    try:
        shutil.copytree( src, dest )
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy( src, dest )
        else:
            raise

    print '\tcp %s %s'%( src, dest )

if __name__ == '__main__':
    main()

