# -*- coding: utf-8 -*-


# Shutdown Ec2 Instance

import sys
import boto
import boto.vpc
import boto.vpc.vpc

def check_ninstance():
    region='us-west-1'	
    ec2=boto.ec2.connect_to_region(region)	

    instlist=ec2.get_all_instances()
    reservations = ec2.get_all_reservations(filters={'instance-state-name': 'running'})
    print "total number of instances:", len(instlist)
    print "total number of running instances:", len(reservations)
    for reservation in reservations:
        for instance in reservation.instances:
            ec2.terminate_instances(instance_ids=instance.id)
            print "shutting down instance ",instance.id
    return len(reservations)       

if __name__=='__main__':

    #install2(ip,keyfile,keypath)
    n_stopped=str(check_ninstance())
    sys.stdout.write(n_stopped)
    exit(0)
