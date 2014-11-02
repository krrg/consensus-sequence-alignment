#!/bin/sh

python fasta_to_reads.py ../Fasta/real.error.large.fasta
python fasta_to_reads.py ../Fasta/real.error.small.fasta
python fasta_to_reads.py ../Fasta/synthetic.noerror.small.fasta
python fasta_to_reads.py ../Fasta/synthetic.noerror.large.fasta
python fasta_to_reads.py ../Fasta/synthetic.example.noerror.small.fasta