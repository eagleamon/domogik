#!/usr/bin/python
# -*- coding: utf-8 -*

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Module purpose
==============

Helper to send xPL messages

Implements
==========

- xPLSendHelper
- AbstractSendHelper
- X10SendHelper

@author: Maxence Dunnewind <maxence@dunnewind.net>
@author:Frédéric Mantegazza <frederic.mantegazza@gbiloba.org>
@copyright: (C) 2007-2009 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import re

from domogik.xpl.lib.xplconnector import Manager
from domogik.common.configloader import Loader


class xPLSendHelper(xPLModule):
    """ Helper to send basic xPL messages.
    """
    def __init__(self):
        """ Init helper.
        """
        xPLModule.__init__(self, name="xplsendhelper")
        self.__xpl_manager = Manager()
        self._log = self.get_my_logger()
        self.x10 = X10SendHelper(self.__xpl_manager)

    def __del__(self):
        self.__xpl_manager.force_leave()


class AbstractSendHelper(object):
    """ Abstract class for send helpers.

    @ivar _xpl: xpl manager
    @itype _xpl: L{Manager}
    """
    def __init__(self, xpl_manager):
        """ Init X10 object.

        @param xpl_manager: xpl manager
        @type xpl_manager:: L{Manager}
        """
        super(AbstractSendHelper, self).__init__()
        self._xpl_manager = xpl_manager
        self._schema = None

        self._init()

    def _init(self):
        """ Additional init.
        """
        raise NotImplemntedError("BaseSendHelper._init() must be overloaded")

    def _check_house_name(self, house):
        """ Checks house name.

        @param device: the house name
        @type device: str

        @raise ValueError: the house name is not valid
        """
        if not re.match(r'^[a-pA-P]$', house):
            raise ValueError("Invalid house name (%s)" % house)

    def _check_device_name(self, device):
        """ Checks device name.

        @param device: the device name
        @type device: str

        @raise ValueError: the device name is not valid
        """
        if not re.match(r'^[a-pA-P][0-9]$', device):
            raise ValueError("Invalid device name (%s)" % device)

    def _check_level(self, level):
        """ Checks level.

        @param level: the level
        @type level: str

        @raise ValueError: the level is not valid
        """
        if not re.match(r'^[0-9]$', level):
            raise ValueError("Invalid level (%s)" % level)

    def _create_message(self, **kwargs):
        """ Create an empty xpl message.

        @return: xpl message
        @rtype: L{Message}
        """
        message = Message()
        mess.set_type('xpl-cmnd')
        mess.set_schema(self._schema)
        for key, value in kwargs.iteritems():
            mess.set_data_key(key, value)

    def _send_message(self, message):
        """ Send the message on teh xpl bus.

        @param message: xpl message
        @type message: L{Message}
        """
        self._xpl_manager.send(message)


class X10SendHelper(AbstractSendHelper):
    """ X10 helper.
    """
    def _init(self):
        self._schema = "x10.basic"

    def on_device(self, device):
        """ Send a message with command 'on' for device.

        @param device: the device to turn on
        @type device: str
        """
        self._check_device_name(device)
        message = self._create_message(device=device, command="on")
        self._send_message(message)

    def off_device(self, device):
        """ Send a message with command "off" for device.

        @param device: the device to turn off
        @type device: str
        """
        self._check_device_name(device)
        message = self._create_message(device=device, command="off'")
        self._send_message(message)

    def on_house(self, house):
        """ Send a message with command "on" for all devices.

        @param house: the house to turn on
        @type house: str
        """
        self._check_house_name(house)
        message = self._create_message(house=house, command="all_devices_on")
        self._send_message(message)

    def off_house(self, house):
        """ Send a message with command "all_devices_off" for house.

        @param house: the house to turn off
        @type house: str
        """
        self._check_house_name(house)
        message = self._create_message(house=house, command="all_devices_off")
        self._send_message(message)

    def on_lights(self, house):
        """ Send a message with command "all_lights_on" for house.

        @param house: the house to light on
        @type house: str
        """
        self._check_house_name(house)
        message = self._create_message(device=house, command="all_lights_on")
        self._send_message(message)

    def off_lights(self, house):
        """ Send a message with command "all_lights_off' for house.

        @param house: the house to light off
        @type house: str
        """
        self._check_house_name(house)
        message = self._create_message(house=house, command="all_lights_off")
        self._send_message(message)

    def bright(self, device, level):
        """ Set a message with command "bright" for device.

        @param device: the device to bright
        @type device: str

        @param level: level to use for brightness (%)
        @type level: str
        """
        self._check_device_name(device)
        self._check_level(level)
        message = self._create_message(device=device, command="bright", level=level)
        self._send_message(message)

    def dim(self, device, level):
        """ Set a message with command "dim" for device.

        @param device: the device to dim
        @type device: str

        @param level: level to use for brightness (%)
        @type level: str
        """
        self._check_device_name(device)
        self._check_level(level)
        message = self._create_message(device=device, command="dim", level=level)
        self._send_message(message)

    def brightb(self, device, level):
        """ Set a message with command "brightb" for device.

        @param device: the device to bright
        @type device: str

        @param level: level to use for brightness (%)
        @type level: str
        """
        self._check_device_name(device)
        self._check_level(level)
        message = self._create_message(device=device, command="brightb", level=level)
        self._send_message(message)

    def dimb(self, device, level):
        """ Set a message with command "dimb" for device.

        @param device: the device to dim
        @type device: str

        @param level: level to use for brightness (%)
        @type level: str
        """
        self._check_device_name(device)
        self._check_level(level)
        message = self._create_message(device=device, command="dimb", level=level)
        self._send_message(message)


class PlcBusSendHelper(AbstractSendHelper):
    """ PLC bus helper.
    """
    def _init(self):
        self._schema = "control.basic"

    def __getattr__(self, name):
        """ Wrapper for all PLC bus function calls.
        """
        if name.upper() in ('ALL_UNITS_OFF',
                            'ALL_LIGHTS_ON',
                            'ON',
                            'OFF',
                            'DIM',
                            'BRIGHT',
                            'ALL_LIGHTS_OFF',
                            'ALL_USER_LTS_ON',
                            'ALL_USER_UNIT_OFF',
                            'ALL_USER_LIGHT_OFF',
                            'BLINK',
                            'FADE_STOP',
                            'PRESET_DIM',
                            'STATUS_OFF',
                            'STATUS_REQUEST',
                            'REC_MASTER_ADD_SETUP',
                            'TRA_MASTER_ADD_SETUP',
                            'SCENE_ADR_SETUP',
                            'SCENE_ADR_ERASE',
                            'ALL_SCENES_ADD_ERASE',
                            'GET_SIGNAL_STRENGTH',
                            'GET_NOISE_STRENGTH',
                            'REPORT_SIGNAL_STREN',
                            'REPORT_NOISE_STREN',
                            'GET_ALL_ID_PULSE',
                            #'GET_ALL_ON_ID_PULSE',
                            'REPORT_ALL_ID_PULSE',
                            'REPORT_ONLY_ON_PULSE',
                            ):
            return lambda *args, **kwargs: self._function_wrapper(name, *args, **kwargs)
        else:
            #return super(PlcBusSendHelper, self).__getattr__(name)
            raise AttributeError("PlcBusSendHelper instance has no attribute %s" % name)

    def _function_wrapper(self, command, device, user_code, level, rate):
        """ Wrapper for all PLC bus commands except "GET_ALL_ON_ID_PULSE".

        @param command: name of the command
        @ptype command: str

        @param device: name of the device
        @type device: str

        @param user_code: the user code
        @type user_code: str

        @param level: the level
        @type level: str

        @param rate: the rate
        @type rate: str
       """
        self._check_device_name(device)
        #self._check_user_code(user)
        self._check_level(user)
        #self._check_rate(user)
        message = self._create_message(device=device, command=command, user_code=user_code,level=level, rate=rate)
        self._send_message(message)

    def get_all_on_id_pulse(self, device, user_code):
        """ Send a message with command "GET_ALL_ON_ID_PULSE" for device/user.

        @param device: the device
        @type device: str

        @param user_code: the user code
        @type user_code: str
        """
        self._check_device_name(device)
        #self._check_user_code(user)
        message = self._create_message(device=device, command="GET_ALL_ON_ID_PULSE", user_code=user_code)
        self._send_message(message)
