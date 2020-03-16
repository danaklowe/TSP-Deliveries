from HashTable import ChainingHashTable
import Location
import Package
import datetime
import random


class Truck:
    # creates a hashtable each for package info, location info, and for mapping package IDs to location IDs
    package_table = Package.create_package_table()
    loc_table = Location.create_location_table()
    loc_pack_table = Location.create_loc_package_table(loc_table, package_table)

    # Truck constructor creates object-specific name, location hashtable, route distance & timer, package list,
    # and list of location sets
    # space-time complexity: O(1)
    def __init__(self, name, current_time):
        self.name = name
        today = datetime.datetime.today()
        time_obj = datetime.datetime.strptime(current_time, '%H:%M:%S').time()
        self.current_time = datetime.datetime.combine(today, time_obj)
        self.destination_table = ChainingHashTable(len(Truck.loc_table.table))
        self.loc_list = []
        self.tour_distance = 0
        self.package_set_list = [set() for _ in range(30)]

    def create_route(self):
        self.screen_packages()
        self.map_packages_to_locations()
        self.determine_best_route()

    # Selects packages to load based on delivery deadlines, required groupings, flight delays, etc. Results in list
    # of 30 sets across 30 semi-randomized iterations. Each set first selects for delivery priority and/or
    # constraints before adding additional, randomly-selected package IDs up to the limit of 16 packages.
    # space-time complexity: O(N^2)
    def screen_packages(self):
        all_packages = set(range(1, len(Truck.package_table.table) + 1))
        high_priority_packages = set()
        priority_packages = set()
        regular_packages = set()
        non_deliverables = set()
        today = datetime.datetime.today()

        # removes from the delivery pool all currently non-deliverable packages
        # space-time complexity: O(N^2)
        for pack_id in all_packages:
            pack_value = Truck.package_table.lookup(str(pack_id))
            if pack_value is not None and (
                    (self.current_time < today.replace(hour=10, minute=5, second=0) and 'Wrong address' in pack_value[
                        7]) or
                    (self.current_time < today.replace(hour=9, minute=5, second=0) and 'Delayed' in pack_value[7]) or
                    (('Truck 1' or 'Truck 3') in self.name and 'truck 2' in pack_value[7]) or (
                            'At hub' not in pack_value[8])):
                for pack_list in Truck.loc_pack_table.table:
                    if pack_id in pack_list:
                        non_deliverables.update(set(pack_list))
                        break
        all_packages -= non_deliverables

        # removes from the delivery pool all packages that must be delivered together
        # space-time complexity: O(N^2)
        for pack_id in all_packages:
            pack_value = Truck.package_table.lookup(str(pack_id))
            if pack_value is not None:
                if 'Must be delivered with' in pack_value[7]:
                    codeliveries = [int(s) for s in pack_value[7].split() if s.isdigit()]
                    high_priority_packages.update(codeliveries)
                    for pack_list in Truck.loc_pack_table.table:
                        if (pack_id in pack_list) or any(x in pack_list for x in codeliveries):
                            high_priority_packages.update(set(pack_list))
        all_packages -= high_priority_packages

        # removes from the delivery pool all packages with morning deadlines
        # space-time complexity: O(N^2)
        for pack_id in all_packages:
            pack_value = Truck.package_table.lookup(str(pack_id))
            if pack_value is not None:
                if '9:00' in pack_value[5] or '10:30' in pack_value[5]:
                    for pack_list in Truck.loc_pack_table.table:
                        if pack_id in pack_list:
                            priority_packages.update(set(pack_list))
                            break
        all_packages -= priority_packages

        # removes from the delivery pool all remaining packages
        # space-time complexity: O(N^2)
        for pack_id in all_packages:
            pack_value = Truck.package_table.lookup(str(pack_id))
            if pack_value is not None:
                for pack_list in Truck.loc_pack_table.table:
                    if pack_id in pack_list:
                        regular_packages.update(set(pack_list))
                        break
        all_packages -= regular_packages

        # reloads delivery pool with priority packages
        all_packages.update(high_priority_packages)
        all_packages.update(priority_packages)

        # creates 30 randomly loaded package sets with priority-package preference and max load size of 16
        # space-time complexity: O(N^2)
        for i in range(30):
            rand_pack_load = all_packages.copy()
            # selects additional packages if space left in truck
            if len(rand_pack_load) < 16:
                rem_spots = 16 - len(rand_pack_load)
                spots_too_small = False
                # selects randomly first from priority packages
                while rem_spots > 0 and not spots_too_small:
                    spots_too_small = True
                    qualified_pack_lists = []
                    for pack_list in Truck.loc_pack_table.table:
                        # checks if list of packages at a location is subset of priority packages & not subset of
                        # packages already loaded. If so, adds it to qualified packages list from which a random
                        # grouping of packages(all sharing the same delivery address) is selected
                        if set(pack_list).issubset(priority_packages) and set(pack_list).isdisjoint(
                                rand_pack_load) and rem_spots >= len(pack_list) > 0:
                            qualified_pack_lists.append(pack_list)
                            spots_too_small = False
                    if len(qualified_pack_lists) > 0:
                        rand_pack_index = random.randrange(len(qualified_pack_lists))
                        rand_pack_list = qualified_pack_lists[rand_pack_index]
                        rand_pack_load.update(rand_pack_list)
                        rem_spots -= len(rand_pack_list)

                spots_too_small = False
                # if there are still spots on the truck remaining after loading priority packages, randomly selects
                # from regular packages
                while rem_spots > 0 and not spots_too_small:
                    spots_too_small = True
                    qualified_pack_lists = []
                    for pack_list in Truck.loc_pack_table.table:
                        # checks if list of packages at a location is subset of regular packages & not subset of
                        # packages already loaded. If so, adds it to qualified packages list from which a random
                        # grouping of packages(all sharing the same delivery address) is selected
                        if set(pack_list).issubset(regular_packages) and set(pack_list).isdisjoint(
                                rand_pack_load) and rem_spots >= len(pack_list) > 0:
                            qualified_pack_lists.append(pack_list)
                            spots_too_small = False
                    if len(qualified_pack_lists) > 0:
                        rand_pack_index = random.randrange(len(qualified_pack_lists))
                        rand_pack_list = qualified_pack_lists[rand_pack_index]
                        rand_pack_load.update(rand_pack_list)
                        rem_spots -= len(rand_pack_list)

            # removes packages if too many loaded onto truck
            else:
                # randomly removes package groupings until total package amount <= 16 load limit, preferentially
                # removing non-priority packages
                while len(rand_pack_load) > 16:
                    if rand_pack_load.issubset(high_priority_packages.union(priority_packages)):
                        pack_to_remove = random.sample(rand_pack_load, 1)[0]
                        for pack_list in Truck.loc_pack_table.table:
                            if int(pack_to_remove) in pack_list:
                                rand_pack_load -= set(pack_list)
                    else:
                        removables = rand_pack_load.difference(high_priority_packages.union(priority_packages))
                        pack_to_remove = random.sample(removables, 1)[0]
                        for pack_list in Truck.loc_pack_table.table:
                            if int(pack_to_remove) in pack_list:
                                rand_pack_load -= set(pack_list)

            # assigns this iteration's semi-random package set to an index in the object's list field.
            self.package_set_list[i] = rand_pack_load

    # iterates through 30 randomized package ID sets to produce 30 corresponding location ID sets
    # space-time complexity: O(N^2)
    def map_packages_to_locations(self):
        for i in range(len(self.package_set_list)):
            dest_table = ChainingHashTable(len(Truck.loc_table.table))
            # inserts hub location and distances from it into destination hashtable
            dest_table.insert(0, (Truck.loc_table.lookup(0))[1])
            # inserts into destination hashtable only locations(and their corresponding distances) who will receive
            # packages with IDs in the set.
            # space-time complexity: O(N^2)
            for package_id in self.package_set_list[i]:
                for loc_pack_list in Truck.loc_pack_table.table:
                    loc_pack_index = Truck.loc_pack_table.table.index(loc_pack_list)
                    if package_id in loc_pack_list and dest_table.lookup(loc_pack_index) is None:
                        dest_table.insert(loc_pack_index, (Truck.loc_table.lookup(loc_pack_index))[1])
            loc_list = []
            # re-formats destination hashtable into pairings of a location ID and a list of tuples of neighbors & their
            # distances from that location
            # space-time complexity: O(N^2)
            for bucket in dest_table.table:
                if len(bucket) > 0:
                    # adds only location id to loc_list
                    loc_list.append(bucket[0][0])
                    new_list = []
                    for j, elem in enumerate(bucket[0][1]):
                        tup = (j, float(elem))
                        new_list.append(tup)
                    bucket[0][1] = new_list
            # filters out from the table all locations with no packages being delivered this particular route
            # final result in the following form: [[[0, [(0, 0.0), (2, 3.8),...]]], [], [[2, [(0, 3.8), (2, 0.0),...[]]
            # space-time complexity: O(N^2)
            for bucket in dest_table.table:
                if len(bucket) > 0:
                    new_list = []
                    table_entry = dest_table.lookup(bucket[0][0])
                    for tup in table_entry:
                        if tup[0] in loc_list:
                            new_list.append(tup)
                    bucket[0][1] = new_list

            # creates a list containing each randomized list of locations and their corresponding neighbors & distances
            tup = i, dest_table
            self.loc_list.append(tup)

    # takes in 30 location sets and returns 30 routes with distances, then sorts & selects shortest route
    # space-time complexity: O(N^2)
    def determine_best_route(self):
        distance_list = []
        for i in range(len(self.loc_list)):
            current_loc = 0
            # list indicating all locations visited thus far
            trial_tour = [current_loc]
            trial_tour_distance = 0

            # loops while current_loc has unvisited neighbors(ie. not yet in trial_tour list)
            while len(set([adj_loc for (adj_loc, distance) in self.loc_list[i][1].lookup(current_loc)]).difference(
                    set(trial_tour))) > 0:
                min_distance_adj = None
                min_distance = None
                # iterates through list of tuples of each neighboring location & its corresponding distance
                for each_adj_loc, each_adj_distance in self.loc_list[i][1].lookup(current_loc):
                    # ensures trial_tour not standing still or revisiting already-visited locations
                    if each_adj_loc != current_loc and each_adj_loc not in trial_tour:
                        # finds the closest neighboring location across all iterations of the for loop
                        if min_distance is not None:
                            if min_distance > each_adj_distance:
                                min_distance = each_adj_distance
                                min_distance_adj = each_adj_loc
                        else:
                            min_distance = each_adj_distance
                            min_distance_adj = each_adj_loc
                closest_adj_loc = (min_distance_adj, min_distance)
                # visits closest neighboring location
                trial_tour.append(closest_adj_loc[0])
                # reassigns current_loc to the closest neighboring location
                current_loc = closest_adj_loc[0]
                # increments trial_tour's total travel distance
                trial_tour_distance += closest_adj_loc[1]
            # return to hub once all locations visited
            trial_tour.append(0)
            trial_tour_distance += self.loc_list[i][1].lookup(current_loc)[0][1]

            trial_tuple = i, trial_tour_distance
            distance_list.append(trial_tuple)
        distance_list.sort(key=lambda tup: tup[1])
        # selects the 1st tuple(route #, distance) in sorted distance_list
        shortest_route = distance_list[0]

        # assigns to truck's final destination table the shortest route's (of 30 trials) destination table
        self.destination_table = self.loc_list[shortest_route[0]][1]

    # Nearest neighbor heuristic algorithm that iterates through all locations in the hashtable to find the closest
    # neighbors, adds those neighbors to the tour list, and adds their "edges" to the total tour distance. Repeats
    # process with closest location until all locations visited.
    # space-time complexity: O(N^2)
    def deliver_packages(self, check_time):
        # ensures route does not begin after user-entered check time.
        if self.current_time > check_time:
            return 0

        # updates package status as truck begins delivery route
        # space-time complexity: O(N^2)
        for bucket in self.destination_table.table:
            if len(bucket) > 0:
                for package in Truck.loc_pack_table.table[bucket[0][0]]:
                    Truck.package_table.update(str(package), 'In route to destination')

        # flag indicating user-specified check-time occurs while route still being processed
        out_for_delivery = False
        current_loc = 0
        # list indicating all locations visited thus far
        tour = [current_loc]
        tour_time = self.current_time

        # continues looping while current_loc's neighbors not yet visited(ie. not yet in tour list). Difference
        # between unvisited locations & tour list approaches 0 as locations are added to the tour list in each loop
        # iteration.
        # space-time complexity: O(N^2)
        while len(set([adj_loc for (adj_loc, distance) in self.destination_table.lookup(current_loc)]).difference(
                set(tour))) > 0:
            min_distance_adj = None
            min_distance = None
            # iterates through list of tuples of each neighboring location & its corresponding distance
            for each_adj_loc, each_adj_distance in self.destination_table.lookup(current_loc):
                # ensures tour not standing still or revisiting already-visited locations
                if each_adj_loc != current_loc and each_adj_loc not in tour:
                    # checks if location has a package due soon and adds location to tour regardless of distance
                    if self.package_due_soon(each_adj_loc):
                        tour.append(each_adj_loc)
                        self.tour_distance += each_adj_distance
                        if tour_time + datetime.timedelta(seconds=(each_adj_distance / 18.0) * 3600.0) > check_time:
                            out_for_delivery = True
                            break
                        tour_time += datetime.timedelta(seconds=(each_adj_distance / 18.0) * 3600.0)
                        current_loc = each_adj_loc
                        # updates status of all packages with destinations corresponding to this location's location ID
                        for package_id in Truck.loc_pack_table.table[current_loc]:
                            Truck.package_table.update(str(package_id),
                                                       'Delivered at ' + str(tour_time.strftime("%H:%M:%S")))
                        continue

                    # finds the closest neighboring location across all iterations of the for loop
                    if min_distance is not None:
                        if min_distance > each_adj_distance:
                            min_distance = each_adj_distance
                            min_distance_adj = each_adj_loc
                    else:
                        min_distance = each_adj_distance
                        min_distance_adj = each_adj_loc
            if out_for_delivery:
                break
            closest_adj_loc = (min_distance_adj, min_distance)
            # calculates seconds elapsed traveling the current edge
            edge_seconds = (closest_adj_loc[1] / 18.0) * 3600.0
            # if latest delivery will put tour time past user-specified end time, cancels delivery of package & breaks
            # out of loop
            if tour_time + datetime.timedelta(seconds=edge_seconds) > check_time:
                out_for_delivery = True
                break
            # adds closest neighboring location to the tour (ie. visits closest neighbor)
            tour.append(closest_adj_loc[0])
            # reassigns current_loc to the closest neighboring location
            current_loc = closest_adj_loc[0]
            # increments tour's total travel distance
            self.tour_distance += closest_adj_loc[1]
            # increments tour's current datetime value by seconds elapsed this edge
            tour_time += datetime.timedelta(seconds=edge_seconds)
            # updates status of all packages with destinations corresponding to this location's location ID
            for package_id in Truck.loc_pack_table.table[current_loc]:
                Truck.package_table.update(str(package_id), 'Delivered at ' + str(tour_time.strftime("%H:%M:%S")))
        # returning to hub
        if not out_for_delivery:
            tour.append(0)
            self.tour_distance += self.destination_table.lookup(current_loc)[0][1]

        self.current_time = tour_time
        tour_minutes = (self.tour_distance / 18.0) * 60

        # prints route-specific data
        print(self.name + ' - Location IDs:', end=' ')
        print('{:<60}'.format(str(tour)), end='')
        print('{:.0f} miles.\t'.format(self.tour_distance), end='')
        print('{:.0f} minutes.'.format(tour_minutes))
        if out_for_delivery:
            print('Delivery still underway...')

    # checks location to see if has packages due within next 30 minutes
    # space-time complexity: O(N)
    def package_due_soon(self, each_adj_loc):
        pack_list = Truck.loc_pack_table.table[each_adj_loc]
        if len(pack_list) > 0:
            for package in pack_list:
                if '9:00' in Truck.package_table.lookup(str(package))[5]:
                    deadline = self.current_time.replace(hour=9, minute=0, second=0)
                    # if deadline within 30 minutes after current_time, return True
                    if (deadline > self.current_time) and (deadline - self.current_time).seconds / 60 < 30:
                        return True
                elif '10:30' in Truck.package_table.lookup(str(package))[5]:
                    deadline = self.current_time.replace(hour=10, minute=30, second=0)
                    # if deadline within 30 minutes after current_time, return True
                    if (deadline > self.current_time) and (deadline - self.current_time).seconds / 60 < 30:
                        return True
            return False
