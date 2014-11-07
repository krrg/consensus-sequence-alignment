consensus-sequence-alignment
============================
## How to compile and run

    make realclean
    make
    ./a.out [inputFile] [outputFile]
    
If you want to record the output:

    make realclean
    make
    ./a.out [inputFile] [outputFile] > logfile.txt

## Info about Speedups
The important function is in `Secali/secali.cpp`.  This is significantly faster than the Python version, even without compiler optimizations.  

I achieve speedups by not allocating the full 2D array of memory, but instead only allocating a 2 rows at the beginning of the function call.  At the end of computing each row, the `current` and `previous` rows are swapped, and the new `current` row is overwritten without requiring a memcpy or malloc.   
