# Karpenter Autoscaler for Amazon EKS - Boilerplate IaC

Karpenter is an open-source, flexible, high-performance Kubernetes cluster autoscaler built with AWS. It helps improve your application availability and cluster efficiency by rapidly launching right-sized compute resources in response to changing application load. Karpenter also provides just-in-time compute resources to meet your application’s needs and will soon automatically optimize a cluster’s compute resource footprint to reduce costs and improve performance. When Karpenter is installed in your cluster, Karpenter observes the aggregate resource requests of unscheduled pods and makes decisions to launch new nodes and terminate them to reduce scheduling latencies and infrastructure costs. Karpenter does this by observing events within the Kubernetes cluster and then sending commands to the underlying cloud provider’s compute service, such as Amazon EC2.

The IaC in this repository is a boilerplate to orchestrate the deployment of **Karpenter** along with following resources in your AWS account using Ansible playbooks and AWS Cloudformation stacks:-

- A VPC spread across two AZs with multiple subnets for APP, DB and WEB tiers.
- S3 bucket to store infrastructure files.
- Lamdba functions to configure Amazon EKS control plane.
- Amazon EKS control plane in APP subnets.
- Necessary Amazon EKS addons for cluster networking.
- Starters nodes in Amazon EC2 autoscaling group.
- `aws-auth` k8s configmap to join new worker nodes to EKS control plane.
- Install `karpenter` helm-charts in EKS cluster along with its pre-requisites in AWS.
- Deploy a sample pod `inflate` to test automated worker node provisioning by karpenter.

## Pre-requisites

### Understanding Repository Directories

It is very important to understand the directory structure of this repo so that you can use the IaC easily to deploy the infrastructure and install Karpenter in Amazon EKS cluster.

```bash
├── ansible
├── ansible.cfg
├── cf-templates
├── examples
├── functions
├── LICENSE
├── local.yml
├── playbooks
├── README.md
├── templates
├── vagrant
└── vars
```

In the above tree, the directories and files are as below:-

- `ansible` holds global host config file.
- `ansible.cfg` holds local ansible configurations.
- `cf-templates` holds YAML templates to create AWS Cloudformation stacks.
- `examples` holds k8s YAML manifests to deploy sample apps for testing Karpenter EKS worker node provisioning.
- `functions` holds Lambda functions files to configure EKS control plane.
- `LICENSE` holds MIT License information.
- `local.yml` is the master plabook which is used for pull-based Ansible setup.
- `playbooks` holds Ansible playbooks orchestrating the infrastructure deployment.
- `README.md` which you are currently reading :grin:.
- `templates` holds environment agnostic Jinja2 templates which are used by Ansible playbooks in `playbooks` directory to deploy infrastructure.
- `vagrant` holds vagrantfile which can help you to setup a local linux VM having all necessary tools as described in [Configure Your System](#configure-your-system).
- `vars` holds YAML variable file(s) which have static paramters used by Ansible playbooks in `playbooks` directory to deploy infrastructure.

### Configure Your System

Your local system should be configured as below to help you use the IaC to deploy the infrastructure:-

- AWS CLI v2.
- AWS profile configured with an IAM user/role having AWS account admin access.
- kubectl CLI.
- Python v3 and pip3.
- Ansible v2.9.0.
- Boto3 python module to interact with AWS services.
- Openshift and kubernetes-validate ansible modules.
- Amazon EC2 SSH Keypair

You can also use the [Vagrantfile](https://github.com/suyashg89/aws-eks-karpenter-boilerplate/tree/main/vagrant/README.md) to create a Linux VM in your local system that will have all the above mentioned tools installed in it. AWS profile and Amazon EC2 SSH Keypair has to be created manually.

### Playbook Variables

#### Runtime Variables

The Ansible playbooks in this repository requires below three runtime variables to be passed with their values while running `local.yml` ansible playbook:-

- `PROFILE` - Your AWS profile name.
- `ENV` - Your chosen environment name and it should match the variable file name in `vars` directory.

#### Static variables

The `vars` directory in the root of this repository contains variable file `sandbox.yml` which holds all the static variables with their values that are used by the Ansible playbooks in `playbooks` directory to deploy infrastructure. The name of the variable file depends on what you name your environment and pass its value to `env` runtime variable. Please make sure to update below variables in the variable file:-

- `aws_account_number` - Your AWS account ID
- `region` - Your preferred AWS region, ex- `eu-west-1`
- `eks_infra_bucket` - Your chosen Amazon S3 bucket name to store Lambda functions and can also be used to store other infrastructure related objects. 
- `eks_cluster_name` - Your chosen Amazon EKS cluster name.
- `ec2_keypair_name` - Amazon EC2 SSH keypair to attach in EKS worker nodes.
- `eks_node_ami_id` - Amazon EKS optimized worker node AMI ID.

You are ofcourse allowed to change the values of other variables as per your requirement.

## Karpenter Specifics

The necessary IaC files for Karpenter service are as below:-

- `<ENV>.yml` var file where `<ENV>` is your chosen environment name, for example in this repository, we have `sandbox.yml`. It holds the karpenter related variables as below which can be updated as per requirement:-

```yaml
eks_karpenter_parameters:
  cf_params:
    Environment: "{{ env }}"
    EksControlPlaneStackName: "{{ cf_stack_names.eks_control_plane_stack_name }}"
    EksClusterName: "{{ eks_cluster_name }}"
    LaunchTemplateName: "{{ env }}-eks-worker-node-template"
    NodeImageId: "{{ eks_node_ami_id }}"
    NodeVolumeSize: "50"
    KeyName: "{{ ec2_keypair_name }}"
    HttpPutResponseHopLimit: "1"
    DisableIMDSv1: "true"
  karpenter_helm_charts_version: v0.6.5
  provisioners:
    - name: "general-purpose"
      ec2_instance_type: "'m5.xlarge', 'm5.2xlarge', 'm5.4xlarge'"
      zone: "'{{ region }}a', '{{ region }}b'"
      arch: "'amd64'"
      capacity_type: "'on-demand'"
      labels:
        team: team-a
      ttlSecondsAfterEmpty: 30
```

- `eks-karpenter-prereqs.yml` Cloudformation template to deploy pre-requisite resources in AWS cloud for Karpenter's use.
- `aws-auth.j2` k8s configmap Jinja2 template which contains code to allow Kapenter provisioned EKS worker node to join the EKS cluster.
- `karpenter-k8s-provisioners.j2` Jinja2 template which is used by `install-eks-karpenter.yml` Ansible playbook to generate and deploy k8s provisioner CRD manifest for Karpenter in EKS cluster.
- `deploy-eks-karpenter-prereqs.yml` Ansible playbook which triggers `eks-karpenter-prereqs.yml` template to create a Cloudformation stack.
- `install-eks-karpenter.yml` Ansible playbook which deploys Karpenter helm-charts and its provisioner(s) in the EKS cluster.

## Deploy Amazon EKS Infrastructure with Karpenter

You can deploy the whole infrastruture in one go by running below ansible command:-

`ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags run_all`

The whole infrastructure will be deployed in approx. 50 mins and you can connect to the cluster by creating your kubeconfig file using below command:-

`aws eks --region <AWS_REGION_OF_EKS_CLUSTER> update-kubeconfig --name <EKS_CLUSTER_NAME> --profile <YOUR_AWS_PROFILE_NAME>`

If you want to review the deployment of each infrastructure component, please follow the below stepwise deployment process:-

- To deploy S3 bucket, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags s3`

- To deploy the Lambda functions to configure Amazon EKS control plane, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_lambda_fn`

- To deploy a VPC with multiple subnets for APP, DB and WEB tiers, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags vpc`

- To deploy necessary IAM Service Roles for EKS cluster, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_iam_roles`

- To deploy Amazon EKS Control Plane, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_control_plane`
  
  You can now create your kubeconfig file by running below command:-

  `aws eks --region <AWS_REGION_OF_EKS_CLUSTER> update-kubeconfig --name <EKS_CLUSTER_NAME> --profile <YOUR_AWS_PROFILE_NAME>`

- To deploy Karpenter pre-requisite resources, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_karpenter_prereqs`

- To deploy `aws-auth` k8s configmap in the EKS cluster, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_aws_auth`

- To deploy Amazon EKS managed add-ons in the EKS cluster, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_addons`

- To deploy starters EKS worker nodegroup, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags eks_starters_nodegroup`

- To install Karpenter helm-charts and its provisioners, please run the below command:-

  `ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags install_eks_karpenter`

## Test Karpenter Worker Node Provisioining for Amazon EKS

An example `inflate` pods deployment can be created in the newly created EKS cluster by running below command:-

`ansible-playbook -e "profile=PROFILE env=ENV" local.yml -vv --tags example_inflate_pods`

Now scale up the deployment to create new inflate pods by running the below command:-

`kubectl scale deployment inflate --replicas 5`

When you check the logs by running below command, you should be able to see that Karpenter is provisioning new EKS worker node as per pods requirement:-

`kubectl logs -f -n karpenter -l app.kubernetes.io/name=karpenter -c controller`

## Guides & Sources

- [Karpenter official documentation](https://karpenter.sh/docs/).
- [Karpenter best practices for Amazon EKS](https://aws.github.io/aws-eks-best-practices/karpenter/).
- [Amazon EKS official documentation](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
