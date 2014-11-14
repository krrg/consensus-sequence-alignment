#!/usr/bin/env python

import sys
import time
aa = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]


def printMatrix2(testMatrix):
    print ' ',
    for i in range(len(testMatrix[1])):  # Make it work with non square matrices.
        print i,
    print
    for i, element in enumerate(testMatrix):
        print str(i), str(''.join(str(element)))


class overlap_aligner():
    def __init__(self):

        self.GAP_PENALTY = -2
        self.MATCH_SCORE = 1

        self.best_score = -1
        self.max_score_coor = []

        self.score_matrix = None
        self.backtracking = None

    def assemble(self, input, outputfile):
        assembled_contigs = []
        with open(input) as f:
            output = open(outputfile, 'w')
            startline = f.next().strip()
            contig = list(startline)
            for line in f:
                print "line = ",line
                if not line.strip(): #break the current contig
                    print "breaking contig"
                    output.write(''.join(contig)+'\n')
                    contig = list(f.next().strip())
                    print "contig = ",contig
                else: #we continue
                    self.align(contig[-100:], line) #align the last 100 chunk of our comparison with the new line.
                    #lets see if we have a best alignment.. if not break. and get new contig
                    if(self.best_score < 25):
                        output.write(''.join(contig))
                        contig = list(line)
                        self.best_score = -1
                        self.max_score_coor = []
                    else:
                        contig = contig[0:-100] + list(self.backtrack(''.join(contig[-100:]), line))
                        self.best_score = -1
                        self.max_score_coor = []
            output.write(''.join(contig)+'\n')

    def align(self, s1, s2):
        print "aligning "
        self.backtracking = [[0 for j in range(len(s1)+1)] for i in range(len(s2)+1)]
        self.score_matrix = [[0 for j in range(len(s1)+1)] for i in range(len(s2)+1)]
        for i, x in enumerate(s2):
            i += 1
            for j, y in enumerate(s1):
                j += 1
                down_score = self.score_matrix[i-1][j] + self.GAP_PENALTY
                right_score = self.score_matrix[i][j-1] + self.GAP_PENALTY
                mismatch_score = self.score_matrix[i-1][j-1] + self.GAP_PENALTY
                maximum = max(down_score, right_score, mismatch_score)
                if( x==y ): #we got a match
                    self.score_matrix[i][j] = self.score_matrix[i-1][j-1] + self.MATCH_SCORE
                    self.backtracking[i][j] = "D" #mismatch
                elif (mismatch_score >= maximum):
                    self.score_matrix[i][j] = mismatch_score
                    self.backtracking[i][j] = "D" #mismatch
                elif (right_score >= maximum):
                    self.score_matrix[i][j] = right_score
                    self.backtracking[i][j] = "L"
                else: #go down
                    self.score_matrix[i][j] = down_score
                    self.backtracking[i][j] = "U"
                if( self.score_matrix[i][j] >= self.best_score and j == len(s1)):
                   #print "got a best score"
                    self.best_score = self.score_matrix[i][j]
                    self.max_score_coor = [i,j]

    def backtrack(self, s1, s2):
        #print s1
        #print s2
        #print self.best_score
        #print self.max_score_coor
        y = self.max_score_coor[0] # s1
        x = self.max_score_coor[1] # s2
        master_align = ""
        align_s1 = ""
        align_s2 = ""
        score = 0
        #printMatrix2(self.backtracking)
        #print "y = ",y
        #print "x = ",x
        while self.backtracking[y][x] != 0:
            if self.backtracking[y][x] == "D": # a match
                align_s1 = s1[x-1] + align_s1
                align_s2 = s2[y-1] + align_s2
                master_align = s2[y-1] + master_align
                x -= 1
                y -= 1
            elif(self.backtracking[y][x] == "L"):
                align_s2 = "-" + align_s2
                align_s1 = s1[x-1] + align_s1
                master_align = s1[x-1] + master_align
                x -= 1
            elif(self.backtracking[y][x] == "U"):
                align_s2 = s2[y-1] + align_s2
                align_s1 = "-" + align_s1
                master_align = s2[y-1] + master_align
                y -= 1
        #now we need to tack on the beginning and end parts..
        master_align = ''.join(s1[0:x]) + master_align
        master_align = master_align + ''.join(s2[self.max_score_coor[0]:-1])
        #print "y = ",y
        #print "x = ",x
        print self.best_score
        #print align_s1
        #print align_s2
        #print s1
        #print s2
        print "master = ",master_align
        return master_align

oa = overlap_aligner()
oa.assemble( sys.argv[ 1 ] , sys.argv[ 2 ]) #input, output