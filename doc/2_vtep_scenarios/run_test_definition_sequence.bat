@echo off
@echo %time%
ECHO All output will be in output.txt file
call :sub >output.txt
exit /b

:sub
rem
rem 1-0
ECHO 1-0
rem
@echo %time%
python ..\..\project_fast.py ixchariot load --silent 	1-0a_VM_to_VM_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	1-0a_VM_to_VM_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	1-0a_VM_to_VM_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	1-0a_VM_to_VM_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	1-0b_10VM_TCP_mesh.json
python ..\..\project_fast.py ixchariot load --silent 	1-0b_10VM_UDP_mesh.json
python ..\..\project_fast.py ixchariot load --silent 	1-1_VM_to_VM_TCP_bidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	1-1_VM_to_VM_UDP_bidirectional0.json
python ..\..\project_fast.py ixchariot load --silent 	1-2_VM_to_10VMs_TCP_bidirectional0.json
python ..\..\project_fast.py ixchariot load --silent 	1-2_VM_to_10VMs_TCP_unidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	1-2_VM_to_10VMs_UDP_bidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	1-2_VM_to_10VMs_UDP_unidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	1-3_10VM_to_10VMs_TCP_bidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	1-3_10VM_to_10VMs_UDP_bidirectional0.json
rem
rem 2-0
ECHO 2-0
rem
@echo %time%
python ..\..\project_fast.py ixchariot load --silent 	2-0a_1VM_to_1VMs_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-0a_1VM_to_1VMs_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	2-0a_1VM_to_1VMs_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-0a_1VM_to_1VMs_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	2-0b_10VM_to_10VMs_TCP_mesh.json
python ..\..\project_fast.py ixchariot load --silent 	2-0b_10VM_to_10VMs_TCP_source_single.json
python ..\..\project_fast.py ixchariot load --silent 	2-0b_10VM_to_10VMs_UDP_mesh.json
python ..\..\project_fast.py ixchariot load --silent 	2-0b_10VM_to_10VMs_UDP_source_single.json
python ..\..\project_fast.py ixchariot load --silent 	2-1a_one-to-one_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-1a_one-to-one_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	2-1a_one-to-one_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-1a_one-to-one_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	2-2_1-to-10_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-2_1-to-10_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	2-2_1-to-10_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-2_1-to-10_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	2-3_10-to-10_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-3_10-to-10_TCP_source_single.json
python ..\..\project_fast.py ixchariot load --silent 	2-3_10-to-10_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	2-3_10-to-10_UDP_source_single.json
rem
rem 3-0
ECHO 3-0
rem
@echo %time%
python ..\..\project_fast.py ixchariot load --silent 	3-0a_baseline_VTEP_performance_TCP_bidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	3-0a_baseline_VTEP_performance_UDP_bidirectional.json
python ..\..\project_fast.py ixchariot load --silent 	3-0c_10VM_to_4xVTEP_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-0c_10VM_to_4xVTEP_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	3-0c_10VM_to_4xVTEP_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-0c_10VM_to_4xVTEP_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	3-1_VMs-to-VTEP_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-1_VMs-to-VTEP_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	3-2_VMs-to-4VTEP_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-2_VMs-to-4VTEP_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	3-2_VMs-to-4VTEP_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-2_VMs-to-4VTEP_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	3-3_10VMs-to-4VTEP_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-3_10VMs-to-4VTEP_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	3-3_10VMs-to-4VTEP_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	3-3_10VMs-to-4VTEP_UDP_source.json
rem
rem 4-0
ECHO 4-0
rem
@echo %time%
python ..\..\project_fast.py ixchariot load --silent 	4-0_6VM_to_10VMs_and_4VTEPs_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	4-0_6VM_to_10VMs_and_4VTEPs_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	4-0_6VM_to_10VMs_and_4VTEPs_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	4-0_6VM_to_10VMs_and_4VTEPs_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	4-1_1VM-to-10+4_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	4-1_1VM-to-10+4_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	4-1_1VM-to-10+4_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	4-1_1VM-to-10+4_UDP_source.json
python ..\..\project_fast.py ixchariot load --silent 	4-2_6VM-to-10+4_TCP_any.json
python ..\..\project_fast.py ixchariot load --silent 	4-2_6VM-to-10+4_TCP_source.json
python ..\..\project_fast.py ixchariot load --silent 	4-2_6VM-to-10+4_UDP_any.json
python ..\..\project_fast.py ixchariot load --silent 	4-2_6VM-to-10+4_UDP_source.json
