'''
Created on Feb 20, 2017

@author: havrila
'''
import json
from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_assign(args):
    pprint (args)

    if args.OBJECT is None:
        print("nuage assign didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'enterprise-to-gateway-vlan':
        if args.entname is None or args.entname == '':
            print("You are assigning  without enterprise name?! Specify --entname for object")
            return        
        if args.gateway is None or args.gateway == '':
            print("You did not specified a gateway with --gateway")
            return
        if args.gateway_interface is None or args.gateway_interface == '':
            print("You did not specified a gateway with --gateway-interface")
            return
        if args.vlan_id is None or args.vlan_id == '':
            print("You did not specified a gateway with --vlan-id")
            return 
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.assign_permission_vlan_under_gateway_interface(args.entname[0],args.gateway[0],args.gateway_interface[0],args.vlan_id[0])     
    
    if args.OBJECT == 'user-to-group':
        print("assigning user-to-group starting")
        if args.entname is None or args.entname == '':
            print("You are assigning  without enterprise any name?! Specify name for object")
            return
        if args.username is None or args.username == '':
            print("You are assigning without username any name?! Specify name for object")
            return
        if args.groupname is None or args.groupname == '':
            print("You are assigning without group any name?! Specify name for object")
            return

        nuage = nuage_vspk_wrapper();
        nuage.connect()       
        return nuage.assign_user_to_group(args.entname[0],args.groupname[0],args.username[0])
        
    if args.OBJECT == 'permission-for-group-to-domain':
        print("assigning permission-for-group-to-domain starting ...")
        if args.entname is None or args.entname == '':
            print("You are assigning  without enterprise any name?! Specify name for object")
            return 1
        if args.groupname is None or args.groupname == '':
            print("You are assigning without group any name?! Specify name for object")
            return 1
        if args.domname is None or args.domname == '':
            print("You are assigning without domain name any name?! Specify name for object")
            return 1   
        if args.permission is None or args.permission == '':
            print("You are assigning without any permission type specified?! Specify permission type for assignment")
            return 1         
             
        nuage = nuage_vspk_wrapper();
        nuage.connect()  
        return nuage.assign_permission_group_to_domain(args.entname[0],args.groupname[0],args.domname[0],args.permission)     
        
    if args.OBJECT == 'permission-for-group-to-zone':
        print("assigning permission-for-group-to-zone starting ...")
        if args.entname is None or args.entname == '':
            print("You are assigning  without enterprise any name?! Specify name for object")
            return 1
        if args.groupname is None or args.groupname == '':
            print("You are assigning without group any name?! Specify name for object")
            return 1
        if args.domname is None or args.domname == '':
            print("You are assigning without domain name any name?! Specify name for object")
            return 1  
        if args.zonename is None or args.zonename == '':
            print("You are assigning without zone name any name?! Specify name for object")
            return 1         
        if args.permission is None or args.permission == '':
            print("You are assigning without any permission type specified?! Specify permission type for assignment")
            return 1         
             
        nuage = nuage_vspk_wrapper();
        nuage.connect()  
        return nuage.assign_permission_group_to_zone(args.entname[0],args.groupname[0],args.domname[0],args.zonename[0],args.permission)             
        
   
        