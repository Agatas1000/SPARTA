#!/bin/bash

# to be executed on the devstack node to enable the routing to the management network #
id=$(openstack router list | grep sdl-router | cut -d\| -f 2 | cut -c 2-); id=$(ip netns list | grep $id | cut -d\( -f 1)
ip=$(ip netns exec $id ifconfig | grep 172.24 | cut -d\: -f 2 | cut -d' ' -f 1)
rid=$(ip netns list | grep $id | cut -d\( -f 1)

echo $id,$ip,$rid

route add -net 192.168.168.0/24 gw $ip
iptables --policy FORWARD ACCEPT
iptables -t nat  -A POSTROUTING -s 172.24.4.0/24 -j MASQUERADE

ip netns exec $rid iptables -t nat -I POSTROUTING 2 -s 172.24.4.0/24 -j SNAT --to 192.168.168.1
ip netns exec $rid iptables -t nat -A PREROUTING -d 169.254.169.254 -p tcp -m tcp --dport 80 -j DNAT --to-destination 172.24.4.1:8775
ip netns exec $rid iptables -t nat -A PREROUTING -p tcp -d 192.168.168.1 --dport 80 -j DNAT --to-destination 172.24.4.1

