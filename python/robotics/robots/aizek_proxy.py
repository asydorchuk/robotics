
import json


class AizekProxy(object):

    INSTRUCTION_TO_POWER = {
        'FORWARD': (0.6, 0.6),
        'FORWARD_LEFT': (0.4, 0.6),
        'FORWARD_RIGHT': (0.6, 0.4),
        'BACKWARD': (-0.6, -0.6),
        'BACKWARD_LEFT': (-0.4, -0.6),
        'BACKWARD_RIGHT': (-0.6, -0.4),
        'LEFT_ROTATION': (-0.5, 0.5),
        'RIGHT_ROTATION': (0.5, -0.5),
        'STOP': (0.0, 0.0),
    }

    def __init__(self, robot):
        self.robot = robot

    def execInstruction(self, instruction):
        #instruction = json.loads(instruction)
        #itype, idetails = instruction['type'], instruction['details']
        itype = instruction

        power = self.INSTRUCTION_TO_POWER.get(itype, None)
        if power is None:
            return False

        self.robot.setPower(power[0], power[1])
        return True
