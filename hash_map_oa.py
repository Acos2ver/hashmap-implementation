# Name: Olivia Choi
# OSU Email: choio@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/12/25
# Description: The hash table dynamic array uses Open Addressing with Quadratic Probing
# for resolving the collision. It must be run in average O(1) runtime complexity.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Using hash map quadratic probing, refresh the state of key-value pair.
        If load factor (lambda) is equal to or greater than 0.5, the table is resized
        """
        # Resize is needed or not
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Check the index location at first
        start_index = self._hash_function(key) % self._capacity
        first_tomb = None

        # Search the bucket by using quadratic probing
        for j in range(self._capacity):
            index = (start_index + j * j) % self._capacity
            hash_item = self._buckets[index]

            # Check empty or tombstone for insertion
            if hash_item is None:
                target = first_tomb if first_tomb is not None else index
                self._buckets[target] = HashEntry(key, value)
                self._size += 1
                return

            # Check and save the tombstone
            elif hash_item.is_tombstone:
                if first_tomb is None:
                    first_tomb = index

            # Refresh
            elif hash_item.key == key:
                hash_item.value = value
                return

        # Adding item into first tombstone after retrieve
        if first_tomb is not None:
            self._buckets[first_tomb] = HashEntry(key, value)
            self._size += 1
            return

        # Just in case, what error comes from
        raise Exception("Hash table is full")


    def resize_table(self, new_capacity: int) -> None:
        """
        Modify the hash table capacity without tombstones
        """
        # Check for using the new capacity correctly
        if new_capacity < self._size:
            return

        # new_capacity is prime or not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Make new and save previous one
        prev_buckets = self._buckets
        self._capacity = new_capacity
        self._size = 0

        # Clear the buckets for new
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Refresh all
        for i in range(prev_buckets.length()):
            hash_item = prev_buckets[i]
            if hash_item is not None and not hash_item.is_tombstone:
                self.put(hash_item.key, hash_item.value)

    def table_load(self) -> float:
        """
        Presenting the hash table load factor from calculating.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        The result is how many empty buckets in hash table.
        """
        empty_hash = 0
        for i in range(self._capacity):
            if self._buckets[i] is None:
                empty_hash += 1

        return empty_hash

    def get(self, key: str) -> object:
        """
        Using quadratic probing, presenting the value from provided key.
        """
        # Checking the index
        start_index = self._hash_function(key) % self._capacity

        # Using quadratic probing to find
        for j in range(self._capacity):
            index = (start_index + j * j) % self._capacity
            hash_item = self._buckets[index]

            # Empty if key does not exist
            if hash_item is None:
                return None

            # Matching key-value pair
            if hash_item.key == key and not hash_item.is_tombstone:
                return hash_item.value

        # Nothing to match
        return None

    def contains_key(self, key: str) -> bool:
        """
        True for key in the hash map, False if nothing.
        """
        if self._size == 0:
            return False

        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Target key removed, and then replace the tombstone into it.
        """
        # Using quadratic probing, find the target
        start_index = self._hash_function(key) % self._capacity

        for j in range(self._capacity):
            index = (start_index + j * j) % self._capacity
            hash_item = self._buckets[index]

            # No target, empty
            if hash_item is None:
                return

            # Deleting the target and replace tombstone
            if hash_item.key == key and not hash_item.is_tombstone:
                hash_item.is_tombstone = True
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Presenting all active key-value pairs as tuple in a dynamic array.
        """
        result = DynamicArray()

        # Retrieve all
        for i in range(self._capacity):
            hash_item = self._buckets[i]
            if hash_item is not None and not hash_item.is_tombstone:
                result.append((hash_item.key, hash_item.value))

        return result

    def clear(self) -> None:
        """
        Empty hash map without any changes.
        """
        self._size = 0

        for i in range(self._capacity):
            self._buckets[i] = None

    def __iter__(self):
        """
        Use only stored item for iterating.
        """
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Search for next slot, if tombstone exists then skip.
        """
        while self._iter_index < self._capacity:
            hash_item = self._buckets[self._iter_index]
            self._iter_index += 1

            # Presenting only stored items
            if hash_item is not None and not hash_item.is_tombstone:
                return hash_item

        # End
        raise StopIteration


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
