import boto3
from dotenv import load_dotenv
import os
load_dotenv()

region_name = boto3.Session().region_name

key_researchAgent_api_endpoint = "researcherAgent_api_endpoint" # this value is from GenerativeAiDemoWebStack
key_researchAgent_sm_endpoint = "ResearchAgent_sm_endpoint"   # this value is from GenerativeAiTxt2ImgSagemakerStack


def get_parameter(name):
    if os.getenv("AWS_ENV") == 'DEV' and os.getenv("LAMBDA_EXECUTION_ROLE") == 'DEV':
        raise NotImplementedError("This function is not implemented for local development. Please use the AWS credentials in the environment variables.")
    elif os.getenv("AWS_ENV") == 'DEV':
        ssm_client = boto3.client(
            "ssm",
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        response = ssm_client.get_parameter(Name=name)
        value = response["Parameter"]["Value"]
        return value
    else:
        """
        This function retrieves a specific value from Systems Manager"s ParameterStore.
        """     
        ssm_client = boto3.client("ssm",region_name=region_name)
        response = ssm_client.get_parameter(Name=name)
        value = response["Parameter"]["Value"]
        
        return value