# -*- coding: utf-8 -*-
import boto
import os.path
import uuid
import sys
class aws_upload():
        

    username= (sys.argv[1]).lower()
    pwd= sys.argv[2]
    keyname= sys.argv[3]
    
    fname= (sys.argv[4]).replace("\\","/")
    print "your filename:",fname
    
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
    
    def uploadfromFile(bucket,fname,keyname):
        
            newkey=bucket.new_key(keyname+"-"+str(uuid.uuid4())[:8])
            newkey.set_contents_from_filename(fname)
            newkey.set_acl('public-read')
            print "File succesfully uploaded.. "
    
    s3=boto.connect_s3()     
    Allusrbucket = get_mybucket(s3,allBuckName)

    
    if os.path.isfile(fname):        
        
        if Allusrbucket:
            userkeyString= get_mykeyobj(Allusrbucket,username)
            usrbucket = get_mybucket(s3,usrbucketname)
    
            if Allusrbucket and usrbucket and userkeyString:
                data = userkeyString.split(",")
                if (data[0]== pwd) and (os.path.isfile(fname)):
                
                    uploadfromFile(usrbucket,fname,keyname)
                                
                else:
                    print "password does'nt match "
                    #print data[0]
            else:
                print "please use the CreateUser to create credentials for this user"
        else:
            print "User Buckets doesnt exist...please use the CreateUser object"
    else:
        print "file doesnt exisit. use the file convention: with double backslash or with forward slash like ./test.txt or within quotes '.\\test.txt' "
   
