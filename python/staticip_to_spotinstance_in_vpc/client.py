import json
import optparse
import sys
import urllib2

import boto.ec2

# parse args
parser = optparse.OptionParser()
parser.add_option('-e', '--eni_id', dest='eni_id')
parser.add_option('-r', '--iam_role', dest='iam_role')
parser.add_option('-t', '--target_iam_role', dest='target_iam_role')
options, reminder = parser.parse_args()

# create ec2connection instance
response =
urllib2.urlopen('http://169.254.169.254/latest/meta-data/iam/security-credentials/'
+ options.target_iam_role)
credential = json.loads(response.read())
ec2connection = boto.ec2.connect_to_region(
	'ap-northeast-1',
	aws_access_key_id=credential["AccessKeyId"],
	aws_secret_access_key=credential["SecretAccessKey"],
	security_token=credential["Token"]
)

# attach eni
response_instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = response_instance_id.read()
print ec2connection.attach_network_interface(options.eni_id, instance_id, 2)
