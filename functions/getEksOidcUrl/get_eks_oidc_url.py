import logging
from crhelper import CfnResource
import boto3
import json

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=True, log_level='INFO')

@helper.create
@helper.update
def create_update_handler(event, _):
    """
    Handler for create and update actions.
    :param cluster_name: EKS Cluster name
    """
    cluster_name = event['ResourceProperties']['cluster_name']
    logging.info('EKS Cluster name is: %s', cluster_name)
    oidc_response_url = fetchClusterOIDC(cluster_name)
    oidc_response=oidc_response_url.split("https://")[1]
    helper.Data.update({"oidc": oidc_response})
    return oidc_response

def fetchClusterOIDC(cluster_name):
    logging.info("Getting Cluster OIDC value for cluster name "+ cluster_name)
    oidc = ''
    client = boto3.client('eks')
    try:
      response = client.describe_cluster(
          name=cluster_name
      )
      if response['ResponseMetadata']['HTTPStatusCode'] == 200:
          logging.info("Success response recieved for describing cluster "+ cluster_name)
          oidc = (response['cluster']['identity']['oidc']['issuer'])
          logging.info('OIDC output recieved '+ oidc + ' for Cluster Name ' + cluster_name)
      return oidc
    except Exception as e:
      logging.info('Failed to fetch Cluster OIDC value for cluster name ' + cluster_name, e)

def lambda_handler(event, context):
        helper(event, context)
