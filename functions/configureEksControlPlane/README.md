## configureEksControlPlane

This lambda function is to configure the control plane with the below

- Enable cloudwatch
- Enable public. private or private and private access of the endpoint
- Append the Public CIDR's

This will only be triggered during the create or update of the cloudforamtion template.

### Lambda Function IAM Role policies
  - EKSAccess - Describe and update cluter config
  - CloudWatchLogsAccess - Create log groups and write Lambda logs to CloudWatch
