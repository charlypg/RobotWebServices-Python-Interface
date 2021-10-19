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

import threading
from rws_client import RWSClient
from listener import Listener

class RWSClientThread(RWSClient, threading.Thread):
    
    """Implements a thread which allows to follow the evolution of resources thanks to
    subsciptions while keeping the basic functionnalities of the RWS client class
    (RWSClient)."""
    
    def __init__(self, rws_server_address, username="Default User", password="robotics"):
        RWSClient.__init__(self, 
                           rws_server_address=rws_server_address, 
                           username=username, 
                           password=password)
        threading.Thread.__init__(self)
        self.listener = None
    
    def __del__(self):
        if self.listener is not None:
            del self.listener
    
    def start(self):
        """Starts the thread : RWSClientThread is a subclass of threading.Thread."""
        return threading.Thread.start(self)
    
    def start_listening(self, resources_dict):
        """Subscribe to the data specified in 'resources_dict' before launching an
        internal 'listener' which allows the user to follow the data evolution
        through the 'get_data_listening' method. 
        
        :param resources_dict: dict : Contains information on resources (to detail) 
        """
        
        resp = RWSClient.subscribe_on_resources(self, resources_dict)
        if resp.status_code == 201:
            location = resp.headers['Location']
            cookie = '-http-session-={0}; ABBCX={1}'.format(resp.cookies['-http-session-'], resp.cookies['ABBCX'])
            header = [('Cookie',cookie)]
            self.listener = Listener(location=location, headers=header)
            self.listener.start()
        else:
            print("Error request : {}".format(resp.status_code))
    
    def get_data_listening(self):
        """Retrieves data from the listener."""
        return self.listener.get_data()
    
    def stop_listening(self):
        """Stops the listener."""
        if self.listener is not None:
            self.listener.stop_listening()
            self.listener.join()
            self.listener = None
    
    def run(self):
        """Should be implemented by the user in a subclass."""
        pass
