#!/bin/sh

# to be executed on the devstack node once #
openstack network create --disable-port-security --share --project admin sdl-mgmt 
openstack subnet create --network sdl-mgmt --subnet-range 192.168.168.0/24 --gateway 0.0.0.0 --allocation-pool start=192.168.168.2,end=192.168.168.254 sdl-mgmt-subnet
openstack router create sdl-router
openstack router set --external-gateway public sdl-router
openstack port create --fixed-ip subnet=sdl-mgmt-subnet,ip-address=192.168.168.1 rt-sdl-mgmt --network sdl-mgmt
openstack --debug router add port sdl-router rt-sdl-mgmt

