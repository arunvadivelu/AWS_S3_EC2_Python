
# -*- coding: utf-8 -*-
import boto
import time
import sys
class awws4():
 

    username = (sys.argv[1]).lower()
    pwd = (sys.argv[2])
    email = sys.argv[3]
    allBuckName="arun-ucsc-test4-allusersbucket"
    usrbucketname=(username+("-arun-ucsc-test4")).lower()
    keyString=pwd+","+email
    
    def create_bucket(conn,bucketname):
        bucket = conn.lookup(bucketname)
        if not bucket:
            print "new bucket to be created:",bucketname
            bucket=conn.create_bucket(bucketname,location="us-west-1")
            
        return bucket
         
    def create_key(bucket,keyname,keyString): 
        newkey=bucket.get_key(keyname)
        if not newkey:
            newkey=bucket.new_key(keyname)
            newkey.set_contents_from_string(keyString)
            newkey.set_acl('public-read')
        return newkey
    
    def update_key(bucket,keyname,keyString): 
        key=bucket.new_key(keyname)
        key.set_contents_from_string(keyString)
        stored_data =	key.get_contents_as_string()
        assert stored_data == keyString
        
    s3=boto.connect_s3()
    Allusrbucket = create_bucket(s3,allBuckName)
    time.sleep(5)
    userkey= create_key(Allusrbucket,username,keyString)
    usrbucket = create_bucket(s3,usrbucketname)
    obj=userkey.get_contents_as_string()   
    print obj	
    data = obj.split(",")
    if (data[0]!= pwd) or (data[1] != email):
        update_key(Allusrbucket,username,keyString)
        print "Pwd and Email updated.."
    else:
        print "Pwd and Email unchanged.."
            




