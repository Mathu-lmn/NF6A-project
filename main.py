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
import time
import re
import matplotlib.colors as colors
import matplotlib.cm as cmx
import utils

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

# print(bikes[2].UID)


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
    It takes a new bike and docks it at a specific station
    """
    global bikes
    global stations
    station = int(input('Enter UID of the station you want to dock the new bike: '))
    # UID of the new bike is the next available UID
    bike = str(int(bikes[-1].UID) + 1)
    # If the bike already exists in the system, you can't dock it
    if bike in bikes:
        print('This bike already exists in the system.')
    else:
        df = pd.read_csv('Stations.csv', sep=',')
        df.set_index('UID', inplace=True)
        # if there is no bike in the station, do not put the comma
        if df.at[station, 'Bikes'] == '' or df.at[station, 'Bikes'] == ' ':
            df.at[station, 'Bikes'] = bike
        else:
            df.at[station, 'Bikes'] += f',{bike}'
        df.to_csv('Stations.csv', sep=',')
        # Add the new bike with 100% battery level, 0 days and 0 rents
        df = pd.read_csv('Bikes.csv', sep=',')
        dict_2 = {'UID': bike, 'battery_percent': 100, 'Nb_days': 0, 'Nb_rents': 0}
        dp = pd.DataFrame(dict_2, index={len(dict_2)+1})
        df = pd.concat([df, dp])
        df.to_csv('Bikes.csv', sep=',', index=False, header=True)
        print('Bike added.')
        # Read the modified files and update the class variables
        data = list(csv.reader(open('Stations.csv'), delimiter=','))
        stations = [Stations(i, data[0]) for i in data[1:]]
        data = list(csv.reader(open('Bikes.csv'), delimiter=','))
        bikes = [Bikes(i, data[0]) for i in data[1:]]


#dock_bike()

def display_stations():
    """
    It takes the bikes docked to a station, sorts them by battery level, and then prints them out in a
    descending order
    """
    print('Stations\nUID\tName\t\tPlaces lefts\tBikes')
    for x in range(len(stations)):
        i = stations[x].Bikes.split(',')
        if len(i) == 0:
            print(f'{stations[x].UID}\t{stations[x].Name}\t\t\t')
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
            left = int(stations[x].Max_bikes) - len(i)
            print(f"{stations[x].UID}\t {stations[x].Name}\t{left}\t\t{','.join(i)}")
# display_stations()
    

def rent_bike():
    """
    User will rent a bike from a station, will return it after x minutes to another or the same station.
    """
    bike = input('Enter bike UID: ')
    bike_uid = int(bike)
    arrival_station = int(input('Enter station UID: '))
    battery_lost = int(input('Enter time of rental: ')) * 2
    bikes[int(bike)-1].battery_percent = int(bikes[int(bike)-1].battery_percent) - battery_lost
    if bikes[int(bike)-1].battery_percent < 0:
        print(f"You can't rent this bike for {battery_lost//2} minutes, the maximum time is {(bikes[int(bike)-1].battery_percent + battery_lost)//2} minutes.")
        bikes[int(bike)-1].battery_percent = int(bikes[int(bike)-1].battery_percent) + battery_lost
    else :
        bikes[int(bike)-1].Nb_rents = int(bikes[int(bike)-1].Nb_rents) + 1
        for i in range(0,len(stations)):
            # If the bike is docked to the station, remove it from the station
            if bike in stations[i].Bikes:
                if int(stations[i].UID) == int(arrival_station):
                    stations[i].Nb_returns = int(stations[i].Nb_returns) + 1
                    stations[i].Nb_rents = int(stations[i].Nb_rents) + 1
                    df = pd.read_csv('Stations.csv', sep=',')
                    df.set_index('UID', inplace=True)
                    df.at[arrival_station, 'Nb_rents'] += 1
                    df.at[arrival_station, 'Nb_returns'] += 1
                    df.to_csv('Stations.csv', sep=',')
                    print(f"The bike {bike} is now docked to the station {stations[i].UID}.")
                    break
                else:
                    if len(stations[int(arrival_station)-1].Bikes) > int(stations[int(arrival_station)-1].Max_bikes):
                        print(f"The station {stations[arrival_station-1].UID} is full for now.\nChoose another station please.")
                        break
                    stations[i].Bikes = stations[i].Bikes.replace(bike, ' ')
                    stations[i].Bikes = stations[i].Bikes.replace(', ,', ',')
                    stations[i].Bikes = stations[i].Bikes.replace(', ', '')
                    stations[i].Bikes = stations[i].Bikes.replace(' ,', '')
                    stations[i].Nb_rents = int(stations[i].Nb_rents) + 1
                    departure_station_UID = int(stations[i].UID)
                    departure_station = departure_station_UID - 1
                    # Add the bike to the returning station
                    if int(stations[i].UID) == int(arrival_station):
                        stations[i].Bikes += f',{bike}'
                        stations[i].Nb_returns = int(stations[i].Nb_returns) + 1
                    print(f"The bike {bike} is now docked to the station {arrival_station}.")
                    # Update the CSV files
                    df = pd.read_csv('Stations.csv', sep=',')
                    df.set_index('UID', inplace=True)
                    if df.at[departure_station_UID, 'Bikes'] == '' or df.at[departure_station_UID, 'Bikes'] == ' ':
                        df.at[departure_station_UID, 'Bikes'] = bike
                    else:
                        if df.at[arrival_station, 'Bikes'] == '' or df.at[arrival_station, 'Bikes'] == ' ':
                            df.at[arrival_station, 'Bikes'] = bike
                            stations[arrival_station-1].Bikes = bike
                        else:
                            df.at[arrival_station, 'Bikes'] += f',{bike}'
                            stations[arrival_station-1].Bikes += f',{bike}'
                    df.at[arrival_station, 'Nb_returns'] += 1
                    df.at[departure_station_UID, 'Nb_rents'] += 1
                    df.at[departure_station_UID, 'Bikes'] = stations[departure_station].Bikes
                    df.to_csv('Stations.csv', sep=',')
                    break

        df = pd.read_csv('Bikes.csv', sep=',')
        df.set_index('UID', inplace=True)
        df.at[bike_uid, 'battery_percent'] = int(bikes[int(bike)-1].battery_percent)
        df.at[bike_uid, 'Nb_days'] = int(bikes[int(bike)-1].Nb_days)
        df.at[bike_uid, 'Nb_rents'] = int(bikes[int(bike)-1].Nb_rents)
        df.to_csv('Bikes.csv', sep=',', header=True)


# rent_bike()

def summary():
    """
    Summary of the bikes and stations.
    """
    print("There is currently ", str(len(bikes)), " bikes and " , str(len(stations)), " stations in the system.")
    print("The average battery level is ", round(sum([int(bikes[i].battery_percent) for i in range(len(bikes))])/len(bikes),2), " %.")
    
    print(colored('\nBikes sorted by number of days in use', 'white', attrs=['bold', 'underline']))
    print('UID\tBattery\tNb_returns')
    sorted_bikes_uid1 = sorted(bikes, key=lambda x: int(x.Nb_days), reverse=True)
    for x in range(len(bikes)):
        print(f"{sorted_bikes_uid1[x].UID}\t {sorted_bikes_uid1[x].battery_percent}%\t {sorted_bikes_uid1[x].Nb_days}")
    pass

    print(colored('\nBikes sorted by number of rentals', 'white', attrs=['bold', 'underline']))
    print('UID\tBattery\tNb_returns')    
    sorted_bikes_uid2 = sorted(bikes, key=lambda x: int(x.Nb_rents), reverse=True)
    for x in range(len(bikes)):
        print(f"{sorted_bikes_uid2[x].UID}\t {sorted_bikes_uid2[x].battery_percent}%\t {sorted_bikes_uid2[x].Nb_rents}")
    pass

    print(colored('\nStations sorted by number of rents', 'white', attrs=['bold', 'underline']))
    print('UID\tName\tNb_returns')
    sorted_stations_uid1 = sorted(stations, key=lambda x: int(x.Nb_rents), reverse=True)
    for x in range(len(stations)):
        print(f"{sorted_stations_uid1[x].UID}\t {sorted_stations_uid1[x].Name}\t {sorted_stations_uid1[x].Nb_rents}")
    pass

    print(colored('\nStations sorted by number of returns', 'white', attrs=['bold', 'underline']))
    print('UID\tName\tNb_returns')
    sorted_stations_uid2 = sorted(stations, key=lambda x: int(x.Nb_returns), reverse=True)
    for x in range(len(stations)):
        print(f"{sorted_stations_uid2[x].UID}\t {sorted_stations_uid2[x].Name}\t {sorted_stations_uid2[x].Nb_returns}")
    pass

    G = nx.Graph()
    G.add_node('Depot', pos=(0,0))
    ColorLegend = {'Open': 1,'Full': 3,'Empty': 2, 'Closed':4}
    val_map = {"Depot":4}
    for i in range(0, len(stations)):
        G.add_node(stations[i].UID, pos=(int(stations[i].x_location), int(stations[i].y_location)))
        if utils.str2bool(stations[i].Closed) == True:
            val_map[stations[i].UID] = ColorLegend['Closed']
        elif stations[i].Bikes == '' or stations[i].Bikes == ' ':
            val_map[stations[i].UID] = ColorLegend['Empty']
        elif len(stations[i].Bikes) >= int(stations[i].Max_bikes):
            val_map[stations[i].UID] = ColorLegend['Full']
        else:
            val_map[stations[i].UID] = ColorLegend['Open']
    values = [val_map.get(node, 0) for node in G.nodes()]
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=max(values))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    f = plt.figure(1)
    ax = f.add_subplot(1,1,1)
    for label in ColorLegend:
        ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[label]),label=label)
    
    nx.draw(G, pos=nx.get_node_attributes(G, 'pos'),cmap = jet,vmin=0, vmax= max(values),node_color=values, with_labels=True,ax=ax)
    plt.legend()
    f.tight_layout()
    plt.show()

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
        bikes[defective_bikes[i]-1].battery_percent = 100
        #Update CSV
        df = pd.read_csv('Bikes.csv', sep=',')
        df.set_index('UID', inplace=True)
        print(bikes[defective_bikes[i]-1].UID)
        df.at[int(bikes[defective_bikes[i]-1].UID), 'battery_percent'] = int(bikes[defective_bikes[i]-1].battery_percent)
        df.at[int(bikes[defective_bikes[i]-1].UID), 'Nb_days'] = int(bikes[defective_bikes[i]-1].Nb_days)
        df.to_csv('Bikes.csv', sep=',', header=True)
    # If the bike is not defective, add a day to the bike
    for i in range(0, len(bikes)):
        if bikes[i].UID not in defective_bikes:
            bikes[i].Nb_days = int(bikes[i].Nb_days) + 1
    # Create the list of stations to visit by maintenance
    for i in range(0,len(stations)):
        station_bikes = stations[i].Bikes.split(',')
        for j in range(0,len(defective_bikes)):
            if str(defective_bikes[j]) in station_bikes:
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

def add_station():
    """
    Add a new station to the system.
    """
    global stations
    station_name = input('Enter the name of the new station : ')
    station_xloc = input('Enter the x coordinates : ')
    station_yloc = input('Enter the y coordinates : ')
    station_name = re.sub(r"\s+", '_', station_name)
    station_max = int(input('Enter the maximum number of bikes : '))
    # UID of the new station is the next available UID
    station_uid = str(int(stations[-1].UID) + 1)
    # If the name already exists in the system, you can't add it
    if station_name in [x.Name for x in stations]:
        print(colored('This name already exists in the system', 'red'))
        return
    else:
        # Add the new bike with 100% battery level, 0 days and 0 rents
        df = pd.read_csv('Stations.csv', sep=',')
        dict_2 = {'UID': station_uid, 'x_location': station_xloc, 'y_location': station_yloc, 'Name': station_name, 'Bikes': ' ', 'Nb_rents':0, 'Nb_returns':0, 'Max_bikes': station_max, 'Closed': "False"}
        dp = pd.DataFrame(dict_2, index={len(dict_2)+1})
        df = pd.concat([df, dp])
        df.to_csv('Stations.csv', sep=',', index=False, header=True)
        print('Station added.')
        # Read the modified files and update the class variables
        data = list(csv.reader(open('Stations.csv'), delimiter=','))
        stations = [Stations(i, data[0]) for i in data[1:]]
        data = list(csv.reader(open('Bikes.csv'), delimiter=','))
        bikes = [Bikes(i, data[0]) for i in data[1:]]


#add_station()


def status_station():
    """
    Edit status of a station
    """
    global stations
    station_uid = int(input('Enter station UID: '))
    station_status = input('Type "open" or "close" to define the status of the station : ')
    status = ""
    b_status = ""
    c_status = ""
    if station_status == "open":
        status = "False"
        b_status = "open"
        c_status = "close"
    elif station_status == "close":
        status = "True"
        b_status = "close"
        c_status = "open"
    else:
        print(colored('Invalid status', 'red'))
        return
    df = pd.read_csv('Stations.csv', sep=',')
    df.set_index('UID', inplace=True)
    df.at[int(station_uid), 'Closed'] = status
    df.to_csv('Stations.csv', sep=',', header=True)
    print(f'Station status updated from {c_status} to {b_status}.')
    # Read the modified files and update the class variables
    data = list(csv.reader(open('Stations.csv'), delimiter=','))
    stations = [Stations(i, data[0]) for i in data[1:]]
    data = list(csv.reader(open('Bikes.csv'), delimiter=','))
    bikes = [Bikes(i, data[0]) for i in data[1:]]


#status_station()


# Create a user panel in the terminal to navigate through the program
def user_panel():
    """
    User panel to navigate through the program.
    """
    print(colored('\nWelcome to the bike rental program!', 'green', attrs=['bold', 'underline']))
    print('\nPlease select an option:\n1. Rent a bike\n2. Dock a bike\n3. Display the stations\n4. Add a station\n5. Summary\n6. Execute the maintenance of the defective bikes\n7. Setup the status of a station\n',colored('\r8. Exit', 'red', attrs=['bold']))
    choice = input('\nEnter your choice: ')

    # if choice is not int or not in range 1-8, ask again
    while not choice.isdigit() or int(choice) not in range(1,9):

        print(colored('\nPlease enter a valid choice!', 'red', attrs=['bold']))
        user_panel()
    else:
        match int(choice):
            case 1:
                rent_bike()
            case 2:
                dock_bike()
            case 3:
                display_stations()
            case 4:
                add_station()
            case 5:
                summary()
            case 6:
                maintenance_defective_bikes()
            case 7:
                status_station()
            case 8:
                print(colored('\nThank you for using the bike rental program!', 'red', attrs=['reverse']))
                exit()
        print("Showing panel in 5 seconds...")
        time.sleep(4)
        print("Executing the user panel...")
        time.sleep(1)
        user_panel()


user_panel()