from HashTable import ChainingHashTable
import csv


# creates 40-key package hashtable and reads in data from package csv file
# space-time complexity: O(N)
def create_package_table():
    package_table = ChainingHashTable(40)
    with open('Package File.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            package_id = row[0]
            street = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            mass = row[6]
            notes = row[7]
            delivery_status = 'At hub'
            entry_value = [package_id, street, city, state, zip_code, deadline, mass, notes, delivery_status]

            key = package_id
            value = entry_value

            package_table.insert(key, value)
    return package_table


# accesses the package hashtable lookup function and prints results for the package ID argument passed in
# space-time complexity: O(N)
def get_package_info(package_table, package_id):
    p_info = package_table.lookup(package_id)
    print('{:<4}{:<30}{:<18}{:<8}{:<5}{:<11}{:<2}'.format(p_info[0], p_info[1][:30], p_info[2], p_info[4], p_info[6],
                                                          p_info[5], p_info[8]))
