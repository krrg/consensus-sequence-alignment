/*
 * File:   main.cpp
 * Author: krr428
 *
 * Created on October 30, 2014, 7:36 PM
 */

#include <cstdlib>
#include <fstream>
#include <iostream>
#include "secali.h"
#include <vector>
#include <string>

void get_reads_from_file(const std::string& fileReads, std::vector<std::string>& reads)
{
    std::ifstream ifile(fileReads);
    while (ifile)
    {
        std::string line;
        std::getline(ifile, line);
        if (line != "\n" && line != "")
        {
            reads.push_back(line);
        }
    }
    ifile.close();
    std::cout << "Finished reading input file." << std::endl;
}

void compute_overlap_matrix(const std::vector<std::string>& reads, const std::string& output_file)
{
    uint_least64_t row = 0;
    std::ofstream ofile(output_file);
    
    for (std::string readA : reads)
    {
        std::vector<int_fast16_t> output_row;
        for (std::string readB : reads)
        {
            int_fast16_t score = get_score(readA, readB, 2);
            output_row.push_back(score);
        }
        for (int_fast16_t n: output_row)
        {
            ofile << n << '\t';
        }
        ofile << std::endl;        
        std::cout << "Handled " << ++row << " of " << reads.size() << std::endl;

    }
    
    ofile.close();
}

//void write_matrix(const std::string& outfile, std::vector<int_fast16_t>& output_matrix, int num_cols)
//{
//    int i = 0;
//    std::ofstream ofile(outfile);
//    for (int_fast16_t n : output_matrix)
//    {
//        ofile << n << ' ';
//        if (i++ == num_cols)
//        {
//            ofile << std::endl;
//            i = 0;
//        }
//    }
//    ofile.close();
//}

/*
 *
 */
int main(int argc, char** argv)
{
//    const std::string input_file = "../Fasta/real.error.large.fasta.txt";
//    const std::string input_file = "../Fasta/test.txt";
    const std::string input_file(argv[1]);

    std::vector<int_fast16_t> output_matrix;
    std::vector<std::string> reads;

    get_reads_from_file(input_file, reads);
    compute_overlap_matrix(reads, argv[2]);

    return 0;
}

