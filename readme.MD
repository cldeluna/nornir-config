# First Brigade Test Run
## Get Facts

## Summary

First test with Brigade.

This was my first use of Brigade.  I started out with the sample get facts run_brigade.py script from from [Patrick Ogenstad at Networklore.](https://networklore.com/introducing-brigade/)

The first_brigade.py script is my attempt to decompose the objects and resulting data structures.

I'm fairly excited about this!  It took me about 45 minutes to get things set up on my Windows 10 system.  It took
almost no time at all on my Mac.

Using PyCharm on my mac the print_result output is formatted and color coded nicely.  Using PyCharm on my Windows 10
system the output is less colorful.

My next Sunday afternoon project will involve generating configurations and applying them.

## Code Example

Like Ansible, Brigade will leverage a set of inventory information.  Here you see a very basic groups.yaml file which
can also contain a default section for more general values and a hosts.yaml file which can reference specific
or more general group settings defined in the groups.yaml file.  These files can take any key:value pair and the values
with the "brigade_" prefix have special meaning as you would expect.



groups.yaml

        ---
        uwaco_network:
          brigade_username: cisco
          brigade_password: cisco
          brigade_nos: ios

hosts.yaml

        ---
        eu-med-as01:
          brigade_host: 10.1.10.25
          groups: ['uwaco_network']
      
        arctic-ds01-as01:
          brigade_host: 10.1.10.26
          groups: ['uwaco_network']



```
(cat_scripts) Claudias-iMac:nornir-config claudia$ python nornir_discovery.py

Keys available when using the cisco_ios_show_vlan.template template:
['STATUS', 'INTERFACES', 'NAME', 'VLAN_ID']
========================================

== Parsing vlan output for device eu-med-as01 using TextFSM and NetworkToCode template.
VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                            12    Keeping this vlan
2       VLAN0002                active                             0    This vlan will be removed!
3       VLAN0003                active                             0    This vlan will be removed!
4       VLAN0004                active                             0    This vlan will be removed!
5       VLAN0005                active                             0    This vlan will be removed!
6       VLAN0006                active                             0    This vlan will be removed!
7       VLAN0007                active                             0    This vlan will be removed!
8       VLAN0008                active                             0    This vlan will be removed!
9       VLAN0009                active                             0    This vlan will be removed!
10      VLAN0010                active                             0    This vlan will be removed!
11      VLAN0011                active                             1    Keeping this vlan
12      VLAN0012                active                             1    Keeping this vlan
13      VLAN0013                active                             1    Keeping this vlan
14      VLAN0014                active                             0    This vlan will be removed!
15      VLAN0015                active                             0    This vlan will be removed!
16      VLAN0016                active                             0    This vlan will be removed!
17      VLAN0017                active                             0    This vlan will be removed!
18      VLAN0018                active                             0    This vlan will be removed!
19      VLAN0019                active                             0    This vlan will be removed!
20      VLAN0020                active                             0    This vlan will be removed!
21      VLAN0021                active                             0    This vlan will be removed!
22      VLAN0022                active                             0    This vlan will be removed!
23      VLAN0023                active                             0    This vlan will be removed!
24      VLAN0024                active                             0    This vlan will be removed!
25      VLAN0025                active                             0    This vlan will be removed!
26      VLAN0026                active                             0    This vlan will be removed!
27      VLAN0027                active                             0    This vlan will be removed!
28      VLAN0028                active                             0    This vlan will be removed!
29      VLAN0029                active                             0    This vlan will be removed!
30      VLAN0030                active                             0    This vlan will be removed!
31      VLAN0031                active                             0    This vlan will be removed!
32      VLAN0032                active                             0    This vlan will be removed!
33      VLAN0033                active                             0    This vlan will be removed!
34      VLAN0034                active                             0    This vlan will be removed!
35      VLAN0035                active                             0    This vlan will be removed!
36      VLAN0036                active                             0    This vlan will be removed!
37      VLAN0037                active                             0    This vlan will be removed!
38      VLAN0038                active                             0    This vlan will be removed!
39      VLAN0039                active                             0    This vlan will be removed!
40      VLAN0040                active                             0    This vlan will be removed!
41      VLAN0041                active                             0    This vlan will be removed!
42      VLAN0042                active                             0    This vlan will be removed!
43      VLAN0043                active                             0    This vlan will be removed!
44      VLAN0044                active                             0    This vlan will be removed!
45      VLAN0045                active                             0    This vlan will be removed!
46      VLAN0046                active                             0    This vlan will be removed!
47      VLAN0047                active                             0    This vlan will be removed!
48      VLAN0048                active                             0    This vlan will be removed!
500     BBTV-500                active                             0    This vlan will be removed!
501     BBTV-501                active                             0    This vlan will be removed!
502     BBTV-502                active                             0    This vlan will be removed!
503     BBTV-503                active                             0    This vlan will be removed!
========================================
========================================

== Parsing vlan output for device arctic-as01 using TextFSM and NetworkToCode template.
VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                            12    Keeping this vlan
2       VLAN0002                active                             0    This vlan will be removed!
3       VLAN0003                active                             0    This vlan will be removed!
4       VLAN0004                active                             0    This vlan will be removed!
5       VLAN0005                active                             0    This vlan will be removed!
6       VLAN0006                active                             0    This vlan will be removed!
7       VLAN0007                active                             0    This vlan will be removed!
8       VLAN0008                active                             0    This vlan will be removed!
9       VLAN0009                active                             0    This vlan will be removed!
10      VLAN0010                active                             0    This vlan will be removed!
11      VLAN0011                active                             1    Keeping this vlan
12      VLAN0012                active                             1    Keeping this vlan
13      VLAN0013                active                             1    Keeping this vlan
14      VLAN0014                active                             0    This vlan will be removed!
15      VLAN0015                active                             0    This vlan will be removed!
16      VLAN0016                active                             0    This vlan will be removed!
17      VLAN0017                active                             0    This vlan will be removed!
18      VLAN0018                active                             0    This vlan will be removed!
19      VLAN0019                active                             0    This vlan will be removed!
20      VLAN0020                active                             0    This vlan will be removed!
21      VLAN0021                active                             0    This vlan will be removed!
22      VLAN0022                active                             0    This vlan will be removed!
23      VLAN0023                active                             0    This vlan will be removed!
24      VLAN0024                active                             0    This vlan will be removed!
25      VLAN0025                active                             0    This vlan will be removed!
26      VLAN0026                active                             0    This vlan will be removed!
27      VLAN0027                active                             0    This vlan will be removed!
28      VLAN0028                active                             0    This vlan will be removed!
29      VLAN0029                active                             0    This vlan will be removed!
30      VLAN0030                active                             0    This vlan will be removed!
31      VLAN0031                active                             0    This vlan will be removed!
32      VLAN0032                active                             0    This vlan will be removed!
33      VLAN0033                active                             0    This vlan will be removed!
34      VLAN0034                active                             0    This vlan will be removed!
35      VLAN0035                active                             0    This vlan will be removed!
36      VLAN0036                active                             0    This vlan will be removed!
37      VLAN0037                active                             0    This vlan will be removed!
38      VLAN0038                active                             0    This vlan will be removed!
39      VLAN0039                active                             0    This vlan will be removed!
40      VLAN0040                active                             0    This vlan will be removed!
41      VLAN0041                active                             0    This vlan will be removed!
42      VLAN0042                active                             0    This vlan will be removed!
43      VLAN0043                active                             0    This vlan will be removed!
44      VLAN0044                active                             0    This vlan will be removed!
45      VLAN0045                active                             0    This vlan will be removed!
46      VLAN0046                active                             0    This vlan will be removed!
47      VLAN0047                active                             0    This vlan will be removed!
48      VLAN0048                active                             0    This vlan will be removed!
500     BBTV-500                active                             0    This vlan will be removed!
501     BBTV-501                active                             0    This vlan will be removed!
502     BBTV-502                active                             0    This vlan will be removed!
503     BBTV-503                active                             0    This vlan will be removed!
========================================
========================================

== Parsing vlan output for device ToR_esx01 using TextFSM and NetworkToCode template.
VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                            12    Keeping this vlan
2       VLAN0002                active                             0    This vlan will be removed!
3       VLAN0003                active                             0    This vlan will be removed!
4       VLAN0004                active                             0    This vlan will be removed!
5       VLAN0005                active                             0    This vlan will be removed!
6       VLAN0006                active                             0    This vlan will be removed!
7       VLAN0007                active                             0    This vlan will be removed!
8       VLAN0008                active                             0    This vlan will be removed!
9       VLAN0009                active                             0    This vlan will be removed!
10      VLAN0010                active                             0    This vlan will be removed!
11      VLAN0011                active                             1    Keeping this vlan
12      VLAN0012                active                             1    Keeping this vlan
13      VLAN0013                active                             1    Keeping this vlan
14      VLAN0014                active                             0    This vlan will be removed!
15      VLAN0015                active                             0    This vlan will be removed!
16      VLAN0016                active                             0    This vlan will be removed!
17      VLAN0017                active                             0    This vlan will be removed!
18      VLAN0018                active                             0    This vlan will be removed!
19      VLAN0019                active                             0    This vlan will be removed!
20      VLAN0020                active                             0    This vlan will be removed!
21      VLAN0021                active                             0    This vlan will be removed!
22      VLAN0022                active                             0    This vlan will be removed!
23      VLAN0023                active                             0    This vlan will be removed!
24      VLAN0024                active                             0    This vlan will be removed!
25      VLAN0025                active                             0    This vlan will be removed!
26      VLAN0026                active                             0    This vlan will be removed!
27      VLAN0027                active                             0    This vlan will be removed!
28      VLAN0028                active                             0    This vlan will be removed!
29      VLAN0029                active                             0    This vlan will be removed!
30      VLAN0030                active                             0    This vlan will be removed!
31      VLAN0031                active                             0    This vlan will be removed!
32      VLAN0032                active                             0    This vlan will be removed!
33      VLAN0033                active                             0    This vlan will be removed!
34      VLAN0034                active                             0    This vlan will be removed!
35      VLAN0035                active                             0    This vlan will be removed!
36      VLAN0036                active                             0    This vlan will be removed!
37      VLAN0037                active                             0    This vlan will be removed!
38      VLAN0038                active                             0    This vlan will be removed!
39      VLAN0039                active                             0    This vlan will be removed!
40      VLAN0040                active                             0    This vlan will be removed!
41      VLAN0041                active                             0    This vlan will be removed!
42      VLAN0042                active                             0    This vlan will be removed!
43      VLAN0043                active                             0    This vlan will be removed!
44      VLAN0044                active                             0    This vlan will be removed!
45      VLAN0045                active                             0    This vlan will be removed!
46      VLAN0046                active                             0    This vlan will be removed!
47      VLAN0047                active                             0    This vlan will be removed!
48      VLAN0048                active                             0    This vlan will be removed!
500     BBTV-500                active                             0    This vlan will be removed!
501     BBTV-501                active                             0    This vlan will be removed!
502     BBTV-502                active                             0    This vlan will be removed!
503     BBTV-503                active                             0    This vlan will be removed!
========================================
========================================

== Parsing vlan output for device pacific-as01 using TextFSM and NetworkToCode template.
VLAN_ID NAME                    STATUS          TOTAL_INT_IN_VLAN       ACTION
1       default                 active                            12    Keeping this vlan
2       VLAN0002                active                             0    This vlan will be removed!
3       VLAN0003                active                             0    This vlan will be removed!
4       VLAN0004                active                             0    This vlan will be removed!
5       VLAN0005                active                             0    This vlan will be removed!
6       VLAN0006                active                             0    This vlan will be removed!
7       VLAN0007                active                             0    This vlan will be removed!
8       VLAN0008                active                             0    This vlan will be removed!
9       VLAN0009                active                             0    This vlan will be removed!
10      VLAN0010                active                             0    This vlan will be removed!
11      VLAN0011                active                             1    Keeping this vlan
12      VLAN0012                active                             1    Keeping this vlan
13      VLAN0013                active                             1    Keeping this vlan
14      VLAN0014                active                             0    This vlan will be removed!
15      VLAN0015                active                             0    This vlan will be removed!
16      VLAN0016                active                             0    This vlan will be removed!
17      VLAN0017                active                             0    This vlan will be removed!
18      VLAN0018                active                             0    This vlan will be removed!
19      VLAN0019                active                             0    This vlan will be removed!
20      VLAN0020                active                             0    This vlan will be removed!
21      VLAN0021                active                             0    This vlan will be removed!
22      VLAN0022                active                             0    This vlan will be removed!
23      VLAN0023                active                             0    This vlan will be removed!
24      VLAN0024                active                             0    This vlan will be removed!
25      VLAN0025                active                             0    This vlan will be removed!
26      VLAN0026                active                             0    This vlan will be removed!
27      VLAN0027                active                             0    This vlan will be removed!
28      VLAN0028                active                             0    This vlan will be removed!
29      VLAN0029                active                             0    This vlan will be removed!
30      VLAN0030                active                             0    This vlan will be removed!
31      VLAN0031                active                             0    This vlan will be removed!
32      VLAN0032                active                             0    This vlan will be removed!
33      VLAN0033                active                             0    This vlan will be removed!
34      VLAN0034                active                             0    This vlan will be removed!
35      VLAN0035                active                             0    This vlan will be removed!
36      VLAN0036                active                             0    This vlan will be removed!
37      VLAN0037                active                             0    This vlan will be removed!
38      VLAN0038                active                             0    This vlan will be removed!
39      VLAN0039                active                             0    This vlan will be removed!
40      VLAN0040                active                             0    This vlan will be removed!
41      VLAN0041                active                             0    This vlan will be removed!
42      VLAN0042                active                             0    This vlan will be removed!
43      VLAN0043                active                             0    This vlan will be removed!
44      VLAN0044                active                             0    This vlan will be removed!
45      VLAN0045                active                             0    This vlan will be removed!
46      VLAN0046                active                             0    This vlan will be removed!
47      VLAN0047                active                             0    This vlan will be removed!
48      VLAN0048                active                             0    This vlan will be removed!
500     BBTV-500                active                             0    This vlan will be removed!
501     BBTV-501                active                             0    This vlan will be removed!
502     BBTV-502                active                             0    This vlan will be removed!
503     BBTV-503                active                             0    This vlan will be removed!
========================================
(cat_scripts) Claudias-iMac:nornir-config claudia$

```