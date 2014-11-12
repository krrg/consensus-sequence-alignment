#!/bin/bash

cd ../Secali && make clean && make

./a.out ../Fasta/reads/real.error.large.fasta.txt ../Fasta/matrix/real.error.large. && \
./a.out ../Fasta/reads/real.error.small.fasta.txt ../Fasta/matrix/real.error.small. && \
./a.out ../Fasta/reads/synthetic.example.noerror.small.fasta.txt ../Fasta/matrix/synthetic.example.noerror.small. && \
./a.out ../Fasta/reads/synthetic.noerror.large.fasta.txt ../Fasta/matrix/synthetic.noerror.large. && \
./a.out ../Fasta/reads/synthetic.noerror.small.fasta.txt ../Fasta/matrix/synthetic.noerror.small. && \

cd ../Utils

python submatrix_to_matrix.py ../Fasta/matrix/real.error.large && \
python submatrix_to_matrix.py ../Fasta/matrix/real.error.small && \
python submatrix_to_matrix.py ../Fasta/matrix/synthetic.example.noerror.small && \
python submatrix_to_matrix.py ../Fasta/matrix/synthetic.noerror.large && \
python submatrix_to_matrix.py ../Fasta/matrix/synthetic.noerror.small

