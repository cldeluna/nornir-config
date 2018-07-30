# Example from Patrick Ogenstad at Networklore
# https://networklore.com/introducing-nornir
# https://blogs.cisco.com/developer/nornir-python-automation-framework
from nornir.core import InitNornir
from nornir.plugins.tasks.networking import napalm_get, napalm_cli
from nornir.plugins.functions.text import print_result

nornir_instance = InitNornir(dry_run=True)


myhosts = nornir_instance.inventory.hosts['pacific-as01'].to_dict()
# print(myhosts)

# result = nornir_object.run(
#              napalm_get,
#              getters=['get_facts'])

cli_result = nornir_instance.run(napalm_cli,commands=['show vlan', 'show ver'])

print()
print("cli keys")
print(cli_result.keys())

print(cli_result['pacific-as01'])

print("result keys")
print(cli_result['pacific-as01'][0].result.keys())

# print(cli_result['pacific-as01'][0].result['show vlan'])
# print(cli_result['pacific-as01'][0].result['show ver'])
# print(len(cli_result['pacific-as01']))
# print(dir(cli_result['pacific-as01'][0]))

# for item in cli_result:
#     myhosts = nornir_instance.inventory.hosts[item].to_dict()
#     print(myhosts)
#     print()
#     print(cli_result[item])
    # # print(dir(cli_result[item]))
    # for i in cli_result[item]:
    #     print("\ti[0] is {}".format(i[0]))
    #     print("++++++++++++++++")
        # print(i['napalm_cli'])
    # print(item)
    # print(dir(item))
    # print(type(item))
print("="*40)

# print_result(cli_result)
# print("="*40)
# print_result(cli_result)