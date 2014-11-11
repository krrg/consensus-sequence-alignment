__author__ = 'krr428'

import sys

def read_input_file(filename):
    reads = set()
    with open(filename) as f:
        for line in f:
            reads.add(line)
    return reads


if __name__ == "__main__":
    print "Set size: ", len(read_input_file(sys.argv[1] if len(sys.argv) > 1 is not None else "/home/krr428/Downloads/19.small.fastq.txt"))