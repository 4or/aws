import boto3
import sys
import ipaddress 
import urllib.request as urllib2

"""
                To use this script you should first configure aws cli with the secret and access key and region, after that run this script

                                            To run this script you should first pass paramater ( insertip or removeip )
                                            Let's say we want to give access to the ip ( 192.168.1.1 )

                                            step 1: python3 waf-ip-set-automation.py insertip
                                            When you run it you will get information like this
                                            INFO: Below array start counting from zero: 0
                                            ['ahmedaccess', 'azureaccess', 'endpointdetection']
                                            Choose from 0 to 2 to select the name:
                                            
                                            Now choose the index of  the WAF IP Set you want to work with ( let's say ahmedaccess )
                                            step 2: type the index of ahmedaccess
                                            Choose from 0 to 2 to select which aws waf set: 0
                                            Next you will get this 
                                            Enter IP address: 
                                            step 3: type the ip address
                                            For example
                                                Enter IP address: 192.168.1.1
                                            Now the new change was made in aws waf ip set
                
                Note: you should first create WAF IP SETs to work with this script

"""
    
if len(sys.argv) == 1:
    print('PLEASE GIVE ARGUMENT [insertip,removeip]')
    sys.exit(0) 

# checking network connection before execute the script 
# if no connection exist the script will not get executed
try:
    urllib2.urlopen('https://google.com', timeout=1)
except : 
    print("ERROR can't make network connection to AWS endpoint!")
    sys.exit() 

waf_client = boto3.client("wafv2", region_name="us-east-2")

def insert_to_set(Name,Id,arr,LockToken,IP):
    arr.append(IP)
    waf_client.update_ip_set(Name=Name,Scope='REGIONAL',Id=Id,Addresses=arr,LockToken=LockToken)
 

def set_up_handler(IpSetName,IPs):    
    for i in waf_client.list_ip_sets(Scope="REGIONAL")["IPSets"]:   
        if i["Name"] == IpSetName: 
            Name = i["Name"]
            Id = i["Id"]
            LockToken = i["LockToken"]
            arr = waf_client.get_ip_set(Name=Name,Scope='REGIONAL',Id="{}".format(i["Id"]))["IPSet"]["Addresses"]
            if len(arr) > 0:
                # Here we are checking if the given ip is in waf ip set and if not the ip will get inserted
                if IPs in arr:
                    print("Found IP [{0}] in waf ip set named [{1}]! No action".format(IPs,Name))
                    break
                else: 
                    print("IP [{0}] was add to AWS WAF! ".format(IPs))
                    insert_to_set(Name,Id,arr,LockToken,IPs)                    
                    return ""
            else: 
                print("IP [{0}] was add to AWS WAF! ".format(IPs))
                insert_to_set(Name,Id,arr,LockToken,IPs)
    return ""


def executing_handler():
    list_set = []
    for i in waf_client.list_ip_sets(Scope="REGIONAL")["IPSets"]:
        list_set.append(i["Name"])  
    print("INFO: Below array start counting from zero: 0")
    print(list_set)
    while True:
        try: 
            integer = int(input("Choose from 0 to {0} to select the name: ".format(len(list_set) -1)))
        except ValueError:
            print("Please, enter a valid integer")
            continue
        except KeyboardInterrupt:
            print("Bye")
            sys.exit()
        try:
            ip = ipaddress.ip_address(input("Enter IP address: "))
        except ValueError:
            print("Please, enter a valid IP")
            continue
        except KeyboardInterrupt:
            print("Bye")
            sys.exit()
        else:
            if  integer <= len(list_set) -1 and integer >=0: 
                if sys.argv[1] == "insertip" :
                    # add ip to aws waf
                    set_up_handler(list_set[integer],"{0}/32".format(ip))
                elif sys.argv[1] == "removeip":
                    # remove ip from aws waf
                    remove_ip_from_ipset_handlers(list_set[integer],"{0}/32".format(ip)) 
                else:
                    print("use correct  syntax [insertip,removeip]")
                
                # continue
            else:
                print("The number you choosed [{0}] is out of range ".format(integer))
                continue
            break

 
# remove ip from aws waf
def remove_ip_from_ipset_handlers(IpSetName,IPs):    
    for i in waf_client.list_ip_sets(Scope="REGIONAL")["IPSets"]:   
        if i["Name"] == IpSetName: 
            Name = i["Name"]
            Id = i["Id"]
            LockToken = i["LockToken"]
            arr = waf_client.get_ip_set(Name=Name,Scope='REGIONAL',Id="{}".format(i["Id"]))["IPSet"]["Addresses"]
            if len(arr) > 0: 
                if IPs in arr:
                    arr.remove(IPs)
                    waf_client.update_ip_set(Name=Name,Scope='REGIONAL',Id=Id,Addresses=arr,LockToken=LockToken)
                    print("IP [{0}] was removed from AWS WAF! ".format(IPs))
                    break
                else: 
                    print("IP [{0}] not found in AWS WAF!".format(IPs))                    
                    return "" 
    return ""

executing_handler()