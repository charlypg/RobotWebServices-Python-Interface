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

import json
import os

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

def score_to_underscore(string):
    new_string = str()
    for caract in string:
        if caract == '-':
            new_string += '_'
        else:
            new_string += caract
    return new_string


SPACE = ' '
TAB_BASE = 4

BASE = {'subscribe_on_resources'}


def build_url_complement_def(python_code, keyword, info, first_line_length):
    for arg, arg_info in zip(info.get('expected_url_complement').keys(), info.get('expected_url_complement').values()):
        python_code += ',\n' + first_line_length*SPACE + score_to_underscore(arg)
    return python_code

def build_param_def(python_code, keyword, info, first_line_length):
    for arg, arg_info in zip(info.get('expected_url_params').keys(), info.get('expected_url_params').values()):
        python_code += ',\n' + first_line_length*SPACE + score_to_underscore(arg) + '='
        if type(arg_info.get('default_value')) == str:
            python_code += '\'' + arg_info.get('default_value') + '\''
        else:
            python_code += str(arg_info.get('default_value')) 
    return python_code
            
def build_data_def(python_code, keyword, info, first_line_length): 
    for arg, arg_info in zip(info.get('expected_data_params').keys(), info.get('expected_data_params').values()):
        python_code += ',\n' + first_line_length*SPACE + score_to_underscore(arg) + '='
        if type(arg_info.get('default_value')) == str:
            python_code += '\'' + arg_info.get('default_value') + '\''
        else:
            python_code += str(arg_info.get('default_value'))
    return python_code

def build_method_def(python_code, keyword, info):
    
    """Builds the definition of the method corresponding to the keyword"""
    
    first_line = TAB_BASE*SPACE + 'def' + SPACE + keyword 
    first_line_length = len(first_line)+1
    python_code += first_line + '(self'
    
    python_code = build_url_complement_def(python_code, keyword, info, first_line_length)
    python_code = build_param_def(python_code, keyword, info, first_line_length)
    python_code = build_data_def(python_code, keyword, info, first_line_length)
    
    python_code += '):\n\n'
    
    return python_code

def build_url_complement_comments(python_code, keyword, info):
    """Builds comments for url complement"""
    for arg, arg_info in zip(info.get('expected_url_complement').keys(), info.get('expected_url_complement').values()):
        python_code += '\n' + 2*TAB_BASE*SPACE + ':param ' + score_to_underscore(arg) + ': ' 
        python_code += str(arg_info.get('description')) + ' ' + str(arg_info.get('possible_values'))
    return python_code

def build_params_comments(python_code, keyword, info):
    """Builds comments for parameters"""
    for arg, arg_info in zip(info.get('expected_url_params').keys(), info.get('expected_url_params').values()):
        python_code += '\n' + 2*TAB_BASE*SPACE + ':param ' + score_to_underscore(arg) + ': ' 
        python_code += str(arg_info.get('description')) + ' ' + str(arg_info.get('possible_values'))
    return python_code

def build_data_comments(python_code, keyword, info):
    """Builds comments for data"""
    for arg, arg_info in zip(info.get('expected_data_params').keys(), info.get('expected_data_params').values()):
        python_code += '\n' + 2*TAB_BASE*SPACE + ':param ' + score_to_underscore(arg) + ': ' 
        python_code += str(arg_info.get('description')) + ' ' + str(arg_info.get('possible_values'))
    return python_code

def build_method_comments(python_code, keyword, info):

    """Builds comments"""
    
    # Comments
    python_code += 2*TAB_BASE*SPACE + '\"\"\"' + info.get('description')
    
    # ajouter les com :param : et :return :
    if info.get('expected_url_params') != dict() or info.get('expected_data_params') != dict() or info.get('expected_url_complement'):
        python_code += '\n'

    python_code = build_url_complement_comments(python_code, keyword, info)
    python_code = build_params_comments(python_code, keyword, info)
    python_code = build_data_comments(python_code, keyword, info)
    
    python_code += '\n' + 2*TAB_BASE*SPACE + '\"\"\"'
    
    return python_code

def build_method_url_complement(python_code, keyword, info):
    
    """Builds the string in order to complement the url"""
    
    python_code += 2*TAB_BASE*SPACE + 'url_complement = '
    
    nb_data = len(info.get('expected_url_complement'))
    if nb_data == 0:
        python_code += 'None\n'
    else:
        python_code += '\''
        compteur = 0
        for arg in info.get('expected_url_complement').keys():
            python_code += '/{' + str(compteur) + '}'
            compteur += 1
        python_code += '\'.format('
        compteur = 0
        for arg in info.get('expected_url_complement').keys():
            compteur += 1
            python_code += score_to_underscore(arg)
            if compteur < nb_data:
                python_code += ','
            else:
                python_code += ')\n'
    
    return python_code
    

def build_method_params(python_code, keyword, info):
    
    """Builds params dictionary"""
    
    python_code += 2*TAB_BASE*SPACE + 'params = '
    
    nb_data = len(info.get('expected_url_params'))
    if nb_data == 0:
        python_code += 'None\n'
    else:
        compteur = 0
        python_code += '{'
        for arg in info.get('expected_url_params').keys():
            compteur += 1
            python_code += '\'' + arg + '\'' + ' : ' + score_to_underscore(arg)
            if compteur < nb_data:
                python_code += ','
            else:
                python_code += '}\n'
    return python_code
            
def build_method_data(python_code, keyword, info):
    
    """Builds data dictionary"""

    python_code += 2*TAB_BASE*SPACE + 'data = '
    
    nb_data = len(info.get('expected_data_params'))
    if nb_data == 0:
        python_code += 'None\n'
    else:
        compteur = 0
        python_code += '{'
        for arg in info.get('expected_data_params').keys():
            compteur += 1
            python_code += '\'' + arg + '\'' + ' : ' + score_to_underscore(arg)
            if compteur < nb_data:
                python_code += ','
            else:
                python_code += '}'
    return python_code

def build_http_arg(python_code, keyword, info):
    python_code += '\n\n'
    python_code = build_method_url_complement(python_code, keyword, info)
    python_code = build_method_params(python_code, keyword, info)
    python_code = build_method_data(python_code, keyword, info)
    return python_code

def build_method_return(python_code, keyword, info):
    """Builds return"""
    python_code += '\n' + 2*TAB_BASE*SPACE + 'return self.client.request(\'' + keyword + '\', params_from_interface=params, data=data, url_complement=url_complement)\n\n'
    return python_code


LECTURE = '../RequestsDictionary.json'
FUNCTION_DICT = extract_json(LECTURE)

base = open('rws_client_base.py', 'r')
python_code = base.read()
base.close()

for keyword, info in zip(FUNCTION_DICT.keys(), FUNCTION_DICT.values()):
    if keyword in BASE:
        pass
    else:
        python_code = build_method_def(python_code, keyword, info)
        python_code = build_method_comments(python_code, keyword, info)
        python_code = build_http_arg(python_code, keyword, info)
        python_code = build_method_return(python_code, keyword, info)
    

FILENAME = '../rws_client.py'
print("Write in : {}".format(FILENAME))
fichier = open(FILENAME, 'w')
fichier.write(python_code)
fichier.close()
