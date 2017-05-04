1) CREATE NUAGE TOPOLOGY (120seconds)
python2 project_fast.py nuage load doc\example_full_test_case\test02_3nic\nuage_topology.json

2) CREATE VMWARE VMs (4m creation + ~30sec boot)
python2 project_fast.py vmware load doc\example_full_test_case\test02_3nic\vmware_vms.json

3) VTEPs ADD (40seconds)
python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private1 --subnetname subnet2 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 9

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 0

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/11" --vlan-id 0

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/33" --vlan-id 0
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/33" --vlan-id 0

4) IxChariot TEST 01 (IGNORED DUE TIME):
python2 project_fast.py ixchariot load doc\example_full_test_case\test02_3nic\ixchariot_test01_4xVM_3xPSEUDO_1xPM.json

6) DELETE VMS
python2 project_fast.py vmware delete vms-of-nuage-enterprise --entname AutomatedHelloWorld

7) DELETE NUAGE TOPOLOGY
python2 project_fast.py nuage delete enterprise --entname AutomatedHelloWorld --tree
