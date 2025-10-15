# HashMap Implementation

Python implementation of hash tables using two collision resolution strategies: Separate Chaining and Open Addressing with Quadratic Probing.

## Overview

This project demonstrates proficiency in data structures and algorithm design through efficient hash table implementations. Both versions support complete CRUD operations with O(1) average time complexity.

## Features

### Separate Chaining
- Uses singly linked lists for collision handling
- Dynamic resizing with automatic load factor management
- Mode-finding algorithm for most frequent key-value pairs

### Open Addressing (Quadratic Probing)
- Efficient collision resolution without chaining overhead
- Python iterator protocol (`__iter__`, `__next__`)
- Tombstone handling for proper deletion management

## Core Operations

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| `put(key, value)` | O(1) average | Insert or update |
| `get(key)` | O(1) average | Retrieve value |
| `remove(key)` | O(1) average | Delete entry |
| `contains_key(key)` | O(1) average | Check existence |
| `resize_table()` | O(n) | Rehash all entries |

## Technical Highlights

- **Dynamic Resizing**: Automatic table resizing using prime capacities for optimal hash distribution
- **Collision Strategies**: Implemented both chaining and open addressing approaches
- **Iterator Pattern**: Pythonic iteration support for traversing hash map
- **Performance Optimization**: Efficient rehashing and load factor management

## Usage
```python
from hash_map_sc import HashMap

hm = HashMap(10)
hm.put("key1", 100)
value = hm.get("key1")  # Returns 100

# Find most frequent elements
keys, frequency = hm.find_mode()
```

## Methods Implemented

**Both Implementations:**
`put()`, `get()`, `remove()`, `contains_key()`, `clear()`, `resize_table()`, `get_keys_and_values()`, `empty_buckets()`, `table_load()`

**Separate Chaining Only:** `find_mode()`

**Open Addressing Only:** `__iter__()`, `__next__()`

## Skills Demonstrated

- Data structure implementation
- Algorithm complexity analysis
- Python iterator protocol
- Hash function optimization
- Dynamic memory management

---

**Language**: Python | **Focus**: Data Structures & Algorithms
