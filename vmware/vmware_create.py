import json
from pprint import pprint
from vmware.API_wrappers.vmware_pyvmomi_interface import vmware_pyvmomi_wrapper

def vmware_create(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("vmware create didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'vm':
        print("vmware show vms starting ...")
        vcenter = vmware_pyvmomi_wrapper()
        vcenter.connect()
        
        if args.template is None or args.template == '':
            print("You didn't specified template with --template")
            return 1
        if args.resource_pool is None or args.resource_pool == '':
            print("You didn't specified resource pool with --resource-pool")
            return 1
        if args.name is None or args.name == '':
            print("You didn't specified name with --name")
            return 1
        if args.nuage_enterprise is None or args.nuage_enterprise == '':
            print("You didn't specified nuage_enterprise with --nuage-enterprise")
            return 1
        if args.nuage_user is None or args.nuage_user == '':
            print("You didn't specified nuage_user with --nuage_user")
            return 1
        if args.production_nic_domain is None or args.production_nic_domain == '':
            print("You didn't specified production_nic_domain with --production_nic_domain")
            return 1
        if args.production_nic_zone is None or args.production_nic_zone == '':
            print("You didn't specified production_nic_zone with --production_nic_zone")
            return 1
        if args.production_nic_subnet is None or args.production_nic_subnet == '':
            print("You didn't specified production_nic_subnet with --production_nic_subnet")
            return 1
        if args.no_dxc == 0:
            if args.dxc_nic_domain is None or args.dxc_nic_domain == '':
                print("You didn't specified dxc_nic_domain with --dxc_nic_domain")
                return 1
            if args.dxc_nic_zone is None or args.dxc_nic_zone == '':
                print("You didn't specified dxc_nic_zone with --dxc_nic_zone")
                return 1
            if args.dxc_nic_subnet is None or args.dxc_nic_subnet == '':
                print("You didn't specified dxc_nic_subnet with --dxc_nic_subnet")
                return 1
        if args.ixia_nic_address is None or args.ixia_nic_address == '':
            print("You didn't specified ixia_nic_address with --ixia_nic_address")
            return 1
        if args.ixia_nic_netmask is None or args.ixia_nic_netmask == '':
            print("You didn't specified ixia_nic_netmask with --ixia_nic_netmask")
            return 1
        #Gateway on IXIA is optional
        #if args.ixia_nic_gateway is None or args.ixia_nic_gateway == '':
        #    print("You didn't specified ixia_nic_gateway with --ixia_nic_gateway")
        #    return 1
        if args.ixia_nic_dns1 is None or args.ixia_nic_dns1 == '':
            print("You didn't specified ixia_nic_dns1 with --ixia_nic_dns1")
            return 1
        if args.ixia_nic_dns2 is None or args.ixia_nic_dns2 == '':
            print("You didn't specified ixia_nic_dns2 with --ixia_nic_dns2")
            return 1
        if args.ixia_nic_domain is None or args.ixia_nic_domain == '':
            print("You didn't specified ixia_nic_domain with --ixia_nic_domain")
            return 1  
        
        vcenter.create_vm_from_template(args.template[0], 
                                        args.resource_pool[0], 
                                        args.name[0], 
                                        args.nuage_enterprise[0], 
                                        args.nuage_user[0], 
                                        args.production_nic_domain[0], 
                                        args.production_nic_zone[0], 
                                        args.production_nic_subnet[0], 
                                        args.dxc_nic_domain[0], 
                                        args.dxc_nic_zone[0], 
                                        args.dxc_nic_subnet[0], 
                                        args.ixia_nic_address[0], 
                                        args.ixia_nic_netmask[0], 
                                        args.ixia_nic_gateway[0], 
                                        args.ixia_nic_dns1[0], 
                                        args.ixia_nic_dns2[0], 
                                        args.ixia_nic_domain[0],
                                        args.power_on,
                                        args.no_dxc)
              