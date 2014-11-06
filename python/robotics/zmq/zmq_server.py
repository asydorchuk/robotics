from datetime import datetime as dt
import logging
import socket
import zmq


# Protocol.
STATE_DISCOVERY = 'DISCOVERY'
STATE_RECEIVING = 'RECEIVING'

TOPIC_DISCOVERY = 'DISCOVERY'

RCOMMAND_ANYBODY_HOME = 'AHOME'
RCOMMAND_OBEY = 'OBEY'
RCOMMAND_PING = 'PING'
RCOMMAND_INSTRUCTION = 'INSTRUCTION'
RCOMMAND_DISCONNECT = 'DISCONNECT'

LCOMMAND_HOME_ALONE = 'HOMEALONE'
LCOMMAND_STATUS_SUCCESS = 'SUCCESS'
LCOMMAND_STATUS_FAILURE = 'FAILURE'

# Settings.
POLL_INTERVAL = 1000  # 1sec
LINGER_TIMEOUT = 5000  # 5 secs
CONTROL_TIMEOUT = 10  # 10 secs
DEVICE_NAME = 'AIZEK-27'


# Logging.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def run_zmq_server(robot):
    context = zmq.Context()
    local_ip = socket.gethostbyname(socket.gethostname())
    local_control_address = '{}:5557'.format(local_ip)

    discovery_sub = context.socket(zmq.SUB)
    discovery_sub.connect('epgm://wlan0;239.192.1.1:5555')
    discovery_sub.setsockopt(zmq.SUBSCRIBE, TOPIC_DISCOVERY)

    control_rep = context.socket(zmq.REP)
    control_rep.bind('tcp://{}'.format(local_control_address))

    poller = zmq.Poller()
    poller.register(discovery_sub, zmq.POLLIN)
    poller.register(control_rep, zmq.POLLIN)

    state = STATE_DISCOVERY
    active_cc_id = None
    last_req_time = dt.now()
    while True:
        try:
            socks = dict(poller.poll(POLL_INTERVAL))
        except KeyboardInterrupt:
            break
        log.info('Poll round complete...')

        if state == STATE_RECEIVING:
            ctime = dt.now()
            dtime = ctime - last_req_time
            if dtime.seconds > CONTROL_TIMEOUT:
                log.info(
                    'No instructions for {} secs. Control released'.format(dtime.seconds))
                state = STATE_DISCOVERY
                active_cc_id = None

        if discovery_sub in socks:
            _, command, raddress = discovery_sub.recv_multipart()
            log.info(
                'Discovered command {} from address {}'.format(command, raddress))
            if command == RCOMMAND_ANYBODY_HOME and state == STATE_DISCOVERY:
                log.info(
                    'Sending discovery notification to {}'.format(raddress))
                req = context.socket(zmq.REQ)
                req.connect('tcp://{}'.format(raddress))
                req.send_multipart(
                    [LCOMMAND_HOME_ALONE, DEVICE_NAME, local_control_address])
                req.close(linger=LINGER_TIMEOUT)

        if control_rep in socks:
            cc_id, command, instruction = control_rep.recv_multipart()
            instruction = instruction.upper()
            log.info('Received command: {} from control center: {} with instruction: {}'.format(
                command, cc_id, instruction))
            if active_cc_id and active_cc_id != cc_id:
                control_rep.send_multipart([LCOMMAND_STATUS_FAILURE, 'Command rejected: protocol violation'])
            else:
                state = STATE_RECEIVING
                active_cc_id = cc_id
                last_req_time = dt.now()
                if command == RCOMMAND_OBEY:
                    control_rep.send_multipart([LCOMMAND_STATUS_SUCCESS, 'Control granted'])
                elif command == RCOMMAND_PING:
                    control_rep.send_multipart([LCOMMAND_STATUS_SUCCESS, 'Ping received'])
                elif command == RCOMMAND_INSTRUCTION:
                    control_rep.send_multipart([LCOMMAND_STATUS_SUCCESS, 'Roger that'])
                elif command == RCOMMAND_DISCONNECT:
                    state = STATE_DISCOVERY
                    active_cc_id = None
                    control_rep.send_multipart([LCOMMAND_STATUS_SUCCESS, 'Control released'])
                else:
                    control_rep.send_multipart([LCOMMAND_STATUS_FAILURE, 'Unknown command: {}'.format(command)])

    control_rep.close()
    discovery_sub.close()
    context.term()


if __name__ == '__main__':
    run_zmq_server(None)
