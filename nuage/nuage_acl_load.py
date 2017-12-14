'''
Created on Dec 14, 2017

@author: havrila
'''
import yaml
from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_load_acl_yaml(args):
    pprint (args)    
    
    # TRY TO LOAD THE YAML PROVIDED 
    data = yaml.load(args.YAML_FILE)     
    print("")
    print("####### YAML ACL LOADED: #######")
    pprint(data)
    
    # CHACK PARAMETERS
    if args.entname is None or args.entname == '':
        print("you have to specify enterprise name with --entname")
        return 1
    if args.domname is None or args.domname == '':        
        print("you have to specify domain name with --domname")
        return 1     

    # CONNECT TO NUAGE
    nuage = nuage_vspk_wrapper();
    nuage.connect() 

    # CREATING NETWORK MACROS
    for network_macro in data['network_macros']:
        error_code = nuage.create_network_macro(args.entname[0],network_macro['name'],network_macro['address'],network_macro['mask'])
        if error_code != 0:
            print("network_macros creation problem, quiting ...")
            return 1
        
    # CREATING NETWORK MACRO GROUPS
    for network_macro_group in data['network_macro_groups']:
        error_code = nuage.create_empty_network_macro_group(args.entname[0],network_macro_group['name'])
        if error_code != 0:
            print("network_macro_group creation problem, quiting ...")
            return 1
        
        for macro in network_macro_group['macros']:
            error_code = nuage.add_macro_to_network_macro_group(args.entname[0], network_macro_group['name'], macro['name'])
            if error_code != 0:
                print("adding macro to group problem, quiting ...")
                return 1            
                    

    return 0
