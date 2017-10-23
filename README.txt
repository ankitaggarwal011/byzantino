PLATFORM
========
DistAlgo version: 1.0.9
Python3 (CPython) version: 3.5.1
Operating System: Windows 7, MAC OS
Hosts: Laptop (without VMs), VM on Google Cloud Compute Engine

INSTRUCTIONS
============

python3 -m da <src file> -i <config file>

e.g.
python3 -m da src/bcr.da -i config/basic_multi_client.txt


WORKLOAD GENERATION
===================

Python's random module and random module's random function is used for pseudorandom workload generation. Initially, the given seed is set, and one of the four operations is randomly selected. Similarly, the keys and values of a particular set length are randomly generated using the above module and function.

BUGS AND LIMITATIONS
====================
1. Multi-node setup produces unhashable set error.

2. Stress testing works for 5 clients with around 50 requests. For any more requests, the program produces TCP transport error on my 4 GB Windows system. 

3. Olympus and Client communication is partially signed, and will be extended in Phase 3.

4. In case of a failure, the client keeps retransmitting the requests because there is no reconfiguration mechanism implemented yet for phase 2. This is an expected limitation, which will be taken care of in phase 3.

CONTRIBUTIONS
=============

Ankit Aggarwal (anaaggarwal, 111485578):
Replica Implementation
Olympus Implementation
Digital Signing and Verification
Logging
Testing

Saraj Munjal (smunjal, 111497962):
Client Implementation
Configuration file parsing
Pseduorandom and other workload generation
Logging
Testing

MAIN FILES
==========

Implementation of the Replica, Olympus, and Client: src/bcr.da
Setting up configuration for the program and workload generation: src/config.py
Parsing the configuration file: src/read_config.py

CODE SIZE
=========

(1a) Lines of code for:
    Algorithm: ~400
    Other: ~350
    Total: ~750

(1b) Counts are obtained using: https://github.com/AlDanial/cloc

(2) Lines of code for:
    Core Algorithm: ~320
    Interleaved testing: ~80

LANGUAGE FEATURE USAGE
====================== 

List Comprehensions: ~5
Dictionary Comprehensions: 0
Set Comprehensions: ~1-2
Aggregations: 0
Quantifications: 0
