import csv
import pandas as pd


class Bikes:
   def __init__(self, row, header):
       self.__dict__ = dict(zip(header, row)) 
   def __repr__(self):
       return self.UID

data = list(csv.reader(open('Bikes.csv'), delimiter=','))
bikes = [Bikes(i, data[0]) for i in data[1:]]

print(bikes[2].UID)


class Stations:
   def __init__(self, row, header):
       self.__dict__ = dict(zip(header, row)) 
   def __repr__(self):
       return self.UID

data = list(csv.reader(open('Stations.csv'), delimiter=','))
stations = [Stations(i, data[0]) for i in data[1:]]

print(stations[3].Location)


def dock_bike():
    """
    Dock a bike at a specific station.
    """
    is_docked = False
    i = int(input('Enter station UID: ')) -1
    j = str(input('Enter bike UID: '))
    df = pd.read_csv('Stations.csv', sep=',')
    for x in range(len(df)):
        if j in df.loc[x,'Bikes']:
            print("The bike is already docked to another station.")
            is_docked = True
        else:
            pass
    if is_docked == False:    
        df.iloc[i,3] = df.iloc[i,3] + ',' + str(j)
    df.to_csv('Stations.csv', index=False)

# print(pd.read_csv('Stations.csv', sep=','))
df = pd.read_csv('Stations.csv', sep=',')
dock_bike()

def display_stations_and_bikes():
    """
    Display all stations and bikes.
    """
    # TODO
    pass

def rent_bike(station, bike):
    """
    Rent a bike from a station.
    """
    # TODO
    pass

def maintenance_defective_bikes():
    """
    Maintenance of all the defective bikes.
    """
    # TODO
    pass