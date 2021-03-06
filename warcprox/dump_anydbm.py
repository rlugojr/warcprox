#!/usr/bin/env python
'''
dump-anydbm - dumps contents of dbm file to stdout

Dump contents of database to stdout. Database can be any file that the anydbm
module can read. Included with warcprox because it's useful for inspecting a
deduplication database or a playback index database, but it is a generic tool.

Copyright (C) 2013-2016 Internet Archive

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
USA.
'''

try:
    import dbm
    from dbm import ndbm
    whichdb = dbm.whichdb

except:
    import anydbm
    dbm = anydbm
    from whichdb import whichdb

import sys
import os.path

if __name__ == "__main__":
    main()

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("usage: {} DBM_FILE\n".format(sys.argv[0]))
        exit(1)

    filename = sys.argv[1]
    which = whichdb(filename)

    # if which returns none and the file does not exist, print usage line
    if which == None and not os.path.exists(sys.argv[1]):
        sys.stderr.write('No such file {}\n\n'.format(sys.argv[1]))
        sys.stderr.write("usage: {} DBM_FILE\n".format(sys.argv[0]))
        exit(1)

    # covers case where an ndbm is checked with its extension & identified incorrectly
    elif 'bsd' in which:
        correct_file = filename.split(".db")[0]
        correct_which = whichdb(correct_file)
        if correct_which in ('dbm', 'dbm.ndbm'):
            filename = correct_file
            which = correct_which

    elif which == '':
        sys.stderr.write("{} is an unrecognized database type\n".format(sys.argv[1]))
        sys.stderr.write("Try the file again by removing the extension\n")
        exit(1)

    try:
        out = sys.stdout.buffer

    except AttributeError:
        out = sys.stdout

    out.write(filename.encode('UTF-8') + b' is a ' + which.encode('UTF-8') + b' db\n')

    db = dbm.open(filename, 'r')
    for key in db.keys():
        out.write(key + b":" + db[key] + b"\n")
