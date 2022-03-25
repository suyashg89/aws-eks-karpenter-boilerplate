import logging
import boto3
from botocore.exceptions import ClientError
import json
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=True, log_level='INFO')

try:
    iam = boto3.client("iam")
except Exception as init_exception:
    helper.init_failure(init_exception)

@helper.create
def create_handler(event, _):
    """
    Handler for create action.
    :param oidc_issuer_url: OIDC issuer url
    """
    oidc_issuer_url = event['ResourceProperties']['OIDCIssuerURL']
    logging.info('OIDC issuer url ' + ' is ' + oidc_issuer_url )
    # This is the ca thumbprint of AWS's issuer
    issuer_thumbprint = '9e99a48a9960b14926bb7f3b02e22da2b0ab7280'
    resp = iam.create_open_id_connect_provider(Url=oidc_issuer_url,ClientIDList=['sts.amazonaws.com'],ThumbprintList=[issuer_thumbprint])
    provider_arn = resp['OpenIDConnectProviderArn']
    logging.info('OIDC Provider is created: %s', provider_arn)
    logging.info(resp)
    return provider_arn

@helper.delete
def delete_handler(event, _):
    provider_arn = event["PhysicalResourceId"]
    resp = iam.delete_open_id_connect_provider(OpenIDConnectProviderArn=provider_arn)
    logging.info('OIDC Provider is deleted: %s', provider_arn)
    logging.info(resp)

def lambda_handler(event, context):
        helper(event, context)
