# -*- coding: utf-8 -*-

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

Plugin purpose
==============

Library to simply manager packages's json file description

Implements
==========

PackageJson

@author: Fritz <fritz.smh@gmail.com>
@copyright: (C) 2007-2010 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from domogik.common.configloader import Loader
import traceback
import urllib2
import datetime
import json




class PackageException(Exception):
    """
    Package exception
    """

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class PackageJson():
    """ PackageJson class
        load the file into a json and complete it
    """
    def __init__(self, id = None, url = None, path = None, pkg_type = "plugin"):
        """ Read json file of a plugin and make an object from it
            @param id : name of package
            @param url : url of file
            @param path : path of file
            @param pkg_type : package type (default : 'plugin')
                          To use only with id != None
        """
        json_file = None
        try:
            # load from sources repository
            if id != None:
                # get config
                cfg = Loader('domogik')
                config = cfg.load()
                conf = dict(config[1])

                if pkg_type == "plugin":
                    if conf.has_key('package_path'):
                        json_directory = "%s/domogik_packages/plugins/" % (conf['package_path'])
                    else:
                        json_directory = "%s/%s" % (conf['src_prefix'], "share/domogik/plugins/")
                elif pkg_type == "external":
                    if conf.has_key('package_path'):
                        json_directory = "%s/domogik_packages/externals/" % (conf['package_path'])
                    else:
                        json_directory = "%s/%s" % (conf['src_prefix'], "share/domogik/externals/")
                else:
                    raise PackageException("Type '%s' doesn't exists" % pkg_type)
                json_file = "%s/%s.json" % (json_directory, id)

                self.info_file = json_file
                self.json = json.load(open(self.info_file))

                # icon file
                if conf.has_key('package_path'):
                    self.icon_file = "%s/domogik_packages/design/%s/%s/icon.png" % (conf['package_path'], pkg_type, id)
                else:
                    self.icon_file = "%s/%s/%s/%s/icon.png" % (conf['src_prefix'], "share/domogik/design/", pkg_type, id)
    
            elif path != None:
                json_file = path
                self.info_file = json_file
                self.json = json.load(open(self.info_file))
                self.icon_file = None

            elif url != None:
                json_file = url
                self.info_file = json_file
                json_data = urllib2.urlopen(json_file)
                self.json = json.load(xml_data)
                self.icon_file = None

            self.validate()

            # complete json
            self.json["identity"]["fullname"] = "%s-%s" % (self.json["identity"]["type"],
                                                           self.json["identity"]["id"])
            self.json["identity"]["info_file"] = self.info_file
            self.json["identity"]["icon_file"] = self.icon_file
            self.json["all_files"] = self.json["files"]
        except PackageException as exp:
            raise PackageException(exp.value)
        except:
            raise PackageException("Error reading json file : %s : %s" % (json_file, str(traceback.format_exc())))


    #def cache_xml(self, cache_folder, url, repo_url, priority):
    #    """ Add package url info in xml data
    #        Store xml in a file in cache_folder
    #        @param cache_folder : folder to put xml file
    #        @param url : package url
    #        @param repo_url : repository url
    #        @param priority : repository priority
    #    """
    #    top_elt = self.xml_content.documentElement
    #    new_elt = self.xml_content.createElementNS(None, 'repository')
    #    new_elt.setAttribute("package", url)
    #    new_elt.setAttribute("priority", priority)
    #    new_elt.setAttribute("source", repo_url)
    #    top_elt.appendChild(new_elt)
    #    cache_file = open("%s/%s" % (cache_folder, self.json_filename), "w") 
    #    cache_file.write(self.xml_content.toxml().encode("utf-8"))
    #    cache_file.close()

    #def set_repo_source(self, source):
    #    """ Add source info in xml data
    #        Store in xml the repository from which it comes
    #        @param source : repository url
    #    """
    #    top_elt = self.xml_content.documentElement
    #    new_elt = self.xml_content.createElementNS(None, 'repository')
    #    new_elt.setAttribute("source", source)
    #    top_elt.appendChild(new_elt)
    #    my_file = open("%s" % (self.info_file), "w") 
    #    my_file.write(self.xml_content.toxml().encode("utf-8"))
    #    my_file.close()

    def validate(self):
        if self.json["json_version"] == 2:
            self._validate_02()
        else:
            return True

    def _validate_keys(self, expected, name, lst, optional=[]):
        for exp in expected:
            if exp not in lst:
                raise PackageException("key '{0}' not found in {1}".format(exp, name))
        explst = expected + optional
        for item in lst:
            if item not in explst:
                raise PackageException("unknown key '{0}' found in {1}".format(item, name))

    def _validate_02(self):
        try:
            #check that all main keys are in the file
            expected = ["configuration", "xpl_commands", "xpl_stats", "commands", "sensors", "device_types", "identity", "files", "json_version"]
            self._validate_keys(expected, "file", self.json.keys(), ["products", "udev-rules", "external"])
            #validate the device_type
            for devtype in self.json["device_types"]:
                devt = self.json["device_types"][devtype]
                expected = ['id', 'name', 'description', 'commands', 'sensors', 'xpl_params']
                self._validate_keys(expected, "device_type {0}".format(devtype), devt.keys())
                #check that all commands exists inisde each device_type
                for cmd in devt["commands"]:
                    if cmd not in self.json["commands"].keys():    
                        raise PackageException("cmd {0} defined in device_type {1} is not found".format(cmd, devtype))
                #check that all sensors exists inside each device type
                for sens in devt["sensors"]:
                    if sens not in self.json["sensors"].keys():    
                        raise PackageException("sensor {0} defined in device_type {1} is not found".format(sens, devtype))
                #see that each xplparam inside device_type has the following keys: key, description, type
                expected = ["key", "type", "description"]
                optional = ["max_value", "min_value"]
                for par in devt["xpl_params"]:
                    self._validate_keys(expected, "a xpl_param for device_type {0}".format(devtype), par.keys(), optional)
            #validate the commands
            for cmdid in self.json["commands"]:
                cmd = self.json["commands"][cmdid]
                expected = ['name', 'return_confirmation', 'params', 'xpl_command']
                self._validate_keys(expected, "command {0}".format(cmdid), cmd.keys())
                # validate the params
                expected = ['key', 'data_type', 'conversion']
                for par in cmd['params']:
                    self._validate_keys(expected, "a param for command {0}".format(cmdid), par.keys())
                # see that the xpl_command is defined
                if cmd["xpl_command"] not in self.json["xpl_commands"].keys():
                    raise PackageException("xpl_command {0} defined in command {1} is not found".format(cmd["xpl_command"], cmdid))
            #validate the sensors
            for senid in self.json["sensors"]:
                sens = self.json["sensors"][senid]
                expected = ['name', 'data_type', 'conversion']
                self._validate_keys(expected, "sensor {0}".format(senid), sens.keys())
            #validate the xpl command
            for xcmdid in self.json["xpl_commands"]:
                xcmd = self.json["xpl_commands"][xcmdid]
                expected = ["name", "schema", "xplstat_name", "parameters"]
                self._validate_keys(expected, "xpl_command {0}".format(xcmdid), xcmd.keys())
                # parameters
                expected = ["static", "device"]
                self._validate_keys(expected, "parameters for xpl_command {0}".format(xcmdid), xcmd['parameters'].keys())
                # static parameter
                expected = ["key", "value"]
                for stat in xcmd['parameters']['static']:
                    self._validate_keys(expected, "a static parameter for xpl_command {0}".format(xcmdid), stat.keys())
                # device parameter
                expected = ["key", "description", "type"]
                for stat in xcmd['parameters']['device']:
                    self._validate_keys(expected, "a device parameter for xpl_command {0}".format(xcmdid), stat.keys())
                # see that the xpl_stat is defined
                if xcmd["xplstat_name"] not in self.json["xpl_stats"].keys():
                    raise PackageException("xplstat_name {0} defined in xpl_command {1} is not found".format(xcmd["xplstat_name"], xcmdid))
            #validate the xpl stats
            for xstatid in self.json["xpl_stats"]:
                xstat = self.json["xpl_stats"][xstatid]
                expected = ["name", "schema", "parameters"]
                self._validate_keys(expected, "xpl_command {0}".format(xstatid), xstat.keys())
                # parameters
                expected = ["static", "device", "dynamic"]
                self._validate_keys(expected, "parameters for xpl_stat {0}".format(xstatid), xstat['parameters'].keys())
                # static parameter
                expected = ["key", "value"]
                for stat in xstat['parameters']['static']:
                    self._validate_keys(expected, "a static parameter for xpl_stat {0}".format(xstatid), stat.keys())
                # device parameter
                expected = ["key", "description", "type"]
                for stat in xstat['parameters']['device']:
                    self._validate_keys(expected, "a device parameter for xpl_stat {0}".format(xstatid), stat.keys())
                # dynamic parameter
                expected = ["key", "sensor"]
                opt = ["ignore_values"]
                for stat in xstat['parameters']['dynamic']:
                    self._validate_keys(expected, "a dynamic parameter for xpl_stat {0}".format(xstatid), stat.keys(), opt)
                    # check that the sensor exists
                    if stat['sensor'] not in self.json["sensors"].keys():    
                        raise PackageException("sensor {0} defined in xpl_stat {1} is not found".format(stat['sensor'], xstatid))
        except PackageException as exp:
            raise PackageException("Error validating the json: {0}".format(exp.value))

    def set_generated(self, path):
        """ Add generation date info in json data
            @param path : path to json file
        """
        my_json = json.load(open(path))
        my_json["identity"]["generated"] = str(datetime.datetime.now())
        my_file = open(path, "w")
        my_file.write(json.dumps(my_json))
        my_file.close()

    def display(self):
        """ Display xml data in a fine way
        """
        print("---- Package informations -------------------------------")
        print("Type                : %s" % self.json["identity"]["type"])
        print("Id                  : %s" % self.json["identity"]["id"])
        print("Full name           : %s" % self.json["identity"]["fullname"])
        print("Version             : %s" % self.json["identity"]["version"])
        print("Category            : %s" % self.json["identity"]["category"])
        print("Link for doc        : %s" % self.json["identity"]["documentation"])
        print("Description         : %s" % self.json["identity"]["description"])
        print("Changelog           : %s" % self.json["identity"]["changelog"])
        print("Author              : %s" % self.json["identity"]["author"])
        print("Author's email      : %s" % self.json["identity"]["author_email"])
        print("Domogik min version : %s" % self.json["identity"]["domogik_min_version"])
        print("----- Package files -------------------------------------")
        for my_file in self.json["files"]:
            print("- %s" % my_file)
        print("---------------------------------------------------------")

    def find_xplstats_for_device_type(self, devtype):
        if self.json["json_version"] != 2:
            return "Bad json version for the plugin"
        ret = {}
        # loop over all xplstat params and see if the sensor is linked to the above list
        for xstatid in self.json["xpl_stats"]:
            xstat = self.json["xpl_stats"][xstatid]
            for stat in xstat['parameters']['dynamic']:
                if stat['sensor'] in self.json["device_types"][devtype]['sensors']:
                    if stat['sensor'] not in ret:
                        ret[stat['sensor']] = []
                    ret[stat['sensor']].append( xstatid )
                        
        return ret


def set_nightly_version(path):
    """ update version for the nightly build
        @param path : path to json file
    """
    my_json = json.load(open(path))
    # suffix the version with .devYYYYMMDD
    suffix = ".dev%s" % datetime.datetime.now().strftime('%Y%m%d')
    my_json["identity"]["version"] += suffix
    my_file = open(path, "w")
    my_file.write(json.dumps(my_json))
    my_file.close()

if __name__ == "__main__":
    pjson = PackageJson("plcbus")
    pjson = PackageJson("velbus")
