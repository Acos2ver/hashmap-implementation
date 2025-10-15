# HashMap Implementation

A Python implementation of HashMap data structures using two distinct collision resolution strategies: Separate Chaining and Open Addressing with Quadratic Probing.

## Overview

This project demonstrates advanced understanding of hash table implementations, collision resolution techniques, and algorithm optimization. Both implementations support complete CRUD operations with efficient time complexity for core operations.

## Features

### Separate Chaining Implementation
- **Collision Resolution**: Uses singly linked lists for handling hash collisions
- **Dynamic Resizing**: Automatic table resizing to maintain optimal load factor
- **Mode Finding**: Specialized algorithm to find the most frequent key-value pairs

### Open Addressing Implementation
- **Quadratic Probing**: Efficient collision resolution without chaining overhead
- **Iterator Protocol**: Python-style iteration support with `__iter__()` and `__next__()`
- **Tombstone Handling**: Proper deletion management for open addressing

## Core Operations

Both implementations support the following operations:

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| `put(key, value)` | O(1) average | Insert or update key-value pair |
| `get(key)` | O(1) average | Retrieve value by key |
| `remove(key)` | O(1) average | Delete key-value pair |
| `contains_key(key)` | O(1) average | Check if key exists |
| `clear()` | O(n) | Remove all entries |
| `resize_table(capacity)` | O(n) | Rehash all entries to new capacity |
| `get_keys_and_values()` | O(n) | Return all key-value pairs |
| `empty_buckets()` | O(n) | Count empty buckets |
| `table_load()` | O(1) | Calculate current load factor |

## Technical Implementation

### Separate Chaining
```python
# Uses singly linked lists for collision handling
# Supports finding mode (most frequent elements)
def find_mode(self) -> tuple:
    # Returns (dynamic_array, frequency) of most common elements
```

### Open Addressing with Quadratic Probing
```python
# Quadratic probing formula: h(k, i) = (h'(k) + i²) mod m
# Implements Python iterator protocol
def __iter__(self):
    self._index = 0
    return self

def __next__(self):
    # Returns key-value pairs in iteration
```

## Key Features

### Dynamic Resizing
- Automatically resizes when load factor exceeds threshold
- Ensures next capacity is prime number for better hash distribution
- Rehashes all existing entries efficiently

### Load Factor Management
- Tracks ratio of entries to capacity
- Optimal performance maintained through automatic resizing
- Configurable thresholds for different use cases

### Collision Resolution
- **Separate Chaining**: Each bucket contains a linked list
- **Open Addressing**: Uses quadratic probing to find next available slot

## Data Structures Used

- **Dynamic Array**: Custom implementation for underlying storage
- **Singly Linked List**: For separate chaining collision resolution
- **Hash Function**: Provided hash function for key distribution

## Performance Characteristics

### Space Complexity
- Separate Chaining: O(n + m) where n = entries, m = capacity
- Open Addressing: O(m) where m = capacity

### Time Complexity
- Average case: O(1) for all core operations
- Worst case: O(n) when all keys collide (rare with good hash function)

## Project Structure
```
hashmap-implementation/
├── hash_map_sc.py          # Separate Chaining implementation
├── hash_map_oa.py          # Open Addressing implementation
├── a6_include.py           # Helper data structures (Dynamic Array, LinkedList)
└── README.md               # This file
```

## Code Example

### Separate Chaining
```python
from hash_map_sc import HashMap

# Create hash map
hm = HashMap(10)

# Insert key-value pairs
hm.put("key1", 100)
hm.put("key2", 200)

# Retrieve value
value = hm.get("key1")  # Returns 100

# Check load factor
load = hm.table_load()  # Returns 0.2

# Find mode
keys, frequency = hm.find_mode()
```

### Open Addressing
```python
from hash_map_oa import HashMap

# Create hash map
hm = HashMap(10)

# Insert and iterate
hm.put("a", 1)
hm.put("b", 2)

# Use iterator
for key, value in hm:
    print(f"{key}: {value}")
```

## Methods Implemented

### Common Methods (Both Implementations)
- `put(key, value)` - Insert or update
- `get(key)` - Retrieve value
- `remove(key)` - Delete entry
- `contains_key(key)` - Check existence
- `clear()` - Remove all entries
- `resize_table(new_capacity)` - Change capacity
- `get_keys_and_values()` - Return all pairs
- `empty_buckets()` - Count empty slots
- `table_load()` - Calculate load factor

### Separate Chaining Only
- `find_mode()` - Find most frequent elements

### Open Addressing Only
- `__iter__()` - Initialize iterator
- `__next__()` - Get next key-value pair

## Skills Demonstrated

- Advanced data structure implementation
- Hash table collision resolution strategies
- Algorithm optimization and complexity analysis
- Python iterator protocol implementation
- Dynamic memory management
- Prime number utilization for hash distribution
- Test-driven development

## Technical Highlights

- **Efficient Rehashing**: Minimizes overhead during resize operations
- **Prime Capacity**: Uses prime numbers for better hash distribution
- **Tombstone Management**: Handles deletions properly in open addressing
- **Memory Efficiency**: Optimized space usage for both implementations
- **Iterator Pattern**: Pythonic iteration support for open addressing

---

**Project Type**: Academic | **Language**: Python | **Focus**: Data Structures & Algorithms
