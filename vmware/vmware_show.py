import json
from pprint import pprint
from vmware.API_wrappers.vmware_pyvmomi_interface import vmware_pyvmomi_wrapper

def vmware_show(args):
    pprint (args)
    
    if args.OBJECT is None:
        print("vmware show didn't recieved mandatory parameter, exiting ....")
        return
    
    if args.OBJECT == 'vms':
        print("vmware show vms starting ...")
        vcenter = vmware_pyvmomi_wrapper()
        vcenter.connect()
        
        vcenter.print_all_vms()
        
    if args.OBJECT == 'folders':
        print("vmware show vms starting ...")
        vcenter = vmware_pyvmomi_wrapper()
        vcenter.connect()
        
        vcenter.print_all_folders()  
        
    if args.OBJECT == 'resource-pools':
        print("vmware show vms starting ...")
        vcenter = vmware_pyvmomi_wrapper()
        vcenter.connect()
        
        vcenter.print_all_resource_pools()              
