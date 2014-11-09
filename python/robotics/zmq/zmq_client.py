import logging
import socket
import sys
import termios
import time
import tty
import uuid
import zmq


# Logging.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Configuration.
CONTROL_CENTER_ID = uuid.uuid4().hex

# Protocol.
TOPIC_DISCOVERY = 'DISCOVERY'

COMMAND_ANYBODY_HOME = 'AHOME'
COMMAND_INSTRUCTION = 'INSTRUCTION'
COMMAND_DISCONNECT = 'DISCONNECT'

# Char to intrsuction map.
CHAR_TO_INSTRUCTION_MAP = {
    'W': 'FORWARD',
    'Q': 'FORWARD_LEFT',
    'E': 'FORWARD_RIGHT',
    'X': 'BACKWARD',
    'Z': 'BACKWARD_LEFT',
    'C': 'BACKWARD_RIGHT',
    'A'; 'LEFT_ROTATION',
    'D': 'RIGHT_ROTATION',
    'S': 'STOP',    
}


def readch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def trigger_discovery(context, local_ip):
    log.info('Polling autobots...')

    pub = context.socket(zmq.PUB)
    pub.bind('epgm://{};239.192.1.1:5555'.format(local_ip))

    rep = context.socket(zmq.REP)
    rep.bind('tcp://{}:5556'.format(local_ip))

    poller = zmq.Poller()
    poller.register(rep, zmq.POLLIN)

    autobots = {}
    for i in xrange(0, 5):
        if len(autobots) == 0:
            pub.send_multipart(
                [TOPIC_DISCOVERY, COMMAND_ANYBODY_HOME, '{}:5556'.format(local_ip)])

        try:
            socks = dict(poller.poll(1000))
        except KeyboardInterrupt:
            break

        if rep in socks:
            command, device, address = rep.recv_multipart()
            rep.send_multipart([command, 'ACKNOWLEDGED'])
            log.info('Received command {} from device {} at address {}'.format(
                command, device, address))
            autobots[device] = address

    rep.close()
    pub.close()
    return autobots


def take_control(context, name, remote_control_address):
    log.info('Taking control over autobot {} at {}'.format(
        name, remote_control_address))
    req = context.socket(zmq.REQ)
    req.connect('tcp://{}'.format(remote_control_address))

    while True:
        ch = readch().upper()
        instruction = CHAR_TO_INSTRUCTION_MAP.get(ch, None)
        log.info('Preseed {}. Sending instruction {}'.format(ch, instruction))
        if instruction is None:
            req.send_multipart([CONTROL_CENTER_ID, COMMAND_DISCONNECT, ''])
        elif:
            req.send_multipart(
                [CONTROL_CENTER_ID, COMMAND_INSTRUCTION, instruction])
        status, message = req.recv_multipart()
        log.info('Instruction result: {} status: {} message: {}'.format(
            instruction, status, message))
        if instruction is None:
            break

    req.close()


def main():
    context = zmq.Context()
    local_ip = socket.gethostbyname(socket.gethostname())

    while True:
        print '------------------------------------------'
        print '| Choose your destiny (press q to quit): |'
        print '| 1. Discover autobots.                  |'
        print '------------------------------------------'
        option = readch()
        print ''
        if option == '1':
            autobots = trigger_discovery(context, local_ip)
            log.info('Discovered autobots: %s', autobots)

            while True:
                names = autobots.keys()

                if len(names) == 0:
                    print 'No autobots found'
                    print ''
                    break

                print 'Pick autobot (press q to return to the previous menu)'
                for idx, autobot in enumerate(names, start=1):
                    print '{}. {}'.format(idx, autobot)
                option = readch()
                print ''
                if option == 'q':
                    break

                try:
                    idx = int(option) - 1
                except ValueError:
                    print 'Wrong option'
                    print ''
                    continue
                if idx >= 0 and idx < len(names):
                    name = names[idx]
                    address = autobots[name]
                    take_control(context, name, address)
                else:
                    print 'Wrong option'
                    print ''
                    continue
        elif option == 'q':
            break
        else:
            print 'Wrong option'
            print ''
            continue

    context.term()

if __name__ == '__main__':
    main()
