#!/bin/sh

python fasta_to_reads.py ../Fasta/reads/real.error.large.fasta
python fasta_to_reads.py ../Fasta/reads/real.error.small.fasta
python fasta_to_reads.py ../Fasta/reads/synthetic.noerror.small.fasta
python fasta_to_reads.py ../Fasta/reads/synthetic.noerror.large.fasta
python fasta_to_reads.py ../Fasta/reads/synthetic.example.noerror.small.fasta