from enum import Enum
import random
import string


class GlobalConfig:
    def __init__(self, dict):
        self.test_case_name = dict['test_case_name']
        self.num_client = int(dict['num_client'])
        self.num_failures = int(dict['t'])
        self.num_replica = 2 * self.num_failures + 1


class ClientConfig:
    def __init__(self, dict):
        self.test_case_name = dict['test_case_name']
        self.num_client = int(dict['num_client'])
        self.num_failures = int(dict['t'])
        self.client_timeout = int(dict['client_timeout'])
        self.hosts = dict['hosts'].split(';')
        for i, host in enumerate(self.hosts):
            self.hosts[i] = host.strip()
        client_hosts = dict['client_hosts'].split(';')
        if len(client_hosts) != self.num_client:
            raise ValueError("Client host mapping must be of size num_client: " + self.num_client.__str__())
        self.client_host_mapping = {}
        for i, host_str in enumerate(client_hosts):
            host_str = host_str.strip()
            if not str.isdecimal(host_str):
                raise ValueError("client host must be an integer")
            self.client_host_mapping[i] = int(host_str)

        self.workloads = {}
        for i in range(0, self.num_client):
            key = 'workload' + '[' + str(i) + ']'
            workload = get_operation_list(dict[key])
            self.workloads[i] = workload

    def __str__(self):
        return "Test case name: {}, # of clients: {}, # of failures = {}, Client timeout in ms: {}, hosts: {}, " \
               "client-host mapping: {}, Workloads: {}".format(self.test_case_name, self.num_client, self.num_failures,
                                                               self.client_timeout, self.hosts,
                                                               self.client_host_mapping, self.workloads)

    __repr__ = __str__


class ClientOperationType(Enum):
    get = 1
    put = 2
    append = 3
    slice = 4

    @classmethod
    def value_of(cls, name):
        for code, member in cls.__members__.items():
            if code == name:
                return member

        return None


class ClientOperation:
    def __init__(self, opcode, args_list):
        self.type = ClientOperationType.value_of(opcode)
        self.args_list = args_list

    def __str__(self):
        return "op: {}, args: {}".format(self.type, self.args_list)

    __repr__ = __str__


def get_random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_pseudo_random_load(seed_str, count_str):
    seed = int(seed_str)
    count = int(count_str)
    word_len = 3
    operations = []

    random.seed(seed)
    for i in range(1, count):
        opcode = random.choice(range(1, 4))
        if opcode == ClientOperationType.get.value:
            operations.append(ClientOperation('get', [get_random_word(word_len), ]))
        elif opcode == ClientOperationType.put.value:
            operations.append(ClientOperation('put', [get_random_word(word_len), get_random_word(word_len)]))
        elif opcode == ClientOperationType.append.value:
            operations.append(ClientOperation('append', [get_random_word(word_len), get_random_word(word_len)]))
        elif opcode == ClientOperationType.slice.value:
            operations.append(ClientOperation('slice', [get_random_word(word_len), '1..3']))
    return operations


def get_operation_list(command):
    command = command.strip()
    if command.__contains__("pseudorandom"):
        lidx = command.find('(')
        ridx = command.find(')')
        [seed, count] = command[lidx + 1:ridx].split(',')
        return generate_pseudo_random_load(seed, count)
    else:
        parts = command.split(';')
        operations = []
        for i, part in enumerate(parts):
            part = part.strip()
            lidx = part.find('(')
            operation = part[0:lidx]
            ridx = part.find(')')
            params = part[lidx + 1:ridx].split(',')
            for i, param in enumerate(params):
                # remove quotes
                params[i] = params[i].replace('\'', '')
                params[i] = params[i].replace('\"', '')
            operations.append(ClientOperation(operation, params))
        return operations


class ReplicaConfig:
    def __init__(self, dict):
        self.test_case_name = dict['test_case_name']
        self.num_failures = int(dict['t'])
        self.num_replica = 2 * self.num_failures + 1
        self.head_timeout = int(dict['head_timeout'])
        self.nonhead_timeout = int(dict['nonhead_timeout'])
        self.hosts = dict['hosts'].split(';')
        for i, host in enumerate(self.hosts):
            self.hosts[i] = host.strip()
        replica_hosts = dict['replica_hosts'].split(';')
        if len(replica_hosts) != self.num_replica:
            raise ValueError("Replica host mapping must be of size num_client: " + self.num_replica.__str__())
        self.replica_host_mapping = {}
        for i, host_str in enumerate(replica_hosts):
            host_str = host_str.strip()
            if not str.isdecimal(host_str):
                raise ValueError("replica host must be an integer")
            self.replica_host_mapping[i] = int(host_str)
        # get failure scenarios from config
        self.failures = {}
        for key, value in list(dict.items()):
            key = key.strip()
            if not key.startswith("failure"):
                continue
            lidx = key.find('[')
            ridx = key.find(']')
            [config_no_str, replica_num_str] = key[lidx + 1:ridx].split(',')
            config_no = int(config_no_str)
            replica_no = int(replica_num_str)
            failures = parse_failures(value)
            config_no_failures = self.failures.get(config_no, {})
            config_no_failures[replica_no] = failures
            self.failures[config_no] = config_no_failures

    def __str__(self):
        return "Test case name: {}, # of replicas: {}, # of failures = {}, Head timeout in ms: {}, nonhead timeout in " \
               "ms:{}, hosts: {}, " \
               "replica-host mapping: {}, Failures: {}".format(self.test_case_name, self.num_replica, self.num_failures,
                                                               self.head_timeout, self.nonhead_timeout, self.hosts,
                                                               self.replica_host_mapping, self.failures)

    __repr__ = __str__


def parse_failures(command):
    command = command.strip()
    scenarios = command.split(';')
    for i, scenario in enumerate(scenarios):
        scenarios[i] = scenarios[i].strip()
    return list(map(lambda s: FailureScenario(s), scenarios))


class FailureScenario:
    def __init__(self, failure_str):
        failure_str = failure_str.strip()
        [trigger_str, action_str] = failure_str.split('),')
        trigger_str = trigger_str.strip()
        lidx = trigger_str.find('(')
        self.failure_type = FailureType.value_of(trigger_str[:lidx])
        self.operands = list(map(lambda s: int(s.strip()), trigger_str[lidx + 1:].split(',')))
        action_str = action_str.strip()
        idx = action_str.find('(')
        self.action_type = FailureActionType.value_of(action_str[:idx])

    def __str__(self):
        return '{}({}), {}()'.format(self.failure_type.name, ','.join(list(map(lambda i: str(i), self.operands))),
                                     self.action_type.name)

    __repr__ = __str__


class FailureType(Enum):
    client_request = 1
    forwarded_request = 2
    shuttle = 3
    result_shuttle = 4

    @classmethod
    def value_of(cls, name):
        for member_name, member in cls.__members__.items():
            if name == member_name:
                return member

        return None

    @classmethod
    def value_of_code(cls, code):
        for name, member in cls.__members__.items():
            if code == member.value:
                return member

        return None


class FailureActionType(Enum):
    change_operation = 1
    change_result = 2
    drop_result_stmt = 3

    @classmethod
    def value_of(cls, name):
        for member_name, member in cls.__members__.items():
            if name == member_name:
                return member

        return None

    @classmethod
    def value_of_code(cls, code):
        for name, member in cls.__members__.items():
            if code == member.value:
                return member

        return None
