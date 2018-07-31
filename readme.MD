# Using Nornir for Discovery and Configuration Creation

## Goal

Here is a small network engineering/network operations task we would like to automate.

 We must evaluate the vlan state of switches in the environment and remove any vlans that are not in use.  In addition, we must ensure that a standard set of vlans is configured on each switch:
- 10 for Data
- 100 for Voice
- 300 for Digital Signage
- 666 for User Static IP Devices

We will take this one step at a time.  First, we will query our devices for the data that we need to help us decide what vlans to keep and what vlans to remove (via the show vlan IOS command).  Next, we will take that data and generate a customized configuration "snippet" or set of commands that we can later apply to each device to achieve our desired result.  When we are done each switch will only have Vlans that are in use and a standard set of vlans supporting voice, data, digital signage, and user devices with static IPs.  As an added wrinkle, I have some devices that are only accessible via Telnet (you would be surprised at how often I find this to be the case.)


## Assumptions

This task may not be completely "real world", but all the strategies and tools used to accomplish this are very applicable to real world scenarios and in fact are based on work I'm currently doing for a Client.

Assumptions:
- All devices in our current inventory are switches
- We only care about vlans 2 through 999
- In this exercise we only want to generate the proposed configurations and save them to file for later review.  We will apply the configuration at a later time.


## Environment and Connections

We spent a little bit of time reviewing the environment set up for Nornir when we [first looked at Nornir](https://www.linkedin.com/pulse/my-first-brigade-claudia-de-luna/?published=t).

Let's expand on that here.

We still have our *groups.yaml* file with a few more groups for us to use in the future.

**groups.yaml**

```yaml
---
uwaco_network:
  nornir_username: cisco
  nornir_password: cisco
  nornir_nos: ios

uwaco_datacenter:
  nornir_username: cisco
  nornir_password: cisco
  nornir_nos: ios

access:
  nornir_username: cisco
  nornir_password: cisco
  nornir_nos: ios
  model: 3800

defaults:
  nornir_username: cisco
  nornir_password: cisco
  nornir_nos: ios
```

Our *hosts.yaml* file has expanded to 4 devices and has some additional attributes.  Notice that the group attribute has to be a list and I show two ways of entering that into your hosts file.  You can use the python square bracket ['element1', 'element2'] convention used for the eu-med-as01 device or the yaml indented "-"" notation used for the pacific-as01 device. Both are equally valid.

It is a good practice to check you YAML files with a [YAML linter](http://www.yamllint.com/).  If there are issues with these files, you won't get far.  A quick check with a linter saves you the time you might otherwise spend troubleshooting what may just be a spacing issue!

The other item to point out here is the "wrinkle" I mentioned when describing the scenario, Telnet.  Some devices do not support SSH.
Thankfully, [Kirk Byers](https://pynet.twb-tech.com/), author of Netmiko added Telnet support and Napalm, which leverages Netmiko for some device connections, can make use of it.   You can see how to do that in the *hosts.yaml* file below.

We are leveraging the *optional_args* optional argument in the [Nornir napalm connection Plugin](https://brigade.readthedocs.io/en/latest/plugins/tasks/connections.html?highlight=optional_args).  


**hosts.yaml**

```yaml
---
eu-med-as01:
  nornir_host: 10.1.10.201
  groups: ['uwaco_network']


pacific-as01:
  nornir_host: 10.1.10.203
  groups:
    - 'uwaco_network'
    - 'access'


ToR_esx01:
  nornir_host: 10.1.10.202
  groups: ['uwaco_datacenter']
  napalm_options: {'transport': 'telnet','secret': 'cisco'}


arctic-as01:
  nornir_host: 10.1.10.100
  groups: ['uwaco_network']
  napalm_options: {'transport': 'telnet','secret': 'cisco'}

```



##  Query Devices and Analyze

The script *nornir_discovery.py* instantiates the Nornir environment defined with our hosts and groups YAML files and executes "show vlan" on every device in the environment.  Nornir has filtering mechanisms that let you act on just the devices you want but that is a topic for a later discussion.  To keep it simpler and let us focus on the important bits we are going to act on all 4 switches.  Later on filtering will seem trivial (it is).

Once we obtain the show vlan output we will put it in a data structure that lets us analyze it.  The *nornir_discovery.py* script is just to show you how this query part works.   You can run it so you can get an idea of the processing we are doing before getting to the configuration creation part of the program.

Note that in this analysis includes Vlan1 however in the actual processing we will exclude Vlan1 as we don't want to remove it (and can't anyway)

```
(nornir) Claudias-iMac:nornir-config claudia$ python nornir_discovery.py
napalm_cli**********************************************************************
* ToR_esx01 ** changed : False *************************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* arctic-as01 ** changed : False ***********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* eu-med-as01 ** changed : False ***********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* pacific-as01 ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

== Parsing vlan output for device eu-med-as01 using TextFSM and NetworkToCode template.
================================================================================
Analyzing Vlans and required actions to implement new vlan policy for device eu-med-as01

VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                          12      Keeping this vlan
2       VLAN0002                active                           0      This vlan will be removed!
3       VLAN0003                active                           0      This vlan will be removed!
4       VLAN0004                active                           0      This vlan will be removed!
5       VLAN0005                active                           0      This vlan will be removed!
6       VLAN0006                active                           0      This vlan will be removed!
7       VLAN0007                active                           0      This vlan will be removed!
8       VLAN0008                active                           0      This vlan will be removed!
9       VLAN0009                active                           0      This vlan will be removed!
10      VLAN0010                active                           0      This vlan will be removed!
11      VLAN0011                active                           1      Keeping this vlan
12      VLAN0012                active                           1      Keeping this vlan
13      VLAN0013                active                           1      Keeping this vlan
14      VLAN0014                active                           0      This vlan will be removed!
15      VLAN0015                active                           0      This vlan will be removed!
16      VLAN0016                active                           0      This vlan will be removed!
17      VLAN0017                active                           0      This vlan will be removed!
18      VLAN0018                active                           0      This vlan will be removed!
19      VLAN0019                active                           0      This vlan will be removed!
20      VLAN0020                active                           0      This vlan will be removed!
21      VLAN0021                active                           0      This vlan will be removed!
22      VLAN0022                active                           0      This vlan will be removed!
23      VLAN0023                active                           0      This vlan will be removed!
24      VLAN0024                active                           0      This vlan will be removed!
25      VLAN0025                active                           0      This vlan will be removed!
26      VLAN0026                active                           0      This vlan will be removed!
27      VLAN0027                active                           0      This vlan will be removed!
28      VLAN0028                active                           0      This vlan will be removed!
29      VLAN0029                active                           0      This vlan will be removed!
30      VLAN0030                active                           0      This vlan will be removed!
31      VLAN0031                active                           0      This vlan will be removed!
32      VLAN0032                active                           0      This vlan will be removed!
33      VLAN0033                active                           0      This vlan will be removed!
34      VLAN0034                active                           0      This vlan will be removed!
35      VLAN0035                active                           0      This vlan will be removed!
36      VLAN0036                active                           0      This vlan will be removed!
37      VLAN0037                active                           0      This vlan will be removed!
38      VLAN0038                active                           0      This vlan will be removed!
39      VLAN0039                active                           0      This vlan will be removed!
40      VLAN0040                active                           0      This vlan will be removed!
41      VLAN0041                active                           0      This vlan will be removed!
42      VLAN0042                active                           0      This vlan will be removed!
43      VLAN0043                active                           0      This vlan will be removed!
44      VLAN0044                active                           0      This vlan will be removed!
45      VLAN0045                active                           0      This vlan will be removed!
46      VLAN0046                active                           0      This vlan will be removed!
47      VLAN0047                active                           0      This vlan will be removed!
48      VLAN0048                active                           0      This vlan will be removed!
500     BBTV-500                active                           0      This vlan will be removed!
501     BBTV-501                active                           0      This vlan will be removed!
502     BBTV-502                active                           0      This vlan will be removed!
503     BBTV-503                active                           0      This vlan will be removed!
================================================================================

== Parsing vlan output for device arctic-as01 using TextFSM and NetworkToCode template.
================================================================================
Analyzing Vlans and required actions to implement new vlan policy for device arctic-as01

VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                           7      Keeping this vlan
10      Management_Vlan         active                           1      Keeping this vlan
20      Web_Tier                active                           0      This vlan will be removed!
30      App_Tier                active                           0      This vlan will be removed!
40      DB_Tier                 active                           0      This vlan will be removed!
================================================================================

== Parsing vlan output for device ToR_esx01 using TextFSM and NetworkToCode template.
================================================================================
Analyzing Vlans and required actions to implement new vlan policy for device ToR_esx01

VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                          12      Keeping this vlan
================================================================================

== Parsing vlan output for device pacific-as01 using TextFSM and NetworkToCode template.
================================================================================
Analyzing Vlans and required actions to implement new vlan policy for device pacific-as01

VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                          12      Keeping this vlan
5       PortSeattle-5           active                           0      This vlan will be removed!
6       VLAN0006                active                           0      This vlan will be removed!
7       DD-MockServer_Vlan      active                           0      This vlan will be removed!
100     Data_Vlan               active                           0      This vlan will be removed!
101     VLAN0101                active                           0      This vlan will be removed!
102     VLAN0102                active                           0      This vlan will be removed!
103     Data_Manutencao         active                          11      Keeping this vlan
104     VLAN0104                active                           0      This vlan will be removed!
200     Voice_Vlan              active                           0      This vlan will be removed!
201     VLAN0201                active                           0      This vlan will be removed!
202     VLAN0202                active                           0      This vlan will be removed!
203     Voice_Manutencao        active                           3      Keeping this vlan
300     WLAN                    active                           0      This vlan will be removed!
303     WLAN_SCAN               active                           0      This vlan will be removed!
571     VLAN0571                active                           0      This vlan will be removed!
888     Native_Vlan888          active                           0      This vlan will be removed!
================================================================================
(nornir) Claudias-iMac:nornir-config claudia$


```


In fact, the main configuration script, *nornir_config_create.py* imports the nornir_discovery.py script so it can make use of the two functions within that script:
- send_napalm_commands
- parse_with_texfsm

In *nornir_config_create.py* we put it all together with a Nornir "Task" function
- config_to_file

Here is where we start getting into "all that Nornir" does for us.  I've just scratched the surface!  These "Task" functions have some special behavior which I'm just figuring out myself.  They act in a task based manner against our selected inventory allowing us a collective task approach that says "do these things to these devices" in a way that does not involve iterating and applying logic to each device.  Wow!  It may take a bit to get used to and you really need to understand the objects you are getting back from Nornir so you can get to the data you want.  

Lets look at the *config_to_file* function first.  


```python {.line-numbers}
def config_to_file(task, arg={}):

    # Define the Jinja2 template file we will use to build our custom commands for each device
    j2template = 'vlan_updates.j2'

    filename = "cfg-{}.txt".format(task.host)

    task.host["rendered_cfg"] = task.run(task=template_file, template=j2template, path='', info=arg)

    with open(filename,"w") as cfg_file:
        cfg_file.write(str(task.host['rendered_cfg'][0]))

    print("\nCreated Configuration file {} for device {} in local directory...".format(task.host,filename))


```


We create a variable *j2template* to hold our Jinja2 template file.  We also create a filename for each of our devices where the resuling customized configuration will be saved.

The Jinja2 template itself is fairly straighforward. The "host" and "host.name" variables are set within the Nornir environment and passed to the *config_to_file* task.  The "info" dictionary was the tricky part as we needed a list of vlans to remove from each host. We built this as a dictionary where the key is the hostname and the value is the list of vlans to remove.   The **for** statement in the Jinja 2 template pulls the key:value pair for the device for which we are building the configuration using info[host.name].  The value is a list of vlans to remove.  The **for** loop iterates over this list and builds as many "no vlanXXXX" lines as required to remove all the unused vlans for that switch.

If you want to see the raw data add a statement just above the for loop to display that particular variable.

```jinja2
! For device {{ host }}
! {{ info[host.name] }} <- add this to the vlan_updates.j2 file to display the list
```

You will see something like this in the resulting configation file:
```jinja2
! For device arctic-as01
! [u'20', u'30', u'40']
```

So we know that "host" and "host.name" are passed to our function via Nornir but how did we get the info dictionary in there?  That was also passed to the Jinja2 rendering "engine" when we ran our Nornir task as we will see in the *config_to_file* function.

vlan_updates.j2 Jinja2 Template file

```jinja2

! For device {{ host }}
!

{% for vlan2remove in info[host.name] %}
no vlan{{ vlan2remove }}

{% endfor %}

vlan 10
 name Data_Vlan

vlan 100
 name Voice_Vlan

vlan 300
 name Digital_Signage

vlan 666
 name User_Static_IP_Devices
```

We know what our Jinja2 template looks like now and hopefully we are getting an idea of how we got at least the host values to the template.   

This is our "money" command:

```python
task.host["rendered_cfg"] = task.run(task=template_file, template=j2template, path='', info=arg)

```

What exactly is happening here you ask?  Well we are running a Nornir "task" actually called **task**.  This can be a little confusing at first but we are in a Nornir "task" function called from within the Nornir instance in the main function (r = nornir_instance.run(task=**config_to_file**, arg=j2_data_dict)).  

Looking at the arguments we are giving to task.run
- we are running the Nornir configuration task "template_file"  
- we are passing the j2template value
- we are passing a path value that is empty so that Nornir will look for the Jinja2 template in the current working directory.
If we passed it path-'./templates' it would look for the jinja2 template in the templates directory under the current working directory

```python
task.host["rendered_cfg"] = task.run(task=template_file, template=j2template, path='./templates', info=arg)
```

So with the first 3 arguments we've defined the task we are asking Nornir to run, we are telling it what Jinja2 template to use and where to find it.    With just these 3 arguments we could generate configs that only used data defined in the task.  However we have spent time constructing a dictionary that has the vlans to remove for each device and so we have to pass an optional argument "info=arg".

The variable "info" is what the Jinja2 template will look for.

Remember the **for** statement in our Jinja2 template?  This is where "info" came from. We passed it to the Nornir Jinja2 rendering task as an additional argument when we called task.run(task=template_file...).
```
{% for vlan2remove in info[host.name] %}
```

What is in "info"?  It is a dictionary where the key maps to the host name and the value is a list of vlans to remove.

Think of this {'sw1':[2.7.9], 'sw2': [201,700]}.

How do I know this?  Because that is what we passed the *config_to_file** task function when we called it from the main function in our *nornir_config_create.py* script.

In the main function of our *nornir_config_create.py* we called (or ran) the *config_to_file* function as a **task** in our Nornir instance.  In our case we also passed a dictionary called j2_data_dict into the optional argument variable "arg".  

In main:
```python
    r = nornir_instance.run(task=config_to_file, arg=j2_data_dict)
```

When we called the template task in the the **config_to_file** function we passed it info=arg thus "handing off" **arg**, which contained our remove vlan dictionary for our Jinja2 template (j2_data_dict) into **info** which can now be directly referenced by our Jinja2 template.

In **config_to_file** function:
```python
task.host["rendered_cfg"] = task.run(task=template_file, template=j2template, path='', info=arg)

```

In Jinja2 template **vlan_updates.j2**:
```jinja2
{% for vlan2remove in info[host.name] %}
no vlan{{ vlan2remove }}

{% endfor %}
```


I hope I'm not belaboring the point but I find that "chain" of variables all the way to the Jinja2 template can be a bit confusing (at least for me).  Lets hope I've lessened the confusion and not added to it!

Finally lets look at our main function.  I've added comments throughout to try to more fully explain what is going on each step of the way.

```python
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
    r = nornir_instance.run(task=config_to_file, arg=j2_data_dict)

    print("\n")
    # Prints abbreviated output
    print_result(r, vars=['stdout'])
    # Prints full output -- good for troubleshooting
    # print_result(r)

```


Upon successful execution of this script you should see new configuration files with a "cfg-" prefix in your working directory.

```bash
(nornir) Claudias-iMac:nornir-config claudia$ ls -al cfg*
-rw-r--r--@ 1 claudia  staff  149 Jul 30 16:31 cfg-ToR_esx01.txt
-rw-r--r--@ 1 claudia  staff  184 Jul 30 16:31 cfg-arctic-as01.txt
-rw-r--r--@ 1 claudia  staff  675 Jul 30 16:31 cfg-eu-med-as01.txt
-rw-r--r--@ 1 claudia  staff  314 Jul 30 16:31 cfg-pacific-as01.txt
(nornir) Claudias-iMac:nornir-config claudia$
```


Lets look at one.

```
(nornir) Claudias-iMac:nornir-config claudia$ cat cfg-arctic-as01.txt

! For device arctic-as01
!

no vlan20

no vlan30

no vlan40


vlan 10
 name Data_Vlan

vlan 100
 name Voice_Vlan

vlan 300
 name Digital_Signage

vlan 666
 name User_Static_IP_Devices

```

So for the switch with hostname arctic-as01, we are removing vlans 20, 30, and 40 and adding the 4 standard vlans per our new policy.

If you recall from the discovery script output:
```
== Parsing vlan output for device arctic-as01 using TextFSM and NetworkToCode template.
================================================================================
Analyzing Vlans and required actions to implement new vlan policy for device arctic-as01

VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                           7      Keeping this vlan
10      Management_Vlan         active                           1      Keeping this vlan
20      Web_Tier                active                           0      This vlan will be removed!
30      App_Tier                active                           0      This vlan will be removed!
40      DB_Tier                 active                           0      This vlan will be removed!
================================================================================

```

I think that is quite enough for now.  I hope all (or some) of this has been useful.   In our next installment I'll look at taking the customized configurations we've created and applying them to each device and validating that each device is now compliant with our new vlan policy.



## Next Steps:

- Apply the configurations

- Introduce filtering of inventory devices

- Start taking a more task oriented approach and use task naming

- Idempotency (we have all the data we need!)

- Refactor
-- One of the things you will notice as you spend more and more time with automation is that you continually improve your code.  Your code will do the same thing but it will be better than it was before (cleaner, faster, more efficient, and more elegant).  Basically refactoring is the [6 Million Dollar Man](https://youtu.be/0CPJ-AbCsT8).
