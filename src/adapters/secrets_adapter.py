import json

import boto3
from botocore.exceptions import ClientError



class SecretsAdapter:
    def __init__(self):
        self.region_name = "us-east-1"


    def get_secret(self, secret_name="estudart-sentiment-data-collector"):
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as err:
            raise err

        secret = get_secret_value_response['SecretString']
        
        return json.loads(secret)
