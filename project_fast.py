# -*- coding: utf-8 -*-
import argparse
import textwrap
import sys

from nuage.API_wrappers.nuage_vspk_interface import nuage_vspk_wrapper
from nuage.nuage_load_json import nuage_load_json
from nuage.nuage_show import nuage_show
from nuage.nuage_create import nuage_create
from nuage.nuage_delete import nuage_delete
from nuage.nuage_assign import nuage_assign
from nuage.nuage_acl_load import nuage_load_acl_yaml
from nuage.vspk_cli import nuage_vspk_cli
from fortinet.fortinet_show import fortinet_show
from vmware.vmware_show import vmware_show
from vmware.vmware_create import vmware_create
from vmware.vmware_delete import vmware_delete
from vmware.vmware_load_json import vmware_load_json
from ixchariot.ixchariot_experiments import ixchariot_experiments
from ixchariot.ixchariot_load_json import ixchariot_load_json
from ixchariot.ixchariot_run import ixchariot_run



def nuage_load(args):
    nuage_load_json(args)
       
if __name__ == "__main__":
    
    VERSION = "Alpha 0.4 (13th December 2017)"
    PROGRAM_NAME="Project FAST"
    COPYRIGHT="2017 (c) Peter Havrila" 
    README="README.md failed to load?"
    with open ("README.md", "r") as myfile:
        README=myfile.read() 
    
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(README),
        prog=PROGRAM_NAME,
        epilog=COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--version', action='version', version=('%(prog)s - ' + VERSION))
    parser.add_argument('-v', action='version', version=('%(prog)s - ' + VERSION))
    subparsers = parser.add_subparsers()
    
    # SUB-PARSERS
    parser_nuage = subparsers.add_parser('nuage')
    parser_vmware = subparsers.add_parser('vmware')
    parser_ixchariot = subparsers.add_parser('ixchariot')
    parser_fortinet = subparsers.add_parser('fortinet')
    
    # Sub-SUB parsers ixia
    subparsers_ixchariot = parser_ixchariot.add_subparsers()
    parsers_ixchariot_experiments = subparsers_ixchariot.add_parser('experiments')
    parsers_ixchariot_load = subparsers_ixchariot.add_parser('load')
    parsers_ixchariot_run = subparsers_ixchariot.add_parser('run')
    
    # ixia RUN PARAMETERS
    parsers_ixchariot_run.add_argument('OBJECT',choices=['session'],help='run existing ixcharriot test and collect results')
    parsers_ixchariot_run.add_argument('--id', nargs=1, help='Specify session ID to run', default="")
    parsers_ixchariot_run.add_argument('--generate-zip', action='store_const', const=1, default=0, help='will generate a ZIP file with full stats')   
    parsers_ixchariot_run.set_defaults(func=ixchariot_run)      
    
    # ixia EXPERMENTS PARAMETERS
    parsers_ixchariot_experiments.add_argument('OBJECT',choices=['test01'],help='alpha test, non-interactive, you have to edit ixchariot_sample.py ')
    parsers_ixchariot_experiments.set_defaults(func=ixchariot_experiments)  
    
    # ixia JSON LOAD PARAMETERS
    parsers_ixchariot_load.add_argument('INFILE', nargs='?', type=argparse.FileType('r'),help='File in JSON format that contains ixchariot test definition',default=sys.stdin)
    parsers_ixchariot_load.add_argument('--silent', action='store_const', const=1, default=0, help='will only show test results and no test definition logs') 
    parsers_ixchariot_load.set_defaults(func=ixchariot_load_json) 
   
    # Sub-SUB parsers vmware
    subparsers_vmware = parser_vmware.add_subparsers()
    parsers_vmware_show = subparsers_vmware.add_parser('show')
    parsers_vmware_create = subparsers_vmware.add_parser('create')
    parsers_vmware_delete = subparsers_vmware.add_parser('delete')
    parsers_vmware_load = subparsers_vmware.add_parser('load')
    
    # VMSARE LOAD
    parsers_vmware_load.add_argument('INFILE', nargs='+', type=argparse.FileType('r'),help='File in JSON format that contains vmware vms definition',default=sys.stdin)
    parsers_vmware_load.set_defaults(func=vmware_load_json)    
    
    # VMWARE SHOW PARAMETERS
    parsers_vmware_show.add_argument('OBJECT',choices=['vms','folders','resource-pools'],help='Select what type of vmware objects you would like listed')
    parsers_vmware_show.set_defaults(func=vmware_show)  
    
    # VMWARE DELETE PARAMETERS
    parsers_vmware_delete.add_argument('OBJECT',choices=['vm','vms-of-nuage-enterprise'],help='Select what type of vmware objects you would like deleted')
    parsers_vmware_delete.add_argument('--name', nargs=1, help='Specify VM name to delete', default="") 
    parsers_vmware_delete.add_argument('--entname', nargs=1, help='Specify nuage Enterprise in which to delete VMs', default="") 
    parsers_vmware_delete.set_defaults(func=vmware_delete)     
    
    # VMWARE CREATE PARAMETERS
    parsers_vmware_create.add_argument('OBJECT',choices=['vm'],help='Select what type of vmware objects you would like created')
    parsers_vmware_create.add_argument('--template', nargs=1, help='Specify template to clone for new VM', default="")
    parsers_vmware_create.add_argument('--datastore', nargs=1, help='Specify datastore to clone for new VM', default="")
    parsers_vmware_create.add_argument('--resource-pool', nargs=1, help='Specify resource-pool for new VM', default="")
    parsers_vmware_create.add_argument('--name', nargs=1, help='Specify name for new VM', default="")
    parsers_vmware_create.add_argument('--nuage-enterprise', nargs=1, help='Specify nuage-enterprise to clone for new VM', default="")
    parsers_vmware_create.add_argument('--nuage-user', nargs=1, help='Specify nuage-user for new VM', default="")
    parsers_vmware_create.add_argument('--production-nic-domain', nargs=1, help='Specify production-nic-domain for new VM', default="")
    parsers_vmware_create.add_argument('--production-nic-zone', nargs=1, help='Specify production-nic-zone to clone for new VM', default="")
    parsers_vmware_create.add_argument('--production-nic-subnet', nargs=1, help='Specify production-nic-subnet for new VM', default="")
    parsers_vmware_create.add_argument('--dxc-nic-domain', nargs=1, help='Specify dxc-nic-domain for new VM', default=[""])
    parsers_vmware_create.add_argument('--dxc-nic-zone', nargs=1, help='Specify dxc-nic-zone for new VM', default=[""])
    parsers_vmware_create.add_argument('--dxc-nic-subnet', nargs=1, help='Specify dxc-nic-subnet to clone for new VM', default=[""])
    parsers_vmware_create.add_argument('--ixia-nic-address', nargs=1, help='Specify ixia-nic-address for new VM', default="")
    parsers_vmware_create.add_argument('--ixia-nic-netmask', nargs=1, help='Specify ixia-nic-netmask for new VM', default="")
    parsers_vmware_create.add_argument('--ixia-nic-gateway', nargs=1, help='Specify ixia-nic-gateway for new VM', default=[""])
    parsers_vmware_create.add_argument('--ixia-nic-dns1', nargs=1, help='Specify ixia-nic-dns1 to clone for new VM', default="")
    parsers_vmware_create.add_argument('--ixia-nic-dns2', nargs=1, help='Specify ixia-nic-dns2 for new VM', default="")
    parsers_vmware_create.add_argument('--ixia-nic-domain', nargs=1, help='Specify ixia-nic-domain for new VM', default="")
    parsers_vmware_create.add_argument('--power-on', action='store_const', const=1, default=0, help='Enter this one if newly created VM should also be immediatelly booted')
    parsers_vmware_create.add_argument('--no-dxc', action='store_const', const=1, default=0, help='will not configure second DXC interface (parameters of dxc-nic become ognored)')         
    parsers_vmware_create.set_defaults(func=vmware_create)     
    
    # Sub-SUB parsers FORTINET
    subparsers_fortinet = parser_fortinet.add_subparsers()
    parsers_fortinet_show = subparsers_fortinet.add_parser('show')
    
    # FORTINET SHOW PARAMETERS
    parsers_fortinet_show.add_argument('OBJECT',choices=['interfaces'],help='Select what type of Fortinet objects you would like listed')
    parsers_fortinet_show.add_argument('--management-ip', nargs=1, help='Specific IP to access fortinet FW', default="")
    parsers_fortinet_show.add_argument('--management-username', nargs=1, help='Specific username to access fortinet FW', default="")
    parsers_fortinet_show.add_argument('--management-password', nargs=1, help='Specific password to access fortinet FW', default="")
    parsers_fortinet_show.set_defaults(func=fortinet_show)
    
    # Sub-SUB parsers NUAGE
    subparsers_nuage = parser_nuage.add_subparsers()
    parsers_nuage_load = subparsers_nuage.add_parser('load')
    parsers_nuage_create = subparsers_nuage.add_parser('create')
    parsers_nuage_delete = subparsers_nuage.add_parser('delete')
    parsers_nuage_show = subparsers_nuage.add_parser('show')
    parsers_nuage_assign = subparsers_nuage.add_parser('assign') 
    parsers_nuage_acl_load = subparsers_nuage.add_parser('acl-load')
    parsers_nuage_vspk_cli = subparsers_nuage.add_parser('vspk-cli')   
    
    # NUAGE LOAD
    parsers_nuage_load.add_argument('INFILE', nargs=1, type=argparse.FileType('r'),help='File in JSON format that contains test definition',default=sys.stdin)
    parsers_nuage_load.set_defaults(func=nuage_load)
    
    # NUAGE CLI
    parsers_nuage_vspk_cli.set_defaults(func=nuage_vspk_cli)
    
    # NUAGE acl LOAD
    parsers_nuage_acl_load.add_argument('--entname', nargs=1, help='Specific enterprise name this is related to (e.g. if searching for user inside enterprise you use entnema for enterprise and --filter for user filtering)', required=True)
    parsers_nuage_acl_load.add_argument('--domname', nargs=1, help='Specific domain name this acl load is related to', required=True)    
    #parsers_nuage_acl_load.add_argument('INFILE', nargs=1, type=argparse.FileType('r'),help='ACL definition file in YAML format',default=sys.stdin)
    parsers_nuage_acl_load.add_argument('--acl-yaml', '--acl', dest='YAML_FILE',  type=file, required=True, metavar='YAML_FILE', help='ACL definition file in YAML format')
    parsers_nuage_acl_load.set_defaults(func=nuage_load_acl_yaml)    
    
    #NUAGE SHOW
    parsers_nuage_show.add_argument('OBJECT',choices=['enterprises', 'domains', 'zones', 'subnets','users','groups','permissions','acls','dhcp-options','gateways'],help='Select what type of Nuage objects you would like listed')
    parsers_nuage_show.add_argument('--filter', nargs=1, help='Specific full name filter for enterprise/domain/zone/subnet/etc... while fetching', default="")
    parsers_nuage_show.add_argument('--tree', action='store_const', const=1, default=0, help='Works only with ENTERPRISES and shows a tree enterprise-domains-zones-subnets')
    parsers_nuage_show.add_argument('--entname', nargs=1, help='Specific enterprise name this is related to (e.g. if searching for user inside enterprise you use entnema for enterprise and --filter for user filtering)', default="")
    parsers_nuage_show.add_argument('--domname', nargs=1, help='Specific full name this is related to', default="")
    parsers_nuage_show.add_argument('--subnetname', nargs=1, help='Specific full name of subnet this is related to', default="")
    parsers_nuage_show.add_argument('--zonename', nargs=1, help='Specific full name of zone this is related to', default="")
    parsers_nuage_show.set_defaults(func=nuage_show)
    
    #NUAGE CREATE
    parsers_nuage_create.add_argument('OBJECT',choices=['acl','enterprise', 'domaintemplate', 'domain', 'zone', 'subnet','user','group','vtep','vlan-on-gateway','default-permit-acls','dhcp-option-121'],help='Select what type of Nuage objects you would like created')
    parsers_nuage_create.add_argument('--entname', nargs=1, help='Specific full name for new enterprise or enterprise parent for other objects... depending on what are you creating', default="")
    parsers_nuage_create.add_argument('--domtempname', nargs=1, help='Specific full name for new domain template or domain template parent for other objects... depending on what are you creating', default="")
    parsers_nuage_create.add_argument('--domname', nargs=1, help='Specific full name for new domain or domain parent for other objects... depending on what are you creating', default="")
    parsers_nuage_create.add_argument('--zonename', nargs=1, help='Specific full name for new zone or zone parent for other objects... depending on what are you creating', default="")
    parsers_nuage_create.add_argument('--subnetname', nargs=1, help='Specific full name for new subnet', default="")
    parsers_nuage_create.add_argument('--subnetNetworkIP', nargs=1, help='Network IP in X.X.X.X format', default="")
    parsers_nuage_create.add_argument('--subnetNetworkMask', nargs=1, help='Network Mask in X.X.X.X format', default="")
    parsers_nuage_create.add_argument('--username', nargs=1, help='Specific username for new user creation', default="")
    parsers_nuage_create.add_argument('--password', nargs=1, help='Specific password for new user creation', default="")
    parsers_nuage_create.add_argument('--firstname', nargs=1, help='Specific firstname for new user creation', default="")
    parsers_nuage_create.add_argument('--lastname', nargs=1, help='Specific lastname for new user creation', default="")
    parsers_nuage_create.add_argument('--useremail', nargs=1, help='Specific useremail for new user creation', default="")  
    parsers_nuage_create.add_argument('--groupname', nargs=1, help='Specific groupname for new group creation', default="") 
    parsers_nuage_create.add_argument('--dhcp-route-prefix', nargs=1, help='Specific prefix for dhcp option 121 route', default="")
    parsers_nuage_create.add_argument('--dhcp-route-prefix-mask', nargs=1, help='Specific prefix for dhcp option 121 route', default="")  
    parsers_nuage_create.add_argument('--dhcp-route-nexthop', nargs=1, help='Specific nexthop for dhcp option 121 routen', default="")
    parsers_nuage_create.add_argument('--gateway', nargs=1, help='Specific gateway', default="")
    parsers_nuage_create.add_argument('--gateway-interface', nargs=1, help='Specific interface on a gateway', default="")
    parsers_nuage_create.add_argument('--vlan-id', nargs=1, help='Specific vlan-id for gateway interface', default="")     
    parsers_nuage_create.set_defaults(func=nuage_create) 
    
    #NUAGE DELETE
    parsers_nuage_delete.add_argument('OBJECT',choices=['network_macros','network_macro_groups','acl','enterprise', 'domaintemplate', 'domain', 'zone', 'subnet','user','group','vtep','dhcp-options'],help='Select what type of Nuage objects you would like DELETED')
    parsers_nuage_delete.add_argument('--entname', nargs=1, help='Specific full name for new enterprise or enterprise parent for other objects... depending on what are you DELETING', default="")
    parsers_nuage_delete.add_argument('--domtempname', nargs=1, help='Specific full name for new domain template or domain template parent for other objects... depending on what are you DELETING', default="")
    parsers_nuage_delete.add_argument('--domname', nargs=1, help='Specific full name for new domain or domain parent for other objects... depending on what are you DELETING', default="")
    parsers_nuage_delete.add_argument('--zonename', nargs=1, help='Specific full name for new zone or zone parent for other objects... depending on what are you DELETING', default="")
    parsers_nuage_delete.add_argument('--subnetname', nargs=1, help='Specific full name for new subnet to DELETE', default="") 
    parsers_nuage_delete.add_argument('--tree', action='store_const', const=1, default=0, help='Works only with ENTERPRISES and destroys the entire enterprise') 
    parsers_nuage_delete.add_argument('--username', nargs=1, help='Specific username for new user deletion', default="")
    parsers_nuage_delete.add_argument('--groupname', nargs=1, help='Specific groupname for group deletion', default="")
    parsers_nuage_delete.add_argument('--vportname', nargs=1, help='Specific vport name', default="") 
    parsers_nuage_delete.set_defaults(func=nuage_delete)
    
    #NUAGE ASSIGN
    parsers_nuage_assign.add_argument('OBJECT',choices=['user-to-group','permission-for-group-to-domain','permission-for-group-to-zone','enterprise-to-gateway-vlan'],help='Select what type of Nuage objects you would like ASSIGNED')
    parsers_nuage_assign.add_argument('--entname', nargs=1, help='Specific full name for enterprise or enterprise that is either source or destination assignment', default="")
    parsers_nuage_assign.add_argument('--username', nargs=1, help='Specific full name for username that is either source or destination assignment', default="")
    parsers_nuage_assign.add_argument('--groupname', nargs=1, help='Specific full name for groupname that is either source or destination assignment', default="")
    parsers_nuage_assign.add_argument('--domname', nargs=1, help='Specific full name for  domain that is either source or destination assignment', default="")
    parsers_nuage_assign.add_argument('--zonename', nargs=1, help='Specific full name for zone that is either source or destination assignment', default="")
    parsers_nuage_assign.add_argument('--permission',choices=['USE','EXTEND','READ','INSTANTIATE','DEPLOY'],help='Select what type of Nuage permission you would like ASSIGNED')   
    parsers_nuage_assign.add_argument('--gateway', nargs=1, help='Specific gateway', default="")
    parsers_nuage_assign.add_argument('--gateway-interface', nargs=1, help='Specific interface on a gateway', default="")
    parsers_nuage_assign.add_argument('--vlan-id', nargs=1, help='Specific vlan-id for gateway interface', default="")     
    parsers_nuage_assign.set_defaults(func=nuage_assign)       
    
    # NUAGE ARGUMENTS
    #parser_nuage.add_argument('--object',choices=['create', 'show', 'delete'])
    #parser_nuage.add_argument('--command',choices=['create', 'show', 'delete'], required=True)
    #parser_nuage.add_argument('-ent', nargs=1, help='enterprise help', required=True)
    
    #parser_nuage.add_argument('enterprise', nargs='+', help='enterprise help')
    
    #parser_nuage.add_argument('-i', type=argparse.FileType('r'))
    #parser_nuage.add_argument('args', nargs=argparse.REMAINDER)
    #parser_nuage.add_argument('--foo', help='foo help')
    
    
    # Binding parsers to arges
    args = parser.parse_args()
    return_code = args.func(args)
    print("Return code:" + str(return_code))
    exit(return_code)
    
    
        
            
    
    
    
        