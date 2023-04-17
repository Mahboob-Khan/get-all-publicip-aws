import boto3
import csv
import os

def lambda_handler(event, context):
    # Get the S3 bucket and key for the input CSV file
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the input CSV file from S3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.download_file(key, '/tmp/input.csv')
    
    # Read the list of AWS accounts from the input CSV file
    accounts = []
    with open('/tmp/input.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            accounts.append({'account_id': row[0], 'role_arn': row[1]})
    
    # Retrieve the public IPs of all network interfaces in each AWS account
    ec2 = boto3.client('ec2')
    public_ips = []
    for account in accounts:
        sts = boto3.client('sts')
        assumed_role = sts.assume_role(
            RoleArn=account['role_arn'],
            RoleSessionName='AssumeRoleSession'
        )
        credentials = assumed_role['Credentials']
        ec2 = boto3.client('ec2',
                           aws_access_key_id=credentials['AccessKeyId'],
                           aws_secret_access_key=credentials['SecretAccessKey'],
                           aws_session_token=credentials['SessionToken'])
        response = ec2.describe_network_interfaces(Filters=[{'Name': 'addresses.public-ip', 'Values': ['*']}])
        for interface in response['NetworkInterfaces']:
            for address in interface['PrivateIpAddresses']:
                if 'Association' in address and 'PublicIp' in address['Association']:
                    public_ips.append({'account_id': account['account_id'], 'public_ip': address['Association']['PublicIp']})
    
    # Export the public IPs to a CSV file and upload it to S3
    with open('/tmp/public_ips.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in public_ips:
            writer.writerow([row['account_id'], row['public_ip']])
    
    s3.meta.client.upload_file('/tmp/public_ips.csv', bucket_name, 'public_ips.csv')
