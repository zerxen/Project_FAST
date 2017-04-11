import json
from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_create(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("nuage create didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'vlan-on-gateway':
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
        nuage.create_vlan_under_gateway_interface(args.gateway[0],args.gateway_interface[0],args.vlan_id[0])   
        
    if args.OBJECT == 'vtep':
        if args.gateway is None or args.gateway == '':
            print("You did not specified a gateway with --gateway")
            return
        if args.gateway_interface is None or args.gateway_interface == '':
            print("You did not specified a gateway with --gateway-interface")
            return
        if args.vlan_id is None or args.vlan_id == '':
            print("You did not specified a gateway with --vlan-id")
            return 
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify --entname for new object")
            return
        if args.domname is None or args.domname == '':
            print("You are creating without any parent domain name?! Specify --domname for new object")
            return
        if args.zonename is None or args.zonename == '':
            print("You are creating without any zone parent name?! Specify --zonename for new object")
            return    
        if args.subnetname is None or args.subnetname == '':
            print("You are creating vtep without any subnet specified?! Specify --subnetname name for new object")
            return               
        nuage = nuage_vspk_wrapper();
        nuage.connect() 
        nuage.create_vtep(args.gateway[0], args.entname[0], args.domname[0], args.zonename[0], args.subnetname[0], args.gateway_interface[0], args.vlan_id[0])       
                     
    
    if args.OBJECT == 'default-permit-acls':
        if args.entname is None or args.entname == '':
            print("You are creating without any name?! Specify name for new object")
            return
        if args.domname is None or args.domname == '':
            print("You are creating without any domain name?! Specify name for new object")
            return           
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_default_permit_acls(args.entname[0],args.domname[0])    
    
    
    if args.OBJECT == 'enterprise':
        if args.entname is None or args.entname == '':
            print("You are creating without any name?! Specify name for new object")
            return
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_enterprise(args.entname[0])
        
        
    if args.OBJECT == 'group':
        if args.entname is None or args.entname == '':
            print("You are creating without any enterprise name?! Specify name for new object")
            return
        if args.groupname is None or args.groupname == '':
            print("You are creating without any group name ?! Specify name for new object")
            return        
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_group(args.entname[0],args.groupname[0])        
        


    if args.OBJECT == 'user':   
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify enterprise name for new object")
            return
        if args.username is None or args.username == '':
            print("You are creating without any username ?! Specify name for new object")
            return
        if args.password is None or args.password == '':
            print("You are creating without any password ?! Specify enterprise name for new object")
            return
        if args.firstname is None or args.firstname == '':
            print("You are creating without any firstname ?! Specify name for new object")
            return
        if args.lastname is None or args.lastname == '':
            print("You are creating without any lastname?! Specify enterprise name for new object")
            return
        if args.useremail is None or args.useremail == '':
            print("You are creating without any email?! Specify enterprise name for new object")
            return        

        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_user(args.entname[0],args.username[0],args.password[0],args.firstname[0],args.lastname[0],args.useremail[0])         
        
        
        
    if args.OBJECT == 'domaintemplate':   
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify name for new object")
            return
        if args.domtempname is None or args.domtempname == '':
            print("You are creating without any domain template name?! Specify name for new object")
            return
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_domain_template(args.entname[0],args.domtempname[0]) 
    
         
        
    if args.OBJECT == 'domain':   
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify name for new object")
            return
        if args.domtempname is None or args.domtempname == '':
            print("You are creating without any parent domain template name?! Specify name for new object")
            return
        if args.domname is None or args.domname == '':
            print("You are creating without any domain name?! Specify name for new object")
            return        
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_domain(args.entname[0],args.domtempname[0],args.domname[0])  
        


    if args.OBJECT == 'zone':   
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify name for new object")
            return
        if args.domname is None or args.domname == '':
            print("You are creating without any parent domain name?! Specify name for new object")
            return
        if args.zonename is None or args.zonename == '':
            print("You are creating without any zone name?! Specify name for new object")
            return        
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_zone(args.entname[0],args.domname[0],args.zonename[0])  
        
        
        
    if args.OBJECT == 'subnet':   
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify name for new object")
            return
        if args.domname is None or args.domname == '':
            print("You are creating without any parent domain name?! Specify name for new object")
            return
        if args.zonename is None or args.zonename == '':
            print("You are creating without any zone parent name?! Specify name for new object")
            return    
        if args.subnetname is None or args.subnetname == '':
            print("You are creating subnet without any name?! Specify name for new object")
            return   
        if args.subnetNetworkIP is None or args.subnetNetworkIP == '':
            print("You are creating subnet without any Network IP?! Specify name for new object")
            return    
        if args.subnetNetworkMask is None or args.subnetNetworkMask == '':
            print("You are creating subnet without any Netwrok Mask?! Specify name for new object")
            return                
            
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_subnet(args.entname[0],args.domname[0],args.zonename[0],args.subnetname[0],args.subnetNetworkIP[0],args.subnetNetworkMask[0])  
        
        
        
    if args.OBJECT == 'dhcp-option-121':   
        if args.entname is None or args.entname == '':
            print("You are creating without any parent enterprise name?! Specify name for new object")
            return
        if args.domname is None or args.domname == '':
            print("You are creating without any parent domain name?! Specify name for new object")
            return
        if args.zonename is None or args.zonename == '':
            print("You are creating without any zone parent name?! Specify name for new object")
            return    
        if args.subnetname is None or args.subnetname == '':
            print("You are creating subnet without any name?! Specify name for new object")
            return   
        if args.dhcp_route_prefix is None or args.dhcp_route_prefix == '':
            print("You are creating route prefix ?! Specify name for new object --dhcp-route-prefix")
            return    
        if args.dhcp_route_nexthop is None or args.dhcp_route_nexthop == '':
            print("You are creating route without nexthop! Specify name for new object --dhcp-route-nexthop")
            return   
        if args.dhcp_route_prefix_mask is None or args.dhcp_route_prefix_mask == '':
            print("You are creating route without prefix mask! Specify name for new object --dhcp-route-prefix-mask")
            return                       
            
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.create_dhcp_option_121(args.entname[0],args.domname[0],args.zonename[0],args.subnetname[0],args.dhcp_route_prefix[0],args.dhcp_route_nexthop[0],args.dhcp_route_prefix_mask[0])                                   
        
        
        
        
    
    