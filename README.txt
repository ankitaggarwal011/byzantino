PLATFORM
========
DistAlgo version: 1.0.11
Python3 (CPython) version: 3.5.1
Operating System: Windows 7, MAC OS
Hosts: Laptop (without VMs), VM on Google Cloud Compute Engine

INSTRUCTIONS
============

python3 -m da <src file> -i <config file>

e.g.
python3 -m da src/bcr.da -i config/basic_multi_client.txt

For multi-node:



WORKLOAD GENERATION
===================

Python's random module and random module's random function is used for pseudorandom workload generation. Initially, the given seed is set, and one of the four operations is randomly selected. Similarly, the keys and values of a particular set length are randomly generated using the above module and function.
As a convention, all keys and values generated have a fixed length of 3 to keep the system simple.

BUGS AND LIMITATIONS
====================


COMPARISON WITH RAFT
====================



CONTRIBUTIONS
=============

Ankit Aggarwal (anaaggarwal, 111485578):
Reconfiguration
Checkpointing
Failure Triggers and Injection
Digital Signing and Verification
Multi-host support
Logging
Testing

Saraj Munjal (smunjal, 111497962):
Reconfiguration
Checkpointing
Failure Triggers and Injection
Digital Signing and Verification
Multi-host support
Logging
Testing

MAIN FILES
==========

Main entry: src/bcr.da
Implementation of the Replica: src/replica.da
Implementation of the Olympus: src/olympus.da
Implementation of the Client: src/client.da
Setting up configuration for the program and workload generation: src/config.py
Parsing the configuration file: src/read_config.py

Implementation for multi-node setup: 

CODE SIZE
=========

(1a) Lines of code for:
    Algorithm: ~800
    Other: ~700
    Total: ~1500

(1b) Counts are obtained using: https://github.com/AlDanial/cloc

(2) Lines of code for:
    Core Algorithm: ~600
    Interleaved testing: ~200

LANGUAGE FEATURE USAGE
====================== 

List Comprehensions: ~15
Dictionary Comprehensions: ~2-3
Set Comprehensions: ~8-9
Aggregations: 0
Quantifications: ~2-3
Classes: 5
Enums: 3
Lambda: ~10
Map: ~10
