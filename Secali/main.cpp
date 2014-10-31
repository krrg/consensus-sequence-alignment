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

using namespace std;

enum Directions
{
    Right,
    Down,
    Diagonal
};

class DynamicMaximizer
{
private:
    std::string left_str;
    std::string top_str;
    int_fast8_t indel;
    int_fast16_t* prev_row;
    int_fast16_t* current_row;


public:

    DynamicMaximizer(std::string seq1, std::string seq2, int_fast8_t indel)
    {
        this->left_str = seq1;
        this->top_str = seq2;
        this->indel = indel;
        this->prev_row = new int_fast16_t[this->top_str.size() + 1];
        this->current_row = new int_fast16_t[this->top_str.size() + 1];
    }

    int_fast16_t get_score()
    {
        std::memset(this->prev_row, 0, sizeof (int_fast16_t) * this->top_str.size() + 1);
        this->current_row[0] = 0;
        
        for (uint_fast16_t row = 1; row < this->left_str.size() + 1; ++row)
        {
            for (uint_fast16_t col = 1; col < this->top_str.size() + 1; ++col)
            {
                int opt_down = this->prev_row[col] - this->indel;
                int opt_side = this->current_row[col - 1] - this->indel;
                int opt_diag = this->left_str[row - 1] == this->top_str[col - 1] ? this->prev_row[col - 1] + 1 : this->prev_row[col - 1] - 2;

                this->current_row[col] = std::max(opt_diag, std::max(opt_side, opt_down));
            }
            std::swap(this->prev_row, this->current_row);
        }
        
        int_fast16_t max_alignment = 0;
        for (uint_fast16_t col = 1; col < this->top_str.size() + 1; ++col)
        {
            if (this->prev_row[col] > max_alignment)
            {
                max_alignment = this->prev_row[col];
            }
        }
        return max_alignment;
        
    }

    ~DynamicMaximizer()
    {
        delete [] this->prev_row;
        delete [] this->current_row;
    }

};

/*
 *
 */
int main(int argc, char** argv)
{
    cout << DynamicMaximizer("PAWHEAE", "HEAGAWGHEE", 5).get_score() << endl;
}

