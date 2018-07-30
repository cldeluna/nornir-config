#!/usr/bin/python -tt
# Project: Dropbox (Indigo Wire Networks)
# Filename: nornir_discovery
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "7/29/18"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import textfsm
from nornir.core import InitNornir
from nornir.plugins.tasks.networking import napalm_cli
from nornir.plugins.functions.text import print_result


def send_napalm_commands(cmds, show_output=False, debug=False):
    """
    For a given list of commands, cmds, execute the napalm_cli method and return a dictionary of dictionaries
    First key = device
    Secondary key(s) = show commands executed via cmds

    show_output is an optional argument which prints out the Ansible-like run output.
    debug is an optional argument which prints out values to assist in debugging.

    :param cmds: list of commands to execute on each device
    :param show_output: Boolean which defaults to False.
        When True values the Ansible-like run output will be printed to stdout
    :param debug: Boolean which defaults to False. When True values will be printed to stdout
    :return: output_dict
    """

    output_dict = {}

    if isinstance(cmds, list):

        nornir_instance = InitNornir(dry_run=True)

        cli_result = nornir_instance.run(napalm_cli, commands=cmds)

        # Our goal is to build a dictionary of dictionaries
        # so that it can be referenced a bit more simply as output_dict[device1][showcmd1]

        # Iterate over the first set of keys in the results object which will represent each device
        for dev_key in cli_result.keys():

            # Iterate over one or more results keys which represent the show command or show commands
            # extracted from each device
            # Alternatively we could use the cmds list to build the inside dict
            # but just in case something goes wrong, lets build it from the actual keys
            if debug: print(cli_result[dev_key][0].result.keys())

            for result_key in cli_result[dev_key][0].result.keys():
                output_dict.update({dev_key: cli_result[dev_key][0].result[result_key]})


        if debug:
            for k,v in output_dict.items():
                print("device: {} \toutput: {}".format(k,v))

    else:
        print("ERROR! argument passed to function must be a list!  Will return empty dictionary.")

    if show_output: print(print_result(cli_result))

    return output_dict


def parse_with_texfsm(content, template_file, debug=False):

    template = open(template_file)

    result_of_template = textfsm.TextFSM(template)

    results = result_of_template.ParseText(content)

    if debug:
        print("\nKeys available when using the {} template:".format(template_file))
        # This shows the "column headers" or fields names of the data we will get back from ParseText
        print(result_of_template.header)
        # This shows the field names and the REGEXP that is being used to pluck out the values
        print(result_of_template.value_map)
        print("\nDetails on the results variable...")
        print("results is of type {}".format(type(results)))
        print("results has {} element(s)".format(len(results)))
        if isinstance(results, list):
            for line in results:
                print(line)
        else:
            print(results)

        print("\n")



    return results


def main():

    send_commands=['show vlan']
    output_dict = send_napalm_commands(send_commands, show_output=False)

    # print("Device List: {}".format(output_dict.keys()))

    # for k, v in output_dict.items():
    #     print("device: {} \toutput: {}".format(k, v))


    # Napalm does not have a direct get_vlan method just yet and so its up to us to get the vlan data into a
    # usable data structure
    # We will use TextFSM and lucky for us we can tap into the NetworkToCode textfsm repository for a
    # parsing template that will do just what we need!
    # https://github.com/networktocode/ntc-templates/blob/master/templates/cisco_ios_show_vlan.template

    # This assumes that the template is in the local directory. If it is elsewhere, make sure the template_file
    # variable reflects the full path to the location.
    template_file = 'cisco_ios_show_vlan.template'

    # Knowing that our dictionary keys are the devices and the values are a dictionary of one or more cli commands sent
    for dev, output in output_dict.items():

        print("\n== Parsing vlan output for device {} using TextFSM and NetworkToCode template.".format(dev))
        # print("device: {} \t\noutput: {}".format(dev, output))

        # I broke out the parsing into a function because it can often be re-used elsewhere
        # parsed_results will be a list.
        # to print out values that can help with debuggign and undersatnding the data structures change debug to True
        # debug=True
        parsed_results = parse_with_texfsm(output, template_file, debug=True)

        print("=" * 40)
        print("{:7}\t{:20}\t{:10}\t{:18}\t{}".format("VLAN_ID", "NAME", "STATUS", "TOTAL_INT_IN_VLAN", "ACTION"))

        for vlan_data in parsed_results:
            # We are only interested in vlans between 2 and 999
            # vlan_data[0] is the vlan number
            if 0 < int(vlan_data[0]) < 1000:

                ints_in_vlan = len(vlan_data[3])

                if ints_in_vlan == 0:
                    vlan_action = "This vlan will be removed!"
                else:
                    vlan_action = "Keeping this vlan"
                print("{:7}\t{:20}\t{:10}\t{:18}\t{}".format(vlan_data[0], vlan_data[1], vlan_data[2],
                                                             len(vlan_data[3]), vlan_action))
        print("=" * 40)



# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python nornir_discovery' ")

    # #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
    #                     default=False)
    arguments = parser.parse_args()
    main()
