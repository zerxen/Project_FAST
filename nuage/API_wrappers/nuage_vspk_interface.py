# -*- coding: utf-8 -*-
from vspk import v4_0 as vsdk
import time
from pprint import pprint
from nuage_access_configuration import nuage_configuration

class nuage_vspk_wrapper():
    '''
    Initializations
    '''
    def __init__(self):
        self.username = nuage_configuration.username
        self.password = nuage_configuration.password
        self.enterprise = nuage_configuration.enterprise
        self.api_url = nuage_configuration.api_url
        
    def connect(self):
        self.nc = vsdk.NUVSDSession(username=self.username, password=self.password, enterprise=self.enterprise, api_url=self.api_url)
        self.nc.start()
        
    '''
    Users
    '''
    def get_users_all_enterprises(self):
        enterprises = self.get_enterprises()
        users = []
        for ent in enterprises:
            users.append(ent.users.get())  
        return users
             
    def get_users_of_one_enterprise(self,filter_name):
        enterprise = self.get_enterprise_find_name(filter_name)
        if enterprise is None:
            print("Failed to get enterprise")
            return         
        users = []
        users = enterprise.users.get()              
        return users  
    
    def get_user_by_name_from_enterprise(self,entname,filter_name):
        users = self.get_users_of_one_enterprise(entname)
        if users is None:
            print("Failed to get users")
            return    
        
        for user in users:
            if user.user_name == filter_name:
                return user
            
        return None    
            
    
    def print_users_of_enterprise(self,entname):
        if entname is None or entname == '':
            print("Invalid enterprise filter")
            return 
        
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return  
        
        print("--- USERS of " + enterprise.name + " ---")
        for user in enterprise.users.get():
            print("USER ID: " + user.user_name)      
        
    def print_users_of_all_enterprises(self):
        enterprises = self.get_enterprises()
        if enterprises is None:
            print("Failed to get enterprises")
            return          
        
        for enterprise in enterprises:
            self.print_users_of_enterprise(enterprise.name)
    
    def create_user(self,entname,username,password,firstname,lastname,email):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return  
        
        user = vsdk.NUUser(user_name=username,password=password,first_name=firstname,last_name=lastname,email=email) 
        enterprise.create_child(user) 
        
    def delete_user(self,entname,username):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return  
        
        user = self.get_user_by_name_from_enterprise(entname, username)
        if user is None:
            print("User not found")
            return   
        
        user.delete()
             
    '''
    Groups
    ''' 
        
    def get_groups_of_one_enterprise(self,entname):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return         
        groups = enterprise.groups.get()              
        return groups              
         
    def get_group_by_name_from_enterprise(self,entname,groupname):
        groups = self.get_groups_of_one_enterprise(entname)
        if groups is None:
            print("Failed to get users")
            return    
        
        for group in groups:
            if group.name == groupname:
                return group
            
        return None              
        
    def print_groups_of_enterprise(self,entname):
        if entname is None or entname == '':
            print("Invalid enterprise filter")
            return 
        
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get groups")
            return  
        
        print("--- GROUPS of " + enterprise.name + " ---")
        for group in enterprise.groups.get():
            print("GROUP name: " + group.name)
                  
        
    def print_groups_of_all_enterprises(self):
        enterprises = self.get_enterprises()
        if enterprises is None:
            print("Failed to get groups")
            return          
        
        for enterprise in enterprises:
            self.print_groups_of_enterprise(enterprise.name) 
            
    def create_group(self,entname,groupname):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return  
        
        group = vsdk.NUGroup(name=groupname) 
        enterprise.create_child(group) 
        
    def delete_group(self,entname,groupname):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return  
        
        group = self.get_group_by_name_from_enterprise(entname, groupname)
        if group is None:
            print("User not found")
            return   
        
        group.delete()                
      
                

    '''
    Enterprises
    '''        
    def get_enterprises(self):
        return self.nc.user.enterprises.get()
    
    def print_enterprises(self,filter_name):
        if filter_name == '':
            enterprises = self.get_enterprises()
            if enterprises is None:
                print("Failed to get any Enterprises")
                return                
        else:
            ent = self.get_enterprise_find_name(filter_name)
            if ent is None:
                print("Failed to find Enterprise using filter \"" + filter_name + "\"")
                return
            else:
                enterprises = [ent]

        print("--- ENTERPRISES ---")
        for ent in enterprises:
            print("ENTERPRISE: " + ent.name)
            print("ID: " + ent.id)
            print("")
        
    def get_enterprise_find_name(self,entname):
        filter = 'name == "' + entname + '"';
        return self.nc.user.enterprises.get_first(filter)
    
    def create_enterprise(self,entname):
        try:
            enterprise = vsdk.NUEnterprise(name=entname)
            self.nc.user.create_child(enterprise)
            print("Enterprise created with name " + entname + " ID: " + enterprise.id)
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1   
        
    def delete_enterprise(self,entname):
        try:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Failed to find the Enterprise! Aborting...")
                return  
            print("Enterprise to be DELETED: " + entname + " ID: " + enterprise.id)
            enterprise.delete()
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1  
        

    '''
    DOmains
    '''    
    
    def get_domains(self):
        return self.nc.user.domains.get()
    
    def get_domains_for_enterprise_object(self,enterprise):
        return enterprise.domains.get()
    
    def get_domain_template_find_name(self,entname,domtempname):
        filter = 'name == "' + entname + '"';
        enterprise = self.nc.user.enterprises.get_first(filter)
        if enterprise is None:
            print("Failed to find parent enterprise")
            return
        filter = 'name == "' + domtempname + '"';
        return enterprise.domain_templates.get_first(filter) 
    
    def get_domain_find_name(self,entname,domname):
        filter = 'name == "' + entname + '"';
        enterprise = self.nc.user.enterprises.get_first(filter)
        if enterprise is None:
            print("Failed to find parent enterprise")
            return
        filter = 'name == "' + domname + '"';
        return enterprise.domains.get_first(filter)        
    
    def print_domains(self):
        domains = self.get_domains()
        if domains is  None:
            print("Failed to get any Domains")
        else:
            print("--- DOMAINS ---")
            for dom in domains:
                print("DOMAIN: " + dom.name)
                print("ID: " + dom.id)
                print("")        
        
    def getDomainsForEnterprise(self,entname):
        
        enterprise = self.getenterprise_find_name(entname)
        if enterprise is not None:
            return enterprise.domains.get()    
        else:
            print("Failed to get enterprise named: " + entname)
            return None
        
    def create_domain_template(self,entname,domtempname):
        try:
            domaintemplate = vsdk.NUDomainTemplate(name=domtempname)
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1
            enterprise.create_child(domaintemplate)
            print("Domain template created with name " + domtempname + " ID: " + domaintemplate.id)
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1    
        
    def create_domain(self,entname,domtempname,domname):
        try:
            domain_template = self.get_domain_template_find_name(entname,domtempname)
            if domain_template is None:
                print("Bad domain template name submitted")
                return 1
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1            
            domain = vsdk.NUDomain(name=domname,template_id=domain_template.id)
            enterprise.create_child(domain)
            print("Domain created with name " + domname + " ID: " + domain.id)
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1                 
    
    def delete_domain_template(self,entname,domtempname):
        try:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1
            domain_template = self.get_domain_template_find_name(entname,domtempname)
            if domain_template is None:
                print("Bad domain template name submitted")
                return 1                    
            print("Domain template deleted with name " + domtempname + " ID: " + domain_template.id)
            domain_template.delete();             
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1    
        
    def delete_domain(self,entname,domname):
        try:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1 
            domain = self.get_domain_find_name(entname,domname)
            if domain is None:
                print("Bad domain name submitted")
                return 1                
            print("Domain deleted with name " + domname + " ID: " + domain.id)
            domain.delete();  
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1      
    '''
    Zones
    '''    
    def get_zones(self):
        return self.nc.user.zones.get()
    
    def get_zones_for_domain_object(self,domain):
        return domain.zones.get()
    
    def get_zone_find_name(self,entname,domname,zonename):
        
        filter = 'name == "' + entname + '"';
        enterprise = self.nc.user.enterprises.get_first(filter)
        if enterprise is None:
            print("Failed to find parent enterprise")
            return
        
        filter = 'name == "' + domname + '"';
        domain = enterprise.domains.get_first(filter)
        if domain is None:
            print("Failed to find parent domain")
            return
        
        filter = 'name == "' + zonename + '"';
        return domain.zones.get_first(filter)
                
    
    def print_zones(self):
        zones = self.get_zones()
        if zones is  None:
            print("Failed to get any Zones")
        else:
            print("--- ZONES ---")
            for zon in zones:
                print("ZONE: " + zon.name)
                print("ID: " + zon.id)
                print("")  
                
    def create_zone(self,entname,domname,zonename):
        try:
            domain = self.get_domain_find_name(entname,domname)
            if domain is None:
                print("Bad domain name submitted")
                return 1
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1            
            zone = vsdk.NUZone(name=zonename)
            domain.create_child(zone)
            print("Zone created with name " + zonename + " ID: " + zone.id)
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1   
        
    def delete_zone(self,entname,domname,zonename):
        try:
            domain = self.get_domain_find_name(entname,domname)
            if domain is None:
                print("Bad domain name submitted")
                return 1
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1   
            zone = self.get_zone_find_name(entname,domname,zonename)
            if zone is None:
                print("Bad zone name")
                return 1                         
            print("Zone deleted with name " + zonename + " ID: " + zone.id)
            zone.delete();
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1                          
                
    '''
    Subnets
    '''    
    def get_subnets(self):
        return self.nc.user.subnets.get()
    
    def get_subnets_for_zone_object(self,zone):
        return zone.subnets.get() 
    
    def get_subnet_find_name(self,entname,domname,zonename,subnetname):
        try:
            filter = 'name == "' + entname + '"';
            enterprise = self.nc.user.enterprises.get_first(filter)
            if enterprise is None:
                print("Failed to find parent enterprise")
                return
            
            filter = 'name == "' + domname + '"';
            domain = enterprise.domains.get_first(filter)
            if domain is None:
                print("Failed to find parent domain")
                return
            
            filter = 'name == "' + zonename + '"';
            zone = domain.zones.get_first(filter)
            if zone is None:
                print("Failed to find parent zone")
                return  
            
            filter = 'name == "' + subnetname + '"';
            return zone.subnets.get_first(filter) 
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1                 
              
    
    
    
    def print_subnets(self):
        subnets = self.get_subnets()
        if subnets is  None:
            print("Failed to get any Subnets")
        else:
            print("--- Subnets ---")
            for sub in subnets:
                print("SUBNET: " + sub.name)
                print("Address: " + sub.address + "/" + sub.netmask)
                print("")  
                
    def create_subnet(self,entname,domname,zonename,subnetname,subnetNetworkIP,subnetNetworkMask):
        try:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1                   
            domain = self.get_domain_find_name(entname,domname)
            if domain is None:
                print("Bad domain name submitted")
                return 1
            zone = self.get_zone_find_name(entname,domname,zonename)
            if zone is None:
                print("Bad zone name submitted")
                return 1            
     
            subnet = vsdk.NUSubnet(name=subnetname,address=subnetNetworkIP,netmask=subnetNetworkMask)
            zone.create_child(subnet)
            print("Subnet created with name " + subnetname)
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1   
        
    def delete_subnet(self,entname,domname,zonename,subnetname):
        try:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("Bad enterprise name")
                return 1                   
            domain = self.get_domain_find_name(entname,domname)
            if domain is None:
                print("Bad domain name submitted")
                return 1
            zone = self.get_zone_find_name(entname,domname,zonename)
            if zone is None:
                print("Bad zone name submitted")
                return 1  
            subnet = self.get_subnet_find_name(entname,domname,zonename,subnetname)
            if subnet is None:
                print("Bad subnet name submitted")
                return 1                      
            print("Subnet deleted with name " + subnetname)
            subnet.delete();
            return 0
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1   
        
    '''
    Permissions
    '''        
    def print_permissions_of_all_enterprises(self):
        enterprises = self.get_enterprises()
        if enterprises is None:
            print("Failed to get enterprises")
            return 
        
        for enterprise in enterprises:
            self.print_permissions_of_one_enterprise(enterprise.name)         
                
             
    def print_permissions_of_one_enterprise(self,entname):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("Failed to get enterprise")
            return  
        
        print("ENTERPRISE: " + enterprise.name)
        for domain in enterprise.domains.get():
            print("  DOMAIN: " + enterprise.name)
            for permission in domain.permissions.get():
                print("    PERMISSION permitted_action: " + permission.permitted_action)
                print("    PERMISSION permitted_entity_id: " + permission.permitted_entity_id)   
                
    def assign_permission_group_to_domain(self,entname,groupname,domname,permission):
        
        filter = 'name == "' + entname + '"';
        print(filter)
        enterprise = self.nc.user.enterprises.get_first(filter)
        pprint(enterprise)
        
        filter = 'name == "' + groupname + '"';
        print(filter)
        group = enterprise.groups.get_first(filter)                           
        pprint(group)
        print("Group ID:" + group.id)
            
        filter = 'name == "' + domname + '"';
        print(filter)
        domain = enterprise.domains.get_first(filter)
        pprint(domain)
                   
        if enterprise is None:
            print("No enterprise found using the filter provided")
            return 1 
        if group is None:
            print("No group found using the filter provided")
            return 1
        if domain is None:
            print("No domain found using the filter provided")
            return 1
             
        # permission_object = vsdk.NUPermission(permitted_action=permission,permitted_entity_id=group.id)
        
        print("")
        print("Validating permission object")
        permission_object = vsdk.NUPermission()
        permission_object.permitted_entity_id = group.id
        permission_object.permitted_action = 'DEPLOY'
        
        pprint(permission_object)
        print("permitted_entiti_id: " + permission_object.permitted_entity_id)
        print("permitted_action: " + permission_object.permitted_action)
        
        domain.create_child(permission_object)
        
        print("permission.id: " + permission_object.id)

        
    def assign_permission_group_to_zone(self,entname,groupname,domname,zonename,permission):
        
        filter = 'name == "' + entname + '"';
        print(filter)
        enterprise = self.nc.user.enterprises.get_first(filter)
        pprint(enterprise)
        
        filter = 'name == "' + groupname + '"';
        print(filter)
        group = enterprise.groups.get_first(filter)                           
        pprint(group)
        print("Group ID:" + group.id)
            
        filter = 'name == "' + domname + '"';
        print(filter)
        domain = enterprise.domains.get_first(filter)
        pprint(domain)
        
        filter = 'name == "' + zonename + '"';
        print(filter)
        zone = domain.zones.get_first(filter)
        pprint(zone)        
                   
        if enterprise is None:
            print("No enterprise found using the filter provided")
            return 1 
        if group is None:
            print("No group found using the filter provided")
            return 1
        if domain is None:
            print("No domain found using the filter provided")
            return 1
        if zone is None:
            print("No zone found using the filter provided")
            return 1        
        
        # There is no group.id ?! how to get permitted entinty ID ?         
        permission_object = vsdk.NUPermission(permitted_action=permission,permitted_entity_id=group.id)
        zone.create_child(permission_object)                                      
    
    '''
    VMs
    '''
    def get_VMs_names_for_enterprise(self,entname):
        if entname == '':
            print("You didn't specified any Eneterprise to search for ...")
            return None
        else:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("No enterprise found using the filter provided")
                return None
            
        vm_list = []
        
        for dom in self.get_domains_for_enterprise_object(enterprise):
            for zon in self.get_zones_for_domain_object(dom):
                for sub in self.get_subnets_for_zone_object(zon):                                             
                    for vport in sub.vports.get():
                        for vm in vport.vms.get():
                            for vmint in vport.vm_interfaces.get():
                                vm_list.append(vm.name)
                                print("Found VM name:" + vm.name + " VM int IP:" + vmint.ip_address + " VM uuid:" + vmint.vmuuid)
                                    
        return vm_list;  
    
    '''
    VPORTS
    '''
    def get_vport_for_enterprise_vm(self,entname,domname,zonename,subnetname,vmname):
        subnet = self.get_subnet_find_name(entname, domname, zonename, subnetname)
        
        for vport in subnet.vports.get():
            for vm in vport.vms.get():
                if vm.name == vmname:
                    for vmint in vport.vm_interfaces.get():
                        print("Searched for VM IP found:" + vm.name + " VM int IP:" + vmint.ip_address + " VM uuid:" + vmint.vmuuid) 
                        return vmint.ip_address       
        
                         
        return None
                
    '''
    Tree
    '''   
    def print_whole_three(self,filter_name):
        
        if filter_name == '':
            enterprises = self.get_enterprises()
            if enterprises is None:
                print("No enterprise found using the filter provided")
                return                
        else:
            ent = self.get_enterprise_find_name(filter_name)
            if ent is None:
                print("No enterprise found using the filter provided")
                return
            enterprises = [ent]
            
        
            
        for ent in enterprises:
            print("+-ENTERPRISE: " + ent.name+ " ID: " + ent.id)
            for gateway in ent.gateways.get():
                print("    +-GATEWAY: " + gateway.name)
            for dom in self.get_domains_for_enterprise_object(ent):
                print("    +-DOMAIN: " + dom.name+ " ID: " + dom.id)
                for zon in self.get_zones_for_domain_object(dom):
                    print("        +-ZONE: " + zon.name+ " ID: " + zon.id)
                    for sub in self.get_subnets_for_zone_object(zon):
                        print("                +-SUBNET: " + sub.name + " Address: " + sub.address + "/" + sub.netmask)
                                             
                        for vport in sub.vports.get():
                            print("                    vPort Name:" + vport.name)
                            for vm in vport.vms.get():
                                for vmint in vport.vm_interfaces.get():
                                    print("                        VM name:" + vm.name + " VM int IP:" + vmint.ip_address + " VM uuid:" + vmint.vmuuid)
                           
                             
                            for bridge_interface in vport.bridge_interfaces.get():
                                print("                        bridge_interface: " + bridge_interface.name  ) 
                            for host_interface in vport.host_interfaces.get():
                                print("                        host_interface: " + host_interface.name)                                     
                        
            print("")
            
    def delete_whole_enterprise_tree(self,entname):
        try:
            enterprise = self.get_enterprise_find_name(entname)
            if enterprise is None:
                print("No enterprise found using the filter provided")
                return 1
            
            domains = enterprise.domains.get()
            for domain in domains:
                zones = domain.zones.get()
                for zone in zones:
                    subnets = zone.subnets.get()
                    for subnet in subnets:
                        for vport in subnet.vports.get():
                            bridge_interfaces = vport.bridge_interfaces.get()
                            for bridge_interface in bridge_interfaces:
                                print("Found nested bridge_interface, deleting...")
                                bridge_interface.delete()
                                
                            host_interfaces = vport.host_interfaces.get()
                            for host_interface in host_interfaces:
                                print("Found nested host_interface, deleting...")
                                host_interface.delete();
                            
                            vport.delete()                            
                            
                        subnet.delete();
                    zone.delete()
                domain.delete()
                
            domain_templates = enterprise.domain_templates.get()
            for domain_template in domain_templates:
                domain_template.delete()
            
            enterprise.delete()
            
        except Exception, e:
            print('Caught exception: %s' % str(e))
            return 1    
        
        
    '''
    Group Assignments
    '''   
       
    def assign_user_to_group(self,entname,groupname,username):
        enterprise = self.get_enterprise_find_name(entname)
        if enterprise is None:
            print("No enterprise found using the filter provided")
            return 1 
        group = self.get_group_by_name_from_enterprise(entname, groupname)
        if group is None:
            print("No group found using the filter provided")
            return 1
        user = self.get_user_by_name_from_enterprise(entname, username)
        if enterprise is None:
            print("No user found using the filter provided")
            return 1
        
        users = group.users.get()
        users.append(user)
        group.assign(users,vsdk.NUUser)
        
    '''
    Access-lists
    '''         
                
    def print_acls(self,entname,domname):
        domain = self.get_domain_find_name(entname, domname)
        if domain is None:
            print("Failed to get specified domain")
            return
        
        eg_acls_list = domain.egress_acl_templates.get()
        in_acls_list = domain.ingress_acl_templates.get()
        
        print("") 
        for in_acls in in_acls_list:        
            if in_acls != None:
                if in_acls.name is not None:
                    print("INGRESS ACL: " + in_acls.name) 
                if in_acls.priority_type is not None:
                    print("priority_type: " + in_acls.priority_type) 
                if in_acls.priority is not None:
                    print("priority: "+ str(in_acls.priority)) 
                if in_acls.default_allow_non_ip is not None:
                    print("default_allow_non_ip: "+ str(in_acls.default_allow_non_ip)) 
                if in_acls.default_allow_ip is not None:
                    print("default_allow_ip: "+ str(in_acls.default_allow_ip)) 
                if in_acls.allow_l2_address_spoof is not None:
                    print("allow_l2_address_spoof: "+ str(in_acls.allow_l2_address_spoof)) 
                if in_acls.active is not None:
                    print("active: "+ str(in_acls.active))   
                    
            print("")
            acl_igress_rules_list = in_acls.ingress_acl_entry_templates.get()
            for acl_igress_rule in acl_igress_rules_list: 
                print("")
                print("ACL rule #" + str(acl_igress_rule.priority) + " name:"+ str(acl_igress_rule.description))
                #pprint(acl_igress_rule)
                attrs = vars(acl_igress_rule)
                print ', '.join("%s: %s" % item for item in attrs.items())                
        
        print("")
        print("")              
        for eg_acls in eg_acls_list:
            if eg_acls != None:
                if eg_acls.name is not None:
                    print("EGRESS ACL: " + eg_acls.name) 
                if eg_acls.priority_type is not None:
                    print("priority_type: " + eg_acls.priority_type) 
                if eg_acls.priority is not None:
                    print("priority: "+ str(eg_acls.priority)) 
                if eg_acls.default_allow_non_ip is not None:
                    print("default_allow_non_ip: "+ str(eg_acls.default_allow_non_ip)) 
                if eg_acls.default_allow_ip is not None:
                    print("default_allow_ip: "+ str(eg_acls.default_allow_ip))  
                if eg_acls.active is not None:
                    print("active: "+ str(eg_acls.active))  
                    
            print("")
            acl_egress_rules_list = eg_acls.egress_acl_entry_templates.get()
            for acl_egress_rule in acl_egress_rules_list:
                print("")
                print("ACL rule #" + str(acl_egress_rule.priority) + " name:"+ str(acl_egress_rule.description))
                #pprint(acl_egress_rule)                
                attrs = vars(acl_egress_rule)
                print ', '.join("%s: %s" % item for item in attrs.items())
                         
                
                                                     
    def create_default_permit_acls(self,entname,domname):
        domain = self.get_domain_find_name(entname, domname)
        if domain is None:
            print("Failed to get specified domain")
            return        
                                                            
        # Creating the job to begin the policy changes
        job = vsdk.NUJob(command='BEGIN_POLICY_CHANGES')
        domain.create_child(job)
        
                   
        # wait for the job to finish
        # can be done with a while loop
         
        # Creating a new Ingress ACL
        ingressacl = vsdk.NUIngressACLTemplate(
            name='Middle Ingress ACL',
            priority_type='NONE', # Possible values: TOP, NONE, BOTTOM (domain only accepts NONE)
            priority=100,
            default_allow_non_ip=True,
            default_allow_ip=True,
            allow_l2_address_spoof=True,
            active=True
            )
        domain.create_child(ingressacl) 
        
        egressacl = vsdk.NUEgressACLTemplate(
            name='Middle Egress ACL',
            priority_type='NONE', # Possible values: TOP, NONE, BOTTOM (domain only accepts NONE)
            priority=100,
            default_allow_non_ip=True,
            default_allow_ip=True,
            active=True
            )
        domain.create_child(egressacl)         
        
        job = vsdk.NUJob(command='APPLY_POLICY_CHANGES')
        domain.create_child(job)    
        
    '''
    GATEWAYS
    '''
    def get_gateways(self):
        return self.nc.user.gateways.get()
    
    
    def print_gateways(self):
        gateways = self.get_gateways()
        if gateways is None:
            print("No Gateways")
        
        print("")
        print("GATEWAYS:")
        print("=========")    
        for gateway in gateways:
            print("")
            print("" + gateway.name + " personality:" + gateway.personality)
            
            ports = gateway.ports.get()
            if ports is None:
                print("    No vports on this gateway")
            else:
                for port in ports:
                    print("    PORT:" + port.name + " port_type:"+port.port_type)
                    
                    port_permissions = port.enterprise_permissions.get()
                    #print("    PORT PERMISSIONS:")
                    for permission in port_permissions:
                        print("        permitted_action(port):"+permission.permitted_action + " permitted_entity_name:"+ permission.permitted_entity_name)
                    
                    vlans = port.vlans.get()
                    #print("    VLANS:")
                    for vlan in vlans:
                        print("        vlan:" + str(vlan.value))
                        
                        vlan_permissions = vlan.enterprise_permissions.get()
                        #print("        VLAN PERMISSIONS:")
                        for permission in vlan_permissions: 
                            print("            permitted_action(vlan):"+permission.permitted_action + " permitted_entity_name:"+ permission.permitted_entity_name + " ID:" + permission.permitted_entity_id)
                    
            
    def assign_permission_vlan_under_gateway_interface(self,entname,gateway_id,gateway_interface,gateway_vlan):
        filter = 'name == "' + gateway_id + '"';
        enterprise = self.get_enterprise_find_name(entname)
        
        if enterprise is None:
            print("Enterprise not found")
            exit(1)
        else:
            print("Found enterprise by ID: " + enterprise.name)        
        
        
        filter = 'name == "' + gateway_id + '"';
        gateway = self.nc.user.gateways.get_first(filter) 
        
        if gateway is None:
            print("Gateway not found")
            exit(1)
        else:
            print("Found gateway by ID: " + gateway.name)
        
        filter = 'name == "' + gateway_interface + '"';
        port = gateway.ports.get_first(filter)   
        if port is None:
            print("Gateway's interface not found")
            exit(1)                  
        else:
            print("Found gateway's interface: " + port.name)
            
        for vlan in port.vlans.get():
            if vlan.value ==  int(gateway_vlan):
                print("Found VLAN ID specified, will add Enterprise ID " + enterprise.id  + " permissions to it")
                
                permission = vsdk.NUEnterprisePermission()
                permission.permitted_entity_id = enterprise.id
                permission.permitted_action = 'USE'                
                vlan.create_child(permission)                 
                
                print("DONE")
                return
        
    
    def create_vlan_under_gateway_interface(self,gateway_id,gateway_interface,gateway_vlan):        
        filter = 'name == "' + gateway_id + '"';
        gateway = self.nc.user.gateways.get_first(filter) 
        
        if gateway is None:
            print("Gateway not found")
            exit(1)
        else:
            print("Found gateway by ID: " + gateway.name)
        
        filter = 'name == "' + gateway_interface + '"';
        port = gateway.ports.get_first(filter)   
        if port is None:
            print("Gateway's interface not found")
            exit(1)                  
        else:
            print("Found gateway's interface: " + port.name)
            
        vlans = port.vlans.get()
        for vlan in vlans:
            if vlan.value == int(gateway_vlan):
                print("This VLAN ID already exists here! Exiting...")
                exit(1)
                
        print("Creating a new VLAN under this gateway/interface")
        vlan = vsdk.NUVLAN(
            value=int(gateway_vlan)
            )
        port.create_child(vlan) 

    def delete_vtep(self,vportname,entname, domname, zonename, subnetname):
        print("VTEP deletion starting ...")
        subnet = self.get_subnet_find_name(entname, domname, zonename, subnetname)
        if subnet is None:
            print("Unable to locate target enterprise-zone-subnet for VTEP deletion")
            exit(1)
            
        print("Found target subnet")
            
        vports = subnet.vports.get()
        
        for vport in vports:
            if vport.name == vportname:
                print("Found the vPort for deletion, deleting ....")
                
                bridge_interfaces = vport.bridge_interfaces.get()
                for bridge_interface in bridge_interfaces:
                    print("Found nested bridge_interface, deleting...")
                    bridge_interface.delete()
                    
                host_interfaces = vport.host_interfaces.get()
                for host_interface in host_interfaces:
                    print("Found nested host_interface, deleting...")
                    host_interface.delete();
                
                vport.delete()
                return
                
        print("vPort for deletion NOT FOUND")
                
            
                  
            
                                
        
    def create_vtep(self,gateway_id,entname, domname, zonename, subnetname, gateway_interface,gateway_vlan):
        print("VTEP creation starting ...")
        subnet = self.get_subnet_find_name(entname, domname, zonename, subnetname)
        if subnet is None:
            print("Unable to locate target enterprise-zone-subnet for VTEP creation")
            exit(1)
            
        print("Found target subnet")
            
        filter = 'name == "' + gateway_id + '"';
        gateway = self.nc.user.gateways.get_first(filter) 
        
        if gateway is None:
            print("Gateway not found")
            exit(1)
        else:
            print("Found gateway by ID: " + gateway.name)
        
        filter = 'name == "' + gateway_interface + '"';
        port = gateway.ports.get_first(filter)   
        if port is None:
            print("Gateway's interface not found")
            exit(1)                  
        else:
            print("Found gateway's interface: " + port.name) 
            
        for vlan in port.vlans.get():
            if vlan.value ==  int(gateway_vlan):
                print("Found VLAN ID "+vlan.id+" specified, will add vport ")
                # TODO: CREATE VPORT
                
                vport_name = "FAST_vport_" + time.strftime('%Y_%b_%d_%H_%M_%p_%S_vlan') + gateway_vlan
                
                vport = vsdk.NUVPort(name=vport_name,
                                     type="BRIDGE",
                                     vlanid=vlan.id)
                
                vport.address_spoofing="ENABLED"
                print("Creating vport inside subnet, name:" + vport_name)
                subnet.create_child(vport)
                
                vbridge_name = "FAST_Bridge_Interface_" + time.strftime('%Y_%b_%d_%H_%M_%p_%S_vlan') + gateway_vlan
                bridgeinterface = vsdk.NUBridgeInterface(name=vbridge_name)
                
                print("Creating vbridge inside vport,name:" + vbridge_name)
                vport.create_child(bridgeinterface)
                
                return 
            
            
        print("DEBUG: There is no VLAN ID " + gateway_vlan + " on this gateway, please create it first!")                   
            
        
            
        
    
            
        
    '''
    DHCP-OPTIONS
    '''
    def one_hex_IP_route_print(self,hex_string):
        import array
        hex_data = hex_string.value.decode("hex")
        hex_octets = array.array('B', hex_data)      
                      
    def dhcp_options_parser(self,dhcp_options_list):
        if dhcp_options_list is not None:
            for dhcp_option in dhcp_options_list:
                print("    DHCP OPTION")
                print("    type(hex): " + dhcp_option.type)
                if dhcp_option.type == "79":
                    print("        value:" + dhcp_option.value)
                    
                    #experimental conversion
                    import array
                    hex_data = dhcp_option.value.decode("hex")
                    hex_octets = array.array('B', hex_data)                    
                    
                    prefix_mask = 0
                    route_octets_lenght = 0
                    route_octets = [0,0,0,0]
                    route_nexthop_octets = [0,0,0,0]

                    
                    next_route_if_this_is_zero = 0
                    for octet in hex_octets:
                        if next_route_if_this_is_zero == 0:
                            route_octets = [0,0,0,0]
                            route_nexthop_octets = [0,0,0,0]
                            prefix_mask = int(octet)
                            if prefix_mask >= 0 and prefix_mask <=8:
                                #print ("          one octet route")
                                route_octets_lenght = 1
                                next_route_if_this_is_zero = 4 + route_octets_lenght
                            elif prefix_mask > 8 and prefix_mask <=16:
                                #print ("          two octet route")
                                route_octets_lenght = 2
                                next_route_if_this_is_zero = 4 + route_octets_lenght  
                            elif prefix_mask > 16 and prefix_mask <=24:
                                #print ("          three octet route")
                                route_octets_lenght = 3
                                next_route_if_this_is_zero = 4 + route_octets_lenght  
                            elif prefix_mask > 24 and prefix_mask <=32:
                                #print ("          four octet route")
                                route_octets_lenght = 4 
                                next_route_if_this_is_zero = 4 + route_octets_lenght
                        
                        elif next_route_if_this_is_zero > 0:
                            
                            if next_route_if_this_is_zero > 4:
                                #print ("next_route_if_this_is_zero: " + str(next_route_if_this_is_zero))
                                #print ("route_octets_lenght: " + str(route_octets_lenght))
                                index = (next_route_if_this_is_zero-route_octets_lenght - 1) 
                                #print("index " + str(index))
                                route_octets[index] = int(octet)
                                #print("          route part: " + str(route_octets[index]))
                                                       
                            else:
                                index = (next_route_if_this_is_zero - 1)
                                #print("index " + str(index))
                                route_nexthop_octets[index] = int(octet) 
                                #print("          next-hop part: " + str(route_nexthop_octets[index]))
                                
                            next_route_if_this_is_zero = next_route_if_this_is_zero - 1
                            #print ( "next_route_if_this_is_zero " + str(next_route_if_this_is_zero))
                            
                            if next_route_if_this_is_zero == 0:
                                ''' we have just now reached the fact that this is one route end, lets print it nicelly '''
                                print("        Route(from hex): " + str(route_octets[3]) + "." + str(route_octets[2]) + "." + str(route_octets[1]) + "." + str(route_octets[0]) + "/" + str(prefix_mask) + " - " + str(route_nexthop_octets[3]) + "." + str(route_nexthop_octets[2]) + "." + str(route_nexthop_octets[1]) + "." + str(route_nexthop_octets[0]) )

                    for act_value in dhcp_option.actual_values: 
                        print("        act. value:" + act_value)        
        
    def print_dhcp_options(self,entname,domname):
        print("DOMAIN: "+ entname)
        domain = self.get_domain_find_name(entname, domname)
        if domain is None:
            print("Failed to get specified domain")
            return
        
        self.dhcp_options_parser(domain.dhcp_options.get())
                 
        zones = domain.zones.get()
        if zones is None:
            print("No zones in this domain")
            return
        
        for zone in zones:
            print("Zone: "+ zone.name)
            self.dhcp_options_parser(zone.dhcp_options.get())
            
            subnets = zone.subnets.get()
            if subnets is not None:
                for subnet in subnets:
                    print("  Subnet: "+ subnet.name)
                    self.dhcp_options_parser(subnet.dhcp_options.get())
                    
    def hex_encode(self,route):
        return b"".join([b"%02x" % int(octet) for octet in route])
    
    def octify_route(self,dhcp_route_prefix,dhcp_route_nexthop,dhcp_route_prefix_mask):
        array_prefix = dhcp_route_prefix.split('.');
        array_next_hop = dhcp_route_nexthop.split('.');
        dhcp_route_prefix_mask = int(dhcp_route_prefix_mask)

        if dhcp_route_prefix_mask >= 0 and dhcp_route_prefix_mask <=8:
            return (str(dhcp_route_prefix_mask),array_prefix[0],array_next_hop[0],array_next_hop[1],array_next_hop[2],array_next_hop[3])
        elif dhcp_route_prefix_mask > 8 and dhcp_route_prefix_mask <=16:
            return (str(dhcp_route_prefix_mask),array_prefix[0],array_prefix[1],array_prefix[1],array_prefix[2],array_next_hop[0],array_next_hop[1],array_next_hop[2],array_next_hop[3])
        elif dhcp_route_prefix_mask > 16 and dhcp_route_prefix_mask <=24:
            return (str(dhcp_route_prefix_mask),array_prefix[0],array_prefix[1],array_prefix[2],array_prefix[1],array_next_hop[0],array_next_hop[1],array_next_hop[2],array_next_hop[3])
        elif dhcp_route_prefix_mask > 24 and dhcp_route_prefix_mask <=32:
            return (str(dhcp_route_prefix_mask),array_prefix[0],array_prefix[1],array_prefix[2],array_prefix[3],array_next_hop[0],array_next_hop[1],array_next_hop[2],array_next_hop[3])        
        #return "vtip"
        
    def create_dhcp_option_121(self,entname,domname,zonename,subnetname,dhcp_route_prefix,dhcp_route_nexthop,dhcp_route_prefix_mask):
        subnet = self.get_subnet_find_name(entname, domname, zonename, subnetname)
        if subnet is None:
            print("Unable to find subnet!")
            return
        
        print("Subnet found with name: " + subnet.name)
        
        # First lets find the current hex string value:
        old_value = ""
        dhcp_options = subnet.dhcp_options.get()
        for dhcp_option in dhcp_options:
            print("    DHCP OPTION")
            print("    type(hex): " + dhcp_option.type)
            if dhcp_option.type == "79":
                print("value(hex):" + dhcp_option.value)
                old_value = dhcp_option.value
                dhcp_option.delete()
        
        new_route = self.octify_route(dhcp_route_prefix,dhcp_route_nexthop,dhcp_route_prefix_mask)
        print (new_route)
        #return
        #new_routes = [
        #    (24, 192,168,10, 10,0,0,1 ), 
        #    (24, 192,168,11, 10,0,0,1 ) 
        #]
        new_hex_value = b"".join(self.hex_encode(new_route))
        
        new_value = old_value + new_hex_value
        
        print("value new(hex):" + new_value)
        
        dhcpoption = vsdk.NUDHCPOption(type=79, value=new_value)
            
        #new_actual_values = [dhcp_route_prefix,dhcp_route_nexthop]
        #new_option = vsdk.NUDHCPOption(actual_type=121,actual_values=new_actual_values)
        
        subnet.create_child(dhcpoption)
        
        
        
    def delete_dhcp_options(self,entname,domname,zonename,subnetname):
        subnet = self.get_subnet_find_name(entname, domname, zonename, subnetname)
        if subnet is None:
            print("Unable to find subnet!")
            return
        
        print("Subnet found with name: " + subnet.name)
        
        dhcp_options = subnet.dhcp_options.get()
        for dhcp_option in dhcp_options:
            dhcp_option.delete()
                 
 
                            
                    
                    
                
                
            
                            
        
      

        
        
            
        

                        
                        
       
                               
            
    
        
    
    
    
        