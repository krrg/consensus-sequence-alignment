__author__ = 'krr428'

import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as inf:
        with open(sys.argv[1] + ".txt", 'w') as outf:
            for line in inf:
                if not line.startswith('>'):
                    outf.write(line)
        print sys.argv[1] + ".txt", "written."

