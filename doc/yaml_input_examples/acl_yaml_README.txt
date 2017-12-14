# YAML DEFINITION FILE FOR AN ACL TO BE LOADED BY Project_FAST SCRIPT
#=====================================================================




action='FORWARD',
description='FULL Learning',
ether_type='0x0800',
flow_logging_enabled=True,
location_type='ANY',
network_type='ANY',
priority=1001,
protocol=17,
reflexive=True,
source_port='*',
destination_port='*',
dscp='*

action='FORWARD',
description='Allow MySQL DB connections from Web Tier',
ether_type='0x0800',
location_type='ZONE',
location_id=from_network.id,
network_type='ZONE',
network_id=to_network.id,
protocol='6',
source_port='*',
destination_port='3306',
dscp='*'


action='FORWARD',
description='Allow HTTP connections between Web-NET VMs',
ether_type='0x0800',
location_type='SUBNET',
location_id=network.id,
network_type='SUBNET',
network_id=network.id,
protocol='6',
source_port='*',
destination_port='80',
dscp='*'





# Creating the job to begin the policy changes
job = vsdk.NUJob(command='BEGIN_POLICY_CHANGES')
domain.create_child(job)
# wait for the job to finish
# can be done with a while loop

# Creating a new Ingress ACL
ingressacl = vsdk.NUIngressACLTemplate(
    name='Middle Ingress ACL',
    priority_type='NONE', # Possible values: TOP, NONE, BOTTOM (domain only accepts NONE)
    priority=100,
    default_allow_non_ip=False,
    default_allow_ip=False,
    allow_l2_address_spoof=False,
    active=True
    )
domain.create_child(ingressacl)

# Creating a new Ingress ACL rule to allow database connectivity
# from the Web-Tier Zone to the DB-Tier Zone
from_network = domain.zones.get_first(filter='name == "Web-Tier"')
to_network = domain.zones.get_first(filter='name == "DB-Tier"')
db_ingressacl_rule = vsdk.NUIngressACLEntryTemplate(
    action='FORWARD',
    description='Allow MySQL DB connections from Web Tier',
    ether_type='0x0800',
    location_type='ZONE',
    location_id=from_network.id,
    network_type='ZONE',
    network_id=to_network.id,
    protocol='6',
    source_port='*',
    destination_port='3306',
    dscp='*'
    )
ingressacl.create_child(db_ingressacl_rule)

# Creating a new Ingress ACL rule to allow Web-Net VMs to
# talk to each other on port 80
network = domain.subnets.get_first(filter='name == "Web-Net"')
web_ingressacl_rule = vsdk.NUIngressACLEntryTemplate(
    action='FORWARD',
    description='Allow HTTP connections between Web-NET VMs',
    ether_type='0x0800',
    location_type='SUBNET',
    location_id=network.id,
    network_type='SUBNET',
    network_id=network.id,
    protocol='6',
    source_port='*',
    destination_port='80',
    dscp='*'
    )
ingressacl.create_child(web_ingressacl_rule)

# Applying the changes to the domain
job = vsdk.NUJob(command='APPLY_POLICY_CHANGES')
domain.create_child(job)