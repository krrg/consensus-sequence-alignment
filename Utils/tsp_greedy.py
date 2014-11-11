from collections import deque

__author__ = 'krr428'

from abc import ABCMeta


class AdjacencyMatrix:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def get_distance_between(self, seqA, seqB):
        pass

class InMemoryAdjacencyMatrix(AdjacencyMatrix):

    def __init__(self, keysfile, matrixfile):
        self.matrix = {}
        self.read_input_file(keysfile, matrixfile)

    def read_input_file(self, keysfile, matrixfile):
        with open(keysfile) as kfile, open(matrixfile) as mfile:
            for key in kfile:
                if key != "":
                    self.matrix[key.strip()] = {}
            for key, valuestr in zip(self.matrix, mfile):
                values = deque(map(int, valuestr.strip().split('\t')))

                if values == "":
                    continue
                for key2 in self.matrix:
                    self.matrix[key][key2] = values.popleft()
                    if key == key2:
                        self.matrix[key][key2] = float("-inf")

    def get_distance_between(self, seqA, seqB):
        try:
            return self.matrix[seqA][seqB]
        except KeyError:
            return float("-inf")


class MaximizingTSP:

    def __init__(self, adjacencyMatrix):
        self.matrix = adjacencyMatrix

    def get_maximum_path(self):
        print self.matrix.iterkeys().next


adjmatrix = InMemoryAdjacencyMatrix("../Fasta/reads/real.error.small.fasta.txt", "../Fasta/matrix/real.error.small.matrix")

print MaximizingTSP(adjmatrix).get_maximum_path()
