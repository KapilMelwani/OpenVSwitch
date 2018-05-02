import console as Console
from common import *
import netifaces
import re


class Common:
	def __init__(self):
		self.array_long_mask = ["0.","128.0.0.0","192.0.0.0","224.0.0.0","240.0.0.0","248.0.0.0","252.0.0.0","254.0.0.0","255.0.0.0",
		"255.128.0.0","255.192.0.0","255.224.0.0","255.240.0.0","255.248.0.0","255.252.0.0","255.254.0.0","255.255.0.0",
		"255.255.128.0","255.255.192.0","255.255.224.0","255.255.240.0","255.255.248.0","255.255.252.0","255.255.254.0","255.255.255.0",
		"255.255.255.128","255.255.255.254","255.255.255.252","255.255.255.240","255.255.255.248","255.255.255.252","255.255.255.254","255.255.255.255"]
		# Instancia de common.get_console(), primeramente le ponemos este nombre "S1@LisaSwitch:~#"
		self.console = Console.Console("S1~", '#')
		# Nombre del usuario, inicializamos a este nombre
		self.user_name = "S1~"
		# Array que contiene un historial de los comandos escritos
		self.array_history = []
		# Array que contiene el id de las vlan creadas en el sistemas
		self.array_vlan_id = []
		# Array que contiene el nombre de las vlan creadas en el sistema
		self.array_vlan_name = []
		# Array que contiene el listado de interfaces excepto la loopback
		self.array_interfaces_all = ["eth0","eth1","eth2","eth3","eth4"]
       		self.array_interfaces = []
        	self.array_interfaces_vlan = []
       		self.array_ip_vlan = []
       		self.multi = False
       		self.initial = 0
        	self.final = 0
        	self.default_counter = 0
        	self.control_counter_mode_access = 0
        	self.control_counter_mode_trunk = 0
        	self.array_multi_interface = []
		self.up_down_interface = []
        	self.update_interfaces()
		for i in range(0,len(self.array_interfaces)):
		    self.up_down_interface.append("Down")


	def get_multi(self):
		return self.multi
	def get_item_up_down_interface(self,index):
		return self.up_down_interface[index]
	def set_up_down_interface(self,index):
		self.up_down_interface[index] = "Up"
	def set_multi_to_false(self):
		self.multi = False
	def set_multi_to_true(self):
		self.multi = True
	def get_control_counter_mode_access(self):
		return self.control_counter_mode_access
	def get_control_counter_mode_trunk(self):
		return self.control_counter_mode_trunk
	def set_control_counter_mode_access(self,value):
		self.control_counter_mode_access= value
	def set_control_counter_mode_trunk(self,value):
		self.control_counter_mode_trunk = value
	def set_running_multi(self):
		self.running_multi = not self.running_multi
	def get_len_array_interfaces_vlan(self):
		return len(self.array_interfaces_vlan)
	def get_default_counter(self):
		return self.default_counter
	def normal_append_array_ip_vlan(self,item):
		self.array_ip_vlan.append(item)
	def set_array_ip_vlan(self,index,ip):
		self.array_ip_vlan[index] = ip
	def get_item_array_ip_vlan(self,index):
		return self.array_ip_vlan[index]
	def append_array_interfaces_vlan(self,interface,index):
		for i in range(len(self.array_interfaces_vlan[index])):
			if(self.array_interfaces_vlan[index][i] == interface):
				return
		self.array_interfaces_vlan[index].append(interface)
	def get_item_by_mini_vector(self,index):
		return self.array_interfaces_vlan[index]
	def normal_append_array_interfaces_vlan(self,interface):
		self.array_interfaces_vlan.append(interface)
	def get_item_array_interfaces_vlan(self,index):
		return self.array_interfaces_vlan[index]
	def get_item_array_interfaces(self,index):
		return self.array_interfaces[index]
	def get_len_array_interfaces_vlan(self):
		return len(self.array_interfaces_vlan)
	def get_init(self):
		return self.initial
	def get_len_array_long_mask(self):
		return len(self.array_long_mask)
	def get_final(self):
		return self.final
	def set_init(self,inicio):
		self.initial = inicio
	def set_final(self,final):
		self.final = final
	def remove_eth0_and_eth1(self):
		self.array_interfaces.remove("lo")
	def get_console(self):
		return self.console
	def get_array_long_mask(self,index):
		return self.array_long_mask[index]
	def get_user_name(self):
		return self.user_name
	def get_array_history(self):
		return self.array_history
	def get_array_vlan_id(self):
		return self.get_array_vlan_id
	def get_array_vlan_name(self):
		return self.array_vlan_name
	def get_append_array_history(self):
		return self.array_interfaces
	def append_array_history(self,line):
		self.array_history.append(line)
	def append_vlan_id(self,id):
		self.array_vlan_id.append(id)
	def append_vlan_name(self,name):
		self.array_vlan_name.append(name)
	def get_array_interfaces(self):
		return self.array_interfaces
	def set_user_name(self,name):
		self.user_name = name
	def get_len_vlan_id(self):
		return len(self.array_vlan_id)
	def get_len_interfaces(self):
		return len(self.array_interfaces)
	def get_item_vlan_id(self,index):
		return self.array_vlan_id[index]
	def get_item_vlan_name(self,index):
		return self.array_vlan_name[index]
	def get_item_interfaces(self,index):
		return self.array_interfaces[index]
	def remove_item_vlan_id(self,item):
		self.array_vlan_id.remove(item)
	def remove_item_vlan_name(self,item):
		self.array_vlan_name.remove(item)
	def get_len_array_history(self):
		return len(self.array_history)
	def get_item_array_history(self,index):
		return self.array_history[index]
	def get_item_multi(self,index):
		return self.array_multi_interface[index]
	def set_array_vlan_name(self,index,name):
		self.array_vlan_name[index] = name
	def get_array_multi(self):
		return self.array_multi_interface
	def append_array_multi(self,line):
		self.array_multi_interface.append(line)
	def get_len_multi(self):
		return len(self.array_multi_interface)
	def get_item_array_long_mask(self,index):
		return self.array_long_mask[index]
	def get_len_vlan_name(self):
		return len(self.array_vlan_name)
	def remove_array_multi(self):
		self.array_multi_interface = []
	def reset(self):
		self.array_vlan_id = []
		self.array_history = []
		self.array_vlan_name = []
		self.array_interfaces_vlan = []
		self.array_ip_vlan = []
   	def update_interfaces(self):
        	for i in range(0,len(self.array_interfaces_all)):
            		patron = re.compile('^eth\d+$')
            		if(patron.match(self.array_interfaces_all[i])):
               	 		self.array_interfaces.append(self.array_interfaces_all[i])
