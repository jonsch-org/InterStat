import paramiko
import getpass
import time
import os
import sys
import re
import signal

print ('')
print ('')
print ('************************************')
print ('**                                **')
print ('**   InterStat.py by jonsch.org   **')
print ('**                                **')
print ('************************************')
print ('')
print ('')


#define active directory credentials
print ('Your active directory credentials')
adUsername = input('AD-Username: ')
adPassword = getpass.getpass('AD-Password: ')
print ('')

#define local credentials
print ('Your local credentials')
locUsername = input('Local-Username: ')
locPassword = getpass.getpass('Local-Password: ')
print ('')

#define privilege (ena) credential
print ('The privilege (ena) credential')
enaPassword = getpass.getpass('Ena-Password: ')
print ('')

#define ssh port
port = ('22')

#path directory
path = (r'G:/InterStat/')

#ip list
with open('ip_list.txt', 'r') as ip:
        ip_list = ip.read().split('\n')

#graceful keyboardInterrupt
def signal_handler(signal, frame):
    print("\n# Program exiting gracefully")
    socket.close(0)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#main programm
def getStatus():
    for ip in ip_list:
        try:
            print ('# Trying to login to %s' % (ip))
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
                    ssh.slave.send(enaPassword)
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

        except TimeoutError:
            print ('# Timeout: Can not connect to device. Check network reachability.')
            print ('')
            ssh.close()

        except:
            print ('# Authentication failed: Can not login with selected credentials.')
            print ('# Trying to login with local credentials...')
            try:
                #create ssh session with active directory credentials
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
                
            except:
                print ('# Authentication failed: Can not login with locale credentials.')
                print ('')
                ssh.close()
            
    print ('Script ran successfully. Script closed.')
getStatus()
