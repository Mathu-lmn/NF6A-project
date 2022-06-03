/**
 * @file c-function.h
 * @author Mathurin Lemoine
 * @brief C function used for the computation of the solution
 * @version 1.0
 * @date 03/06/2022 
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/**
 * @brief Function that returns the path of the TSP
 * @param[in] stations_to_visit : List of stations to visit
 * @param[in] size : Size of the list of stations to visit
 * @param[out] order : The order of the stations to visit
 * @return The path of the TSP
 */
void tsp_with_coords(int stations_to_visit[], size_t size, int order[]);