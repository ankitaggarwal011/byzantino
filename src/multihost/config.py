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
        self.client_timeout = int(dict['client_timeout']) / 1000

        self.workloads = {}
        for i in range(0, self.num_client):
            key = 'workload' + '[' + str(i) + ']'
            workload = get_operation_list(dict[key])
            self.workloads[i] = workload

    def __str__(self):
        return "Test case name: {}, # of clients: {}, # of failures = {}, Client timeout in ms: {}, " \
               "Workloads: {}".format(self.test_case_name, self.num_client, self.num_failures,
                                                               self.client_timeout, self.workloads)

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
        return "Operation: {}, Arguments: {}".format(self.type, self.args_list)

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
    for i in range(count):
        opcode = random.choice(range(1, 5))
        if opcode == ClientOperationType.get.value:
            operations.append(ClientOperation('get', [get_random_word(word_len), ]))
        elif opcode == ClientOperationType.put.value:
            operations.append(ClientOperation('put', [get_random_word(word_len), get_random_word(word_len)]))
        elif opcode == ClientOperationType.append.value:
            operations.append(ClientOperation('append', [get_random_word(word_len), get_random_word(word_len)]))
        elif opcode == ClientOperationType.slice.value:
            range1 = random.choice(range(word_len))
            range2 = random.choice(range(word_len))
            lower = min(range1, range2)
            upper = max(range1, range2)
            operations.append(ClientOperation('slice', [get_random_word(word_len), '{}:{}'.format(str(lower), str(upper))]))
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
        self.head_timeout = int(dict['head_timeout']) / 1000
        self.nonhead_timeout = int(dict['nonhead_timeout']) / 1000
        self.checkpt_interval = (int(dict['checkpt_interval']) if 'checkpt_interval' in dict else 1000)
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
               "ms:{}, checkpt_interval: {}, " \
               "Failures: {}".format(self.test_case_name, self.num_replica, self.num_failures,
                                                               self.head_timeout, self.nonhead_timeout, self.checkpt_interval,
                                                               self.failures)

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
        triggs = trigger_str[lidx + 1:].split(',')
        self.operands = []
        for trig in triggs:
            if len(trig.strip()) > 0:
                self.operands.append(int(trig.strip()))
        action_str = action_str.strip()
        idx = action_str.find('(')
        self.action_type = FailureActionType.value_of(action_str[:idx])
        actions = action_str[idx + 1:-1].split(',')
        self.action_operands = []
        for act in actions:
            if len(act.strip()) > 0:
                self.action_operands.append(int(act.strip()))

    def __str__(self):
        return '{}({}), {}({})'.format(self.failure_type.name, ','.join(list(map(lambda i: str(i), self.operands))),
                                     self.action_type.name, ','.join(list(map(lambda i: str(i), self.action_operands))))

    __repr__ = __str__


class FailureType(Enum):
    client_request = 1
    forwarded_request = 2
    shuttle = 3
    result_shuttle = 4
    wedge_request = 5
    new_configuration = 6
    checkpoint = 7
    completed_checkpoint = 8
    get_running_state = 9
    catch_up = 10

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
    crash = 4
    truncate_history = 5
    sleep = 6
    drop = 7
    increment_slot = 8
    extra_op = 9
    invalid_order_sig = 10
    invalid_result_sig = 11
    drop_checkpt_stmts = 12

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
