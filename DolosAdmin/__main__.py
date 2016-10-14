import sys
from adduser import *

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'adduser':
            addUser(sys.argv[2], sys.argv[3])
        if sys.argv[1] == 'help':
            print 'Methods:'
            print 'adduser -> arguments: [username] [password]'

    except IndexError:
        print 'Incorrect format. To use this package:'
        print 'python DolosAdmin [method] [arg1] [arg2] [...] [argk]'
        print 'For help, use:'
        print 'python DolosAdmin help'
