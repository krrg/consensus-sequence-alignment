from itertools import cycle

__author__ = 'krr428'

import sys

if __name__ == "__main__":
    filehandles = {}

    for i in xrange(16):
        filehandles[i] = open(sys.argv[1] + "." + str(i) + ".submatrix")

    with open(sys.argv[1] + ".matrix", 'w') as m:
        for i, j in zip(cycle(xrange(16)), xrange(100000)):
            m.write(filehandles[i].readline())
            if j % 1000 == 0:
                print j

    for key in filehandles:
        filehandles[key].close()


