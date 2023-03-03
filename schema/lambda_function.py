import json
import os
import boto3
from graphql import graphql_sync
from baseball_schema import schema

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get the module file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    module_code = response['Body'].read().decode('utf-8')
    
    # Load the module dynamically
    module = compile(module_code, key, 'exec')
    exec(module)
    
    # Get the GraphQL query and variables
    query = event.get('query')
    variables = event.get('variables')
    
    # Execute the GraphQL query
    result = graphql_sync(
        schema,
        query,
        variables=variables
    )
    
    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps(result.data)
    }
