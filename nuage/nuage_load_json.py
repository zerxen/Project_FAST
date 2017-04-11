import json
from pprint import pprint
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def nuage_load_json(args):
    pprint (args)
    
    pprint(args.INFILE)
    
    #json_data=open(json_file)
    #pprint(json_data)
    #json_data=open(args.INFILE)
    data = json.load(args.INFILE)
    args.INFILE.close()
    #pprint(data)
    #args.infile.close()
    try:
        print("Enterprise: " + data['enterprise'])
        print("")
        print("Users: ")
        for user in data['users']:
            print("    Username:" + user["username"])
            print("    password:" + user["password"])
            print("    useremail:" + user["useremail"])
            print("    firstname:" + user["firstname"])
            print("    lastname:" + user["lastname"])
            
        print("")     
        print("Grops: ")
        for group in data['groups']:
            print("    groupname:" + group["groupname"])
            for members in group["members"]:
                print("        member:" + members["username"])
        
        print("")           
        print("Dom. Templates: ")
        for dtemp in data['domaintemplates']:
            print("    Template: " + dtemp['domaintemplate'])
        
        print("")
        print("Domains: ")
        for domain in data['domains']:
            print("    Domain: " + domain['domain'])
            print("        ACLs: ")
            for rule in domain['acls']:
                print("        rule type:" + rule['type'])
            for permission in domain["permissions"]:
                print("        Permission type:" + permission["type"] + " for " + permission["group"])
            for zone in domain['zones']:
                print("        Zone: " + zone['zone'])
                for permission in zone["permissions"]:
                    print("            Permission type:" + permission["type"] + " for " + permission["group"])                
                for subnet in zone['subnets']:
                    print("            Subnet: " + subnet['subnet'])
                    print("            Address: " + subnet['address'])
                    print("            Netmask: " + subnet['netmask'])
                    if subnet["dhcp-options"]:
                        for dhcp_option in subnet["dhcp-options"]:
                            print("            DHCP option:")
                            print("                type:" + dhcp_option["type"])
                            if dhcp_option["type"] == str(121):
                                print("                prefix:" + dhcp_option["prefix"] + "/" + dhcp_option["mask"])
                                print("                prefix:" + dhcp_option["nexthop"])

    except Exception, e:
        print('Caught exception: %s' % str(e))
        return 1   
    
    print("")
    print("Looks like the JSON go loaded completely, will create topology now...")
    
    nuage = nuage_vspk_wrapper();
    nuage.connect()      
    
    nuage.create_enterprise(data['enterprise'])
    
    for user in data['users']:
        nuage.create_user(data['enterprise'], user['username'], user['password'], user['firstname'], user['lastname'], user['useremail'])
        
    for group in data['groups']:
        nuage.create_group(data['enterprise'], group['groupname'])
        for member in group['members']:
            nuage.assign_user_to_group(data['enterprise'], group['groupname'], member['username'])
            
    
    for dtemp in data['domaintemplates']:
        nuage.create_domain_template(data['enterprise'],dtemp['domaintemplate'])
    
    for domain in data['domains']:
        nuage.create_domain(data['enterprise'],domain['template_parent'],domain['domain'])
        for permission in domain['permissions']:
            nuage.assign_permission_group_to_domain(data['enterprise'], permission['group'], domain['domain'], permission['type'])
        
        for acl_rule in domain['acls']:
            if acl_rule['type'] == "permit-all":
                nuage.create_default_permit_acls(data['enterprise'], domain['domain'])
             
        for zone in domain['zones']:
            nuage.create_zone(data['enterprise'],domain['domain'],zone['zone']) 
            for permission in zone['permissions']:
                nuage.assign_permission_group_to_zone(data['enterprise'], permission['group'], domain['domain'], zone['zone'], permission['type'])            
            for subnet in zone['subnets']:
                nuage.create_subnet(data['enterprise'],domain['domain'],zone['zone'],subnet['subnet'],subnet['address'],subnet['netmask'])
                for dhcp_option in subnet['dhcp-options']:
                    if dhcp_option['type'] == "121":
                        nuage.create_dhcp_option_121(data['enterprise'], domain['domain'], zone['zone'], subnet['subnet'], dhcp_option['prefix'], dhcp_option['nexthop'], dhcp_option['mask'])  
        
    
    #pprint(data)