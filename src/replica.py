# -*- generated by 1.0.9 -*-
import da
PatternExpr_402 = da.pat.ConstantPattern('Shutdown')
PatternExpr_406 = da.pat.BoundPattern('_BoundPattern407_')
PatternExpr_420 = da.pat.ConstantPattern('Shutdown')
PatternExpr_424 = da.pat.FreePattern('olympus')
PatternExpr_441 = da.pat.TuplePattern([da.pat.ConstantPattern('Configuration'), da.pat.FreePattern('olympus_'), da.pat.FreePattern('replicas_'), da.pat.FreePattern('head_'), da.pat.FreePattern('tail_'), da.pat.FreePattern('config_data')])
PatternExpr_522 = da.pat.TuplePattern([da.pat.ConstantPattern('Key'), da.pat.FreePattern('private_key_')])
PatternExpr_529 = da.pat.FreePattern('olympus')
PatternExpr_549 = da.pat.TuplePattern([da.pat.ConstantPattern('Client_keys'), da.pat.FreePattern('client_id'), da.pat.FreePattern('client_public_key')])
PatternExpr_587 = da.pat.TuplePattern([da.pat.FreePattern('sender_id'), da.pat.ConstantPattern('Request'), da.pat.FreePattern('type'), da.pat.FreePattern('request_from'), da.pat.FreePattern('client'), da.pat.FreePattern('request_id'), da.pat.FreePattern('client_id'), da.pat.FreePattern('client_args'), da.pat.FreePattern('args')])
PatternExpr_919 = da.pat.BoundPattern('_BoundPattern925_')
PatternExpr_1372 = da.pat.BoundPattern('_BoundPattern1378_')
PatternExpr_1886 = da.pat.BoundPattern('_BoundPattern1892_')
PatternExpr_1939 = da.pat.TuplePattern([da.pat.FreePattern('sender_id'), da.pat.ConstantPattern('Checkpoint_proof'), da.pat.FreePattern('args')])
PatternExpr_2128 = da.pat.TuplePattern([da.pat.FreePattern('sender_id'), da.pat.ConstantPattern('Result_shuttle'), da.pat.FreePattern('request_from'), da.pat.FreePattern('request_id'), da.pat.FreePattern('client_id'), da.pat.FreePattern('result_shuttle')])
PatternExpr_2454 = da.pat.ConstantPattern('wedge_request')
PatternExpr_2458 = da.pat.FreePattern('olympus')
PatternExpr_2487 = da.pat.TuplePattern([da.pat.ConstantPattern('catch_up'), da.pat.FreePattern('gap')])
PatternExpr_2494 = da.pat.FreePattern('olympus')
PatternExpr_2568 = da.pat.ConstantPattern('get_running_state')
PatternExpr_2572 = da.pat.FreePattern('olympus')
PatternExpr_2594 = da.pat.TuplePattern([da.pat.ConstantPattern('get_running_state'), da.pat.FreePattern('client'), da.pat.FreePattern('requests_')])
PatternExpr_408 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern414_')]), da.pat.ConstantPattern('Shutdown')])
PatternExpr_927 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.BoundPattern('_BoundPattern934_')])
PatternExpr_1380 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.BoundPattern('_BoundPattern1387_')])
PatternExpr_1894 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.BoundPattern('_BoundPattern1901_')])
_config_object = {'channel': 'fifo'}
from nacl.hash import sha256
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
from json import dumps
from ast import literal_eval
from time import time, sleep
from config import *
import read_config

class Replica(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._ReplicaReceivedEvent_0 = []
        self._ReplicaReceivedEvent_6 = []
        self._ReplicaReceivedEvent_7 = []
        self._ReplicaReceivedEvent_8 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_0', PatternExpr_402, sources=[PatternExpr_406], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_1', PatternExpr_420, sources=[PatternExpr_424], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_419]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_2', PatternExpr_441, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_440]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_3', PatternExpr_522, sources=[PatternExpr_529], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_521]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_4', PatternExpr_549, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_548]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_5', PatternExpr_587, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_586]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_6', PatternExpr_919, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_7', PatternExpr_1372, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_8', PatternExpr_1886, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_9', PatternExpr_1939, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_1938]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_10', PatternExpr_2128, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_2127]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_11', PatternExpr_2454, sources=[PatternExpr_2458], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_2453]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_12', PatternExpr_2487, sources=[PatternExpr_2494], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_2486]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_13', PatternExpr_2568, sources=[PatternExpr_2572], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_2567]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_14', PatternExpr_2594, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_2593])])

    def setup(self, id, name, running_state, replica_failures, replica_timeout, olympus_public_key, checkpt_interval, slot_number, **rest_3010):
        super().setup(id=id, name=name, running_state=running_state, replica_failures=replica_failures, replica_timeout=replica_timeout, olympus_public_key=olympus_public_key, checkpt_interval=checkpt_interval, slot_number=slot_number, **rest_3010)
        self._state.id = id
        self._state.name = name
        self._state.running_state = running_state
        self._state.replica_failures = replica_failures
        self._state.replica_timeout = replica_timeout
        self._state.olympus_public_key = olympus_public_key
        self._state.checkpt_interval = checkpt_interval
        self._state.slot_number = slot_number
        self.output_wrapper(('Replica failures: ' + str(self._state.replica_failures)))
        self._state.status = 0
        self._state.order_proof = list()
        self._state.result_proof = list()
        self._state.result_cache = dict()
        self._state.checkpoint = 0
        self._state.checkpt_proof = list()
        self._state.last_slot_number = self._state.slot_number
        self._state.olympus = None
        self._state.replicas = None
        self._state.head = None
        self._state.tail = None
        self._state.replica_public_keys = None
        self._state.private_key = None
        self._state.client_keys = dict()
        self._state.configuration = None
        self._state.pending_failures = {}
        self._state.pending_failure_scenarios = {}
        self._state.messages_received_from_client = {}
        self._state.messages_shuttle = {}
        self._state.messages_result_shuttle = {}
        self._state.messages_forwarded_request = {}
        self._state.ongoing_request_id = None
        self._state.history = list()
        self._state.most_recent_result = dict()
        self._state.request_to_client = dict()

    def run(self):
        self._state.status = 1
        self._state.olympus_public_key = VerifyKey(self._state.olympus_public_key, encoder=HexEncoder)
        self.output_wrapper(((('A new replica (' + str(self._state.name)) + ') ') + ' is created.'))
        super()._label('_st_label_399', block=False)
        _st_label_399 = 0
        while (_st_label_399 == 0):
            _st_label_399 += 1
            if PatternExpr_408.match_iter(self._ReplicaReceivedEvent_0, _BoundPattern414_=self._state.olympus, SELF_ID=self._id):
                _st_label_399 += 1
            else:
                super()._label('_st_label_399', block=True)
                _st_label_399 -= 1

    def validate_checkpoint(self, checkpt_p):
        if (len(checkpt_p) == 0):
            return False
        checkpt = checkpt_p[0]
        if ((not (checkpt_p.count(checkpt) == len(checkpt_p))) or (checkpt[0] <= self._state.checkpoint)):
            return False
        return True

    def update_running_state(self, type, args):
        if (type == 'put'):
            if (len(args) > 1):
                self._state.running_state[args[0]] = args[1]
            return 'OK'
        elif (type == 'get'):
            if (len(args) > 0):
                if (args[0] in self._state.running_state):
                    return self._state.running_state[args[0]]
                else:
                    return ''
        elif (type == 'slice'):
            if (len(args) > 1):
                (lower, upper) = map(int, args[1].split(':'))
                if ((args[0] in self._state.running_state) and (lower >= 0) and (upper <= len(self._state.running_state[args[0]]))):
                    self._state.running_state[args[0]] = self._state.running_state[args[0]][lower:upper]
                    return self._state.running_state[args[0]]
                else:
                    return 'fail'
        elif (type == 'append'):
            if (len(args) > 1):
                if (args[0] in self._state.running_state):
                    self._state.running_state[args[0]] = (self._state.running_state[args[0]] + args[1])
                    return 'OK'
                else:
                    return 'fail'

    def calculate_hash(self, val):
        if isinstance(val, str):
            return sha256(str.encode(val), encoder=HexEncoder)
        elif isinstance(val, dict):
            return sha256(str.encode(dumps(val, sort_keys=True)), encoder=HexEncoder)
        return sha256(val, encoder=HexEncoder)

    def validate_shuttle(self, shuttle):
        (self._state.order_proof, self._state.result_proof) = shuttle
        (self._state.slot_number, operation, self._state.configuration, order_stmt, request_id) = self._state.order_proof
        if (not (self._state.last_slot_number == (self._state.slot_number - 1))):
            return False
        for stmt in order_stmt:
            if ((not (stmt[0] == self._state.slot_number)) or (not (stmt[1] == operation)) or (not (stmt[2] == self._state.configuration))):
                return False
        return True

    def validate_result_shuttle(self, result_shuttle):
        (result, self._state.result_proof) = result_shuttle
        if (not (len(self._state.result_proof) == len(self._state.replicas))):
            return False
        hash = self.calculate_hash(result)
        for i in self._state.result_proof:
            if (not (hash == i[1])):
                return False
        return True

    def sign_and_send(self, data, to_):
        data = ([self._state.id] + list(data))
        data[(- 1)] = self._state.private_key.sign(str(data[(- 1)]).encode('utf-8'))
        self.send(tuple(data), to=to_)

    def verify_data_with_key(self, data, pub_key):
        try:
            pub_key.verify(data)
            return literal_eval(data.message.decode('utf-8'))
        except BadSignatureError:
            return None

    def check_failure(self, replica_failures, source_id, source_message_count, required_type):
        for (i, failure) in enumerate(replica_failures):
            oper = failure.operands
            if ((failure.failure_type == required_type) and (source_id == oper[0]) and (source_message_count == oper[1])):
                return (True, failure)
        return (False, None)

    def output_wrapper(self, log):
        self.output('[TS: {}][{}]'.format(str(time()), self._state.name), log)

    def _Replica_handler_419(self, olympus):
        self.output_wrapper((((self._state.name + " is now shutting down.\nIt's final running state is:\n") + str(self._state.running_state)) + '.\n'))
    _Replica_handler_419._labels = None
    _Replica_handler_419._notlabels = None

    def _Replica_handler_440(self, olympus_, replicas_, head_, tail_, config_data):
        self._state.olympus = olympus_
        self._state.replicas = replicas_
        self._state.head = head_
        self._state.tail = tail_
        config_data = self.verify_data_with_key(config_data, self._state.olympus_public_key)
        if (config_data is None):
            self.output_wrapper('Verification of message sent by Olympus has failed.')
            self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
            return
        (replica_public_keys_, self._state.configuration) = config_data
        self._state.replica_public_keys = [VerifyKey(key, encoder=HexEncoder) for key in replica_public_keys_]
        self.output_wrapper('{} received replica references and public keys from Olympus'.format(self._state.name))
        self.send(('ACK', self._state.name), to=self._state.olympus)
    _Replica_handler_440._labels = None
    _Replica_handler_440._notlabels = None

    def _Replica_handler_521(self, private_key_, olympus):
        self._state.private_key = private_key_
        self.output_wrapper((self._state.name + ' has received its private key from Olympus.'))
        self.send(('ACK', self._state.name), to=olympus)
    _Replica_handler_521._labels = None
    _Replica_handler_521._notlabels = None

    def _Replica_handler_548(self, client_id, client_public_key):
        self._state.client_keys[client_id] = VerifyKey(client_public_key, encoder=HexEncoder)
        self.output_wrapper('{} has received client public key: {} for client {}'.format(self._state.name, str(client_public_key), str(client_id)))
        self.send(('ACK', self._state.name), to=self._state.olympus)
    _Replica_handler_548._labels = None
    _Replica_handler_548._notlabels = None

    def _Replica_handler_586(self, sender_id, type, request_from, client, request_id, client_id, client_args, args):
        self.output_wrapper((((((((str(type) + ' request with request id ') + str(request_id)) + ' from ') + str(request_from)) + ' is received by ') + str(self._state.name)) + '.'))
        self._state.request_to_client[request_id] = client_id
        if (self._state.status == 0):
            self.output_wrapper((self._state.name + ' is in PENDING state.'))
        elif (self._state.status == 1):
            self.output_wrapper((self._state.name + ' is in ACTIVE state.'))
        elif (self._state.status == 2):
            self.output_wrapper((self._state.name + ' is in IMMUTABLE state.'))
        if (not (self._state.status == 1)):
            if ((request_from == client) and (self._state.status == 2)):
                self.output_wrapper('Sending ERROR message to the client.')
                self.send((self._state.id, 'Operation_result_error', request_id), to=client)
            return
        if ((isinstance(self._state.head, set) and (self._id in self._state.head)) or ((not isinstance(self._state.head, set)) and (self._id == self._state.head))):
            if (self._state.ongoing_request_id == request_id):
                self.output_wrapper((((('Request id ' + str(request_id)) + ' of Client ') + str(client_id)) + ' is already running.'))
                return
            self._state.ongoing_request_id = request_id
        if (request_from == client):
            if (not (client_id in self._state.messages_received_from_client)):
                self._state.messages_received_from_client[client_id] = 0
            (is_trigger, scenario) = self.check_failure(self._state.replica_failures, client_id, self._state.messages_received_from_client[client_id], FailureType.client_request)
            if is_trigger:
                self._state.pending_failures[scenario.action_type] = 1
                self._state.pending_failure_scenarios[scenario.action_type] = scenario
                self.output_wrapper('Replica {}: Trigger client request failure for client_id: {} and message count: {}, scenario: {}'.format(self._state.name, client_id, self._state.messages_received_from_client[client_id], self._state.pending_failures))
            self._state.messages_received_from_client[client_id] += 1
            args = self.verify_data_with_key(client_args, self._state.client_keys[client_id])
            if (args == None):
                self.output_wrapper((('Verification of message sent by Client ' + str(client_id)) + ' has failed.'))
                self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                return
            if (request_id in self._state.result_cache):
                self.sign_and_send(('Operation_result', self._state.result_cache[(client_id, request_id)]), client)
                self.send(('Operation_result_' + str(request_id)), to=client)
                self.output_wrapper((((((('Result sent to Client ' + str(client_id)) + ' for request id ') + str(request_id)) + ' from the cache of ') + self._state.name) + '.'))
                return
            elif ((isinstance(self._state.head, set) and (not (self._id in self._state.head))) or ((not isinstance(self._state.head, set)) and (not (self._id == self._state.head)))):
                self.output_wrapper((('Forwarding the request received from Client ' + str(client_id)) + ' to HEAD.'))
                self.sign_and_send(('Request', type, self._id, client, request_id, client_id, client_args, client_args), self._state.head)
                super()._label('_st_label_916', block=False)
                _st_label_916 = 0
                self._timer_start()
                while (_st_label_916 == 0):
                    _st_label_916 += 1
                    if PatternExpr_927.match_iter(self._ReplicaReceivedEvent_6, _BoundPattern934_=('Result_shuttle_' + str(request_id)), SELF_ID=self._id):
                        self.output_wrapper(((('Head-forwarded result shuttle is received at ' + str(self._state.name)) + ' for request id ') + str(request_id)))
                        _st_label_916 += 1
                    elif self._timer_expired:
                        self.output_wrapper((((((str(self._state.name) + ' has timed out waiting for the result shuttle of head-forwarded request id ') + str(request_id)) + ' from Client ') + str(client_id)) + '. Sending reconfiguration request.'))
                        self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                        _st_label_916 += 1
                    else:
                        super()._label('_st_label_916', block=True, timeout=self._state.replica_timeout)
                        _st_label_916 -= 1
                return
        else:
            _client_args = self.verify_data_with_key(client_args, self._state.client_keys[client_id])
            if (_client_args == None):
                self.output_wrapper((('Verification of message forwarded by head and sent by Client ' + str(client_id)) + ' has failed.'))
                self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                return
            args = self.verify_data_with_key(args, self._state.replica_public_keys[sender_id])
            if (args == None):
                self.output_wrapper((('Verification of message sent by Replica ' + str(sender_id)) + ' has failed.'))
                self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                return
            if (not (_client_args == args[0][1][1])):
                self.output_wrapper((('Verification of operations forwarded by head and sent by Client ' + str(client_id)) + ' has failed. Head might be faulty.'))
                self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                return
        if ((isinstance(self._state.head, set) and (self._id in self._state.head)) or ((not isinstance(self._state.head, set)) and (self._id == self._state.head))):
            if ((isinstance(request_from, set) and (not (client in request_from))) or ((not isinstance(request_from, set)) and (not (request_from == client)))):
                if (not (client_id in self._state.messages_forwarded_request)):
                    self._state.messages_forwarded_request[client_id] = 0
                (is_trigger, scenario) = self.check_failure(self._state.replica_failures, client_id, self._state.messages_forwarded_request[client_id], FailureType.forwarded_request)
                if is_trigger:
                    self._state.pending_failures[scenario.action_type] = 1
                    self._state.pending_failure_scenarios[scenario.action_type] = scenario
                    self.output_wrapper('Replica {}: Trigger forwarded request failure for client_id: {} and message count: {}, scenario: {}'.format(self._state.name, client_id, self._state.messages_forwarded_request[client_id], scenario))
                self._state.messages_forwarded_request[client_id] += 1
            self._state.slot_number += 1
            result = self.update_running_state(type, args)
            if ((self._state.slot_number > 0) and ((self._state.slot_number % self._state.checkpt_interval) == 0)):
                self.output_wrapper((('Initiating checkpoint shuttle for slot number: ' + str(self._state.slot_number)) + '.'))
                self._state.checkpt_proof = [[self._state.slot_number, self.calculate_hash(self._state.running_state)]]
            else:
                self._state.checkpt_proof = None
            res_stmt = [(type, args), self.calculate_hash(result)]
            self._state.most_recent_result[client_id] = [result, res_stmt, request_id]
            if ((FailureActionType.change_operation in self._state.pending_failures) and (self._state.pending_failures[FailureActionType.change_operation] == 1)):
                stmt_type = 'get'
                stmt_args = ['x']
                self.output_wrapper('Executing failure scenario: {}'.format(str(self._state.pending_failure_scenarios[FailureActionType.change_operation])))
                self._state.pending_failures[FailureActionType.change_operation] = 0
                self._state.pending_failure_scenarios[FailureActionType.change_operation] = None
            else:
                stmt_type = type
                stmt_args = args
            order_stmt = [[self._state.slot_number, (stmt_type, stmt_args), self._state.configuration]]
            self._state.order_proof = [self._state.slot_number, (type, args), self._state.configuration, order_stmt, request_id]
            self._state.result_proof = [[(type, args), self.calculate_hash(result)]]
            shuttle = (self._state.order_proof, self._state.result_proof, self._state.checkpt_proof)
            self._state.history.append(self._state.order_proof)
            self.output_wrapper((((((((('Shuttle with slot number ' + str(self._state.slot_number)) + ' for request id ') + str(request_id)) + ' and Client ') + str(client_id)) + ' is sent from ') + str(self._state.name)) + ' to next replica.'))
            self.sign_and_send(('Request', type, self._id, client, request_id, client_id, client_args, shuttle), self._state.replicas.get((self._state.id + 1)))
            self._state.last_slot_number = self._state.slot_number
            super()._label('_st_label_1369', block=False)
            _st_label_1369 = 0
            self._timer_start()
            while (_st_label_1369 == 0):
                _st_label_1369 += 1
                if PatternExpr_1380.match_iter(self._ReplicaReceivedEvent_7, _BoundPattern1387_=('Result_shuttle_' + str(request_id)), SELF_ID=self._id):
                    self._state.ongoing_request_id = None
                    _st_label_1369 += 1
                elif self._timer_expired:
                    self.output_wrapper('{} has timed out while waiting for result shuttle for request id {}. Sending reconfiguration request to Olympus'.format(self._state.name, str(request_id)))
                    self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                    return
                    _st_label_1369 += 1
                else:
                    super()._label('_st_label_1369', block=True, timeout=self._state.replica_timeout)
                    _st_label_1369 -= 1
        else:
            if (not (client_id in self._state.messages_shuttle)):
                self._state.messages_shuttle[client_id] = 0
            (is_trigger, scenario) = self.check_failure(self._state.replica_failures, client_id, self._state.messages_shuttle[client_id], FailureType.shuttle)
            if is_trigger:
                self._state.pending_failures[scenario.action_type] = 1
                self._state.pending_failure_scenarios[scenario.action_type] = scenario
                self.output_wrapper('Replica {}: Trigger shuttle failure for client_id: {} and message count: {}, scenario: {}'.format(self._state.name, client_id, self._state.messages_shuttle[client_id], scenario))
            self._state.messages_shuttle[client_id] += 1
            if (not self.validate_shuttle(args[:(- 1)])):
                self.output_wrapper('{} failed to validate shuttle for request_id: {}. Triggering reconfiguration'.format(self._state.name, request_id))
                self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                return
            (self._state.order_proof, self._state.result_proof, self._state.checkpt_proof) = args
            (self._state.slot_number, operation, self._state.configuration, order_stmt, request_id) = self._state.order_proof
            (type, operation_args) = operation
            result = self.update_running_state(type, operation_args)
            if ((not (self._state.checkpt_proof == None)) and (self._state.slot_number > 0) and ((self._state.slot_number % self._state.checkpt_interval) == 0)):
                if self.validate_checkpoint(self._state.checkpt_proof):
                    self._state.checkpt_proof.append([self._state.slot_number, self.calculate_hash(self._state.running_state)])
                else:
                    self.output_wrapper((('Checkpoint validation has failed at ' + str(self._state.name)) + '. Sending reconfiguration request.'))
                    self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                    return
            res_stmt = [(type, operation_args), self.calculate_hash(result)]
            self._state.most_recent_result[client_id] = [result, res_stmt, request_id]
            if ((FailureActionType.change_operation in self._state.pending_failures) and (self._state.pending_failures[FailureActionType.change_operation] == 1)):
                self.output_wrapper('Executing failure scenario: {}'.format(str(self._state.pending_failure_scenarios[FailureActionType.change_operation])))
                type = 'get'
                operation_args = ['x']
                self._state.pending_failures[FailureActionType.change_operation] = 0
                self._state.pending_failure_scenarios[FailureActionType.change_operation] = None
            self._state.order_proof[3].append([self._state.slot_number, (type, operation_args), self._state.configuration])
            self._state.result_proof.append([(type, operation_args), self.calculate_hash(result)])
            shuttle = (self._state.order_proof, self._state.result_proof, self._state.checkpt_proof)
            self._state.history.append(self._state.order_proof)
            if ((isinstance(self._state.tail, set) and (self._id in self._state.tail)) or ((not isinstance(self._state.tail, set)) and (self._id == self._state.tail))):
                result_shuttle = [result, self._state.result_proof]
                if ((FailureActionType.change_result in self._state.pending_failures) and (self._state.pending_failures[FailureActionType.change_result] == 1)):
                    op_t = result_shuttle[1][self._state.id][0]
                    result_shuttle[1][self._state.id] = [op_t, self.calculate_hash('OK')]
                if ((FailureActionType.drop_result_stmt in self._state.pending_failures) and (self._state.pending_failures[FailureActionType.drop_result_stmt] == 1)):
                    result_t = result_shuttle[0]
                    result_shuttle = [result_t, result_shuttle[1][1:]]
                self.sign_and_send(('Operation_result', request_id, result_shuttle), client)
                self.send(('Operation_result_' + str(request_id)), to=client)
                self.sign_and_send(('Result_shuttle', self._id, request_id, client_id, result_shuttle), self._state.tail)
                self.send(('Result_shuttle_' + str(request_id)), to=self._state.tail)
                if ((not (self._state.checkpt_proof == None)) and (self._state.slot_number > 0) and ((self._state.slot_number % self._state.checkpt_interval) == 0)):
                    self.sign_and_send(('Checkpoint_proof', self._state.checkpt_proof), self._id)
                self._state.last_slot_number = self._state.slot_number
            else:
                self.output_wrapper((((((((('Shuttle with slot number ' + str(self._state.slot_number)) + ' for request id ') + str(request_id)) + ' and Client ') + str(client_id)) + ' is sent from ') + str(self._state.name)) + ' to next replica.'))
                if ((not (self._state.checkpt_proof == None)) and (self._state.slot_number > 0) and ((self._state.slot_number % self._state.checkpt_interval) == 0)):
                    self.output_wrapper((((('Checkpoint shuttle for slot number: ' + str(self._state.slot_number)) + ' is at ') + str(self._state.name)) + '. Forwarding it to next Replica.'))
                self.sign_and_send(('Request', type, self._id, client, request_id, client_id, client_args, shuttle), self._state.replicas.get((self._state.id + 1)))
                self._state.last_slot_number = self._state.slot_number
                super()._label('_st_label_1883', block=False)
                _st_label_1883 = 0
                self._timer_start()
                while (_st_label_1883 == 0):
                    _st_label_1883 += 1
                    if PatternExpr_1894.match_iter(self._ReplicaReceivedEvent_8, _BoundPattern1901_=('Result_shuttle_' + str(request_id)), SELF_ID=self._id):
                        pass
                        _st_label_1883 += 1
                    elif self._timer_expired:
                        self.output_wrapper((((((str(self._state.name) + ' has timed out waiting for the result shuttle of request id ') + str(request_id)) + ' from Client ') + str(client_id)) + '. Sending reconfiguration request.'))
                        self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
                        return
                        _st_label_1883 += 1
                    else:
                        super()._label('_st_label_1883', block=True, timeout=self._state.replica_timeout)
                        _st_label_1883 -= 1
    _Replica_handler_586._labels = None
    _Replica_handler_586._notlabels = None

    def _Replica_handler_1938(self, sender_id, args):
        args = self.verify_data_with_key(args, self._state.replica_public_keys[sender_id])
        if (args == None):
            self.output_wrapper((('Verification of message sent by Replica ' + str(sender_id)) + ' has failed.'))
            self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
            return
        if (not self.validate_checkpoint(args)):
            self.output_wrapper((('Checkpoint proof validation back the chain has failed at ' + str(self._state.name)) + '. Sending reconfiguration request.'))
            self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
            return
        s_n = args[0][0]
        self._state.checkpoint = s_n
        self._state.history = self._state.history[self._state.checkpoint:]
        self.output_wrapper((((('Truncating history at ' + str(self._state.name)) + ' to validated checkpoint proof on the slot number ') + str(self._state.checkpoint)) + '.'))
        if ((isinstance(self._state.head, set) and (not (self._id in self._state.head))) or ((not isinstance(self._state.head, set)) and (not (self._id == self._state.head)))):
            self.output_wrapper((((('Checkpoint proof shuttle back the chain for slot number: ' + str(s_n)) + ' is at ') + str(self._state.name)) + '. Forwarding it to next Replica back the chain.'))
            self.sign_and_send(('Checkpoint_proof', args), self._state.replicas.get((self._state.id - 1)))
        else:
            self.output_wrapper(('Checkpointing is complete at checkpoint ' + str(self._state.checkpoint)))
    _Replica_handler_1938._labels = None
    _Replica_handler_1938._notlabels = None

    def _Replica_handler_2127(self, sender_id, request_from, request_id, client_id, result_shuttle):
        if (not (client_id in self._state.messages_result_shuttle)):
            self._state.messages_result_shuttle[client_id] = 0
        (is_trigger, scenario) = self.check_failure(self._state.replica_failures, client_id, self._state.messages_result_shuttle[client_id], FailureType.result_shuttle)
        if is_trigger:
            self._state.pending_failures[scenario.action_type] = 1
            self._state.pending_failure_scenarios[scenario.action_type] = scenario
            self.output_wrapper('{}: Trigger result shuttle failure for client_id: {} and message count: {}, scenario: {}'.format(self._state.name, client_id, self._state.messages_result_shuttle[client_id], scenario))
        self._state.messages_result_shuttle[client_id] += 1
        result_shuttle = self.verify_data_with_key(result_shuttle, self._state.replica_public_keys[sender_id])
        if (result_shuttle == None):
            self.output_wrapper((('Verification of message sent by Replica ' + str(sender_id)) + ' has failed.'))
            self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
            return
        if self.validate_result_shuttle(result_shuttle):
            self._state.result_cache[(client_id, request_id)] = result_shuttle
            if ((isinstance(self._state.head, set) and (not (self._id in self._state.head))) or ((not isinstance(self._state.head, set)) and (not (self._id == self._state.head)))):
                if ((FailureActionType.change_result in self._state.pending_failures) and (self._state.pending_failures[FailureActionType.change_result] == 1)):
                    self.output_wrapper('Executing failure scenario: {}'.format(str(self._state.pending_failure_scenarios[FailureActionType.change_result])))
                    op_t = result_shuttle[1][self._state.id][0]
                    result_shuttle[1][self._state.id] = [op_t, self.calculate_hash('OK')]
                    self._state.pending_failures[FailureActionType.change_result] = 0
                    self._state.pending_failure_scenarios[FailureActionType.change_result] = None
                if ((FailureActionType.drop_result_stmt in self._state.pending_failures) and (self._state.pending_failures[FailureActionType.drop_result_stmt] == 1)):
                    self.output_wrapper('Executing failure scenario: {}'.format(str(self._state.pending_failure_scenarios[FailureActionType.drop_result_stmt])))
                    result_t = result_shuttle[0]
                    result_shuttle = [result_t, result_shuttle[1][1:]]
                    self._state.pending_failures[FailureActionType.drop_result_stmt] = 0
                    self._state.pending_failure_scenarios[FailureActionType.drop_result_stmt] = None
                self.sign_and_send(('Result_shuttle', self._id, request_id, client_id, result_shuttle), self._state.replicas.get((self._state.id - 1)))
                self.send(('Result_shuttle_' + str(request_id)), to=self._state.replicas.get((self._state.id - 1)))
            self.output_wrapper((((((('Result shuttle for request id ' + str(request_id)) + ' of Client ') + str(client_id)) + ' is at ') + str(self._state.name)) + '.'))
        else:
            self.output_wrapper((((((('Result shuttle sent by Replica ' + str(sender_id)) + ' for request id ') + str(request_id)) + ' of Client ') + str(client_id)) + ' is not valid.'))
            self.send(('Reconfiguration', self._state.name, self._state.configuration), to=self._state.olympus)
            return
    _Replica_handler_2127._labels = None
    _Replica_handler_2127._notlabels = None

    def _Replica_handler_2453(self, olympus):
        self._state.status = 2
        self.output_wrapper((str(self._state.name) + ' is now IMMUTABLE.'))
        self.output_wrapper('Received wedge request from Olympus')
        self.send(('wedge', self._state.history, self._state.checkpt_proof, self._state.checkpoint, self._state.id), to=olympus)
    _Replica_handler_2453._labels = None
    _Replica_handler_2453._notlabels = None

    def _Replica_handler_2486(self, gap, olympus):
        for op_to_apply in gap:
            type = op_to_apply[1][0]
            args = op_to_apply[1][1]
            config = op_to_apply[2]
            result = self.update_running_state(type, args)
            request_id = op_to_apply[3]
            res_stmt = [(type, args), self.calculate_hash(result)]
            self._state.most_recent_result[self._state.request_to_client[request_id]] = [result, res_stmt, request_id]
        self.send(('caught_up', self.calculate_hash(self._state.running_state), self._state.id, self._state.most_recent_result), to=olympus)
    _Replica_handler_2486._labels = None
    _Replica_handler_2486._notlabels = None

    def _Replica_handler_2567(self, olympus):
        self.output_wrapper((('Response to get_running_state sent to Olympus by ' + str(self._state.name)) + '.'))
        self.send(('response_get_running_state', self._state.id, self._state.running_state), to=olympus)
    _Replica_handler_2567._labels = None
    _Replica_handler_2567._notlabels = None

    def _Replica_handler_2593(self, client, requests_):
        self.send(('running_state', self._state.running_state), to=client)
        self.send(('running_state_' + str(requests_)), to=client)
    _Replica_handler_2593._labels = None
    _Replica_handler_2593._notlabels = None
