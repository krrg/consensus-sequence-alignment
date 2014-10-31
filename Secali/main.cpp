/* 
 * File:   main.cpp
 * Author: krr428
 *
 * Created on October 30, 2014, 5:13 PM
 */

#include <string>
#include <stdint.h>
#include <algorithm>

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
    int_fast16_t* nodes;


public:

    DynamicMaximizer(std::string seq1, std::string seq2, int_fast8_t indel)
    {
        this->left_str = seq1;
        this->top_str = seq2;
        this->indel = indel;
    }

    void __prepare_dp_table()
    {
        this->nodes = int_fast16_t[this->left_str.size() + 1][this->top_str.size() + 1];
        for (uint_fast16_t row = 0; row < this->left_str.size() + 1; ++row)
        {
            for (uint_fast16_t col = 0; col < this->top_str.size() + 1; ++col)
            {
                if (row == 0 || col == 0)
                {
                    this->nodes[row][col] = 0;
                    continue;
                }

                int opt_down = this->nodes[row - 1][col - 1] - this->indel;
                int opt_side = this->nodes[row][col - 1] - this->indel;
                int opt_diag = this->left_str[row - 1] == this->top_str[col - 1] ? this->nodes[row - 1][col - 1] + 1 : this->nodes[row - 1][col - 1] - 2;
                
                this->nodes[row][col] = std::max(opt_diag, std::max(opt_side, opt_down));
            }
        }
    }

};

/*
 * 
 */
int main(int argc, char** argv)
{

    return 0;
}

