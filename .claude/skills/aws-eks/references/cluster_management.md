# Aws-Eks - Cluster Management

*This file summarizes AWS EKS documentation and includes links to canonical AWS pages. Content adapted from Amazon Web Services EKS User Guide. For attribution and licensing details, see the official [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/).*

---

## Monitor your cluster with the observability dashboard

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/observability-dashboard.html

The Amazon EKS observability dashboard provides visibility into cluster performance to help detect, troubleshoot, and remediate issues. Key features:

- **Health & performance summary**: Overview of cluster health metrics with clickable links to detailed views
- **Control plane monitoring**: Metrics, CloudWatch Logs Insights, and control plane log viewing for Kubernetes 1.28+ clusters
- **Cluster insights**: Configuration analysis and upgrade readiness indicators

Actions available: Refresh dashboard data, link to CloudWatch metrics, and access Prometheus monitoring.

For complete documentation, see [Amazon EKS Observability Dashboard](https://docs.aws.amazon.com/eks/latest/userguide/observability-dashboard.html).

---

## Create an EKS Auto Mode Cluster with the eksctl CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-eksctl.html

**Contents:**
- Create an EKS Auto Mode Cluster with the eksctl CLI
        - Note
- Create an EKS Auto Mode cluster with a CLI command
- Create an EKS Auto Mode cluster with a YAML file

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic shows you how to create an Amazon EKS Auto Mode cluster using the eksctl command line interface (CLI). You can create an Auto Mode cluster either by running a single CLI command or by applying a YAML configuration file. Both methods provide the same functionality, with the YAML approach offering more granular control over cluster settings.

The eksctl CLI simplifies the process of creating and managing EKS Auto Mode clusters by handling the underlying AWS resource creation and configuration. Before proceeding, ensure you have the necessary AWS credentials and permissions configured on your local machine. This guide assumes you’re familiar with basic Amazon EKS concepts and have already installed the required CLI tools.

You must install version 0.195.0 or greater of eksctl. For more information, see eksctl releases on GitHub.

Run the following command to create a new EKS Auto Mode cluster:

**Examples:**

Example 1 (bash):
```bash
eksctl create cluster --name my-cluster --region us-west-2 --enable-auto-mode
```

Example 2 (yaml):
```yaml
# cluster.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: my-cluster  # Replace with your cluster name
  region: us-west-2  # Replace with your AWS region

iam:
  # ARN of the Cluster IAM Role
  # Optional: eksctl creates a new role if not supplied
  # Suggested to use one Cluster IAM Role per account
  # serviceRoleARN: arn:aws:iam::ACCOUNT_ID:role/ClusterRole  # Replace ACCOUNT_ID

autoModeConfig:
  enabled: true  # Enable EKS Auto Mode
  # Optional: Leave nodePools empty to use defaults (general-purpose, system)
  # To disable creation of default node pools, set to: []
  nodePools: []  # EKS Auto Mode will create default node pools
  # Optional: Leave nodeRoleARN unspecified to create a new Node IAM Role
  # nodeRoleARN: arn:aws:iam::ACCOUNT_ID:role/NodeRole  # Replace ACCOUNT_ID if reusing existing role
```

Save the ClusterConfig file as cluster.yaml, then run:

```bash
eksctl create cluster -f cluster.yaml
```

---

## Learn about IPv6 addresses to clusters, Pods, and services

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-ipv6.html

**Contents:**
- Learn about IPv6 addresses to clusters, Pods, and services
- IPv6 Feature support
- IP address assignments
- How to use IPv6 with EKS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Applies to: Pods with Amazon EC2 instances and Fargate Pods

By default, Kubernetes assigns IPv4 addresses to your Pods and services. Instead of assigning IPv4 addresses to your Pods and services, you can configure your cluster to assign IPv6 addresses to them. Amazon EKS doesn’t support dual-stacked Pods or services, even though Kubernetes does. As a result, you can’t assign both IPv4 and IPv6 addresses to your Pods and services.

You select which IP family you want to use for your cluster when you create it. You can’t change the family after you create the cluster.

For a tutorial to deploy an Amazon EKS IPv6 cluster, see Deploying an Amazon EKS IPv6 cluster and managed Amazon Linux nodes.

The following are considerations for using the feature:

No Windows support: Windows Pods and services aren’t supported.

Nitro-based EC2 nodes required: You can only use IPv6 with AWS Nitro-based Amazon EC2 or Fargate nodes.

EC2 and Fargate nodes supported: You can use IPv6 with Assign security groups to individual Pods with Amazon EC2 nodes and Fargate nodes.

Outposts not supported: You can’t use IPv6 with Deploy Amazon EKS on-premises with AWS Outposts.

FSx for Lustre is not supported: The Use high-performance app storage with Amazon FSx for Lustre is not supported.

Custom networking not supported: If you previously used Deploy Pods in alternate subnets with custom networking to help alleviate IP address exhaustion, you can use IPv6 instead. You can’t use custom networking with IPv6. If you use custom networking for network isolation, then you might need to continue to use custom networking and the IPv4 family for your clusters.

Kubernetes services: Kubernetes services are only assigned an IPv6 addresses. They aren’t assigned IPv4 addresses.

Pods: Pods are assigned an IPv6 address and a host-local IPv4 address. The host-local IPv4 address is assigned by using a host-local CNI plugin chained with VPC CNI and the address is not reported to the Kubernetes control plane. It is only used when a pod needs to communicate with an external IPv4 resources in another Amazon VPC or the internet. The host-local IPv4 address gets SNATed (by VPC CNI) to the primary IPv4 address of the primary ENI of the worker node.

Pods and services: Pods and services receive only IPv6 addresses, not IPv4 addresses. When Pods need to communic

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
BootstrapArguments
```

Example 2 (unknown):
```unknown
BootstrapArguments
```

Example 3 (unknown):
```unknown
--ip-family ipv6 --service-ipv6-cidr your-cidr
```

Example 4 (unknown):
```unknown
aws eks describe-cluster --name my-cluster --query cluster.kubernetesNetworkConfig.serviceIpv6Cidr --output text
```

---

## Create an Amazon EKS cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html

**Contents:**
- Create an Amazon EKS cluster
        - Note
- Prerequisites
- Step 1: Create cluster IAM role
  - Service Linked Role
- Step 2: Create cluster
  - Create cluster - eksctl
    - Optional Settings
  - Create cluster - AWS console
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers creating EKS clusters without EKS Auto Mode.

For detailed instructions on creating an EKS Auto Mode cluster, see Create an Amazon EKS Auto Mode cluster.

To get started with EKS Auto Mode, see Get started with Amazon EKS – EKS Auto Mode.

This topic provides an overview of the available options and describes what to consider when you create an Amazon EKS cluster. If you need to create a cluster with your on-premises infrastructure as the compute for nodes, see Create an Amazon EKS cluster with hybrid nodes. If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our guides in Get started with Amazon EKS. These guides help you to create a simple, default cluster without expanding into all of the available options.

An existing VPC and subnets that meet Amazon EKS requirements. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements. If you don’t have a VPC and subnets, you can create them using an Amazon EKS provided AWS CloudFormation template.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

An IAM principal with permissions to create and describe an Amazon EKS cluster. For more information, see Create a local Kubernetes cluster on an Outpost and List or describe all clusters.

If you already have a cluster IAM role, or you're going to create your cluster with eksctl, you can skip the IAM role creation step. See also: [Create cluster IAM role](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html), [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), [Allowing users to access your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html), and [Launching Amazon EKS nodes](https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html).

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 3 (unknown):
```unknown
eks-cluster-role-trust-policy.json
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html

Creates an Amazon EKS control plane. The control plane runs in an AWS-managed account and consists of Kubernetes components (etcd, API server) provisioned across multiple Availability Zones.

Commonly configured fields include:

- **kubernetesNetworkConfig**: IP family (ipv4/ipv6) and service CIDR block configuration
- **resourcesVpcConfig**: VPC subnets and security groups for cluster placement
- **logging**: Enable/disable control plane log export to CloudWatch (disabled by default)
- **upgradePolicy**: Kubernetes version upgrade settings

Default behaviors: Public endpoint access enabled, private endpoint disabled; CloudWatch logs disabled by default; cluster creation typically takes several minutes.

For complete API reference with all request/response fields, see [CreateCluster API Reference](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html).

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-health

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-update.html

**Contents:**
- Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration
- Prerequisites
- Considerations
- Enable hybrid nodes on an existing cluster
  - Enable EKS Hybrid Nodes in an existing cluster - AWS CloudFormation
  - Enable EKS Hybrid Nodes in an existing cluster - AWS CLI
  - Enable EKS Hybrid Nodes in an existing cluster - AWS Management Console
- Update hybrid nodes configuration in an existing cluster
  - Update hybrid configuration in an existing cluster - AWS CloudFormation
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you add, change, or remove the hybrid nodes configuration for an Amazon EKS cluster.

To enable an Amazon EKS cluster to use hybrid nodes, add the IP address CIDR ranges of your on-premises node and optionally pod network in the RemoteNetworkConfig configuration. EKS uses this list of CIDRs to enable connectivity between the cluster and your on-premises networks. For a full list of options when updating your cluster configuration, see the UpdateClusterConfig in the Amazon EKS API Reference.

You can do any of the following actions to the EKS Hybrid Nodes networking configuration in a cluster:

Add remote network configuration to enable EKS Hybrid Nodes in an existing cluster.

Add, change, or remove the remote node networks or the remote pod networks in an existing cluster.

Remove all remote node network CIDR ranges to disable EKS Hybrid Nodes in an existing cluster.

Before enabling your Amazon EKS cluster for hybrid nodes, ensure your environment meets the requirements outlined at Prerequisite setup for hybrid nodes, and detailed at Prepare networking for hybrid nodes, Prepare operating system for hybrid nodes, and Prepare credentials for hybrid nodes.

Your cluster must use IPv4 address family.

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode. The process for modifying the cluster authentication mode is described at Change authentication mode to use access entries.

We recommend that you use either public or private endpoint access for the Amazon EKS Kubernetes API server endpoint, but not both. If you choose “Public and Private”, the Amazon EKS Kubernetes API server endpoint will always resolve to the public IPs for hybrid nodes running outside of your VPC, which can prevent your hybrid nodes from joining the cluster. The process for modifying network access to your cluster is described at Cluster API server endpoint.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the latest versio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
RemoteNetworkConfig
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
aws --version
```

Example 4 (unknown):
```unknown
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: eks.amazonaws.com/compute-type
          operator: NotIn
          values:
          - hybrid
```

---

## Create an Amazon EKS cluster with hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-create.html#hybrid-nodes-cluster-create-console

**Contents:**
- Create an Amazon EKS cluster with hybrid nodes
- Prerequisites
- Considerations
- Step 1: Create cluster IAM role
- Step 2: Create hybrid nodes-enabled cluster
  - Create hybrid nodes-enabled cluster - eksctl
  - Create hybrid nodes-enabled cluster - AWS CloudFormation
  - Create hybrid nodes-enabled cluster - AWS CLI
  - Create hybrid nodes-enabled cluster - AWS Management Console
- Step 3: Update kubeconfig

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you create a hybrid nodes-enabled Amazon EKS cluster. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes, including standard and extended support.

If you are not planning to use EKS Hybrid Nodes, see the primary Amazon EKS create cluster documentation at Create an Amazon EKS cluster.

The Prerequisite setup for hybrid nodes completed. Before you create your hybrid nodes-enabled cluster, you must have your on-premises node and optionally pod CIDRs identified, your VPC and subnets created according to the EKS requirements, and hybrid nodes requirements, and your security group with inbound rules for your on-premises and optionally pod CIDRs. For more information on these prerequisites, see Prepare networking for hybrid nodes.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the last version of the AWS CLI and Configuring settings for the AWS CLI in the AWS Command Line Interface User Guide.

An IAM principal with permissions to create IAM roles and attach policies, and create and describe EKS clusters

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode.

Your cluster must use IPv4 address family.

Your cluster must use either Public or Private cluster endpoint connectivity. Your cluster cannot use “Public and Private” cluster endpoint connectivity, because the Amazon EKS Kubernetes API server endpoint will resolve to the public IPs for hybrid nodes running outside of your VPC.

OIDC authentication is supported for EKS clusters with hybrid nodes.

You can add, change, or remove the hybrid nodes configuration of an existing cluster. For more information, see Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration.

If you already have a cluster IAM role, or you’re going to create your cluster with eksctl or AWS CloudFormation, then you can skip this step. By default, eksctl and the AWS CloudFormation template create the cluste

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-remoteNetworkConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Assess EKS cluster resiliency with AWS Resilience Hub

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/integration-resilience-hub.html

**Contents:**
- Assess EKS cluster resiliency with AWS Resilience Hub

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

AWS Resilience Hub assesses the resiliency of an Amazon EKS cluster by analyzing its infrastructure. AWS Resilience Hub uses the Kubernetes role-based access control (RBAC) configuration to assess the Kubernetes workloads deployed to your cluster. For more information, see Enabling AWS Resilience Hub access to your Amazon EKS cluster in the AWS Resilience Hub User Guide.

---

## Learn how EKS Pod Identity grants pods access to AWS services

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html#pod-id-cluster-versions

**Contents:**
- Learn how EKS Pod Identity grants pods access to AWS services
- Benefits of EKS Pod Identities
        - Note
        - Important
- Overview of setting up EKS Pod Identities
- Limits
- Considerations
  - EKS Pod Identity cluster versions
  - EKS Pod Identity restrictions

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Applications in a Pod’s containers can use an AWS SDK or the AWS CLI to make API requests to AWS services using AWS Identity and Access Management (IAM) permissions. Applications must sign their AWS API requests with AWS credentials.

EKS Pod Identities provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance’s role, you associate an IAM role with a Kubernetes service account and configure your Pods to use the service account.

Each EKS Pod Identity association maps a role to a service account in a namespace in the specified cluster. If you have the same application in multiple clusters, you can make identical associations in each cluster without modifying the trust policy of the role.

If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod. The environment variables configure the AWS SDKs, including the AWS CLI, to use the EKS Pod Identity credentials.

EKS Pod Identities provide the following benefits:

Least privilege – You can scope IAM permissions to a service account, and only Pods that use that service account have access to those permissions. This feature also eliminates the need for third-party solutions such as kiam or kube2iam.

Credential isolation – When access to the Amazon EC2 Instance Metadata Service (IMDS) is restricted, a Pod’s containers can only retrieve credentials for the IAM role that’s associated with the service account that the container uses. A container never has access to credentials that are used by other containers in other Pods. If IMDS is not restricted, the Pod’s containers also have access to the Amazon EKS node IAM role and the containers may be able to gain access to credentials of IAM roles of other Pods on the same node. For more information, see Restrict access to the instance profile assigned to the worker node.

Pods configured with hostNetwork: true will always have IMDS access, but the AWS SDKs and CLI will use Pod Identity credentials when enabled.

Auditability – Access and event logging is available through AWS CloudTrail to help facilitate retrospective auditing.

Containers are not 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
hostNetwork: true
```

Example 2 (unknown):
```unknown
            "Principal": {
                "Service": "pods.eks.amazonaws.com"
            }
```

Example 3 (unknown):
```unknown
hostNetwork
```

Example 4 (unknown):
```unknown
169.254.170.23
```

---

## Create a cluster with Amazon EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-auto.html

**Contents:**
- Create a cluster with Amazon EKS Auto Mode
        - Note
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter explains how to create an Amazon EKS cluster with Auto Mode enabled using various tools and interfaces. Auto Mode simplifies cluster creation by automatically configuring and managing the cluster’s compute, networking, and storage infrastructure. You’ll learn how to create an Auto Mode cluster using the AWS CLI, AWS Management Console, or the eksctl command line tool.

EKS Auto Mode requires Kubernetes version 1.29 or greater.

Choose your preferred tool based on your needs: The AWS Management Console provides a visual interface ideal for learning about EKS Auto Mode features and creating individual clusters. The AWS CLI is best suited for scripting and automation tasks, particularly when integrating cluster creation into existing workflows or CI/CD pipelines. The eksctl CLI offers a Kubernetes-native experience and is recommended for users familiar with Kubernetes tooling who want simplified command line operations with sensible defaults.

Before you begin, ensure you have the necessary prerequisites installed and configured, including appropriate IAM permissions to create EKS clusters. To learn how to install CLI tools such as kubectl, aws, and eksctl, see Set up to use Amazon EKS.

You can use the AWS CLI, AWS Management Console, or eksctl CLI to create a cluster with Amazon EKS Auto Mode.

Create an EKS Auto Mode Cluster with the eksctl CLI

Create an EKS Auto Mode Cluster with the AWS CLI

Create an EKS Auto Mode Cluster with the AWS Management Console

---

## Using roles for Amazon EKS clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/using-service-linked-roles-eks.html

**Contents:**
- Using roles for Amazon EKS clusters
- Service-linked role permissions for Amazon EKS
        - Note
- Creating a service-linked role for Amazon EKS
- Editing a service-linked role for Amazon EKS
- Deleting a service-linked role for Amazon EKS
  - Cleaning up a service-linked role
        - Note
  - Manually delete the service-linked role
- Supported regions for Amazon EKS service-linked roles

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon Elastic Kubernetes Service uses AWS Identity and Access Management (IAM) service-linked roles. A service-linked role is a unique type of IAM role that is linked directly to Amazon EKS. Service-linked roles are predefined by Amazon EKS and include all the permissions that the service requires to call other AWS services on your behalf.

A service-linked role makes setting up Amazon EKS easier because you don’t have to manually add the necessary permissions. Amazon EKS defines the permissions of its service-linked roles, and unless defined otherwise, only Amazon EKS can assume its roles. The defined permissions include the trust policy and the permissions policy, and that permissions policy cannot be attached to any other IAM entity.

You can delete a service-linked role only after first deleting their related resources. This protects your Amazon EKS resources because you can’t inadvertently remove permission to access the resources.

For information about other services that support service-linked roles, see AWS services that work with IAM and look for the services that have Yes in the Service-linked role column. Choose a Yes with a link to view the service-linked role documentation for that service.

Amazon EKS uses the service-linked role named AWSServiceRoleForAmazonEKS. The role allows Amazon EKS to manage clusters in your account. The attached policies allow the role to manage the following resources: network interfaces, security groups, logs, and VPCs.

The AWSServiceRoleForAmazonEKS service-linked role is distinct from the role required for cluster creation. For more information, see Amazon EKS cluster IAM role.

The AWSServiceRoleForAmazonEKS service-linked role trusts the following services to assume the role:

The role permissions policy allows Amazon EKS to complete the following actions on the specified resources:

AmazonEKSServiceRolePolicy

You must configure permissions to allow an IAM entity (such as a user, group, or role) to create, edit, or delete a service-linked role. For more information, see Service-linked role permissions in the IAM User Guide.

You don’t need to manually create a service-linked role. When you create a cluster in the AWS Management Console, the AWS CLI, or the AWS API, Amazon EKS creates the service-linked role for you.

If you delete this service-linked role, and 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AWSServiceRoleForAmazonEKS
```

Example 2 (unknown):
```unknown
AWSServiceRoleForAmazonEKS
```

Example 3 (unknown):
```unknown
AWSServiceRoleForAmazonEKS
```

Example 4 (unknown):
```unknown
eks.amazonaws.com
```

---

## Create an Amazon VPC for your Amazon EKS cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/creating-a-vpc.html

**Contents:**
- Create an Amazon VPC for your Amazon EKS cluster
- Prerequisites
- Public and private subnets
- Only public subnets
- Only private subnets

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use Amazon Virtual Private Cloud (Amazon VPC) to launch AWS resources into a virtual network that you’ve defined. This virtual network closely resembles a traditional network that you might operate in your own data center. However, it comes with the benefits of using the scalable infrastructure of Amazon Web Services. We recommend that you have a thorough understanding of the Amazon VPC service before deploying production Amazon EKS clusters. For more information, see the Amazon VPC User Guide.

An Amazon EKS cluster, nodes, and Kubernetes resources are deployed to a VPC. If you want to use an existing VPC with Amazon EKS, that VPC must meet the requirements that are described in View Amazon EKS networking requirements for VPC and subnets. This topic describes how to create a VPC that meets Amazon EKS requirements using an Amazon EKS provided AWS CloudFormation template. Once you’ve deployed a template, you can view the resources created by the template to know exactly what resources it created, and the configuration of those resources. If you are using hybrid nodes, your VPC must have routes in its route table for your on-premises network. For more information about the network requirements for hybrid nodes, see Prepare networking for hybrid nodes.

To create a VPC for Amazon EKS, you must have the necessary IAM permissions to create Amazon VPC resources. These resources are VPCs, subnets, security groups, route tables and routes, and internet and NAT gateways. For more information, see Create a VPC with a public subnet example policy in the Amazon VPC User Guide and the full list of Actions in the Service Authorization Reference.

You can create a VPC with public and private subnets, only public subnets, or only private subnets.

This VPC has two public and two private subnets. A public subnet’s associated route table has a route to an internet gateway. However, the route table of a private subnet doesn’t have a route to an internet gateway. One public and one private subnet are deployed to the same Availability Zone. The other public and private subnets are deployed to a second Availability Zone in the same AWS Region. We recommend this option for most deployments.

With this option, you can deploy your nodes to private subnets. This option allows Kubernetes to deploy load balancers to the public su

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
```

Example 2 (unknown):
```unknown
https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-ipv6-vpc-public-private-subnets.yaml
```

Example 3 (unknown):
```unknown
https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml
```

Example 4 (unknown):
```unknown
amazon-eks-vpc-sample
```

---

## Secure Amazon EKS clusters with best practices

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-best-practices.html

**Contents:**
- Secure Amazon EKS clusters with best practices

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon EKS security best practices are in the Best Practices for Security in the Amazon EKS Best Practices Guide.

---

## Create an Amazon EKS Auto Mode cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-cluster-auto.html

**Contents:**
- Create an Amazon EKS Auto Mode cluster
        - Note
- Prerequisites
- Create cluster - AWS console
        - Note
- Create cluster - AWS CLI
  - Create an EKS Auto Mode Cluster IAM Role
    - Step 1: Create the Trust Policy
    - Step 2: Create the IAM Role
    - Step 3: Note the Role ARN

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides detailed instructions for creating an Amazon EKS Auto Mode cluster using advanced configuration options. It covers prerequisites, networking options, and add-on configurations. The process includes setting up IAM roles, configuring cluster settings, specifying networking parameters, and selecting add-ons. Users can create clusters using either the AWS Management Console or the AWS CLI, with step-by-step guidance provided for both methods.

For users seeking a less complex setup process, refer to the following for simplified cluster creation steps:

Create an EKS Auto Mode Cluster with the eksctl CLI

Create an EKS Auto Mode Cluster with the AWS CLI

Create an EKS Auto Mode Cluster with the AWS Management Console

This advanced configuration guide is intended for users who require more granular control over their EKS Auto Mode cluster setup and are familiar with Amazon EKS concepts and requirements. Before proceeding with the advanced configuration, ensure you have met all prerequisites and have a thorough understanding of the networking and IAM requirements for EKS Auto Mode clusters.

EKS Auto Mode requires additional IAM permissions. For more information, see:

IAM Roles for EKS Auto Mode Clusters

Learn about identity and access in EKS Auto Mode

If you want to create a cluster without EKS Auto Mode, see Create an Amazon EKS cluster.

This topic covers advanced configuration. If you are looking to get started with EKS Auto Mode, see Create a cluster with Amazon EKS Auto Mode.

An existing VPC and subnets that meet Amazon EKS requirements. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements. If you don’t have a VPC and subnets, you can create them using an Amazon EKS provided AWS CloudFormation template.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. For example, if your cluster version is 1.29, you can use kubectl version 1.28, 1.29, or 1.30 with it. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS Clou

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
10.2.0.0/16
```

Example 3 (unknown):
```unknown
172.16.0.0/12
```

Example 4 (unknown):
```unknown
192.168.0.0/16
```

---

## ClusterIssue

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ClusterIssue.html#AmazonEKS-Type-ClusterIssue-message

**Contents:**
- ClusterIssue
- Contents
- See Also

An issue with your Amazon EKS cluster.

The error code of the issue.

Valid Values: AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other

A description of the issue.

The resource IDs that the issue relates to.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other
```

---

## Launch low-latency EKS clusters with AWS Local Zones

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/local-zones.html

**Contents:**
- Launch low-latency EKS clusters with AWS Local Zones

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

An AWS Local Zone is an extension of an AWS Region in geographic proximity to your users. Local Zones have their own connections to the internet and support AWS Direct Connect. Resources created in a Local Zone can serve local users with low-latency communications. For more information, see the AWS Local Zones User Guide and Local Zones in the Amazon EC2 User Guide.

Amazon EKS supports certain resources in Local Zones. This includes managed node groups, self-managed Amazon EC2 nodes, Amazon EBS volumes, and Application Load Balancers (ALBs). We recommend that you consider the following when using Local Zones as part of your Amazon EKS cluster.

You can’t create Fargate nodes in Local Zones with Amazon EKS.

The Amazon EKS managed Kubernetes control plane always runs in the AWS Region. The Amazon EKS managed Kubernetes control plane can’t run in the Local Zone. Because Local Zones appear as a subnet within your VPC, Kubernetes sees your Local Zone resources as part of that subnet.

The Amazon EKS Kubernetes cluster communicates with the Amazon EC2 instances you run in the AWS Region or Local Zone using Amazon EKS managed elastic network interfaces. To learn more about Amazon EKS networking architecture, see Configure networking for Amazon EKS clusters.

Unlike regional subnets, Amazon EKS can’t place network interfaces into your Local Zone subnets. This means that you must not specify Local Zone subnets when you create your cluster. However, you can have worker nodes in different multiple Local Zones connected to the same cluster.

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-createdAt

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-name

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Automate cluster infrastructure with EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/automode.html

**Contents:**
- Automate cluster infrastructure with EKS Auto Mode
- Features
- Automated Components
- Configuration
- Shared responsibility model

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

EKS Auto Mode extends AWS management of Kubernetes clusters beyond the cluster itself, to allow AWS to also set up and manage the infrastructure that enables the smooth operation of your workloads. You can delegate key infrastructure decisions and leverage the expertise of AWS for day-to-day operations. Cluster infrastructure managed by AWS includes many Kubernetes capabilities as core components, as opposed to add-ons, such as compute autoscaling, pod and service networking, application load balancing, cluster DNS, block storage, and GPU support.

To get started, you can deploy a new EKS Auto Mode cluster or enable EKS Auto Mode on an existing cluster. You can deploy, upgrade, or modify your EKS Auto Mode clusters using eksctl, the AWS CLI, the AWS Management Console, EKS APIs, or your preferred infrastructure-as-code tools.

With EKS Auto Mode, you can continue using your preferred Kubernetes-compatible tools. EKS Auto Mode integrates with AWS services like Amazon EC2, Amazon EBS, and ELB, leveraging AWS cloud resources that follow best practices. These resources are automatically scaled, cost-optimized, and regularly updated to help minimize operational costs and overhead.

EKS Auto Mode provides the following high-level features:

Streamline Kubernetes Cluster Management: EKS Auto Mode streamlines EKS management by providing production-ready clusters with minimal operational overhead. With EKS Auto Mode, you can run demanding, dynamic workloads confidently, without requiring deep EKS expertise.

Application Availability: EKS Auto Mode dynamically adds or removes nodes in your EKS cluster based on the demands of your Kubernetes applications. This minimizes the need for manual capacity planning and ensures application availability.

Efficiency: EKS Auto Mode is designed to optimize compute costs while adhering to the flexibility defined by your NodePool and workload requirements. It also terminates unused instances and consolidates workloads onto other nodes to improve cost efficiency.

Security: EKS Auto Mode uses AMIs that are treated as immutable, for your nodes. These AMIs enforce locked-down software, enable SELinux mandatory access controls, and provide read-only root file systems. Additionally, nodes launched by EKS Auto Mode have a maximum lifetime of 21 days (which you can reduce), after which they 

*[Content truncated]*

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-deletionProtection

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Update self-managed nodes for your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/update-workers.html

**Contents:**
- Update self-managed nodes for your cluster
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When a new Amazon EKS optimized AMI is released, consider replacing the nodes in your self-managed node group with the new AMI. Likewise, if you have updated the Kubernetes version for your Amazon EKS cluster, update the nodes to use nodes with the same Kubernetes version.

This topic covers node updates for self-managed nodes. If you are using managed node groups, see Update a managed node group for your cluster.

There are two basic ways to update self-managed node groups in your clusters to use a new AMI:

Create a new node group and migrate your Pods to that group. Migrating to a new node group is more graceful than simply updating the AMI ID in an existing AWS CloudFormation stack. This is because the migration process taints the old node group as NoSchedule and drains the nodes after a new stack is ready to accept the existing Pod workload.

Update the AWS CloudFormation stack for an existing node group to use the new AMI. This method isn’t supported for node groups that were created with eksctl.

---

## Monitor cluster data with Amazon CloudWatch

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cloudwatch.html

**Contents:**
- Monitor cluster data with Amazon CloudWatch
- Basic metrics in Amazon CloudWatch
- Amazon CloudWatch Observability Operator

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon CloudWatch is a monitoring service that collects metrics and logs from your cloud resources. CloudWatch provides some basic Amazon EKS metrics for free when using a new cluster that is version 1.28 and above. However, when using the CloudWatch Observability Operator as an Amazon EKS add-on, you can gain enhanced observability features.

For clusters that are Kubernetes version 1.28 and above, you get CloudWatch vended metrics for free in the AWS/EKS namespace. The following table gives a list of the basic metrics that are available for the supported versions. Every metric listed has a frequency of one minute.

scheduler_schedule_attempts_total

The number of total attempts by the scheduler to schedule Pods in the cluster for a given period. This metric helps monitor the scheduler’s workload and can indicate scheduling pressure or potential issues with Pod placement.

Valid statistics: Sum

scheduler_schedule_attempts_SCHEDULED

The number of successful attempts by the scheduler to schedule Pods to nodes in the cluster for a given period.

Valid statistics: Sum

scheduler_schedule_attempts_UNSCHEDULABLE

The number of attempts to schedule Pods that were unschedulable for a given period due to valid constraints, such as insufficient CPU or memory on a node.

Valid statistics: Sum

scheduler_schedule_attempts_ERROR

The number of attempts to schedule Pods that failed for a given period due to an internal problem with the scheduler itself, such as API Server connectivity issues.

Valid statistics: Sum

scheduler_pending_pods

The number of total pending Pods to be scheduled by the scheduler in the cluster for a given period.

Valid statistics: Sum

scheduler_pending_pods_ACTIVEQ

The number of pending Pods in activeQ, that are waiting to be scheduled in the cluster for a given period.

Valid statistics: Sum

scheduler_pending_pods_UNSCHEDULABLE

The number of pending Pods that the scheduler attempted to schedule and failed, and are kept in an unschedulable state for retry.

Valid statistics: Sum

scheduler_pending_pods_BACKOFF

The number of pending Pods in backoffQ in a backoff state that are waiting for their backoff period to expire.

Valid statistics: Sum

scheduler_pending_pods_GATED

The number of pending Pods that are currently waiting in a gated state as they cannot be scheduled until they meet requ

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
scheduler_schedule_attempts_total
```

Example 2 (unknown):
```unknown
scheduler_schedule_attempts_SCHEDULED
```

Example 3 (unknown):
```unknown
scheduler_schedule_attempts_UNSCHEDULABLE
```

Example 4 (unknown):
```unknown
scheduler_schedule_attempts_ERROR
```

---

## ClusterHealth

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ClusterHealth.html#AmazonEKS-Type-ClusterHealth-issues

**Contents:**
- ClusterHealth
- Contents
- See Also

An object representing the health of your Amazon EKS cluster.

An object representing the health issues of your Amazon EKS cluster.

Type: Array of ClusterIssue objects

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Cluster API server endpoint

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html#private-access

**Contents:**
- Cluster API server endpoint
- IPv6 cluster endpoint format
        - Note
- IPv4 cluster endpoint format
        - Note
- Cluster private endpoint
        - Note
- Modifying cluster endpoint access
- Accessing a private only API server

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic helps you to enable private access for your Amazon EKS cluster’s Kubernetes API server endpoint and limit, or completely disable, public access from the internet.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster (using Kubernetes management tools such as kubectl). By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management (IAM) and native Kubernetes Role Based Access Control (RBAC). This endpoint is known as the cluster public endpoint. Also there is a cluster private endpoint. For more information about the cluster private endpoint, see the following section Cluster private endpoint.

EKS creates a unique dual-stack endpoint in the following format for new IPv6 clusters that are made after October 2024. An IPv6 cluster is a cluster that you select IPv6 in the IP family (ipFamily) setting of the cluster.

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.amazonwebservices.com.cn

The dual-stack cluster endpoint was introduced in October 2024. For more information about IPv6 clusters, see Learn about IPv6 addresses to clusters, Pods, and services. Clusters made before October 2024, use following endpoint format instead.

EKS creates a unique endpoint in the following format for each cluster that select IPv4 in the IP family (ipFamily) setting of the cluster:

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.amazonwebservices.com.cn

Before October 2024, IPv6 clusters used this endpoint format also. For those clusters, both the public endpoint and the private endpoint have only IPv4 addresses resolve from this endpoint.

You can enable private access to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server.

Because this e

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 2 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 3 (unknown):
```unknown
eks-cluster.region.api.amazonwebservices.com.cn
```

Example 4 (unknown):
```unknown
eks-cluster.region.eks.amazonaws.com
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-encryptionConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Prevent increased cluster costs by disabling EKS extended support

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/disable-extended-support.html

**Contents:**
- Prevent increased cluster costs by disabling EKS extended support
        - Important
- Disable EKS extended support (AWS Console)
- Disable EKS extended support (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how to set the upgrade policy of an EKS cluster to disable extended support. The upgrade policy of an EKS cluster determines what happens when a cluster reaches the end of the standard support period. If a cluster upgrade policy has extended support disabled, it will be automatically upgraded to the next Kubernetes version.

For more information about upgrade policies, see Cluster upgrade policy.

You cannot disable extended support once your cluster has entered it. You can only disable extended support for clusters on standard support.

AWS recommends upgrading your cluster to a version in the standard support period.

Navigate to your EKS cluster in the AWS Console. Select the Overview tab on the Cluster Info page.

In the Kubernetes version setting section, select Manage.

Select Standard support and then Save changes.

Verify the AWS CLI is installed and you are logged in. Learn how to update and install the AWS CLI.

Determine the name of your EKS cluster.

Run the following command:

**Examples:**

Example 1 (unknown):
```unknown
aws eks update-cluster-config \
--name <cluster-name> \
--upgrade-policy supportType=STANDARD
```

---

## Monitor your cluster metrics with Prometheus

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/prometheus.html

**Contents:**
- Monitor your cluster metrics with Prometheus
- Step 1: Turn on Prometheus metrics
        - Important
        - Important
- Step 2: Use the Prometheus metrics
- Step 3: Manage Prometheus scrapers

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Prometheus is a monitoring and time series database that scrapes endpoints. It provides the ability to query, aggregate, and store collected data. You can also use it for alerting and alert aggregation. This topic explains how to set up Prometheus as either a managed or open source option. Monitoring Amazon EKS control plane metrics is a common use case.

Amazon Managed Service for Prometheus is a Prometheus-compatible monitoring and alerting service that makes it easy to monitor containerized applications and infrastructure at scale. It is a fully-managed service that automatically scales the ingestion, storage, querying, and alerting of your metrics. It also integrates with AWS security services to enable fast and secure access to your data. You can use the open-source PromQL query language to query your metrics and alert on them. Also, you can use alert manager in Amazon Managed Service for Prometheus to set up alerting rules for critical alerts. You can then send these critical alerts as notifications to an Amazon SNS topic.

There are several different options for using Prometheus with Amazon EKS:

You can turn on Prometheus metrics when first creating an Amazon EKS cluster or you can create your own Prometheus scraper for existing clusters. Both of these options are covered by this topic.

You can deploy Prometheus using Helm. For more information, see Deploy Prometheus using Helm.

You can view control plane raw metrics in Prometheus format. For more information, see Fetch control plane raw metrics in Prometheus format.

Amazon Managed Service for Prometheus resources are outside of the cluster lifecycle and need to be maintained independent of the cluster. When you delete your cluster, make sure to also delete any applicable scrapers to stop applicable costs. For more information, see Find and delete scrapers in the Amazon Managed Service for Prometheus User Guide.

Prometheus discovers and collects metrics from your cluster through a pull-based model called scraping. Scrapers are set up to gather data from your cluster infrastructure and containerized applications. When you turn on the option to send Prometheus metrics, Amazon Managed Service for Prometheus provides a fully managed agentless scraper.

If you haven’t created the cluster yet, you can turn on the option to send metrics to Prometheus when

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonManagedScraperRole
```

Example 2 (unknown):
```unknown
AmazonManagedScraperRole
```

Example 3 (unknown):
```unknown
AmazonManagedScraperRole
```

Example 4 (unknown):
```unknown
DescribeScraper
```

---

## AccessConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_AccessConfigResponse.html#AmazonEKS-Type-AccessConfigResponse-bootstrapClusterCreatorAdminPermissions

**Contents:**
- AccessConfigResponse
- Contents
- See Also

The access configuration for the cluster.

The current authentication mode of the cluster.

Valid Values: API | API_AND_CONFIG_MAP | CONFIG_MAP

Specifies whether or not the cluster creator IAM principal was set as a cluster admin access entry during cluster creation time.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
API | API_AND_CONFIG_MAP | CONFIG_MAP
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-zonalShiftConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-identity

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Cluster API server endpoint

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html#cluster-endpoint-private

**Contents:**
- Cluster API server endpoint
- IPv6 cluster endpoint format
        - Note
- IPv4 cluster endpoint format
        - Note
- Cluster private endpoint
        - Note
- Modifying cluster endpoint access
- Accessing a private only API server

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic helps you to enable private access for your Amazon EKS cluster’s Kubernetes API server endpoint and limit, or completely disable, public access from the internet.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster (using Kubernetes management tools such as kubectl). By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management (IAM) and native Kubernetes Role Based Access Control (RBAC). This endpoint is known as the cluster public endpoint. Also there is a cluster private endpoint. For more information about the cluster private endpoint, see the following section Cluster private endpoint.

EKS creates a unique dual-stack endpoint in the following format for new IPv6 clusters that are made after October 2024. An IPv6 cluster is a cluster that you select IPv6 in the IP family (ipFamily) setting of the cluster.

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.amazonwebservices.com.cn

The dual-stack cluster endpoint was introduced in October 2024. For more information about IPv6 clusters, see Learn about IPv6 addresses to clusters, Pods, and services. Clusters made before October 2024, use following endpoint format instead.

EKS creates a unique endpoint in the following format for each cluster that select IPv4 in the IP family (ipFamily) setting of the cluster:

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.amazonwebservices.com.cn

Before October 2024, IPv6 clusters used this endpoint format also. For those clusters, both the public endpoint and the private endpoint have only IPv4 addresses resolve from this endpoint.

You can enable private access to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server.

Because this e

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 2 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 3 (unknown):
```unknown
eks-cluster.region.api.amazonwebservices.com.cn
```

Example 4 (unknown):
```unknown
eks-cluster.region.eks.amazonaws.com
```

---

## Create an EKS Auto Mode Cluster with the AWS Management Console

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-console.html

**Contents:**
- Create an EKS Auto Mode Cluster with the AWS Management Console
- Create an EKS Auto Mode using the quick configuration option
- Next Steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Creating an EKS Auto Mode cluster in the AWS Management Console requires less configuration than other options. EKS integrates with AWS IAM and VPC Networking to help you create the resources associated with an EKS cluster.

You have two options to create a cluster in the console:

Quick configuration (with EKS Auto Mode)

In this topic, you will learn how to create an EKS Auto Mode cluster using the Quick configuration option.

You must be logged into the AWS Management Console with sufficient permissions to manage AWS resources including: EC2 instances, EC2 networking, EKS clusters, and IAM roles.

Navigate to the EKS Console

Confirm the Quick configuration option is selected

Determine the following values, or use the defaults for a test cluster.

Select the Cluster IAM Role. If this is your first time creating an EKS Auto Mode cluster, use the Create recommended role option.

Optionally, you can reuse a single Cluster IAM Role in your AWS account for all EKS Auto Mode clusters.

The Cluster IAM Role includes required permissions for EKS Auto Mode to manage resources including EC2 instances, EBS volumes, and EC2 load balancers.

The Create recommended role option pre-fills all fields with recommended values. Select Next and then Create. The role will use a suggested name (for example: AmazonEKSAutoClusterRole). These are example names, not required—follow least-privilege principles and reference AWS managed policies or IAM best practices documentation.

If you recently created a new role, use the Refresh icon to reload the role selection dropdown.

Select the Node IAM Role. If this is your first time creating an EKS Auto Mode cluster, use the Create recommended role option.

Optionally, you can reuse a single Node IAM Role in your AWS account for all EKS Auto Mode clusters.

The Node IAM Role includes required permissions for Auto Mode nodes to connect to the cluster. The Node IAM Role must include permissions to retrieve ECR images for your containers.

The Create recommended role option pre-fills all fields with recommended values. Select Next and then Create. The role will use a suggested name (for example: AmazonEKSAutoNodeRole). These are example names, not required—follow least-privilege principles and reference AWS managed policies or IAM best practices documentation.

If you recently created a new role, use the Refresh icon to reload the role selection dropdown.

Select the VPC for your EKS Auto Mode cluster. Choose the Create VPC to create a new VPC for EKS, or choose a VPC you previously created for EKS.

If you use the VPC Console to create a new VPC, AWS suggests you create at least one NAT Gateway per 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKSAutoClusterRole
```

Example 2 (unknown):
```unknown
AmazonEKSAutoNodeRole
```

---

## Create a managed node group for your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-managed-node-group.html

**Contents:**
- Create a managed node group for your cluster
        - Important
- eksctl
        - Important
        - Note
- AWS Management Console
        - Important
        - Note
        - Important
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how you can launch Amazon EKS managed node groups of nodes that register with your Amazon EKS cluster. After the nodes join the cluster, you can deploy Kubernetes applications to them.

If this is your first time launching an Amazon EKS managed node group, we recommend that you instead follow one of our guides in Get started with Amazon EKS. These guides provide walkthroughs for creating an Amazon EKS cluster with nodes.

Amazon EKS nodes are standard Amazon EC2 instances. You’re billed based on the normal Amazon EC2 prices. For more information, see Amazon EC2 Pricing.

You can’t create managed nodes in an AWS Region where you have AWS Outposts or AWS Wavelength enabled. You can create self-managed nodes instead. For more information, see Create self-managed Amazon Linux nodes, Create self-managed Microsoft Windows nodes, and Create self-managed Bottlerocket nodes. You can also create a self-managed Amazon Linux node group on an Outpost. For more information, see Create Amazon Linux nodes on AWS Outposts.

If you don’t specify an AMI ID for the bootstrap.sh file included with Amazon EKS optimized Linux or Bottlerocket, managed node groups enforce a maximum number on the value of maxPods. For instances with less than 30 vCPUs, the maximum number is 110. For instances with greater than 30 vCPUs, the maximum number jumps to 250. These numbers are based on Kubernetes scalability thresholds and recommended settings by internal Amazon EKS scalability team testing. For more information, see the Amazon VPC CNI plugin increases pods per node limits blog post.

An existing Amazon EKS cluster. To deploy one, see Create an Amazon EKS cluster.

An existing IAM role for the nodes to use. To create one, see Amazon EKS node IAM role. If this role doesn’t have either of the policies for the VPC CNI, the separate role that follows is required for the VPC CNI pods.

(Optional, but recommended) The Amazon VPC CNI plugin for Kubernetes add-on configured with its own IAM role that has the necessary IAM policy attached to it. For more information, see Configure Amazon VPC CNI plugin to use IRSA.

Familiarity with the considerations listed in Choose an optimal Amazon EC2 node instance type. Depending on the instance type you choose, there may be additional prerequisites for your cluster and VPC.

To add a Window

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
bootstrap.sh
```

Example 2 (unknown):
```unknown
eksctl version
```

Example 3 (unknown):
```unknown
boostrap.sh
```

Example 4 (unknown):
```unknown
eksctl create nodegroup --help
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-accessConfig

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Create an Amazon EKS cluster with hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-create.html#hybrid-nodes-cluster-create-kubeconfig

**Contents:**
- Create an Amazon EKS cluster with hybrid nodes
- Prerequisites
- Considerations
- Step 1: Create cluster IAM role
- Step 2: Create hybrid nodes-enabled cluster
  - Create hybrid nodes-enabled cluster - eksctl
  - Create hybrid nodes-enabled cluster - AWS CloudFormation
  - Create hybrid nodes-enabled cluster - AWS CLI
  - Create hybrid nodes-enabled cluster - AWS Management Console
- Step 3: Update kubeconfig

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you create a hybrid nodes-enabled Amazon EKS cluster. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes, including standard and extended support.

If you are not planning to use EKS Hybrid Nodes, see the primary Amazon EKS create cluster documentation at Create an Amazon EKS cluster.

The Prerequisite setup for hybrid nodes completed. Before you create your hybrid nodes-enabled cluster, you must have your on-premises node and optionally pod CIDRs identified, your VPC and subnets created according to the EKS requirements, and hybrid nodes requirements, and your security group with inbound rules for your on-premises and optionally pod CIDRs. For more information on these prerequisites, see Prepare networking for hybrid nodes.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the last version of the AWS CLI and Configuring settings for the AWS CLI in the AWS Command Line Interface User Guide.

An IAM principal with permissions to create IAM roles and attach policies, and create and describe EKS clusters

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode.

Your cluster must use IPv4 address family.

Your cluster must use either Public or Private cluster endpoint connectivity. Your cluster cannot use “Public and Private” cluster endpoint connectivity, because the Amazon EKS Kubernetes API server endpoint will resolve to the public IPs for hybrid nodes running outside of your VPC.

OIDC authentication is supported for EKS clusters with hybrid nodes.

You can add, change, or remove the hybrid nodes configuration of an existing cluster. For more information, see Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration.

If you already have a cluster IAM role, or you’re going to create your cluster with eksctl or AWS CloudFormation, then you can skip this step. By default, eksctl and the AWS CloudFormation template create the cluste

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## Manage kube-proxy in Amazon EKS clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/managing-kube-proxy.html

**Contents:**
- Manage kube-proxy in Amazon EKS clusters
        - Tip
- Install as Amazon EKS Add-on
- kube-proxy versions
        - Note
- kube-proxy container image

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

With Amazon EKS Auto Mode, you don’t need to install or upgrade networking add-ons. Auto Mode includes pod networking and load balancing capabilities.

For more information, see Automate cluster infrastructure with EKS Auto Mode.

We recommend adding the Amazon EKS type of the add-on to your cluster instead of using the self-managed type of the add-on. If you’re not familiar with the difference between the types, see Amazon EKS add-ons. For more information about adding an Amazon EKS add-on to your cluster, see Create an Amazon EKS add-on. If you’re unable to use the Amazon EKS add-on, we encourage you to submit an issue about why you can’t to the Containers roadmap GitHub repository.

The kube-proxy add-on is deployed on each Amazon EC2 node in your Amazon EKS cluster. It maintains network rules on your nodes and enables network communication to your Pods. The add-on isn’t deployed to Fargate nodes in your cluster. For more information, see kube-proxy in the Kubernetes documentation.

The following table lists the latest version of the Amazon EKS add-on type for each Kubernetes version.

An earlier version of the documentation was incorrect. kube-proxy versions v1.28.5, v1.27.9, and v1.26.12 aren’t available.

If you’re self-managing this add-on, the versions in the table might not be the same as the available self-managed versions.

The kube-proxy container image is based on a minimal base image maintained by Amazon EKS Distro, which contains minimal packages and doesn’t have shells. For more information, see Amazon EKS Distro.

The following table lists the latest available self-managed kube-proxy container image version for each Amazon EKS cluster version.

v1.33.3-minimal-eksbuild.11

v1.32.6-minimal-eksbuild.13

v1.31.10-minimal-eksbuild.13

v1.30.14-minimal-eksbuild.8

v1.29.15-minimal-eksbuild.16

v1.28.15-minimal-eksbuild.31

When you update an Amazon EKS add-on type, you specify a valid Amazon EKS add-on version, which might not be a version listed in this table. This is because Amazon EKS add-on versions don’t always match container image versions specified when updating the self-managed type of this add-on. When you update the self-managed type of this add-on, you specify a valid container image version listed in this table.

---

## Logging

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Logging.html#AmazonEKS-Type-Logging-clusterLogging

**Contents:**
- Logging
- Contents
- See Also

An object representing the logging configuration for resources in your cluster.

The cluster control plane logging configuration for your cluster.

Type: Array of LogSetup objects

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Create an EKS Auto Mode Cluster with the AWS CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-cli.html#auto-mode-create-roles

**Contents:**
- Create an EKS Auto Mode Cluster with the AWS CLI
- Prerequisites
- Specify VPC subnets
- IAM Roles for EKS Auto Mode Clusters
  - Cluster IAM Role
  - Node IAM Role
- Create an EKS Auto Mode Cluster IAM Role
  - Step 1: Create the Trust Policy
  - Step 2: Create the IAM Role
  - Step 3: Note the Role ARN

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

EKS Auto Mode Clusters automate routine cluster management tasks for compute, storage, and networking. For example, EKS Auto Mode Clusters automatically detect when additional nodes are required and provision new EC2 instances to meet workload demands.

This topic guides you through creating a new EKS Auto Mode Cluster using the AWS CLI and optionally deploying a sample workload.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide.

Login to the CLI with sufficent IAM permissions to create AWS resources including IAM Policies, IAM Roles, and EKS Clusters.

The kubectl command line tool installed on your device. AWS suggests you use the same kubectl version as the Kubernetes version of your EKS Cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Amazon EKS Auto Mode deploy nodes to VPC subnets. When creating an EKS cluster, you must specify the VPC subnets where the nodes will be deployed. You can use the default VPC subnets in your AWS account or create a dedicated VPC for critical workloads.

AWS suggests creating a dedicated VPC for your cluster. Learn how to Create an Amazon VPC for your Amazon EKS cluster.

The EKS Console assists with creating a new VPC. Learn how to Create an EKS Auto Mode Cluster with the AWS Management Console.

Alternatively, you can use the default VPC of your AWS account. Use the following instructions to find the Subnet IDs.

Run the following command to list the default VPC and its subnets:

Save the output and note the Subnet IDs.

EKS Auto Mode requires a Cluster IAM Role to perform actions in your AWS account, such as provisioning new EC2 instances. You must create this role to grant EKS the necessary permissions. AWS recommends attaching the following AWS managed policies to the Cluster IAM Role:

AmazonEKSComputePolicy

AmazonEKSBlockStoragePolicy

AmazonEKSLoadBalancingPolicy

AmazonEKSNetworkingPolicy

AmazonEKSClusterPolicy

When you create an EKS Auto Mode cluster, you specify a Node IAM Role. When EKS Auto Mode creates nodes to process pending workloads, each new EC2 instance node is assigned the Node IAM Role. This ro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
trust-policy.json
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ]
    }
  ]
}
```

Example 4 (unknown):
```unknown
aws iam attach-role-policy \
    --role-name AmazonEKSAutoClusterRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-endpoint

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Delete a cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/delete-cluster.html

**Contents:**
- Delete a cluster
- Considerations
  - Considerations for EKS Auto Mode
- Delete cluster (eksctl)
- Delete cluster (AWS console)
        - Note
- Delete cluster (AWS CLI)
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you’re done using an Amazon EKS cluster, you should delete the resources associated with it so that you don’t incur any unnecessary costs.

You can delete a cluster with eksctl, the AWS Management Console, or the AWS CLI.

If you receive an error because the cluster creator has been removed, see this article to resolve.

Amazon Managed Service for Prometheus resources are outside of the cluster lifecycle and need to be maintained independent of the cluster. When you delete your cluster, make sure to also delete any applicable scrapers to stop applicable costs. For more information, see Find and delete scrapers in the Amazon Managed Service for Prometheus User Guide.

To remove a connected cluster, see Deregister a Kubernetes cluster from the Amazon EKS console

Any EKS Auto Mode Nodes will be deleted, including the EC2 managed instances

All load balancers will be deleted

For more information, see Disable EKS Auto Mode.

This procedure requires eksctl version 0.215.0 or later. You can check your version with the following command:

For instructions on how to install or upgrade eksctl, see Installation in the eksctl documentation.

List all services running in your cluster.

Delete any services that have an associated EXTERNAL-IP value. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released. Replace service-name with the name of each service listed as described.

Delete the cluster and its associated nodes with the following command, replacing prod with your cluster name.

List all services running in your cluster.

Delete any services that have an associated EXTERNAL-IP value. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released. Replace service-name with the name of each service listed as described.

Delete all node groups and Fargate profiles.

Open the Amazon EKS console.

In the left navigation pane, choose Amazon EKS Clusters, and then in the tabbed list of clusters, choose the name of the cluster that you want to delete.

Choose the Compute tab and choose a node group to delete. Choose Delete, enter the name of the node group, and then cho

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl version
```

Example 2 (unknown):
```unknown
kubectl get svc --all-namespaces
```

Example 3 (unknown):
```unknown
EXTERNAL-IP
```

Example 4 (unknown):
```unknown
service-name
```

---

## Create an Amazon EKS cluster with hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-create.html

**Contents:**
- Create an Amazon EKS cluster with hybrid nodes
- Prerequisites
- Considerations
- Step 1: Create cluster IAM role
- Step 2: Create hybrid nodes-enabled cluster
  - Create hybrid nodes-enabled cluster - eksctl
  - Create hybrid nodes-enabled cluster - AWS CloudFormation
  - Create hybrid nodes-enabled cluster - AWS CLI
  - Create hybrid nodes-enabled cluster - AWS Management Console
- Step 3: Update kubeconfig

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you create a hybrid nodes-enabled Amazon EKS cluster. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes, including standard and extended support.

If you are not planning to use EKS Hybrid Nodes, see the primary Amazon EKS create cluster documentation at Create an Amazon EKS cluster.

The Prerequisite setup for hybrid nodes completed. Before you create your hybrid nodes-enabled cluster, you must have your on-premises node and optionally pod CIDRs identified, your VPC and subnets created according to the EKS requirements, and hybrid nodes requirements, and your security group with inbound rules for your on-premises and optionally pod CIDRs. For more information on these prerequisites, see Prepare networking for hybrid nodes.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the last version of the AWS CLI and Configuring settings for the AWS CLI in the AWS Command Line Interface User Guide.

An IAM principal with permissions to create IAM roles and attach policies, and create and describe EKS clusters

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode.

Your cluster must use IPv4 address family.

Your cluster must use either Public or Private cluster endpoint connectivity. Your cluster cannot use “Public and Private” cluster endpoint connectivity, because the Amazon EKS Kubernetes API server endpoint will resolve to the public IPs for hybrid nodes running outside of your VPC.

OIDC authentication is supported for EKS clusters with hybrid nodes.

You can add, change, or remove the hybrid nodes configuration of an existing cluster. For more information, see Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration.

If you already have a cluster IAM role, or you’re going to create your cluster with eksctl or AWS CloudFormation, then you can skip this step. By default, eksctl and the AWS CloudFormation template create the cluste

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-accessConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-computeConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Create an Amazon EKS cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html#step2-cli

**Contents:**
- Create an Amazon EKS cluster
        - Note
- Prerequisites
- Step 1: Create cluster IAM role
  - Service Linked Role
- Step 2: Create cluster
  - Create cluster - eksctl
    - Optional Settings
  - Create cluster - AWS console
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers creating EKS clusters without EKS Auto Mode.

For detailed instructions on creating an EKS Auto Mode cluster, see Create an Amazon EKS Auto Mode cluster.

To get started with EKS Auto Mode, see Get started with Amazon EKS – EKS Auto Mode.

This topic provides an overview of the available options and describes what to consider when you create an Amazon EKS cluster. If you need to create a cluster with your on-premises infrastructure as the compute for nodes, see Create an Amazon EKS cluster with hybrid nodes. If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our guides in Get started with Amazon EKS. These guides help you to create a simple, default cluster without expanding into all of the available options.

An existing VPC and subnets that meet Amazon EKS requirements. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements. If you don’t have a VPC and subnets, you can create them using an Amazon EKS provided AWS CloudFormation template.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

An IAM principal with permissions to create and describe an Amazon EKS cluster. For more information, see Create a local Kubernetes cluster on an Outpost and List or describe all clusters.

If you already have a cluster IAM role, or you're going to create your cluster with eksctl, you can skip the IAM role creation step. See also: [Create cluster IAM role](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html), [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), [Allowing users to access your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html), and [Launching Amazon EKS nodes](https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html).

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 3 (unknown):
```unknown
eks-cluster-role-trust-policy.json
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## Deploying an Amazon EKS IPv6 cluster and managed Amazon Linux nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/deploy-ipv6-cluster.html

**Contents:**
- Deploying an Amazon EKS IPv6 cluster and managed Amazon Linux nodes
- Prerequisites
- Deploy an IPv6 cluster with eksctl
- Deploy an IPv6 cluster with AWS CLI
        - Important
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

In this tutorial, you deploy an IPv6 Amazon VPC, an Amazon EKS cluster with the IPv6 family, and a managed node group with Amazon EC2 Amazon Linux nodes. You can’t deploy Amazon EC2 Windows nodes in an IPv6 cluster. You can also deploy Fargate nodes to your cluster, though those instructions aren’t provided in this topic for simplicity.

Complete the following before you start the tutorial:

Install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster.

We recommend that you familiarize yourself with all settings and deploy a cluster with the settings that meet your requirements. For more information, see Create an Amazon EKS cluster, Simplify node lifecycle with managed node groups, and the Considerations for this topic. You can only enable some settings when creating your cluster.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. For example, if your cluster version is 1.29, you can use kubectl version 1.28, 1.29, or 1.30 with it. To install or upgrade kubectl, see Set up kubectl and eksctl.

The IAM security principal that you’re using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources. For more information, see Actions and Using service-linked roles in the IAM User Guide.

If you use the eksctl, install version 0.215.0 or later on your computer. To install or update to it, see Installation in the eksctl documentation.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see [Installing and Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/install-cli.html) in the AWS CloudShell User Guide.

See also: [Create an Amazon EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html), [Control plane logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html), [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), [Access and node launch documentation](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html).

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
ipv6-cluster.yaml
```

Example 3 (unknown):
```unknown
region-code
```

Example 4 (unknown):
```unknown
my-nodegroup
```

---

## Cluster API server endpoint

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html#modify-endpoint-access

**Contents:**
- Cluster API server endpoint
- IPv6 cluster endpoint format
        - Note
- IPv4 cluster endpoint format
        - Note
- Cluster private endpoint
        - Note
- Modifying cluster endpoint access
- Accessing a private only API server

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic helps you to enable private access for your Amazon EKS cluster’s Kubernetes API server endpoint and limit, or completely disable, public access from the internet.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster (using Kubernetes management tools such as kubectl). By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management (IAM) and native Kubernetes Role Based Access Control (RBAC). This endpoint is known as the cluster public endpoint. Also there is a cluster private endpoint. For more information about the cluster private endpoint, see the following section Cluster private endpoint.

EKS creates a unique dual-stack endpoint in the following format for new IPv6 clusters that are made after October 2024. An IPv6 cluster is a cluster that you select IPv6 in the IP family (ipFamily) setting of the cluster.

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.amazonwebservices.com.cn

The dual-stack cluster endpoint was introduced in October 2024. For more information about IPv6 clusters, see Learn about IPv6 addresses to clusters, Pods, and services. Clusters made before October 2024, use following endpoint format instead.

EKS creates a unique endpoint in the following format for each cluster that select IPv4 in the IP family (ipFamily) setting of the cluster:

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.amazonwebservices.com.cn

Before October 2024, IPv6 clusters used this endpoint format also. For those clusters, both the public endpoint and the private endpoint have only IPv4 addresses resolve from this endpoint.

You can enable private access to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server.

Because this e

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 2 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 3 (unknown):
```unknown
eks-cluster.region.api.amazonwebservices.com.cn
```

Example 4 (unknown):
```unknown
eks-cluster.region.eks.amazonaws.com
```

---

## Deploy Windows nodes on EKS clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html

**Contents:**
- Deploy Windows nodes on EKS clusters
- Considerations
- Prerequisites
- Enable Windows support
- Deploy Windows Pods
- Support higher Pod density on Windows nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Learn how to enable and manage Windows support for your Amazon EKS cluster to run Windows containers alongside Linux containers.

Before deploying Windows nodes, be aware of the following considerations.

EKS Auto Mode does not support Windows nodes

You can use host networking on Windows nodes using HostProcess Pods. For more information, see Create a Windows HostProcessPod in the Kubernetes documentation.

Amazon EKS clusters must contain one or more Linux or Fargate nodes to run core system Pods that only run on Linux, such as CoreDNS.

The kubelet and kube-proxy event logs are redirected to the EKS Windows Event Log and are set to a 200 MB limit.

You can’t use Assign security groups to individual pods with Pods running on Windows nodes.

You can’t use custom networking with Windows nodes.

You can’t use IPv6 with Windows nodes.

Windows nodes support one elastic network interface per node. By default, the number of Pods that you can run per Windows node is equal to the number of IP addresses available per elastic network interface for the node’s instance type, minus one. For more information, see IP addresses per network interface per instance type in the Amazon EC2 User Guide.

In an Amazon EKS cluster, a single service with a load balancer can support up to 1024 back-end Pods. Each Pod has its own unique IP address. The previous limit of 64 Pods is no longer the case, after a Windows Server update starting with OS Build 17763.2746.

Windows containers aren’t supported for Amazon EKS Pods on Fargate.

You can’t use Amazon EKS Hybrid Nodes with Windows as the operating system for the host.

You can’t retrieve logs from the vpc-resource-controller Pod. You previously could when you deployed the controller to the data plane.

There is a cool down period before an IPv4 address is assigned to a new Pod. This prevents traffic from flowing to an older Pod with the same IPv4 address due to stale kube-proxy rules.

The source for the controller is managed on GitHub. To contribute to, or file issues against the controller, visit the project on GitHub.

When specifying a custom AMI ID for Windows managed node groups, add eks:kube-proxy-windows to your AWS IAM Authenticator configuration map. For more information, see Limits and conditions when specifying an AMI ID.

If preserving your available IPv4 addresses is cr

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
HostProcess
```

Example 2 (unknown):
```unknown
EKS Windows
```

Example 3 (unknown):
```unknown
vpc-resource-controller
```

Example 4 (unknown):
```unknown
eks:kube-proxy-windows
```

---

## Monitor your cluster metrics with Prometheus

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/prometheus.html#turn-on-prometheus-metrics

**Contents:**
- Monitor your cluster metrics with Prometheus
- Step 1: Turn on Prometheus metrics
        - Important
        - Important
- Step 2: Use the Prometheus metrics
- Step 3: Manage Prometheus scrapers

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Prometheus is a monitoring and time series database that scrapes endpoints. It provides the ability to query, aggregate, and store collected data. You can also use it for alerting and alert aggregation. This topic explains how to set up Prometheus as either a managed or open source option. Monitoring Amazon EKS control plane metrics is a common use case.

Amazon Managed Service for Prometheus is a Prometheus-compatible monitoring and alerting service that makes it easy to monitor containerized applications and infrastructure at scale. It is a fully-managed service that automatically scales the ingestion, storage, querying, and alerting of your metrics. It also integrates with AWS security services to enable fast and secure access to your data. You can use the open-source PromQL query language to query your metrics and alert on them. Also, you can use alert manager in Amazon Managed Service for Prometheus to set up alerting rules for critical alerts. You can then send these critical alerts as notifications to an Amazon SNS topic.

There are several different options for using Prometheus with Amazon EKS:

You can turn on Prometheus metrics when first creating an Amazon EKS cluster or you can create your own Prometheus scraper for existing clusters. Both of these options are covered by this topic.

You can deploy Prometheus using Helm. For more information, see Deploy Prometheus using Helm.

You can view control plane raw metrics in Prometheus format. For more information, see Fetch control plane raw metrics in Prometheus format.

Amazon Managed Service for Prometheus resources are outside of the cluster lifecycle and need to be maintained independent of the cluster. When you delete your cluster, make sure to also delete any applicable scrapers to stop applicable costs. For more information, see Find and delete scrapers in the Amazon Managed Service for Prometheus User Guide.

Prometheus discovers and collects metrics from your cluster through a pull-based model called scraping. Scrapers are set up to gather data from your cluster infrastructure and containerized applications. When you turn on the option to send Prometheus metrics, Amazon Managed Service for Prometheus provides a fully managed agentless scraper.

If you haven’t created the cluster yet, you can turn on the option to send metrics to Prometheus when

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonManagedScraperRole
```

Example 2 (unknown):
```unknown
AmazonManagedScraperRole
```

Example 3 (unknown):
```unknown
AmazonManagedScraperRole
```

Example 4 (unknown):
```unknown
DescribeScraper
```

---

## View Amazon EKS security group requirements for clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html#security-group-restricting-cluster-traffic

**Contents:**
- View Amazon EKS security group requirements for clusters
- Default cluster security group
        - Important
- Restricting cluster traffic
- Shared security groups
  - Considerations for Amazon EKS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes the security group requirements of an Amazon EKS cluster.

When you create a cluster, Amazon EKS creates a security group that’s named eks-cluster-sg-my-cluster-uniqueID . This security group has the following default rules:

0.0.0.0/0(IPv4) or ::/0 (IPv6)

Self (for EFA traffic)

The default security group includes an outbound rule that allows Elastic Fabric Adapter (EFA) traffic with the destination of the same security group. This enables EFA traffic within the cluster, which is beneficial for AI/ML and High Performance Computing (HPC) workloads. For more information, see Elastic Fabric Adapter for AI/ML and HPC workloads on Amazon EC2 in the Amazon Elastic Compute Cloud User Guide.

If your cluster doesn’t need the outbound rule, you can remove it. If you remove it, you must still have the minimum rules listed in Restricting cluster traffic. If you remove the inbound rule, Amazon EKS recreates it whenever the cluster is updated.

Amazon EKS adds the following tags to the security group. If you remove the tags, Amazon EKS adds them back to the security group whenever your cluster is updated.

kubernetes.io/cluster/my-cluster

eks-cluster-sg-my-cluster-uniqueid

Amazon EKS automatically associates this security group to the following resources that it also creates:

2–4 elastic network interfaces (referred to for the rest of this document as network interface) that are created when you create your cluster.

Network interfaces of the nodes in any managed node group that you create.

The default rules allow all traffic to flow freely between your cluster and nodes, and allows all outbound traffic to any destination. When you create a cluster, you can (optionally) specify your own security groups. If you do, then Amazon EKS also associates the security groups that you specify to the network interfaces that it creates for your cluster. However, it doesn’t associate them to any node groups that you create.

You can determine the ID of your cluster security group in the AWS Management Console under the cluster’s Networking section. Or, you can do so by running the following AWS CLI command.

If you need to limit the open ports between the cluster and nodes, you can remove the default outbound rule and add the following minimum rules that are required for the cluster. If you remove the default 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueID
```

Example 2 (unknown):
```unknown
kubernetes.io/cluster/my-cluster
```

Example 3 (unknown):
```unknown
aws:eks:cluster-name
```

Example 4 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueid
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#policy-create-local-cluster

**Contents:**
- Amazon EKS identity-based policy examples
        - Topics
- Policy best practices
- Using the Amazon EKS console
        - Important
- Allow IAM users to view their own permissions
- Create a Kubernetes cluster on the AWS Cloud
- Create a local Kubernetes cluster on an Outpost
- Update a Kubernetes cluster
- List or describe all clusters

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

By default, IAM users and roles don’t have permission to create or modify Amazon EKS resources. They also can’t perform tasks using the AWS Management Console, AWS CLI, or AWS API. An IAM administrator must create IAM policies that grant users and roles permission to perform specific API operations on the specified resources they need. The administrator must then attach those policies to the IAM users or groups that require those permissions.

To learn how to create an IAM identity-based policy using these example JSON policy documents, see Creating policies on the JSON tab in the IAM User Guide.

When you create an Amazon EKS cluster, the IAM principal that creates the cluster is automatically granted system:masters permissions in the cluster’s role-based access control (RBAC) configuration in the Amazon EKS control plane. This principal doesn’t appear in any visible configuration, so make sure to keep track of which principal originally created the cluster. To grant additional IAM principals the ability to interact with your cluster, edit the aws-auth ConfigMap within Kubernetes and create a Kubernetes rolebinding or clusterrolebinding with the name of a group that you specify in the aws-auth ConfigMap.

For more information about working with the ConfigMap, see Grant IAM users and roles access to Kubernetes APIs.

Policy best practices

Using the Amazon EKS console

Allow IAM users to view their own permissions

Create a Kubernetes cluster on the AWS Cloud

Create a local Kubernetes cluster on an Outpost

Update a Kubernetes cluster

List or describe all clusters

Identity-based policies determine whether someone can create, access, or delete Amazon EKS resources in your account. These actions can incur costs for your AWS account. When you create or edit identity-based policies, follow these guidelines and recommendations:

Get started with AWS managed policies and move toward least-privilege permissions – To get started granting permissions to your users and workloads, use the AWS managed policies that grant permissions for many common use cases. They are available in your AWS account. We recommend that you reduce permissions further by defining AWS customer managed policies that are specific to your use cases. For more information, see AWS managed policies or AWS managed policies for job functions in the 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
system:masters
```

Example 2 (unknown):
```unknown
aws-auth ConfigMap
```

Example 3 (unknown):
```unknown
rolebinding
```

Example 4 (unknown):
```unknown
clusterrolebinding
```

---

## Learn how access control works in Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-auth.html

**Contents:**
- Learn how access control works in Amazon EKS
- Common Tasks
- Background
- Considerations for EKS Auto Mode

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Learn how to manage access to your Amazon EKS cluster. Using Amazon EKS requires knowledge of how both Kubernetes and AWS Identity and Access Management (AWS IAM) handle access control.

This section includes:

Grant IAM users and roles access to Kubernetes APIs — Learn how to enable applications or users to authenticate to the Kubernetes API. You can use access entries, the aws-auth ConfigMap, or an external OIDC provider.

View Kubernetes resources in the AWS Management Console — Learn how to configure the AWS Management Console to communicate with your Amazon EKS cluster. Use the console to view Kubernetes resources in the cluster, such as namespaces, nodes, and Pods.

Connect kubectl to an EKS cluster by creating a kubeconfig file — Learn how to configure kubectl to communicate with your Amazon EKS cluster. Use the AWS CLI to create a kubeconfig file.

Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts — Learn how to associate a Kubernetes service account with AWS IAM Roles. You can use Pod Identity or IAM Roles for Service Accounts (IRSA).

Grant developers access to the Kubernetes API. View Kubernetes resources in the AWS Management Console.

Solution: Use access entries to associate Kubernetes RBAC permissions with AWS IAM Users or Roles.

Configure kubectl to talk to an Amazon EKS cluster using AWS Credentials.

Solution: Use the AWS CLI to create a kubeconfig file.

Use an external identity provider, such as Ping Identity, to authenticate users to the Kubernetes API.

Solution: Link an external OIDC provider.

Grant workloads on your Kubernetes cluster the ability to call AWS APIs.

Solution: Use Pod Identity to associate an AWS IAM Role to a Kubernetes Service Account.

Learn how Kubernetes Service Accounts work.

Review the Kubernetes Role Based Access Control (RBAC) Model

For more information about managing access to AWS resources, see the AWS IAM User Guide. Alternatively, take a free introductory training on using AWS IAM.

EKS Auto Mode integrates with EKS Pod Identity and EKS EKS access entries.

EKS Auto Mode uses access entries to grant the EKS control plane Kubernetes permissions. For example, the access policies enable EKS Auto Mode to read information about network endpoints and services.

You cannot disable access entries on an EKS Auto Mode cluster.

You can opti

*[Content truncated]*

---

## Compliance validation for Amazon EKS clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/compliance.html

**Contents:**
- Compliance validation for Amazon EKS clusters

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To learn whether an AWS service is within the scope of specific compliance programs, see AWS services in Scope by Compliance Program and choose the compliance program that you are interested in. For general information, see AWS Compliance Programs.

You can download third-party audit reports using AWS Artifact. For more information, see Downloading Reports in AWS Artifact.

Your compliance responsibility when using AWS services is determined by the sensitivity of your data, your company’s compliance objectives, and applicable laws and regulations. AWS provides the following resources to help with compliance:

Security Compliance & Governance – These solution implementation guides discuss architectural considerations and provide steps for deploying security and compliance features.

HIPAA Eligible Services Reference – Lists HIPAA eligible services. Not all AWS services are HIPAA eligible.

AWS Compliance Resources – This collection of workbooks and guides might apply to your industry and location.

AWS Customer Compliance Guides – Understand the shared responsibility model through the lens of compliance. The guides summarize the best practices for securing AWS services and map the guidance to security controls across multiple frameworks (including National Institute of Standards and Technology (NIST), Payment Card Industry Security Standards Council (PCI), and International Organization for Standardization (ISO)).

Evaluating Resources with Rules in the AWS Config Developer Guide – The AWS Config service assesses how well your resource configurations comply with internal practices, industry guidelines, and regulations.

AWS Security Hub – This AWS service provides a comprehensive view of your security state within AWS. Security Hub uses security controls to evaluate your AWS resources and to check your compliance against security industry standards and best practices. For a list of supported services and controls, see Security Hub controls reference.

Amazon GuardDuty – This AWS service detects potential threats to your AWS accounts, workloads, containers, and data by monitoring your environment for suspicious and malicious activities. GuardDuty can help you address various compliance requirements, like PCI DSS, by meeting intrusion detection requirements mandated by certain compliance frameworks.

AWS Audit Ma

*[Content truncated]*

---

## Organize and monitor cluster resources

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-managing.html

**Contents:**
- Organize and monitor cluster resources

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter includes the following topics to help you manage your cluster. You can also view information about your Kubernetes resources with the AWS Management Console.

The Kubernetes Dashboard is a general purpose, web-based UI for Kubernetes clusters. It allows users to manage applications running in the cluster and troubleshoot them, as well as manage the cluster itself. For more information, see The Kubernetes Dashboard GitHub repository.

View resource usage with the Kubernetes Metrics Server – The Kubernetes Metrics Server is an aggregator of resource usage data in your cluster. It isn’t deployed by default in your cluster, but is used by Kubernetes add-ons, such as the Kubernetes Dashboard and Scale pod deployments with Horizontal Pod Autoscaler. In this topic you learn how to install the Metrics Server.

Deploy applications with Helm on Amazon EKS – The Helm package manager for Kubernetes helps you install and manage applications on your Kubernetes cluster. This topic helps you install and run the Helm binaries so that you can install and manage charts using the Helm CLI on your local computer.

Organize Amazon EKS resources with tags – To help you manage your Amazon EKS resources, you can assign your own metadata to each resource in the form of tags. This topic describes tags and shows you how to create them.

View and manage Amazon EKS and Fargate service quotas – Your AWS account has default quotas, formerly referred to as limits, for each AWS service. Learn about the quotas for Amazon EKS and how to increase them.

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-outpostConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## ClusterIssue

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ClusterIssue.html#AmazonEKS-Type-ClusterIssue-resourceIds

**Contents:**
- ClusterIssue
- Contents
- See Also

An issue with your Amazon EKS cluster.

The error code of the issue.

Valid Values: AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other

A description of the issue.

The resource IDs that the issue relates to.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other
```

---

## ClusterIssue

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ClusterIssue.html

**Contents:**
- ClusterIssue
- Contents
- See Also

An issue with your Amazon EKS cluster.

The error code of the issue.

Valid Values: AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other

A description of the issue.

The resource IDs that the issue relates to.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other
```

---

## Create an Amazon EKS cluster with hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-create.html#hybrid-nodes-cluster-create-cli

**Contents:**
- Create an Amazon EKS cluster with hybrid nodes
- Prerequisites
- Considerations
- Step 1: Create cluster IAM role
- Step 2: Create hybrid nodes-enabled cluster
  - Create hybrid nodes-enabled cluster - eksctl
  - Create hybrid nodes-enabled cluster - AWS CloudFormation
  - Create hybrid nodes-enabled cluster - AWS CLI
  - Create hybrid nodes-enabled cluster - AWS Management Console
- Step 3: Update kubeconfig

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you create a hybrid nodes-enabled Amazon EKS cluster. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes, including standard and extended support.

If you are not planning to use EKS Hybrid Nodes, see the primary Amazon EKS create cluster documentation at Create an Amazon EKS cluster.

The Prerequisite setup for hybrid nodes completed. Before you create your hybrid nodes-enabled cluster, you must have your on-premises node and optionally pod CIDRs identified, your VPC and subnets created according to the EKS requirements, and hybrid nodes requirements, and your security group with inbound rules for your on-premises and optionally pod CIDRs. For more information on these prerequisites, see Prepare networking for hybrid nodes.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the last version of the AWS CLI and Configuring settings for the AWS CLI in the AWS Command Line Interface User Guide.

An IAM principal with permissions to create IAM roles and attach policies, and create and describe EKS clusters

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode.

Your cluster must use IPv4 address family.

Your cluster must use either Public or Private cluster endpoint connectivity. Your cluster cannot use “Public and Private” cluster endpoint connectivity, because the Amazon EKS Kubernetes API server endpoint will resolve to the public IPs for hybrid nodes running outside of your VPC.

OIDC authentication is supported for EKS clusters with hybrid nodes.

You can add, change, or remove the hybrid nodes configuration of an existing cluster. For more information, see Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration.

If you already have a cluster IAM role, or you’re going to create your cluster with eksctl or AWS CloudFormation, then you can skip this step. By default, eksctl and the AWS CloudFormation template create the cluste

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#API_CreateCluster_RequestSyntax

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## View Amazon EKS security group requirements for clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html#security-group-default-rules

**Contents:**
- View Amazon EKS security group requirements for clusters
- Default cluster security group
        - Important
- Restricting cluster traffic
- Shared security groups
  - Considerations for Amazon EKS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes the security group requirements of an Amazon EKS cluster.

When you create a cluster, Amazon EKS creates a security group that’s named eks-cluster-sg-my-cluster-uniqueID . This security group has the following default rules:

0.0.0.0/0(IPv4) or ::/0 (IPv6)

Self (for EFA traffic)

The default security group includes an outbound rule that allows Elastic Fabric Adapter (EFA) traffic with the destination of the same security group. This enables EFA traffic within the cluster, which is beneficial for AI/ML and High Performance Computing (HPC) workloads. For more information, see Elastic Fabric Adapter for AI/ML and HPC workloads on Amazon EC2 in the Amazon Elastic Compute Cloud User Guide.

If your cluster doesn’t need the outbound rule, you can remove it. If you remove it, you must still have the minimum rules listed in Restricting cluster traffic. If you remove the inbound rule, Amazon EKS recreates it whenever the cluster is updated.

Amazon EKS adds the following tags to the security group. If you remove the tags, Amazon EKS adds them back to the security group whenever your cluster is updated.

kubernetes.io/cluster/my-cluster

eks-cluster-sg-my-cluster-uniqueid

Amazon EKS automatically associates this security group to the following resources that it also creates:

2–4 elastic network interfaces (referred to for the rest of this document as network interface) that are created when you create your cluster.

Network interfaces of the nodes in any managed node group that you create.

The default rules allow all traffic to flow freely between your cluster and nodes, and allows all outbound traffic to any destination. When you create a cluster, you can (optionally) specify your own security groups. If you do, then Amazon EKS also associates the security groups that you specify to the network interfaces that it creates for your cluster. However, it doesn’t associate them to any node groups that you create.

You can determine the ID of your cluster security group in the AWS Management Console under the cluster’s Networking section. Or, you can do so by running the following AWS CLI command.

If you need to limit the open ports between the cluster and nodes, you can remove the default outbound rule and add the following minimum rules that are required for the cluster. If you remove the default 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueID
```

Example 2 (unknown):
```unknown
kubernetes.io/cluster/my-cluster
```

Example 3 (unknown):
```unknown
aws:eks:cluster-name
```

Example 4 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueid
```

---

## Delete a managed node group from your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/delete-managed-node-group.html

**Contents:**
- Delete a managed node group from your cluster
        - Important
- eksctl
- AWS Management Console
- AWS CLI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how you can delete an Amazon EKS managed node group. When you delete a managed node group, Amazon EKS first sets the minimum, maximum, and desired size of your Auto Scaling group to zero. This then causes your node group to scale down.

Before each instance is terminated, Amazon EKS sends a signal to drain that node. During the drain process, Kubernetes does the following for each pod on the node: runs any configured preStop lifecycle hooks, sends SIGTERM signals to the containers, then waits for the terminationGracePeriodSeconds for graceful shutdown. If the node hasn’t been drained after 5 minutes, Amazon EKS lets Auto Scaling continue the forced termination of the instance. After all instances have been terminated, the Auto Scaling group is deleted.

If you delete a managed node group that uses a node IAM role that isn’t used by any other managed node group in the cluster, the role is removed from the aws-auth ConfigMap. If any of the self-managed node groups in the cluster are using the same node IAM role, the self-managed nodes move to the NotReady status. Additionally, the cluster operation is also disrupted. To add a mapping for the role you’re using only for the self-managed node groups, see Create access entries, if your cluster’s platform version is at least minimum version listed in the prerequisites section of Grant IAM users access to Kubernetes with EKS access entries. If your platform version is earlier than the required minimum version for access entries, you can add the entry back to the aws-auth ConfigMap. For more information, enter eksctl create iamidentitymapping --help in your terminal.

You can delete a managed node group with:

AWS Management Console

Delete a managed node group with eksctl

Enter the following command. Replace every <example value> with your own values.

For more options, see Deleting and draining nodegroups in the eksctl documentation.

Delete a managed node group with AWS Management Console

Open the Amazon EKS console.

On the Clusters page, choose the cluster that contains the node group to delete.

On the selected cluster page, choose the Compute tab.

In the Node groups section, choose the node group to delete. Then choose Delete.

In the Delete node group confirmation dialog box, enter the name of the node group. Then choose Delete.

Delete 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
terminationGracePeriodSeconds
```

Example 2 (unknown):
```unknown
eksctl create iamidentitymapping --help
```

Example 3 (unknown):
```unknown
<example value>
```

Example 4 (unknown):
```unknown
eksctl delete nodegroup \
  --cluster <my-cluster> \
  --name <my-mng> \
  --region <region-code>
```

---

## Monitor your cluster performance and view logs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-observe.html

**Contents:**
- Monitor your cluster performance and view logs
- Monitoring and logging on Amazon EKS
        - Note
- Amazon EKS monitoring and logging tools

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can observe your data in Amazon EKS using many available monitoring or logging tools. Your Amazon EKS log data can be streamed to AWS services or to partner tools for data analysis. There are many services available in the AWS Management Console that provide data for troubleshooting your Amazon EKS issues. You can also use an AWS-supported open-source solution for monitoring Amazon EKS infrastructure.

After selecting Clusters in the left navigation pane of the Amazon EKS console, you can view cluster health and details by choosing your cluster’s name and choosing the Observability tab. To view details about any existing Kubernetes resources that are deployed to your cluster, see View Kubernetes resources in the AWS Management Console.

Monitoring is an important part of maintaining the reliability, availability, and performance of Amazon EKS and your AWS solutions. We recommend that you collect monitoring data from all of the parts of your AWS solution. That way, you can more easily debug a multi-point failure if one occurs. Before you start monitoring Amazon EKS, make sure that your monitoring plan addresses the following questions.

What are your goals? Do you need real-time notifications if your clusters scale dramatically?

What resources need to be observed?

How frequently do you need to observe these resources? Does your company want to respond quickly to risks?

What tools do you intend to use? If you already run AWS Fargate as part of your launch, then you can use the built-in log router.

Who do you intend to perform the monitoring tasks?

Whom do you want notifications to be sent to when something goes wrong?

Amazon EKS provides built-in tools for monitoring and logging. For supported versions, the observability dashboard gives visibility into the performance of your cluster. It helps you to quickly detect, troubleshoot, and remediate issues. In addition to monitoring features, it includes lists based on the control plane audit logs. The Kubernetes control plane exposes a number of metrics that that can also be scraped outside of the console.

Control plane logging records all API calls to your clusters, audit information capturing what users performed what actions to your clusters, and role-based information. For more information, see Logging and monitoring on Amazon EKS in the AWS Prescripti

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
level=info msg="mapping IAM role" groups="[]" role="arn:aws:iam::111122223333:role/XXXXXXXXXXXXXXXXXX-NodeManagerRole-XXXXXXXX" username="eks:node-manager"
```

---

## Update existing cluster to new Kubernetes version

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html

**Contents:**
- Update existing cluster to new Kubernetes version
        - Important
        - Note
- Considerations for Amazon EKS Auto Mode
- Summary
- Step 1: Prepare for upgrade
- Step 2: Review upgrade considerations
  - Review upgrade insights
  - Detailed considerations
- Step 3: Update cluster control plane

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When a new Kubernetes version is available in Amazon EKS, you can update your Amazon EKS cluster to the latest version.

Once you upgrade a cluster, you can’t downgrade to a previous version. Before you update to a new Kubernetes version, we recommend that you review the information in Understand the Kubernetes version lifecycle on EKS and the update steps in this topic.

New Kubernetes versions sometimes introduce significant changes. Therefore, we recommend that you test the behavior of your applications against a new Kubernetes version before you update your production clusters. You can do this by building a continuous integration workflow to test your application behavior before moving to a new Kubernetes version.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they’re working as expected. However, once you’ve started the cluster upgrade, you can’t pause or stop it. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version. Running applications aren’t affected, and your cluster is never left in a non-deterministic or unrecoverable state. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary. We’re constantly evaluating and improving our Kubernetes infrastructure management processes.

To update the cluster, Amazon EKS requires up to five available IP addresses from the subnets that you specified when you created your cluster. Amazon EKS creates new cluster elastic network interfaces (network interfaces) in any of the subnets that you specified. The network interfaces may be created in different subnets than your existing network interfaces are in, so make sure that your security group rules allow required cluster communication for any of the subnets that you specified when you created your cluster. If any of the subnets that you specified when you created the cluster don’t exist, don’t have enough available IP addresses, or don’t have security group rules that allows necessary cluster communication, then the update can fail.

To ensure that the API server endpoint 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
cluster-autoscaler
```

Example 2 (unknown):
```unknown
kubectl version
```

Example 3 (unknown):
```unknown
kubectl get nodes
```

Example 4 (unknown):
```unknown
kube-apiserver
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-kubernetesNetworkConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## CreateAccessConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateAccessConfigRequest.html#AmazonEKS-Type-CreateAccessConfigRequest-bootstrapClusterCreatorAdminPermissions

**Contents:**
- CreateAccessConfigRequest
- Contents
- See Also

The access configuration information for the cluster.

The desired authentication mode for the cluster. If you create a cluster by using the EKS API, AWS SDKs, or AWS CloudFormation, the default is CONFIG_MAP. If you create the cluster by using the AWS Management Console, the default value is API_AND_CONFIG_MAP.

Valid Values: API | API_AND_CONFIG_MAP | CONFIG_MAP

Specifies whether or not the cluster creator IAM principal was set as a cluster admin access entry during cluster creation time. The default value is true.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 2 (unknown):
```unknown
API | API_AND_CONFIG_MAP | CONFIG_MAP
```

---

## Remove an Amazon EKS add-on from a cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/removing-an-add-on.html

**Contents:**
- Remove an Amazon EKS add-on from a cluster
- Prerequisites
- Procedure
  - Remove add-on (eksctl)
  - Remove add-on (AWS Console)
  - Remove add-on (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can remove an Amazon EKS add-on from your cluster using eksctl, the AWS Management Console, or the AWS CLI.

When you remove an Amazon EKS add-on from a cluster:

There is no downtime for the functionality that the add-on provides.

If you are using IAM Roles for Service Accounts (IRSA) and the add-on has an IAM role associated with it, the IAM role isn’t removed.

If you are using Pod Identities, any Pod Identity Associations owned by the add-on are removed. If you specify the --preserve option to the AWS CLI, the associations are preserved.

Amazon EKS stops managing settings for the add-on.

The console stops notifying you when new versions are available.

You can’t update the add-on using any AWS tools or APIs.

You can choose to leave the add-on software on your cluster so that you can self-manage it, or you can remove the add-on software from your cluster. You should only remove the add-on software from your cluster if there are no resources on your cluster are dependent on the functionality that the add-on provides.

Complete the following before you create an add-on:

An existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS.

Check if your add-on requires an IAM role. For more information, see

Version 0.215.0 or later of the eksctl command line tool installed on your device or AWS CloudShell. To install or update eksctl, see Installation in the eksctl documentation..

You have two options when removing an Amazon EKS add-on.

Preserve add-on software on your cluster – This option removes Amazon EKS management of any settings. It also removes the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add-on after you initiate an update. However, it preserves the add-on software on your cluster. This option makes the add-on a self-managed installation, rather than an Amazon EKS add-on. With this option, there’s no downtime for the add-on.

Remove add-on software entirely from your cluster – We recommend that you remove the Amazon EKS add-on from your cluster only if there are no resources on your cluster that are dependent on it.

You can remove an Amazon EKS add-on using eksctl, the AWS Management Console, or the AWS CLI.

Determine the current add-ons installed on your cluster. Replace my-cluster with the name of your cluster.

An example outpu

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl get addon --cluster my-cluster
```

Example 2 (unknown):
```unknown
NAME        VERSION              STATUS  ISSUES  IAMROLE  UPDATE AVAILABLE
coredns     v1.8.7-eksbuild.2    ACTIVE  0
kube-proxy  v1.23.7-eksbuild.1   ACTIVE  0
vpc-cni     v1.10.4-eksbuild.1   ACTIVE  0
[...]
```

Example 3 (unknown):
```unknown
name-of-add-on
```

Example 4 (unknown):
```unknown
eksctl delete addon --cluster my-cluster --name name-of-addon --preserve
```

---

## Cluster API server endpoint

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html

**Contents:**
- Cluster API server endpoint
- IPv6 cluster endpoint format
        - Note
- IPv4 cluster endpoint format
        - Note
- Cluster private endpoint
        - Note
- Modifying cluster endpoint access
- Accessing a private only API server

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic helps you to enable private access for your Amazon EKS cluster’s Kubernetes API server endpoint and limit, or completely disable, public access from the internet.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster (using Kubernetes management tools such as kubectl). By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management (IAM) and native Kubernetes Role Based Access Control (RBAC). This endpoint is known as the cluster public endpoint. Also there is a cluster private endpoint. For more information about the cluster private endpoint, see the following section Cluster private endpoint.

EKS creates a unique dual-stack endpoint in the following format for new IPv6 clusters that are made after October 2024. An IPv6 cluster is a cluster that you select IPv6 in the IP family (ipFamily) setting of the cluster.

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.aws

EKS cluster public/private endpoint: eks-cluster.region.api.amazonwebservices.com.cn

The dual-stack cluster endpoint was introduced in October 2024. For more information about IPv6 clusters, see Learn about IPv6 addresses to clusters, Pods, and services. Clusters made before October 2024, use following endpoint format instead.

EKS creates a unique endpoint in the following format for each cluster that select IPv4 in the IP family (ipFamily) setting of the cluster:

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.eks.amazonaws.com

EKS cluster public/private endpoint eks-cluster.region.amazonwebservices.com.cn

Before October 2024, IPv6 clusters used this endpoint format also. For those clusters, both the public endpoint and the private endpoint have only IPv4 addresses resolve from this endpoint.

You can enable private access to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server.

Because this e

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 2 (unknown):
```unknown
eks-cluster.region.api.aws
```

Example 3 (unknown):
```unknown
eks-cluster.region.api.amazonwebservices.com.cn
```

Example 4 (unknown):
```unknown
eks-cluster.region.eks.amazonaws.com
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-id

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Verify Amazon EKS add-on version compatibility with a cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/addon-compat.html

**Contents:**
- Verify Amazon EKS add-on version compatibility with a cluster
- Add-on compatibility with compute types

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Before you create an Amazon EKS add-on you need to verify that the Amazon EKS add-on version is compatible with your cluster.

Use the describe-addon-versions API to list the available versions of EKS add-ons, and which Kubernetes versions each addon version supports.

Verify the AWS CLI is installed and working with aws sts get-caller-identity. If this command doesn’t work, learn how to Get started with the AWS CLI.

Determine the name of the add-on you want to retrieve version compatibility information for, such as amazon-cloudwatch-observability.

Determine the Kubernetes version of your cluster, such as 1.33.

Use the AWS CLI to retrieve the addon versions that are compatible with the Kubernetes version of your cluster.

An example output is as follows.

This output shows that addon version vX.X.X-eksbuild.X is compatible with Kubernetes cluster version 1.33.

The computeTypes field in the describe-addon-versions output indicates an add-on’s compatibility with EKS Auto Mode Managed Nodes or Hybrid Nodes. Add-ons marked auto work with EKS Auto Mode’s cloud-based, AWS-managed infrastructure, while those marked hybrid can run on on-premises nodes connected to the EKS cloud control plane.

For more information, see Considerations for Amazon EKS Auto Mode.

**Examples:**

Example 1 (unknown):
```unknown
aws sts get-caller-identity
```

Example 2 (unknown):
```unknown
amazon-cloudwatch-observability
```

Example 3 (unknown):
```unknown
aws eks describe-addon-versions --addon-name amazon-cloudwatch-observability --kubernetes-version 1.33
```

Example 4 (unknown):
```unknown
{
    "addons": [
        {
            "addonName": "amazon-cloudwatch-observability",
            "type": "observability",
            "addonVersions": [
                {
                    "addonVersion": "vX.X.X-eksbuild.X",
                    "architecture": [
                        "amd64",
                        "arm64"
                    ],
                    "computeTypes": [
                        "ec2",
                        "auto",
                        "hybrid"
                    ],
                    "compatibilities": [
                        {
                   
...
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-resourcesVpcConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Create an IAM OIDC provider for your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html

**Contents:**
- Create an IAM OIDC provider for your cluster
- Prerequisites
- Create OIDC provider (eksctl)
        - Note
- Create OIDC provider (AWS Console)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Your cluster has an OpenID Connect (OIDC) issuer URL associated with it. To use AWS Identity and Access Management (IAM) roles for service accounts, an IAM OIDC provider must exist for your cluster’s OIDC issuer URL.

An existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. For example, if your cluster version is 1.29, you can use kubectl version 1.28, 1.29, or 1.30 with it. To install or upgrade kubectl, see Set up kubectl and eksctl.

An existing kubectl config file that contains your cluster configuration. To create a kubectl config file, see Connect kubectl to an EKS cluster by creating a kubeconfig file.

You can create an IAM OIDC provider for your cluster using eksctl or the AWS Management Console.

Version 0.215.0 or later of the eksctl command line tool installed on your device or AWS CloudShell. To install or update eksctl, see Installation in the eksctl documentation.

Determine the OIDC issuer ID for your cluster.

Retrieve your cluster’s OIDC issuer ID and store it in a variable. Replace <my-cluster> with your own value.

Determine whether an IAM OIDC provider with your cluster’s issuer ID is already in your account.

If output is returned, then you already have an IAM OIDC provider for your cluster and you can skip the next step. If no output is returned, then you must create an IAM OIDC provider for your cluster.

Create an IAM OIDC identity provider for your cluster with the followi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
<my-cluster>
```

Example 3 (unknown):
```unknown
cluster_name=<my-cluster>
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo $oidc_id
```

Example 4 (unknown):
```unknown
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-clientRequestToken

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-upgradePolicy

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-logging

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Amazon EKS cluster IAM role

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-iam-role.html

**Contents:**
- Amazon EKS cluster IAM role
        - Note
- Check for an existing cluster role
- Creating the Amazon EKS cluster role

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

An Amazon EKS cluster IAM role is required for each cluster. Kubernetes clusters managed by Amazon EKS use this role to manage nodes and the legacy Cloud Provider uses this role to create load balancers with Elastic Load Balancing for services.

Before you can create Amazon EKS clusters, you must create an IAM role with either of the following IAM policies:

AmazonEKSClusterPolicy

A custom IAM policy. The minimal permissions that follow allows the Kubernetes cluster to manage nodes, but doesn’t allow the legacy Cloud Provider to create load balancers with Elastic Load Balancing. Your custom IAM policy must have at least the following permissions:

Prior to October 3, 2023, AmazonEKSClusterPolicy was required on the IAM role for each cluster.

Prior to April 16, 2020, AmazonEKSServicePolicy and AmazonEKSClusterPolicy was required and the suggested name for the role was eksServiceRole. With the AWSServiceRoleForAmazonEKS service-linked role, the AmazonEKSServicePolicy policy is no longer required for clusters created on or after April 16, 2020.

You can use the following procedure to check and see if your account already has the Amazon EKS cluster role.

Open the IAM console at https://console.aws.amazon.com/iam/.

In the left navigation pane, choose Roles.

Search the list of roles for eksClusterRole. If a role that includes eksClusterRole doesn’t exist, then see Creating the Amazon EKS cluster role to create the role. If a role that includes eksClusterRole does exist, then select the role to view the attached policies.

Ensure that the AmazonEKSClusterPolicy managed policy is attached to the role. If the policy is attached, your Amazon EKS cluster role is properly configured.

Choose Trust relationships, and then choose Edit trust policy.

Verify that the trust relationship contains the following policy. If the trust relationship matches the following policy, choose Cancel. If the trust relationship doesn’t match, copy the policy into the Edit trust policy window and choose Update policy.

You can use the AWS Management Console or the AWS CLI to create the cluster role.

Open the IAM console at https://console.aws.amazon.com/iam/.

Choose Roles, then Create role.

Under Trusted entity type, select AWS service.

From the Use cases for other AWS services dropdown list, choose EKS.

Choose EKS - Cluster for your

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags"
      ],
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "ForAnyValue:StringLike": {
          "aws:TagKeys": "kubernetes.io/cluster/*"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeVpcs",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeInstanceTopology",
        "kms:DescribeKey
...
```

Example 2 (unknown):
```unknown
eksServiceRole
```

Example 3 (unknown):
```unknown
AWSServiceRoleForAmazonEKS
```

Example 4 (unknown):
```unknown
eksClusterRole
```

---

## View current cluster upgrade policy

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/view-upgrade-policy.html

**Contents:**
- View current cluster upgrade policy
        - Important
- View cluster upgrade policy (AWS Console)
- View cluster upgrade policy (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The cluster upgrade policy determines what happens to your cluster when it leaves the standard support period. If your upgrade policy is EXTENDED, the cluster will not be automatically upgraded, and will enter extended support. If your upgrade policy is STANDARD, it will be automatically upgraded.

Amazon EKS controls for Kubernetes version policy allows you to choose the end of standard support behavior for your EKS clusters. With these controls you can decide which clusters should enter extended support and which clusters should be automatically upgraded at the end of standard support for a Kubernetes version.

A minor version is under standard support in Amazon EKS for the first 14 months after it’s released. Once a version is past the end of standard support date, it enters extended support for the next 12 months. Extended support allows you to stay at a specific Kubernetes version for longer at an additional cost per cluster hour. You can enable or disable extended support for an EKS Cluster. If you disable extended support, AWS will automatically upgrade your cluster to the next version at the end of standard support. If you enable extended support, you can stay at the current version for an additional cost for a limited period of time. Plan to regularly upgrade your Kubernetes cluster, even if you use extended support.

You can set the version policy for both new and existing clusters, using the supportType property. There are two options that can be used to set the version support policy:

STANDARD — Your EKS cluster eligible for automatic upgrade at the end of standard support. You will not incur extended support charges with this setting but you EKS cluster will automatically upgrade to the next supported Kubernetes version in standard support.

EXTENDED — Your EKS cluster will enter into extended support once the Kubernetes version reaches end of standard support. You will incur extended support charges with this setting. You can upgrade your cluster to a standard supported Kubernetes version to stop incurring extended support charges. Clusters running on extended support will be eligible for automatic upgrade at the end of extended support.

Extended support is enabled by default for new clusters, and existing clusters. You can view if extended support is enabled for a cluster in the AWS Management

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
supportType
```

Example 2 (unknown):
```unknown
aws eks describe-cluster \
--name <cluster-name> \
--query "cluster.upgradePolicy.supportType"
```

---

## Troubleshoot problems with Amazon EKS clusters and nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html#cluster-health-status

**Contents:**
- Troubleshoot problems with Amazon EKS clusters and nodes
- Insufficient capacity
- Nodes fail to join cluster
- Unauthorized or access denied (kubectl)
- hostname doesn’t match
- getsockopt: no route to host
- Instances failed to join the Kubernetes cluster
- Managed node group error codes
- Not authorized for images
- Node is in NotReady state

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them. If you need to troubleshoot specific Amazon EKS areas, see the separate Troubleshooting IAM, Troubleshoot Amazon EKS Connector issues, and Troubleshooting for ADOT using EKS Add-Ons topics.

For other troubleshooting information, see Knowledge Center content about Amazon Elastic Kubernetes Service on AWS re:Post.

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified doesn’t have sufficient capacity to support a cluster.

Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message.

There are Availability Zones that a cluster can’t reside in. Compare the Availability Zones that your subnets are in with the list of Availability Zones in the Subnet requirements and considerations.

There are a few common reasons that prevent nodes from joining the cluster:

If the nodes are managed nodes, Amazon EKS adds entries to the aws-auth ConfigMap when you create the node group. If the entry was removed or modified, then you need to re-add it. For more information, enter eksctl create iamidentitymapping --help in your terminal. You can view your current aws-auth ConfigMap entries by replacing my-cluster in the following command with the name of your cluster and then running the modified command: eksctl get iamidentitymapping --cluster my-cluster . The ARN of the role that you specify can’t include a path other than /. For example, if the name of your role is development/apps/my-role, you’d need to change it to my-role when specifying the ARN for the role. Make sure that you specify the node IAM role ARN (not the instance profile ARN).

If the nodes are self-managed, and you haven’t created access entries for the ARN of the node’s IAM role, then run the same commands listed for managed nodes. If you have created an access entry for the ARN for your node IAM role, then it might not be configured properly in the access entry. Make s

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c
```

Example 2 (unknown):
```unknown
eksctl create iamidentitymapping --help
```

Example 3 (unknown):
```unknown
eksctl get iamidentitymapping --cluster my-cluster
```

Example 4 (unknown):
```unknown
development/apps/my-role
```

---

## Create an Amazon EKS cluster with hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-create.html#hybrid-nodes-cluster-create-cfn

**Contents:**
- Create an Amazon EKS cluster with hybrid nodes
- Prerequisites
- Considerations
- Step 1: Create cluster IAM role
- Step 2: Create hybrid nodes-enabled cluster
  - Create hybrid nodes-enabled cluster - eksctl
  - Create hybrid nodes-enabled cluster - AWS CloudFormation
  - Create hybrid nodes-enabled cluster - AWS CLI
  - Create hybrid nodes-enabled cluster - AWS Management Console
- Step 3: Update kubeconfig

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you create a hybrid nodes-enabled Amazon EKS cluster. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes, including standard and extended support.

If you are not planning to use EKS Hybrid Nodes, see the primary Amazon EKS create cluster documentation at Create an Amazon EKS cluster.

The Prerequisite setup for hybrid nodes completed. Before you create your hybrid nodes-enabled cluster, you must have your on-premises node and optionally pod CIDRs identified, your VPC and subnets created according to the EKS requirements, and hybrid nodes requirements, and your security group with inbound rules for your on-premises and optionally pod CIDRs. For more information on these prerequisites, see Prepare networking for hybrid nodes.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the last version of the AWS CLI and Configuring settings for the AWS CLI in the AWS Command Line Interface User Guide.

An IAM principal with permissions to create IAM roles and attach policies, and create and describe EKS clusters

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode.

Your cluster must use IPv4 address family.

Your cluster must use either Public or Private cluster endpoint connectivity. Your cluster cannot use “Public and Private” cluster endpoint connectivity, because the Amazon EKS Kubernetes API server endpoint will resolve to the public IPs for hybrid nodes running outside of your VPC.

OIDC authentication is supported for EKS clusters with hybrid nodes.

You can add, change, or remove the hybrid nodes configuration of an existing cluster. For more information, see Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration.

If you already have a cluster IAM role, or you’re going to create your cluster with eksctl or AWS CloudFormation, then you can skip this step. By default, eksctl and the AWS CloudFormation template create the cluste

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## Troubleshoot problems with Amazon EKS clusters and nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html#unauthorized

**Contents:**
- Troubleshoot problems with Amazon EKS clusters and nodes
- Insufficient capacity
- Nodes fail to join cluster
- Unauthorized or access denied (kubectl)
- hostname doesn’t match
- getsockopt: no route to host
- Instances failed to join the Kubernetes cluster
- Managed node group error codes
- Not authorized for images
- Node is in NotReady state

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them. If you need to troubleshoot specific Amazon EKS areas, see the separate Troubleshooting IAM, Troubleshoot Amazon EKS Connector issues, and Troubleshooting for ADOT using EKS Add-Ons topics.

For other troubleshooting information, see Knowledge Center content about Amazon Elastic Kubernetes Service on AWS re:Post.

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified doesn’t have sufficient capacity to support a cluster.

Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message.

There are Availability Zones that a cluster can’t reside in. Compare the Availability Zones that your subnets are in with the list of Availability Zones in the Subnet requirements and considerations.

There are a few common reasons that prevent nodes from joining the cluster:

If the nodes are managed nodes, Amazon EKS adds entries to the aws-auth ConfigMap when you create the node group. If the entry was removed or modified, then you need to re-add it. For more information, enter eksctl create iamidentitymapping --help in your terminal. You can view your current aws-auth ConfigMap entries by replacing my-cluster in the following command with the name of your cluster and then running the modified command: eksctl get iamidentitymapping --cluster my-cluster . The ARN of the role that you specify can’t include a path other than /. For example, if the name of your role is development/apps/my-role, you’d need to change it to my-role when specifying the ARN for the role. Make sure that you specify the node IAM role ARN (not the instance profile ARN).

If the nodes are self-managed, and you haven’t created access entries for the ARN of the node’s IAM role, then run the same commands listed for managed nodes. If you have created an access entry for the ARN for your node IAM role, then it might not be configured properly in the access entry. Make s

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c
```

Example 2 (unknown):
```unknown
eksctl create iamidentitymapping --help
```

Example 3 (unknown):
```unknown
eksctl get iamidentitymapping --cluster my-cluster
```

Example 4 (unknown):
```unknown
development/apps/my-role
```

---

## Monitor and optimize Amazon EKS cluster costs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cost-monitoring.html

**Contents:**
- Monitor and optimize Amazon EKS cluster costs

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Cost monitoring is an essential aspect of managing your Kubernetes clusters on Amazon EKS. By gaining visibility into your cluster costs, you can optimize resource utilization, set budgets, and make data-driven decisions about your deployments. Amazon EKS provides two cost monitoring solutions, each with its own unique advantages, to help you track and allocate your costs effectively:

AWS Billing split cost allocation data for Amazon EKS — This native feature integrates seamlessly with the AWS Billing Console, allowing you to analyze and allocate costs using the same familiar interface and workflows you use for other AWS services. With split cost allocation, you can gain insights into your Kubernetes costs directly alongside your other AWS spend, making it easier to optimize costs holistically across your AWS environment. You can also leverage existing AWS Billing features like Cost Categories and Cost Anomaly Detection to further enhance your cost management capabilities. For more information, see Understanding split cost allocation data in the AWS Billing User Guide.

Kubecost — Amazon EKS supports Kubecost, a Kubernetes cost monitoring tool. Kubecost offers a feature-rich, Kubernetes-native approach to cost monitoring, providing granular cost breakdowns by Kubernetes resources, cost optimization recommendations, and out-of-the-box dashboards and reports. Kubecost also retrieves accurate pricing data by integrating with the AWS Cost and Usage Report, ensuring you get a precise view of your Amazon EKS costs. Learn how to Install Kubecost. See the Kubecost AWS Marketplace page for information on getting a free Kubecost subscription.

---

## Amazon EKS cluster lifecycle and configuration

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/clusters.html

### Lifecycle
- [Create an Amazon EKS Auto Mode cluster](https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started.html)
- [Create an Amazon EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)
- [Update existing cluster to new Kubernetes version](https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)
- [Prepare for Kubernetes version upgrades](https://docs.aws.amazon.com/eks/latest/userguide/cluster-insights.html)

### Networking
- [Cluster API server endpoint](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)
- [Network requirements for VPC and subnets](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html)

### Security/IAM
- [Cluster access control](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)
- [Grant IAM users and roles access to Kubernetes APIs](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)

### Compute
- [Scale cluster compute with Karpenter and Cluster Autoscaler](https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html)
- [Deploy Windows nodes on EKS clusters](https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html)

### Observability
- [Control plane logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
- [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/)

### Cost
- [EKS pricing](https://aws.amazon.com/eks/pricing/)
- [Cost optimization](https://docs.aws.amazon.com/eks/latest/userguide/cost-optimization.html)

---

## Create local Amazon EKS clusters on AWS Outposts for high availability

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-local-cluster-overview.html

**Contents:**
- Create local Amazon EKS clusters on AWS Outposts for high availability
- Supported AWS Regions
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use local clusters to run your entire Amazon EKS cluster locally on AWS Outposts. This helps mitigate the risk of application downtime that might result from temporary network disconnects to the cloud. These disconnects can be caused by fiber cuts or weather events. Because the entire Kubernetes cluster runs locally on Outposts, applications remain available. You can perform cluster operations during network disconnects to the cloud. For more information, see Prepare local Amazon EKS clusters on AWS Outposts for network disconnects. The following diagram shows a local cluster deployment.

Local clusters are generally available for use with Outposts racks.

You can create local clusters in the following AWS Regions: US East (Ohio), US East (N. Virginia), US West (N. California), US West (Oregon), Asia Pacific (Seoul), Asia Pacific (Singapore), Asia Pacific (Sydney), Asia Pacific (Tokyo), Canada (Central), Europe (Frankfurt), Europe (Ireland), Europe (London), Middle East (Bahrain), and South America (São Paulo). For detailed information about supported features, see Comparing the deployment options.

---

## Prepare cluster access for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-prep.html

**Contents:**
- Prepare cluster access for hybrid nodes
- Using Amazon EKS access entries for Hybrid Nodes IAM role
  - AWS CLI
  - AWS Management Console
- Using aws-auth ConfigMap for Hybrid Nodes IAM role

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Before connecting hybrid nodes to your Amazon EKS cluster, you must enable your Hybrid Nodes IAM Role with Kubernetes permissions to join the cluster. See Prepare credentials for hybrid nodes for information on how to create the Hybrid Nodes IAM role. Amazon EKS supports two ways to associate IAM principals with Kubernetes Role-Based Access Control (RBAC), Amazon EKS access entries and the aws-auth ConfigMap. For more information on Amazon EKS access management, see Grant IAM users and roles access to Kubernetes APIs.

Use the procedures below to associate your Hybrid Nodes IAM role with Kubernetes permissions. To use Amazon EKS access entries, your cluster must have been created with the API or API_AND_CONFIG_MAP authentication modes. To use the aws-auth ConfigMap, your cluster must have been created with the API_AND_CONFIG_MAP authentication mode. The CONFIG_MAP-only authentication mode is not supported for hybrid nodes-enabled Amazon EKS clusters.

There is an Amazon EKS access entry type for hybrid nodes named HYBRID_LINUX that can be used with an IAM role. With this access entry type, the username is automatically set to system:node:{{SessionName}}. For more information on creating access entries, see Create access entries.

You must have the latest version of the AWS CLI installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide.

Create your access entry with the following command. Replace CLUSTER_NAME with the name of your cluster and HYBRID_NODES_ROLE_ARN with the ARN of the role you created in the steps for Prepare credentials for hybrid nodes.

Open the Amazon EKS console at Amazon EKS console.

Choose the name of your hybrid nodes-enabled cluster.

Choose the Access tab.

Choose Create access entry.

For IAM principal, select the Hybrid Nodes IAM role you created in the steps for Prepare credentials for hybrid nodes.

For Type, select Hybrid Linux.

(Optional) For Tags, assign labels to the access entry. For example, to make it easier to find all resources with the same tag.

Choose Skip to review and create. Y

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
aws --version
```

Example 4 (unknown):
```unknown
aws eks create-access-entry --cluster-name CLUSTER_NAME \
    --principal-arn HYBRID_NODES_ROLE_ARN \
    --type HYBRID_LINUX
```

---

## Troubleshoot problems with Amazon EKS clusters and nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html#access-denied-managed-node-groups

**Contents:**
- Troubleshoot problems with Amazon EKS clusters and nodes
- Insufficient capacity
- Nodes fail to join cluster
- Unauthorized or access denied (kubectl)
- hostname doesn’t match
- getsockopt: no route to host
- Instances failed to join the Kubernetes cluster
- Managed node group error codes
- Not authorized for images
- Node is in NotReady state

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them. If you need to troubleshoot specific Amazon EKS areas, see the separate Troubleshooting IAM, Troubleshoot Amazon EKS Connector issues, and Troubleshooting for ADOT using EKS Add-Ons topics.

For other troubleshooting information, see Knowledge Center content about Amazon Elastic Kubernetes Service on AWS re:Post.

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified doesn’t have sufficient capacity to support a cluster.

Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message.

There are Availability Zones that a cluster can’t reside in. Compare the Availability Zones that your subnets are in with the list of Availability Zones in the Subnet requirements and considerations.

There are a few common reasons that prevent nodes from joining the cluster:

If the nodes are managed nodes, Amazon EKS adds entries to the aws-auth ConfigMap when you create the node group. If the entry was removed or modified, then you need to re-add it. For more information, enter eksctl create iamidentitymapping --help in your terminal. You can view your current aws-auth ConfigMap entries by replacing my-cluster in the following command with the name of your cluster and then running the modified command: eksctl get iamidentitymapping --cluster my-cluster . The ARN of the role that you specify can’t include a path other than /. For example, if the name of your role is development/apps/my-role, you’d need to change it to my-role when specifying the ARN for the role. Make sure that you specify the node IAM role ARN (not the instance profile ARN).

If the nodes are self-managed, and you haven’t created access entries for the ARN of the node’s IAM role, then run the same commands listed for managed nodes. If you have created an access entry for the ARN for your node IAM role, then it might not be configured properly in the access entry. Make s

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c
```

Example 2 (unknown):
```unknown
eksctl create iamidentitymapping --help
```

Example 3 (unknown):
```unknown
eksctl get iamidentitymapping --cluster my-cluster
```

Example 4 (unknown):
```unknown
development/apps/my-role
```

---

## Create an Amazon EKS cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html#step2-eksctl

**Contents:**
- Create an Amazon EKS cluster
        - Note
- Prerequisites
- Step 1: Create cluster IAM role
  - Service Linked Role
- Step 2: Create cluster
  - Create cluster - eksctl
    - Optional Settings
  - Create cluster - AWS console
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers creating EKS clusters without EKS Auto Mode.

For detailed instructions on creating an EKS Auto Mode cluster, see Create an Amazon EKS Auto Mode cluster.

To get started with EKS Auto Mode, see Get started with Amazon EKS – EKS Auto Mode.

This topic provides an overview of the available options and describes what to consider when you create an Amazon EKS cluster. If you need to create a cluster with your on-premises infrastructure as the compute for nodes, see Create an Amazon EKS cluster with hybrid nodes. If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our guides in Get started with Amazon EKS. These guides help you to create a simple, default cluster without expanding into all of the available options.

An existing VPC and subnets that meet Amazon EKS requirements. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements. If you don’t have a VPC and subnets, you can create them using an Amazon EKS provided AWS CloudFormation template.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

An IAM principal with permissions to create and describe an Amazon EKS cluster. For more information, see Create a local Kubernetes cluster on an Outpost and List or describe all clusters.

If you already have a cluster IAM role, or you're going to create your cluster with eksctl, you can skip the IAM role creation step. See also: [Create cluster IAM role](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html), [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), [Allowing users to access your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html), and [Launching Amazon EKS nodes](https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html).

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 3 (unknown):
```unknown
eks-cluster-role-trust-policy.json
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-encryptionConfig

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-computeConfig

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-connectorConfig

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## ClusterIssue

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ClusterIssue.html#AmazonEKS-Type-ClusterIssue-code

**Contents:**
- ClusterIssue
- Contents
- See Also

An issue with your Amazon EKS cluster.

The error code of the issue.

Valid Values: AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other

A description of the issue.

The resource IDs that the issue relates to.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
AccessDenied | ClusterUnreachable | ConfigurationConflict | InternalFailure | ResourceLimitExceeded | ResourceNotFound | IamRoleNotFound | VpcNotFound | InsufficientFreeAddresses | Ec2ServiceNotSubscribed | Ec2SubnetNotFound | Ec2SecurityGroupNotFound | KmsGrantRevoked | KmsKeyNotFound | KmsKeyMarkedForDeletion | KmsKeyDisabled | StsRegionalEndpointDisabled | UnsupportedVersion | Other
```

---

## Create an Amazon EKS cluster with hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cluster-create.html#hybrid-nodes-cluster-create-eksctl

**Contents:**
- Create an Amazon EKS cluster with hybrid nodes
- Prerequisites
- Considerations
- Step 1: Create cluster IAM role
- Step 2: Create hybrid nodes-enabled cluster
  - Create hybrid nodes-enabled cluster - eksctl
  - Create hybrid nodes-enabled cluster - AWS CloudFormation
  - Create hybrid nodes-enabled cluster - AWS CLI
  - Create hybrid nodes-enabled cluster - AWS Management Console
- Step 3: Update kubeconfig

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the available options and describes what to consider when you create a hybrid nodes-enabled Amazon EKS cluster. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes, including standard and extended support.

If you are not planning to use EKS Hybrid Nodes, see the primary Amazon EKS create cluster documentation at Create an Amazon EKS cluster.

The Prerequisite setup for hybrid nodes completed. Before you create your hybrid nodes-enabled cluster, you must have your on-premises node and optionally pod CIDRs identified, your VPC and subnets created according to the EKS requirements, and hybrid nodes requirements, and your security group with inbound rules for your on-premises and optionally pod CIDRs. For more information on these prerequisites, see Prepare networking for hybrid nodes.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing or updating to the last version of the AWS CLI and Configuring settings for the AWS CLI in the AWS Command Line Interface User Guide.

An IAM principal with permissions to create IAM roles and attach policies, and create and describe EKS clusters

Your cluster must use either API or API_AND_CONFIG_MAP for the cluster authentication mode.

Your cluster must use IPv4 address family.

Your cluster must use either Public or Private cluster endpoint connectivity. Your cluster cannot use “Public and Private” cluster endpoint connectivity, because the Amazon EKS Kubernetes API server endpoint will resolve to the public IPs for hybrid nodes running outside of your VPC.

OIDC authentication is supported for EKS clusters with hybrid nodes.

You can add, change, or remove the hybrid nodes configuration of an existing cluster. For more information, see Enable hybrid nodes on an existing Amazon EKS cluster or modify configuration.

If you already have a cluster IAM role, or you’re going to create your cluster with eksctl or AWS CloudFormation, then you can skip this step. By default, eksctl and the AWS CloudFormation template create the cluste

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-response-cluster

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-deletionProtection

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Create an EKS Auto Mode Cluster with the AWS CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-cli.html

**Contents:**
- Create an EKS Auto Mode Cluster with the AWS CLI
- Prerequisites
- Specify VPC subnets
- IAM Roles for EKS Auto Mode Clusters
  - Cluster IAM Role
  - Node IAM Role
- Create an EKS Auto Mode Cluster IAM Role
  - Step 1: Create the Trust Policy
  - Step 2: Create the IAM Role
  - Step 3: Note the Role ARN

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

EKS Auto Mode Clusters automate routine cluster management tasks for compute, storage, and networking. For example, EKS Auto Mode Clusters automatically detect when additional nodes are required and provision new EC2 instances to meet workload demands.

This topic guides you through creating a new EKS Auto Mode Cluster using the AWS CLI and optionally deploying a sample workload.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide.

Login to the CLI with sufficent IAM permissions to create AWS resources including IAM Policies, IAM Roles, and EKS Clusters.

The kubectl command line tool installed on your device. AWS suggests you use the same kubectl version as the Kubernetes version of your EKS Cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Amazon EKS Auto Mode deploy nodes to VPC subnets. When creating an EKS cluster, you must specify the VPC subnets where the nodes will be deployed. You can use the default VPC subnets in your AWS account or create a dedicated VPC for critical workloads.

AWS suggests creating a dedicated VPC for your cluster. Learn how to Create an Amazon VPC for your Amazon EKS cluster.

The EKS Console assists with creating a new VPC. Learn how to Create an EKS Auto Mode Cluster with the AWS Management Console.

Alternatively, you can use the default VPC of your AWS account. Use the following instructions to find the Subnet IDs.

Run the following command to list the default VPC and its subnets:

Save the output and note the Subnet IDs.

EKS Auto Mode requires a Cluster IAM Role to perform actions in your AWS account, such as provisioning new EC2 instances. You must create this role to grant EKS the necessary permissions. AWS recommends attaching the following AWS managed policies to the Cluster IAM Role:

AmazonEKSComputePolicy

AmazonEKSBlockStoragePolicy

AmazonEKSLoadBalancingPolicy

AmazonEKSNetworkingPolicy

AmazonEKSClusterPolicy

When you create an EKS Auto Mode cluster, you specify a Node IAM Role. When EKS Auto Mode creates nodes to process pending workloads, each new EC2 instance node is assigned the Node IAM Role. This ro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version
```

Example 2 (unknown):
```unknown
trust-policy.json
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ]
    }
  ]
}
```

Example 4 (unknown):
```unknown
aws iam attach-role-policy \
    --role-name AmazonEKSAutoClusterRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#policy-create-cluster

**Contents:**
- Amazon EKS identity-based policy examples
        - Topics
- Policy best practices
- Using the Amazon EKS console
        - Important
- Allow IAM users to view their own permissions
- Create a Kubernetes cluster on the AWS Cloud
- Create a local Kubernetes cluster on an Outpost
- Update a Kubernetes cluster
- List or describe all clusters

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

By default, IAM users and roles don’t have permission to create or modify Amazon EKS resources. They also can’t perform tasks using the AWS Management Console, AWS CLI, or AWS API. An IAM administrator must create IAM policies that grant users and roles permission to perform specific API operations on the specified resources they need. The administrator must then attach those policies to the IAM users or groups that require those permissions.

To learn how to create an IAM identity-based policy using these example JSON policy documents, see Creating policies on the JSON tab in the IAM User Guide.

When you create an Amazon EKS cluster, the IAM principal that creates the cluster is automatically granted system:masters permissions in the cluster’s role-based access control (RBAC) configuration in the Amazon EKS control plane. This principal doesn’t appear in any visible configuration, so make sure to keep track of which principal originally created the cluster. To grant additional IAM principals the ability to interact with your cluster, edit the aws-auth ConfigMap within Kubernetes and create a Kubernetes rolebinding or clusterrolebinding with the name of a group that you specify in the aws-auth ConfigMap.

For more information about working with the ConfigMap, see Grant IAM users and roles access to Kubernetes APIs.

Policy best practices

Using the Amazon EKS console

Allow IAM users to view their own permissions

Create a Kubernetes cluster on the AWS Cloud

Create a local Kubernetes cluster on an Outpost

Update a Kubernetes cluster

List or describe all clusters

Identity-based policies determine whether someone can create, access, or delete Amazon EKS resources in your account. These actions can incur costs for your AWS account. When you create or edit identity-based policies, follow these guidelines and recommendations:

Get started with AWS managed policies and move toward least-privilege permissions – To get started granting permissions to your users and workloads, use the AWS managed policies that grant permissions for many common use cases. They are available in your AWS account. We recommend that you reduce permissions further by defining AWS customer managed policies that are specific to your use cases. For more information, see AWS managed policies or AWS managed policies for job functions in the 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
system:masters
```

Example 2 (unknown):
```unknown
aws-auth ConfigMap
```

Example 3 (unknown):
```unknown
rolebinding
```

Example 4 (unknown):
```unknown
clusterrolebinding
```

---

## Upgrade hybrid nodes for your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-upgrade.html

**Contents:**
- Upgrade hybrid nodes for your cluster
        - Important
- Prerequisites
- Cutover migration (blue-green) upgrades
- In-place upgrades

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The guidance for upgrading hybrid nodes is similar to self-managed Amazon EKS nodes that run in Amazon EC2. We recommend that you create new hybrid nodes on your target Kubernetes version, gracefully migrate your existing applications to the hybrid nodes on the new Kubernetes version, and remove the hybrid nodes on the old Kubernetes version from your cluster. Be sure to review the Amazon EKS Best Practices for upgrades before initiating an upgrade. Amazon EKS Hybrid Nodes have the same Kubernetes version support for Amazon EKS clusters with cloud nodes, including standard and extended support.

Amazon EKS Hybrid Nodes follow the same version skew policy for nodes as upstream Kubernetes. Amazon EKS Hybrid Nodes cannot be on a newer version than the Amazon EKS control plane, and hybrid nodes may be up to three Kubernetes minor versions older than the Amazon EKS control plane minor version.

If you do not have spare capacity to create new hybrid nodes on your target Kubernetes version for a cutover migration upgrade strategy, you can alternatively use the Amazon EKS Hybrid Nodes CLI (nodeadm) to upgrade the Kubernetes version of your hybrid nodes in-place.

If you are upgrading your hybrid nodes in-place with nodeadm, there is downtime for the node during the process where the older version of the Kubernetes components are shut down and the new Kubernetes version components are installed and started.

Before upgrading, make sure you have completed the following prerequisites.

The target Kubernetes version for your hybrid nodes upgrade must be equal to or less than the Amazon EKS control plane version.

If you are following a cutover migration upgrade strategy, the new hybrid nodes you are installing on your target Kubernetes version must meet the Prerequisite setup for hybrid nodes requirements. This includes having IP addresses within the Remote Node Network CIDR you passed during Amazon EKS cluster creation.

For both cutover migration and in-place upgrades, the hybrid nodes must have access to the required domains to pull the new versions of the hybrid nodes dependencies.

You must have kubectl installed on your local machine or instance you are using to interact with your Amazon EKS Kubernetes API endpoint.

The version of your CNI must support the Kubernetes version you are upgrading to. If it does not, up

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
nodeadm install
```

Example 2 (unknown):
```unknown
kubectl cordon NODE_NAME
```

Example 3 (unknown):
```unknown
K8S_VERSION=1.28
for node in $(kubectl get nodes -o json | jq --arg K8S_VERSION "$K8S_VERSION" -r '.items[] | select(.status.nodeInfo.kubeletVersion | match("\($K8S_VERSION)")).metadata.name')
do
    echo "Cordoning $node"
    kubectl cordon $node
done
```

Example 4 (unknown):
```unknown
kubectl scale deployments/coredns --replicas=2 -n kube-system
```

---

## Deploy private clusters with limited internet access

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html

**Contents:**
- Deploy private clusters with limited internet access
- Cluster architecture requirements
- Node requirements
        - Note
- Pod requirements

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how to deploy an Amazon EKS cluster that is deployed on the AWS Cloud, but doesn’t have outbound internet access. If you have a local cluster on AWS Outposts, see Create Amazon Linux nodes on AWS Outposts, instead of this topic.

If you’re not familiar with Amazon EKS networking, see De-mystifying cluster networking for Amazon EKS worker nodes. If your cluster doesn’t have outbound internet access, then it must meet the following requirements:

Your cluster must pull images from a container registry that’s in your VPC. You can create an Amazon Elastic Container Registry in your VPC and copy container images to it for your nodes to pull from. For more information, see Copy a container image from one repository to another repository.

Your cluster must have endpoint private access enabled. This is required for nodes to register with the cluster endpoint. Endpoint public access is optional. For more information, see Cluster API server endpoint.

Self-managed Linux and Windows nodes must include the following bootstrap arguments before they’re launched. These arguments bypass Amazon EKS introspection and don’t require access to the Amazon EKS API from within the VPC.

Determine the value of your cluster’s endpoint with the following command. Replace my-cluster with the name of your cluster.

An example output is as follows.

Determine the value of your cluster’s certificate authority with the following command. Replace my-cluster with the name of your cluster.

The returned output is a long string.

Replace cluster-endpoint and certificate-authority in the following commands with the values returned in the output from the previous commands. For more information about specifying bootstrap arguments when launching self-managed nodes, see Create self-managed Amazon Linux nodes and Create self-managed Microsoft Windows nodes.

For additional arguments, see the bootstrap script on GitHub.

If you’re using custom service CIDR, then you need to specify it using the -ServiceCIDR parameter. Otherwise, the DNS resolution for Pods in the cluster will fail.

For additional arguments, see Bootstrap script configuration parameters.

Your cluster’s aws-auth ConfigMap must be created from within your VPC. For more information about creating and adding entries to the aws-auth ConfigMap, enter eksctl create iam

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws eks describe-cluster --name my-cluster --query cluster.endpoint --output text
```

Example 2 (unknown):
```unknown
https://EXAMPLE108C897D9B2F1B21D5EXAMPLE.sk1.region-code.eks.amazonaws.com
```

Example 3 (unknown):
```unknown
aws eks describe-cluster --name my-cluster --query cluster.certificateAuthority --output text
```

Example 4 (unknown):
```unknown
cluster-endpoint
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-roleArn

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-certificateAuthority

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Encrypt Kubernetes secrets with KMS on existing clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/enable-kms.html

**Contents:**
- Encrypt Kubernetes secrets with KMS on existing clusters
        - Important
        - Warning
        - Note
        - Warning
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This procedure only applies to EKS clusters running Kubernetes version 1.27 or lower. If you are running Kubernetes version 1.28 or higher, your Kubernetes secrets are protected with envelope encryption by default. For more information, see Default envelope encryption for all Kubernetes API Data.

If you enable secrets encryption, the Kubernetes secrets are encrypted using the AWS KMS key that you select. The KMS key must meet the following conditions:

Can encrypt and decrypt data

Created in the same AWS Region as the cluster

If the KMS key was created in a different account, the IAM principal must have access to the KMS key.

For more information, see Allowing IAM principals in other accounts to use a KMS key in the AWS Key Management Service Developer Guide .

You can’t disable secrets encryption after enabling it. This action is irreversible.

This procedure only applies to EKS clusters running Kubernetes version 1.27 or lower. For more information, see Default envelope encryption for all Kubernetes API Data.

You can enable encryption in two ways:

Add encryption to your cluster with a single command.

To automatically re-encrypt your secrets, run the following command.

To opt-out of automatically re-encrypting your secrets, run the following command.

Add encryption to your cluster with a kms-cluster.yaml file.

To have your secrets re-encrypt automatically, run the following command.

To opt out of automatically re-encrypting your secrets, run the following command.

This procedure only applies to EKS clusters running Kubernetes version 1.27 or lower. For more information, see Default envelope encryption for all Kubernetes API Data.

Open the Amazon EKS console.

Choose the cluster that you want to add KMS encryption to.

Choose the Overview tab (this is selected by default).

Scroll down to the Secrets encryption section and choose Enable.

Select a key from the dropdown list and choose the Enable button. If no keys are listed, you must create one first. For more information, see Creating keys

Choose the Confirm button to use the chosen key.

This procedure only applies to EKS clusters running Kubernetes version 1.27 or lower. For more information, see Default envelope encryption for all Kubernetes API Data.

Associate the secrets encryption configuration with your cluster using the following AWS C

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl utils enable-secrets-encryption \
    --cluster my-cluster \
    --key-arn arn:aws:kms:region-code:account:key/key
```

Example 2 (unknown):
```unknown
eksctl utils enable-secrets-encryption
    --cluster my-cluster \
    --key-arn arn:aws:kms:region-code:account:key/key \
    --encrypt-existing-secrets=false
```

Example 3 (unknown):
```unknown
kms-cluster.yaml
```

Example 4 (unknown):
```unknown
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: my-cluster
  region: region-code

secretsEncryption:
  keyARN: arn:aws:kms:region-code:account:key/key
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-clientRequestToken

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-arn

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Manage CoreDNS for DNS in Amazon EKS clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/managing-coredns.html

**Contents:**
- Manage CoreDNS for DNS in Amazon EKS clusters
        - Tip
- CoreDNS versions
        - Important
- Important CoreDNS upgrade considerations
  - CoreDNS v1.11 upgrade considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

With Amazon EKS Auto Mode, you don’t need to install or upgrade networking add-ons. Auto Mode includes pod networking and load balancing capabilities.

For more information, see Automate cluster infrastructure with EKS Auto Mode.

CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster. The CoreDNS Pods provide name resolution for all Pods in the cluster. The CoreDNS Pods can be deployed to Fargate nodes if your cluster includes a Fargate Profile with a namespace that matches the namespace for the CoreDNS deployment. For more information about CoreDNS, see Using CoreDNS for Service Discovery in the Kubernetes documentation.

The following table lists the latest version of the Amazon EKS add-on type for each Kubernetes version.

If you’re self-managing this add-on, the versions in the table might not be the same as the available self-managed versions. For more information about updating the self-managed type of this add-on, see Update the CoreDNS Amazon EKS self-managed add-on.

CoreDNS updates utilize a PodDisruptionBudget to help maintain DNS service availability during the update process.

To improve the stability and availability of the CoreDNS Deployment, versions v1.9.3-eksbuild.6 and later and v1.10.1-eksbuild.3 are deployed with a PodDisruptionBudget. If you’ve deployed an existing PodDisruptionBudget, your upgrade to these versions might fail. If the upgrade fails, completing one of the following tasks should resolve the issue:

When doing the upgrade of the Amazon EKS add-on, choose to override the existing settings as your conflict resolution option. If you’ve made other custom settings to the Deployment, make sure to back up your settings before upgrading so that you can reapply your other custom settings after the upgrade.

Remove your existing PodDisruptionBudget and try the upgrade again.

In EKS add-on versions v1.9.3-eksbuild.3 and later and v1.10.1-eksbuild.6 and later, the CoreDNS Deployment sets the readinessProbe to use the /ready endpoint. This endpoint is enabled in the Corefile configuration file for CoreDNS.

If you use a custom Corefile, you must add the ready plugin to the 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
v1.9.3-eksbuild.6
```

Example 2 (unknown):
```unknown
v1.10.1-eksbuild.3
```

Example 3 (unknown):
```unknown
PodDisruptionBudget
```

Example 4 (unknown):
```unknown
PodDisruptionBudget
```

---

## Create a VPC and subnets for Amazon EKS clusters on AWS Outposts

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-vpc-subnet-requirements.html

**Contents:**
- Create a VPC and subnets for Amazon EKS clusters on AWS Outposts
- VPC requirements and considerations
- Subnet requirements and considerations
- Subnet access to AWS services
  - Using a NAT gateway
  - Using interface VPC endpoints
- Create a VPC

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you create a local cluster, you specify a VPC and at least one private subnet that runs on Outposts. This topic provides an overview of the VPC and subnets requirements and considerations for your local cluster.

When you create a local cluster, the VPC that you specify must meet the following requirements and considerations:

Make sure that the VPC has enough IP addresses for the local cluster, any nodes, and other Kubernetes resources that you want to create. If the VPC that you want to use doesn’t have enough IP addresses, increase the number of available IP addresses. You can do this by associating additional Classless Inter-Domain Routing (CIDR) blocks with your VPC. You can associate private (RFC 1918) and public (non-RFC 1918) CIDR blocks to your VPC either before or after you create your cluster. It can take a cluster up to 5 hours for a CIDR block that you associated with a VPC to be recognized.

The VPC can’t have assigned IP prefixes or IPv6 CIDR blocks. Because of these constraints, the information that’s covered in Assign more IP addresses to Amazon EKS nodes with prefixes and Learn about IPv6 addresses to clusters, Pods, and services isn’t applicable to your VPC.

The VPC has a DNS hostname and DNS resolution enabled. Without these features, the local cluster fails to create, and you need to enable the features and recreate your cluster. For more information, see DNS attributes for your VPC in the Amazon VPC User Guide.

To access your local cluster over your local network, the VPC must be associated with your Outpost’s local gateway route table. For more information, see VPC associations in the AWS Outposts User Guide.

When you create the cluster, specify at least one private subnet. If you specify more than one subnet, the Kubernetes control plane instances are evenly distributed across the subnets. If more than one subnet is specified, the subnets must exist on the same Outpost. Moreover, the subnets must also have proper routes and security group permissions to communicate with each other. When you create a local cluster, the subnets that you specify must meet the following requirements:

The subnets are all on the same logical Outpost.

The subnets together have at least three available IP addresses for the Kubernetes control plane instances. If three subnets are specified, each subnet

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
com.amazonaws.region-code.ssm
```

Example 2 (unknown):
```unknown
region-code
```

Example 3 (unknown):
```unknown
com.amazonaws.region-code.ssmmessages
```

Example 4 (unknown):
```unknown
region-code
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-bootstrapSelfManagedAddons

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-tags

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Scale cluster compute with Karpenter and Cluster Autoscaler

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html

**Contents:**
- Scale cluster compute with Karpenter and Cluster Autoscaler
- EKS Auto Mode
- Additional Solutions
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Autoscaling is a function that automatically scales your resources out and in to meet changing demands. This is a major Kubernetes function that would otherwise require extensive human resources to perform manually.

Amazon EKS Auto Mode automatically scales cluster compute resources. If a pod can’t fit onto existing nodes, EKS Auto Mode creates a new one. EKS Auto Mode also consolidates workloads and deletes nodes. EKS Auto Mode builds upon Karpenter.

For more information, see:

Automate cluster infrastructure with EKS Auto Mode

Create a Node Pool for EKS Auto Mode

Deploy a sample inflate workload to an Amazon EKS Auto Mode cluster

Amazon EKS supports two additional autoscaling products:

Karpenter is a flexible, high-performance Kubernetes cluster autoscaler that helps improve application availability and cluster efficiency. Karpenter launches right-sized compute resources (for example, Amazon EC2 instances) in response to changing application load in under a minute. Through integrating Kubernetes with AWS, Karpenter can provision just-in-time compute resources that precisely meet the requirements of your workload. Karpenter automatically provisions new compute resources based on the specific requirements of cluster workloads. These include compute, storage, acceleration, and scheduling requirements. Amazon EKS supports clusters using Karpenter, although Karpenter works with any conformant Kubernetes cluster. For more information, see the Karpenter documentation.

Karpenter is open-source software which AWS customers are responsible for installing, configuring, and managing in their Kubernetes clusters. AWS provides technical support when Karpenter is run unmodified using a compatible version in Amazon EKS clusters. It is essential that customers maintain the availability and security of the Karpenter controller as well as appropriate testing procedures when upgrading it or the Kubernetes cluster in which it’s running, just like any other customer-managed software. There is no AWS Service Level Agreement (SLA) for Karpenter and customers are responsible for ensuring that the EC2 instances launched by Karpenter meet their business requirements.

The Kubernetes Cluster Autoscaler automatically adjusts the number of nodes in your cluster when pods fail or are rescheduled onto other nodes. The Cluster Autosc

*[Content truncated]*

---

## Connect kubectl to an EKS cluster by creating a kubeconfig file

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html

**Contents:**
- Connect kubectl to an EKS cluster by creating a kubeconfig file
- Create kubeconfig file automatically

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

In this topic, you create a kubeconfig file for your cluster (or update an existing one).

The kubectl command-line tool uses configuration information in kubeconfig files to communicate with the API server of a cluster. For more information, see Organizing Cluster Access Using kubeconfig Files in the Kubernetes documentation.

Amazon EKS uses the aws eks get-token command with kubectl for cluster authentication. By default, the AWS CLI uses the same credentials that are returned with the following command:

An existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. For example, if your cluster version is 1.29, you can use kubectl version 1.28, 1.29, or 1.30 with it. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

An IAM user or role with permission to use the eks:DescribeCluster API action for the cluster that you specify. For more information, see Amazon EKS identity-based policy examples. If you use an identity from your own OpenID Connect provider to access your cluster, then see Using kubectl in the Kubernetes documentation to create or update your kube config file.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws eks get-token
```

Example 2 (unknown):
```unknown
aws sts get-caller-identity
```

Example 3 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 4 (unknown):
```unknown
eks:DescribeCluster
```

---

## Create an Amazon EKS cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html#step3

**Contents:**
- Create an Amazon EKS cluster
        - Note
- Prerequisites
- Step 1: Create cluster IAM role
  - Service Linked Role
- Step 2: Create cluster
  - Create cluster - eksctl
    - Optional Settings
  - Create cluster - AWS console
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers creating EKS clusters without EKS Auto Mode.

For detailed instructions on creating an EKS Auto Mode cluster, see Create an Amazon EKS Auto Mode cluster.

To get started with EKS Auto Mode, see Get started with Amazon EKS – EKS Auto Mode.

This topic provides an overview of the available options and describes what to consider when you create an Amazon EKS cluster. If you need to create a cluster with your on-premises infrastructure as the compute for nodes, see Create an Amazon EKS cluster with hybrid nodes. If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our guides in Get started with Amazon EKS. These guides help you to create a simple, default cluster without expanding into all of the available options.

An existing VPC and subnets that meet Amazon EKS requirements. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements. If you don’t have a VPC and subnets, you can create them using an Amazon EKS provided AWS CloudFormation template.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

An IAM principal with permissions to create and describe an Amazon EKS cluster. For more information, see Create a local Kubernetes cluster on an Outpost and List or describe all clusters.

If you already have a cluster IAM role, or you're going to create your cluster with eksctl, you can skip the IAM role creation step. See also: [Create cluster IAM role](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html), [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), [Allowing users to access your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html), and [Launching Amazon EKS nodes](https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html).

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 3 (unknown):
```unknown
eks-cluster-role-trust-policy.json
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## Create an Amazon EKS cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html#step2-console

**Contents:**
- Create an Amazon EKS cluster
        - Note
- Prerequisites
- Step 1: Create cluster IAM role
  - Service Linked Role
- Step 2: Create cluster
  - Create cluster - eksctl
    - Optional Settings
  - Create cluster - AWS console
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers creating EKS clusters without EKS Auto Mode.

For detailed instructions on creating an EKS Auto Mode cluster, see Create an Amazon EKS Auto Mode cluster.

To get started with EKS Auto Mode, see Get started with Amazon EKS – EKS Auto Mode.

This topic provides an overview of the available options and describes what to consider when you create an Amazon EKS cluster. If you need to create a cluster with your on-premises infrastructure as the compute for nodes, see Create an Amazon EKS cluster with hybrid nodes. If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our guides in Get started with Amazon EKS. These guides help you to create a simple, default cluster without expanding into all of the available options.

An existing VPC and subnets that meet Amazon EKS requirements. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements. If you don’t have a VPC and subnets, you can create them using an Amazon EKS provided AWS CloudFormation template.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. To install or upgrade kubectl, see Set up kubectl and eksctl.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

An IAM principal with permissions to create and describe an Amazon EKS cluster. For more information, see Create a local Kubernetes cluster on an Outpost and List or describe all clusters.

If you already have a cluster IAM role, or you're going to create your cluster with eksctl, you can skip the IAM role creation step. See also: [Create cluster IAM role](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html), [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), [Allowing users to access your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html), and [Launching Amazon EKS nodes](https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html).

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example 3 (unknown):
```unknown
eks-cluster-role-trust-policy.json
```

Example 4 (unknown):
```unknown
iam:CreateRole
```

---

## Troubleshoot problems with Amazon EKS clusters and nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html#ice

**Contents:**
- Troubleshoot problems with Amazon EKS clusters and nodes
- Insufficient capacity
- Nodes fail to join cluster
- Unauthorized or access denied (kubectl)
- hostname doesn’t match
- getsockopt: no route to host
- Instances failed to join the Kubernetes cluster
- Managed node group error codes
- Not authorized for images
- Node is in NotReady state

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them. If you need to troubleshoot specific Amazon EKS areas, see the separate Troubleshooting IAM, Troubleshoot Amazon EKS Connector issues, and Troubleshooting for ADOT using EKS Add-Ons topics.

For other troubleshooting information, see Knowledge Center content about Amazon Elastic Kubernetes Service on AWS re:Post.

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified doesn’t have sufficient capacity to support a cluster.

Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message.

There are Availability Zones that a cluster can’t reside in. Compare the Availability Zones that your subnets are in with the list of Availability Zones in the Subnet requirements and considerations.

There are a few common reasons that prevent nodes from joining the cluster:

If the nodes are managed nodes, Amazon EKS adds entries to the aws-auth ConfigMap when you create the node group. If the entry was removed or modified, then you need to re-add it. For more information, enter eksctl create iamidentitymapping --help in your terminal. You can view your current aws-auth ConfigMap entries by replacing my-cluster in the following command with the name of your cluster and then running the modified command: eksctl get iamidentitymapping --cluster my-cluster . The ARN of the role that you specify can’t include a path other than /. For example, if the name of your role is development/apps/my-role, you’d need to change it to my-role when specifying the ARN for the role. Make sure that you specify the node IAM role ARN (not the instance profile ARN).

If the nodes are self-managed, and you haven’t created access entries for the ARN of the node’s IAM role, then run the same commands listed for managed nodes. If you have created an access entry for the ARN for your node IAM role, then it might not be configured properly in the access entry. Make s

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c
```

Example 2 (unknown):
```unknown
eksctl create iamidentitymapping --help
```

Example 3 (unknown):
```unknown
eksctl get iamidentitymapping --cluster my-cluster
```

Example 4 (unknown):
```unknown
development/apps/my-role
```

---

## View Amazon EKS security group requirements for clusters

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html

**Contents:**
- View Amazon EKS security group requirements for clusters
- Default cluster security group
        - Important
- Restricting cluster traffic
- Shared security groups
  - Considerations for Amazon EKS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes the security group requirements of an Amazon EKS cluster.

When you create a cluster, Amazon EKS creates a security group that’s named eks-cluster-sg-my-cluster-uniqueID . This security group has the following default rules:

0.0.0.0/0(IPv4) or ::/0 (IPv6)

Self (for EFA traffic)

The default security group includes an outbound rule that allows Elastic Fabric Adapter (EFA) traffic with the destination of the same security group. This enables EFA traffic within the cluster, which is beneficial for AI/ML and High Performance Computing (HPC) workloads. For more information, see Elastic Fabric Adapter for AI/ML and HPC workloads on Amazon EC2 in the Amazon Elastic Compute Cloud User Guide.

If your cluster doesn’t need the outbound rule, you can remove it. If you remove it, you must still have the minimum rules listed in Restricting cluster traffic. If you remove the inbound rule, Amazon EKS recreates it whenever the cluster is updated.

Amazon EKS adds the following tags to the security group. If you remove the tags, Amazon EKS adds them back to the security group whenever your cluster is updated.

kubernetes.io/cluster/my-cluster

eks-cluster-sg-my-cluster-uniqueid

Amazon EKS automatically associates this security group to the following resources that it also creates:

2–4 elastic network interfaces (referred to for the rest of this document as network interface) that are created when you create your cluster.

Network interfaces of the nodes in any managed node group that you create.

The default rules allow all traffic to flow freely between your cluster and nodes, and allows all outbound traffic to any destination. When you create a cluster, you can (optionally) specify your own security groups. If you do, then Amazon EKS also associates the security groups that you specify to the network interfaces that it creates for your cluster. However, it doesn’t associate them to any node groups that you create.

You can determine the ID of your cluster security group in the AWS Management Console under the cluster’s Networking section. Or, you can do so by running the following AWS CLI command.

If you need to limit the open ports between the cluster and nodes, you can remove the default outbound rule and add the following minimum rules that are required for the cluster. If you remove the default 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueID
```

Example 2 (unknown):
```unknown
kubernetes.io/cluster/my-cluster
```

Example 3 (unknown):
```unknown
aws:eks:cluster-name
```

Example 4 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueid
```

---

## Amazon EKS cluster IAM role

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-iam-role.html#create-service-role

**Contents:**
- Amazon EKS cluster IAM role
        - Note
- Check for an existing cluster role
- Creating the Amazon EKS cluster role

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

An Amazon EKS cluster IAM role is required for each cluster. Kubernetes clusters managed by Amazon EKS use this role to manage nodes and the legacy Cloud Provider uses this role to create load balancers with Elastic Load Balancing for services.

Before you can create Amazon EKS clusters, you must create an IAM role with either of the following IAM policies:

AmazonEKSClusterPolicy

A custom IAM policy. The minimal permissions that follow allows the Kubernetes cluster to manage nodes, but doesn’t allow the legacy Cloud Provider to create load balancers with Elastic Load Balancing. Your custom IAM policy must have at least the following permissions:

Prior to October 3, 2023, AmazonEKSClusterPolicy was required on the IAM role for each cluster.

Prior to April 16, 2020, AmazonEKSServicePolicy and AmazonEKSClusterPolicy was required and the suggested name for the role was eksServiceRole. With the AWSServiceRoleForAmazonEKS service-linked role, the AmazonEKSServicePolicy policy is no longer required for clusters created on or after April 16, 2020.

You can use the following procedure to check and see if your account already has the Amazon EKS cluster role.

Open the IAM console at https://console.aws.amazon.com/iam/.

In the left navigation pane, choose Roles.

Search the list of roles for eksClusterRole. If a role that includes eksClusterRole doesn’t exist, then see Creating the Amazon EKS cluster role to create the role. If a role that includes eksClusterRole does exist, then select the role to view the attached policies.

Ensure that the AmazonEKSClusterPolicy managed policy is attached to the role. If the policy is attached, your Amazon EKS cluster role is properly configured.

Choose Trust relationships, and then choose Edit trust policy.

Verify that the trust relationship contains the following policy. If the trust relationship matches the following policy, choose Cancel. If the trust relationship doesn’t match, copy the policy into the Edit trust policy window and choose Update policy.

You can use the AWS Management Console or the AWS CLI to create the cluster role.

Open the IAM console at https://console.aws.amazon.com/iam/.

Choose Roles, then Create role.

Under Trusted entity type, select AWS service.

From the Use cases for other AWS services dropdown list, choose EKS.

Choose EKS - Cluster for your

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags"
      ],
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "ForAnyValue:StringLike": {
          "aws:TagKeys": "kubernetes.io/cluster/*"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeVpcs",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeInstanceTopology",
        "kms:DescribeKey
...
```

Example 2 (unknown):
```unknown
eksServiceRole
```

Example 3 (unknown):
```unknown
AWSServiceRoleForAmazonEKS
```

Example 4 (unknown):
```unknown
eksClusterRole
```

---

## Update a managed node group for your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/update-managed-node-group.html

**Contents:**
- Update a managed node group for your cluster
- Update a node group version
- eksctl
        - Note
- AWS Management Console
- Edit a node group configuration
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you initiate a managed node group update, Amazon EKS automatically updates your nodes for you, completing the steps listed in Understand each phase of node updates. If you’re using an Amazon EKS optimized AMI, Amazon EKS automatically applies the latest security patches and operating system updates to your nodes as part of the latest AMI release version.

There are several scenarios where it’s useful to update your Amazon EKS managed node group’s version or configuration:

You have updated the Kubernetes version for your Amazon EKS cluster and want to update your nodes to use the same Kubernetes version.

A new AMI release version is available for your managed node group. For more information about AMI versions, see these sections:

Retrieve Amazon Linux AMI version information

Create nodes with optimized Bottlerocket AMIs

Retrieve Windows AMI version information

You want to adjust the minimum, maximum, or desired count of the instances in your managed node group.

You want to add or remove Kubernetes labels from the instances in your managed node group.

You want to add or remove AWS tags from your managed node group.

You need to deploy a new version of a launch template with configuration changes, such as an updated custom AMI.

You have deployed version 1.9.0 or later of the Amazon VPC CNI add-on, enabled the add-on for prefix delegation, and want new AWS Nitro System instances in a node group to support a significantly increased number of Pods. For more information, see Assign more IP addresses to Amazon EKS nodes with prefixes.

You have enabled IP prefix delegation for Windows nodes and want new AWS Nitro System instances in a node group to support a significantly increased number of Pods. For more information, see Assign more IP addresses to Amazon EKS nodes with prefixes.

If there’s a newer AMI release version for your managed node group’s Kubernetes version, you can update your node group’s version to use the newer AMI version. Similarly, if your cluster is running a Kubernetes version that’s newer than your node group, you can update the node group to use the latest AMI release version to match your cluster’s Kubernetes version.

When a node in a managed node group is terminated due to a scaling operation or update, the Pods in that node are drained first. For more information, see Understa

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
example value
```

Example 2 (unknown):
```unknown
eksctl upgrade nodegroup \
  --name=node-group-name \
  --cluster=my-cluster \
  --region=region-code
```

Example 3 (unknown):
```unknown
--launch-template-version version-number
```

Example 4 (unknown):
```unknown
version-number
```

---

## Cluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Cluster.html#AmazonEKS-Type-Cluster-kubernetesNetworkConfig

**Contents:**
- Cluster
- Contents
- See Also

An object representing an Amazon EKS cluster.

The access configuration for the cluster.

Type: AccessConfigResponse object

The Amazon Resource Name (ARN) of the cluster.

The certificate-authority-data for your cluster.

Type: Certificate object

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Type: ComputeConfigResponse object

The configuration used to connect to a cluster for registration.

Type: ConnectorConfigResponse object

The Unix epoch timestamp at object creation.

The current deletion protection setting for the cluster. When true, deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When false, the cluster can be deleted normally. This setting only applies to clusters in an active state.

The encryption configuration for the cluster.

Type: Array of EncryptionConfig objects

Array Members: Maximum number of 1 item.

The endpoint for your Kubernetes API server.

An object representing the health of your Amazon EKS cluster.

Type: ClusterHealth object

The ID of your local Amazon EKS cluster on an AWS Outpost. This property isn't available for an Amazon EKS cluster on the AWS cloud.

The identity provider information for the cluster.

Type: Identity object

The Kubernetes network configuration for the cluster.

Type: KubernetesNetworkConfigResponse object

The logging configuration for your cluster.

The name of your cluster.

An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.

Type: OutpostConfigResponse object

The platform version of your Amazon EKS cluster. For more information about clusters deployed on the AWS Cloud, see Platform versions in the Amazon EKS User Guide . For more information about local clusters deployed on an Outpost, see Amazon EKS local cluster platform versions in the Amazon EKS User Guide .

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

Type: RemoteNetworkConfigResponse object

The VPC configur

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
CREATING | ACTIVE | DELETING | FAILED | UPDATING | PENDING
```

---

## Amazon EKS cluster IAM role

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html

**Contents:**
- Amazon EKS cluster IAM role
        - Note
- Check for an existing cluster role
- Creating the Amazon EKS cluster role

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

An Amazon EKS cluster IAM role is required for each cluster. Kubernetes clusters managed by Amazon EKS use this role to manage nodes and the legacy Cloud Provider uses this role to create load balancers with Elastic Load Balancing for services.

Before you can create Amazon EKS clusters, you must create an IAM role with either of the following IAM policies:

AmazonEKSClusterPolicy

A custom IAM policy. The minimal permissions that follow allows the Kubernetes cluster to manage nodes, but doesn’t allow the legacy Cloud Provider to create load balancers with Elastic Load Balancing. Your custom IAM policy must have at least the following permissions:

Prior to October 3, 2023, AmazonEKSClusterPolicy was required on the IAM role for each cluster.

Prior to April 16, 2020, AmazonEKSServicePolicy and AmazonEKSClusterPolicy was required and the suggested name for the role was eksServiceRole. With the AWSServiceRoleForAmazonEKS service-linked role, the AmazonEKSServicePolicy policy is no longer required for clusters created on or after April 16, 2020.

You can use the following procedure to check and see if your account already has the Amazon EKS cluster role.

Open the IAM console at https://console.aws.amazon.com/iam/.

In the left navigation pane, choose Roles.

Search the list of roles for eksClusterRole. If a role that includes eksClusterRole doesn’t exist, then see Creating the Amazon EKS cluster role to create the role. If a role that includes eksClusterRole does exist, then select the role to view the attached policies.

Ensure that the AmazonEKSClusterPolicy managed policy is attached to the role. If the policy is attached, your Amazon EKS cluster role is properly configured.

Choose Trust relationships, and then choose Edit trust policy.

Verify that the trust relationship contains the following policy. If the trust relationship matches the following policy, choose Cancel. If the trust relationship doesn’t match, copy the policy into the Edit trust policy window and choose Update policy.

You can use the AWS Management Console or the AWS CLI to create the cluster role.

Open the IAM console at https://console.aws.amazon.com/iam/.

Choose Roles, then Create role.

Under Trusted entity type, select AWS service.

From the Use cases for other AWS services dropdown list, choose EKS.

Choose EKS - Cluster for your

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags"
      ],
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "ForAnyValue:StringLike": {
          "aws:TagKeys": "kubernetes.io/cluster/*"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeVpcs",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeInstanceTopology",
        "kms:DescribeKey
...
```

Example 2 (unknown):
```unknown
eksServiceRole
```

Example 3 (unknown):
```unknown
AWSServiceRoleForAmazonEKS
```

Example 4 (unknown):
```unknown
eksClusterRole
```

---

## CreateCluster

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html#AmazonEKS-CreateCluster-request-storageConfig

**Contents:**
- CreateCluster
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
        - Note
        - Note
- Response Syntax
- Response Elements
- Errors

Creates an Amazon EKS control plane.

The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and the API server. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support kubectl exec, logs, and proxy data flows).

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

You can use the endpointPublicAccess and endpointPrivateAccess parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Amazon EKS Cluster Endpoint Access Control in the Amazon EKS User Guide .

You can use the logging parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see Amazon EKS Cluster Control Plane Logs in the Amazon EKS User Guide .

CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing.

In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see Allowing users to access your cluster and Launching Amazon EKS nodes in the Amazon EKS User Guide.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

The access configuration for the cluster.

Type: CreateAccessConfigRequest object

If you set this value to False when creating a cluster, the default networking add-ons will not be installed.

The default networking add-ons (VPC CNI, CoreDNS, kube-proxy) are installed automatically unless `bootstrapSelfManagedAddons` is set to false. See also: [Amazon EKS Cluster Control Plane Logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/).

**Examples:**

Example 1 (unknown):
```unknown
kubectl exec
```

Example 2 (unknown):
```unknown
endpointPublicAccess
```

Example 3 (unknown):
```unknown
endpointPrivateAccess
```

Example 4 (unknown):
```unknown
POST /clusters HTTP/1.1
Content-type: application/json

{
   "accessConfig": {
      "authenticationMode": "string",
      "bootstrapClusterCreatorAdminPermissions": boolean
   },
   "bootstrapSelfManagedAddons": boolean,
   "clientRequestToken": "string",
   "computeConfig": {
      "enabled": boolean,
      "nodePools": [ "string" ],
      "nodeRoleArn": "string"
   },
   "deletionProtection": boolean,
   "encryptionConfig": [
      {
         "provider": {
            "keyArn": "string"
         },
         "resources": [ "string" ]
      }
   ],
   "kubernetesNetworkConfig": {
      "elast
...
```

---

## Use application data storage for your cluster

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/storage.html

**Contents:**
- Use application data storage for your cluster
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use a range of AWS storage services with Amazon EKS for the storage needs of your applications. Through an AWS-supported breadth of Container Storage Interface (CSI) drivers, you can easily use Amazon EBS, Amazon S3, Amazon EFS, Amazon FSX, and Amazon File Cache for the storage needs of your applications running on Amazon EKS.

This chapter covers storage options for Amazon EKS clusters.

Use Kubernetes volume storage with Amazon EBS

Use elastic file system storage with Amazon EFS

Use high-performance app storage with Amazon FSx for Lustre

Use high-performance app storage with FSx for NetApp ONTAP

Use data storage with Amazon FSx for OpenZFS

Minimize latency with Amazon File Cache

Access Amazon S3 objects with Mountpoint for Amazon S3 CSI driver

Enable snapshot functionality for CSI volumes

---

## Troubleshoot problems with Amazon EKS clusters and nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html#not-authorized-for-images

**Contents:**
- Troubleshoot problems with Amazon EKS clusters and nodes
- Insufficient capacity
- Nodes fail to join cluster
- Unauthorized or access denied (kubectl)
- hostname doesn’t match
- getsockopt: no route to host
- Instances failed to join the Kubernetes cluster
- Managed node group error codes
- Not authorized for images
- Node is in NotReady state

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them. If you need to troubleshoot specific Amazon EKS areas, see the separate Troubleshooting IAM, Troubleshoot Amazon EKS Connector issues, and Troubleshooting for ADOT using EKS Add-Ons topics.

For other troubleshooting information, see Knowledge Center content about Amazon Elastic Kubernetes Service on AWS re:Post.

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified doesn’t have sufficient capacity to support a cluster.

Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message.

There are Availability Zones that a cluster can’t reside in. Compare the Availability Zones that your subnets are in with the list of Availability Zones in the Subnet requirements and considerations.

There are a few common reasons that prevent nodes from joining the cluster:

If the nodes are managed nodes, Amazon EKS adds entries to the aws-auth ConfigMap when you create the node group. If the entry was removed or modified, then you need to re-add it. For more information, enter eksctl create iamidentitymapping --help in your terminal. You can view your current aws-auth ConfigMap entries by replacing my-cluster in the following command with the name of your cluster and then running the modified command: eksctl get iamidentitymapping --cluster my-cluster . The ARN of the role that you specify can’t include a path other than /. For example, if the name of your role is development/apps/my-role, you’d need to change it to my-role when specifying the ARN for the role. Make sure that you specify the node IAM role ARN (not the instance profile ARN).

If the nodes are self-managed, and you haven’t created access entries for the ARN of the node’s IAM role, then run the same commands listed for managed nodes. If you have created an access entry for the ARN for your node IAM role, then it might not be configured properly in the access entry. Make s

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c
```

Example 2 (unknown):
```unknown
eksctl create iamidentitymapping --help
```

Example 3 (unknown):
```unknown
eksctl get iamidentitymapping --cluster my-cluster
```

Example 4 (unknown):
```unknown
development/apps/my-role
```

---

## Prepare for Kubernetes version upgrades and troubleshoot misconfigurations with cluster insights

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cluster-insights.html

**Contents:**
- Prepare for Kubernetes version upgrades and troubleshoot misconfigurations with cluster insights
- Cluster insight types
- Considerations
- Use cases
  - Upgrade insights
        - Important
  - Configuration insights
- Get started

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS cluster insights provide detection of issues and recommendations to resolve them to help you manage your cluster. Every Amazon EKS cluster undergoes automatic, recurring checks against an Amazon EKS curated list of insights. These insight checks are fully managed by Amazon EKS and offer recommendations on how to address any findings.

Configuration insights: Identifies misconfigurations in your EKS Hybrid Nodes setup that could impair functionality of your cluster or workloads.

Upgrade insights: Identifies issues that could impact your ability to upgrade to new versions of Kubernetes.

Frequency: Amazon EKS refreshes cluster insights every 24 hours, or you can manually refresh them to see the latest status. For example, you can manually refresh cluster insights after addressing an issue to see if the issue was resolved.

Permissions: Amazon EKS automatically creates a cluster access entry for cluster insights in every EKS cluster. This entry gives EKS permission to view information about your cluster. Amazon EKS uses this information to generate the insights. For more information, see AmazonEKSClusterInsightsPolicy.

Cluster insights in Amazon EKS provide automated checks to help maintain the health, reliability, and optimal configuration of your Kubernetes clusters. Below are key use cases for cluster insights, including upgrade readiness and configuration troubleshooting.

Upgrade insights are a specific type of insight checks within cluster insights. These checks returns insights related to Kubernetes version upgrade readiness. Amazon EKS runs upgrade insight checks on every EKS cluster.

Amazon EKS has temporarily rolled back a feature that would require you to use a --force flag to upgrade your cluster when there were certain cluster insight issues. For more information, see Temporary rollback of enforcing upgrade insights on update cluster version on GitHub.

For more information about updating your cluster, see Step 3: Update cluster control plane.

Before updating your cluster Kubernetes version, you can use the Upgrade insights tab of the observability dashboard in the Amazon EKS console. If your cluster has identified issues, review them and make appropriate fixes. The issues include links to Amazon EKS and Kubernetes documentation. After fixing the issue, refresh cluster insights on-dema

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ListInsights
```

---
