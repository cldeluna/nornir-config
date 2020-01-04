#!/usr/bin/python -tt
# Project: Dropbox (Indigo Wire Networks)
# Filename: first_brigade
# claudia
# PyCharm
# Python3

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/7/18"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result


def main():

    # Create instance using default hosts.yaml and groups.yaml
    nr = InitNornir(config_file='config.yaml')

    # print(dir(nr))
    print("Hosts derived from the Inventory file are: \t{}".format(nr.inventory.hosts))
    print("Groups derived from the Inventory file are: \t{}".format(nr.inventory.groups))

    print("\nDecomposing Groups...")
    my_groups = nr.inventory.groups
    group_keys = list(my_groups.keys())
    print("Group keys = {} of type {} ".format(group_keys, type(group_keys)))
    for i in group_keys:
        print(f"- {i}")

    print("\nDecomposing Hosts...")
    my_hosts = nr.inventory.hosts
    print("Type of nr.inventory.hosts in var my_hosts is {}".format(type(my_hosts)))

    host_keys = list(my_hosts.keys())
    print("Host keys = {} of type {} ".format(host_keys, type(host_keys)))
    for i in host_keys:
        print(f"- {i}")

    print("\n")

    print(f"Logging into hosts in inventory and getting napalm facts...")
    result = nr.run(
        napalm_get,
        getters=['get_facts'])

    print(f"napalm facts stored in the varialbe 'result'...")

    # Printing now may help you decompose the resulting objects
    # print_result(result)


    print(f"\nDecomposing Nornir Result Object of type {type(result)}...\n")

    for i in result:
        print(f"Iterating through result object of type{type(result[i])} for item {i}")

        print(f"\tGet the top level key(s) for the device:")
        top_result_keys = result[i].result.keys()
        print(f"\t{top_result_keys}")
        # Example output: dict_keys(['get_facts'])

        print(f"\n\tGet the next level of key(s):")
        next_keys = result[i].result['get_facts'].keys()
        print(f"\t{next_keys}")
        # Example output: dict_keys(['uptime', 'vendor', 'os_version', 'serial_number', 'model', 'hostname', 'fqdn', 'interface_list'])

        # Iterate through the keys and values
        print(f"\tDecomposing Result Object for hostname {i}...")
        for k in next_keys :
            print(f"\t\tKey {k} \t has Value: {result[i].result['get_facts'][k]}")

        print("\n")

    print(f"\nPrint run results with the print_result module."
           "\nThis is a built-in Ansible like run status that will format the output for easy viewing...")
    print_result(result)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="First Brigade Script - Discovery",
                                     epilog="Usage: ' python first_brigade.py' ")

    arguments = parser.parse_args()
    main()
