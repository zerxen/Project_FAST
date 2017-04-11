import json
from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_show(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("nuage show didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'users':
        print("nuage show users starting ...")
        nuage = nuage_vspk_wrapper()
        nuage.connect()
        if args.entname is None or args.entname == '':
            nuage.print_users_of_all_enterprises();
        else:
            nuage.print_users_of_enterprise(args.entname[0])
            
    if args.OBJECT == 'groups':
        print("nuage show groups starting ...")
        nuage = nuage_vspk_wrapper()
        nuage.connect()
        if args.entname is None or args.entname == '':
            nuage.print_groups_of_all_enterprises();
        else:
            nuage.print_groups_of_enterprise(args.entname[0])
        
    if args.OBJECT == 'enterprises':
        print("nuage show enterprises, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        
        if args.tree == 1 and args.filter is not None and args.filter != '' :
            nuage.print_whole_three(args.filter[0]);
        elif args.tree == 1 and args.entname is not None or args.entname != '':
            nuage.print_whole_three(args.entname[0]);            
        elif args.filter != '':
            nuage.print_enterprises(args.filter[0]);
        else:
            nuage.print_enterprises('');
        
    if args.OBJECT == 'domains':
        print("nuage show domains, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        nuage.print_domains();
        
    if args.OBJECT == 'zones':
        print("nuage show zones, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        nuage.print_zones();     
        
    if args.OBJECT == 'subnets':
        print("nuage show subnets, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        nuage.print_subnets();   
        
    if args.OBJECT == 'permissions':
        print("nuage show permissions, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        if args.entname is None or args.entname == '':
            nuage.print_permissions_of_all_enterprises();
        else:
            nuage.print_permissions_of_enterprise(args.entname[0])  
            
    if args.OBJECT == 'acls':
        print("nuage show acls, starting ...")
        if args.entname is None or args.entname == '':
            print("you have to specify enterprise name with --entname")
            return
        if args.domname is None or args.domname == '':        
            print("you have to specify domain name with --domname")
            return    
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        nuage.print_acls(args.entname[0],args.domname[0]);  
        
   

    if args.OBJECT == 'dhcp-options':
        print("nuage show dhcp-options, starting ...")
        if args.entname is None or args.entname == '':
            print("you have to specify enterprise name with --entname")
            return
        if args.domname is None or args.domname == '':        
            print("you have to specify domain name with --domname")
            return    
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        nuage.print_dhcp_options(args.entname[0],args.domname[0]); 
        
    if args.OBJECT == 'gateways':
        print("nuage show gateways starting ...")
        nuage = nuage_vspk_wrapper()
        nuage.connect() 
        
        '''TODO'''
        nuage.print_gateways()
                                          
        

        