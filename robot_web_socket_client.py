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

from collections import deque
from ws4py.client.threadedclient import WebSocketClient

class RobotWebSocketClient(WebSocketClient):

    """The RobotWebSocketClient daemon simply puts
    the received data in a deque (double ended queue).
    
    The advantage of the deque collection in python is that
    the 'append' and 'pop' operations are ATOMIC."""
    
    def __init__(self, location, headers):
        WebSocketClient.__init__(self, 
                                 location, 
                                 protocols=['robapi2_subscription'],
                                 headers=headers)
        
        self.buffer = deque()
    
    def __del__(self):
        self.close()
    
    def opened(self):
        print("Web Sockect connection established")
 
    def closed(self, code, reason=None):
        print("Closed down", code, reason)
        
    def received_message(self, event_xml):        
        if event_xml.is_text:
            self.buffer.append(str(event_xml))
        else:
            print("Received Illegal Event " + str(event_xml))
