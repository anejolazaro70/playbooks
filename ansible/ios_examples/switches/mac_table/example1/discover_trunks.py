"""
El objetivo del script es obtener la informacion de la tabla MAC organizada de
la forma siguiente:
{puerto: {vlan1: [mac11, mac12,..., mac1N], vlan2: [mac21, mac22,..., mac2N]}} 
 """
import sys
import json
#from pprint import pprint


def read_table(mac_table):
    """ Procesa la tabla de direcciones MAC obtenida a traves del comando show mac address-table para obtener esta informacion:
        direcciones MAC asociadas a cada VLAN en cada INTERFACE"""
    lineas = []
    entries = {}
    with open(mac_table, "rb") as file:
        datos = json.load(file)
    for data in datos:
        entry = data.split()
        # si la interface no se ha revisado antes
        if entry[3] not in entries.keys():
            # se crea diccionario para VLAN-ID
            # se crea lista para guardar MACs asociadas a VLAN-ID en este puerto
            macs = []
            macs.append(entry[1])
            vlan_mac = {}
            vlan_mac[entry[0]] = macs
            entries[entry[3]] = vlan_mac
        # si la interface se ha revisado antes 
        else:
            # pero el VLAN-ID no estaba en la lista
            if entry[0] not in entries[entry[3]].keys():
                macs = []
                macs.append(entry[1])
                entries[entry[3]][entry[0]] = macs
            # el VLAN-ID estaba en la lista
            else:
                entries[entry[3]][entry[0]].append(entry[1])
    return entries

def ports(mac_table):
    """identifica que puertos de un switch son TRUNK Y ACCESS. Dentro de los puertos ACCESS, identifica cuales tienen varias direcciones MAC"""
    access_ports = []
    trunk_ports = []
    multimac_ports = []
    ports = mac_table.keys()
    for port, vlan in mac_table.items():
        # print "Interface: ", port
        # print "Vlan: ", vlan
        if len(vlan.keys()) == 1:
            access_ports.append(port)
            if multimac(vlan):
                multimac_ports.append(port)
        else:
            trunk_ports.append(port)
    return access_ports, trunk_ports, multimac_ports

def multimac(vlan):
    """detecta si una VLAN tiene una o varias direcciones MAC"""
    multimac = False
    #print "VLAN analizada: \n", vlan
    #print "MAC de VLAN: \n", vlan.values()
    if len(vlan.values()[0]) > 1:
        multimac = True
    return multimac

if __name__ == '__main__':
    mac_table = read_table(sys.argv[1])
    #for port, vlan in mac_table.items():
    #    print "----------------------------------"
    #    print "PUERTO: ", port
    #    for vlan, mac in vlan.items():
    #        print "VLAN: ", vlan
    #        print "MAC: ", mac
    acc_p, trnk_p, mmac_p = ports(mac_table)
    print "\n--------------------------\n"
    print "Lista de puertos access:\n", acc_p
    print "\n--------------------------\n"
    print "Lista de puertos trunk:\n", trnk_p
    print "\n--------------------------\n"
    print "Lista de puertos access con varias MAC:\n", mmac_p
