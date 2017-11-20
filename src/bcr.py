# -*- generated by 1.0.9 -*-
import da
_config_object = {'channel': 'fifo'}
from nacl.hash import sha256
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
from ast import literal_eval
from config import *
import read_config
client_module = da.import_da('client')
olympus_module = da.import_da('olympus')
import sys
import getopt
from time import time

def parse_program_args(argv):
    inputfile = ''
    output_wrapperfile = ''
    try:
        (opts, args) = getopt.getopt(argv, 'hi:o:', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        output_wrapper('Error in parsing arguments')
        return None
    for (opt, arg) in opts:
        if (opt in ('-i', '--ifile')):
            inputfile = arg
        elif (opt in ('-o', '--ofile')):
            output_wrapperfile = arg
    return [inputfile, output_wrapperfile]

def are_dicts_valid(d1, d2):
    return all(((k in d2) for k in d1))

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])

    def run(self):

        def output_wrapper(log):
            self.output('[Main][TS: {}]'.format(str(time())), log)
        if (len(sys.argv) < 2):
            output_wrapper('Incorrect argument count. Must specify the input configuration file atleast')
            return
        [infile, outfile] = parse_program_args(sys.argv[1:])
        if (infile == None):
            output_wrapper('Must specify input configuration file!')
            sys.exit(2)
        config_dict = read_config.parse_config_file(infile)
        global_config = GlobalConfig(config_dict)
        client_config = ClientConfig(config_dict)
        replica_config = ReplicaConfig(config_dict)
        output_wrapper(('Running BCR simulation for test case: ' + global_config.test_case_name))
        olympus = self.new(olympus_module.Olympus, args=('Olympus', replica_config.num_replica, replica_config.num_failures, replica_config.failures, replica_config.head_timeout, replica_config.nonhead_timeout, replica_config.checkpt_interval))
        self._start(olympus)
        clients = dict()
        for i in range(client_config.num_client):
            request_id_counter = (i * 10000)
            modified_ops = list(map((lambda o: (o.type.name, o.args_list)), client_config.workloads[i]))
            output_wrapper('Workload for client {} : {}'.format(str(i), str(modified_ops)))
            client = self.new(client_module.Client, args=(i, olympus, (request_id_counter - 1), client_config.client_timeout, modified_ops, client_config.num_failures))
            clients[i] = client
        self._start(set(clients.values()))
