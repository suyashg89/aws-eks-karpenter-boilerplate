## configureEksOidcProvider

This lambda function is create IAM OIDC provider.
Ref: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html

This will only be triggered during the create or update of the cloudforamtion template.

### Lambda Function IAM Role policies
  - EKSAccess - Describe cluter config
  - CloudWatchLogsAccess - Create log groups and write Lambda logs to CloudWatch
