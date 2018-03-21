#!/usr/bin/env python2
#-*- coding: utf-8 -*-


# Start Ec2 Instance

import os,sys,time
import boto
import boto.vpc
import boto.vpc.vpc
import paramiko
import urllib2

def startinstance(ami_instance, securitygroup, sshkeyfilename, keylocation, vpcid, delete):
    instance_type='t2.micro'
    os.chdir(keylocation) # require path for pem file
    ec2 = boto.connect_ec2()
    ec2 = boto.ec2.connect_to_region('us-west-1')

    vpccon = boto.vpc.connect_to_region('us-west-1')
    vpc = vpccon.get_all_vpcs(vpc_ids=[vpcid])[0]
    sn = vpccon.get_all_subnets(filters={'vpc-id':[vpc.id]})[0]

    group = ec2.get_all_security_groups(group_ids=[securitygroup])[0]

    key = ec2.get_all_key_pairs(keynames=[sshkeyfilename])[0]

    reservation = ec2.run_instances(ami_instance,
                                    instance_type=instance_type,
                                    security_group_ids=[group.id],
                                    subnet_id=sn.id,
                                    key_name=key.name)

    # wait for the instance to start
    instance = reservation.instances[0]
    # print instance, instance state, 'queued to start'

    while instance.state != 'running':
        #print "."
        instance.update()

    #print " "
    #print instance
    #print instance, 'started'

    return instance.ip_address+","+instance.id

if __name__=='__main__':

    count = 1
    ami_instance = 'ami-3a674d5a'

    #change variables to match yours
    securitygroup = 'sg-xxxxxx'
    secGroupId = 'sg-xxxxxx'

    
    vpcid = 'vpc-7fd9bc1b'
    delete = False
    keyfile = 'SSH_keypair01.pem'
    keylocation = '/home/xxxxxx/Desktop/xxxxxx'
    keypair = 'SSH_xxxxxxx'

    
    ip = startinstance(ami_instance, securitygroup, keypair, keylocation, vpcid, delete)

    sys.stdout.write(ip)
