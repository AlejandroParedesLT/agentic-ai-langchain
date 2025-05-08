import boto3
import json
from dotenv import load_dotenv
import os
load_dotenv()
# Step 1: Set AWS Credentials and Region
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_DEFAULT_REGION")

def main():
    # Create SageMaker client (not used in this example, but good to check credentials)
    sagemaker_client = boto3.client(
        'sagemaker-runtime',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    bucket_name = "testucketcredentials"  # Replace with your desired bucket name

    try:
        if region_name == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region_name}
            )
        print(f"Bucket {bucket_name} created successfully.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket {bucket_name} already exists and is owned by you.")
    except s3_client.exceptions.BucketAlreadyExists:
        print(f"Bucket {bucket_name} already exists and is owned by someone else.")
    except Exception as e:
        print(f"Error creating bucket: {e}")



    # Step 3: Define the SageMaker endpoint
    endpoint_name = "researcherAgent_api_endpoint"  # The endpoint name you want to access

    # Step 4: Prepare your payload (for a simple test, let's say we send a string input)
    payload = {
        "inputs": "Hello, can you generate something?"
    }

    # Step 5: Make the request to the endpoint
    try:
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        # Step 6: Process the response
        result = response['Body'].read().decode('utf-8')
        print("Response from SageMaker endpoint:", result)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()