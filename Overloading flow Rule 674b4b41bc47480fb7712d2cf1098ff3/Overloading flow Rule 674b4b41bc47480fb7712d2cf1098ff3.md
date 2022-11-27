# Overloading flow Rule

The goal is to add flow rule to the switch and see how that impact the latency of LLDP packet.

# Environment

- Python 3.9
- Floodlight v1.2
- mininet 2.3.1b1
- Ubuntu **22.04.1 LTS**

# Network Topology

![Untitled](Overloading%20flow%20Rule%20674b4b41bc47480fb7712d2cf1098ff3/Untitled.png)

h2 is constantly ping h4 and h4 will also change the ip address every time. In order to install new flow rule into S1 and S2

# Executing

Have floodlight running first

In my environment the floodlight is running at 127.0.0.1:6653

```bash
sudo ./flow_rule_overload.py
```

You can also change the frequency in the code by yourself which indicating ping/sec 

There is two way you can check flow rule on each switch, you can either use this command in mininet CLI to check flow rule on s1

```bash
sh ovs-ofctl dump-flows s1
```

This command will just return number of line, subtract by 1 is the number of flow rule on the switch 

```bash
sh ovs-ofctl dump-flows s2 | wc -l
```

# Example

First lets take look at sending 10 pings every sec

```bash
sudo ./flow_rule_overload.py
```

you should see output 

```bash
le_overload.py 
[sudo] password for lamonkey: 
*** Adding controller
*** Add s1
*** Add h1 and h2 to s1
*** Attach h3 h4 host to s2
*** Starting network
*** Configuring hosts
h1 h2 h3 h4 
*** Starting switches
*** h2 begin install flowrule on s1 and s2
*** Starting CLI:
**** overloading
```

Then run 

```bash
sh ovs-ofctl dump-flows s2 | wc -l
```

```bash
98
```

which indicate there is 97 flow rule on switch 

also you can check floodlight gui for s1

![Untitled](Overloading%20flow%20Rule%20674b4b41bc47480fb7712d2cf1098ff3/Untitled%201.png)

Next we try 100 ping per sec 

![Untitled](Overloading%20flow%20Rule%20674b4b41bc47480fb7712d2cf1098ff3/Untitled%202.png)

there is 650 flow rule installed this time.