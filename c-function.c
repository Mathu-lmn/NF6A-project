#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
int j = 1;
int i = 0;

typedef struct key_value
{
    int UID;
    int x_locations;
    int y_locations;
} dict;

int main()
{
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
    // printf("%d", values[1].x_locations);
}

float dist(dict a, dict b) {
    return sqrt(pow(a.x_locations - b.x_locations, 2) + pow(a.y_locations - b.y_locations, 2));
}

int tsp_with_coords(int stations_to_visit[], size_t size, dict values[]) {
    int cost[size][size];
    int visited[size];
    int costs = 0;
    int order[size];

    for (int i = 0; i < size; i++)
        visited[i] = 0;

    for (int i = 0; i < size; i++){
        for (int j = 0; j < size; j++){
            cost[i][j] = dist(values[stations_to_visit[i]], values[stations_to_visit[j]]);
        }
    }

    for (int i = 0; i < size; i++){
        int min = INT_MAX;
        int min_index = -1;
        for (int j = 0; j < size; j++){
            if (visited[j] == 0 && cost[i][j] < min){
                min = cost[i][j];
                min_index = j;
                order[i] = min_index;
            }
        }
        costs += min;
        visited[min_index] = 1;
    }
    return order;
}