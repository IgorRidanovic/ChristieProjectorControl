#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Christie projector TruLife+ command class for TCP/IP API for Christie Eclipse,
M RGB Series, and Griffyn Series projectors. Refer to "Christie TruLife+ Serial
Commands" Technical Reference 020-103316-08 documentation.

The class provides a high level interface to the API. Only some commands are
implemented at this time.

Igor Ridanovic, igor(at)hdhead.com
'''

import socket

class ChristieProjector():

    def __init__(self, ip):
        self.projectorIP    = ip
        self.port           = 3002
        self.responseLength = 48


    def _open(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.projectorIP, self.port))
        self.s.settimeout(1)


    def _close(self):
        self.s.close()


    def interactiveLoop(self):
        print("Interactive loop mode, Press CTRL+C to break. Type projector commands.")

        self._open()

        while True:
            m = input()

            if m == 'exit' or m == 'EXIT':
                self._close()
                break

            self.s.send(m.encode('utf-8'))

            try:
            	response = self.s.recv(self.responseLength)
            	print('Projector:', response.decode('utf-8'))
            except socket.timeout:
                pass

        self._close()


    def _communicate(self, message, rLength=48):

        self._open()

        try:
            self.s.send(message.encode('utf-8'))
            response = self.s.recv(rLength)
            self._close()
            return str(response.decode('utf-8'))

        except socket.timeout:
            self._close()
            return 'Projector is not responding'


    def getStatus(self):
        return(self._communicate('(SST?)'))


    def getPowerState(self):
        '''Returns True when the power is on, False when the power is off'''

        r = self._communicate('(PWR?)')

        if '"on"' in r.lower():
            return True

        if 'standby' in r.lower():
            return False

        return(None)


    def setPowerState(self, state):
        '''True powers up the projector. False powers it off. No response is returned.'''
        if state == True:
            p = '1'
        elif state == False:
            p = '0'
        else:
            raise TypeError('setPowerState() requires a Boolean argument')

        cmdString = '(PWR <s>)'.replace('<s>', p)
        r = self._communicate(cmdString)

        return self.getPowerState()


    def getShutterState(self):
        '''Returns True when the shutter is closed, False when it's open'''

        r = self._communicate('(SHU?)')

        if 'closed' in r.lower():
            return True

        if 'open' in r.lower():
            return False

        return(None)


    def setShutterState(self, state):
        '''Set the arg to True to close the shutter, False to open'''

        # (SHU 1) is closed.
        if state == True:
            p = '1'
        elif state == False:
            p = '0'
        else:
            raise TypeError('setShutterState() requires a Boolean argument')

        # Shutter open/close returns no message
        responseLength = 0
        cmdString = '(SHU <s>)'.replace('<s>', p)
        return(self._communicate(cmdString, responseLength))



if __name__ == '__main__':

    # Usage example.

    # Make a projector instance.
    projectorIP = '192.168.1.128'
    projector   = ChristieProjector(projectorIP)

    # Use interactiveLoop() to type and send command to the projector, i.e. '(SHU?)'
    # returns the state of the shutter.
    # projector.interactiveLoop()

    # Power up.
    # state = projector.setPowerState(True)

    # Power down.
    # state = projector.setShutterState(False)

    # Get shutter state.
    # state = projector.getShutterState()

    # Get power state.
    # state = projector.getPowerState()

    # print(state)
