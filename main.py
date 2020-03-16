# Project Author: Dana K Lowe | dlowe47@wgu.edu

from Truck import Truck
import Timer
import Package

# takes 8AM start time, user input delivery status "check time", and creates corresponding datetime object
check_time = Timer.delivery_status_timer()

# creates Truck objects, each with its own name, departure time, location hash table, etc.
truck_1 = Truck('Truck 1', "08:00:01")
truck_2 = Truck('Truck 2', "10:05:01")
truck_3 = Truck('Truck 3', "09:05:01")

# creates route using location & package CSV files, prioritization, randomization, and nearest neighbor algorithm.
truck_1.create_route()
# parses best available route, updates truck time & distance, and updates delivery status of relevant packages
truck_1.deliver_packages(check_time)

truck_3.create_route()
truck_3.deliver_packages(check_time)

truck_2.create_route()
truck_2.deliver_packages(check_time)

# calculates and prints sum of all route distances
total_distance = truck_1.tour_distance + truck_2.tour_distance + truck_3.tour_distance
print('\n{:.1f} total miles.\n'.format(total_distance))

print('Package status as of', check_time, '...\n')
print('{:<4}{:<30}{:<18}{:<8}{:<5}{:<11}{:<2}'.format('ID', 'Street', 'City', 'Zip', 'Kgs', 'Deadline', 'Delivery '
                                                                                                        'Status'))
# accesses hashtable lookup function to print status of all packages as of the user-specified check time
for entry in Truck.package_table.table:
    Package.get_package_info(Truck.package_table, entry[0][0])
