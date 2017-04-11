1) CREATE NUAGE TOPOLOGY (120seconds)
python2 project_fast.py nuage load doc\example_full_test_case\test01\nuage_topology.json

2) CREATE VMWARE VMs (4m creation + ~30sec boot)
python2 project_fast.py vmware load doc\example_full_test_case\test01\vmware_vms.json

3) IxChariot TEST 01 (IGNORED DUE TIME):
python2 project_fast.py ixchariot load doc\example_full_test_case\test01\ixchariot_test01.json

4) VTEPs ADD (40seconds)
python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/33" --vlan-id 8 
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/33" --vlan-id 8 

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 8 
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.43 --gateway-interface "usplnACvpclab1002:::Ten-GigabitEthernet1/0/34" --vlan-id 8 

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 8 
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/33" --vlan-id 8 

python2 project_fast.py nuage assign enterprise-to-gateway-vlan --entname AutomatedHelloWorld --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 8 
python2 project_fast.py nuage create vtep --entname AutomatedHelloWorld --domname Instance1 --zonename private2 --subnetname subnet3 --gateway 29.203.0.44 --gateway-interface "usplnACvpclab1001:::Ten-GigabitEthernet1/0/34" --vlan-id 8 

5) VTEP IxChariot tests (5minutes)
python2 project_fast.py ixchariot load doc\example_full_test_case\test01\ixchariot_test02_vteps.json

6) DELETE VMS
python2 project_fast.py vmware delete vms-of-nuage-enterprise --entname AUtomatedHelloWorld

7) DELETE NUAGE TOPOLOGY
python2 project_fast.py nuage delete enterprise --entname AutomatedHelloWorld --tree
