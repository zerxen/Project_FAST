##################
## PREPARATION: ##
##################
- log4j set to DEBUG mode on all four VRS boxes
- setup SSH to activate on all VRS boxes

1) CREATE NEW NUAGE ENTERPRISE + TOPOLOGY (120seconds)
python project_fast.py nuage load doc\full_test_case\nuage_topology.json

########################################################################
## REBOOT ALL ESX HOSTS (no maintenance mode, VRS running during reboot)
########################################################################

2) VTEPs ADD (40seconds)
python project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9
python project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private1 --subnetname subnet2 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9

python project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0
python project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0

python project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0
python project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0

python project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 0
python project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 0

3) TEST ALL THE L3VTEP SYSTEMS CAN COMMUNICATE
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test01_3xPSEUDO_1xPM.json
/// python project_fast.py ixchariot run session --id xx

###########################################
# CONTINUE ONLY IF TEST SUCCESFULL ########
###########################################

4) CREATE VMWARE VMs (4m creation + ~30sec boot)
python project_fast.py vmware load doc\mtu_dif\vmware_vms_part1.json
python project_fast.py vmware load doc\mtu_dif\vmware_vms_part2.json
python project_fast.py ixchariot run session --id 299


python project_fast.py ixchariot load doc\full_test_case\ixchariot_test19_40xVM_20onESX1-to-20onOtherESXs.json
echo DONE

#######################
# CONNECTIVITY TESTS ##
#######################

5) TEST FULL MESH CONNECTIIVTY
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test02_10xVM_3xPSEUDO_1xPM_mesh.json
/// python project_fast.py ixchariot run session --id X

6) TEST STAR CONNECTIIVTY FROM FOUR VMs [260]
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test03_10xVM_3xPSEUDO_1xPM_star.json

7) TEST STAR CONNECTIIVTY FROM VTEP
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test04_10xVM_3xPSEUDO_1xPM_star_on_VTEP.json

7) TEST STAR CONNECTIIVTY VIA OOB to VM ixia 137
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test05_10xVM_3xPSEUDO_1xPM_star_on_pseudo_VTEP.json

###########################################
# MTU PERFORMANCE TESTS ###################
###########################################

8) ONE ESX, TWO VMs on L2 [258]
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test06_two_vms_one_esx_L2.json

9) ONE ESX, TWO VMs on L3 [259]
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test07_two_vms_one_esx_L3.json

10) Two ESX, 2-3 VMs in each cross-performance (e.g. all VMs on ESX1 to all VMS on ESX1)
python project_fast.py ixchariot load doc\full_test_case\ixchariot_test08_ESX1_VMs_to_others.json


##################################################
## DELECTION AND REMOVAL SO YOU CAN START AGAIN ##
##################################################

7) DELETE VMS
python project_fast.py vmware delete vms-of-nuage-enterprise --entname AutomatedHelloWorld

8) DELETE NUAGE TOPOLOGY
python project_fast.py nuage delete enterprise --entname AutomatedHelloWorld --tree
