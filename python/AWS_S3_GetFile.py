# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 23:19:08 2017

@author: yvaska
"""

import os.path
import time
import boto
import sys
class aws_GetFile():

    username= (sys.argv[1]).lower()
    pwd= sys.argv[2]
    keyname= sys.argv[3]
    fdownloadPath= (sys.argv[4]).replace("\\","/")
         
    
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
    
    def get_keyname(conn,bucket,keyname): 
        print "list of files in the user bucket:",str(bucket)
        #bucket = conn.lookup('bucket-name')
        for key in bucket:
            print key.name
        matchingfiles = [s.name for s in bucket if keyname in s.name]
        return matchingfiles
        
    def get_contetns(bucket,keyname,fname):
        fullfilename=fname+"/"+keyname
        key = bucket.get_key(keyname)
        key.get_contents_to_filename(fullfilename)
    
    def check_dir(dPath):    
       if os.path.isdir(dPath):
           return True
       else:
            os.makedirs(dPath)
            return True
            
    
    s3=boto.connect_s3() 
    Allusrbucket = get_mybucket(s3,allBuckName)
    time.sleep(5)  
    
    if check_dir(fdownloadPath): 
        
        if Allusrbucket:
            userkeyString= get_mykeyobj(Allusrbucket,username)
            usrbucket = get_mybucket(s3,usrbucketname)
    
            if Allusrbucket and usrbucket and userkeyString:
                data = userkeyString.split(",")
                if (data[0]== pwd) :
                    mymtachedlist= get_keyname(s3,usrbucket,keyname)
                    print "matched files to download:",mymtachedlist
                    for i in mymtachedlist:
                        get_contetns(usrbucket,i,fdownloadPath)
                
                else:
                    print "password does'nt match "
                    #print data[0]
            else:
                print "please use the CreateUser code object"
        else:
            print "User Buckets doesnt exist...please use the CreateUser object"
    else:
        
        print "DOwnload File directory does'nt exist..with double backslash or with forward slash like ./test.txt or within quotes '.\\test.txt'"
