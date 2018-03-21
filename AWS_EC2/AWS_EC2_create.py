import boto	
import boto.vpc	
import time
region='us-west-1'	
ec2=boto.ec2.connect_to_region(region)	
vpccon = boto.vpc.connect_to_region(region)
#get	vpc-id	from	VPC	Dashboard	
vpcid ='vpc-xxxxx'
vpc = vpccon.get_all_vpcs(vpc_ids=[vpcid])[0];	
	
#getsecurity group id	
secgrpid='sg-xxxxxxx'
group = ec2.get_all_security_groups(group_ids=[secgrpid])[0]

#get	subnet	from	VPC	
sn=vpccon.get_all_subnets(filters={'vpcId':[vpcid]})	
sn1=sn[0]

#get KeyPair from Keypairs 	
keypairname= 'SSH_xxxxxx'


#  AMI-ID
amiid='ami-3a674d5a'

n_instance =2
instances_running=[]


for x in range(n_instance):
    ec2.run_instances(amiid, instance_type='t2.micro',security_group_ids=[group.id],subnet_id=sn1.id, key_name=keypairname)
    print "instance created: ",x+1
    time.sleep(10)


count = 0
while count<n_instance:
    reservations1 = ec2.get_all_reservations(filters={'instance-state-name': 'running'})
    for reservation1 in reservations1:
        for instance1 in reservation1.instances:
            count=count+1
            print "waiting for all instances to be running..: ",count
            time.sleep(8)
    
reservations0 = ec2.get_all_reservations()
print "reservationcount",reservations0
for reservation0 in reservations0:
    for instance0 in reservation0.instances:
        ec2.terminate_instances(instance_ids=instance0.id)
        print "shutting down instance ",instance0.id
        

  
