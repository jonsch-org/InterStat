import paramiko
import getpass
import time
import os
import sys
import re
import signal


#define active directory credentials
adUsername = input('AD-Username: ')
adPassword = getpass.getpass('AD-Password: ')

#define local credentials
locUsername = input('Local-Username: ')
locPassword = getpass.getpass('Local-Password: ')

#define ssh port
port = ('22')

#define path of directory
path = (r'G:/InterStat/')

#ip list of devices
with open('ip_list.txt', 'r') as ip:
        ip_list = ip.read().split('\n')

#graceful handling of keyboardInterruption
def signal_handler(signal, frame):
    print("\n# Program exiting gracefully")
    socket.close(0)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#main programm
def getStatus():
    for ip in ip_list:
        try:
            print ('# Trying to log in to %s' % (ip))
            #create ssh session with active directory credentials
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                        ip,
                        port = port,
                        username = adUsername,
                        password = adPassword,
                        look_for_keys = False,
                        allow_agent = False)
            ssh.slave = ssh.invoke_shell()
            print ('# Logged in with AD credentials')

            #check ena
            def checkEna():
                time.sleep(3)
                ssh.slave.send('\n')
                time.sleep(1)
                enaOutput = ssh.slave.recv(9999).decode('UTF-8')
                if '#' in enaOutput:
                    print ('# Logged in privilege mode')
                else:
                    print ('# Trying to log in privilege mode')
                    ssh.slave.send('ena\n')
                    time.sleep(1)
                    ssh.slave.send(locPassword)
                    ssh.slave.send('\n')
                    time.sleep(1)
                    enaOutput = ssh.slave.recv(9999).decode('UTF-8')
                    if '#' in enaOutput:
                        print ('# Logged in privilege mode')
                    else:
                        print ('# Can not log in privilege mode, script closed')
                        ssh.close()
            checkEna()

            #disable paging
            def disPage():
                ssh.slave.send('term len 0\n')
                print ('# Paging disabled')
                ssh.slave.recv(9999).decode('UTF-8')
                time.sleep(1)
            disPage()

            #lookup for hostname
            def checkHost():
                global hostname
                ssh.slave.send('show version\n')
                time.sleep(1)
                brandOutput = ssh.slave.recv(9999).decode('UTF-8')
                if re.search(r'Cisco', brandOutput) or re.search(r'cisco', brandOutput):
                    print ('# Brand of device is Cisco')
                    try:
                        ssh.slave.send('show run | include hostname\n')
                        time.sleep(5)
                        hostOutput = ssh.slave.recv(9999).decode('UTF-8')
                        hostname = hostOutput.split('\n')[1].split(' ')[1]
                        print ('# Hostname of device is %s' % (hostname.strip()))
                    except:
                        print ('# Can not find out hostname, script closed')
                        ssh.close()
                elif re.search(r'Dell', brandOutput) or re.search(r'dell', brandOutput): 
                    print ('# Brand of device is Dell')
                    try:
                        ssh.slave.send('show run | find hostname\n')
                        time.sleep(5)
                        hostOutput = ssh.slave.recv(9999).decode('UTF-8')
                        hostname = hostOutput.split('\n')[1].split(' ')[1]
                        print ('# Hostname of device is %s' % (hostname.strip()))
                    except:
                        print ('# Can not find out hostname, script closed')
                        ssh.close()
            checkHost()

            #inter status
            def interStat():
                global statusOutput
                ssh.slave.send('show inter status\n')
                print ('# Lookup for inter status')
                time.sleep(2)
                statusOutput = ssh.slave.recv(9999).decode('UTF-8')
            interStat()

            #inter status file
            def writeStat():
                print ('# Write output of inter status to %s%s.txt' % (path, hostname.strip()))
                time.sleep(1)
                for line in statusOutput.splitlines():
                    statFile = open('%sInterStatus-%s.txt' % (path, hostname.strip()), 'a')
                    statFile.write(line)
                    statFile.write('\n')
                    statFile.close()
                print ('# Inter status output saved to %s%s.txt' % (path, hostname.strip()))
                print ('')
            writeStat()
            ssh.close()

        except:
            #create ssh session with local credentials
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                        ip,
                        port = port,
                        username = locUsername,
                        password = locPassword,
                        look_for_keys = False,
                        allow_agent = False)
            ssh.slave = ssh.invoke_shell()
            print ('# Logged in with local credentials')

            #check ena
            def checkEna():
                time.sleep(3)
                ssh.slave.send('\n')
                time.sleep(1)
                enaOutput = ssh.slave.recv(9999).decode('UTF-8')
                if '#' in enaOutput:
                    print ('# Logged in privilege mode')
                else:
                    print ('# Trying to log in privilege mode')
                    ssh.slave.send('ena\n')
                    time.sleep(1)
                    ssh.slave.send(locPassword)
                    ssh.slave.send('\n')
                    time.sleep(1)
                    enaOutput = ssh.slave.recv(9999).decode('UTF-8')
                    if '#' in enaOutput:
                        print ('# Logged in privilege mode')
                    else:
                        print ('# Can not log in privilege mode, script closed')
                        ssh.close()
            checkEna()

            #disable paging
            def disPage():
                ssh.slave.send('term len 0\n')
                print ('# Paging disabled')
                ssh.slave.recv(9999).decode('UTF-8')
                time.sleep(1)
            disPage()

            #lookup for hostname
            def checkHost():
                global hostname
                ssh.slave.send('show version\n')
                time.sleep(1)
                brandOutput = ssh.slave.recv(9999).decode('UTF-8')
                if re.search(r'Cisco', brandOutput) or re.search(r'cisco', brandOutput):
                    print ('# Brand of device is Cisco')
                    try:
                        ssh.slave.send('show run | include hostname\n')
                        time.sleep(5)
                        hostOutput = ssh.slave.recv(9999).decode('UTF-8')
                        hostname = hostOutput.split('\n')[1].split(' ')[1]
                        print ('# Hostname of device is %s' % (hostname.strip()))
                    except:
                        print ('# Can not find out hostname, script closed')
                        ssh.close()
                elif re.search(r'Dell', brandOutput) or re.search(r'dell', brandOutput): 
                    print ('# Brand of device is Dell')
                    try:
                        ssh.slave.send('show run | find hostname\n')
                        time.sleep(5)
                        hostOutput = ssh.slave.recv(9999).decode('UTF-8')
                        hostname = hostOutput.split('\n')[1].split(' ')[1]
                        print ('# Hostname of device is %s' % (hostname.strip()))
                    except:
                        print ('# Can not find out hostname, script closed')
                        ssh.close()
            checkHost()

            #inter status
            def interStat():
                global statusOutput
                ssh.slave.send('show inter status\n')
                print ('# Lookup for inter status')
                time.sleep(2)
                statusOutput = ssh.slave.recv(9999).decode('UTF-8')
            interStat()

            #inter status file
            def writeStat():
                print ('# Write output of inter status to %s%s.txt' % (path, hostname.strip()))
                time.sleep(1)
                for line in statusOutput.splitlines():
                    statFile = open('%sInterStatus-%s.txt' % (path, hostname.strip()), 'a')
                    statFile.write(line)
                    statFile.write('\n')
                    statFile.close()
                print ('# Inter status output saved to %s%s.txt' % (path, hostname.strip()))
                print ('')
            writeStat()
            ssh.close()
    print ('Script ran successfully. Script closed.')
getStatus()
