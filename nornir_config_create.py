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
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.text import template_file


def config_to_file(task, arg={}):
    """
    Nornir Task

    :param task:
    :param arg:
    :return:
    """

    # Define the Jinja2 template file we will use to build our custom commands for each device
    j2template = 'vlan_updates.j2'

    # Generate a unique text file of commands for each device in our inventory
    filename = "cfg-{}.txt".format(task.host)


    task.host["rendered_cfg"] = task.run(task=template_file, template=j2template, path='', info=arg)

    with open(filename,"w") as cfg_file:
        cfg_file.write(str(task.host['rendered_cfg'][0]))

    print("\nCreated Configuration file {} for device {} in local directory...".format(task.host,filename))


def main():

    # Get our shov vlan output from each device in our inventory
    send_commands=['show vlan']
    output_dict = nornir_discovery.send_napalm_commands(send_commands, show_output=True, debug=False)

    # Set the TextFSM template we will be using to parse the show vlan output so we get it back in a way we can use
    template_filename = 'cisco_ios_show_vlan.template'

    # Initialize the vlan dictionary we will send to our Jinja2 template
    j2_data_dict = {}

    # ======= Define the Nornir Environment ========
    nornir_instance = InitNornir()


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

    # ====== Generate Configs
    # Execute a task "run" in the Nornir environment using our config_file Task function and pass it the customized data
    # which is required to build out a custom config for each device removing any unused vlans and adding the standard
    # vlans
    print(f"Generating configurations")
    r = nornir_instance.run(task=config_to_file, arg=j2_data_dict)

    print("\n")
    # Prints abbreviated output
    print_result(r, vars=['stdout'])
    # Prints full output -- good for troubleshooting
    print_result(r)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python nornir_config_create' ")

    arguments = parser.parse_args()
    main()
