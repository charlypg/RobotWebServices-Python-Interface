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

    def get_service_list(self):

        """Returns the services list
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_service_list', params_from_interface=params, data=data, url_complement=url_complement)

    def logout(self):

        """Performs logging out
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('logout', params_from_interface=params, data=data, url_complement=url_complement)

    def get_rapid_variable_data(self,
                                task,
                                module,
                                variable):

        """Returns RAPID variable state

        :param task: RAPID task wherin the variable is defined []
        :param module: RAPID module wherin the variable is defined []
        :param variable: Name of the RAPID variable []
        """

        url_complement = '/{0}/{1}/{2}'.format(task,module,variable)
        params = None
        data = None

        return self.client.request('get_rapid_variable_data', params_from_interface=params, data=data, url_complement=url_complement)

    def update_rapid_variable_current_value(self,
                                            task,
                                            module,
                                            variable,
                                            value='true'):

        """Update the current value of a RAPID variable

        :param task: RAPID task wherin the variable is defined []
        :param module: RAPID module wherin the variable is defined []
        :param variable: Name of the RAPID variable []
        :param value: Value to be written ['boolean', 'num', 'string']
        """

        url_complement = '/{0}/{1}/{2}'.format(task,module,variable)
        params = None
        data = {'value' : value}
        return self.client.request('update_rapid_variable_current_value', params_from_interface=params, data=data, url_complement=url_complement)

    def get_subscription_actions(self):

        """Returns possible actions with the subscription service
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_subscription_actions', params_from_interface=params, data=data, url_complement=url_complement)

    def get_user_resources(self,
                           user_type='None'):

        """Returns user ressources

        :param user_type: Type of user ['self', 'None']
        """

        url_complement = None
        params = {'user-type' : user_type}
        data = None

        return self.client.request('get_user_resources', params_from_interface=params, data=data, url_complement=url_complement)

    def get_user_actions(self):

        """user actions
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_user_actions', params_from_interface=params, data=data, url_complement=url_complement)

    def get_controller_resources(self):

        """Returns controller resources
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_controller_resources', params_from_interface=params, data=data, url_complement=url_complement)

    def get_controller_actions(self):

        """Returns actions available on controller resources
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_controller_actions', params_from_interface=params, data=data, url_complement=url_complement)

    def get_file_service_resources(self):

        """Returns file service resources
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_file_service_resources', params_from_interface=params, data=data, url_complement=url_complement)

    def get_robotware_services(self):

        """Returns robotware services
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_robotware_services', params_from_interface=params, data=data, url_complement=url_complement)

    def get_rapid_system_resources(self):

        """Returns RAPID resources
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_rapid_system_resources', params_from_interface=params, data=data, url_complement=url_complement)

    def get_rapid_execution_state(self,
                                  continue_on_err='None'):

        """Returns RAPID execution state

        :param continue_on_err: Continue on error ['1', '0', 'None']
        """

        url_complement = None
        params = {'continue-on-err' : continue_on_err}
        data = None

        return self.client.request('get_rapid_execution_state', params_from_interface=params, data=data, url_complement=url_complement)

    def get_rapid_execution_actions(self):

        """Returns available actions on RAPID execution
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('get_rapid_execution_actions', params_from_interface=params, data=data, url_complement=url_complement)

    def start_rapid_execution(self,
                              regain='continue',
                              execmode='continue',
                              cycle='once',
                              condition='none',
                              stopatbp='disabled',
                              alltaskbytsp='false'):

        """Starts a RAPID execution. The robot has to be in 'Auto' mode.

        :param regain: Regain ['continue', 'regain', 'clear']
        :param execmode: Execution mode ['continue', 'stepin', 'stepover', 'stepout', 'stepback', 'steplast', 'stepmotion']
        :param cycle: Cycle ['forever', 'asis', 'once']
        :param condition: Condition ['none', 'callchain']
        :param stopatbp: Stop execution at breakpoint ['disabled', 'enabled']
        :param alltaskbytsp: alltaskbytsp ['true', 'false']
        """

        url_complement = None
        params = None
        data = {'regain' : regain,'execmode' : execmode,'cycle' : cycle,'condition' : condition,'stopatbp' : stopatbp,'alltaskbytsp' : alltaskbytsp}
        return self.client.request('start_rapid_execution', params_from_interface=params, data=data, url_complement=url_complement)

    def stop_rapid_execution(self,
                             stopmode='stop',
                             usetsp='normal'):

        """Stops a RAPID execution. The robot has to be in 'Auto' mode.

        :param stopmode: Stop mode ['cycle', 'instr', 'stop', 'qstop']
        :param usetsp: Use tsp ['normal', 'alltsk']
        """

        url_complement = None
        params = None
        data = {'stopmode' : stopmode,'usetsp' : usetsp}
        return self.client.request('stop_rapid_execution', params_from_interface=params, data=data, url_complement=url_complement)

    def start_rapid_execution_from_prod_entry(self):

        """Starts a RAPID execution from a production entry
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('start_rapid_execution_from_prod_entry', params_from_interface=params, data=data, url_complement=url_complement)

    def reset_rapid_program_pointer_to_main(self):

        """Resets the program pointer (RAPID) to main procedure (PROC main). The robot has to be in 'Auto' mode.
        """

        url_complement = None
        params = None
        data = None

        return self.client.request('reset_rapid_program_pointer_to_main', params_from_interface=params, data=data, url_complement=url_complement)

