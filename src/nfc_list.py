"""
    Websocket interface to a NFC reader.
    Copyright (C) 2014 Lennart Buit, Jelte Zeilstra

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
"""

import threading
import nfc

from time import sleep

from __init__ import debug

class NFCReader(threading.Thread):
    def __init__(self, context, pnd, callback):
        threading.Thread.__init__(self)
        self.context = context
        self.pnd = pnd
        self.callback = callback
        self.running = True

    def run(self):
        if debug:
            print("started thread")

        nms = []

        nm = nfc.modulation()
        nm.nmt = nfc.NMT_ISO14443A
        nm.nbr = nfc.NBR_106

        nms.append(nm)

        while self.running:
            sleep(0.1) # Python doesn't have a yield function, this is to make sure that other threads also have time to serve requests
            target = nfc.target()
            status = nfc.initiator_poll_target(self.pnd, nm, 1, 0x01, 0x02, target)

            if status > 0:
                uid = ":".join(["{:0>2x}".format(target.nti.nai.abtUid[i]) for i in range(target.nti.nai.szUidLen)])
                atqa = ":".join(["{:0>2x}".format(target.nti.nai.abtAtqa[i]) for i in range(2)])
                sak = "{:0>2x}".format(target.nti.nai.btSak)
                
                if debug:
                    print(uid, atqa, sak)
                
                self.callback(uid, atqa, sak)

def init_reader(callback):
    context = nfc.init()

    devs =  nfc.list_devices(context, 16)

    if devs:
        for dev in devs:
            pnd = nfc.open(context, dev)

            if pnd:
                if nfc.initiator_init(pnd) < 0:
                    nfc.perror(pnd, "nfc_initator_init")
                    nfc.close(pnd)
                else:
                    reader = NFCReader(context, pnd, callback)
                    reader.daemon = True
                    reader.start()
                
    else:
        print("failed to find a NFC device")

if __name__ == "__main__":
    init_reader()

    while True:
        sleep(10)

