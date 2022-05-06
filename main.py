import csv
from tempfile import tempdir
import pandas as pd


class Bikes:
   def __init__(self, row, header):
       self.__dict__ = dict(zip(header, row)) 
   def __repr__(self):
       return self.UID

data = list(csv.reader(open('Bikes.csv'), delimiter=','))
bikes = [Bikes(i, data[0]) for i in data[1:]]

#print(bikes[2].UID)


class Stations:
   def __init__(self, row, header):
       self.__dict__ = dict(zip(header, row)) 
   def __repr__(self):
       return self.UID

data = list(csv.reader(open('Stations.csv'), delimiter=','))
stations = [Stations(i, data[0]) for i in data[1:]]


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
#df = pd.read_csv('Stations.csv', sep=',')
#dock_bike()

def display_stations():
    """
    Display all stations and the bikes docked to it in a descending order according to their battery level.
    """
    print('Stations\nUID\tLocation\tBikes')
    for x in range(len(stations)):
        i = stations[x].Bikes.split(',')
        if len(i) == 1:
            print(f"{stations[x].UID}\t {stations[x].Location}\t {stations[x].Bikes}")
        else:
            for y in range(len(i)-1):
                for j in range(0,len(i)-y-1):
                    #print(f"in for loop {i} and j is {j}, bike {i[j]} has a battery level of {bikes[int(i[j])-1].battery_percent}, bike {i[j+1]} has a battery level of {bikes[int(i[j+1])-1].battery_percent}")
                    if int(bikes[int(i[j])-1].battery_percent) < int(bikes[int(i[j+1])-1].battery_percent):
                        k = i[j+1]
                        i[j+1] = bikes[int(i[j])-1].UID
                        i[j] = bikes[int(k)-1].UID
                    else:
                        pass
            print(f"{stations[x].UID}\t {stations[x].Location}\t {','.join(i)}")

#display_stations()
    

def rent_bike(station, bike):
    """
    User will rent a bike from a station, will return it after x minutes to another or the same station.
    """
    bike = input('Enter bike UID: ')
    arrival_station = input('Enter station UID: ')
    rental_time = input('Enter time of rental: ')
    

def maintenance_defective_bikes():
    """
    Maintenance of all the defective bikes.
    """
    # TODO
    pass