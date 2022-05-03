import csv

class Bikes:
   def __init__(self, row, header):
       self.__dict__ = dict(zip(header, row)) 
   def __repr__(self):
       return self.UID

data = list(csv.reader(open('Bikes.csv')))
bikes = [Bikes(i, data[0]) for i in data[1:]]

print(bikes[2].UID)


class Stations:
   def __init__(self, row, header):
       self.__dict__ = dict(zip(header, row)) 
   def __repr__(self):
       return self.UID

data = list(csv.reader(open('Stations.csv')))
stations = [Stations(i, data[0]) for i in data[1:]]

print(stations[3].Location)

# stationsfile = 'Stations.csv'
# def import_stations(stationsfile):
#     """
#     Import all the stations from the file.
#     """
#     with open(stationsfile) as csvfile:
#         reader = csv.reader(csvfile, delimiter=',')
#         for row in reader:
#             station = Stations()
#             station.UID = row[0]
#             station.Name = row[1]
#             station.Location = [list(row[2])]
#             station.Bikes = [list(row[3])]
#             station.Nb_rents = row[4]
#             station.Nb_returns = row[5]
#         return station

# bikefile = 'Bikes.csv'
# def import_bikes(bikefile):
#     """
#     Import all the bikes from the file.
#     """
#     with open(bikefile) as csvfile:
#         reader = csv.reader(csvfile, delimiter=',')
#         for row in reader:
#             bike = Bikes()
#             bike.UID = row[0]
#             bike.Battery_percent = row[1]
#             bike.Nb_days = row[2]
#             bike.Nb_rents = row[3]
#         return bike

def dock_bike(station, bike):
    """
    Dock a bike at a station.
    """
    # TODO
    pass

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