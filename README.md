# InterStat

<b><h3>Supported devices/OS</h3></b>
Cisco (IOS, IOS-XE, NX-OS)<br>
Dell (FTOS)


<b><h3>What is InterStat?</h3></b>
<b>InterStat</b> is a simple python script for saving the output of the current interface status from a list of devices. It is using the libary paramiko for building up a ssh connection to the network devices (switches, routers,...) which are defined in a list of ip adresses.

After successful connection to a device, the script collect some device informations like privilege mode, paging, brand hostname and of course the interface status. The device information will just printed out to the command line and only the interface status output will be saved to a file called the hostname of the device.


<b><h3>How to use?</h3></b>
Before you can start the script, you have to change some parameters. There are three variables you have to look for.

<b><h4>1. SSH-Port </h4></b>
By default the ssh port is <b>22</b>. If you want to take another port for the ssh connection, you have to edit the <code><b>line 38</b></code> which defines the ssh port. Change the <b>22</b> to the port you prefer.

<code>port = ('22')</code>

<b><h4>2. Destination path </h4></b>
By default the destination path is <b>"G:/InterStat/"</b>. Normally you want to costumize the path where the files should be saved. In this reason you have to edit the <code><b>line 41</b></code> which defines the path to the destination directory. Change the path to the directory you prefer.

<code>path = (r'G:/InterStat/')</code>

<b><h4>3. IP-List </h4></b>
By default the ip list for the devices is named <b>"ip_list.txt</b>. Maybe you want to rename the filename. For this case you have to edit the <code><b>line 44</b></code>, <code><b>line 45</b></code> and <code><b>line 57</b></code> which defines the the filename. Change the filename <b>"ip_list.txt</b> you prefer.

<code>with open('ip_list.txt', 'r') as ip:</code><br>
and<br>
<code>ip_list = ip.read().split('\n')</code><br>
and<br>
<code>for ip in ip_list:</code><br>


<b><h3>Step by Step</h3></b>
After you changed the parameters and the directories are defined, you can start the script.

1. First of all you get asked for your credentials to login to the device. There are two options to login. The first credentials you will get asked are your active directory once if you are using RADIUS or any other kind of authentication process. If you are just using local credentials on each device or your active directory login fails, the script will use your local account.  

2. After login the script will open in a for loop the ip list and pick the ip address of the first line. In the next step the ssh connection to the device will be build up. The first try of login will be with the active directory credentials and after that with the local credentials. 

3. In the next step the InterStat.py check if you are still in privilege mode, if not the login will be tried with the ena password you defined at the start.

4. The script will disable the paging function to get the maximum output.

5. To get the hostname of the device the script will find out with the <b>show version</b> command, which brand the device is of. By default the brand could be cisco (IOS, IOS-XE, NX-OS, ...) and dell (Force 10). Depending on which one, the script will prompt the <b>show run | include hostname</b> or <b>show run | find hostname</b> command to pick out the hostname of the device.

6. After that the main function will start his work. The <b>interface status</b> command will be promt and the output will be saved to a textfile with the hostname fo the device as filename to the directory you defined at the start. If this succeed the script will pick the next ip address of the ip list and repeat the process.

The script will end with the last ip address in the ip list.
