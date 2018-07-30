#!/usr/bin/python -tt
# Project: Dropbox (Indigo Wire Networks)
# Filename: first_nornir
# claudia
# PyCharm
# Python3

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/7/18"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
from nornir.core import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result


def main():

    # Create Nornir instance using default hosts.yaml and groups.yaml
    print("= Creating a Nornir instances which sets up a basic environment we can explore..")
    nornir_instance = InitNornir()


    # print(dir(nornir_instance))
    print("\nHosts derived from the Inventory file are: \n{}".format(nornir_instance.inventory.hosts))
    for k,v in nornir_instance.inventory.hosts.items():
        print("\tKey: {} \tValue: {}".format(k,v))
    
    print("Groups derived from the Inventory file are: \n{}".format(nornir_instance.inventory.groups))
    for k,v in nornir_instance.inventory.groups.items():
        print("\tKey: {} \tValue: {}".format(k,v))

    print('\n\n== Lets "decompose" some of these instance objects so we know what we have to work with...' )

    print("Decomposing Hosts object <nornir_instance.inventory.hosts>...")
    my_hosts = nornir_instance.inventory.hosts
    print("\tType of my_hosts is {}".format(type(my_hosts)))

    host_keys = list(my_hosts.keys())
    print("\tHost keys = {} of type {} ".format(host_keys, type(host_keys)))
    for i in host_keys:
        print(i)


    print("\nDecomposing Groups <nornir_instance.inventory.groups>...")
    my_groups = nornir_instance.inventory.groups
    group_keys = list(my_groups.keys())
    print("\tGroup keys = {} of type {} ".format(group_keys, type(group_keys)))
    for i in group_keys:
        print(i)

    print("\n")

    print("Now that we have an environment established, lets run some discovery unsing napalm getters...")
    input("Press any key to continue...")
    print("We are now executing napalm get_facts on all of the hosts in our inventory.")

    result = nornir_instance.run(
        napalm_get,
        getters=['get_facts'])

    print("\nDecomposing Result Object of type {}...".format(type(result)))

    result_dict = dict(result)
    print("Lets turn our result object into a dictionary so that now result is of type {}".format(type(result_dict)))

    for i in result_dict:

        li = list(result_dict[i])

        li_keys = li[0].result['get_facts'].keys()
        # dict_keys(['uptime', 'vendor', 'os_version', 'serial_number', 'model', 'hostname', 'fqdn', 'interface_list'])
        #
        print("\n\tDecomposing Result Object for hostname {}...".format(li[0].result['get_facts']['hostname']))
        for k in li_keys:
            print("\t\tKey {} \t : Value = {}".format(k, li[0].result['get_facts'][k]))

        print("\n")


    print("Print run results with the print_result module (this is an Ansible like run status)...")
    print_result(result)





# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="First nornir Script - Discovery",
                                     epilog="Usage: ' python first_nornir.py' ")

    arguments = parser.parse_args()
    main()
