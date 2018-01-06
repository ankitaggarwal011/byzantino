# byzantino: Byzantine Chain Replication

This project is the implementation of the Byzantine chain replication (BCR), as described in

Robbert van Renesse, Chi Ho, and Nicolas Schiper. [Byzantine Chain Replication](http://www.cs.cornell.edu/~ns672/publications/2012OPODIS.pdf). Proceedings of the 16th International Conference on Principles of Distributed Systems (OPODIS 2012), pages 345-359. Springer Verlag, December 2012.

The project was completed as a part of the graduate course [CSE 535 Asynchronous Systems](http://www3.cs.stonybrook.edu/~stoller/cse535/) by Prof. Scott Stoller at Stony Brook University in Fall '17. It was implemented using DistAlgo, a very high-level language for programming distributed algorithms.

Byzantine-tolerant State Machine Replication (BSMR) is the only known generic approach to making applications (servers, routing daemons, and so on) tolerate arbitrary faults beyond crash failures in an asynchronous environment. Byzantine Chain Replication is a new class of highly reconfigurable Chain Replication protocols that are easily reconfigurable, do not require accurate failure detection, and are able to tolerate Byzantine failures.

## Platform
[DistAlgo](https://github.com/DistAlgo/distalgo) version: 1.0.11  
Python3 (CPython) version: 3.5.1, 3.6 (for multi-host on Docker)  
Operating System: Windows 7, MAC OS  
Hosts: Laptop (without VMs), Docker Images  

## Dependencies
PyDistAlgo  
PyNacl  
Pickle [Pre-installed]  
JSON [Pre-installed]  

```
pip install --upgrade pydistalgo pynacl
```

## Instructions
```
python3 -m da <src file> -i <config file>
```

e.g.
```
python3 -m da src/bcr.da -i config/phase3/test_phase3.txt
```

For large workloads, we increased the recursion limit of Python.

For multi-node:  
Node 1: Other Replicas, Client, Olympus  
Node 2 : Head  

```
python3 -m da --logfile --logfilename=logs/simple-log.txt --logfilelevel=info --message-buffer-size=96000 -n Node1 -H <Node1's own IP> -R <Other node's IP> src/multihost/bcr.da -i config/phase3/simple.txt
python3 -m da --logfile --logfilename=logs/simple-log.txt --logfilelevel=info --message-buffer-size=96000 -n Node2 -D -H <Node2's own IP> -R <Other node's IP> src/multihost/bcr.da -i config/phase3/simple.txt
```

## Workload Generation
Python's random module and random module's random function is used for pseudorandom workload generation. Initially, the given seed is set, and one of the four operations is randomly selected. Similarly, the keys and values of a particular set length are randomly generated using the above module and function.  
As a convention, all keys and values generated have a fixed length of 3 to keep the system simple.

## Multi-Host Setup
We used two docker images (on Mac) with Python 3.6 and PyDistAlgo 1.0.11 to simulate multi-host setup.  
For large workloads, we increased the recursion limit of Python and RAM given to the docker images.  

## Code Structure
Main entry: src/bcr.da  
Implementation of the Replica: src/replica.da  
Implementation of the Olympus: src/olympus.da  
Implementation of the Client: src/client.da  
Setting up configuration for the program and workload generation: src/config.py  
Parsing the configuration file: src/read_config.py  

Implementation for multi-node setup: Head on Node2, everything else on Node1  
Main entry: src/multihost/bcr.da  
Implementation of the Replica: src/multihost/replica.da  
Implementation of the Olympus: src/multihost/olympus.da  
Implementation of the Client: src/multihost/client.da  
Setting up configuration for the program and workload generation: src/multihost/config.py  
Parsing the configuration file: src/multihost/read_config.py  

## License

[MIT License](https://github.com/ankitaggarwal011/byzantino/blob/master/LICENSE)

## Authors
Ankit Aggarwal  
Saraj Munjal  
