#include "c-function.h" 
int j = 1;
int i = 0;


typedef struct key_value
{
    int UID;
    int x_locations;
    int y_locations;
} dict;

float dist(dict a, dict b) {
    return sqrt(pow(a.x_locations - b.x_locations, 2) + pow(a.y_locations - b.y_locations, 2));
}

void tsp_with_coords(int stations_to_visit[], size_t size, int order[]) {

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

    if (size == 1) {
        order[0] = stations_to_visit[0];
        return;
    }

    int cost[size][size];
    for (int i = 0; i < size; i++){
        for (int j = 0; j < size; j++){
            cost[i][j] = dist(values[stations_to_visit[i]], values[stations_to_visit[j]]);
        }
    }
// now we want to find the minimum cost path
    int min_cost_path[size];
    int min_cost = INT_MAX;
    int min_cost_path_index = 0;
    for (int i = 0; i < size; i++){
        int cost_path[size];
        cost_path[0] = stations_to_visit[i];
        int cost_path_index = 1;
        int cost_path_total = 0;
        for (int j = 0; j < size; j++){
            if (j == i){
                continue;
            }
            cost_path[cost_path_index] = stations_to_visit[j];
            cost_path_index++;
            cost_path_total += cost[i][j];
        }
        if (cost_path_total < min_cost){
            min_cost = cost_path_total;
            min_cost_path_index = i;
            for (int k = 0; k < size; k++){
                min_cost_path[k] = cost_path[k];
            }
        }
    }
    order[0] = min_cost_path[0];
    for (int i = 1; i < size; i++){
        order[i] = min_cost_path[i];
    }
}

// void main(){
//     int stations_to_visit[] = {1, 2, 3};
//     int order[3];
//     tsp_with_coords(stations_to_visit, 3, order);
//     for (int i = 0; i < 3; i++) {
//         printf("%d\n", order[i]);
//     }
// }
