from abc import ABCMeta
from collections import deque, defaultdict
import unittest
import sys

__author__ = 'krr428'


class AdjacencyMatrix:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def get_distance_between(self, seqA, seqB):
        pass

    def iterkeys(self):
        pass


class InMemoryAdjacencyMatrix(AdjacencyMatrix):

    def __init__(self, keysfile, matrixfile):
        self.matrix = {}
        self.read_input_file(keysfile, matrixfile)
        self.preferred = deque()

    def read_input_file(self, keysfile, matrixfile):
        with open(keysfile) as kfile, open(matrixfile) as mfile:
            keylist = []
            for key in kfile:
                if key != "":
                    self.matrix[key.strip()] = {}
                    keylist.append(key.strip())
            for key, valuestr in zip(keylist, mfile):
                values = deque(map(int, valuestr.strip().split('\t')))
                if values == "":
                    continue
                for key2 in keylist:
                    self.matrix[key][key2] = values.popleft()
                    if key == key2:
                        self.matrix[key][key2] = float("-inf")

    def get_distance_between(self, seqA, seqB):
        try:
            return self.matrix[seqA][seqB]
        except KeyError:
            return float("-inf")

    def iterkeys(self):
        return self.matrix.iterkeys()

    def iteritems(self):
        return self.matrix.iteritems()

    def __getitem__(self, item):
        return self.matrix[item]

    def __len__(self):
        return len(self.matrix)

    def __iter__(self):
        return self.matrix.iterkeys()

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __delitem__(self, key):
        del self.matrix[key]

    def has_preferred(self):
        return len(self.preferred) > 0

    def get_preferred(self):
        return self.preferred.popleft()


class MaximizingTSP:


    def __init__(self, adjacencyMatrix):
        self.matrix = adjacencyMatrix

    def invalidate_col(self, column):
        for key in self.matrix:
            self.matrix[key][column] = float("-inf")

    def invalidate_row(self, row):
        # self.matrix[row] = defaultdict(lambda: float("-inf"))
        del self.matrix[row]

    def get_next_avail_row(self):
        if self.matrix.has_preferred():
            return self.matrix.get_preferred()
        LOWER_BOUND = 0
        for key in self.matrix:
            if max(self.matrix[key].iteritems(), key=lambda x: x[1])[1] > LOWER_BOUND:
                # print "Arbitrary node: ", key
                return key
        return None

    def get_maximum_path(self):
        current = self.get_next_avail_row()
        path = [current]
        self.invalidate_col(current)

        while True:

            if not current or len(self.matrix) <= 1:
                path.append("\n")
                break

            bestmatch = max(self.matrix[current].iteritems(), key=lambda x: x[1])
            # print bestmatch

            if bestmatch[1] <= 0:
                path.append("\n")
                self.invalidate_row(current)
                current = self.get_next_avail_row()
                path.append(current)
                self.invalidate_col(current)
                continue
            elif bestmatch[0] not in self.matrix:
                path.append("\n")
                self.invalidate_row(current)
                current = self.get_next_avail_row()
                continue

            self.invalidate_col(bestmatch[0])
            self.invalidate_row(current)

            self.matrix[bestmatch[0]][current] = float("-inf")
            path.append(bestmatch[0])
            current = bestmatch[0]

        return path


if __name__ == "__main__":
    # adjmatrix = InMemoryAdjacencyMatrix("../Fasta/reads/real.error.small.fasta.txt", "../Fasta/matrix/real.error.small.matrix")
    adjmatrix = InMemoryAdjacencyMatrix(sys.argv[1], sys.argv[2])
    print "\n".join(MaximizingTSP(adjmatrix).get_maximum_path())



class GreedyTSPTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_case1(self):
        adjmatrix = InMemoryAdjacencyMatrix("tests/case1/reads.txt", "tests/case1/test.matrix")
        adjmatrix.preferred.append('A')
        print MaximizingTSP(adjmatrix).get_maximum_path()

    def test_simple_break_case(self):
        adjmatrix = InMemoryAdjacencyMatrix("tests/case2/reads.txt", "tests/case2/test.matrix")
        adjmatrix.preferred.append('A')
        print MaximizingTSP(adjmatrix).get_maximum_path()

    def test_large_break_case(self):
        adjmatrix = InMemoryAdjacencyMatrix("tests/case3/reads.txt", "tests/case3/test.matrix")
        adjmatrix.preferred.extend(['D', 'G'])
        print MaximizingTSP(adjmatrix).get_maximum_path()

    def test_shmed_break_case(self):
        adjmatrix = InMemoryAdjacencyMatrix("tests/case3.5/reads.txt", "tests/case3.5/test.matrix")
        adjmatrix.preferred.extend(['B', 'F'])
        print MaximizingTSP(adjmatrix).get_maximum_path()

    def test_krmed_break_case(self):
        adjmatrix = InMemoryAdjacencyMatrix("tests/case2.5/reads.txt", "tests/case2.5/test.matrix")
        adjmatrix.preferred.extend(['A'])
        print MaximizingTSP(adjmatrix).get_maximum_path()

