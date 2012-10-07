import json
import optparse
import urllib2
import sys

import boto.ec2

# parse args
parser = optparse.OptionParser()
parser.add_option('-e', '--eni_id', dest='eni_id')
parser.add_option('-r', '--iam_role', dest='iam_role')
parser.add_option('-t', '--target_iam_role', dest='target_iam_role')
parser.add_option('-a', '--iam_arn', dest='iam_arn')
parser.add_option('-p', '--price', dest='price')
parser.add_option('-k', '--key', dest='key')
parser.add_option('-s', '--sg_id', dest='sg_id')
parser.add_option('-i', '--ami', dest='ami')
parser.add_option('-n', '--subnet', dest='subnet')
options, reminder = parser.parse_args()

# create a ec2connection instance
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/iam/security-credentials/' + options.iam_role)
credential = json.loads(response.read())
ec2connection = boto.ec2.connect_to_region(
	'ap-northeast-1',
	aws_access_key_id=credential["AccessKeyId"],
	aws_secret_access_key=credential["SecretAccessKey"],
	security_token=credential["Token"]
)

# make a spot_instance request
user_data = "#!/bin/bash -ex \n python /usr/local/staticip_to_spotinstance_in_vpc/client.py -e" + options.eni_id + " -t " + options.target_iam_role
request_spot_instance = ec2connection.request_spot_instances(
	options.price,
	options.ami,
	user_data=user_data,
	key_name=options.key, 
	subnet_id=options.subnet,
	security_group_ids=[options.sg_id],
	instance_profile_arn=options.iam_arn
)

print request_spot_instance
