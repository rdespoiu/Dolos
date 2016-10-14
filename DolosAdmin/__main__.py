import sys
from adduser import *

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'adduser':
            addUser(sys.argv[2], sys.argv[3])

    except IndexError:
        print 'Incorrect format. To use this package:'
        print 'python DolosAdmin [method] [username] [password]'
