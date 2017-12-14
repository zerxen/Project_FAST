import json
from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_delete(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("nuage delete didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'vtep':
        if args.vportname is None or args.vportname == '':
            print("You did not specified a vportname with --vportname")
            return 
        if args.entname is None or args.entname == '':
            print("You did not specified any parent enterprise name?! Specify --entname ")
            return
        if args.domname is None or args.domname == '':
            print("You did not specified any parent domain name?! Specify --domname")
            return
        if args.zonename is None or args.zonename == '':
            print("You did not specified any zone parent name?! Specify --zonename")
            return    
        if args.subnetname is None or args.subnetname == '':
            print("You did not specified any subnetname?! Specify --subnetname")
            return               
        nuage = nuage_vspk_wrapper();
        nuage.connect() 
        nuage.delete_vtep(args.vportname[0], args.entname[0], args.domname[0], args.zonename[0], args.subnetname[0])       
      
    
    if args.OBJECT == 'enterprise':
        if args.entname is None or args.entname == '':
            print("You are deleting without any name?! Specify name for object")
            return

        nuage = nuage_vspk_wrapper();
        nuage.connect()  
                
        if args.tree == 1:
            return nuage.delete_whole_enterprise_tree(args.entname[0])
        else:
            return nuage.delete_enterprise(args.entname[0])
            
    if args.OBJECT == 'user':
        if args.entname is None or args.entname == '':
            print("You are deleting without any enterprise reference?! Specify name for object")
            return 1
        if args.username is None or args.username == '':
            print("You are deleting without any username reference?! Specify name for object")
            return 1        

        nuage = nuage_vspk_wrapper();
        nuage.connect()  
        return nuage.delete_user(args.entname[0],args.username[0])
        
            
    if args.OBJECT == 'group':
        if args.entname is None or args.entname == '':
            print("You are deleting without any enterprise reference?! Specify name for object")
            return 1
        if args.groupname is None or args.groupname == '':
            print("You are deleting without any group name reference?! Specify name for object")
            return 1        

        nuage = nuage_vspk_wrapper();
        nuage.connect()  
        return nuage.delete_group(args.entname[0],args.groupname[0])        
        
    if args.OBJECT == 'domaintemplate':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return 1
        if args.domtempname is None or args.domtempname == '':
            print("You are deleting without any domain template name?! Specify name for object")
            return 1
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_domain_template(args.entname[0],args.domtempname[0])   
        
        
    if args.OBJECT == 'domain':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return
        if args.domname is None or args.domname == '':
            print("You are deleting without any domain name?! Specify name for object")
            return        
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_domain(args.entname[0],args.domname[0])
    
    if args.OBJECT == 'acl':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return 1
        if args.domname is None or args.domname == '':
            print("You are deleting without any domain name?! Specify name for object")
            return 1        
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_acl(args.entname[0],args.domname[0])     

    if args.OBJECT == 'network_macros':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return 1     
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_network_macros(args.entname[0]) 
    
    if args.OBJECT == 'network_macro_groups':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return 1     
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_network_macro_groups(args.entname[0])      
        


    if args.OBJECT == 'zone':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return 1
        if args.domname is None or args.domname == '':
            print("You are deleting without any parent domain name?! Specify name for object")
            return 1
        if args.zonename is None or args.zonename == '':
            print("You are deleting without any zone name?! Specify name for object")
            return 1       
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_zone(args.entname[0],args.domname[0],args.zonename[0])  
        
        
        
    if args.OBJECT == 'subnet':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return 1
        if args.domname is None or args.domname == '':
            print("You are deleting without any parent domain name?! Specify name for object")
            return 1
        if args.zonename is None or args.zonename == '':
            print("You are deleting without any zone parent name?! Specify name for object")
            return 1   
        if args.subnetname is None or args.subnetname == '':
            print("You are deleting subnet without any name?! Specify name for object")
            return 1   

        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        return nuage.delete_subnet(args.entname[0],args.domname[0],args.zonename[0],args.subnetname[0])  
        
    if args.OBJECT == 'dhcp-options':   
        if args.entname is None or args.entname == '':
            print("You are deleting without any parent enterprise name?! Specify name for object")
            return
        if args.domname is None or args.domname == '':
            print("You are deleting without any parent domain name?! Specify name for object")
            return
        if args.zonename is None or args.zonename == '':
            print("You are deleting without any zone parent name?! Specify name for object")
            return    
        if args.subnetname is None or args.subnetname == '':
            print("You are deleting subnet without any name?! Specify name for object")
            return   

        nuage = nuage_vspk_wrapper();
        nuage.connect()        
        nuage.delete_dhcp_options(args.entname[0],args.domname[0],args.zonename[0],args.subnetname[0])         
        
        
        
                      