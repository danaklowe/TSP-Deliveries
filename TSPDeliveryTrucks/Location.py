from HashTable import ChainingHashTable
import csv


# creates 27-key hashtable and reads in data from location csv file
# space-time complexity: O(N)
def create_location_table():
    loc_table = ChainingHashTable(27)
    with open('Distance Table.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        i = 0
        for row in reader:
            loc_id = i
            loc_description = row[0]
            distances = row[1:]

            key = loc_id
            value = loc_description, distances

            loc_table.insert(key, value)
            i += 1
    return loc_table


# creates 27-key hashtable to associate packages with locations
# space-time complexity: O(N)
def create_loc_package_table(loc_table, package_table):
    loc_pack_table = ChainingHashTable(27)
    for location in loc_table.table:
        for package in package_table.table:
            # checks matching street addresses between loc_table & package_table and populates loc_pack_table with
            # the resulting integers. Each location ID indexes a list of matching package IDs.
            if location[0][1][0] == package[0][1][1]:
                loc_pack_table.table[int(location[0][0])].append(int(package[0][0]))
    return loc_pack_table
