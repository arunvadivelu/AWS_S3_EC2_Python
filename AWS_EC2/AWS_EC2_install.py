# Install Tomcat

import os,sys,time
import paramiko
import urllib2

def install2(ip_address, sshkeyfilename,keylocation):
    sshuser='ec2-user'
    os.chdir(keylocation)

    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sys.stderr.write("ip="+ip_address)

    ssh.connect(hostname=ip_address,username=sshuser,key_filename=sshkeyfilename)

    stdin, stdout, stderr = ssh.exec_command("sudo yum -y install tomcat6 tomcat6-webapps")
    stdin.flush()
    data = stdout.read().splitlines()
    print data [-1]

    #start Tomcat
    stdin, stdout, stderr = ssh.exec_command("sudo service tomcat6 start")
    stdin.flush()
    data = stdout.read().splitlines()
    print data [-1]

    stdin, stdout, stderr = ssh.exec_command("sudo service tomcat6 status")
    stdin.flush()
    data = stdout.read().splitlines()
    print data [-1]


    stdin, stdout, stderr = ssh.exec_command("sudo chmod 777 /usr/share/tomcat6/webapps")
    stdin.flush()

    ssh.exec_command("echo this is my Assignment 07 spin-up with ip: "+ ip_address+ " > remotefile.txt")
    stdin.flush()
    
    stdin, stdout, stderr = ssh.exec_command("sudo chmod o+rwx ./remotefile.txt")
    stdin.flush() 
    
    ssh.exec_command("sudo mkdir -p /usr/share/tomcat6/webapps/myApp")
    stdin.flush()

    stdin, stdout, stderr = ssh.exec_command("sudo chmod o+rwx /usr/share/tomcat6/webapps/myApp")
    stdin.flush()  
    
    stdin, stdout, stderr = ssh.exec_command("sudo chmod 777 /usr/share/tomcat6/webapps/myApp")
    stdin.flush()      
    
    ssh.exec_command("sudo mv ./remotefile.txt /usr/share/tomcat6/webapps/myApp/index.html")
    stdin.flush()
    
    url= "http://"+ip_address+":8080//myApp/index.html"
    sys.stdout.write(url)
    response = urllib2.urlopen(url)
    html = response.read()
    print(html)
    
    if len( html ) >0 :
            return "succesfully lauched and verified:"+url
    else:
            return "could not host:"+url
 

if __name__=='__main__':
    sys.stderr.write("sleeping\n")
    time.sleep(30)
    sys.stderr.write("wake up\n")
    ip=sys.argv[1]

    # user keypairs and paths that match your system
    keypair = 'SSH_xxxxxx'
    keyfile='SSH_xxxxxxx.pem'
    keypath='/home/xxxxxxx/Desktop/xxxxx'
    
    myreturn=install2(ip,keyfile,keypath)
    sys.stdout.write(myreturn)
    exit(0)
