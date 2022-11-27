#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from multiprocessing import Process
import time
import ipaddress
cli = None
def run_cli(net):
    global cli 
    cli = CLI(net)
    net.stop()

def ping_command(host, target):
    ping_command = f"ping -c 1 -i 0.01 {target} 2>&1 | awk -F '/' "
    filter = 'END{ print (/^rtt/? "OK "$5" ms":"FAIL") }'
    filter_command = f"'{filter}'"
    result = host.cmd(ping_command + filter_command)
    return result
#host ping target and store reuslt in results
def check_delay(host, target ,results):
    while(True):
        # ping -qc1 google.com 2>&1 | awk -F'/' 'END{ print (/^rtt/? "OK "$5" ms":"FAIL") }'
        ping_command = f"ping -c 1 -i 0.01 {target} 2>&1 | awk -F '/' "
        filter = 'END{ print (/^rtt/? "OK "$5" ms":"FAIL") }'
        filter_command = f"'{filter}'"
        result = host.cmd(ping_command + filter_command)
        print(result)
        #results.push(host.cmd(f'ping h3 -c 1 i 0.01'))

    
#ping different host every time to install flow rule on switch
def install_flow_rule(host,host2,freq):
    info(f'**** overloading\n')
    time_to_sleep = 1/freq
    while True:
        net4 = ipaddress.ip_network('10.0.0.0/8')
        for ip in net4.hosts():
            # info(f'**** change h4 ip to {str(ip)}\n')
            host2.setIP(str(ip))
            result = ping_command(host,ip)
            # print(result)
            time.sleep(time_to_sleep)

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8'
                   )

    info( '*** Adding controller\n' )
    c0 = net.addController("c0", controller=RemoteController, ip='127.0.0.1',port=6653, protocol='tcp')


    info( '*** Add s1\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols=["OpenFlow13"]) 
    info( '*** Add h1 and h2 to s1\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
   

    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols=["OpenFlow10"]) 
    net.addLink(s1,s2)
   
    info(f'*** Attach h3 h4 host to s2\n')
    h3 = net.addHost('h3', cls=Host)
    net.addLink(s2,h3)
    h4 = net.addHost('h4', cls=Host)
    net.addLink(s2,h4)
            

    info( '*** Starting network\n')
    net.build()


    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    return net

def iterate_host_number():
    for i in range(1,50,1):
        pass
        # #start network 
        # net,target_ips = myNetwork(50)
        # h1 = net.getNodeByName('h1')
        # h2 = net.getNodeByName('h2')
        # h3_ip = net.getNodeByName('h3').IP()
        
        # p1 = Process(targe
        
        # t=check_delay,args=[h1,h3_ip,None])
        # p2 = Process(target=install_flow_rule,args=[h2,target_ips])
        # p1.start()
        # p2.start()
        # p1.join()
        # p2.join()

        # #start 
        # #stop
        # net.stop()
        # #
        

if __name__ == '__main__':
    setLogLevel( 'info' )
    net = myNetwork()
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')
    h4 = net.getNodeByName('h4')
    # info( '*** h1 begin checking the latency\n')
    # p1 = Process(target=check_delay,args=[h1,h3.IP(),None])
    info( '*** h2 begin install flowrule on s1 and s2\n')
    p2 = Process(target=install_flow_rule,args=[h2,h4,100])
    # p1.start()
    p2.start()
    # p1.join()
    # with open('flow_rule_log.txt','w') as file:
    cli = CLI(net)
  
    # while cli is None:
    #     print("waiting cli to configure")
    cli.do_sh('ovs-ofctl dump-flows s2 | wc -l')
    # cli.do_sh('sh ovs-ofctl dump-flows s2 | wc -l')
   
    p2.join()
    net.stop()
