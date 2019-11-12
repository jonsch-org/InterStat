# InterStat

<b><h3>Explanation</h3></b>
<b>InterStat</b> is a simple python script for saving the output of the current interface status from a list of devices. It is using the libary paramiko for building up a ssh connection to the network devices (switches, routers,...) which are defined in a list of ip adresses.

After successful connection to a device, the script collect some device informations like privilege mode, paging, brand hostname and of course the interface status. The device information will just printed out to the command line and only the interface status output will be saved to a file called the hostname of the device.

<code>kinkln</code>
