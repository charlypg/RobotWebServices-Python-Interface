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

import json
import os
import time
from requests.auth import HTTPDigestAuth
from requests import Session

def extract_json(filename):
    """Extracts info from a json file under the form of a dictionary.
    It is used to declare HTTPClient's static variables
    
    :param filename: str : Name of the json file (or path)
    :return: dict : Image dictionary of the json file"""
    this_directory = os.path.dirname(__file__)
    file = open(os.path.join(this_directory, filename), 'r')
    string = file.read()
    file.close()
    return json.loads(string)

class HTTPClient:
    
    """The HTTPClient class implements an HTTP client for RWS. It builds requests 
    from raw data. """
    
    HTTP_STATUS_CODES = extract_json("HTTP_Status_Codes.json")
    REQUESTS_DICTIONARY = extract_json("RequestsDictionary.json")
    DEBUG = False
    
    def __init__(self, rws_server_address, username="Default User", password="robotics"):
        
        # ip address or domain name of the robot controller
        self.rws_server_address = rws_server_address
        
        # url of the robot controller
        self.rws_server_url = "http://" + rws_server_address
        
        # username and password for the session
        self.username = username
        self.password = password
        
        # session : Digest Authentification (Cf RWS documentation)
        self.session = Session()
        self.session.auth = HTTPDigestAuth(self.username, self.password)
    
    def __del__(self):
        return None
    
    def __str__(self):
        string = "HTTP Client\n"
        string += "username : {}\n".format(self.username)
        string += "RWS server address : {}".format(self.rws_server_address)
        return string
    
    def __repr__(self):
        string = "HTTP Client\n"
        string += "username : {}\n".format(self.username)
        string += "RWS server address : {}".format(self.rws_server_address)
        return string
    
    def get_rws_server_url(self):
        """Getter : rws_server_url
        
        :return: str : Returns the RWS Server url.
        """
        return self.rws_server_url
    
    def close_session(self):
        """Closes the HTTP session"""
        self.session.close()
    
    @staticmethod
    def dict_fusion(receiver_dict, other_dict):
        """Performs the fusion of both dictionaries in argument. If there exists a common key, then
        the receiver dictionary takes the value from the other with this particular key.
        
        It does not return the reference of the receiver dictionary ! 
        
        :param receiver_dict: dict : Reference to the receiver dictionary
        :param other_dict: dict : Reference to the other dictionary
        :return: Nothing
        """
        if other_dict is not None:
            for (key, value) in zip(other_dict.keys(), other_dict.values()):
                receiver_dict[key] = value
    
    @staticmethod
    def dict_fusion_return_ref(receiver_dict, other_dict):
        """Performs the fusion of both dictionaries in argument. If there exists a common key, then
        the receiver dictionary takes the value from the other with this particular key.
        
        This one returns the reference of the receiver dictionary, contrary to 'dict_fusion'
        
        :param receiver_dict: dict : Reference to the receiver dictionary
        :param other_dict: dict : Reference to the other dictionary
        :return: dict : Reference to the receiver dictionary
        """
        if other_dict is not None:
            for (key, value) in zip(other_dict.keys(), other_dict.values()):
                receiver_dict[key] = value
        
        return receiver_dict
    
    def request(self, keyword, params_from_interface=None, data=None, url_complement=None):
        
        """
        Builds an HTTP request from raw data. 
        
        The keyword corresponds to the desired action, as mentionned above. 
        ex: 'start_rapid_execution' in order to start the execution of a 
        program on the robot.
        
        Some URL parameters are undirectly given by the user, from the interface, 
        under the form of a dictionary : params_from_interface. 
        
        Data can also be sent if necessary. Like parameters, data are given thanks 
        to the 'data' dictionary in argument.
        
        :param keyword: str : Keyword corresponding to a particular action
        :param params_from_interface: dict : URL parameters 
        :param data: dict : Data which will be sent
        
        :return: Response : The request's response. 
        """
        
        # dictionary corresponding to the called service
        # its gives data enabling to build the request
        service_dictionary = HTTPClient.REQUESTS_DICTIONARY.get(keyword)
        
        if HTTPClient.DEBUG:
            print("service_dictionary : {}".format(service_dictionary))
        
        # service_dictionary.get('url') : location of the resource 
        # in the RWS tree-like structure
        url = self.rws_server_url + service_dictionary.get('url')
        if url_complement is not None:
            url += url_complement
        
        if HTTPClient.DEBUG:
            print("url : {}".format(url))
        
        # parameters by default are completed or replaced by the parameters in argument
        params = service_dictionary.get('default_params')
        HTTPClient.dict_fusion(params, params_from_interface)
        
        if HTTPClient.DEBUG:
            print("params : {}".format(params))
            print("data : {}".format(data))
        
        # request building and returning the response
        return self.session.request(service_dictionary.get('method'), url, params=params, data=data)
    
    def test_get(self, display=True, display_content=False):
        """ Tests GET requests in order to debug the RequestsDictionary.json file
        
        :param display: bool : If True then every request's HTTP status code will be printed
        :param display_content: bool : If True then the response's content will be also printed
        :return: dict : A dictionary where keys are the keywords and values are the corresponding responses
        """
        test_dict = dict()
        keywords = HTTPClient.REQUESTS_DICTIONARY.keys()
        infos = HTTPClient.REQUESTS_DICTIONARY.values()
        
        for (keyword, info) in zip(keywords, infos):
            if info.get('method') == 'GET':
                test_dict[keyword] = self.request(keyword)
                if display:
                    print("{0} : {1}".format(keyword, test_dict[keyword].status_code))
                    if display_content:
                        print(test_dict[keyword].content)
                        print("\n\n")
                time.sleep(0.3)
                
        return test_dict
        
    
