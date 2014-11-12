from abc import ABCMeta
from collections import deque, defaultdict
from datetime import datetime
from blist import sortedlist
import unittest
import sys
import plyvel


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

    def set_col(self, column):
        for key in self.matrix.iterkeys():
            self.matrix[key][column] = float("-inf")

    def remove_row(self, row):
        del self.matrix[row]


class LevelDBAdjacencyMatrix(AdjacencyMatrix):

    def __init__(self, keysfile, matrixfile):
        self.matrix = plyvel.DB("/tmp/" + str(datetime.now()), create_if_missing=True)
        self.prefkeys = sortedlist(self.read_input_file(keysfile, matrixfile))

    def read_input_file(self, keysfile, matrixfile):
        print "about to open"
        with open(keysfile) as kfile, open(matrixfile) as mfile:
            keylist = []
            for key in kfile:
                if key != "":
                    keylist.append(key.strip())
            for key, valuestr in zip(keylist, mfile):
                values = deque(map(int, valuestr.strip().split('\t')))
                if values == "":
                    continue
                for key2 in keylist:
                    self.matrix.put(key + key2, bytes(values.popleft()))
                    if key == key2:
                        self.matrix.put(key + key2, bytes(float("-inf")))
            for key in keylist:
                for key2 in keylist:
                    print self.matrix.get(key + key2),"\t",
                print
            for key in keylist:
                print max(self.matrix.iterator(prefix=key), key=lambda x: x[1])
            return keylist

    def get_distance_between(self, seqA, seqB):
        dist = self.matrix.get(seqA + seqB)
        if dist:
            return dist
        else:
            return float("-inf")

    def iteritems(self):
        return self.matrix.iterator()

    def iterator(self, prefix=None):
        return self.matrix.iterator(prefix=prefix)

    def __getitem__(self, item):
        return self.matrix.prefixed_db(item)

    def __len__(self):
        return len(self.prefkeys)

    def __iter__(self):
        return self.matrix.iterator(include_value=False)

    def __setitem__(self, key, value):
        self.matrix.put(key, value)

    def __delitem__(self, key):
        for key in self.matrix.iterator(prefix=key, include_value=False):
            self.matrix.delete(key)

    def has_preferred(self):
        return len(self.preferred) > 0

    def get_preferred(self):
        return self.preferred.popleft()

    def remove_col(self, column):
        for pref in self.prefkeys:
            self.matrix.delete(pref + column)

    def remove_row(self, row):
        for key in self.matrix.iterator(prefix=row, include_value=False):
            self.matrix.delete(key)
        if row in self.prefkeys:
            self.prefkeys.remove(row)

    def get(self, key):
        return self.matrix.get(key)

    def put(self, key, value):
        self.matrix.put(key, value)


class MaximizingTSP:


    def __init__(self, adjacencyMatrix):
        self.matrix = adjacencyMatrix

    def invalidate_col(self, column):
        self.matrix.remove_col(column)

    def invalidate_row(self, row):
        # self.matrix[row] = defaultdict(lambda: float("-inf"))
        self.matrix.remove_row(row)

    def get_next_avail_row(self):
        LOWER_BOUND = 0
        for key in self.matrix.prefkeys:
            if max(self.matrix.iterator(prefix=key), key=lambda x: x[1])[1] > LOWER_BOUND:
                print "Arbitrary node: ", key
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

            bestmatch = max(self.matrix.iterator(prefix=current), key=lambda x: x[1])
            # print bestmatch

            if bestmatch[1] <= 0:
                path.append("\n")
                self.invalidate_row(current)
                current = self.get_next_avail_row()
                if current:
                    path.append(current)
                self.invalidate_col(current)
                continue
            elif self.matrix.get(bestmatch[0]) is None:
                path.append("\n")
                self.invalidate_row(current)
                current = self.get_next_avail_row()
                continue

            self.invalidate_col(bestmatch[0])
            self.invalidate_row(current)

            self.matrix.put(bestmatch[0] + current, bytes(float("-inf")))
            path.append(bestmatch[0])
            current = bestmatch[0]

        return path


if __name__ == "__main__":
    # adjmatrix = InMemoryAdjacencyMatrix("../Fasta/reads/real.error.small.fasta.txt", "../Fasta/matrix/real.error.small.matrix")
    # adjmatrix = InMemoryAdjacencyMatrix(sys.argv[1], sys.argv[2])
    adjmatrix = LevelDBAdjacencyMatrix("../Fasta/reads/real.error.small.fasta.txt", "../Fasta/matrix/real.error.small.matrix")
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

