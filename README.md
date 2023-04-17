# get-all-publicip-aws
To run the Python script to get the public IPs of all network interfaces in a serverless manner in AWS, you can use AWS Lambda and AWS Step Functions. Here's a high-level overview of how you can set this up:

Create an S3 bucket to store your input CSV file and your Python script.

Upload your input CSV file and your Python script to the S3 bucket.

Create an IAM role that has the necessary permissions to access the S3 bucket, create and manage AWS Step Functions, and access the AWS accounts that you want to retrieve the public IPs from.

Create an AWS Step Functions state machine that triggers a Lambda function to retrieve the public IPs from the AWS accounts listed in the input CSV file.

Create a Lambda function that retrieves the input CSV file from the S3 bucket, reads the list of AWS accounts from the file, and retrieves the public IPs of all network interfaces in those accounts using the boto3 library.
Export the list of public IPs to a CSV file and upload it to the S3 bucket.

Configure AWS Step Functions to trigger the Lambda function when a new input CSV file is uploaded to the S3 bucket.

Here's an example of how the Python script for the Lambda function might look like:
