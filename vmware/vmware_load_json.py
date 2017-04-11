import json
from pprint import pprint
from vmware.API_wrappers.vmware_pyvmomi_interface import vmware_pyvmomi_wrapper

def vmware_load_json(args):
    pprint (args)
    
    pprint(args.INFILE)
    
    #json_data=open(json_file)
    #pprint(json_data)
    #json_data=open(args.INFILE)
    data = json.load(args.INFILE)
    args.INFILE.close()
    #pprint(data)
    #args.infile.close()
    print('')
    try:
        for vm in data['vms']:
            print("type: " + vm['type'])
            print("name: " + vm['name'])
            print("    autopower: " + vm['autopower'])
            print("    template:" + vm['template'])
            print("    resource-pool: " + vm["resource-pool"])
            print("    nuage-enterprise" + vm['nuage-enterprise'])
            print("    nuage-user: " + vm['nuage-enterprise'])
            print("    ixia-address: " + vm['ixia-address'])
            print("    ixia-netmask: " + vm['ixia-netmask'])
            print("    ixia-dns1: " + vm['ixia-dns1'])
            print("    ixia-dns2: " + vm['ixia-dns2'])
            print("    ixia-nic-domain: " + vm['ixia-nic-domain'])
            for nic in vm['nuage-nics']:
                print("        NIC name: " + nic['name'])
                print("        NIC domain: " + nic['domain'])
                print("        NIC zone: " + nic['zone'])
                print("        NIC subnet: " + nic['subnet'])
                print("        NIC ip-type: " + nic['ip-type'])
                if nic['ip-type'] == "static":
                    print("        NIC IP: " + nic['ip'])

    except Exception, e:
        print('Caught exception: %s' % str(e))
        return 1   
    
    print("")
    print("Looks like the JSON go loaded completely, will create VMs now...")
    
    vcenter = vmware_pyvmomi_wrapper()
    vcenter.connect()
    
    for vm in data['vms']:
        if vm['type'] == "2nic-no-DXC":
            print("VM: " + vm['name'] + " type: " + vm['type'])
            print("creating 2 nic VM, one VM in nuage subnet, one in Ixia VLAN.")
            
            ''' DEFAULT no_dxc for this type '''
            no_dxc = 1
            
            power_on = 0
            if vm['autopower'] == "yes":
                power_on = 1
                
            vcenter.create_vm_from_template(vm['template'], 
                                            vm['resource-pool'], 
                                            vm['name'], 
                                            vm['nuage-enterprise'], 
                                            vm['nuage-user'], 
                                            vm['nuage-nics'][0]['domain'], 
                                            vm['nuage-nics'][0]['zone'], 
                                            vm['nuage-nics'][0]['subnet'], 
                                            "", 
                                            "", 
                                            "", 
                                            vm['ixia-address'], 
                                            vm['ixia-netmask'], 
                                            vm['ixia-gateway'], 
                                            vm['ixia-dns1'], 
                                            vm['ixia-dns2'], 
                                            vm['ixia-nic-domain'],
                                            power_on,
                                            no_dxc)            
            
        else:
            print("UNKNOWN VM TYPE!")
    
       
    
    #pprint(data)