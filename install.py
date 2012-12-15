#!/usr/bin/python

import sys
import os
import errno
import shutil

sources = [
        'bashrc',
        'vimrc',
        'vim',
        'screenrc',
        'config',
        ]

class UserObjectionException(Exception):
    pass

def main():
    destdir = os.path.expanduser( '~/' )

    assert os.path.exists( destdir )

    response = raw_input( 'Install to %s? (y/n) '%( destdir ) )

    if response != 'y':
        sys.exit( 1 )

    for src in sources:
        dest = os.path.join( destdir, '.'+src )

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

