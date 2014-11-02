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

void compute_overlap_matrix(const std::vector<std::string>& reads, std::vector<int_fast16_t>& output_matrix)
{
    uint_least64_t row = 0;
    for (std::string readA : reads)
    {
        for (std::string readB : reads)
        {
            output_matrix.push_back(get_score(readA, readB, 2));
        }
        if (row % 1 == 0)
        {
            std::cout << "Handled " << row << " of " << reads.size() << std::endl;
        }
        row += 1;

    }
}

void write_matrix(const std::string& outfile, std::vector<int_fast16_t>& output_matrix)
{
    std::ofstream ofile(outfile);
    for (int_fast16_t n : output_matrix)
    {
        ofile << n << ' ';
    }
    ofile.close();
}

/*
 *
 */
int main(int argc, char** argv)
{
    const std::string input_file = "/home/krr428/Downloads/19.fastq.txt";

    std::vector<int_fast16_t> output_matrix;
    std::vector<std::string> reads;

    get_reads_from_file(input_file, reads);
    compute_overlap_matrix(reads, output_matrix);
    write_matrix("/home/krr428/Downloads/19.fastq.matrix.txt", output_matrix);



    return 0;
}

