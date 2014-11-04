/* 
 * File:   secali.h
 * Author: krr428
 *
 * Created on October 30, 2014, 7:26 PM
 */

#ifndef SECALI_H
#define	SECALI_H

#include <string>
#include <stdint.h>
#include <algorithm>
#include <iostream>
#include <cstring>

int_fast16_t get_score(const std::string& left_str, const std::string& top_str, const int& indel);

#endif	/* SECALI_H */

