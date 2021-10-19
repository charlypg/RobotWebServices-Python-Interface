# RobotWebServices-Python-Interface

RobotWebServices-Python-Interface is a Python library which implements a Robot Web Services (RWS) client for ABB Robots in Python. 

## Installation 

To get the library, just clone the repository : 

`git clone https://github.com/charlypg/RobotWebServices-Python-Interface.git`

## Description

The library provides an interface which allows the user to communicate with an ABB Robot thanks to Robot Web Services (RWS). 

Essentially, it allows to : 

- Communicate with a robot in HTTP 
- Follow the evolution of resource

The library facilitates the use of RWS. The user has not to manage directly HTTP requests and responses, or sockets. The user only needs to know the action and the data he wants to send to the robot. 

In order to communicate using only HTTP, an instance of the class *RWSClient* (*rws_client* file) can be used.

To follow a resource and also communicate in HTTP, an instance of the class *RWSClientThread* (*rws_client_thread* file) can be used.

### Warnings

This library has only been tested on the robot YuMi (IRB14000) and for RWS version 1.0

Also, the the documentation contains a few bugs that need to be fixed. 

## Licence

Copyright (c) 2021 Charly PECQUEUX--GUÉZÉNEC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
