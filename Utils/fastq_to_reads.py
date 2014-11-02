__author__ = 'krr428'

import sys

if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        with open(sys.argv[1] + '.txt', 'w') as f2:
            i = 0
            while True:
                lines = f.readline(), f.readline(), f.readline(), f.readline()
                if all(lines):
                    i += 1
                    if i % 10000 == 0:
                        print i
                    f2.write(lines[1])
                else:
                    print "Breaking"
                    break
