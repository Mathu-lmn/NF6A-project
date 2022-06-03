/**
 * @file c-function.c
 * @author Mathurin Lemoine
 * @brief Solving the TSP problem with the C language
 * @version 1.0
 * @date 03/06/2022
 */

#include "c-function.h" 
int j = 1;
int i = 0;

/**
 * @brief Structure containing the informations about a station
 * @param UID : Unique ID of the station
 * @param x_locations : x-coordinate of the station
 * @param y_locations : y-coordinate of the station
 */
typedef struct key_value
{
    int UID;
    int x_locations;
    int y_locations;
} dict;

/**
 * @brief Function to calculate the distance between two stations
 * @param[in] a : Station 1
 * @param[in] b : Station 2
 * @return The distance between the two stations
 */
float dist(dict a, dict b) {
    return sqrt(pow(a.x_locations - b.x_locations, 2) + pow(a.y_locations - b.y_locations, 2));
}

/**
 * @brief Function that returns the path of the TSP
 * @param[in] stations_to_visit : List of stations to visit
 * @param[in] size : Size of the list of stations to visit
 * @param[out] order : The order of the stations to visit
 * @return The path of the TSP
 */
void tsp_with_coords(int stations_to_visit[], size_t size, int order[]) {
    // Opening the file containing the informations about the stations and storing them in the structure previously defined
    FILE *fp;
    char *token;
    fp = fopen("Stations.csv", "r");
    if (fp == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }
    char buffer[1024];
    for (char c = getc(fp); c != EOF; c = getc(fp))
    {
        if (c == '\n')
        {
            j++;
        }
    }
    dict values[j + 1];
    int i = 0;
    rewind(fp);
    while (fgets(buffer, 200, fp) != NULL)
    {
        values[i].UID = atoi(strtok(buffer, ","));
        values[i].x_locations = atoi(strtok(NULL, ","));
        values[i].y_locations = atoi(strtok(NULL, ","));
        i++;
    }
    fclose(fp);
    // If the size of the list of stations to visit is 1, the path is the only station
    if (size == 1) {
        order[0] = stations_to_visit[0];
        return;
    }
    // Defining the matrix of distances between the stations
    int cost[size][size];
    for (int i = 0; i < size; i++){
        for (int j = 0; j < size; j++){
            cost[i][j] = dist(values[stations_to_visit[i]], values[stations_to_visit[j]]);
        }
    }
// Finding the minimum cost path
    int min_cost_path[size];
    int min_cost = INT_MAX;
    int min_cost_path_index = 0;
    for (int i = 0; i < size; i++){
        int cost_path[size];
        cost_path[0] = stations_to_visit[i];
        int cost_path_index = 1;
        int cost_path_total = 0;
        // Finding the cost of the path
        for (int j = 0; j < size; j++){
            if (j == i){
                continue;
            }
            cost_path[cost_path_index] = stations_to_visit[j];
            cost_path_index++;
            cost_path_total += cost[i][j];
        }
        // If the cost of the path is lower than the minimum cost, the minimum cost is updated and the path is stored
        if (cost_path_total < min_cost){
            min_cost = cost_path_total;
            min_cost_path_index = i;
            for (int k = 0; k < size; k++){
                min_cost_path[k] = cost_path[k];
            }
        }
    }
    // Storing the path in the order array
    order[0] = min_cost_path[0];
    for (int i = 1; i < size; i++){
        order[i] = min_cost_path[i];
    }
}