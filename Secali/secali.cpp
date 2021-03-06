/*
 * File:   main.cpp
 * Author: krr428
 *
 * Created on October 30, 2014, 5:13 PM
 */

#include <string>
#include <stdint.h>
#include <algorithm>
#include <iostream>
#include <cstring>

#define MINIMUM_OVERLAP 5

int_fast16_t get_score(const std::string& left_str, const std::string& top_str, const int& indel)
{
    int_fast16_t* prev_row = new int_fast16_t[top_str.size() + 1];
    int_fast16_t* current_row = new int_fast16_t[top_str.size() + 1];
    

    std::memset(prev_row, 0, sizeof(int_fast16_t) * (top_str.size() + 1));
    current_row[0] = 0;

    for (int_fast16_t row = 1; row < left_str.size() + 1; ++row)
    {
        for (int_fast16_t col = 1; col < top_str.size() + 1; ++col)
        {
            int_fast16_t opt_down = prev_row[col] - indel;
            int_fast16_t opt_side = current_row[col - 1] - indel;
            int_fast16_t opt_diag = left_str[row - 1] == top_str[col - 1] ? prev_row[col - 1] + 1 : prev_row[col - 1] - 2;

            current_row[col] = std::max(opt_diag, std::max(opt_side, opt_down));
        }
        std::swap(prev_row, current_row);
    }

    int_fast16_t max_alignment = 0;
    
    
    
    for (int_fast16_t col = MINIMUM_OVERLAP; col < top_str.size() + 1; ++col)
    {
        if (prev_row[col] > max_alignment)
        {
            max_alignment = prev_row[col];
        }
    }
    
    delete [] prev_row;
    delete [] current_row;

    return max_alignment;        
}


