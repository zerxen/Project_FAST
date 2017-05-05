##################
## PREPARATION: ##
##################
- log4j set to DEBUG mode on all four VRS boxes
- setup SSH to activate on all VRS boxes

1) CREATE NEW NUAGE ENTERPRISE + TOPOLOGY (120seconds)
python2 project_fast.py nuage load doc\full_test_case\nuage_topology.json

########################################################################
## REBOOT ALL ESX HOSTS (no maintenance mode, VRS running during reboot)
########################################################################

2) VTEPs ADD (40seconds)
python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private1 --subnetname subnet2 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 0
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 0

3) TEST ALL THE L3VTEP SYSTEMS CAN COMMUNICATE
python2 project_fast.py ixchariot load doc\full_test_case\ixchariot_test01_3xPSEUDO_1xPM.json

###########################################
# CONTINUE ONLY IF TEST SUCCESFULL ########
###########################################

4) CREATE VMWARE VMs (4m creation + ~30sec boot)
python2 project_fast.py vmware load doc\full_test_case\vmware_vms.json

###########################################
# CONNECTIVITY TESTS ######################
###########################################

5) TEST FULL MESH CONNECTIIVTY
python2 project_fast.py ixchariot load doc\full_test_case\ixchariot_test01_3xPSEUDO_1xPM.json

6) TEST STAR CONNECTIIVTY FROM TWO VMs
python2 project_fast.py ixchariot load doc\example_full_test_case\test02_3nic\ixchariot_test01_4xVM_3xPSEUDO_1xPM.json

##################################################
## DELECTION AND REMOVAL SO YOU CAN START AGAIN ##
##################################################

7) DELETE VMS
python2 project_fast.py vmware delete vms-of-nuage-enterprise --entname AutomatedHelloWorld

8) DELETE NUAGE TOPOLOGY
python2 project_fast.py nuage delete enterprise --entname AutomatedHelloWorld --tree
