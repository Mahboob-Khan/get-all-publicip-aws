import boto3
import csv

# Open the CSV file containing a list of AWS account IDs
with open('aws_accounts.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    # Create a list to store the public IP addresses
    public_ips = []
    # Iterate through each row in the CSV file
    for row in reader:
        account_id = row['account_id']
        # Create a new session for the AWS account
        session = boto3.Session(profile_name=f'aws-account-{account_id}')
        # Create an EC2 client object for the AWS account
        ec2 = session.client('ec2')
        # Retrieve a list of all network interfaces in the AWS account
        response = ec2.describe_network_interfaces()
        # Iterate through each network interface in the response
        for network_interface in response['NetworkInterfaces']:
            # Check if the network interface has a public IP address
            if 'Association' in network_interface and 'PublicIp' in network_interface['Association']:
                public_ip = network_interface['Association']['PublicIp']
                # Append the public IP address to the list
                public_ips.append({
                    'aws_account': account_id,
                    'network_interface_id': network_interface['NetworkInterfaceId'],
                    'public_ip': public_ip
                })

# Open a new CSV file to write the public IP addresses
with open('public_ips.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['aws_account', 'network_interface_id', 'public_ip'])
    writer.writeheader()
    # Write each public IP address to the CSV file
    for public_ip in public_ips:
        writer.writerow(public_ip)

print("Public IP addresses exported to public_ips.csv.")
