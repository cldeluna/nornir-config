#!/usr/bin/python -tt
# Project: Dropbox (Indigo Wire Networks)
# Filename: nornir_config_create
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "7/30/18"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import nornir_discovery
from nornir.core import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.text import template_file



def config_to_file(task,arg={}):
    # print(task)

    j2template = 'vlan_updates.j2'
    # j2template = 'test.j2'

    # http://nornir.readthedocs.io/en/latest/plugins/tasks/text.html
    # cfg_result = task.run(task=template_file, template=j2template, path='', info=arg)

    # print(cfg_result[0])
    # print(dir(cfg_result))

    filename = "cfg-{}.txt".format(task.host)

    task.host["rendered_cfg"] = task.run(task=template_file, template=j2template, path='', info=arg)

    with open(filename,"w") as cfg_file:
        cfg_file.write(str(task.host['rendered_cfg'][0]))

    print("\nCreated Configuration file {} for device {} in local directory...".format(task.host,filename))


def main():


    send_commands=['show vlan']

    output_dict = nornir_discovery.send_napalm_commands(send_commands, show_output=True, debug=False)

    template_filename = 'cisco_ios_show_vlan.template'

    nornir_instance = InitNornir()

    # nornir_instance.inventory.hosts.update({'test':"somevalue"})

    # print(nornir_instance.inventory.hosts.values)
    # print(dir(nornir_instance.inventory.hosts))
    # print("******")
    j2template = 'vlan_updates.j2'
    j2template = 'test.j2'


    j2_data_dict = {}

    # For each device lets build out the list of vlans which must be removed
    for dev, output in output_dict.items():

        parsed_results = nornir_discovery.parse_with_texfsm(output, template_filename, debug=False)
        remove_vlan_list = []

        # For each Vlan we found configured on the device
        for vlan_data in parsed_results:
            # We are only interested in vlans between 1 and 999
            # vlan_data[0] is the vlan number
            if 1 < int(vlan_data[0]) < 1000:

                ints_in_vlan = len(vlan_data[3])

                # If the vlan has no associated interfaces, the add it to the remove_vlan_list list
                if ints_in_vlan == 0:
                    remove_vlan_list.append(vlan_data[0])

        # Build a dictionary where the key is the device or host and the value the list of vlans to remove
        # This will be passed along when we build our configs
        j2_data_dict.update({dev: remove_vlan_list})

    # nornir_instance.inventory.hosts.update({'remove_vlan_list': remove_vlan_list})
    #
    # nornir_instance.inventory.hosts.update
    # print(j2_data_dict)

    r = nornir_instance.run(task=config_to_file, arg=j2_data_dict)
    # print_result(r, vars=['stdout'])
    print("\n")
    print_result(r, vars=['stdout'])

    # j2_data_dict[dev] = remove_vlan_list
    # print(j2_data_dict)
    #
    #
    #
    #
    #
    # print(cfg_result)
    # print(cfg_result.keys())
    # for k in cfg_result.keys():
    #     print(cfg_result[k].result)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python nornir_config_create' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
                        default=False)
    arguments = parser.parse_args()
    main()
