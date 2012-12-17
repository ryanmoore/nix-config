#!/usr/bin/python

import sys
import os
import errno
import shutil

class UserObjectionException(Exception):
    pass

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s [user]'%sys.argv[0]
        sys.exit(1)

    if os.getuid() != 0:
        print 'Installation to some directories requires sudo. Please rerun with elevated permissions.'
        sys.exit(1)

    files = (
            ( 'bashrc',      '/home/{USER}/.bashrc'.format( USER=sys.argv[1] )),
            ( 'vimrc',       '/home/{USER}/.vimrc'.format( USER=sys.argv[1] )),
            ( 'vim',         '/home/{USER}/.vim'.format( USER=sys.argv[1] )),
            ( 'screenrc',    '/home/{USER}/.screenrc'.format( USER=sys.argv[1] )),
            ( 'config',      '/home/{USER}/.config'.format( USER=sys.argv[1] )),
            ( 'Xdefaults',   '/home/{USER}/.Xdefaults'.format( USER=sys.argv[1] )),
            ( 'DIR_COLORS',  '/etc/DIR_COLORS' ),
            ( 'bash.bashrc', '/etc/bash.bashrc' ),
            )

    for src,dest in files:
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

