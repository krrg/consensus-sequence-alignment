consensus-sequence-alignment
============================

## About the sequence aligner

The aligner is currently a complex program composed of multiple modules written in C++, Python, and Java.  The general workflow is:

    Fasta/Fastq -----> Reads File ------> Matrix ------> Alignment File -------> Contigs
                            |                            ^
                            L----------------------------|
                            
A Fasta or Fastq file is first converted into a reads file.  The reads file is converted into a matrix file, which contains the alignment scores pertaining to each read against every other read in the reads file.  The reads file and the matrix file is then used to compute the alignment file, which is an ordered listing of reads in tail-head ordering.  The alignment file can then be formed into a contigs file.

## Running a complete workflow.

Say that you have a FASTA file named myreads.fasta.  To assemble these reads into contigs:

 
First, convert into a straight reads file:


    python Util/fasta_to_reads.py myreads.fasta
   


Next, compute submatrices from reads file: (the second argument to Secali is the prefix with which the reads files will be named) 


    cd Secali && make clean
    ./a.out ../myreads.fasta.txt ../myreads
    cd ..


Combine submatrices to form a single matrix file:


    python submatrix_to_matrix.py myreads
    

Run the TSP algorithm on the matrix file (two options):
#### Option 1 -- In memory (somewhat faster, not as reliable):


    python tsp_greedy.py myreads.fasta.txt myreads.matrix > TSPOUTPUT.txt


#### Option 2 -- On disk (slower but very reliable) (uses LevelDB):


    java -jar Utils/tsp_ldb_java/out/artifacts/tsp_ldb_java_jar/tsp_ldb_java.jar myreads.fasta.txt myreads.matrix > TSPOUTPUT.txt
    
    
We currently recommend Option 2, since it prints out intermediate results and does not seem to have issues crashing.
  
To run the final step of the assembler and get the assembled contigs:

    python Util/tsp_to_contigs.py TSPOUTPUT.txt OUTPUT_CONTIGS.txt
     


# Other notes
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

## Requirements

* C++11 capable compiler, with pthreads library.
* Python 2.7  (Python 2.6 is not necessarily supported for some steps)

##### On Disk TSP Algorithm:
* Java 1.7
* LevelDB library and headers


