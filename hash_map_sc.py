# Name: Olivia Choi
# OSU Email: choio@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/12/25
# Description: The goal is to implement a HashMap using a DynamicArray for buckets,
# with a linked list in each bucket to manage collisions.
# Collisions are resolved by chaining, using a prime number of buckets for uniform distribution,
# designed for an average runtime complexity of O(1).
# Bad case must be run in O(N) runtime complexity.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Creates a hash map entry by inserting or updating a key-value pair.
        If load factor (lambda) is equal to or greater than 1, the table is resized.
        """
        # Checking if resizing is needed
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # Finding bucket location
        index_hash = self._hash_function(key) % self._capacity
        bucket_hash = self._buckets[index_hash]

        # Checking if key already exists
        current_node = bucket_hash.contains(key)
        if current_node:
            current_node.value = value
            return

        # key not found, add new key-value pair
        bucket_hash.insert(key, value)
        self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to new capacity and rehashes all existing key-value pairs
        with prime number.
        """
        # Create new_capacity or not
        if new_capacity < 1:
            return

        # Make sure the prime number in new_capacity
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Save previous bucket for new
        prev_buckets = self._buckets
        self._capacity = new_capacity
        self._size = 0

        # Empty for new buckets
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Existing pair must be rehashed
        for i in range(prev_buckets.length()):
            current_node = prev_buckets[i]
            for node in current_node:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        It represents the load factor of hash table from computing.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Check the number of hash table empty buckets.
        """
        empty_hash = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_hash += 1

        return empty_hash

    def get(self, key: str) -> object:
        """
        Showing the key-value pair or nothing if no match.
        """
        # Searching for the target location
        index_hash = self._hash_function(key) % self._capacity
        bucket_hash = self._buckets[index_hash]

        # Checking the key location
        current_node = bucket_hash.contains(key)
        if current_node:
            return current_node.value

        # Nothing matches
        return None

    def contains_key(self, key: str) -> bool:
        """
        True for key in the hash map, False nothing matches.
        """
        if self._size == 0:
            return False

        # Checking key existence
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Hash map removes the target key-value pair.
        If the key is not present, do nothing.
        """
        # Checking the target location
        index_hash = self._hash_function(key) % self._capacity
        bucket_hash = self._buckets[index_hash]

        # Checking the key location
        if bucket_hash.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Presenting current key-value pairs as a tuple to a dynamic array.
        """
        result = DynamicArray()

        # Retrieve all
        for i in range(self._capacity):
            linked_list = self._buckets[i]
            for node in linked_list:
                result.append((node.key, node.value))

        return result

    def clear(self) -> None:
        """
        Empty hash map with same capacity.
        """
        # Initialize the table size
        self._size = 0

        # Empty all
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Presenting a tuple with computing the mode value in DynamicArray and
    find the highest frequency.
    Must run in average O(N) runtime complexity.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # Checking the individual frequency
    for i in range(da.length()):
        each_element = da[i]
        current_number = map.get(each_element)
        if current_number is None:
            map.put(each_element, 1)
        else:
            map.put(each_element, current_number + 1)

    # Checking the highest frequency
    max_frequency = 0
    tuples = map.get_keys_and_values()
    for i in range(tuples.length()):
        key, value = tuples[i]
        if value > max_frequency:
            max_frequency = value

    # Get the all highest frequency
    result = DynamicArray()
    for i in range(tuples.length()):
        key, value = tuples[i]
        if value == max_frequency:
            result.append(key)

    return result, max_frequency


# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
