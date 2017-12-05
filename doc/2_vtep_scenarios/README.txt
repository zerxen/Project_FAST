##################
## PREPARATION: ##
##################
- log4j set to DEBUG mode on all four VRS boxes
- setup SSH to activate on all VRS boxes

1) CREATE NEW NUAGE ENTERPRISE + TOPOLOGY (120seconds)
python ..\..\project_fast.py nuage load nuage_topology.json

########################################################################
## REBOOT ALL ESX HOSTS (no maintenance mode, VRS running during reboot)
########################################################################

2) VTEPs ADD (40seconds)
python ..\..\project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9
python ..\..\project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private1 --subnetname subnet2 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9

python ..\..\project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0
python ..\..\project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0

python ..\..\project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0
python ..\..\project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0

python ..\..\project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 0
python ..\..\project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 0

#3) TEST ALL THE L3VTEP SYSTEMS CAN COMMUNICATE
#python ..\..\project_fast.py ixchariot load 1-0_5xVTEP_PMs.json
#/// python ..\..\project_fast.py ixchariot run session --id 68

python ..\..\project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/12" --vlan-id 0
python ..\..\project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/12" --vlan-id 0

python ..\..\project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/12" --vlan-id 0
python ..\..\project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/12" --vlan-id 0

###########################################
# ACTIVE/ACTIVE test on phy1       ########
###########################################

python ..\..\project_fast.py ixchariot load 1-1_10xVM_5xVTEP_phy1_star.json

###########################################
# ACLs test on 10xVM and 4x VTEP   ########
###########################################

# Load VMs
python ..\..\project_fast.py vmware load vmware_vms_part1.json

# Run TEST designed to test ACLs
//python ..\..\project_fast.py ixchariot run session --id 69
python ..\..\project_fast.py ixchariot load 1-2_5xVM_4xVTEP_full_mesh.json

##################################################
## DELECTION AND REMOVAL SO YOU CAN START AGAIN ##
##################################################

7) DELETE VMS
python ..\..\project_fast.py vmware delete vms-of-nuage-enterprise --entname AutomatedHelloWorld

8) DELETE NUAGE TOPOLOGY
python project_fast.py nuage delete enterprise --entname AutomatedHelloWorld --tree
