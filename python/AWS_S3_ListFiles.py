# -*- coding: utf-8 -*-

import sys
import time
import boto
class aws_ListFiles():

       
    #username="username01"
    #pwd="pwd1122"
    username= (sys.argv[1]).lower()
    pwd= sys.argv[2]    
    
    allBuckName="arun-ucsc-test4-allusersbucket"
    usrbucketname=(username+("-arun-ucsc-test4")).lower()

    def get_mybucket(conn,bucketname):
        bucket = conn.lookup(bucketname)
        if not bucket:
            print "bucket doesnt exist:",bucketname            
        return bucket
         
    def get_mykeyobj(bucket,keyname): 
        newkey=bucket.get_key(keyname)
        if not newkey:
            print "key for the user doesnt exist:",keyname 
        else: 
            obj=newkey.get_contents_as_string()  
            return obj
    
    def list_all(conn,bucket): 
        print "list of files in the user bucket:",str(bucket)
        #bucket = conn.lookup('bucket-name')
        for key in bucket:
            print key.name
    
    s3=boto.connect_s3() 
    Allusrbucket = get_mybucket(s3,allBuckName)
    time.sleep(5)  
        
    if Allusrbucket:
        userkeyString= get_mykeyobj(Allusrbucket,username)
        usrbucket = get_mybucket(s3,usrbucketname)
    
        if Allusrbucket and usrbucket and userkeyString:
            data = userkeyString.split(",")
            if (data[0]== pwd) :
                list_all(s3,usrbucket)
                
            else:
                print "password does'nt match "
                    #print data[0]
        else:
            print "please use the CreateUser code object"
    else:
            print "User Buckets doesnt exist...please use the CreateUser object"
