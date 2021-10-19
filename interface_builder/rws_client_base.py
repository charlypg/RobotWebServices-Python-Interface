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

from http_client import HTTPClient

class RWSClient:
    """Implements a simple interface for a user who aims to build his/her 
    own application.
    
    It contains documented methods, each having a name corresponding to what it does."""
    
    def __init__(self, rws_server_address, username="Default User", password="robotics"):
        self.client = HTTPClient(rws_server_address, username, password)
        
    def __del__(self):
        self.client.close_session()
        return None
    
    def __str__(self):
        string = "RWS Interface\n\n"
        string += self.client.__str__()
        return string
    
    def __repr__(self):
        string = "RWS Interface\n\n"
        string += self.client.__repr__()
        return string

    def close_http_session(self):
        self.client.close_session()

    def subscribe_on_resources(self, data_resources):

        """Subscribe on resources
        """

        params = None
        data = data_resources

        return self.client.request('subscribe_on_resources', params_from_interface=params, data=data)

