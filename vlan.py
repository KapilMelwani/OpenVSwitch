import vswitch

#borramos configuracion anterior
vswitch.ovs_vsctl_del_bridge("br0")
#creamos el bridge br0
vswitch.ovs_vsctl_add_bridge("br0")

#anadimos interfaces administrativas
vswitch.ovs_vsctl_admin_port("br0","vlan10","10")
vswitch.ovs_vsctl_set_admin("vlan10","internal")
vswitch.ovs_vsctl_admin_port("br0","vlan20","20")
vswitch.ovs_vsctl_set_admin("vlan20","internal")
vswitch.ifconfig("192.168.0.10/24","vlan10")
vswitch.ifconfig("192.168.1.10/24","vlan20")

#anadimos las interfaces al bridge
vswitch.ovs_vsctl_add_port_to_bridge("br0","eth2")
vswitch.ovs_vsctl_add_port_to_bridge("br0","eth3")
vswitch.ovs_vsctl_add_port_to_bridge("br0","eth4")
vswitch.ovs_vsctl_add_port_to_bridge("br0","eth5")

#metemos los vpcs a vlan 10 y 20
vswitch.ovs_vsctl_set("Port","eth2","tag",None,"10")
vswitch.ovs_vsctl_set("Port","eth3","tag",None,"10")
vswitch.ovs_vsctl_set("Port","eth4","tag",None,"20")
vswitch.ovs_vsctl_add_trunk_port("eth5","trunks=10,20")
#vswitch.ovs_vsctl_set("Port","eth5","tag",None,"20")
