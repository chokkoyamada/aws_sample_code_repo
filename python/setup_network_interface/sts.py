import json
import sys
import urllib2

import boto.ec2

response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/iam/security-credentials/general')
credential = json.loads(response.read())
ec2connection = boto.ec2.connect_to_region(
	'ap-northeast-1',
	aws_access_key_id=credential["AccessKeyId"],
	aws_secret_access_key=credential["SecretAccessKey"],
	security_token=credential["Token"]
)

response_instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = response_instance_id.read()

args = sys.argv
print ec2connection.attach_network_interface(args[1], instance_id, 2)
