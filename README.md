# mininet-pox-openflow
Use the NOX/POX controller platform for programming an OpenFlow-based SDN-enabled switch. The goal is to supply  ow rules to the switch's  ow table to implement a L2 learning switching functionality.

## How to run
Go to https://github.com/mininet/mininet/releases/ and download the lastest recommended VM image. As of 2022-11-20, release 2.3.0 is the lastest, and its recommended VM image is `mininet-2.3.0-210211-ubuntu-20.04.1-legacy-server-amd64-ovf.zip`.

Once the VM is installed, the credentials to login are user: `mininet` password: `mininet`. Ensure that you can connect to the VM from the host computer.

When in the home directory, place the files into their respective folders `~/mininet` and `~/pox` by using software such as FileZilla or manually creating the files and copying its contents.

The directory should be as follows:

    ~/
        mininet/
            ...
           custom_tree_topology.py
        pox/
            ...
            custom_l2_learning.py

Once the files are in their directories, open two SSH sessions.

In the first window, make your way to the `~/pox` directory and run the file.

`cd ~/pox`

`./pox.py custom_l2_learning`

In the second window, make your way to the `~/mininet` directory and run the file.

`cd ~/mininet`

`sudo python -u custom_tree_topology.py`

If there is an issue getting the mininet file working, you might need reset interface pair files, and try again.

`sudo mn -c`