# Topological Attacks

# Relay Attack

## Step1: Have the floodlight running

```bash
java -jar /target/floodlight.jar
```

## Step 2: Create Topology

This will create a simple tree topology

```bash
sudo mn --topo=tree,2 --mac --controller=remote,ip=127.0.0.1,port=6653 --switch ovsk,protocols=OpenFlow13
```

verify it was connected by using pingall on mini net

```bash
pingall 
```

next add a link between h1 and h4 which will be invisible to the controller 

```bash
py net.addLink(h1,h4)
```

### Step 3: Run Script

I use scapy for sniffing and forwarding. For now it forwarding all package, next step is to figure out which those are actually working so we can do injection attack

run these in mininet to open xterm for h1 and h4

```bash
xterm h1
xterm h4
```

in xterm for h1

```bash
chmod +x relay_h1.py #make it executable
./relay_h1.py #start the script
```

in xterm for h4

```bash
chmod +x relay_h4.py #make it executable
./relay_h4.py #start the script
```

Give it couple second for next round of LLDP propagation, go to the GUI interface of floodlight localhost:8080/ui/index.html, you should see a fake link created between two switches

![Untitled](Topological%20Attacks%20d3514ba31c7a4557ab0acf872d0ddb26/Untitled.png)

## Stopping Attack

After stopping the attack the topology recoved

why there is an extra host? 

![Untitled](Topological%20Attacks%20d3514ba31c7a4557ab0acf872d0ddb26/Untitled%201.png)