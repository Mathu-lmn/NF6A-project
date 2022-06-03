"""!
@file main.py
@brief Main file of the project.
@author Mathurin Lemoine
@date 2022
@version 1.0
"""
import csv
import ctypes as ct
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from termcolor import colored

def open_dll(name='./testlib.dll'):
    """!
    Load the c library.
    @param name: Name of the DLL file.
    @return: The library.
    """
    return ct.CDLL(name)

c_lib = open_dll()



class Bikes:
    """
    Class to manage the bikes.
    """
    def __init__(self, row, header):
        """!
        Constructor of the class.
        @param row: Row of the CSV file.
        @param header: Header of the CSV file.
        """
        self.__dict__ = dict(zip(header, row)) 
    def __repr__(self):
        """!
        Representation of the class.
        @return: String.
        """
        return self.UID

data = list(csv.reader(open('Bikes.csv'), delimiter=','))
bikes = [Bikes(i, data[0]) for i in data[1:]]

#print(bikes[2].UID)


class Stations:
    """
    Class to manage the stations.
    """
    def __init__(self, row, header):
        """!
        Constructor of the class.
        @param row: Row of the CSV file.
        @param header: Header of the CSV file.
        """
        self.__dict__ = dict(zip(header, row)) 
    def __repr__(self):
        """!
        Representation of the class.
        @return: String.
        """
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
        stations[i].Bikes += f',{j}'
#dock_bike()

def display_stations():
    """
    Display all stations and the bikes docked to it in a descending order according to their battery level.
    """
    print('Stations\nUID\tName\t\tBikes')
    for x in range(len(stations)):
        i = stations[x].Bikes.split(',')
        if len(i) == 1:
            print(f"{stations[x].UID}\t {stations[x].Name}\t {stations[x].Bikes}")
        else:
            for y in range(len(i)-1):
                for j in range(0,len(i)-y-1):
                    # Sort the bikes by battery level
                    if int(bikes[int(i[j])-1].battery_percent) < int(bikes[int(i[j+1])-1].battery_percent):
                        k = i[j+1]
                        i[j+1] = bikes[int(i[j])-1].UID
                        i[j] = bikes[int(k)-1].UID
                    else:
                        pass
            print(f"{stations[x].UID}\t {stations[x].Name}\t {','.join(i)}")

# display_stations()
    

def rent_bike():
    """
    User will rent a bike from a station, will return it after x minutes to another or the same station.
    """
    bike = input('Enter bike UID: ')
    arrival_station = int(input('Enter station UID: '))
    battery_lost = int(input('Enter time of rental: ')) * 2

    bikes[int(bike)-1].battery_percent = int(bikes[int(bike)-1].battery_percent) - battery_lost
    if bikes[int(bike)-1].battery_percent < 0:
        print(f"You can't rent this bike for {battery_lost//2} minutes.")
        bikes[int(bike)-1].battery_percent = int(bikes[int(bike)-1].battery_percent) + battery_lost
    else :
        bikes[int(bike)-1].Nb_rents = int(bikes[int(bike)-1].Nb_rents) + 1
        for i in range(0,len(stations)):
            # If the bike is docked to the station, remove it from the station
            if bike in stations[i].Bikes:
                stations[i].Bikes = stations[i].Bikes.replace(bike, ' ')
                stations[i].Bikes = stations[i].Bikes.replace(', ,', ',')
                stations[i].Bikes = stations[i].Bikes.replace(', ', '')
                stations[i].Bikes = stations[i].Bikes.replace(' ,', '')
                stations[i].Nb_rents = int(stations[i].Nb_rents) + 1
            # Add the bike to the returning station
            if int(stations[i].UID) == int(arrival_station):
                stations[i].Bikes += f',{bike}'
                stations[i].Nb_returns = int(stations[i].Nb_returns) + 1


#rent_bike()
#display_stations()

def summary():
    """
    Summary of the bikes and stations.
    """
    print('\nBikes sorted by number of days in use\nUID\tBattery\tNb_days')
    sorted_bikes_uid1 = sorted(bikes, key=lambda x: int(x.Nb_days), reverse=True)
    for x in range(len(bikes)):
        print(f"{sorted_bikes_uid1[x].UID}\t {sorted_bikes_uid1[x].battery_percent}\t {sorted_bikes_uid1[x].Nb_days}")
    pass

    print('\nBikes sorted by number of rentals\nUID\tBattery\tNb_rents')
    sorted_bikes_uid2 = sorted(bikes, key=lambda x: int(x.Nb_rents), reverse=True)
    for x in range(len(bikes)):
        print(f"{sorted_bikes_uid2[x].UID}\t {sorted_bikes_uid2[x].battery_percent}\t {sorted_bikes_uid2[x].Nb_rents}")
    pass

    print("\nStations sorted by number of rents\nUID\tName\t\tNb_rents")
    sorted_stations_uid1 = sorted(stations, key=lambda x: int(x.Nb_rents), reverse=True)
    for x in range(len(stations)):
        print(f"{sorted_stations_uid1[x].UID}\t {sorted_stations_uid1[x].Name}\t {sorted_stations_uid1[x].Nb_rents}")
    pass

    print("\nStations sorted by number of returns\nUID\tName\t\tNb_returns")
    sorted_stations_uid2 = sorted(stations, key=lambda x: int(x.Nb_returns), reverse=True)
    for x in range(len(stations)):
        print(f"{sorted_stations_uid2[x].UID}\t {sorted_stations_uid2[x].Name}\t {sorted_stations_uid2[x].Nb_returns}")
    pass

# summary()


def maintenance_defective_bikes():
    """
    Maintenance of all the defective bikes entered by the user.
    """
    defective_bikes = []
    stations_visit = []
    nb_def_bikes = int(input('Enter number of defective bikes: '))
    for i in range(0, nb_def_bikes):
        defective_bikes.append(int(input('Enter UID of the bike: ')))
    # Resetting the nb days of defective bikes
    for i in range(0, nb_def_bikes):
        bikes[defective_bikes[i]-1].Nb_days = 0
    # If the bike is not defective, add a day to the bike
    for i in range(0, len(bikes)):
        if bikes[i].UID not in defective_bikes:
            bikes[i].Nb_days = int(bikes[i].Nb_days) + 1
    # Create the list of stations to visit by maintenance
    for i in range(0,len(stations)):
        for j in range(0,len(defective_bikes)):
            if str(defective_bikes[j]) in stations[i].Bikes and int(stations[i].UID) not in stations_visit:
                stations_visit.append(int(stations[i].UID))
    stations_visit = list(dict.fromkeys(stations_visit))
    array = (ct.c_int * len(stations_visit))(*stations_visit)
    result = (ct.c_int * len(stations_visit))()
    # Execute the tsp algorithm
    c_lib.tsp_with_coords(array, len(stations_visit), result)
    for i in range(0, len(result)):
        print(f"{stations[int(result[i])-1].UID}\t {stations[int(result[i])-1].Name}")

    # Use networkx to display the graph of the result path using coordinates and starting from (0,0) and going back to (0,0)
    G = nx.Graph()
    G.add_node('Depot', pos=(0,0))
    for i in range(0, len(stations)):
        G.add_node(stations[i].UID, pos=(int(stations[i].x_location), int(stations[i].y_location)))
    # Add edges to the graph using the result path
    G.add_edge('Depot', stations[int(result[0])-1].UID, weight=0)
    for i in range(0, len(result)):
        if i < len(result)-1:
            G.add_edge(stations[int(result[i])-1].UID, stations[int(result[i+1])-1].UID, weight=1)
        else:
            G.add_edge(stations[int(result[i])-1].UID, 'Depot', weight=0)
    nx.draw(G, pos=nx.get_node_attributes(G, 'pos'), with_labels=True)
    plt.show()


# maintenance_defective_bikes()

# Create a user panel in the terminal to navigate through the program
def user_panel():
    """
    User panel to navigate through the program.
    """
    print(colored('\nWelcome to the bike rental program!', 'green', attrs=['bold', 'underline']))
    print('\nPlease select an option:\n1. Rent a bike\n2. Dock a bike\n3. Display the stations\n4. Summary\n5. Execute the maintenance of the defective bikes\n',colored('\r6. Exit', 'red', attrs=['bold']))
    while True:
        try:
            choice = int(input('\nEnter your choice: '))
            if choice == 1:
                rent_bike()
                user_panel()
            elif choice == 2:
                dock_bike()
                user_panel()
            elif choice == 3:
                display_stations()
                user_panel()
            elif choice == 4:
                summary()
                user_panel()
            elif choice == 5:
                maintenance_defective_bikes()
                user_panel()
            elif choice == 6:
                print('\nThank you for using the bike rental program!')
                break
            else:
                print('\nPlease enter a valid choice!')
                user_panel()
        except ValueError:
            print('\nPlease enter a valid choice!')
            user_panel()
user_panel()