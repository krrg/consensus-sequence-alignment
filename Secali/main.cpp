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
#include <thread>

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

void compute_overlap_matrix(const std::vector<std::string>& reads, const std::string& output_file, int start_offset, int skip)
{
    uint_least64_t row = 0;
    std::ofstream ofile(output_file);

    for (int i = start_offset; i < reads.size(); i += skip)
    {
        const std::string readA = reads.at(i);
        std::vector<int_fast16_t> output_row;
        for (const std::string readB : reads)
        {
            int_fast16_t score = get_score(readA, readB, 2);
            output_row.push_back(score);
        }
        for (int_fast16_t n : output_row)
        {
            ofile << n << '\t';
        }
        ofile << std::endl;
        if (++row % 10 == 0)
        {
            std::cout << "Thread " << start_offset << " handled " << row << " of " << reads.size() / skip << std::endl;
        }
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

void begin_manage_threads(const std::vector<std::string>& reads, int num_threads, const std::string& filename_prefix)
{
    std::thread * thread_pool[num_threads];
    for (int i = 0; i < num_threads; i++)
    {
        //compute_overlap_matrix(reads, filename_prefix + std::to_string(i) + ".submatrix", i, num_threads);
        thread_pool[i] = new std::thread(compute_overlap_matrix, reads, filename_prefix + std::to_string(i) + ".submatrix", i, num_threads);
        std::cout << "Started " << thread_pool[i]->get_id() << std::endl;
    }

    for (int i = 0; i < num_threads; i++)
    {
        thread_pool[i]->join();
        delete thread_pool[i];
    }
}

/*
 *
 */
int main(int argc, char** argv)
{
    //    const std::string input_file = "../Fasta/real.error.large.fasta.txt";
    //    const std::string input_file = "../Fasta/test.txt";
    const std::string input_file(argv[1]);

    std::vector<std::string> reads;

    get_reads_from_file(input_file, reads);
    //    compute_overlap_matrix(reads, argv[2]);
    begin_manage_threads(reads, 16, argv[2]);

    return 0;
}

