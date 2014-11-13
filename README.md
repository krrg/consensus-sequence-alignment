consensus-sequence-alignment
============================

## About the sequence aligner

The aligner is currently a complex program composed of multiple modules written in C++, Python, and Java.  The general workflow is:

    Fasta/Fastq -----> Reads File ------> Matrix ------> Alignment File -------> Contigs
                            |                            ^
                            L----------------------------|
                            
A Fasta or Fastq file is first converted into a reads file.  The reads file is converted into a matrix file, which contains the alignment scores pertaining to each read against every other read in the reads file.  The reads file and the matrix file is then used to compute the alignment file, which is an ordered listing of reads in tail-head ordering.  The alignment file can then be formed into a contigs file.

## How to compile and run Secali

    make realclean
    make
    ./a.out [inputFile] [outputFile]
    
If you want to record the output:

    make realclean
    make
    ./a.out [inputFile] [outputFile] > logfile.txt

## Info about Speedups
The important function is in `Secali/secali.cpp`.  This is significantly faster than the Python version, even without compiler optimizations.  

We achieve speedups by not allocating the full 2D array of memory, but instead only allocating a 2 rows at the beginning of the function call.  At the end of computing each row, the `current` and `previous` rows are swapped, and the new `current` row is overwritten without requiring a memcpy or malloc.   
