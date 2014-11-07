__author__ = 'krr428'

def read_input_matrix(filename):
    matrix = []
    with open(filename) as f:
        for line in f:
            matrix.append(map(int, [x for x in line.strip().split('\t') if x != '']))
    return matrix

print len(read_input_matrix("./Fasta/real.error.large.fasta.matrix"))

