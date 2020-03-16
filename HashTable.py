# implements a chaining hashtable to use as base data structure for storing package & location data
class ChainingHashTable:
    # constructor creates a list of initially empty lists
    # space-time complexity: O(1)
    def __init__(self, initial_cap):
        self.table = []
        for i in range(initial_cap):
            self.table.append([])

    # hash function converts passed-in key value to index value based on table's length
    # space-time complexity: O(1)
    def hash_key(self, key):
        return int(key) % len(self.table)

    # inserts a passed-in value into the appropriate list within the table, according to the passed-in key.
    # See Package.py for package insertion function(create_package_table()) which calls this method.
    # space-time complexity: O(N)
    def insert(self, key, value):
        bucket = self.hash_key(key)
        item = [key, value]
        if self.table[bucket] is None:
            self.table[bucket] = list(item)
            return True
        else:
            for entry in self.table[bucket]:
                if entry[0] == key:
                    entry[1] = item
                    return True
            self.table[bucket].append(item)
            return True

    # replaces existing value with passed-in value at list index corresponding to the passed-in key
    # space-time complexity: O(N)
    def update(self, key, value):
        bucket = self.hash_key(key)
        if self.table[bucket] is None:
            print('Error attempting to update key: ' + key)
        else:
            for entry in self.table[bucket]:
                if entry[0] == key:
                    # value specifically pertaining to package hashtable delivery_status column
                    entry[1][8] = value
                    return True

    # hashtable lookup function: returns value corresponding to passed-in key
    # See Package.py for package lookup function(get_package_info()) which calls this method.
    # space-time complexity: O(N)
    def lookup(self, key):
        bucket = self.hash_key(key)
        if self.table[bucket] is not None:
            for entry in self.table[bucket]:
                if entry[0] == key:
                    return entry[1]
        return None

    # removes a value from the hashtable corresponding to passed-in key
    # space-time complexity: O(N)
    def remove(self, key):
        bucket = self.hash_key(key)
        bucket_list = self.table[bucket]
        if bucket_list is not None:
            for entry in bucket_list:
                if entry[0] == key:
                    bucket_list.remove(entry)
                    return True
        return False
