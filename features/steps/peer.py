from utils import instrument
import mock


@given(u'a packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_packet('this is a test packet')


@when(u'peer.send_packet is called')  # noqa
def step_impl(context):
    context.peer.send_packet(context.packet)


@when(u'all data with the peer is processed')  # noqa
def step_impl(context):
    context.peer.run()


@then(u'the packet sent through connection should be the given packet')  # noqa
def step_impl(context):
    assert context.sent_packets == [context.packet]


@when(u'peer.send_Hello is called')  # noqa
def step_impl(context):
    context.peer.send_Hello()


@then(u'the packet sent through connection should be a Hello packet')  # noqa
def step_impl(context):
    packet = context.packeter.dump_Hello()
    assert context.sent_packets == [packet]


@given(u'a valid Hello packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_Hello()


@given(u'a Hello packet with protocol version incompatible')  # noqa
def step_impl(context):
    packeter = context.packeter
    data = [packeter.cmd_map_by_name['Hello'],
            'incompatible_protocal_version',
            packeter.NETWORK_ID,
            packeter.CLIENT_ID,
            packeter.config.getint('network', 'listen_port'),
            packeter.CAPABILITIES,
            packeter.config.get('wallet', 'pub_key')
            ]
    context.packet = packeter.dump_packet(data)


@given(u'a Hello packet with network id incompatible')  # noqa
def step_impl(context):
    packeter = context.packeter
    data = [packeter.cmd_map_by_name['Hello'],
            packeter.PROTOCOL_VERSION,
            'incompatible_network_id',
            packeter.CLIENT_ID,
            packeter.config.getint('network', 'listen_port'),
            packeter.CAPABILITIES,
            packeter.config.get('wallet', 'pub_key')
            ]
    context.packet = packeter.dump_packet(data)


@when(u'peer.send_Hello is instrumented')  # noqa
def step_impl(context):
    context.peer.send_Hello = instrument(context.peer.send_Hello)


@then(u'peer.send_Hello should be called once')  # noqa
def step_impl(context):
    func = context.peer.send_Hello
    assert func.call_count == 1


@when(u'peer.send_Disconnect is instrumented')  # noqa
def step_impl(context):
    context.peer.send_Disconnect = instrument(context.peer.send_Disconnect)


@when(u'the packet is received from peer')  # noqa
def step_impl(context):
    context.add_recv_packet(context.packet)


@then(u'peer.send_Disconnect should be called once with args: reason')  # noqa
def step_impl(context):
    func = context.peer.send_Disconnect
    assert func.call_count == 1
    assert len(func.call_args[0]) == 1 or 'reason' in func.call_args[1]


@when(u'peer.send_Ping is called')  # noqa
def step_impl(context):
    context.peer.send_Ping()


@then(u'the packet sent through connection should be a Ping packet')  # noqa
def step_impl(context):
    packet = context.packeter.dump_Ping()
    assert context.sent_packets == [packet]


@given(u'a Ping packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_Ping()


@when(u'peer.send_Pong is instrumented')  # noqa
def step_impl(context):
    context.peer.send_Pong = instrument(context.peer.send_Pong)


@then(u'peer.send_Pong should be called once')  # noqa
def step_impl(context):
    func = context.peer.send_Pong
    assert func.call_count == 1


@when(u'peer.send_Pong is called')  # noqa
def step_impl(context):
    context.peer.send_Pong()


@then(u'the packet sent through connection should be a Pong packet')  # noqa
def step_impl(context):
    packet = context.packeter.dump_Pong()
    assert context.sent_packets == [packet]


@given(u'a Pong packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_Pong()


@when(u'handler for a disconnect_requested signal is registered')  # noqa
def step_impl(context):
    from pyethereum.signals import disconnect_requested
    context.disconnect_requested_handler = mock.MagicMock()
    disconnect_requested.connect(context.disconnect_requested_handler)


@when(u'peer.send_Disconnect is called')  # noqa
def step_impl(context):
    context.peer.send_Disconnect()


@then(u'the packet sent through connection should be'  # noqa
' a Disconnect packet')
def step_impl(context):
    packet = context.packeter.dump_Disconnect()
    assert context.sent_packets == [packet]


@then(u'the disconnect_requested handler should be called once'  # noqa
' after sleeping for at least 2 seconds')
def step_impl(context):
    import time  # time is already pathced for mocks
    assert context.disconnect_requested_handler.call_count == 1
    sleeping = sum(x[0][0] for x in time.sleep.call_args_list)
    assert sleeping >= 2


@given(u'a Disconnect packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_Disconnect()


@then(u'the disconnect_requested handler should be called once')  # noqa
def step_impl(context):
    assert context.disconnect_requested_handler.call_count == 1


@when(u'peer.send_GetPeers is called')  # noqa
def step_impl(context):
    context.peer.send_GetPeers()


@then(u'the packet sent through connection should be'  # noqa
' a GetPeers packet')
def step_impl(context):
    packet = context.packeter.dump_GetPeers()
    assert context.sent_packets == [packet]


@given(u'a GetPeers packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_GetPeers()


@given(u'peers data')  # noqa
def step_impl(context):
    context.peers_data = [
        ['127.0.0.1', 1234, 'local'],
        ['1.0.0.1', 1234, 'remote'],
    ]


@given(u'a peers data provider')  # noqa
def step_impl(context):
    from pyethereum.signals import peers_data_requested, peers_data_ready

    def peers_data_requested_handler(sender, request_data, **kwargs):
        peers_data_ready.send(
            sender=None, requester=sender, ready_data=context.peers_data)

    context.peers_data_requested_handler = peers_data_requested_handler
    peers_data_requested.connect(context.peers_data_requested_handler)


@when(u'peer.send_Peers is instrumented')  # noqa
def step_impl(context):
    context.peer.send_Peers = instrument(context.peer.send_Peers)


@then(u'peer.send_Peers should be called once with the peers data')  # noqa
def step_impl(context):
    assert context.peer.send_Peers.call_count == 1
    assert context.peer.send_Peers.call_args[0][0] == context.peers_data


@when(u'peer.send_Peers is called')  # noqa
def step_impl(context):
    context.peer.send_Peers(context.peers_data)


@then(u'the packet sent through connection should be a Peers packet'  # noqa
' with the peers data')
def step_impl(context):
    assert context.sent_packets == [
        context.packeter.dump_Peers(context.peers_data)]


@given(u'a Peers packet with the peers data')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_Peers(context.peers_data)


@when(u'handler for a new_peer_received signal is registered')  # noqa
def step_impl(context):
    context.new_peer_received_handler = mock.MagicMock()
    from pyethereum.signals import new_peer_received
    new_peer_received.connect(context.new_peer_received_handler)


@then(u'the new_peer_received handler should be called once'  # noqa
' for each peer')
def step_impl(context):
    call_args_list = context.new_peer_received_handler.call_args_list
    assert len(call_args_list) == len(context.peers_data)
    pairs = zip(call_args_list, context.peers_data)
    for call, peer in pairs:
        assert call[1]['peer'] == peer


@when(u'peer.send_GetTransactions is called')  # noqa
def step_impl(context):
    context.peer.send_GetTransactions()


@then(u'the packet sent through connection should be'  # noqa
' a GetTransactions packet')
def step_impl(context):
    packet = context.packeter.dump_GetTransactions()
    assert context.sent_packets == [packet]


@given(u'a GetTransactions packet')  # noqa
def step_impl(context):
    context.packet = context.packeter.dump_GetTransactions()


@given(u'transactions data')  # noqa
def step_impl(context):
    context.transactions_data = [
        ['nonce-1', 'receiving_address-1', 1],
        ['nonce-2', 'receiving_address-2', 2],
        ['nonce-3', 'receiving_address-3', 3],
    ]


@given(u'a transactions data provider')  # noqa
def step_impl(context):
    from pyethereum.signals import (transactions_data_requested,
                                    transactions_data_ready)

    def handler(sender, request_data, **kwargs):
        transactions_data_ready.send(
            sender=None, requester=sender,
            ready_data=context.transactions_data)

    context.transactions_data_requested_handler = handler
    transactions_data_requested.connect(handler)


@when(u'peer.send_Transactions is instrumented')  # noqa
def step_impl(context):
    context.peer.send_Transactions = instrument(context.peer.send_Transactions)


@then(u'peer.send_Transactions should be called once'  # noqa
' with the transactions data')
def step_impl(context):
    assert context.peer.send_Transactions.call_count == 1
    transactions_args = context.peer.send_Transactions.call_args[0][0]
    assert transactions_args == context.transactions_data
