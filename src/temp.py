# imports for encryption and hashing
from nacl.hash import sha256
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

# import for deserialization of message objects
from ast import literal_eval

# import all config objects and functions
from config import *
import read_config

# misc imports
import sys
import getopt
from time import time

# Configure a reliable FIFO channel
config(channel={'reliable', 'fifo'})


# Implementation of the Replica process
# The replica process receives Olympus' public key, its timeout value in seconds, and its failure scenarios from Olympus
# in setup
# Failure handling: for each replica, we maintain two dictionaries
#                pending_failures[scenario.action_type] = 1
#                pending_failure_scenarios[scenario.action_type] = scenario
# Key is the scenario action type enum in config.py. This lets us keep track of what scenarios to execute later

class Replica(process):
    ## Replica setup method called from
    def setup(id, name, replica_failures, replica_timeout, olympus_public_key):
        output_wrapper('replica failures: ' + str(replica_failures))
        self.status = 0  # PENDING
        self.running_state = dict()  # supports put, get, slice, and append operations
        self.order_proof = list()
        self.result_proof = list()
        self.result_cache = dict()
        self.slot_number = 0
        self.last_slot_number = 0
        self.olympus = None
        self.replicas = None
        self.head = None
        self.tail = None
        self.replica_public_keys = None
        self.private_key = None
        self.client_keys = dict()
        self.configuration = None
        self.pending_failures = {}  # dict of failure_action_type vs boolean
        self.pending_failure_scenarios = {}
        self.messages_received_from_client = {}  # messages received for each client
        self.messages_shuttle = {}  # shuttles received for each client
        self.messages_result_shuttle = {}  # result shuttles received for each client
        self.messages_forwarded_request = {}  # forwarded requests received for each client

    # Replica starts off in the ACTIVE state. It verifies Olympus and then awaits other messages or Shutdown message.
    def run():
        status = 1  # ACTIVE
        olympus_public_key = VerifyKey(olympus_public_key, encoder=HexEncoder)
        await(received(('Shutdown'), from_=olympus))

    # Replica will shut down if it receives the Shutdown message from Olympus (its waiting in run() will expire)
    def receive(msg=('Shutdown'), from_=olympus):
        status = 2  # IMMUTABLE
        output_wrapper(name + ' is immutable and shutting down.')

    # Each replica receives its configuration data from Olympus. This happens after replica is created.
    # It gets references to other replicas in chain, head, tail, Olympus, and public keys for other replicas
    def receive(msg=('Configuration', olympus_, replicas_, head_, tail_, config_data)):
        olympus = olympus_
        replicas = replicas_
        head = head_
        tail = tail_
        config_data = verify_data_with_key(config_data, olympus_public_key)
        if config_data is None:
            output_wrapper('Verification of message sent by Olympus has failed.')
            return
        replica_public_keys_, configuration = config_data
        replica_public_keys = [VerifyKey(key, encoder=HexEncoder) for key in replica_public_keys_]
        output_wrapper('{} received replica references and public keys from Olympus'.format(name))
        send(('ACK', name), to=olympus)

    # Replica receives its private key from Olympus, that it uses to sign results and proofs
    def receive(msg=('Key', private_key_), from_=olympus):
        private_key = private_key_
        output_wrapper(name + ' has receives its private key from Olympus.')
        send(('ACK', name), to=olympus)

    # Replica receives client public key from Olympus, used to verify client requests
    def receive(msg=('Client_keys', client_id, client_public_key)):
        client_keys[client_id] = VerifyKey(client_public_key, encoder=HexEncoder)
        output_wrapper(
            '{} has received client public key: {} for client {}'.format(name, str(client_public_key), str(client_id)))
        send(('ACK', name), to=olympus)

    # This is a global message handler for requests for replicas. It handles all possible cases: requests directly
    # from the client, requests from replicas  before in the chain(shuttle)
    def receive(msg=(sender_id, 'Request', type, request_from, client, request_id, client_id, args)):
        output_wrapper(str(type) + ' request with request id ' + str(request_id) + ' received by ' + name + '.')
        if status == 0:
            output_wrapper(name + ' is in PENDING state.')
        elif status == 1:
            output_wrapper(name + ' is in ACTIVE state.')
        elif status == 2:
            output_wrapper(name + ' is in IMMUTABLE state.')

        if status != 1:  # if replica is not ACTIVE
            output_wrapper('Replica is not in ACTIVE state. Not handling message')
            return

        if request_from == client:
            # client_request failure trigger
            if client_id not in messages_received_from_client:
                messages_received_from_client[client_id] = 0
            is_trigger, scenario = check_failure(replica_failures, client_id, messages_received_from_client[client_id],
                                                 FailureType.client_request)
            if is_trigger:
                # mark this failure scenario
                pending_failures[scenario.action_type] = 1
                pending_failure_scenarios[scenario.action_type] = scenario
                output_wrapper(
                    'Replica {}: Trigger client request failure for client_id: {} and message count: {}, scenario: {}'.format(
                        name, client_id, messages_received_from_client[client_id], pending_failures));

            messages_received_from_client[client_id] += 1

            # Verification of digital signature of client
            args = verify_data_with_key(args, client_keys[client_id])
            if args == None:
                output_wrapper('Verification of message sent by Client ' + str(client_id) + ' has failed.')
                return

            if request_id in result_cache:
                sign_and_send(('Operation_result', result_cache[request_id]), client)
                output_wrapper('Result sent from cache of ' + name + '.')
                return
            elif self != head:
                sign_and_send(('Request', type, self, client, request_id, client_id, args), head)
                if await(received(('Result_shuttle_' + str(request_id)))):
                    pass
                elif timeout(replica_timeout):
                    send(('Reconfiguration', name, None), to=olympus)
                return
        else:
            # Verification of digital signature of replicas
            args = verify_data_with_key(args, replica_public_keys[sender_id])
            if args == None:
                output_wrapper('Verification of message sent by Replica ' + str(sender_id) + ' has failed.')
                return

        if self == head:
            if request_from != client:
                # forwarded_request failure trigger
                if client_id not in messages_forwarded_request:
                    messages_forwarded_request[client_id] = 0
                is_trigger, scenario = check_failure(replica_failures, client_id, messages_forwarded_request[client_id],
                                                     FailureType.forwarded_request)
                if is_trigger:
                    # mark this failure scenario
                    pending_failures[scenario.action_type] = 1
                    pending_failure_scenarios[scenario.action_type] = scenario
                    output_wrapper(
                        'Replica {}: Trigger forwarded request failure for client_id: {} and message count: {}, '
                        'scenario: {}'.format(name, client_id, messages_forwarded_request[client_id], scenario))
                messages_forwarded_request[client_id] += 1
            # update running state
            result = update_running_state(type, args)
            slot_number += 1
            # if there is a change_operation failure scenario to execute, do it. Else, proceed as normal.
            if FailureActionType.change_operation in pending_failures and pending_failures[
                FailureActionType.change_operation] == 1:
                stmt_type = 'get'
                stmt_args = ['x']
                output_wrapper('Executing failure scenario: {}'.format(
                    str(pending_failure_scenarios[FailureActionType.change_operation])))
                pending_failures[FailureActionType.change_operation] = 0
                pending_failure_scenarios[FailureActionType.change_operation] = None
            else:
                stmt_type = type
                stmt_args = args

            # generate order statement and order proof
            order_stmt = [[slot_number, (stmt_type, stmt_args), configuration]]  # (type, args) is operation (o)
            order_proof = [slot_number, (type, args), configuration, order_stmt]
            result_proof = [[(type, args), calculate_hash(result)]]  # add result stmt
            shuttle = (order_proof, result_proof)

            # sign and send the shuttle (request shuttle) to the next replica in chain
            sign_and_send(('Request', type, self, client, request_id, client_id, shuttle), replicas[id + 1])
            last_slot_number = slot_number
            if await(received(('Result_shuttle_' + str(request_id)))):
                pass
            elif timeout(replica_timeout):
                output_wrapper(
                    '{} has timed out while waiting for result shuttle for request id {}. Sending reconfiguration '
                    'request to Olympus'.format(
                        name, str(request_id)))
                send(('Reconfiguration', name, None), to=olympus)
        else:
            # case of shuttle from some previous replica
            # shuttle failure trigger
            if client_id not in messages_shuttle:
                messages_shuttle[client_id] = 0
            is_trigger, scenario = check_failure(replica_failures, client_id, messages_shuttle[client_id],
                                                 FailureType.shuttle)
            if is_trigger:
                # mark this failure scenario
                pending_failures[scenario.action_type] = 1
                pending_failure_scenarios[scenario.action_type] = scenario
                output_wrapper(
                    'Replica {}: Trigger shuttle failure for client_id: {} and message count: {}, scenario: {}'.format(
                        name, client_id, messages_shuttle[client_id], scenario));
            messages_shuttle[client_id] += 1

            # if the shuttle is invalid, trigger reconfiguration and return
            if not validate_shuttle(args):
                output_wrapper(
                    '{} failed to validate shuttle for request_id: {}. Triggering reconfiguration'.format(name,
                                                                                                          request_id))
                send(('Reconfiguration', name, None), to=olympus)
                return

            # unpack arguments
            order_proof, result_proof = args
            slot_number, operation, configuration, order_stmt = order_proof
            last_slot_number = slot_number
            type, operation_args = operation
            # update running state
            result = update_running_state(type, operation_args)
            # if there is a pending change_operation failure scenario to perform, do it.
            if FailureActionType.change_operation in pending_failures and pending_failures[
                FailureActionType.change_operation] == 1:
                output_wrapper('Executing failure scenario: {}'.format(
                    str(pending_failure_scenarios[FailureActionType.change_operation])))
                type = 'get'
                operation_args = ['x']
                pending_failures[FailureActionType.change_operation] = 0
                pending_failure_scenarios[FailureActionType.change_operation] = None
            order_proof[3].append([slot_number, (type, operation_args), configuration])  # append to order_stmt
            result_proof.append([(type, operation_args), calculate_hash(result)])  # append result stmt
            shuttle = (order_proof, result_proof)
            # if tail, send result to client. Else, forward result to next replica in chain.
            if self == tail:
                result_shuttle = [result, result_proof]
                if FailureActionType.change_result in pending_failures and pending_failures[
                    FailureActionType.change_result] == 1:
                    op_t = result_shuttle[1][id][0]
                    result_shuttle[1][id] = [op_t, calculate_hash('OK')]

                if FailureActionType.drop_result_stmt in pending_failures and pending_failures[
                    FailureActionType.drop_result_stmt] == 1:
                    result_t = result_shuttle[0]
                    result_shuttle = [result_t, result_shuttle[1][1:]]

                sign_and_send(('Operation_result', request_id, result_shuttle), client)

                # we send a separate 'Operation_result_' message to client for tracking the completion of a
                # particular request with this request_id. It is not possible for the client to wait for specific
                # requests in any other way.
                send(('Operation_result_' + str(request_id)), to=client)

                # The tail sends a result_shuttle message to itself to initiate the result shuttle handler train
                sign_and_send(('Result_shuttle', self, request_id, client_id, result_shuttle), tail)
            else:
                sign_and_send(('Request', type, self, client, request_id, client_id, shuttle), replicas[id + 1])
                if await(received(('Result_shuttle_' + str(request_id)))):
                    pass
                elif timeout(replica_timeout):
                    send(('Reconfiguration', name, None), to=olympus)

    # message handler for Result shuttle message received from the next replica in chain

    def receive(msg=(sender_id, 'Result_shuttle', request_from, request_id, client_id, result_shuttle)):
        # mark result_shuttle failure trigger
        if client_id not in messages_result_shuttle:
            messages_result_shuttle[client_id] = 0
        is_trigger, scenario = check_failure(replica_failures, client_id, messages_result_shuttle[client_id],
                                             FailureType.result_shuttle)
        if is_trigger:
            # mark this failure scenario
            pending_failures[scenario.action_type] = 1
            pending_failure_scenarios[scenario.action_type] = scenario
            output_wrapper(
                '{}: Trigger result shuttle failure for client_id: {} and message count: {}, scenario: {}'.format(name,
                                                                                                                  client_id,
                                                                                                                  messages_result_shuttle[
                                                                                                                      client_id],
                                                                                                                  scenario))
        messages_result_shuttle[client_id] += 1

        # Verification of signature of replicas sending result shuttles
        result_shuttle = verify_data_with_key(result_shuttle, replica_public_keys[sender_id])
        if result_shuttle == None:
            output_wrapper('Verification of message sent by Replica ' + str(sender_id) + ' has failed.')
            return

        if validate_result_shuttle(result_shuttle):
            result_cache[request_id] = result_shuttle
            if self != head:
                if FailureActionType.change_result in pending_failures and pending_failures[FailureActionType.change_result] == 1:
                    output_wrapper('Executing failure scenario: {}'.format(
                        str(pending_failure_scenarios[FailureActionType.change_result])))
                    op_t = result_shuttle[1][id][0]
                    result_shuttle[1][id] = [op_t, calculate_hash('OK')]
                    pending_failures[FailureActionType.change_result] = 0
                    pending_failure_scenarios[FailureActionType.change_result] = None
                if FailureActionType.drop_result_stmt in pending_failures and pending_failures[
                    FailureActionType.drop_result_stmt] == 1:
                    output_wrapper('Executing failure scenario: {}'.format(
                        str(pending_failure_scenarios[FailureActionType.drop_result_stmt])))
                    result_t = result_shuttle[0]
                    result_shuttle = [result_t, result_shuttle[1][1:]]
                    pending_failures[FailureActionType.drop_result_stmt] = 0
                    pending_failure_scenarios[FailureActionType.drop_result_stmt] = None
                sign_and_send(('Result_shuttle', self, request_id, client_id, result_shuttle), replicas[id - 1])
                send(('Result_shuttle_' + str(request_id)), to=replicas[id - 1])
            output_wrapper('Result shuttle is at ' + str(name) + '.')
        else:
            output_wrapper('Result shuttle sent by Replica ' + str(sender_id) + ' is not valid.')
            send(('Reconfiguration', name, None), to=olympus)

    # method to update running state in replica. It performs one out of 4 supported operations.
    def update_running_state(type, args):
        if type == 'put':
            if len(args) > 1:
                running_state[args[0]] = args[1]
            return 'OK'
        elif type == 'get':
            if len(args) > 0:
                if args[0] in running_state:
                    return running_state[args[0]]
                else:
                    return ''
        elif type == 'slice':
            if len(args) > 1:
                lower, upper = map(int, args[1].split(':'))
                if args[0] in running_state and lower >= 0 and upper <= len(running_state[args[0]]):
                    running_state[args[0]] = running_state[args[0]][lower:upper]
                    return running_state[args[0]]
                else:
                    return 'fail'
        elif type == 'append':
            if len(args) > 1:
                if args[0] in running_state:
                    running_state[args[0]] = running_state[args[0]] + args[1]
                    return 'OK'
                else:
                    return 'fail'

    # calculate the sha256 hash of value
    def calculate_hash(val):
        if isinstance(val, str):
            return sha256(str.encode(val), encoder=HexEncoder)
        return sha256(val, encoder=HexEncoder)

    # validate the shuttle coming from previous replica
    def validate_shuttle(shuttle):
        order_proof, result_proof = shuttle
        slot_number, operation, configuration, order_stmt = order_proof
        if last_slot_number != slot_number - 1:
            return False
        for stmt in order_stmt:
            if stmt[0] != slot_number or stmt[1] != operation or stmt[2] != configuration:
                return False
        return True

    # validate the result shuttle coming back from next replica
    def validate_result_shuttle(result_shuttle):
        result, result_proof = result_shuttle
        if len(result_proof) != len(replicas):
            return False
        hash = calculate_hash(result)
        for i in result_proof:
            if hash != i[1]:
                return False
        return True

    # encrypt data with own private key and send
    def sign_and_send(data, to_):
        data = [id] + list(data)
        data[-1] = private_key.sign(str(data[-1]).encode('utf-8'))
        send(tuple(data), to=to_)

    # verify data with own public key and parse it
    def verify_data_with_key(data, pub_key):
        try:
            pub_key.verify(data)
            return literal_eval(data.message.decode('utf-8'))
        except BadSignatureError:
            return None

    # method that checks if a failure scenario is applicable with current parameters
    # if it is, the caller will update the current failure scenario dicts accordingly

    def check_failure(replica_failures, source_id, source_message_count, required_type):
        for i, failure in enumerate(replica_failures):
            oper = failure.operands
            if failure.failure_type == required_type and source_id == oper[0] and source_message_count == oper[1]:
                return (True, failure)

        return (False, None)

    # Utility method for logging, prepends process name and time to each log statement
    def output_wrapper(log):
        output('[{}][TS: {}]'.format(name, str(time())), log)


# The Olympus process. It creates replicas, and co-ordinates the passing of public keys to and from clients and replicas
# It also handles system reconfiguration, which is not implemented yet
class Olympus(process):
    # Olympus setup method. It receives config information, and passes it to applicable replicas
    def setup(name, num_replicas, all_replica_conf_failures, head_timeout, replica_timeout):
        self.replicas = list()
        self.replica_private_keys = list()
        self.replica_public_keys = list()
        self.head = None
        self.tail = None
        # generate own keys
        self.private_key = SigningKey.generate()
        self.public_key = self.private_key.verify_key.encode(encoder=HexEncoder)
        self.configuration_number = 0  # default configuration for phase 2
        self.client_keys = {}  # client keys will be obtained later in message passing
        # get all replica failures in current configuration
        all_replica_failures = all_replica_conf_failures.get(self.configuration_number, {})
        for i in range(num_replicas):
            # get all failure scenarios in current replica
            replica_failures = all_replica_failures.get(i, {})
            if i == 0:
                # create head replica
                replica = new(Replica, args=(i, 'Head', replica_failures, head_timeout, public_key))
                self.head = replica
            elif i == num_replicas - 1:
                # create tail replica
                replica = new(Replica, args=(i, 'Tail', replica_failures, replica_timeout, public_key))
                self.tail = replica
            else:
                # create other replica
                replica = new(Replica, args=(i, 'Replica ' + str(i), replica_failures, replica_timeout, public_key))
            self.replicas.append(replica)
            replica_name = 'Replica ' + str(i)
            output_wrapper('Olympus created replica process: {}'.format(replica_name))
            signing_key = SigningKey.generate()
            verify_key = signing_key.verify_key.encode(encoder=HexEncoder)
            output_wrapper(
                'Olympus created keys for replica process: {}. Public key: {}'.format(replica_name, str(verify_key)))
            self.replica_private_keys.append(signing_key)
            self.replica_public_keys.append(verify_key)

    # ACK message from client/replica
    def receive(msg=('ACK', sender)):
        output_wrapper('ACK from ' + str(sender) + '.')

    # Get configuration message handler from client in which client passes its own reference and key
    # Pass required information to all replicas and reply to client with current configuration details (replicas, head)
    def receive(msg=('Get_configuration', client, client_name, client_id, client_public_key)):
        client_keys[client_id] = VerifyKey(client_public_key, encoder=HexEncoder)
        send(('Configuration', replicas, head), to=client)
        send(('Keys', replica_public_keys, public_key), to=client)
        send(('Client_keys', client_id, client_public_key), to=replicas)
        output_wrapper('Received public key: {} from client: {}'.format(str(client_public_key), str(client_name)))
        output_wrapper('Configuration sent to ' + str(client_name) + '.')

    # Reconfiguration request. This may come from a client or a replica. Client sends proof of misbehavior, replica doesn't.
    # This is not implemented in Phase 2. Will be done in Phase 3.
    def receive(msg=('Reconfiguration', sender, proof_of_misbehavior)):
        output_wrapper('Reconfiguration request received from ' + str(sender) + '.')
        output_wrapper('No reconfiguration mechanism implemented yet.')
        # Reconfigure and send new configuration to client and replicas

    # Encrypt data with own private key and send
    def sign_and_send(data, to_):
        data = list(data)
        data[-1] = private_key.sign(str(data[-1]).encode('utf-8'))
        send(tuple(data), to=to_)

    # Verify and unpack data with someone else's public key
    def verify_data_with_key(data, pub_key):
        try:
            pub_key.verify(data)
            return literal_eval(data.message.decode('utf-8'))
        except BadSignatureError:
            return None

    # Run loop. Won't exit till Shutdown is received (never).
    # Start replicas and send them initial configuration message
    def run():
        start(replicas)
        sign_and_send(('Configuration', self, replicas, head, tail, [replica_public_keys, configuration_number]),
                      replicas)
        for i in range(len(replicas)):
            send(('Key', replica_private_keys[i]), to=replicas[i])
        await(received(('ACK', None)))
        await(received(('Shutdown')))

    # Utility method for logging, prepends process name and time to each log statement
    def output_wrapper(log):
        output('[{}][TS: {}]'.format(name, str(time())), log)


class Client(process):
    def setup(client_id, olympus, request_id, client_timeout, operations, num_failures):
        self.name = 'Client ' + str(client_id)
        self.replicas = None
        self.head = None
        self.replica_public_keys = None
        self.olympus_public_key = None
        self.private_key = SigningKey.generate()
        self.public_key = self.private_key.verify_key.encode(encoder=HexEncoder)
        self.client_running_state = dict()
        self.client_running_state_sync = dict()

    def receive(msg=('Configuration', replicas_, head_), from_=olympus):
        replicas = replicas_
        head = head_
        output_wrapper(name + ' is configured.')
        send(('ACK', name), to=olympus)

    def receive(msg=('Keys', replica_public_keys_, olympus_public_key_), from_=olympus):
        replica_public_keys = [VerifyKey(key, encoder=HexEncoder) for key in replica_public_keys_]
        olympus_public_key = VerifyKey(olympus_public_key_, encoder=HexEncoder)
        output_wrapper('Received the public keys of replicas from Olympus')
        output_wrapper('Received the public key of Olympus.')
        send(('ACK', name), to=olympus)

    def receive(msg=(sender_id, 'Operation_result', request_id, result_shuttle)):
        # Verification of signature of replicas
        result_shuttle = verify_data_with_key(result_shuttle, replica_public_keys[sender_id])
        if result_shuttle == None:
            output_wrapper('Verification of message sent by Replica ' + str(sender_id) + ' has failed.')
            return

        result, result_proof = result_shuttle
        is_result__valid, is_reconfiguration_required = validate_result(result, result_proof)
        if is_result__valid:
            if result != 'fail' or result != '':
                update_client_running_state(client_running_state_sync, result_proof[0][0][0], result_proof[0][0][1])
                # updating state from the tail response
            output_wrapper('Valid result: {} received for request id: {}'.format(str(result), str(request_id)))
        if is_reconfiguration_required:
            # send reconfiguration request to Olympus with proof of misbehavior
            output_wrapper('Misbehaviour detected in request id: {}! Sending reconfiguration request to Olympus'.format(
                request_id))
            send(('Reconfiguration', name, result_shuttle), to=olympus)

    def sign_and_send(data, to_):
        data = list(data)
        data[-1] = private_key.sign(str(data[-1]).encode('utf-8'))
        send(tuple(data), to=to_)

    def verify_data_with_key(data, pub_key):
        try:
            pub_key.verify(data)
            return literal_eval(data.message.decode('utf-8'))
        except BadSignatureError:
            return None

    def run():
        if replicas is None:
            send(('Get_configuration', self, name, client_id, public_key), to=olympus)
            await(received(('Configuration', replicas, head)))
        for op in operations:
            update_client_running_state(client_running_state, op[0], op[1])
            retry = 0
            while True:
                send_request(op[0], op[1], retry)
                if await(received(('Operation_result_' + str(request_id)))):
                    break
                elif timeout(client_timeout):
                    output_wrapper('Timeout: Retrying request id: {}, sending to all replicas'.format(str(request_id)))
                    retry = 1
        output_wrapper(
            'Local running state of client after the given set of operations: ' + str(client_running_state) + '.')
        output_wrapper(
            'Running state of client at the server (assuming no conflicting keys from other clients) after the given set of operations: ' + str(
                client_running_state_sync) + '.')
        if are_dicts_equal(client_running_state, client_running_state_sync):
            output_wrapper('\n\nTest case passed! Actual and expected running states match.\n\n')
        else:
            output_wrapper('\n\nTest case failed! Actual and expected running states don\'t match\n\n')
        await(received('Shutdown'))

    def update_client_running_state(running_state, type, args):
        if type == 'put':
            if len(args) > 1:
                running_state[args[0]] = args[1]
            return 'OK'
        elif type == 'get':
            if len(args) > 0:
                if args[0] in running_state:
                    return running_state[args[0]]
                else:
                    return ''
        elif type == 'slice':
            if len(args) > 1:
                lower, upper = map(int, args[1].split(':'))
                if args[0] in running_state and lower >= 0 and upper <= len(running_state[args[0]]):
                    running_state[args[0]] = running_state[args[0]][lower:upper]
                    return running_state[args[0]]
                else:
                    return 'fail'
        elif type == 'append':
            if len(args) > 1:
                if args[0] in running_state:
                    running_state[args[0]] = running_state[args[0]] + args[1]
                    return 'OK'
                else:
                    return 'fail'

    def send_request(type, args, retry):
        args = private_key.sign(str(args).encode('utf-8'))  # sign the request
        if retry:
            send((None, 'Request', type, self, self, request_id, client_id, args), to=replicas)
        else:
            request_id += 1
            send((None, 'Request', type, self, self, request_id, client_id, args), to=head)

    # returns a tuple of booleans (is_valid_result_shuttle, send_reconfiguration_request)
    def validate_result(result, result_proof):
        if len(result_proof) < num_failures + 1:
            output_wrapper('Number of result proofs received are less than the majority (failures + 1).')
            return (False, True)

        # ASSUMPTION: client checks all result proofs for validating correctness of response.
        # Another approach may be to check that a majority of result proofs are the same as hash(tail_response)
        majority = 0
        hash = calculate_hash(result)
        for i in result_proof:
            if hash == i[1]:
                majority += 1
        output_wrapper(
            'Number of correct result proofs received :{}, required majority: {}'.format(majority, num_failures + 1))
        if majority < num_failures + 1:
            return (False, True)
        elif majority < 2 * num_failures + 1:
            return (True, True)
        return (True, False)

    def calculate_hash(val):
        if isinstance(val, str):
            return sha256(str.encode(val), encoder=HexEncoder)
        return sha256(val, encoder=HexEncoder)

    def output_wrapper(log):
        output('[{}][TS: {}]'.format(name, str(time())), log)


# Utility method for parsing program arguments
def parse_program_args(argv):
    inputfile = ''
    output_wrapperfile = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        output_wrapper('Error in parsing arguments')
        return None
    for opt, arg in opts:
        if opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            output_wrapperfile = arg
    return [inputfile, output_wrapperfile]


# Utility method to find if two dictionaries are equal
def are_dicts_equal(d1, d2):
    return (len(d1) == len(d2) and all(k in d2 for k in d1))


# Main entry point
def main():
    def output_wrapper(log):
        output('[Main][TS: {}]'.format(str(time())), log)

    # ignore the 1st argument because it will be the program binary path
    if len(sys.argv) < 2:
        output_wrapper('Incorrect argument count. Must specify the input configuration file atleast')
        return

    [infile, outfile] = parse_program_args(sys.argv[1:])
    if infile == None:
        output_wrapper('Must specify input configuration file!')
        sys.exit(2)

    config_dict = read_config.parse_config_file(infile)
    global_config = GlobalConfig(config_dict)
    client_config = ClientConfig(config_dict)
    replica_config = ReplicaConfig(config_dict)

    output_wrapper('Running BCR simulation for test case: ' + global_config.test_case_name)
    olympus = new(Olympus, args=(
        'Olympus', replica_config.num_replica, replica_config.failures, replica_config.head_timeout,
        replica_config.nonhead_timeout))
    start(olympus)
    clients = list()

    for i in range(client_config.num_client):
        request_id_counter = i * 10000  # assuming each client will not perform more than 10000 operations in a single run
        modified_ops = list(map(lambda o: (o.type.name, o.args_list), client_config.workloads[i]))
        output_wrapper('Workload for client {} : {}'.format(str(i), str(modified_ops)))
        client = new(Client, args=(
            i, olympus, request_id_counter - 1, client_config.client_timeout, modified_ops, client_config.num_failures))
        clients.append(client)

    start(clients)
