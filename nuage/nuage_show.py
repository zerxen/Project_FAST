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
        if (args.filter is not None and  len(args.filter) > 0) and (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.find_user_in_enterprise(args.entname[0],args.filter[0])             
        elif (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.print_users_of_enterprise(args.entname[0])
        else:
            return nuage.print_users_of_all_enterprises();
            
    if args.OBJECT == 'groups':
        print("nuage show groups starting ...")
        nuage = nuage_vspk_wrapper()
        nuage.connect()
        if (args.filter is not None and  len(args.filter) > 0) and (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.find_group_in_enterprise(args.entname[0],args.filter[0])
        elif (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.print_groups_of_enterprise(args.entname[0])
        else:
            nuage.print_groups_of_all_enterprises();
            return 0
        
    if args.OBJECT == 'enterprises':
        print("nuage show enterprises, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        
        print ("Printing TREE? : " + str(args.tree))
        if len(args.entname) > 0 and args.entname[0] is not None:
            print ("Filtering by entname: " + str(args.entname[0]))
        
        if args.tree == 1 and (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.print_whole_three(args.entname[0]);
        elif args.tree == 0 and (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.print_enterprises(args.entname[0]);                    
        else:
            nuage.print_enterprises('');
            return 0;
        
    if args.OBJECT == 'domains':
        print("nuage show domains, starting ...")
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        if (args.domname is not None and  len(args.domname) > 0) and (args.entname is not None and len(args.entname) > 0):
            return nuage.print_domain_for_enterprise(args.entname[0],args.domname[0])        
        elif (args.entname is not None and len(args.entname) > 0 and  args.entname[0] != ''):
            return nuage.print_domains_for_enterprise(args.entname[0])
        else:
            return nuage.print_domains();
        
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
            return 1
        if args.domname is None or args.domname == '':        
            print("you have to specify domain name with --domname")
            return 1         
        
        nuage = nuage_vspk_wrapper();
        nuage.connect()
        if args.subnetname is not None and args.zonename is not None and len(args.subnetname) > 0 and len(args.zonename) > 0:         
            return nuage.print_dhcp_options_of_subnet(args.entname[0],args.domname[0],args.zonename[0],args.subnetname[0]);
        else:
            return nuage.print_dhcp_options_of_domain(args.entname[0],args.domname[0]); 
        
    if args.OBJECT == 'gateways':
        print("nuage show gateways starting ...")
        nuage = nuage_vspk_wrapper()
        nuage.connect() 
        
        '''TODO'''
        nuage.print_gateways()
                                          
        

        