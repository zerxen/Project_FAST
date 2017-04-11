import json
from pprint import pprint
from vmware.API_wrappers.vmware_pyvmomi_interface import vmware_pyvmomi_wrapper
from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper

def vmware_delete(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("vmware show didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'vm':
        print("vmware delete vm starting ...")
        vcenter = vmware_pyvmomi_wrapper()
        vcenter.connect()
        
        if args.name is None or args.name == '':
            print("You didn't specified name with --name")
            return 1
                
        vcenter.delete_vm(args.name[0])
        
    if args.OBJECT == 'vms-of-nuage-enterprise':
        print("vmware delete vms of entire Nuage enterprise starting ...")
        if args.entname is None or args.entname == '':
            print("You didn't specified Enterprise name with --entname")
            return 1  
        
        nuage = nuage_vspk_wrapper()
        nuage.connect() 
        vm_list = nuage.get_VMs_names_for_enterprise(args.entname[0])  
        
        if vm_list is None:
            print("There are no VMs in this enterprise or enterprise doesn't exist")
            return 1
        
        vcenter = vmware_pyvmomi_wrapper()
        vcenter.connect()
        
        for vm in vm_list:
            print("Recieved VM name: " + vm)
            vcenter.delete_vm(vm)
        
        # TODO: DELTE VM
        
           
        
        