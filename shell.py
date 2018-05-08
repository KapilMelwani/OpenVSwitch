#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
/etc/init.d/openvswitch-switch restart
-Configurar nombre del switch
-Guardar configuracion: write memory
- CREAR VLAN:
	S1(config)# vlan 20
	S1(config-vlan)# name profesores
	S1(config-vlan)# exit
- ASIGNAR PUERTOS DE ACCESO
	S1(config)# interface eth2
	S1(config-if)# switchport mode access
	S1(config-if)# switchport access vlan 10
	S1(config-if)# no shutdown
	S1(config-if)# end

- CONFIGURAR ENLACES TRONCALES
	S1(config)# interface eth0
	S1(config-if)# switchport mode trunk
	S1(config-if)# switchport trunk allowed vlan 10,20
	S1(config-if)# no shutdown
	S1(config-if)# end

- ASIGNAR INTERFAZ DE ADMIN EN LA VLAN 20
	S1(config)# interface vlan 20
	S1(config)# ip address 192.168.1.3 255.255.255.

'''

import command as Command

import sys
import subprocess
import os
import os.path
import netifaces
import re
import vswitch
from common import *

common = Common()

class ConnectingInterfaces:
    def __init__(self):
        self.connect = ""
    def set_connect(self,data):
        self.connect = data
    def get_connect(self):
        return self.connect

connecting_interfaces = ConnectingInterfaces()

class ConnectingVlan:
	def __init__(self):
		self.connect_vlan = 0 #nos olvidamos de esta
		self.connect_vlan_id_interface_vlan = ""
		self.connect_vlan_id_switchport_vlan = ""
		self.interface = ""
	def append_array_interfaces_vlan(self):
		self.array_interfaces_vlan.append()
	def set_connect_vlan(self,index_vlan):
		self.connect_vlan = index_vlan #####################nos olvidamos tb
	def get_connect_vlan(self):
		return self.connect_vlan
	def set_connect_vlan_interface(self,interface): # Interfaz para interface eth0 para el switchport
		self.interface = interface
	def get_connect_vlan_interface(self): # Cambia valor de interface
		return self.interface
	def set_connect_vlan_id_interface_vlan(self,id): # VLAN ID para interface vlan [id]
		self.connect_vlan_id_interface_vlan = id
	def get_connect_vlan_id_interface_vlan(self): # retorna valor VLAN ID Para interface vlan [id]
		return self.connect_vlan_id_interface_vlan
	def set_connect_vlan_id_switchport_vlan(self,id): # toma el valor de la vlan id puesto en switchport access vlan [ID]
		self.connect_vlan_id_switchport_vlan = id
	def get_connect_vlan_id_switchport_vlan(self): # retorna el valor de la vlan id puesto en switchport access vlan [ID]
		return self.connect_vlan_id_switchport_vlan

connecting_vlan = ConnectingVlan()


class CargandoFichero:
    def __init__(self):
        self.cargando_fichero = False
    def set_cargando(self):
        self.cargando_fichero = not self.cargando_fichero
    def get_cargando(self):
        return self.cargando_fichero

cargando = CargandoFichero()

class RunMulti:
	def run_multi(self):
		cargando.set_cargando()
		common.set_multi_to_false()
		for i in range(common.get_init(),common.get_final()+1):
			if(common.console.prompt == "(config)"):
				line = "interface " + common.get_item_array_interfaces(i)
				common.get_console().walk(line,0,run=True,full_line=line)
				for j in range(0,common.get_len_multi()):
					common.get_console().walk(common.get_item_multi(j),0,run=True,full_line=common.get_item_multi(j))
			else:
				print Colors.FAIL + "[ERROR]" + Colors.ENDC + "algo ha ido mal"
				cargando.set_cargando()
				return
		print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Applied all interface configuration")
		cargando.set_cargando()
		common.remove_array_multi()


run = RunMulti()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#common.remove_eth0_and_eth1()
# Falta comprobar con expresiones regulares la mascara y la ip
class IPAdminInterface(Command.Command):
	def args(self):
		return ["ip address"]
	def testing_ip(self,ip):
		ip_without_point = ip.replace("."," ")
		ip_for_test = ip_without_point.split()
		for i in range(len(ip_for_test)):
			if (int(ip_for_test[i]) < 0) or (int(ip_for_test[i]) > 255):
				return False
		return True
	def run(self,line):
		args = line.split()
		if(common.get_console().prompt == "(config-if)"):
			if(len(args) < 2):
				print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: ip address [ip/mask]")
				return
			if(args[1:][0] == "address"):
				patron_ip = re.compile('^(\d{1,3}.){3}\d{1,3}$')
				patron_short_mask = re.compile('^\d{1,2}$')
				if(len(args[2:]) == 0):
					print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Not IP/MASK specified")
					return
				ip_address = args[2:][0]
				str_ip_address = str(ip_address).strip('[]').strip('\'"')
				address_mask = str_ip_address.replace("/"," ")
				address_mask = address_mask.split()
				test_ip = self.testing_ip(address_mask[0])
				if(test_ip == False):
					print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Wrong IP Address")
					return
				if(patron_ip.match(address_mask[0])):
					if(len(address_mask) == 1):
						if(len(args[2:]) != 2):
							print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "You must specified netmask")
							return
						else:
							if(len(args[2:]) == 2):
								mask = args[3]
								str_mask = str(mask).strip('[]').strip('\'"')
								if(str_mask.find('.') > 0):
									short_mask = 0
									for i in range(common.get_len_array_long_mask()):
										if(str_mask == common.get_item_array_long_mask(i)):
											for j in range(0,common.get_len_array_long_mask()):
												if(str_mask == common.get_item_array_long_mask(i)):
													short_mask = str(i)
											print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "ip address: " + str_ip_address + " mask: " + str_mask + " added")
											vlan_str = "vlan" + connecting_vlan.get_connect_vlan_interface()
											vswitch.ovs_vsctl_admin_port("br0",vlan_str,connecting_vlan.get_connect_vlan_interface())
											vswitch.ovs_vsctl_set_admin(vlan_str,"internal")
											print vswitch.ifconfig(str_ip_address + '/' + short_mask,vlan_str)
											print vswitch.iplink(vlan_str,"up")
											for k in range(0,common.get_len_vlan_id()):
												if(common.get_item_vlan_id(k) == connecting_vlan.get_connect_vlan_id_interface_vlan()):
													common.set_array_ip_vlan(k,str_ip_address + "/" + short_mask)
											common.append_array_history(line)
											return
									print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Wrong long mask")
								else:
									print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Wrong long mask")
					else:
						if(patron_short_mask.match(address_mask[1])):
							mask = address_mask[1]
							if(int(mask) > common.get_len_array_long_mask() or int(mask) < 0):
								print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Wrong short mask")
								return
							long_mask = common.get_array_long_mask(int(mask))
							vlan_str = "vlan" + connecting_vlan.get_connect_vlan_interface()
							vswitch.ovs_vsctl_admin_port("br0",vlan_str,connecting_vlan.get_connect_vlan_interface())
							vswitch.ovs_vsctl_set_admin(vlan_str,"internal")
							print vswitch.ifconfig(str_ip_address,vlan_str)
							print vswitch.iplink(vlan_str,"up")
							print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "ip address: " + str_ip_address + " mask: " + long_mask + " added")
							for k in range(0,common.get_len_vlan_id()):
								if(common.get_item_vlan_id(k) == connecting_vlan.get_connect_vlan_id_interface_vlan()):
									common.set_array_ip_vlan(k,address_mask[0] + "/" + address_mask[1])

							common.append_array_history(line)
				else:
					print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Not a valid IP Address")
			else:
				print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: ip address [ip/mask]")
		else:
			print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command Use")

# Clase ConfigureInterface la cual nos sirve para acceder a la configuracion
# de una de las interfaces que tenga el switch. Previamente, comprobamos la existencia
# de dicha interfaz

# InterfaceVlan es una clase que nos permite acceder a la configuracion de una
# vlan existente. La propia funcion run() comprueba previamente que la vlan
# se haya creado
# Falta comprobar la existencia de la interfaz
class ConfigureInterface(Command.Command):
	def testing_interface(self,line):
		patron = re.compile('eth\d+-eth\d+$')
		if(patron.match(line)):
			return True
		return False

	def args(self):
		array = []
		for i in range(0,common.get_len_interfaces()):
			array.append(common.get_item_interfaces(i))
		array.append("range")
		return array
	def run(self,line):
		if(common.get_console().prompt == "(config)"):
			args = line.split()
			if(len(args) < 2):
				print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: interface vlan [vlan id]")
				return
			if(args[1] == "range"):
				common.set_multi_to_true()
				if(not self.testing_interface(args[2])):
					common.set_multi_to_false()
					print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "interface range ethX-ethY")
					return
				argument = args[2].replace('-',' ')
				interface_range = argument.split()
				common.set_init(-1)
				common.set_final(-1)
				for i in range(0,common.get_len_interfaces()):
					if(interface_range[0] == common.get_item_interfaces(i)):
						common.set_init(i)
					else:
						if(interface_range[1] == common.get_item_interfaces(i)):
							common.set_final(i)
				if(common.get_init() == -1 or common.get_final() == -1):
					print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "This range doesnt exist")
					return
				common.get_console().prompt = "(config-if)"
				if(cargando.get_cargando() == False):
					common.get_console().loop()
			else:
				argument = args[1:][0]
				str_argument = str(argument).strip('[]').strip('\'"')
				if(str_argument == "vlan"):
					if(len(args[2:]) == 0):
						print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: interface vlan [vlan id]")
						return
					vlan_id = args[2:]
					str_vlan_id_interface = args[2]
					connecting_vlan.set_connect_vlan_id_interface_vlan(str_vlan_id_interface) #################################################################
					testing_vlan_id_interface = False
					if(common.get_len_vlan_id()!= 0):
						for i in range(0,common.get_len_vlan_id()):
							if(str_vlan_id_interface == common.get_item_vlan_id(i)):
								testing_vlan_id_interface = True
								connecting_vlan.set_connect_vlan_interface(str_vlan_id_interface)
								print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Configuring vlan " + str_vlan_id_interface)
								common.append_array_history(line)
								common.get_console().prompt = "(config-if)"
								if(cargando.get_cargando() == False):
									common.get_console().loop()
								break
							else:
								if(i == common.get_len_vlan_id()-1 and not testing_vlan_id_interface):
									print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: interface vlan [id]")
									return
					else:
						print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "No vlan's created")
						return
				else:
					check = False
					for i in range (0,common.get_len_interfaces()):
						if(common.get_item_interfaces(i) == argument):
							check = True
							connecting_interfaces.set_connect(argument)
							common.append_array_history(line)
							common.get_console().prompt = "(config-if)"
							connecting_vlan.set_connect_vlan_interface(argument)
							if(cargando.get_cargando() == False):
								common.get_console().loop()
							break
					if(not(check)):
						print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Interface " + argument + " doesn't exist")
						return
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")
			return




# Clase SwitchPort, en esta clase debemos tener en cuenta que el comando SwitchPort
# puede seguir de:
# 	- switchport mode access
# 	- switchport access vlan [id]
# 	- switchport mode trunk
# 	- switchport trunk allowed vlan [id]
# Por tanto hemos tenido que realizar un cpdigo que aborde todas estas posibilidades
# Ademas, hay que tener en cuenta tambien que antes de poder hacer:
# 	- switchport access vlan [id]
# 	- switchport trunk allowed vlan [id]
# Debemos hacer un:
# 	- switchport mode access
# 	- switchport mode trunk
# Tambien tenemos en cuenta que las vlan que se pongan en [id] ya existan


# Falta comprobar que primero se haga mode access o trunk y despues la siguiente

class Switchport(Command.Command):

	def args(self):
		return ["mode access","mode trunk","trunk allowed vlan","access vlan","access","trunk","allowed vlan"]
	def run(self,line):

		if(common.get_console().prompt == "(config-if)"):
			args = line.split()
			if(len(args) > 1):
				options = args[1:][0]
				important_mode = ""
				str_options = str(options).strip('[]').strip('\'"')
				if (str_options == "mode"):
					mode = args[2:]
					str_mode = str(mode).strip('[]').strip('\'"')
					if(str_mode == "trunk"):
						important_mode = "trunk"
						if(common.get_multi() == True):
							common.append_array_multi(line)
						else:
							common.append_array_history(line)
						common.set_control_counter_mode_trunk(1)
					else:
						if(str_mode == "access"):
							important_mode = "access"
							if(common.get_multi() == True):
								common.append_array_multi(line)
							else:
								common.append_array_history(line)
							common.set_control_counter_mode_access(1)
						else:
							print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")
							return
				else:
					if(str_options == "trunk"):
						if(common.get_control_counter_mode_trunk() == 0):
							print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "first switchport mode trunk")
							return
						if(len(args[1:]) == 4):
							if (len(args[2:]) > 0) and (args[2:][0] == "allowed") and (args[2:][1] == "vlan"):
								allowed_vlan = args[4:]
								allowed_vlan_divide = str(args[4:]).strip('[]').strip('\'"')
								allowed_vlan_test = allowed_vlan_divide.replace(',',' ')
								vlan_for_testing = allowed_vlan_test.split()
								testing_vlan = False
								for i in range(0,len(vlan_for_testing)):
									testing_vlan = False
									for j in range(0,common.get_len_vlan_id()):
										if(vlan_for_testing[i] == common.get_item_vlan_id(j)):
											testing_vlan = True
											break
									if(not(testing_vlan)):
										print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "One or more vlans specified are not created")
										return
								str_allowed_vlan = str(allowed_vlan).strip('[]').strip('\'"')
								if(common.get_multi() == True):
									common.append_array_multi(line)
								else:
									common.append_array_history(line)
									vswitch.ovs_vsctl_add_trunk_port(connecting_interfaces.get_connect(),"trunks=%s" % allowed_vlan_divide)
								print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Allowed VLAN's = " + allowed_vlan_divide + " in port " + connecting_interfaces.get_connect())
								common.set_control_counter_mode_trunk(0)
							else:
								print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "first switchport mode [trunk|access]")
						else:
							print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: switchport trunk allowed vlan [vlan1],[vlan2]")
					else:
						if(str_options == "access"):
							if(common.get_control_counter_mode_access() == 0):
								print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "first switchport mode access")
								return
							if(len(args[1:]) == 3):
								if (args[2:][0] == "vlan"):
									access_vlan = args[3:]
									str_access_vlan = str(access_vlan).strip('[]').strip('\'"')
									connecting_vlan.set_connect_vlan_id_switchport_vlan(str_access_vlan)
									check = False
									for i in range(0,common.get_len_vlan_id()):
										if(common.get_item_vlan_id(i) == str_access_vlan):
											check = True
											if(common.get_multi() == True):
												common.append_array_multi(line)
											else:
												common.append_array_history(line)
												common.append_array_interfaces_vlan(connecting_vlan.get_connect_vlan_interface(),i)
												vswitch.ovs_vsctl_set("Port",connecting_interfaces.get_connect(),"tag",None,str_access_vlan)
												common.set_control_counter_mode_access(0)
									if(not check):
										print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "this vlan doesnt exist")
								else:
									print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: switchport access vlan [vlan id]")
							else:
								print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: switchport access vlan [vlan id]")
						else:
							print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "first switchport mode [trunk|access]")
			else:
				print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")


class Reload(Command.Command):
	def run(self,line):
		if(common.get_console().prompt == common.get_user_name()):
			print("Reloading Bridge")
			common.reset()
			vswitch.ovs_vsctl_del_bridge("br0")
			vswitch.ovs_vsctl_add_bridge("br0")
			for i in range(0,common.get_len_interfaces()):
				vswitch.ovs_vsctl_add_port_to_bridge("br0",common.get_item_interfaces(i))
		else:
			print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")

# Clase Switchname nos sirve para cambiar el nombre de usuario del switch al que nosotros
# queramos
class Hostname(Command.Command):
    name = []
    def run(self, line):
		if(common.get_console().prompt == common.get_user_name()):
			args = line.split()
			Command.Command = ['hostname']
			if len(line) > 1:
				name = args[1:]
				common.get_console().prompt = str(name).strip('[]').strip('\'"')
				common.set_user_name(str(name).strip('[]').strip('\'"'))
				print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "New session has been opened with name " + str(name).strip('[]').strip('\'"'))
				common.get_console().loop()
				if(cargando.get_cargando() == False):
					common.get_console().loop()
					print (Colors.OKBLUE + "Session closed" + Colors.ENDC)
			else:
				print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")


    def get_name(self):
        return self.name

# Clase ConfigureSwitch nos sive para acceder al (config) de nuestro switch
class ConfigureSwitch(Command.Command):
    configure_counter = 0
    def run(self,line):
		if(common.get_console().prompt == common.get_user_name()):
			common.append_array_history(line)
			common.get_console().prompt = "(config)"
			if(cargando.get_cargando() == False):
				common.get_console().loop()
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")
			return

# Clase VLAN la cual nos permite crear las VLAN que nosotros queramos siempre
# y cuando estemos dentro de la configuracion del switch. Una vez creada la Vlan
# accederemos a la configuracion de la misma para ponerle el nombre que queramos
class Vlan(Command.Command):
	def args(self):
		return ["vlan"]
	def testing_vlan(self,id):
		patron = re.compile('^\d+$')
		if(patron.match(str(id))):
			return True
		return False
	vlan_id = []
	def run(self,line):
		if common.get_console().prompt == "(config)":
			args = line.split()
			if(len(args) < 2):
				print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: vlan [id integrer]")
				return
			vlan_id = args[1:][0]
			if(self.testing_vlan(vlan_id) == False) or (len(vlan_id) == 0):
				print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: vlan [id integrer]")
				return
			str_vlan_id = str(vlan_id).strip('[]').strip('\'"')
			if(common.get_len_vlan_id() != 0):
				for i in range(0,common.get_len_vlan_id()):
					if(str_vlan_id == common.get_item_vlan_id(i)):
						print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "vlan id already exists")
						return
					else:
						common.append_vlan_id(str_vlan_id)
						connecting_vlan.set_connect_vlan(common.get_len_vlan_id()-1)
						common.append_vlan_name("default-" + str(common.get_len_vlan_id()))
						print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Vlan " + str_vlan_id  + " has been created")
						common.normal_append_array_interfaces_vlan([])
						common.normal_append_array_ip_vlan(" ")

						common.append_array_history(line)
						common.get_console().prompt = "(config-vlan)"
						if(cargando.get_cargando() == False):
							common.get_console().loop()
			else:
				common.append_vlan_id(str_vlan_id)
				connecting_vlan.set_connect_vlan(common.get_len_vlan_id()-1)
				common.append_vlan_name("default-" + str(common.get_len_vlan_id()))
				print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Vlan " + str_vlan_id  + " has been created")
				common.normal_append_array_interfaces_vlan([])
				############ES AQUI
				common.normal_append_array_ip_vlan(" ")
				common.append_array_history(line)
				common.get_console().prompt = "(config-vlan)"
				if(cargando.get_cargando() == False):
					common.get_console().loop()
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")


# Clase VLAN Name la cual nos sirve para ponerle nombre a una vlan Previamente
# creada
class VlanName(Command.Command):
    vlan_name = []
    def run(self,line):
        if common.get_console().prompt == "(config-vlan)":
            args = line.split()
            vlan_name = args[1:]
            str_vlan_name = str(vlan_name).strip('[]').strip('\'"')
            common.set_array_vlan_name(connecting_vlan.get_connect_vlan(),str_vlan_name)
            print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Vlan name " + str_vlan_name  + " assigned")
            common.append_array_history(line)

        else:
            print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")

class Show(Command.Command):
	def args(self):
		return ["vlan","interfaces","running-config"]
	def run(self,line):
		if(common.get_console().prompt == common.get_user_name()):
			args = line.split()
			argument = args[1:]
			if (str(argument).strip('[]').strip('\'"') == "vlan"):
				if(common.get_len_vlan_id() == 0):
					print(Colors.WARNING + "[WARNING] " + Colors.ENDC + "No VLAN's created")
					return
				print ("VLAN NAME\t\tVLAN ID\t\tINTERFACE\t\tIP ADDRESS")
				for i in range (common.get_len_vlan_id()):
					str_aux =  (common.get_item_vlan_name(i) + ":" + (" " *(8 - len(common.get_item_vlan_name(i)))) + "\t\t" + common.get_item_vlan_id(i) + "\t\t")
					for j in range(len(common.get_item_by_mini_vector(i))):
						str_aux = str_aux + (common.get_item_by_mini_vector(i)[j] + " ")
					str_aux = str_aux + (" " *(32- (4*len(common.get_item_by_mini_vector(i))))+(common.get_item_array_ip_vlan(i)))
					print(str_aux)
			else:
				if (str(argument).strip('[]').strip('\'"') == "interfaces"):
					print ("INTERFACES\t\tSTATUS")
					for i in range(0,common.get_len_interfaces()):
						str_aux = (common.get_item_interfaces(i) + "\t\t\t" + common.get_item_up_down_interface(i))
						print str_aux
				else:
					if (str(argument).strip('[]').strip('\'"') == "running-config"):
						# fichero_para_leer = open('/home/LisaSwitch.txt','r')
						# line = fichero_para_leer.readline()
						if(common.get_len_array_history() > 0):
							print("!")
							for i in range(0,common.get_len_array_history()):
								if(common.get_item_array_history(i) == "exit"):
									print(common.get_item_array_history(i))
									print("!")
								else:
									print(common.get_item_array_history(i))
						else:
							print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "No configuration saved")
					else:
						print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")


class Exit(Command.Command):
    def run(self,line):
		if (common.get_console().prompt == common.get_user_name()):
			sys.exit(1)
		else:
			if common.get_console().prompt == "(config-if)":
				common.get_console().prompt = "(config)"
				if(common.get_multi() == True):
					common.append_array_multi(line)
					print common.get_array_multi()
					run.run_multi()
				else:
					common.append_array_history(line)
				if (cargando.get_cargando() == False):
					common.get_console().loop()
			else:
				if common.get_console().prompt == "(config-vlan)":
					common.get_console().prompt = "(config)"
					common.append_array_history(line)
					if (cargando.get_cargando() == False):
						common.get_console().loop()
				else:
					if common.get_console().prompt == "(config)":
						common.get_console().prompt = common.get_user_name()
						common.append_array_history(line)
						if (cargando.get_cargando() == False):
							common.get_console().loop()

class History(Command.Command):
    def run(self,line):
		if(common.get_console().prompt == common.get_user_name()):
			for i in range (common.get_len_array_history()):
				print ("\t" + str(i+1) + ":  " + common.get_item_array_history(i))
		else:
			print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")

#copy running-config startup-config --> SAVE
#copy startup-config runnning-config --> LOAD
class Save_Load(Command.Command):
	def args(self):
		return ["running-config startup-config","startup-config running-config"]
	def run(self,line):
		args = line.split()
		if(common.get_console().prompt == common.get_user_name()):
			if(args[1:][0] == "running-config" and args[1:][1] == "startup-config"):
				print ("Creando fichero")
				fichero = open('/home/config.txt','w+')
				for i in range(0,common.get_len_array_history()):
					fichero.write(common.get_item_array_history(i) + '\n')
				fichero.close()
			else:
				if(args[1:][0] == "startup-config" and args[1:][1] == "running-config"):
					if(os.path.exists("/home/config.txt") == True):
						cargando.set_cargando()
						fichero_leer = open('/home/config.txt','r')
						linea = fichero_leer.readline()
						while(linea != ""):
							common.get_console().walk(linea,0,run=True,full_line=linea)
							linea = fichero_leer.readline()
						fichero_leer.close()
						cargando.set_cargando()
					else:
						print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "There is no configuration saved")
				else:
					print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command Use")
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad Command use")

class No(Command.Command):
	def testing_no_vlan(self,id):
		patron = re.compile('^\d+$')
		if(patron.match(str(id))):
			return True
		return False

	def args(self):
		if (Clases.common.get_console().prompt == "(config)"):
			return ["vlan"]
		else:
			if(common.get_console().prompt == "(config-if)"):
				return ["shutdown"]

	def run(self,line):
		args = line.split()
		check = False
		if(len(args) > 1):
			argument = args[0:][1]
			if(argument == "vlan"):
				if(common.get_console().prompt == "(config)"):
					if(len(args[1:]) == 2):
						vlan_id_to_delete = args[0:][2]
						if(self.testing_no_vlan(vlan_id_to_delete)):
							if(common.get_len_vlan_id() > 0):
								for i in range(0,common.get_len_vlan_id()):
									if(vlan_id_to_delete == common.get_item_vlan_id(i)):
										check = True
										for j in range(0,len(common.get_item_by_mini_vector(i))):
											vswitch.ovs_vsctl_del_port_from_bridge(common.get_item_by_mini_vector(i)[j])
											vswitch.ovs_vsctl_add_port_to_bridge("br0",common.get_item_by_mini_vector(i)[j])
										common.remove_item_vlan_id(common.get_item_vlan_id(i))
										common.remove_item_vlan_name(common.get_item_vlan_name(i))
										common.append_array_history(line)
										break
								if(check == False):
									print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "VLAN doesnt exist")
							else:
								print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "No VLAN's created")
						else:
							print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: no vlan [vlan id]")
					else:
						print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Usage: no vlan [vlan id]")
				else:
					print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")

			else:
				if(argument == "shutdown"):
					if(common.get_console().prompt == "(config-if)"):
						if(common.get_multi() == True):
							common.append_array_multi(line)
						else:
							try:
								subprocess.call(['ifconfig','%s' % connecting_interfaces.get_connect(),'up'])
								common.append_array_history(line)
								for i in range(0,common.get_len_interfaces()):
									if(connecting_interfaces.get_connect() == common.get_item_array_interfaces(i)):
										common.set_up_down_interface(i)
							except KeyboardInterrupt:
								print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")
								return
					else:
						print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")
		else:
			print(Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")


class Ping(Command.Command):
	def run(self,line):
		if(common.get_console().prompt == common.get_user_name()):
			destination = line.split()[-1]
			try:
				subprocess.call(['ping','%s' % destination])
			except KeyboardInterrupt:
				print("Ping Command canceled.")
				return
		else:
			print (Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use")


class Shutdown(Command.Command):
	def args(self):
		return ["shutdown"]
	def run(self, line):
		if(common.get_console().prompt == "(config-if)"):
			try:
				subprocess.call(['ifconfig','%s' % connecting_interfaces.get_connect(),'down'])
				common.append_array_history(line)
			except KeyboardInterrupt:
				print (Colors.FAIL + "[ERROR] " + Colors.ENDC)
				return

class See(Command.Command):
    def run(self,line):
		vswitch.ovs_vsctl_show()

class ActualCommand(Command.Command):
	def run(self,line):
		if(common.get_console().prompt == common.get_user_name()):
			print("\t\tconfigure")
			print("\t\treload")
			print("\t\thostname [new switch name]")
			print("\t\thistory")
			print("\t\tcopy startup-config running-config")
			print("\t\tcopy running-config startup-config")
			print("\t\tshow vlan")
			print("\t\tshow interfaces")
			print("\t\texit")
			print("\t\tping [address]")

		else:
			if(common.get_console().prompt == '(config)'):
				print("Commands in 'config' prompt:\n")
				print("\t\tvlan [vlan id]")
				print("\t\tno vlan [vlan]")
				print("\t\tinterface [interface name]")
				print("\t\tinterface vlan [vlan id")
				print("\t\texit")
			else:
				if(common.get_console().prompt == '(config-if)'):
					print("Commands in '(config-if)' prompt:\n")
					print("\t\tswitchport mode access")
					print("\t\tswitchport mode trunk ")
					print("\t\tswitchport access vlan [vlan id]")
					print("\t\tswitchport trunk allowed vlan [allowed vlans]")
					print("\t\tshutdown")
					print("\t\tno shutdown")
					print("\t\texit")
					print("\t\tip address [address] [mask]")
				else:
					if(common.get_console().prompt == '(config-vlan)'):
						print("Commands in '(config-vlan)' prompt:\n")
						print("\t\tname [vlan name]")
						print("\t\texit")

def main():
	hostname = Hostname("hostname",help="Usage: hostname [name]",dynamic_args=True)
	configureswitch = ConfigureSwitch("configure",help="Usage: configure to access to the switch configuration")
	vlan = Vlan("vlan",help="Usage: vlan [vlan id]",dynamic_args=True)
	vlan_name = VlanName("name",help="Usage: name [vlan_name]")
	show = Show("show",help="Usage: show [interfaces | vlan ]",dynamic_args=True)
	exit = Exit("exit",help="Usage: exit",dynamic_args=True)
	history = History("history",help="Usage: history")
	configure_interface = ConfigureInterface("interface",help="Usage: interface [interface]",dynamic_args=True)
	switchport = Switchport("switchport",help="switchport [mode|access|trunk]:\n \tmode: switchport mode [access|trunk]\n \taccess: switchport access vlan [access vlan]\n \ttrunk: switchport trunk allowed vlan [allowed vlan's]",dynamic_args=True)
	ipadmininterface = IPAdminInterface("ip",help="Usage: ip address [ip] [short|long mask]",dynamic_args=True)
	saveload = Save_Load("copy",help="Usage: Load Config: copy startup-config running-config || Save: copy running-config startup-config",dynamic_args=True)
	no = No("no",help="Usage: no [vlan] [vlan_id]",dynamic_args=True)
	ping = Ping("ping",help="Usage: ping [ip address]")
	shutdown = Shutdown("shutdown",help="Usage: shutdown",dynamic_args=True)
	see = See("see",help="Show in OpenVSwitch")
	reload_ = Reload("reload",help="Reset bridge",dynamic_args=True)
	actualcommand = ActualCommand("?",help="Actual command depends of prompt")
	common.get_console().addChild(configureswitch)
	common.get_console().addChild(hostname)
	common.get_console().addChild(vlan)
	common.get_console().addChild(vlan_name)
	common.get_console().addChild(exit)
	common.get_console().addChild(switchport)
	common.get_console().addChild(show)
	common.get_console().addChild(history)
	common.get_console().addChild(configure_interface)
	common.get_console().addChild(ipadmininterface)
	common.get_console().addChild(no)
	common.get_console().addChild(saveload)
	common.get_console().addChild(ping)
	common.get_console().addChild(see)
	common.get_console().addChild(actualcommand)
	common.get_console().addChild(shutdown)
	common.get_console().addChild(reload_)
	subprocess.call(["/etc/init.d/openvswitch-switch","start"])
	if(vswitch.ovs_vsctl_is_ovs_bridge("br0") == False):
		vswitch.ovs_vsctl_add_bridge("br0")
		print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Bridge Created with name br0")
		contador = 0
		load_or_not = raw_input("Do you have any configuration saved? (y/n): ")
		if(load_or_not == "y"):
			common.get_console().walk("copy startup-config running-config",0,run=True,full_line="copy startup-config running-config")
		for i in range(0,common.get_len_interfaces()):
			vswitch.ovs_vsctl_add_port_to_bridge("br0",common.get_item_interfaces(i))
			vswitch.iplink(common.get_item_interfaces(i),"down")
			contador = contador + 1
			print (Colors.OKGREEN + "[OK] " + Colors.ENDC + "Adding " + str(contador) + " interface to bridge br0")
	common.get_console().loop()
	print (Colors.OKBLUE + "Bye" + Colors.ENDC)
if __name__ == '__main__':
	main()
