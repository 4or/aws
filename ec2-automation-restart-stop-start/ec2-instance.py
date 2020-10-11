
import boto3
import sys

"""
	
	GitHub:  https://github.com/ahmedbejaouiJS
"""
"""

	this script can start stop or reboot ec2 instance all you need is to login to your aws console account with aws cli to let boto3 locate ( credentials ) file in path ~/.aws
	nano or vi into  ~/.aws/credentials and put region={ your region } under [default] 

	-----> { your region } is where the instance is located
	-----> aws_regions = ['eu-central-1','ap-southeast-1','ap-northeast-1','us-east-1','us-west-2','us-west-1','eu-west-1' ,'ap-southeast-2','ap-northeast-2','sa-east-1']


"""

def main(instance_id): 
	 
	if len(sys.argv) == 1:
		print('PLEASE GIVE ARGUMENT [start,stop,reboot]')
		sys.exit(0)
	elif sys.argv[1] == "start" :
		start_instance(instance_id)
	elif sys.argv[1] == "stop":
		stop_instance(instance_id)
	elif sys.argv[1] == "reboot":
		restart_instance(instance_id)
	else:
		print("use correct  syntax [start,stop,reboot]") 
 

def stop_instance(instance_id):
 
	print("Attempt on stoping  Instance Id : {0} ".format(instance_id))
	ec2 = None 
	try:
		ec2 = boto3.client('ec2') 
	except Exception as ec: 
		print("Oops!! %s " % str(ec))
		sys.exit(0)
	try: 
		inc2 = ec2.describe_instance_status(InstanceIds=[ instance_id ])

		for i in inc2['InstanceStatuses']:
			if i['InstanceState']['Name'] == "running": 
				starting = ec2.stop_instances(  InstanceIds=[instance_id] )
				# print(i)
				print("Instance get stoped : {0} ".format(instance_id))
			else:
			  	print("Oops!! it looks like instance %s have some problem" % str(instance_id)) 
	except Exception as ei: 
		print("Oops!! %s" % str(ei))
		sys.exit(0)

def start_instance(instance_id):
 
	print("Attempt on starting the Instance Id : {0} ".format(instance_id))
	ec2 = None 
	try:
		ec2 = boto3.client('ec2') 
	except Exception as ec: 
		print("Oops!! %s " % str(ec))
		sys.exit(0)
	try:  
	   starting = ec2.start_instances(  InstanceIds=[instance_id] )
	   print("Instance get started : {0} ".format(instance_id)) 
	except Exception as ei: 
		print("Oops!! %s" % str(ei))
		sys.exit(0)



def restart_instance(instance_id):
 
	print("Attempt on rebooting the Instance Id : {0} ".format(instance_id))
	ec2 = None 
	try:
		ec2 = boto3.client('ec2') 
	except Exception as ec: 
		print("Oops!! %s " % str(ec))
		sys.exit(0)
	try: 
		inc2 = ec2.describe_instance_status(InstanceIds=[ instance_id ])

		for i in inc2['InstanceStatuses']:
			if i['InstanceState']['Name'] == "running": 
				response = ec2.reboot_instances(  InstanceIds=[instance_id] )
				# print(i)
				print("Instance get rebooted : {0} ".format(instance_id))
			else:
			  	print("Oops!! it looks like instance %s have some problem" % str(instance_id)) 
	except Exception as ei: 
		print("Oops!! %s" % str(ei))
		sys.exit(0)

 
instance_id = 'i-0f50a8d5e90f7b3d7'
main(instance_id) 