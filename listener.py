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
from robot_web_socket_client import RobotWebSocketClient

class Listener(threading.Thread):
    
    def __init__(self, location, headers):
        threading.Thread.__init__(self)
        self.listening = True
        self.data = None
        self.data_lock = threading.Lock()
        self.robot_socket = RobotWebSocketClient(location, headers)
    
    def __del__(self):
        del self.robot_socket
    
    def stop_listening(self):
        self.listening = False
    
    def update_data(self):
        buffer_empty = False
        try: 
            self.data_lock.acquire()
            self.data = self.robot_socket.buffer.popleft()
            #self.data_lock.release()
        except:
            buffer_empty = True
            pass
        self.data_lock.release()
        return buffer_empty
    
    def get_data(self):
        self.data_lock.acquire()
        data = self.data
        self.data_lock.release()
        return data
    
    def run(self):
        self.robot_socket.connect()
        while self.listening:
            self.update_data()
