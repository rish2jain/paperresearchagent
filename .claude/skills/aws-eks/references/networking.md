# Aws-Eks - Networking

**Pages:** 25

---

## Assign IPs to Pods with the Amazon VPC CNI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html

**Contents:**
- Assign IPs to Pods with the Amazon VPC CNI
        - Tip
- Amazon VPC CNI versions
        - Important
        - Important
- Considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

With Amazon EKS Auto Mode, you don’t need to install or upgrade networking add-ons. Auto Mode includes pod networking and load balancing capabilities.

For more information, see Automate cluster infrastructure with EKS Auto Mode.

The Amazon VPC CNI plugin for Kubernetes add-on is deployed on each Amazon EC2 node in your Amazon EKS cluster. The add-on creates elastic network interfaces and attaches them to your Amazon EC2 nodes. The add-on also assigns a private IPv4 or IPv6 address from your VPC to each Pod.

A version of the add-on is deployed with each Fargate node in your cluster, but you don’t update it on Fargate nodes. Other compatible CNI plugins are available for use on Amazon EKS clusters, but this is the only CNI plugin supported by Amazon EKS for nodes that run on AWS infrastructure. For more information about the other compatible CNI plugins, see Alternate CNI plugins for Amazon EKS clusters. The VPC CNI isn’t supported for use with hybrid nodes. For more information about your CNI options for hybrid nodes, see Configure CNI for hybrid nodes.

The following table lists the latest available version of the Amazon EKS add-on type for each Kubernetes version.

If you’re self-managing this add-on, the versions in the table might not be the same as the available self-managed versions. For more information about updating the self-managed type of this add-on, see Update the Amazon VPC CNI (self-managed add-on).

To upgrade to VPC CNI v1.12.0 or later, you must upgrade to VPC CNI v1.7.0 first. We recommend that you update one minor version at a time.

The following are considerations for using the feature.

Versions are specified as major-version.minor-version.patch-version-eksbuild.build-number.

Check version compatibility for each feature. Some features of each release of the Amazon VPC CNI plugin for Kubernetes require certain Kubernetes versions. When using different Amazon EKS features, if a specific version of the add-on is required, then it’s noted in the feature documentation. Unless you have a specific reason for running an earlier version, we recommend running the latest version.

**Examples:**

Example 1 (unknown):
```unknown
major-version.minor-version.patch-version-eksbuild.build-number
```

---

## VPC and Subnet Considerations

**URL:** https://docs.aws.amazon.com/eks/latest/best-practices/subnets.html

**Contents:**
- VPC and Subnet Considerations
- Overview
  - EKS Cluster Architecture
  - EKS Control Plane Communication
    - Public Endpoint
    - Public and Private Endpoint
    - Private Endpoint
  - VPC configurations
  - You can configure VPC and Subnets in three different ways:
    - Using only public subnets

Operating an EKS cluster requires knowledge of AWS VPC networking, in addition to Kubernetes networking.

We recommend you understand the EKS control plane communication mechanisms before you start designing your VPC or deploying clusters into existing VPCs.

Refer to Cluster VPC considerations and Amazon EKS security group considerations when architecting a VPC and subnets to be used with EKS.

An EKS cluster consists of two VPCs:

An AWS-managed VPC that hosts the Kubernetes control plane. This VPC does not appear in the customer account.

A customer-managed VPC that hosts the Kubernetes nodes. This is where containers run, as well as other customer-managed AWS infrastructure such as load balancers used by the cluster. This VPC appears in the customer account. You need to create customer-managed VPC prior creating a cluster. The eksctl creates a VPC if you do not provide one.

The nodes in the customer VPC need the ability to connect to the managed API server endpoint in the AWS VPC. This allows the nodes to register with the Kubernetes control plane and receive requests to run application Pods.

The nodes connect to the EKS control plane through (a) an EKS public endpoint or (b) a Cross-Account elastic network interfaces (X-ENI) managed by EKS. When a cluster is created, you need to specify at least two VPC subnets. EKS places a X-ENI in each subnet specified during cluster create (also called cluster subnets). The Kubernetes API server uses these Cross-Account ENIs to communicate with nodes deployed on the customer-managed cluster VPC subnets.

As the node starts, the EKS bootstrap script is executed and Kubernetes node configuration files are installed. As part of the boot process on each instance, the container runtime agents, kubelet, and Kubernetes node agents are launched.

To register a node, Kubelet contacts the Kubernetes cluster endpoint. It establishes a connection with either the public endpoint outside of the VPC or the private endpoint within the VPC. Kubelet receives API instructions and provides status updates and heartbeats to the endpoint on a regular basis.

EKS has two ways to control access to the cluster endpoint. Endpoint access control lets you choose whether the endpoint can be reached from the public internet or only through your VPC. You can turn on the public endpoint (which is the default), the private endpoint, or both at once.

The configuration of the cluster API endpoint determines the path that nodes take to communicate

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
kubernetes.io/role/elb
```

Example 2 (unknown):
```unknown
kubernetes.io/role/internal-elb
```

Example 3 (unknown):
```unknown
custom networking feature
```

Example 4 (unknown):
```unknown
eks-cluster-sg-my-cluster-uniqueID
```

---

## Configure Amazon VPC CNI plugin to use IRSA

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-iam-role.html#cni-iam-role-create-ipv6-policy

**Contents:**
- Configure Amazon VPC CNI plugin to use IRSA
        - Note
        - Note
- Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role
- Step 2: Re-deploy Amazon VPC CNI plugin for Kubernetes Pods
- Step 3: Remove the CNI policy from the node IAM role
- Create IAM policy for clusters that use the IPv6 family

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon VPC CNI plugin for Kubernetes is the networking plugin for Pod networking in Amazon EKS clusters. The plugin is responsible for allocating VPC IP addresses to Kubernetes pods and configuring the necessary networking for Pods on each node.

The Amazon VPC CNI plugin also supports Amazon EKS Pod Identities. For more information, see Assign an IAM role to a Kubernetes service account.

Requires AWS Identity and Access Management (IAM) permissions. If your cluster uses the IPv4 family, the permissions are specified in the AmazonEKS_CNI_Policy AWS managed policy. If your cluster uses the IPv6 family, then the permissions must be added to an IAM policy that you create; for instructions, see Create IAM policy for clusters that use the IPv6 family. You can attach the policy to the Amazon EKS node IAM role, or to a separate IAM role. For instructions to attach the policy to the Amazon EKS node IAM role, see Amazon EKS node IAM role. We recommend that you assign it to a separate role, as detailed in this topic.

Creates and is configured to use a Kubernetes service account named aws-node when it’s deployed. The service account is bound to a Kubernetes clusterrole named aws-node, which is assigned the required Kubernetes permissions.

The Pods for the Amazon VPC CNI plugin for Kubernetes have access to the permissions assigned to the Amazon EKS node IAM role, unless you block access to IMDS. For more information, see Restrict access to the instance profile assigned to the worker node.

Requires an existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS.

Requires an existing AWS Identity and Access Management (IAM) OpenID Connect (OIDC) provider for your cluster. To determine whether you already have one, or to create one, see Create an IAM OIDC provider for your cluster.

Determine the IP family of your cluster.

An example output is as follows.

The output may return ipv6 instead.

Create the IAM role. You can use eksctl or kubectl and the AWS CLI to create your IAM role.

Create an IAM role and attach the IAM policy to the role with the command that matches the IP family of your cluster. The command creates and deploys an AWS CloudFormation stack that creates an IAM role, attaches the policy that you specify to it, and annotates the existing aws-node Kubernetes service account with the A

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKS_CNI_Policy
```

Example 2 (unknown):
```unknown
clusterrole
```

Example 3 (unknown):
```unknown
aws eks describe-cluster --name my-cluster | grep ipFamily
```

Example 4 (unknown):
```unknown
"ipFamily": "ipv4"
```

---

## KubernetesNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_KubernetesNetworkConfigRequest.html#AmazonEKS-Type-KubernetesNetworkConfigRequest-serviceIpv4Cidr

**Contents:**
- KubernetesNetworkConfigRequest
- Contents
        - Important
- See Also

The Kubernetes network configuration for the cluster.

Request to enable or disable the load balancing capability on your EKS Auto Mode cluster. For more information, see EKS Auto Mode load balancing capability in the Amazon EKS User Guide.

Type: ElasticLoadBalancing object

Specify which IP family is used to assign Kubernetes pod and service IP addresses. If you don't specify a value, ipv4 is used by default. You can only specify an IP family when you create a cluster and can't change this value once the cluster is created. If you specify ipv6, the VPC and subnets that you specify for cluster creation must have both IPv4 and IPv6 CIDR blocks assigned to them. You can't specify ipv6 for clusters in China Regions.

You can only specify ipv6 for 1.21 and later clusters that use version 1.10.1 or later of the Amazon VPC CNI add-on. If you specify ipv6, then ensure that your VPC meets the requirements listed in the considerations listed in Assigning IPv6 addresses to pods and services in the Amazon EKS User Guide. Kubernetes assigns services IPv6 addresses from the unique local address range (fc00::/7). You can't specify a custom IPv6 CIDR block. Pod addresses are assigned from the subnet's IPv6 CIDR.

Valid Values: ipv4 | ipv6

Don't specify a value if you select ipv6 for ipFamily. The CIDR block to assign Kubernetes service IP addresses from. If you don't specify a block, Kubernetes assigns addresses from either the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks. We recommend that you specify a block that does not overlap with resources in other networks that are peered or connected to your VPC. The block must meet the following requirements:

Within one of the following private IP address blocks: 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16.

Doesn't overlap with any CIDR block assigned to the VPC that you selected for VPC.

You can only specify a custom CIDR block when you create a cluster. You can't change this value after the cluster is created.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
ipv4 | ipv6
```

Example 2 (unknown):
```unknown
10.100.0.0/16
```

Example 3 (unknown):
```unknown
172.20.0.0/16
```

Example 4 (unknown):
```unknown
172.16.0.0/12
```

---

## Learn how EKS Pod Identity grants pods access to AWS services

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html

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

## IAM roles for Amazon EKS add-ons

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/add-ons-iam.html

**Contents:**
- IAM roles for Amazon EKS add-ons

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Certain Amazon EKS add-ons need IAM roles and permissions to call AWS APIs. For example, the Amazon VPC CNI add-on calls certain AWS APIs to configure networking resources in your account. These add-ons need to be granted permission using IAM. More specifically, the service account of the pod running the add-on needs to be associated with an IAM role with a specific IAM policy.

The recommended way to grant AWS permissions to cluster workloads is using the Amazon EKS feature Pod Identities. You can use a Pod Identity Association to map the service account of an add-on to an IAM role. If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod. The environment variables configure the AWS SDKs, including the AWS CLI, to use the EKS Pod Identity credentials. For more information, see Learn how EKS Pod Identity grants pods access to AWS services

Amazon EKS add-ons can help manage the life cycle of pod identity associations corresponding to the add-on. For example, you can create or update an Amazon EKS add-on and the necessary pod identity association in a single API call. Amazon EKS also provides an API for retrieving suggested IAM policies.

Confirm that Amazon EKS pod identity agent is setup on your cluster.

Determine if the add-on you want to install requires IAM permissions using the describe-addon-versions AWS CLI operation. If the requiresIamPermissions flag is true, then you should use the describe-addon-configurations operation to determine the permissions needed by the addon. The response includes a list of suggested managed IAM policies.

Retrieve the name of the Kubernetes Service Account and the IAM policy using the describe-addon-configuration CLI operation. Evaluate the scope of the suggested policy against your security requirements.

Create an IAM role using the suggested permissions policy, and the trust policy required by Pod Identity. For more information, see Create a Pod Identity association (AWS Console).

Create or update an Amazon EKS add-on using the CLI. Specify at least one pod identity association. A pod identity association is the name of a Kubernetes service account, and the ARN of the IAM role.

Pod identity associations created using the add-on APIs are owned by the respective add-on. If you delete the add-on, the po

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
describe-addon-versions
```

Example 2 (unknown):
```unknown
requiresIamPermissions
```

Example 3 (unknown):
```unknown
describe-addon-configurations
```

Example 4 (unknown):
```unknown
describe-addon-configuration
```

---

## Configure Pods to access AWS services with service accounts

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-configure-pods.html

**Contents:**
- Configure Pods to access AWS services with service accounts
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

If a Pod needs to access AWS services, then you must configure it to use a Kubernetes service account. The service account must be associated to an AWS Identity and Access Management (IAM) role that has permissions to access the AWS services.

An existing cluster. If you don’t have one, you can create one using one of the guides in Get started with Amazon EKS.

An existing Kubernetes service account and an EKS Pod Identity association that associates the service account with an IAM role. The role must have an associated IAM policy that contains the permissions that you want your Pods to have to use AWS services. For more information about how to create the service account and role, and configure them, see Assign an IAM role to a Kubernetes service account.

The latest version of the AWS CLI installed and configured on your device or AWS CloudShell. You can check your current version with aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. For example, if your cluster version is 1.29, you can use kubectl version 1.28, 1.29, or 1.30 with it. To install or upgrade kubectl, see Set up kubectl and eksctl.

An existing kubectl config file that contains your cluster configuration. To create a kubectl config file, see Connect kubectl to an EKS cluster by creating a kubeconfig file.

Use the following command to create a deployment manifest that you can deploy a Pod to confirm configuration with. Replace the example values with your own values.

Deploy the manifest to your cluster.

Confirm that the required environment variables exist for your Pod.

View the Pods that were deployed with the deployment in the previous step.

An example output is as follows.

Confirm that the

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
cat >my-deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      serviceAccountName: my-service-account
      containers:
      - name: my-app
        image: public.ecr.aws/nginx/nginx:X.XX
EOF
```

Example 3 (unknown):
```unknown
kubectl apply -f my-deployment.yaml
```

Example 4 (unknown):
```unknown
kubectl get pods | grep my-app
```

---

## IAM roles for service accounts

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html

**Contents:**
- IAM roles for service accounts
        - Note
        - Important
        - Note
- IAM, Kubernetes, and OpenID Connect (OIDC) background information

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Applications in a Pod’s containers can use an AWS SDK or the AWS CLI to make API requests to AWS services using AWS Identity and Access Management (IAM) permissions. Applications must sign their AWS API requests with AWS credentials. IAM roles for service accounts (IRSA) provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance’s role, you associate an IAM role with a Kubernetes service account and configure your Pods to use the service account. You can’t use IAM roles for service accounts with local clusters for Amazon EKS on AWS Outposts.

IAM roles for service accounts provide the following benefits:

Least privilege – You can scope IAM permissions to a service account, and only Pods that use that service account have access to those permissions. This feature also eliminates the need for third-party solutions such as kiam or kube2iam.

Credential isolation – When access to the Amazon EC2 Instance Metadata Service (IMDS) is restricted, a Pod’s containers can only retrieve credentials for the IAM role that’s associated with the service account that the container uses. A container never has access to credentials that are used by other containers in other Pods. If IMDS is not restricted, the Pod’s containers also have access to the Amazon EKS node IAM role and the containers may be able to gain access to credentials of IAM roles of other Pods on the same node. For more information, see Restrict access to the instance profile assigned to the worker node.

Pods configured with hostNetwork: true will always have IMDS access, but the AWS SDKs and CLI will use IRSA credentials when enabled.

Auditability – Access and event logging is available through AWS CloudTrail to help ensure retrospective auditing.

Containers are not a security boundary, and the use of IAM roles for service accounts does not change this. Pods assigned to the same node will share a kernel and potentially other resources depending on your Pod configuration. While Pods running on separate nodes will be isolated at the compute layer, there are node applications that have additional permissions in the Kubernetes API beyond the scope of a

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
hostNetwork: true
```

Example 2 (unknown):
```unknown
https://oidc.eks.region.amazonaws.com
```

Example 3 (unknown):
```unknown
server cant find oidc.eks.region.amazonaws.com: NXDOMAIN
```

Example 4 (unknown):
```unknown
AssumeRoleWithWebIdentity
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#security-iam-service-with-iam-policy-best-practices

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

## View Amazon EKS networking requirements for VPC and subnets

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html

**Contents:**
- View Amazon EKS networking requirements for VPC and subnets
- VPC requirements and considerations
        - Important
- Subnet requirements and considerations
  - Subnet requirements for clusters
  - IP address family usage by component
        - Note
  - Subnet requirements for nodes
- Shared subnet requirements and considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you create a cluster, you specify a VPC and at least two subnets that are in different Availability Zones. This topic provides an overview of Amazon EKS specific requirements and considerations for the VPC and subnets that you use with your cluster. If you don’t have a VPC to use with Amazon EKS, see Create an Amazon VPC for your Amazon EKS cluster. If you’re creating a local or extended cluster on AWS Outposts, see Create a VPC and subnets for Amazon EKS clusters on AWS Outposts instead of this topic. The content in this topic applies for Amazon EKS clusters with hybrid nodes. For additional networking requirements for hybrid nodes, see Prepare networking for hybrid nodes.

When you create a cluster, the VPC that you specify must meet the following requirements and considerations:

The VPC must have a sufficient number of IP addresses available for the cluster, any nodes, and other Kubernetes resources that you want to create. If the VPC that you want to use doesn’t have a sufficient number of IP addresses, try to increase the number of available IP addresses.

You can do this by updating the cluster configuration to change which subnets and security groups the cluster uses. You can update from the AWS Management Console, the latest version of the AWS CLI, AWS CloudFormation, and eksctl version v0.164.0-rc.0 or later. You might need to do this to provide subnets with more available IP addresses to successfully upgrade a cluster version.

All subnets that you add must be in the same set of AZs as originally provided when you created the cluster. New subnets must satisfy all of the other requirements, for example they must have sufficient IP addresses.

For example, assume that you made a cluster and specified four subnets. In the order that you specified them, the first subnet is in the us-west-2a Availability Zone, the second and third subnets are in us-west-2b Availability Zone, and the fourth subnet is in us-west-2c Availability Zone. If you want to change the subnets, you must provide at least one subnet in each of the three Availability Zones, and the subnets must be in the same VPC as the original subnets.

If you need more IP addresses than the CIDR blocks in the VPC have, you can add additional CIDR blocks by associating additional Classless Inter-Domain Routing (CIDR) blocks with your VPC. You ca

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
v0.164.0-rc.0
```

Example 2 (unknown):
```unknown
kubectl attach
```

Example 3 (unknown):
```unknown
kubectl exec
```

Example 4 (unknown):
```unknown
kubectl logs
```

---

## Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html

**Contents:**
- Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts
- Service account tokens
- Cluster add-ons
- Granting AWS Identity and Access Management permissions to workloads on Amazon Elastic Kubernetes Service clusters
  - Comparing EKS Pod Identity and IRSA
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The BoundServiceAccountTokenVolume feature is enabled by default in Kubernetes versions. This feature improves the security of service account tokens by allowing workloads running on Kubernetes to request JSON web tokens that are audience, time, and key bound. Service account tokens have an expiration of one hour. In earlier Kubernetes versions, the tokens didn’t have an expiration. This means that clients that rely on these tokens must refresh the tokens within an hour. The following Kubernetes client SDKs refresh tokens automatically within the required time frame:

Go version 0.15.7 and later

Python version 12.0.0 and later

Java version 9.0.0 and later

JavaScript version 0.10.3 and later

Haskell version 0.3.0.0

C# version 7.0.5 and later

If your workload is using an earlier client version, then you must update it. To enable a smooth migration of clients to the newer time-bound service account tokens, Kubernetes adds an extended expiry period to the service account token over the default one hour. For Amazon EKS clusters, the extended expiry period is 90 days. Your Amazon EKS cluster’s Kubernetes API server rejects requests with tokens that are greater than 90 days old. We recommend that you check your applications and their dependencies to make sure that the Kubernetes client SDKs are the same or later than the versions listed previously.

When the API server receives requests with tokens that are greater than one hour old, it annotates the API audit log event with annotations.authentication.k8s.io/stale-token. The value of the annotation looks like the following example:

If your cluster has control plane logging enabled, then the annotations are in the audit logs. You can use the following CloudWatch Logs Insights query to identify all the Pods in your Amazon EKS cluster that are using stale tokens:

The subject refers to the service account that the Pod used. The elapsedtime indicates the elapsed time (in seconds) after reading the latest token. The requests to the API server are denied when the elapsedtime exceeds 90 days (7,776,000 seconds). You should proactively update your applications' Kubernetes client SDK to use one of the version listed previously that automatically refresh the token. If the service account token used is close to 90 days and you don’t have sufficient time to update your cl

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
annotations.authentication.k8s.io/stale-token
```

Example 2 (unknown):
```unknown
subject: system:serviceaccount:common:fluent-bit, seconds after warning threshold: 4185802.
```

Example 3 (unknown):
```unknown
fields @timestamp
|filter @logStream like /kube-apiserver-audit/
|filter @message like /seconds after warning threshold/
|parse @message "subject: *, seconds after warning threshold:*\"" as subject, elapsedtime
```

Example 4 (unknown):
```unknown
elapsedtime
```

---

## Analyze AWS CloudTrail log file entries

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/understanding-service-name-entries.html

**Contents:**
- Analyze AWS CloudTrail log file entries
- Log Entries for Amazon EKS Service Linked Roles

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

A trail is a configuration that enables delivery of events as log files to an Amazon S3 bucket that you specify. CloudTrail log files contain one or more log entries. An event represents a single request from any source and includes information about the requested action. This include information such as the date and time of the action and the request parameters that were used. CloudTrail log files aren’t an ordered stack trace of the public API calls, so they don’t appear in any specific order.

The following example shows a CloudTrail log entry that demonstrates the CreateCluster action.

The Amazon EKS service linked roles make API calls to AWS resources. CloudTrail log entries with username: AWSServiceRoleForAmazonEKS and username: AWSServiceRoleForAmazonEKSNodegroup appears for calls made by the Amazon EKS service linked roles. For more information about Amazon EKS and service linked roles, see Using service-linked roles for Amazon EKS.

The following example shows a CloudTrail log entry that demonstrates a DeleteInstanceProfile action that’s made by the AWSServiceRoleForAmazonEKSNodegroup service linked role, noted in the sessionContext.

**Examples:**

Example 1 (unknown):
```unknown
CreateCluster
```

Example 2 (unknown):
```unknown
{
  "eventVersion": "1.05",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AKIAIOSFODNN7EXAMPLE",
    "arn": "arn:aws:iam::111122223333:user/username",
    "accountId": "111122223333",
    "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
    "userName": "username"
  },
  "eventTime": "2018-05-28T19:16:43Z",
  "eventSource": "eks.amazonaws.com",
  "eventName": "CreateCluster",
  "awsRegion": "region-code",
  "sourceIPAddress": "205.251.233.178",
  "userAgent": "PostmanRuntime/6.4.0",
  "requestParameters": {
    "resourcesVpcConfig": {
      "subnetIds": [
        "subnet-a670c2df",
     
...
```

Example 3 (unknown):
```unknown
username: AWSServiceRoleForAmazonEKS
```

Example 4 (unknown):
```unknown
username: AWSServiceRoleForAmazonEKSNodegroup
```

---

## Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html#service-account-tokens

**Contents:**
- Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts
- Service account tokens
- Cluster add-ons
- Granting AWS Identity and Access Management permissions to workloads on Amazon Elastic Kubernetes Service clusters
  - Comparing EKS Pod Identity and IRSA
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The BoundServiceAccountTokenVolume feature is enabled by default in Kubernetes versions. This feature improves the security of service account tokens by allowing workloads running on Kubernetes to request JSON web tokens that are audience, time, and key bound. Service account tokens have an expiration of one hour. In earlier Kubernetes versions, the tokens didn’t have an expiration. This means that clients that rely on these tokens must refresh the tokens within an hour. The following Kubernetes client SDKs refresh tokens automatically within the required time frame:

Go version 0.15.7 and later

Python version 12.0.0 and later

Java version 9.0.0 and later

JavaScript version 0.10.3 and later

Haskell version 0.3.0.0

C# version 7.0.5 and later

If your workload is using an earlier client version, then you must update it. To enable a smooth migration of clients to the newer time-bound service account tokens, Kubernetes adds an extended expiry period to the service account token over the default one hour. For Amazon EKS clusters, the extended expiry period is 90 days. Your Amazon EKS cluster’s Kubernetes API server rejects requests with tokens that are greater than 90 days old. We recommend that you check your applications and their dependencies to make sure that the Kubernetes client SDKs are the same or later than the versions listed previously.

When the API server receives requests with tokens that are greater than one hour old, it annotates the API audit log event with annotations.authentication.k8s.io/stale-token. The value of the annotation looks like the following example:

If your cluster has control plane logging enabled, then the annotations are in the audit logs. You can use the following CloudWatch Logs Insights query to identify all the Pods in your Amazon EKS cluster that are using stale tokens:

The subject refers to the service account that the Pod used. The elapsedtime indicates the elapsed time (in seconds) after reading the latest token. The requests to the API server are denied when the elapsedtime exceeds 90 days (7,776,000 seconds). You should proactively update your applications' Kubernetes client SDK to use one of the version listed previously that automatically refresh the token. If the service account token used is close to 90 days and you don’t have sufficient time to update your cl

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
annotations.authentication.k8s.io/stale-token
```

Example 2 (unknown):
```unknown
subject: system:serviceaccount:common:fluent-bit, seconds after warning threshold: 4185802.
```

Example 3 (unknown):
```unknown
fields @timestamp
|filter @logStream like /kube-apiserver-audit/
|filter @message like /seconds after warning threshold/
|parse @message "subject: *, seconds after warning threshold:*\"" as subject, elapsedtime
```

Example 4 (unknown):
```unknown
elapsedtime
```

---

## View helpful references for AWS CloudTrail

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/service-name-info-in-cloudtrail.html

**Contents:**
- View helpful references for AWS CloudTrail

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you create your AWS account, CloudTrail is also enabled on your AWS account. When any activity occurs in Amazon EKS, that activity is recorded in a CloudTrail event along with other AWS service events in Event history. You can view, search, and download recent events in your AWS account. For more information, see Viewing events with CloudTrail event history.

For an ongoing record of events in your AWS account, including events for Amazon EKS, create a trail. A trail enables CloudTrail to deliver log files to an Amazon S3 bucket. By default, when you create a trail in the console, the trail applies to all AWS Regions. The trail logs events from all AWS Regions in the AWS partition and delivers the log files to the Amazon S3 bucket that you specify. Additionally, you can configure other AWS services to further analyze and act upon the event data that’s collected in CloudTrail logs. For more information, see the following resources.

Overview for creating a trail

CloudTrail supported services and integrations

Configuring Amazon SNS notifications for CloudTrail

Receiving CloudTrail log files from multiple regions and Receiving CloudTrail log files from multiple accounts

All Amazon EKS actions are logged by CloudTrail and are documented in the Amazon EKS API Reference. For example, calls to the CreateCluster, ListClusters and DeleteCluster sections generate entries in the CloudTrail log files.

Every event or log entry contains information about the type of IAM identity that made the request, and which credentials were used. If temporary credentials were used, the entry shows how the credentials were obtained.

For more information, see the CloudTrail userIdentity element.

---

## Configure Amazon VPC CNI plugin to use IRSA

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-iam-role.html

**Contents:**
- Configure Amazon VPC CNI plugin to use IRSA
        - Note
        - Note
- Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role
- Step 2: Re-deploy Amazon VPC CNI plugin for Kubernetes Pods
- Step 3: Remove the CNI policy from the node IAM role
- Create IAM policy for clusters that use the IPv6 family

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon VPC CNI plugin for Kubernetes is the networking plugin for Pod networking in Amazon EKS clusters. The plugin is responsible for allocating VPC IP addresses to Kubernetes pods and configuring the necessary networking for Pods on each node.

The Amazon VPC CNI plugin also supports Amazon EKS Pod Identities. For more information, see Assign an IAM role to a Kubernetes service account.

Requires AWS Identity and Access Management (IAM) permissions. If your cluster uses the IPv4 family, the permissions are specified in the AmazonEKS_CNI_Policy AWS managed policy. If your cluster uses the IPv6 family, then the permissions must be added to an IAM policy that you create; for instructions, see Create IAM policy for clusters that use the IPv6 family. You can attach the policy to the Amazon EKS node IAM role, or to a separate IAM role. For instructions to attach the policy to the Amazon EKS node IAM role, see Amazon EKS node IAM role. We recommend that you assign it to a separate role, as detailed in this topic.

Creates and is configured to use a Kubernetes service account named aws-node when it’s deployed. The service account is bound to a Kubernetes clusterrole named aws-node, which is assigned the required Kubernetes permissions.

The Pods for the Amazon VPC CNI plugin for Kubernetes have access to the permissions assigned to the Amazon EKS node IAM role, unless you block access to IMDS. For more information, see Restrict access to the instance profile assigned to the worker node.

Requires an existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS.

Requires an existing AWS Identity and Access Management (IAM) OpenID Connect (OIDC) provider for your cluster. To determine whether you already have one, or to create one, see Create an IAM OIDC provider for your cluster.

Determine the IP family of your cluster.

An example output is as follows.

The output may return ipv6 instead.

Create the IAM role. You can use eksctl or kubectl and the AWS CLI to create your IAM role.

Create an IAM role and attach the IAM policy to the role with the command that matches the IP family of your cluster. The command creates and deploys an AWS CloudFormation stack that creates an IAM role, attaches the policy that you specify to it, and annotates the existing aws-node Kubernetes service account with the A

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKS_CNI_Policy
```

Example 2 (unknown):
```unknown
clusterrole
```

Example 3 (unknown):
```unknown
aws eks describe-cluster --name my-cluster | grep ipFamily
```

Example 4 (unknown):
```unknown
"ipFamily": "ipv4"
```

---

## Learn how EKS Auto Mode works

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/auto-reference.html

**Contents:**
- Learn how EKS Auto Mode works
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Use this chapter to learn how the components of Amazon EKS Auto Mode clusters work.

Learn about Amazon EKS Auto Mode Managed instances

Learn about identity and access in EKS Auto Mode

Learn about VPC Networking and Load Balancing in EKS Auto Mode

---

## Learn how EKS Pod Identity grants pods access to AWS services

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html#pod-id-benefits

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

## AWS add-ons

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/workloads-add-ons-available-eks.html#add-ons-vpc-cni

**Contents:**
- AWS add-ons
- Amazon VPC CNI plugin for Kubernetes
        - Note
  - Required IAM permissions
  - Update information
- CoreDNS
        - Note
  - Required IAM permissions
  - Additional information
- Kube-proxy

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The following Amazon EKS add-ons are available to create on your cluster. You can view the most current list of available add-ons using eksctl, the AWS Management Console, or the AWS CLI. To see all available add-ons or to install an add-on, see Create an Amazon EKS add-on. If an add-on requires IAM permissions, then you must have an IAM OpenID Connect (OIDC) provider for your cluster. To determine whether you have one, or to create one, see Create an IAM OIDC provider for your cluster. You can an create or delete an add-on after you’ve installed it. For more information, see Update an Amazon EKS add-on or Remove an Amazon EKS add-on from a cluster. For more information about considerations specific to running EKS add-ons with Amazon EKS Hybrid Nodes, see Configure add-ons for hybrid nodes.

You can use any of the following Amazon EKS add-ons.

Provide native VPC networking for your cluster

Amazon VPC CNI plugin for Kubernetes

A flexible, extensible DNS server that can serve as the Kubernetes cluster DNS

EC2, Fargate, EKS Auto Mode, EKS Hybrid Nodes

Maintain network rules on each Amazon EC2 node

EC2, EKS Hybrid Nodes

Provide Amazon EBS storage for your cluster

Amazon EBS CSI driver

Provide Amazon EFS storage for your cluster

Amazon EFS CSI driver

Provide Amazon FSx for Lustre storage for your cluster

Amazon FSx CSI driver

Provide Amazon S3 storage for your cluster

Mountpoint for Amazon S3 CSI Driver

Detect additional node health issues

Node monitoring agent

EC2, EKS Hybrid Nodes

Enable the use of snapshot functionality in compatible CSI drivers, such as the Amazon EBS CSI driver

CSI snapshot controller

EC2, Fargate, EKS Auto Mode, EKS Hybrid Nodes

SageMaker HyperPod task governance optimizes compute resource allocation and usage across teams in Amazon EKS clusters, addressing inefficiencies in task prioritization and resource sharing.

Amazon SageMaker HyperPod task governance

The Amazon SageMaker HyperPod Observability AddOn provides comprehensive monitoring and observability capabilities for HyperPod clusters.

Amazon SageMaker HyperPod Observability Add-on

Amazon SageMaker HyperPod training operator enables efficient distributed training on Amazon EKS clusters with advanced scheduling and resource management capabilities.

Amazon SageMaker HyperPod training operator

A Kubernetes agent

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKSVPCCNIRole
```

Example 2 (unknown):
```unknown
AmazonEKS_CNI_Policy
```

Example 3 (unknown):
```unknown
eksctl create iamserviceaccount --name aws-node --namespace kube-system --cluster my-cluster --role-name AmazonEKSVPCCNIRole \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --approve
```

Example 4 (unknown):
```unknown
1.28.x-eksbuild.y
```

---

## Assign security groups to individual Pods

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html

**Contents:**
- Assign security groups to individual Pods
- Compatibility with Amazon VPC CNI plugin for Kubernetes features
- Considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Applies to: Linux nodes with Amazon EC2 instances

Applies to: Private subnets

Security groups for Pods integrate Amazon EC2 security groups with Kubernetes Pods. You can use Amazon EC2 security groups to define rules that allow inbound and outbound network traffic to and from Pods that you deploy to nodes running on many Amazon EC2 instance types and Fargate. For a detailed explanation of this capability, see the Introducing security groups for Pods blog post.

You can use security groups for Pods with the following features:

IPv4 Source Network Address Translation - For more information, see Enable outbound internet access for Pods.

IPv6 addresses to clusters, Pods, and services - For more information, see Learn about IPv6 addresses to clusters, Pods, and services.

Restricting traffic using Kubernetes network policies - For more information, see Limit Pod traffic with Kubernetes network policies.

Before deploying security groups for Pods, consider the following limitations and conditions:

Security groups for Pods can’t be used with Windows nodes or EKS Auto Mode.

Security groups for Pods can be used with clusters configured for the IPv6 family that contain Amazon EC2 nodes by using version 1.16.0 or later of the Amazon VPC CNI plugin. You can use security groups for Pods with clusters configure IPv6 family that contain only Fargate nodes by using version 1.7.7 or later of the Amazon VPC CNI plugin. For more information, see Learn about IPv6 addresses to clusters, Pods, and services

Security groups for Pods are supported by most Nitro-based Amazon EC2 instance families, though not by all generations of a family. For example, the m5, c5, r5, m6g, c6g, and r6g instance family and generations are supported. No instance types in the t family are supported. For a complete list of supported instance types, see the limits.go file on GitHub. Your nodes must be one of the listed instance types that have IsTrunkingCompatible: true in that file.

If you’re using custom networking and security groups for Pods together, the security group specified by security groups for Pods is used instead of the security group specified in the ENIConfig.

If you’re using version 1.10.2 or earlier of the Amazon VPC CNI plugin and you include the terminationGracePeriodSeconds setting in your Pod spec, the value for the setting ca

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
IsTrunkingCompatible: true
```

Example 2 (unknown):
```unknown
terminationGracePeriodSeconds
```

Example 3 (unknown):
```unknown
POD_SECURITY_GROUP_ENFORCING_MODE
```

Example 4 (unknown):
```unknown
LoadBalancer
```

---

## Configure Amazon VPC CNI plugin to use IRSA

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-iam-role.html#cni-iam-role-create-role

**Contents:**
- Configure Amazon VPC CNI plugin to use IRSA
        - Note
        - Note
- Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role
- Step 2: Re-deploy Amazon VPC CNI plugin for Kubernetes Pods
- Step 3: Remove the CNI policy from the node IAM role
- Create IAM policy for clusters that use the IPv6 family

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon VPC CNI plugin for Kubernetes is the networking plugin for Pod networking in Amazon EKS clusters. The plugin is responsible for allocating VPC IP addresses to Kubernetes pods and configuring the necessary networking for Pods on each node.

The Amazon VPC CNI plugin also supports Amazon EKS Pod Identities. For more information, see Assign an IAM role to a Kubernetes service account.

Requires AWS Identity and Access Management (IAM) permissions. If your cluster uses the IPv4 family, the permissions are specified in the AmazonEKS_CNI_Policy AWS managed policy. If your cluster uses the IPv6 family, then the permissions must be added to an IAM policy that you create; for instructions, see Create IAM policy for clusters that use the IPv6 family. You can attach the policy to the Amazon EKS node IAM role, or to a separate IAM role. For instructions to attach the policy to the Amazon EKS node IAM role, see Amazon EKS node IAM role. We recommend that you assign it to a separate role, as detailed in this topic.

Creates and is configured to use a Kubernetes service account named aws-node when it’s deployed. The service account is bound to a Kubernetes clusterrole named aws-node, which is assigned the required Kubernetes permissions.

The Pods for the Amazon VPC CNI plugin for Kubernetes have access to the permissions assigned to the Amazon EKS node IAM role, unless you block access to IMDS. For more information, see Restrict access to the instance profile assigned to the worker node.

Requires an existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS.

Requires an existing AWS Identity and Access Management (IAM) OpenID Connect (OIDC) provider for your cluster. To determine whether you already have one, or to create one, see Create an IAM OIDC provider for your cluster.

Determine the IP family of your cluster.

An example output is as follows.

The output may return ipv6 instead.

Create the IAM role. You can use eksctl or kubectl and the AWS CLI to create your IAM role.

Create an IAM role and attach the IAM policy to the role with the command that matches the IP family of your cluster. The command creates and deploys an AWS CloudFormation stack that creates an IAM role, attaches the policy that you specify to it, and annotates the existing aws-node Kubernetes service account with the A

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKS_CNI_Policy
```

Example 2 (unknown):
```unknown
clusterrole
```

Example 3 (unknown):
```unknown
aws eks describe-cluster --name my-cluster | grep ipFamily
```

Example 4 (unknown):
```unknown
"ipFamily": "ipv4"
```

---

## Security considerations for Amazon Elastic Kubernetes Service

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-eks.html

**Contents:**
- Security considerations for Amazon Elastic Kubernetes Service
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The following are considerations for security of the cloud, as they affect Amazon EKS.

Infrastructure security in Amazon EKS

Understand resilience in Amazon EKS clusters

Cross-service confused deputy prevention in Amazon EKS

---

## Assign an IAM role to a Kubernetes service account

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-association.html

**Contents:**
- Assign an IAM role to a Kubernetes service account
- Create a Pod Identity association (AWS Console)
        - Note
- Create a Pod Identity association (AWS CLI)
        - Note
        - Note
- Confirm configuration
- Next Steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers how to configure a Kubernetes service account to assume an AWS Identity and Access Management (IAM) role with EKS Pod Identity. Any Pods that are configured to use the service account can then access any AWS service that the role has permissions to access.

To create an EKS Pod Identity association, there is only a single step; you create the association in EKS through the AWS Management Console, AWS CLI, AWS SDKs, AWS CloudFormation and other tools. There isn’t any data or metadata about the associations inside the cluster in any Kubernetes objects and you don’t add any annotations to the service accounts.

An existing cluster. If you don’t have one, you can create one by following one of the guides in Get started with Amazon EKS.

The IAM principal that is creating the association must have iam:PassRole.

The latest version of the AWS CLI installed and configured on your device or AWS CloudShell. You can check your current version with aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version. To update it, see Installing AWS CLI to your home directory in the AWS CloudShell User Guide.

The kubectl command line tool is installed on your device or AWS CloudShell. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster. For example, if your cluster version is 1.29, you can use kubectl version 1.28, 1.29, or 1.30 with it. To install or upgrade kubectl, see Set up kubectl and eksctl.

An existing kubectl config file that contains your cluster configuration. To create a kubectl config file, see Connect kubectl to an EKS cluster by creating a kubeconfig file.

Open the Amazon EKS console.

In the left navigation pane, select Clusters, and then select the name of the cluster that you want to configure the EKS Pod Identity Agent add-on for.

Choose the Access tab.

In the Pod Identity associations, choose Create.

For the IAM role, select the IAM role with the permissions that you want

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
iam:PassRole
```

Example 2 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AllowEksAuthToAssumeRoleForPodIdentity",
            "Effect": "Allow",
            "Principal": {
                "Service": "pods.eks.amazonaws.com"
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
sts:AssumeRole
```

---
