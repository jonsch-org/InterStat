# InterStat

<b><h3>What is InterStat?</h3></b>
<b>InterStat</b> is a simple python script for saving the output of the current interface status from a list of devices. It is using the libary paramiko for building up a ssh connection to the network devices (switches, routers,...) which are defined in a list of ip adresses.

After successful connection to a device, the script collect some device informations like privilege mode, paging, brand hostname and of course the interface status. The device information will just printed out to the command line and only the interface status output will be saved to a file called the hostname of the device.

<b><h3>How to use?</h3></b>
Before you can start the script you have to change some parameters. There are three variables you have to look for.

<b><h4>1. SSH-Port </h4></b>
By default the ssh port is <b>22</b>. If you want to take another port for the ssh connection, you have to edit the <code><b>line 33</b></code> which defines the ssh port. Change the <b>22</b> to the port you prefer.

<code>port = ('22')</code>

<b><h4>2. Destination path </h4></b>
By default the destination path is <b>"G:/InterStat/"</b>. Normally you want to costumize the path where the files should be saved. In this reason you have to edit the <code><b>line 36</b></code> which defines the path to the destination directory. Change the path to the directory you prefer.

<code>path = (r'G:/InterStat/')</code>

<b><h4>3. IP-List </h4></b>
By default the ip list for the devices is named <b>"ip_list.txt</b>. Maybe you want to rename the filename. For this case you have to edit the <code><b>line 39</b></code>, <code><b>line 40</b></code> and <code><b>line 52</b></code> which defines the the filename. Change the filename <b>"ip_list.txt</b> you prefer.

<code>with open('ip_list.txt', 'r') as ip:</code><br>
and<br>
<code>ip_list = ip.read().split('\n')</code><br>
and<br>
<code>for ip in ip_list:</code><br>

<b><h3>Step by Step</h3></b>
After you changed the parameters and the directories are defined, you can start the script.

First of all you get asked for your credentials to login to the device. There are two options to login. The first credentials you will get asked are your active directory once if you are using RADIUS or any other kind of authentication process. If you are just using local credentials on each device or your active directory login fails, the script will use your local account.  

After login the script will open in a for loop the ip list and pick the ip address of the first line. In the next step the ssh connection to the device will be build up. The first try of login will be with the active directory credentials and after that with the local credentials. 

In the next step the InterStat.py check if you are still in privilege mode, if not the login will be tried with the ena password you defined at the start.

