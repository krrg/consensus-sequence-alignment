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


/*
 * 
 */
int main(int argc, char** argv)
{
    std::ifstream infile("inputText.txt");
    
    std::string seqA;
    std::string seqB;
    
    std::getline(infile, seqA);
    std::getline(infile, seqB);
    
    std::cout << get_score(seqA, seqB, 2);
    
    return 0;
}

