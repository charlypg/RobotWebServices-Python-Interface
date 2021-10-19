#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2021 Charly PECQUEUX--GUÉZÉNEC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
from rws_client_thread import RWSClientThread

class RWSClientThreadCustom(RWSClientThread):
    
    def run(self):
        """Subscribes to the panel control state resource (motor off/on, guardstop, etc)
        and retrieves regularly the current state of the resource. 
        """
        
        payload = {'resources':['1'],
            '1':'/rw/panel/ctrlstate',
            '1-p':'1'}
        
        """
        payload = {'resources':['1', '2'],
            '1':'/rw/panel/ctrlstate',
            '1-p':'1',
            '2':'/rw/panel/opmode',
            '2-p':'1'}
        """
        
        self.start_listening(payload)
        
        for i in range(30):
            print(i)
            print(self.get_data_listening())
            print('\n\n')
            time.sleep(1)
            
        self.stop_listening()
        
        self.logout()
        self.close_http_session()


if __name__ == "__main__":
    ROBOT_IP_ADDR = '192.168.125.1'
    client = RWSClientThreadCustom(ROBOT_IP_ADDR)
    client.start()
    client.join()
