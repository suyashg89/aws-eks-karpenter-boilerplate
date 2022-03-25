## getEksOidcUrl

This lambda function is fetch the OIDC url from the control plane.

This will only be triggered during the create or update of the cloudforamtion template.

### Lambda Function IAM Role policies
  - EKSAccess - Describe cluter config
  - CloudWatchLogsAccess - Create log groups and write Lambda logs to CloudWatch
