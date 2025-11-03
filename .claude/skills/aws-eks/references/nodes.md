# Aws-Eks - Nodes

**Pages:** 48

---

## ComputeConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigResponse.html#AmazonEKS-Type-ComputeConfigResponse-nodeRoleArn

**Contents:**
- ComputeConfigResponse
- Contents
- See Also

Indicates the status of the request to update the compute capability of your EKS Auto Mode cluster.

Indicates if the compute capability is enabled on your EKS Auto Mode cluster. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account.

Indicates the current configuration of node pools in your EKS Auto Mode cluster. For more information, see EKS Auto Mode Node Pools in the Amazon EKS User Guide.

Type: Array of strings

The ARN of the IAM Role EKS will assign to EC2 Managed Instances in your EKS Auto Mode cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## VpcConfigRequest

For VPC configuration details, see the canonical [VpcConfigRequest](https://docs.aws.amazon.com/eks/latest/APIReference/API_VpcConfigRequest.html) API reference or the VpcConfigRequest section below in this document.

---

## Create self-managed Microsoft Windows nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/launch-windows-workers.html

**Contents:**
- Create self-managed Microsoft Windows nodes
        - Important
- eksctl
        - Note
        - Important
        - Note
- AWS Management Console
        - Important
        - Note
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how to launch Auto Scaling groups of Windows nodes that register with your Amazon EKS cluster. After the nodes join the cluster, you can deploy Kubernetes applications to them.

Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices. For more information, see Amazon EC2 pricing.

You can launch Windows nodes in Amazon EKS extended clusters on AWS Outposts, but you can’t launch them in local clusters on AWS Outposts. For more information, see Deploy Amazon EKS on-premises with AWS Outposts.

Enable Windows support for your cluster. We recommend that you review important considerations before you launch a Windows node group. For more information, see Enable Windows support.

You can launch self-managed Windows nodes with either of the following:

AWS Management Console

Launch self-managed Windows nodes using eksctl

This procedure requires that you have installed eksctl, and that your eksctl version is at least 0.215.0. You can check your version with the following command.

For instructions on how to install or upgrade eksctl, see Installation in the eksctl documentation.

This procedure only works for clusters that were created with eksctl.

(Optional) If the AmazonEKS_CNI_Policy managed IAM policy (if you have an IPv4 cluster) or the AmazonEKS_CNI_IPv6_Policy (that you created yourself if you have an IPv6 cluster) is attached to your Amazon EKS node IAM role, we recommend assigning it to an IAM role that you associate to the Kubernetes aws-node service account instead. For more information, see Configure Amazon VPC CNI plugin to use IRSA.

This procedure assumes that you have an existing cluster. If you don’t already have an Amazon EKS cluster and an Amazon Linux node group to add a Windows node group to, we recommend that you follow Get started with Amazon EKS – eksctl. This guide provides a complete walkthrough for how to create an Amazon EKS cluster with Amazon Linux nodes.

Create your node group with the following command. Replace region-code with the AWS Region that your cluster is in. Replace my-cluster with your cluster name. The name can contain only alphanumeric characters (case-sensitive) and hyphens. It must start with an alphanumeric character and can’t be longer than 100 characters. The name must be unique 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl version
```

Example 2 (unknown):
```unknown
AmazonEKS_CNI_IPv6_Policy
```

Example 3 (unknown):
```unknown
region-code
```

Example 4 (unknown):
```unknown
eksctl create nodegroup \
    --region region-code \
    --cluster my-cluster \
    --name ng-windows \
    --node-type t2.large \
    --nodes 3 \
    --nodes-min 1 \
    --nodes-max 4 \
    --managed=false \
    --node-ami-family WindowsServer2019FullContainer
```

---

## ComputeConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigResponse.html#AmazonEKS-Type-ComputeConfigResponse-nodePools

**Contents:**
- ComputeConfigResponse
- Contents
- See Also

Indicates the status of the request to update the compute capability of your EKS Auto Mode cluster.

Indicates if the compute capability is enabled on your EKS Auto Mode cluster. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account.

Indicates the current configuration of node pools in your EKS Auto Mode cluster. For more information, see EKS Auto Mode Node Pools in the Amazon EKS User Guide.

Type: Array of strings

The ARN of the IAM Role EKS will assign to EC2 Managed Instances in your EKS Auto Mode cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## RemoteNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_RemoteNetworkConfigRequest.html#AmazonEKS-Type-RemoteNetworkConfigRequest-remoteNodeNetworks

**Contents:**
- RemoteNetworkConfigRequest
- Contents
- See Also

The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.

The list of network CIDRs that can contain hybrid nodes.

These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator.

Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, 10.2.0.0/16).

It must satisfy the following requirements:

Each block must be within an IPv4 RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.

Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway, AWS Site-to-Site VPN, or AWS Direct Connect.

Each host must allow outbound connection to the EKS cluster control plane on TCP ports 443 and 10250.

Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations.

Each host must allow TCP and UDP network connectivity to and from other hosts that are running CoreDNS on UDP port 53 for service and pod DNS names.

Type: Array of RemoteNodeNetwork objects

Array Members: Maximum number of 1 item.

The list of network CIDRs that can contain pods that run Kubernetes webhooks on hybrid nodes.

These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations.

Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, 10.2.0.0/16).

It must satisfy the following requirements:

Each block must be within an IPv4 RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.

Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

Type: Array of RemotePodNetwork objects

Array Members: Maximum number of 1 item.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
 10.2.0.0/16
```

Example 2 (unknown):
```unknown
 10.2.0.0/16
```

---

## VpcConfigRequest

See the canonical [VpcConfigRequest API reference](https://docs.aws.amazon.com/eks/latest/APIReference/API_VpcConfigRequest.html) for complete details.

---

## Create nodes with optimized Amazon Linux AMIs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html#arm-ami

**Contents:**
- Create nodes with optimized Amazon Linux AMIs
        - Note
- Amazon EKS-optimized accelerated Amazon Linux AMIs
- Amazon EKS-optimized Arm Amazon Linux AMIs
- More information

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon EKS-optimized Amazon Linux AMIs are built on top of Amazon Linux 2 (AL2) and Amazon Linux 2023 (AL2023). They are configured to serve as the base images for Amazon EKS nodes. The AMIs are configured to work with Amazon EKS and they include the following components:

AWS IAM Authenticator

You can track security or privacy events for Amazon Linux at the Amazon Linux security center by choosing the tab for your desired version. You can also subscribe to the applicable RSS feed. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue.

Before deploying an accelerated or Arm AMI, review the information in Amazon EKS-optimized accelerated Amazon Linux AMIs and Amazon EKS-optimized Arm Amazon Linux AMIs.

Amazon EC2 P2 instances aren’t supported on Amazon EKS because they require NVIDIA driver version 470 or earlier.

Any newly created managed node groups in clusters on version 1.30 or newer will automatically default to using AL2023 as the node operating system. Previously, new node groups would default to AL2. You can continue to use AL2 by choosing it as the AMI type when creating a new node group.

Amazon EKS will no longer publish EKS-optimized Amazon Linux 2 (AL2) AMIs after November 26th, 2025. Additionally, Kubernetes version 1.32 is the last version for which Amazon EKS will release AL2 AMIs. From version 1.33 onwards, Amazon EKS will continue to release AL2023 and Bottlerocket based AMIs.

The Amazon EKS-optimized accelerated Amazon Linux AMIs are built on top of the standard Amazon EKS-optimized Amazon Linux AMIs. They are configured to serve as optional images for Amazon EKS nodes to support GPU, Inferentia, and Trainium based workloads.

For more information, see Use EKS-optimized accelerated AMIs for GPU instances.

Arm instances deliver significant cost savings for scale-out and Arm-based applications such as web servers, containerized microservices, caching fleets, and distributed data stores. When adding Arm nodes to your cluster, review the following considerations.

If your cluster was deployed before August 17, 2020, you must do a one-time upgrade of critical cluster add-on manifests. This is so that Kubernetes can pull the correct image for each hardware architecture in use in your cluster. For mor

*[Content truncated]*

---

## VpcConfigRequest

See the canonical [VpcConfigRequest API reference](https://docs.aws.amazon.com/eks/latest/APIReference/API_VpcConfigRequest.html) for complete details.

---

## Maintain nodes yourself with self-managed nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/worker.html

**Contents:**
- Maintain nodes yourself with self-managed nodes
        - Important
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

A cluster contains one or more Amazon EC2 nodes that Pods are scheduled on. Amazon EKS nodes run in your AWS account and connect to the control plane of your cluster through the cluster API server endpoint. You’re billed for them based on Amazon EC2 prices. For more information, see Amazon EC2 pricing.

A cluster can contain several node groups. Each node group contains one or more nodes that are deployed in an Amazon EC2 Auto Scaling group. The instance type of the nodes within the group can vary, such as when using attribute-based instance type selection with Karpenter. All instances in a node group must use the Amazon EKS node IAM role.

Amazon EKS provides specialized Amazon Machine Images (AMIs) that are called Amazon EKS optimized AMIs. The AMIs are configured to work with Amazon EKS. Their components include containerd, kubelet, and the AWS IAM Authenticator. The AMIs also contain a specialized bootstrap script that allows it to discover and connect to your cluster’s control plane automatically.

If you restrict access to the public endpoint of your cluster using CIDR blocks, we recommend that you also enable private endpoint access. This is so that nodes can communicate with the cluster. Without the private endpoint enabled, the CIDR blocks that you specify for public access must include the egress sources from your VPC. For more information, see Cluster API server endpoint.

To add self-managed nodes to your Amazon EKS cluster, see the topics that follow. If you launch self-managed nodes manually, add the following tag to each node while making sure that <cluster-name> matches your cluster. For more information, see Adding and deleting tags on an individual resource. If you follow the steps in the guides that follow, the required tag is automatically added to nodes for you.

kubernetes.io/cluster/<cluster-name>

Tags in Amazon EC2 Instance Metadata Service (IMDS) are not compatible with EKS nodes. When Instance Metadata Tags are enabled, the use of forward slashes ('/') in tag values is prevented. This limitation can cause instance launch failures, particularly when using node management tools like Karpenter or Cluster Autoscaler, as these services rely on tags containing forward slashes for proper functionality.

For more information about nodes from a general Kubernetes perspective, see Nodes in the

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<cluster-name>
```

Example 2 (unknown):
```unknown
kubernetes.io/cluster/<cluster-name>
```

---

## Control if a workload is deployed on EKS Auto Mode nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/associate-workload.html

**Contents:**
- Control if a workload is deployed on EKS Auto Mode nodes
- Require a workload is deployed to EKS Auto Mode nodes
        - Note
- Require a workload is not deployed to EKS Auto Mode nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When running workloads in an EKS cluster with EKS Auto Mode, you might need to control whether specific workloads run on EKS Auto Mode nodes or other compute types. This topic describes how to use node selectors and affinity rules to ensure your workloads are scheduled on the intended compute infrastructure.

The examples in this topic demonstrate how to use the eks.amazonaws.com/compute-type label to either require or prevent workload deployment on EKS Auto Mode nodes. This is particularly useful in mixed-mode clusters where you’re running both EKS Auto Mode and other compute types, such as self-managed Karpenter provisioners or EKS Managed Node Groups.

EKS Auto Mode nodes have set the value of the label eks.amazonaws.com/compute-type to auto. You can use this label to control if a workload is deployed to nodes managed by EKS Auto Mode.

This nodeSelector value is not required for EKS Auto Mode. This nodeSelector value is only relevant if you are running a cluster in a mixed mode, node types not managed by EKS Auto Mode. For example, you may have static compute capacity deployed to your cluster with EKS Managed Node Groups, and have dynamic compute capacity managed by EKS Auto Mode.

You can add this nodeSelector to Deployments or other workloads to require Kubernetes schedule them onto EKS Auto Mode nodes.

You can add this nodeAffinity to Deployments or other workloads to require Kubernetes not schedule them onto EKS Auto Mode nodes.

**Examples:**

Example 1 (unknown):
```unknown
eks.amazonaws.com/compute-type
```

Example 2 (unknown):
```unknown
eks.amazonaws.com/compute-type
```

Example 3 (unknown):
```unknown
nodeSelector
```

Example 4 (unknown):
```unknown
nodeSelector
```

---

## Create nodes with optimized Amazon Linux AMIs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html#gpu-ami

**Contents:**
- Create nodes with optimized Amazon Linux AMIs
        - Note
- Amazon EKS-optimized accelerated Amazon Linux AMIs
- Amazon EKS-optimized Arm Amazon Linux AMIs
- More information

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon EKS-optimized Amazon Linux AMIs are built on top of Amazon Linux 2 (AL2) and Amazon Linux 2023 (AL2023). They are configured to serve as the base images for Amazon EKS nodes. The AMIs are configured to work with Amazon EKS and they include the following components:

AWS IAM Authenticator

You can track security or privacy events for Amazon Linux at the Amazon Linux security center by choosing the tab for your desired version. You can also subscribe to the applicable RSS feed. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue.

Before deploying an accelerated or Arm AMI, review the information in Amazon EKS-optimized accelerated Amazon Linux AMIs and Amazon EKS-optimized Arm Amazon Linux AMIs.

Amazon EC2 P2 instances aren’t supported on Amazon EKS because they require NVIDIA driver version 470 or earlier.

Any newly created managed node groups in clusters on version 1.30 or newer will automatically default to using AL2023 as the node operating system. Previously, new node groups would default to AL2. You can continue to use AL2 by choosing it as the AMI type when creating a new node group.

Amazon EKS will no longer publish EKS-optimized Amazon Linux 2 (AL2) AMIs after November 26th, 2025. Additionally, Kubernetes version 1.32 is the last version for which Amazon EKS will release AL2 AMIs. From version 1.33 onwards, Amazon EKS will continue to release AL2023 and Bottlerocket based AMIs.

The Amazon EKS-optimized accelerated Amazon Linux AMIs are built on top of the standard Amazon EKS-optimized Amazon Linux AMIs. They are configured to serve as optional images for Amazon EKS nodes to support GPU, Inferentia, and Trainium based workloads.

For more information, see Use EKS-optimized accelerated AMIs for GPU instances.

Arm instances deliver significant cost savings for scale-out and Arm-based applications such as web servers, containerized microservices, caching fleets, and distributed data stores. When adding Arm nodes to your cluster, review the following considerations.

If your cluster was deployed before August 17, 2020, you must do a one-time upgrade of critical cluster add-on manifests. This is so that Kubernetes can pull the correct image for each hardware architecture in use in your cluster. For mor

*[Content truncated]*

---

## VpcConfigRequest

See the canonical [VpcConfigRequest API reference](https://docs.aws.amazon.com/eks/latest/APIReference/API_VpcConfigRequest.html) for complete details.

---

## Deploy Pods in alternate subnets with custom networking

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-custom-network.html

**Contents:**
- Deploy Pods in alternate subnets with custom networking
        - Tip
- Considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Applies to: Linux IPv4 Fargate nodes, Linux nodes with Amazon EC2 instances

By default, when the Amazon VPC CNI plugin for Kubernetes creates secondary elastic network interfaces (network interfaces) for your Amazon EC2 node, it creates them in the same subnet as the node’s primary network interface. It also associates the same security groups to the secondary network interface that are associated to the primary network interface. For one or more of the following reasons, you might want the plugin to create secondary network interfaces in a different subnet or want to associate different security groups to the secondary network interfaces, or both:

There’s a limited number of IPv4 addresses that are available in the subnet that the primary network interface is in. This might limit the number of Pods that you can create in the subnet. By using a different subnet for secondary network interfaces, you can increase the number of available IPv4 addresses available for Pods.

For security reasons, your Pods might need to use a different subnet or security groups than the node’s primary network interface.

The nodes are configured in public subnets, and you want to place the Pods in private subnets. The route table associated to a public subnet includes a route to an internet gateway. The route table associated to a private subnet doesn’t include a route to an internet gateway.

You can also add a new or existing subnet directly to your Amazon EKS Cluster, without using custom networking. For more information, see Add an existing VPC Subnet to an Amazon EKS cluster from the management console.

The following are considerations for using the feature.

With custom networking enabled, no IP addresses assigned to the primary network interface are assigned to Pods. Only IP addresses from secondary network interfaces are assigned to Pods.

If your cluster uses the IPv6 family, you can’t use custom networking.

If you plan to use custom networking only to help alleviate IPv4 address exhaustion, you can create a cluster using the IPv6 family instead. For more information, see Learn about IPv6 addresses to clusters, Pods, and services.

Even though Pods deployed to subnets specified for secondary network interfaces can use different subnet and security groups than the node’s primary network interface, the subnets and securi

*[Content truncated]*

---

## VpcConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_VpcConfigRequest.html

**Contents:**
- VpcConfigRequest
- Contents
- See Also

An object representing the VPC configuration to use for an Amazon EKS cluster.

Set this value to true to enable private access for your cluster's Kubernetes API server endpoint. If you enable private access, Kubernetes API requests from within your cluster's VPC use the private VPC endpoint. The default value for this parameter is false, which disables private access for your Kubernetes API server. If you disable private access and you have nodes or AWS Fargate pods in the cluster, then ensure that publicAccessCidrs includes the necessary CIDR blocks for communication with the nodes or Fargate pods. For more information, see Cluster API server endpoint in the Amazon EKS User Guide .

Set this value to false to disable public access to your cluster's Kubernetes API server endpoint. If you disable public access, your cluster's Kubernetes API server can only receive requests from within the cluster VPC. The default value for this parameter is true, which enables public access for your Kubernetes API server. The endpoint domain name and IP address family depends on the value of the ipFamily for the cluster. For more information, see Cluster API server endpoint in the Amazon EKS User Guide .

The CIDR blocks that are allowed access to your cluster's public Kubernetes API server endpoint. Communication to the endpoint from addresses outside of the CIDR blocks that you specify is denied. The default value is 0.0.0.0/0 and additionally ::/0 for dual-stack `IPv6` clusters. If you've disabled private endpoint access, make sure that you specify the necessary CIDR blocks for every node and AWS Fargate Pod in the cluster. For more information, see Cluster API server endpoint in the Amazon EKS User Guide .

Note that the public endpoints are dual-stack for only IPv6 clusters that are made after October 2024. You can't add IPv6 CIDR blocks to IPv4 clusters or IPv6 clusters that were made before October 2024.

Type: Array of strings

Specify one or more security groups for the cross-account elastic network interfaces that Amazon EKS creates to use that allow communication between your nodes and the Kubernetes control plane. If you don't specify any security groups, then familiarize yourself with the difference between Amazon EKS defaults for clusters deployed with Kubernetes. For more information, see Amazon EKS security group considerations in the Amazon EKS User Guide .

Type: Array of strings

Specify subnets for your Amazon EKS nodes. Amazon EKS creates cross-account

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
publicAccessCidrs
```

---

## Hybrid nodes nodeadm reference

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-nodeadm.html

**Contents:**
- Hybrid nodes nodeadm reference
        - Important
- Download nodeadm
- nodeadm install
- nodeadm config check
- nodeadm init
- nodeadm upgrade
- nodeadm uninstall
- nodeadm debug
- Nodeadm file locations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon EKS Hybrid Nodes CLI (nodeadm) simplifies the installation, configuration, registration, and uninstallation of the hybrid nodes components. You can include nodeadm in your operating system images to automate hybrid node bootstrap, see Prepare operating system for hybrid nodes for more information.

The nodeadm version for hybrid nodes differs from the nodeadm version used for bootstrapping Amazon EC2 instances as nodes in Amazon EKS clusters. Follow the documentation and references for the appropriate nodeadm version. This documentation page is for the hybrid nodes nodeadm version.

The source code for the hybrid nodes nodeadm is published in the https://github.com/aws/eks-hybrid GitHub repository.

You must run nodeadm with a user that has root/sudo privileges.

The hybrid nodes version of nodeadm is hosted in Amazon S3 fronted by Amazon CloudFront. To install nodeadm on each on-premises host, you can run the following command from your on-premises hosts.

Add executable file permission to the downloaded binary on each host.

The nodeadm install command is used to install the artifacts and dependencies required to run and join hybrid nodes to an Amazon EKS cluster. The nodeadm install command can be run individually on each hybrid node or can be run during image build pipelines to preinstall the hybrid nodes dependencies in operating system images.

(Required) KUBERNETES_VERSION The major.minor version of EKS Kubernetes to install, for example 1.32

--credential-provider

Credential provider to install. Supported values are iam-ra and ssm. See Prepare credentials for hybrid nodes for more information.

Source for containerd. nodeadm supports installing containerd from the OS distro, Docker packages, and skipping containerd install.

distro - This is the default value. nodeadm will install the latest containerd package distributed by the node OS that is compatible with the EKS Kubernetes version. distro is not a supported value for Red Hat Enterprise Linux (RHEL) operating systems.

docker - nodeadm will install the latest containerd package built and distributed by Docker that is compatible with the EKS Kubernetes version. docker is not a supported value for Amazon Linux 2023.

none - nodeadm will not install containerd package. You must manually install containerd before running nodeadm init.

Spe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
curl -OL 'https://hybrid-assets.eks.amazonaws.com/releases/latest/bin/linux/amd64/nodeadm'
```

Example 2 (unknown):
```unknown
curl -OL 'https://hybrid-assets.eks.amazonaws.com/releases/latest/bin/linux/arm64/nodeadm'
```

Example 3 (unknown):
```unknown
chmod +x nodeadm
```

Example 4 (unknown):
```unknown
nodeadm install
```

---

## Prepare credentials for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-creds.html

**Contents:**
- Prepare credentials for hybrid nodes
- Hybrid Nodes IAM Role
- Setup AWS SSM hybrid activations
        - Important
- Setup AWS IAM Roles Anywhere
- Create the Hybrid Nodes IAM role
  - AWS CloudFormation
  - AWS CLI
  - AWS Management Console

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS Hybrid Nodes use temporary IAM credentials provisioned by AWS SSM hybrid activations or AWS IAM Roles Anywhere to authenticate with the Amazon EKS cluster. You must use either AWS SSM hybrid activations or AWS IAM Roles Anywhere with the Amazon EKS Hybrid Nodes CLI (nodeadm). You should not use both AWS SSM hybrid activations and AWS IAM Roles Anywhere. We recommend that you use AWS SSM hybrid activations if you do not have existing Public Key Infrastructure (PKI) with a Certificate Authority (CA) and certificates for your on-premises environments. If you do have existing PKI and certificates on-premises, use AWS IAM Roles Anywhere.

Before you can connect hybrid nodes to your Amazon EKS cluster, you must create an IAM role that will be used with AWS SSM hybrid activations or AWS IAM Roles Anywhere for your hybrid nodes credentials. After cluster creation, you will use this role with an Amazon EKS access entry or aws-auth ConfigMap entry to map the IAM role to Kubernetes Role-Based Access Control (RBAC). For more information on associating the Hybrid Nodes IAM role with Kubernetes RBAC, see Prepare cluster access for hybrid nodes.

The Hybrid Nodes IAM role must have the following permissions.

Permissions for nodeadm to use the eks:DescribeCluster action to gather information about the cluster used for connecting hybrid nodes to the cluster. If you do not enable the eks:DescribeCluster action, then you must pass your Kubernetes API endpoint, cluster CA bundle, and service IPv4 CIDR in the node configuration you pass to nodeadm when you run nodeadm init.

Permissions for the kubelet to use container images from Amazon Elastic Container Registry (Amazon ECR) as defined in the AmazonEC2ContainerRegistryPullOnly policy.

If using AWS SSM, permissions for nodeadm init to use AWS SSM hybrid activations as defined in the aws-managed-policy/latest/reference/AmazonSSMManagedInstanceCore.html policy.

If using AWS SSM, permissions to use the ssm:DeregisterManagedInstance action and ssm:DescribeInstanceInformation action for nodeadm uninstall to deregister instances.

(Optional) Permissions for the Amazon EKS Pod Identity Agent to use the eks-auth:AssumeRoleForPodIdentity action to retrieve credentials for pods.

Before setting up AWS SSM hybrid activations, you must have a Hybrid Nodes IAM role created and c

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:DescribeCluster
```

Example 2 (unknown):
```unknown
eks:DescribeCluster
```

Example 3 (unknown):
```unknown
ssm:DeregisterManagedInstance
```

Example 4 (unknown):
```unknown
ssm:DescribeInstanceInformation
```

---

## Amazon EKS Hybrid Nodes overview

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-overview.html

**Contents:**
- Amazon EKS Hybrid Nodes overview
- Features
- Limits
- Considerations
- Additional resources

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

With Amazon EKS Hybrid Nodes, you can use your on-premises and edge infrastructure as nodes in Amazon EKS clusters. AWS manages the AWS-hosted Kubernetes control plane of the Amazon EKS cluster, and you manage the hybrid nodes that run in your on-premises or edge environments. This unifies Kubernetes management across your environments and offloads Kubernetes control plane management to AWS for your on-premises and edge applications.

Amazon EKS Hybrid Nodes works with any on-premises hardware or virtual machines, bringing the efficiency, scalability, and availability of Amazon EKS to wherever your applications need to run. You can use a wide range of Amazon EKS features with Amazon EKS Hybrid Nodes including Amazon EKS add-ons, Amazon EKS Pod Identity, cluster access entries, cluster insights, and extended Kubernetes version support. Amazon EKS Hybrid Nodes natively integrates with AWS services including AWS Systems Manager, AWS IAM Roles Anywhere, Amazon Managed Service for Prometheus, and Amazon CloudWatch for centralized monitoring, logging, and identity management.

With Amazon EKS Hybrid Nodes, there are no upfront commitments or minimum fees, and you are charged per hour for the vCPU resources of your hybrid nodes when they are attached to your Amazon EKS clusters. For more pricing information, see Amazon EKS Pricing.

EKS Hybrid Nodes has the following high-level features:

Managed Kubernetes control plane: AWS manages the AWS-hosted Kubernetes control plane of the EKS cluster, and you manage the hybrid nodes that run in your on-premises or edge environments. This unifies Kubernetes management across your environments and offloads Kubernetes control plane management to AWS for your on-premises and edge applications. By moving the Kubernetes control plane to AWS, you can conserve on-premises capacity for your applications and trust that the Kubernetes control plane scales with your workloads.

Consistent EKS experience: Most EKS features are supported with EKS Hybrid Nodes for a consistent EKS experience across your on-premises and cloud environments including EKS add-ons, EKS Pod Identity, cluster access entries, cluster insights, extended Kubernetes version support, and more. See Configure add-ons for hybrid nodes for more information on the EKS add-ons supported with EKS Hybrid Nodes.

Centralized ob

*[Content truncated]*

---

## EKS Hybrid Nodes and network disconnections

**URL:** https://docs.aws.amazon.com/eks/latest/best-practices/hybrid-nodes-network-disconnections.html

**Contents:**
- EKS Hybrid Nodes and network disconnections

The EKS Hybrid Nodes architecture can be new to customers who are accustomed to running local Kubernetes clusters entirely in their own data centers or edge locations. With EKS Hybrid Nodes, the Kubernetes control plane runs in an AWS Region and only the nodes run on-premises, resulting in a “stretched” or “extended” Kubernetes cluster architecture.

This leads to a common question, “What happens if my nodes get disconnected from the Kubernetes control plane?”

In this guide, we answer that question through a review of the following topics. It is recommended to validate the stability and reliability of your applications through network disconnections as each application may behave differently based on its dependencies, configuration, and environment. See the aws-samples/eks-hybrid-examples GitHub repo for test setup, procedures, and results you can reference to test network disconnections with EKS Hybrid Nodes and your own applications. The GitHub repo also contains additional details of the tests used to validate the behavior explained in this guide.

Best practices for stability through network disconnections

Kubernetes pod failover behavior through network disconnections

Application network traffic through network disconnections

Host credentials through network disconnections

---

## Simplify node lifecycle with managed node groups

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html

**Contents:**
- Simplify node lifecycle with managed node groups
- Managed node groups concepts
        - Important
- Managed node group capacity types
  - On-Demand
  - Spot

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes (Amazon EC2 instances) for Amazon EKS Kubernetes clusters.

With Amazon EKS managed node groups, you don’t need to separately provision or register the Amazon EC2 instances that provide compute capacity to run your Kubernetes applications. You can create, automatically update, or terminate nodes for your cluster with a single operation. Node updates and terminations automatically drain nodes to ensure that your applications stay available.

Every managed node is provisioned as part of an Amazon EC2 Auto Scaling group that’s managed for you by Amazon EKS. Every resource including the instances and Auto Scaling groups runs within your AWS account. Each node group runs across multiple Availability Zones that you define.

Managed node groups can also optionally leverage node auto repair, which continuously monitors the health of nodes. It automatically reacts to detected problems and replaces nodes when possible. This helps overall availability of the cluster with minimal manual intervention. For more information, see Enable node auto repair and investigate node health issues.

You can add a managed node group to new or existing clusters using the Amazon EKS console, eksctl, AWS CLI, AWS API, or infrastructure as code tools including AWS CloudFormation. Nodes launched as part of a managed node group are automatically tagged for auto-discovery by the Kubernetes Cluster Autoscaler. You can use the node group to apply Kubernetes labels to nodes and update them at any time.

There are no additional costs to use Amazon EKS managed node groups, you only pay for the AWS resources you provision. These include Amazon EC2 instances, Amazon EBS volumes, Amazon EKS cluster hours, and any other AWS infrastructure. There are no minimum fees and no upfront commitments.

To get started with a new Amazon EKS cluster and managed node group, see Get started with Amazon EKS – AWS Management Console and AWS CLI.

To add a managed node group to an existing cluster, see Create a managed node group for your cluster.

Amazon EKS managed node groups create and manage Amazon EC2 instances for you.

Every managed node is provisioned as part of an Amazon EC2 Auto Scaling group that’s managed for you by Amazon EKS. Moreover, every resource including Amaz

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
--balance-similar-node-groups
```

Example 2 (unknown):
```unknown
MapPublicIpOnLaunch
```

Example 3 (unknown):
```unknown
com.amazonaws.region-code.ecr.api
```

Example 4 (unknown):
```unknown
region-code
```

---

## Customize managed nodes with launch templates

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html#mng-specify-eks-ami

**Contents:**
- Customize managed nodes with launch templates
- Launch template configuration basics
        - Note
- Tagging Amazon EC2 instances
- Using custom security groups
- Amazon EC2 user data
        - Note
        - Important
        - Note
- Specifying an AMI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

For the highest level of customization, you can deploy managed nodes using your own launch template. Using a launch template allows capabilities such as the following:

Provide bootstrap arguments at deployment of a node, such as extra kubelet arguments.

Assign IP addresses to Pods from a different CIDR block than the IP address assigned to the node.

Deploy your own custom AMI to nodes.

Deploy your own custom CNI to nodes.

When you give your own launch template upon first creating a managed node group, you will also have greater flexibility later. As long as you deploy a managed node group with your own launch template, you can iteratively update it with a different version of the same launch template. When you update your node group to a different version of your launch template, all nodes in the group are recycled to match the new configuration of the specified launch template version.

Managed node groups are always deployed with a launch template to be used with the Amazon EC2 Auto Scaling group. When you don’t provide a launch template, the Amazon EKS API creates one automatically with default values in your account. However, we don’t recommend that you modify auto-generated launch templates. Furthermore, existing node groups that don’t use a custom launch template can’t be updated directly. Instead, you must create a new node group with a custom launch template to do so.

You can create an Amazon EC2 Auto Scaling launch template with the AWS Management Console, AWS CLI, or an AWS SDK. For more information, see Creating a Launch Template for an Auto Scaling group in the Amazon EC2 Auto Scaling User Guide. Some of the settings in a launch template are similar to the settings used for managed node configuration. When deploying or updating a node group with a launch template, some settings must be specified in either the node group configuration or the launch template. Don’t specify a setting in both places. If a setting exists where it shouldn’t, then operations such as creating or updating a node group fail.

The following table lists the settings that are prohibited in a launch template. It also lists similar settings, if any are available, that are required in the managed node group configuration. The listed settings are the settings that appear in the console. They might have similar but different n

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
bootstrap.sh
```

Example 2 (unknown):
```unknown
InstanceRequirements
```

Example 3 (unknown):
```unknown
TagSpecification
```

Example 4 (unknown):
```unknown
CreateNodegroup
```

---

## Configure add-ons for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-add-ons.html

**Contents:**
- Configure add-ons for hybrid nodes
- AWS add-ons
- kube-proxy and CoreDNS
- CloudWatch Observability agent
- Amazon Managed Prometheus managed collector for hybrid nodes
- AWS Distro for OpenTelemetry (ADOT)
- AWS Load Balancer Controller
- EKS Pod Identity Agent
        - Note
  - Ubuntu/RHEL/AL2023

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This page describes considerations for running AWS add-ons and community add-ons on Amazon EKS Hybrid Nodes. To learn more about Amazon EKS add-ons and the processes for creating, upgrading, and removing add-ons from your cluster, see Amazon EKS add-ons. Unless otherwise noted on this page, the processes for creating, upgrading, and removing Amazon EKS add-ons is the same for Amazon EKS clusters with hybrid nodes as it is for Amazon EKS clusters with nodes running in AWS Cloud. Only the add-ons included on this page have been validated for compatibility with Amazon EKS Hybrid Nodes.

The following AWS add-ons are compatible with Amazon EKS Hybrid Nodes.

v1.25.14-eksbuild.2 and above

v1.9.3-eksbuild.7 and above

AWS Distro for OpenTelemetry (ADOT)

v0.102.1-eksbuild.2 and above

CloudWatch Observability agent

v2.2.1-eksbuild.1 and above

EKS Pod Identity Agent

v1.3.3-eksbuild.1 and above, except for Bottlerocket

v1.3.7-eksbuild.2 and above for Bottlerocket

Node monitoring agent

v1.2.0-eksbuild.1 and above

CSI snapshot controller

v8.1.0-eksbuild.1 and above

AWS Private CA Connector for Kubernetes

v1.6.0-eksbuild.1 and above

The following community add-ons are compatible with Amazon EKS Hybrid Nodes. To learn more about community add-ons, see Community add-ons.

Kubernetes Metrics Server

v0.7.2-eksbuild.1 and above

v1.17.2-eksbuild.1 and above

Prometheus Node Exporter

v1.9.1-eksbuild.2 and above

v2.15.0-eksbuild.4 and above

v0.19.0-eksbuild.1 and above

In addition to the Amazon EKS add-ons in the tables above, the Amazon Managed Service for Prometheus Collector, and the AWS Load Balancer Controller for application ingress (HTTP) and load balancing (TCP/UDP) are compatible with hybrid nodes.

There are AWS add-ons and community add-ons that aren’t compatible with Amazon EKS Hybrid Nodes. The latest versions of these add-ons have an anti-affinity rule for the default eks.amazonaws.com/compute-type: hybrid label applied to hybrid nodes. This prevents them from running on hybrid nodes when deployed in your clusters. If you have clusters with both hybrid nodes and nodes running in AWS Cloud, you can deploy these add-ons in your cluster to nodes running in AWS Cloud. The Amazon VPC CNI is not compatible with hybrid nodes, and Cilium and Calico are supported as the Container Networking Interfaces (CNI

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks.amazonaws.com/compute-type: hybrid
```

Example 2 (unknown):
```unknown
amazoncloudwatchagents
```

Example 3 (unknown):
```unknown
RUN_WITH_IRSA
```

Example 4 (unknown):
```unknown
kubectl edit amazoncloudwatchagents -n amazon-cloudwatch cloudwatch-agent
```

---

## Create self-managed Amazon Linux nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html

**Contents:**
- Create self-managed Amazon Linux nodes
- eksctl
        - Important
- AWS Management Console
        - Note
        - Note
        - Important
        - Note
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how you can launch Auto Scaling groups of Linux nodes that register with your Amazon EKS cluster. After the nodes join the cluster, you can deploy Kubernetes applications to them. You can also launch self-managed Amazon Linux nodes with eksctl or the AWS Management Console. If you need to launch nodes on AWS Outposts, see Create Amazon Linux nodes on AWS Outposts.

An existing Amazon EKS cluster. To deploy one, see Create an Amazon EKS cluster. If you have subnets in the AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled, those subnets must not have been passed in when you created your cluster.

An existing IAM role for the nodes to use. To create one, see Amazon EKS node IAM role. If this role doesn’t have either of the policies for the VPC CNI, the separate role that follows is required for the VPC CNI pods.

(Optional, but recommended) The Amazon VPC CNI plugin for Kubernetes add-on configured with its own IAM role that has the necessary IAM policy attached to it. For more information, see Configure Amazon VPC CNI plugin to use IRSA.

Familiarity with the considerations listed in Choose an optimal Amazon EC2 node instance type. Depending on the instance type you choose, there may be additional prerequisites for your cluster and VPC.

You can launch self-managed Linux nodes using either of the following:

AWS Management Console

Launch self-managed Linux nodes using eksctl

Install version 0.215.0 or later of the eksctl command line tool installed on your device or AWS CloudShell. To install or update eksctl, see Installation in the eksctl documentation.

(Optional) If the AmazonEKS_CNI_Policy managed IAM policy is attached to your Amazon EKS node IAM role, we recommend assigning it to an IAM role that you associate to the Kubernetes aws-node service account instead. For more information, see Configure Amazon VPC CNI plugin to use IRSA.

The following command creates a node group in an existing cluster. Replace al-nodes with a name for your node group. The node group name can’t be longer than 63 characters. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters. Replace my-cluster with the name of your cluster. The name can contain only alphanumeric characters (case-sensitive) and hyphens. It must star

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
example value
```

Example 2 (unknown):
```unknown
--node-type
```

Example 3 (unknown):
```unknown
volumeType: gp2
```

Example 4 (unknown):
```unknown
eksctl create nodegroup \
  --cluster my-cluster \
  --name al-nodes \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4 \
  --ssh-access \
  --managed=false \
  --ssh-public-key my-key
```

---

## Customize managed nodes with launch templates

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html#launch-template-tagging

**Contents:**
- Customize managed nodes with launch templates
- Launch template configuration basics
        - Note
- Tagging Amazon EC2 instances
- Using custom security groups
- Amazon EC2 user data
        - Note
        - Important
        - Note
- Specifying an AMI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

For the highest level of customization, you can deploy managed nodes using your own launch template. Using a launch template allows capabilities such as the following:

Provide bootstrap arguments at deployment of a node, such as extra kubelet arguments.

Assign IP addresses to Pods from a different CIDR block than the IP address assigned to the node.

Deploy your own custom AMI to nodes.

Deploy your own custom CNI to nodes.

When you give your own launch template upon first creating a managed node group, you will also have greater flexibility later. As long as you deploy a managed node group with your own launch template, you can iteratively update it with a different version of the same launch template. When you update your node group to a different version of your launch template, all nodes in the group are recycled to match the new configuration of the specified launch template version.

Managed node groups are always deployed with a launch template to be used with the Amazon EC2 Auto Scaling group. When you don’t provide a launch template, the Amazon EKS API creates one automatically with default values in your account. However, we don’t recommend that you modify auto-generated launch templates. Furthermore, existing node groups that don’t use a custom launch template can’t be updated directly. Instead, you must create a new node group with a custom launch template to do so.

You can create an Amazon EC2 Auto Scaling launch template with the AWS Management Console, AWS CLI, or an AWS SDK. For more information, see Creating a Launch Template for an Auto Scaling group in the Amazon EC2 Auto Scaling User Guide. Some of the settings in a launch template are similar to the settings used for managed node configuration. When deploying or updating a node group with a launch template, some settings must be specified in either the node group configuration or the launch template. Don’t specify a setting in both places. If a setting exists where it shouldn’t, then operations such as creating or updating a node group fail.

The following table lists the settings that are prohibited in a launch template. It also lists similar settings, if any are available, that are required in the managed node group configuration. The listed settings are the settings that appear in the console. They might have similar but different n

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
bootstrap.sh
```

Example 2 (unknown):
```unknown
InstanceRequirements
```

Example 3 (unknown):
```unknown
TagSpecification
```

Example 4 (unknown):
```unknown
CreateNodegroup
```

---

## Manage compute resources by using nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-compute.html

**Contents:**
- Manage compute resources by using nodes
        - Note
- Compare compute options
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

A Kubernetes node is a machine that runs containerized applications. Each node has the following components:

Container runtime – Software that’s responsible for running the containers.

kubelet – Makes sure that containers are healthy and running within their associated Pod.

kube-proxy – Maintains network rules that allow communication to your Pods.

For more information, see Nodes in the Kubernetes documentation.

Your Amazon EKS cluster can schedule Pods on any combination of EKS Auto Mode managed nodes, self-managed nodes, Amazon EKS managed node groups, AWS Fargate, and Amazon EKS Hybrid Nodes. To learn more about nodes deployed in your cluster, see View Kubernetes resources in the AWS Management Console.

Excluding hybrid nodes, nodes must be in the same VPC as the subnets you selected when you created the cluster. However, the nodes don’t have to be in the same subnets.

The following table provides several criteria to evaluate when deciding which options best meet your requirements. Self-managed nodes are another option which support all of the criteria listed, but they require a lot more manual maintenance. For more information, see Maintain nodes yourself with self-managed nodes.

Bottlerocket has some specific differences from the general information in this table. For more information, see the Bottlerocket documentation on GitHub.

Can be deployed to AWS Outposts

Can be deployed to an AWS Local Zone

Can run containers that require Windows

Can run containers that require Linux

Can run workloads that require the Inferentia chip

Yes – Amazon Linux nodes only

Can run workloads that require a GPU

Yes – Amazon Linux nodes only

Can run workloads that require Arm processors

Can run AWS Bottlerocket

Pods share CPU, memory, storage, and network resources with other Pods.

Must deploy and manage Amazon EC2 instances

No - Learn about EC2 managed instances

Yes – the on-premises physical or virtual machines are managed by you with your choice of tooling.

Must secure, maintain, and patch the operating system of Amazon EC2 instances

Yes – the operating system running on your physical or virtual machines are managed by you with your choice of tooling.

Can provide bootstrap arguments at deployment of a node, such as extra kubelet arguments.

Yes – Using eksctl or a launch template with a custom AMI.


*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
HostNetwork
```

---

## ComputeConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigRequest.html#AmazonEKS-Type-ComputeConfigRequest-nodeRoleArn

**Contents:**
- ComputeConfigRequest
- Contents
- See Also

Request to update the configuration of the compute capability of your EKS Auto Mode cluster. For example, enable the capability. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Request to enable or disable the compute capability on your EKS Auto Mode cluster. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account.

Configuration for node pools that defines the compute resources for your EKS Auto Mode cluster. For more information, see EKS Auto Mode Node Pools in the Amazon EKS User Guide.

Type: Array of strings

The ARN of the IAM Role EKS will assign to EC2 Managed Instances in your EKS Auto Mode cluster. This value cannot be changed after the compute capability of EKS Auto Mode is enabled. For more information, see the IAM Reference in the Amazon EKS User Guide.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Configure webhooks for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-webhooks.html#hybrid-nodes-considerations-mixed-mode

**Contents:**
- Configure webhooks for hybrid nodes
- Considerations for mixed mode clusters
- Configure mixed mode clusters
  - Configure Service Traffic Distribution
  - Configure CoreDNS replicas
  - Configure webhooks for add-ons
    - AWS Load Balancer Controller
    - CloudWatch Observability Agent
    - AWS Distro for OpenTelemetry (ADOT)
    - cert-manager

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This page details considerations for running webhooks with hybrid nodes. Webhooks are used in Kubernetes applications and open source projects, such as the AWS Load Balancer Controller and CloudWatch Observability Agent, to perform mutating and validation capabilities at runtime.

Routable pod networks

If you are able to make your on-premises pod CIDR routable on your on-premises network, you can run webhooks on hybrid nodes. There are several techniques you can use to make your on-premises pod CIDR routable on your on-premises network including Border Gateway Protocol (BGP), static routes, or other custom routing solutions. BGP is the recommended solution as it is more scalable and easier to manage than alternative solutions that require custom or manual route configuration. AWS supports the BGP capabilities of Cilium and Calico for advertising pod CIDRs, see Configure CNI for hybrid nodes and Routable remote Pod CIDRs for more information.

Unroutable pod networks

If you cannot make your on-premises pod CIDR routable on your on-premises network and need to run webhooks, we recommend that you run all webhooks on cloud nodes in the same EKS cluster as your hybrid nodes.

Mixed mode clusters are defined as EKS clusters that have both hybrid nodes and nodes running in AWS Cloud. When running a mixed mode cluster, consider the following recommendations:

Run the VPC CNI on nodes in AWS Cloud and either Cilium or Calico on hybrid nodes. Cilium and Calico are not supported by AWS when running on nodes in AWS Cloud.

Configure webhooks to run on nodes in AWS Cloud. See Configure webhooks for add-ons for how to configure the webhooks for AWS and community add-ons.

If your applications require pods running on nodes in AWS Cloud to directly communicate with pods running on hybrid nodes ("east-west communication"), and you are using the VPC CNI on nodes in AWS Cloud, and Cilium or Calico on hybrid nodes, then your on-premises pod CIDR must be routable on your on-premises network.

Run at least one replica of CoreDNS on nodes in AWS Cloud and at least one replica of CoreDNS on hybrid nodes.

Configure Service Traffic Distribution to keep Service traffic local to the zone it is originating from. For more information on Service Traffic Distribution, see Configure Service Traffic Distribution.

If you are using AWS Appli

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
kubectl get mutatingwebhookconfigurations
```

Example 2 (unknown):
```unknown
kubectl get validatingwebhookconfigurations
```

Example 3 (unknown):
```unknown
enable-service-topology
```

Example 4 (unknown):
```unknown
--set loadBalancer.serviceTopology=true
```

---

## Customize managed nodes with launch templates

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html

**Contents:**
- Customize managed nodes with launch templates
- Launch template configuration basics
        - Note
- Tagging Amazon EC2 instances
- Using custom security groups
- Amazon EC2 user data
        - Note
        - Important
        - Note
- Specifying an AMI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

For the highest level of customization, you can deploy managed nodes using your own launch template. Using a launch template allows capabilities such as the following:

Provide bootstrap arguments at deployment of a node, such as extra kubelet arguments.

Assign IP addresses to Pods from a different CIDR block than the IP address assigned to the node.

Deploy your own custom AMI to nodes.

Deploy your own custom CNI to nodes.

When you give your own launch template upon first creating a managed node group, you will also have greater flexibility later. As long as you deploy a managed node group with your own launch template, you can iteratively update it with a different version of the same launch template. When you update your node group to a different version of your launch template, all nodes in the group are recycled to match the new configuration of the specified launch template version.

Managed node groups are always deployed with a launch template to be used with the Amazon EC2 Auto Scaling group. When you don’t provide a launch template, the Amazon EKS API creates one automatically with default values in your account. However, we don’t recommend that you modify auto-generated launch templates. Furthermore, existing node groups that don’t use a custom launch template can’t be updated directly. Instead, you must create a new node group with a custom launch template to do so.

You can create an Amazon EC2 Auto Scaling launch template with the AWS Management Console, AWS CLI, or an AWS SDK. For more information, see Creating a Launch Template for an Auto Scaling group in the Amazon EC2 Auto Scaling User Guide. Some of the settings in a launch template are similar to the settings used for managed node configuration. When deploying or updating a node group with a launch template, some settings must be specified in either the node group configuration or the launch template. Don’t specify a setting in both places. If a setting exists where it shouldn’t, then operations such as creating or updating a node group fail.

The following table lists the settings that are prohibited in a launch template. It also lists similar settings, if any are available, that are required in the managed node group configuration. The listed settings are the settings that appear in the console. They might have similar but different n

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
bootstrap.sh
```

Example 2 (unknown):
```unknown
InstanceRequirements
```

Example 3 (unknown):
```unknown
TagSpecification
```

Example 4 (unknown):
```unknown
CreateNodegroup
```

---

## VpcConfigRequest

See the canonical [VpcConfigRequest API reference](https://docs.aws.amazon.com/eks/latest/APIReference/API_VpcConfigRequest.html) for complete details.

---

## Simplify compute management with AWS Fargate

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/fargate.html

**Contents:**
- Simplify compute management with AWS Fargate
- AWS Fargate considerations
- Fargate Comparison Table

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic discusses using Amazon EKS to run Kubernetes Pods on AWS Fargate. Fargate is a technology that provides on-demand, right-sized compute capacity for containers. With Fargate, you don’t have to provision, configure, or scale groups of virtual machines on your own to run containers. You also don’t need to choose server types, decide when to scale your node groups, or optimize cluster packing.

You can control which Pods start on Fargate and how they run with Fargate profiles. Fargate profiles are defined as part of your Amazon EKS cluster. Amazon EKS integrates Kubernetes with Fargate by using controllers that are built by AWS using the upstream, extensible model provided by Kubernetes. These controllers run as part of the Amazon EKS managed Kubernetes control plane and are responsible for scheduling native Kubernetes Pods onto Fargate. The Fargate controllers include a new scheduler that runs alongside the default Kubernetes scheduler in addition to several mutating and validating admission controllers. When you start a Pod that meets the criteria for running on Fargate, the Fargate controllers that are running in the cluster recognize, update, and schedule the Pod onto Fargate.

This topic describes the different components of Pods that run on Fargate, and calls out special considerations for using Fargate with Amazon EKS.

Here are some things to consider about using Fargate on Amazon EKS.

Each Pod that runs on Fargate has its own compute boundary. They don’t share the underlying kernel, CPU resources, memory resources, or elastic network interface with another Pod.

Network Load Balancers and Application Load Balancers (ALBs) can be used with Fargate with IP targets only. For more information, see Create a network load balancer and Route application and HTTP traffic with Application Load Balancers.

Fargate exposed services only run on target type IP mode, and not on node IP mode. The recommended way to check the connectivity from a service running on a managed node and a service running on Fargate is to connect via service name.

Pods must match a Fargate profile at the time that they’re scheduled to run on Fargate. Pods that don’t match a Fargate profile might be stuck as Pending. If a matching Fargate profile exists, you can delete pending Pods that you have created to reschedule them onto Farg

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
HostNetwork
```

Example 2 (unknown):
```unknown
.spec.ttlSecondsAfterFinished
```

Example 3 (unknown):
```unknown
apiVersion: batch/v1
kind: Job
metadata:
  name: busybox
spec:
  template:
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ["/bin/sh", "-c", "sleep 10"]
      restartPolicy: Never
  ttlSecondsAfterFinished: 60 # <-- TTL controller
```

Example 4 (unknown):
```unknown
HostNetwork
```

---

## Assign more IP addresses to Amazon EKS nodes with prefixes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html

**Contents:**
- Assign more IP addresses to Amazon EKS nodes with prefixes
- Compatibility with Amazon VPC CNI plugin for Kubernetes features
- Considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Applies to: Linux and Windows nodes with Amazon EC2 instances

Applies to: Public and private subnets

Each Amazon EC2 instance supports a maximum number of elastic network interfaces and a maximum number of IP addresses that can be assigned to each network interface. Each node requires one IP address for each network interface. All other available IP addresses can be assigned to Pods. Each Pod requires its own IP address. As a result, you might have nodes that have available compute and memory resources, but can’t accommodate additional Pods because the node has run out of IP addresses to assign to Pods.

You can increase the number of IP addresses that nodes can assign to Pods by assigning IP prefixes, rather than assigning individual secondary IP addresses to your nodes. Each prefix includes several IP addresses. If you don’t configure your cluster for IP prefix assignment, your cluster must make more Amazon EC2 application programming interface (API) calls to configure network interfaces and IP addresses necessary for Pod connectivity. As clusters grow to larger sizes, the frequency of these API calls can lead to longer Pod and instance launch times. This results in scaling delays to meet the demand of large and spiky workloads, and adds cost and management overhead because you need to provision additional clusters and VPCs to meet scaling requirements. For more information, see Kubernetes Scalability thresholds on GitHub.

You can use IP prefixes with the following features:

IPv4 Source Network Address Translation - For more information, see Enable outbound internet access for Pods.

IPv6 addresses to clusters, Pods, and services - For more information, see Learn about IPv6 addresses to clusters, Pods, and services.

Restricting traffic using Kubernetes network policies - For more information, see Limit Pod traffic with Kubernetes network policies.

The following list provides information about the Amazon VPC CNI plugin settings that apply. For more information about each setting, see amazon-vpc-cni-k8s on GitHub.

Consider the following when you use this feature:

Each Amazon EC2 instance type supports a maximum number of Pods. If your managed node group consists of multiple instance types, the smallest number of maximum Pods for an instance in the cluster is applied to all nodes in the cluster.

By def

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
WARM_IP_TARGET
```

Example 2 (unknown):
```unknown
MINIMUM_IP_TARGET
```

Example 3 (unknown):
```unknown
WARM_PREFIX_TARGET
```

Example 4 (unknown):
```unknown
POD_SECURITY_GROUP_ENFORCING_MODE
```

---

## Configure CNI for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-cni.html

**Contents:**
- Configure CNI for hybrid nodes
- Version compatibility
- Supported capabilities
- Cilium considerations
- Install Cilium on hybrid nodes
  - Procedure
- Upgrade Cilium on hybrid nodes
- Delete Cilium from hybrid nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Cilium is the AWS-supported Container Networking Interface (CNI) for Amazon EKS Hybrid Nodes. You must install a CNI for hybrid nodes to become ready to serve workloads. Hybrid nodes appear with status Not Ready until a CNI is running. You can manage the CNI with your choice of tools such as Helm. The instructions on this page cover Cilium lifecycle management (install, upgrade, delete). See Cilium Ingress and Cilium Gateway Overview, Service type LoadBalancer, and Configure Kubernetes Network Policies for hybrid nodes for how to configure Cilium for ingress, load balancing, and network policies.

Cilium is not supported by AWS when running on nodes in AWS Cloud. The Amazon VPC CNI is not compatible with hybrid nodes and the VPC CNI is configured with anti-affinity for the eks.amazonaws.com/compute-type: hybrid label.

The Calico documentation previously on this page has been moved to the EKS Hybrid Examples Repository.

Cilium version v1.17.x is supported for EKS Hybrid Nodes for every Kubernetes version supported in Amazon EKS.

See Kubernetes version support for the Kubernetes versions supported by Amazon EKS. EKS Hybrid Nodes have the same Kubernetes version support as Amazon EKS clusters with cloud nodes.

AWS maintains builds of Cilium for EKS Hybrid Nodes that are based on the open source Cilium project. To receive support from AWS for Cilium, you must be using the AWS-maintained Cilium builds and supported Cilium versions.

AWS provides technical support for the default configurations of the following capabilities of Cilium for use with EKS Hybrid Nodes. If you plan to use functionality outside the scope of AWS support, it is recommended to obtain alternative commercial support for Cilium or have the in-house expertise to troubleshoot and contribute fixes to the Cilium project.

Kubernetes network conformance

Core cluster connectivity

IP Address Management (IPAM)

Cilium IPAM Cluster Scope

Kubernetes Network Policy

Border Gateway Protocol (BGP)

Cilium BGP Control Plane

Cilium Ingress, Cilium Gateway

Service LoadBalancer IP Allocation

Cilium Load Balancer IPAM

Service LoadBalancer IP Address Advertisement

Cilium BGP Control Plane

kube-proxy replacement

Helm repository - AWS hosts the Cilium Helm chart in the Amazon Elastic Container Registry Public (Amazon ECR Public) at Amazon EKS Cilium/Ci

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks.amazonaws.com/compute-type: hybrid
```

Example 2 (unknown):
```unknown
oci://public.ecr.aws/eks/cilium/cilium:1.17.6-0
```

Example 3 (unknown):
```unknown
cilium-values.yaml
```

Example 4 (unknown):
```unknown
eks.amazonaws.com/compute-type: hybrid
```

---

## Prerequisite setup for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-prereqs.html

**Contents:**
- Prerequisite setup for hybrid nodes
- Hybrid network connectivity
- On-premises network configuration
- EKS cluster configuration
- VPC configuration
- Security group configuration
- Infrastructure
- Operating system
- On-premises IAM credentials provider

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To use Amazon EKS Hybrid Nodes, you must have private connectivity from your on-premises environment to/from AWS, bare metal servers or virtual machines with a supported operating system, and AWS IAM Roles Anywhere or AWS Systems Manager (SSM) hybrid activations configured. You are responsible for managing these prerequisites throughout the hybrid nodes lifecycle.

Hybrid network connectivity from your on-premises environment to/from AWS

Infrastructure in the form of physical or virtual machines

Operating system that is compatible with hybrid nodes

On-premises IAM credentials provider configured

The communication between the Amazon EKS control plane and hybrid nodes is routed through the VPC and subnets you pass during cluster creation, which builds on the existing mechanism in Amazon EKS for control plane to node networking. There are several documented options available for you to connect your on-premises environment with your VPC including AWS Site-to-Site VPN, AWS Direct Connect, or your own VPN connection. Reference the AWS Site-to-Site VPN and AWS Direct Connect user guides for more information on how to use those solutions for your hybrid network connection.

For an optimal experience, we recommend that you have reliable network connectivity of at least 100 Mbps and a maximum of 200ms round trip latency for the hybrid nodes connection to the AWS Region. This is general guidance that accommodates most use cases but is not a strict requirement. The bandwidth and latency requirements can vary depending on the number of hybrid nodes and your workload characteristics, such as application image size, application elasticity, monitoring and logging configurations, and application dependencies on accessing data stored in other AWS services. We recommend that you test with your own applications and environments before deploying to production to validate that your networking setup meets the requirements for your workloads.

You must enable inbound network access from the Amazon EKS control plane to your on-premises environment to allow the Amazon EKS control plane to communicate with the kubelet running on hybrid nodes and optionally with webhooks running on your hybrid nodes. Additionally, you must enable outbound network access for your hybrid nodes and components running on them to communicate with the Amaz

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
RemoteNodeNetwork
```

Example 2 (unknown):
```unknown
RemotePodNetwork
```

Example 3 (unknown):
```unknown
RemoteNodeNetwork
```

Example 4 (unknown):
```unknown
RemotePodNetwork
```

---

## ComputeConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigRequest.html#AmazonEKS-Type-ComputeConfigRequest-nodePools

**Contents:**
- ComputeConfigRequest
- Contents
- See Also

Request to update the configuration of the compute capability of your EKS Auto Mode cluster. For example, enable the capability. For more information, see EKS Auto Mode compute capability in the Amazon EKS User Guide.

Request to enable or disable the compute capability on your EKS Auto Mode cluster. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account.

Configuration for node pools that defines the compute resources for your EKS Auto Mode cluster. For more information, see EKS Auto Mode Node Pools in the Amazon EKS User Guide.

Type: Array of strings

The ARN of the IAM Role EKS will assign to EC2 Managed Instances in your EKS Auto Mode cluster. This value cannot be changed after the compute capability of EKS Auto Mode is enabled. For more information, see the IAM Reference in the Amazon EKS User Guide.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Amazon EKS node IAM role

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html

**Contents:**
- Amazon EKS node IAM role
        - Note
        - Note
- Check for an existing node role
        - Note
- Creating the Amazon EKS node IAM role

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon EKS node kubelet daemon makes calls to AWS APIs on your behalf. Nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch nodes and register them into a cluster, you must create an IAM role for those nodes to use when they are launched. This requirement applies to nodes launched with the Amazon EKS optimized AMI provided by Amazon, or with any other node AMIs that you intend to use. Additionally, this requirement applies to both managed node groups and self-managed nodes.

You can’t use the same role that is used to create any clusters.

Before you create nodes, you must create an IAM role with the following permissions:

Permissions for the kubelet to describe Amazon EC2 resources in the VPC, such as provided by the AmazonEKSWorkerNodePolicy policy. This policy also provides the permissions for the Amazon EKS Pod Identity Agent.

Permissions for the kubelet to use container images from Amazon Elastic Container Registry (Amazon ECR), such as provided by the AmazonEC2ContainerRegistryPullOnly policy. The permissions to use container images from Amazon Elastic Container Registry (Amazon ECR) are required because the built-in add-ons for networking run pods that use container images from Amazon ECR.

(Optional) Permissions for the Amazon EKS Pod Identity Agent to use the eks-auth:AssumeRoleForPodIdentity action to retrieve credentials for pods. If you don’t use the AmazonEKSWorkerNodePolicy, then you must provide this permission in addition to the EC2 permissions to use EKS Pod Identity.

(Optional) If you don’t use IRSA or EKS Pod Identity to give permissions to the VPC CNI pods, then you must provide permissions for the VPC CNI on the instance role. You can use either the AmazonEKS_CNI_Policy managed policy (if you created your cluster with the IPv4 family) or an IPv6 policy that you create (if you created your cluster with the IPv6 family). Rather than attaching the policy to this role however, we recommend that you attach the policy to a separate role used specifically for the Amazon VPC CNI add-on. For more information about creating a separate role for the Amazon VPC CNI add-on, see Configure Amazon VPC CNI plugin to use IRSA.

The Amazon EC2 node groups must have a different IAM role than the Fargate profile. For more information

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-auth:AssumeRoleForPodIdentity
```

Example 2 (unknown):
```unknown
AmazonEKS_CNI_Policy
```

Example 3 (unknown):
```unknown
eksNodeRole
```

Example 4 (unknown):
```unknown
AmazonEKSNodeRole
```

---

## Migrate from EKS Managed Node Groups to EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/auto-migrate-mng.html

**Contents:**
- Migrate from EKS Managed Node Groups to EKS Auto Mode
- Prerequisites
- Procedure

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When transitioning your Amazon EKS cluster to use EKS auto mode, you can smoothly migrate your existing workloads from managed node groups (MNGs) using the eksctl CLI tool. This process ensures continuous application availability while EKS auto mode optimizes your compute resources. The migration can be performed with minimal disruption to your running applications.

This topic walks you through the steps to safely drain pods from your existing managed node groups and allow EKS auto mode to reschedule them on newly provisioned instances. By following this procedure, you can take advantage of EKS auto mode’s intelligent workload consolidation while maintaining your application’s availability throughout the migration.

Cluster with EKS Auto Mode enabled

eksctl CLI installed and connected to your cluster. For more information, see Set up to use Amazon EKS.

Karpenter is not installed on the cluster.

Use the following eksctl CLI command to initiate draining pods from the existing managed node group instances. EKS Auto Mode will create new nodes to back the displaced pods.

You will need to run this command for each managed node group in your cluster.

For more information on this command, see Deleting and draining nodegroups in the eksctl docs.

**Examples:**

Example 1 (unknown):
```unknown
eksctl delete nodegroup --cluster=<clusterName> --name=<nodegroupName>
```

---

## Prepare networking for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-networking.html

**Contents:**
- Prepare networking for hybrid nodes
- On-premises networking configuration
  - Minimum network requirements
  - On-premises node and pod CIDRs
  - On-premises pod network routing
  - Access required during hybrid node installation and upgrade
        - Note
  - Access required for ongoing cluster operations
        - Important
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic provides an overview of the networking setup you must have configured before creating your Amazon EKS cluster and attaching hybrid nodes. This guide assumes you have met the prerequisite requirements for hybrid network connectivity using AWS Site-to-Site VPN, AWS Direct Connect, or your own VPN solution.

For an optimal experience, we recommend that you have reliable network connectivity of at least 100 Mbps and a maximum of 200ms round trip latency for the hybrid nodes connection to the AWS Region. This is general guidance that accommodates most use cases but is not a strict requirement. The bandwidth and latency requirements can vary depending on the number of hybrid nodes and your workload characteristics, such as application image size, application elasticity, monitoring and logging configurations, and application dependencies on accessing data stored in other AWS services. We recommend that you test with your own applications and environments before deploying to production to validate that your networking setup meets the requirements for your workloads.

Identify the node and pod CIDRs you will use for your hybrid nodes and the workloads running on them. The node CIDR is allocated from your on-premises network and the pod CIDR is allocated from your Container Network Interface (CNI) if you are using an overlay network for your CNI. You pass your on-premises node CIDRs and pod CIDRs as inputs when you create your EKS cluster with the RemoteNodeNetwork and RemotePodNetwork fields. Your on-premises node CIDRs must be routable on your on-premises network. See the following section for information on the on-premises pod CIDR routability.

The on-premises node and pod CIDR blocks must meet the following requirements:

Be within one of the following IPv4 RFC-1918 ranges: 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16.

Not overlap with each other, the VPC CIDR for your EKS cluster, or your Kubernetes service IPv4 CIDR.

When using EKS Hybrid Nodes, we generally recommend that you make your on-premises pod CIDRs routable on your on-premises network to enable full cluster communication and functionality between cloud and on-premises environments.

Routable pod networks

If you are able to make your pod network routable on your on-premises network, follow the guidance below.

Configure the RemotePodNetwork

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
RemoteNodeNetwork
```

Example 2 (unknown):
```unknown
RemotePodNetwork
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

## Delete a Fargate profile

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/delete-fargate-profile.html

**Contents:**
- Delete a Fargate profile
- eksctl
- AWS Management Console
- AWS CLI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how to delete a Fargate profile. When you delete a Fargate profile, any Pods that were scheduled onto Fargate with the profile are deleted. If those Pods match another Fargate profile, then they’re scheduled on Fargate with that profile. If they no longer match any Fargate profiles, then they aren’t scheduled onto Fargate and might remain as pending.

Only one Fargate profile in a cluster can be in the DELETING status at a time. Wait for a Fargate profile to finish deleting before you can delete any other profiles in that cluster.

You can delete a profile with any of the following tools:

AWS Management Console

Delete a Fargate profile with eksctl

Use the following command to delete a profile from a cluster. Replace every example value with your own values.

Delete a Fargate profile with AWS Management Console

Open the Amazon EKS console.

In the left navigation pane, choose Clusters. In the list of clusters, choose the cluster that you want to delete the Fargate profile from.

Choose the Compute tab.

Choose the Fargate profile to delete, and then choose Delete.

On the Delete Fargate profile page, enter the name of the profile, and then choose Delete.

Delete a Fargate profile with AWS CLI

Use the following command to delete a profile from a cluster. Replace every example value with your own values.

**Examples:**

Example 1 (unknown):
```unknown
example value
```

Example 2 (unknown):
```unknown
eksctl delete fargateprofile  --name my-profile --cluster my-cluster
```

Example 3 (unknown):
```unknown
example value
```

Example 4 (unknown):
```unknown
aws eks delete-fargate-profile --fargate-profile-name my-profile --cluster-name my-cluster
```

---

## Create nodes with optimized Bottlerocket AMIs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami-bottlerocket.html

**Contents:**
- Create nodes with optimized Bottlerocket AMIs
- Advantages
- Considerations
- More information

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Bottlerocket is an open source Linux distribution that’s sponsored and supported by AWS. Bottlerocket is purpose-built for hosting container workloads. With Bottlerocket, you can improve the availability of containerized deployments and reduce operational costs by automating updates to your container infrastructure. Bottlerocket includes only the essential software to run containers, which improves resource usage, reduces security threats, and lowers management overhead. The Bottlerocket AMI includes containerd, kubelet, and AWS IAM Authenticator. In addition to managed node groups and self-managed nodes, Bottlerocket is also supported by Karpenter.

Using Bottlerocket with your Amazon EKS cluster has the following advantages:

Higher uptime with lower operational cost and lower management complexity – Bottlerocket has a smaller resource footprint, shorter boot times, and is less vulnerable to security threats than other Linux distributions. Bottlerocket’s smaller footprint helps to reduce costs by using less storage, compute, and networking resources.

Improved security from automatic OS updates – Updates to Bottlerocket are applied as a single unit which can be rolled back, if necessary. This removes the risk of corrupted or failed updates that can leave the system in an unusable state. With Bottlerocket, security updates can be automatically applied as soon as they’re available in a minimally disruptive manner and be rolled back if failures occur.

Premium support – AWS provided builds of Bottlerocket on Amazon EC2 is covered under the same AWS Support plans that also cover AWS services such as Amazon EC2, Amazon EKS, and Amazon ECR.

Consider the following when using Bottlerocket for your AMI type:

Bottlerocket supports Amazon EC2 instances with x86_64 and arm64 processors.

Bottlerocket supports Amazon EC2 instances with GPUs. For more information, see Use EKS-optimized accelerated AMIs for GPU instances.

Bottlerocket images don’t include an SSH server or a shell. You can employ out-of-band access methods to allow SSH. These approaches enable the admin container and to pass some bootstrapping configuration steps with user data. For more information, refer to the following sections in Bottlerocket OS on GitHub:

Bottlerocket uses different container types:

By default, a control container is enabled. Thi

*[Content truncated]*

---

## Create a Node Class for Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-node-class.html

**Contents:**
- Create a Node Class for Amazon EKS
- Create a Node Class
  - Basic Node Class Example
- Create node class access entry
  - Create access entry with CLI
  - Create access entry with CloudFormation
- Node Class Specification
- Considerations
- Subnet selection for Pods
  - Use cases

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS Node Classes are templates that offer granular control over the configuration of your EKS Auto Mode managed nodes. A Node Class defines infrastructure-level settings that apply to groups of nodes in your EKS cluster, including network configuration, storage settings, and resource tagging. This topic explains how to create and configure a Node Class to meet your specific operational requirements.

When you need to customize how EKS Auto Mode provisions and configures EC2 instances beyond the default settings, creating a Node Class gives you precise control over critical infrastructure parameters. For example, you can specify private subnet placement for enhanced security, configure instance ephemeral storage for performance-sensitive workloads, or apply custom tagging for cost allocation.

To create a NodeClass, follow these steps:

Create a YAML file (for example, nodeclass.yaml) with your Node Class configuration

Apply the configuration to your cluster using kubectl

Reference the Node Class in your Node Pool configuration. For more information, see Create a Node Pool for EKS Auto Mode.

You need kubectl installed and configured. For more information, see Set up to use Amazon EKS.

Here’s an example Node Class:

This NodeClass increases the amount of ephemeral storage on the node.

Apply this configuration by using:

Next, reference the Node Class in your Node Pool configuration. For more information, see Create a Node Pool for EKS Auto Mode.

If you create a custom node class, you need to create an EKS Access Entry to permit the nodes to join the cluster. EKS automatically creates access entries when you use the built-in node class and node pools.

For information about how Access Entries work, see Grant IAM users access to Kubernetes with EKS access entries.

When creating access entries for EKS Auto Mode node classes, you need to use the EC2 access entry type.

To create an access entry for EC2 nodes and associate the EKS Auto Node Policy:

Update the following CLI commands with your cluster name, and node role ARN. The node role ARN is specified in the node class YAML.

To create an access entry for EC2 nodes and associate the EKS Auto Node Policy:

Update the following CloudFormation with your cluster name, and node role ARN. The node role ARN is specified in the node class YAML.

For informa

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
nodeclass.yaml
```

Example 2 (unknown):
```unknown
apiVersion: eks.amazonaws.com/v1
kind: NodeClass
metadata:
  name: private-compute
spec:
  subnetSelectorTerms:
    - tags:
        Name: "private-subnet"
        kubernetes.io/role/internal-elb: "1"
  securityGroupSelectorTerms:
    - tags:
        Name: "eks-cluster-sg"
  ephemeralStorage:
    size: "160Gi"
```

Example 3 (unknown):
```unknown
kubectl apply -f nodeclass.yaml
```

Example 4 (unknown):
```unknown
# Create the access entry for EC2 nodes
aws eks create-access-entry \
  --cluster-name <cluster-name> \
  --principal-arn <node-role-arn> \
  --type EC2

# Associate the auto node policy
aws eks associate-access-policy \
  --cluster-name <cluster-name> \
  --principal-arn <node-role-arn> \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSAutoNodePolicy \
  --access-scope type=cluster
```

---

## Configure webhooks for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-webhooks.html

**Contents:**
- Configure webhooks for hybrid nodes
- Considerations for mixed mode clusters
- Configure mixed mode clusters
  - Configure Service Traffic Distribution
  - Configure CoreDNS replicas
  - Configure webhooks for add-ons
    - AWS Load Balancer Controller
    - CloudWatch Observability Agent
    - AWS Distro for OpenTelemetry (ADOT)
    - cert-manager

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This page details considerations for running webhooks with hybrid nodes. Webhooks are used in Kubernetes applications and open source projects, such as the AWS Load Balancer Controller and CloudWatch Observability Agent, to perform mutating and validation capabilities at runtime.

Routable pod networks

If you are able to make your on-premises pod CIDR routable on your on-premises network, you can run webhooks on hybrid nodes. There are several techniques you can use to make your on-premises pod CIDR routable on your on-premises network including Border Gateway Protocol (BGP), static routes, or other custom routing solutions. BGP is the recommended solution as it is more scalable and easier to manage than alternative solutions that require custom or manual route configuration. AWS supports the BGP capabilities of Cilium and Calico for advertising pod CIDRs, see Configure CNI for hybrid nodes and Routable remote Pod CIDRs for more information.

Unroutable pod networks

If you cannot make your on-premises pod CIDR routable on your on-premises network and need to run webhooks, we recommend that you run all webhooks on cloud nodes in the same EKS cluster as your hybrid nodes.

Mixed mode clusters are defined as EKS clusters that have both hybrid nodes and nodes running in AWS Cloud. When running a mixed mode cluster, consider the following recommendations:

Run the VPC CNI on nodes in AWS Cloud and either Cilium or Calico on hybrid nodes. Cilium and Calico are not supported by AWS when running on nodes in AWS Cloud.

Configure webhooks to run on nodes in AWS Cloud. See Configure webhooks for add-ons for how to configure the webhooks for AWS and community add-ons.

If your applications require pods running on nodes in AWS Cloud to directly communicate with pods running on hybrid nodes ("east-west communication"), and you are using the VPC CNI on nodes in AWS Cloud, and Cilium or Calico on hybrid nodes, then your on-premises pod CIDR must be routable on your on-premises network.

Run at least one replica of CoreDNS on nodes in AWS Cloud and at least one replica of CoreDNS on hybrid nodes.

Configure Service Traffic Distribution to keep Service traffic local to the zone it is originating from. For more information on Service Traffic Distribution, see Configure Service Traffic Distribution.

If you are using AWS Appli

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
kubectl get mutatingwebhookconfigurations
```

Example 2 (unknown):
```unknown
kubectl get validatingwebhookconfigurations
```

Example 3 (unknown):
```unknown
enable-service-topology
```

Example 4 (unknown):
```unknown
--set loadBalancer.serviceTopology=true
```

---

## Create nodes with optimized Windows AMIs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-windows-ami.html#bootstrap-script-configuration-parameters

**Contents:**
- Create nodes with optimized Windows AMIs
        - Note
        - Important
- Release calendar
- Bootstrap script configuration parameters
  - gMSA authentication support
- Cached container images
- More information

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Windows Amazon EKS optimized AMIs are built on top of Windows Server 2019 and Windows Server 2022. They are configured to serve as the base image for Amazon EKS nodes. By default, the AMIs include the following components:

AWS IAM Authenticator for Kubernetes

You can track security or privacy events for Windows Server with the Microsoft security update guide.

Amazon EKS offers AMIs that are optimized for Windows containers in the following variants:

Amazon EKS-optimized Windows Server 2019 Core AMI

Amazon EKS-optimized Windows Server 2019 Full AMI

Amazon EKS-optimized Windows Server 2022 Core AMI

Amazon EKS-optimized Windows Server 2022 Full AMI

The Amazon EKS-optimized Windows Server 20H2 Core AMI is deprecated. No new versions of this AMI will be released.

To ensure that you have the latest security updates by default, Amazon EKS maintains optimized Windows AMIs for the last 4 months. Each new AMI will be available for 4 months from the time of initial release. After this period, older AMIs are made private and are no longer accessible. We encourage using the latest AMIs to avoid security vulnerabilities and losing access to older AMIs which have reached the end of their supported lifetime. While we can’t guarantee that we can provide access to AMIs that have been made private, you can request access by filing a ticket with AWS Support.

The following table lists the release and end of support dates for Windows versions on Amazon EKS. If an end date is blank, it’s because the version is still supported.

Windows Server 2022 Core

Windows Server 2022 Full

Windows Server 20H2 Core

Windows Server 2004 Core

Windows Server 2019 Core

Windows Server 2019 Full

Windows Server 1909 Core

When you create a Windows node, there’s a script on the node that allows for configuring different parameters. Depending on your setup, this script can be found on the node at a location similar to: C:\Program Files\Amazon\EKS\Start-EKSBootstrap.ps1. You can specify custom parameter values by specifying them as arguments to the bootstrap script. For example, you can update the user data in the launch template. For more information, see Amazon EC2 user data.

The script includes the following command-line parameters:

-EKSClusterName – Specifies the Amazon EKS cluster name for this worker node to join.

-KubeletExtraArgs 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
C:\Program Files\Amazon\EKS\Start-EKSBootstrap.ps1
```

Example 2 (unknown):
```unknown
-EKSClusterName
```

Example 3 (unknown):
```unknown
-KubeletExtraArgs
```

Example 4 (unknown):
```unknown
-KubeProxyExtraArgs
```

---

## CreateNodegroup

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateNodegroup.html

**Contents:**
- CreateNodegroup
        - Note
- Request Syntax
- URI Request Parameters
- Request Body
- Response Syntax
- Response Elements
- Errors
- Examples
  - Example 1

Creates a managed node group for an Amazon EKS cluster.

You can only create a node group for your cluster that is equal to the current Kubernetes version for the cluster. All node groups are created with the latest AMI release version for the respective minor Kubernetes version of the cluster, unless you deploy a custom AMI using a launch template.

For later updates, you will only be able to update a node group using a launch template only if it was originally deployed with a launch template. Additionally, the launch template ID or name must match what was used when the node group was created. You can update the launch template version with necessary changes. For more information about using launch templates, see Customizing managed nodes with launch templates.

An Amazon EKS managed node group is an Amazon EC2 Auto Scaling group and associated Amazon EC2 instances that are managed by AWS for an Amazon EKS cluster. For more information, see Managed node groups in the Amazon EKS User Guide.

Windows AMI types are supported in all public AWS Regions and the AWS GovCloud (US) Regions.

The request uses the following URI parameters.

The name of your cluster.

The request accepts the following data in JSON format.

The AMI type for your node group. If you specify launchTemplate, and your launch template uses a custom AMI, then don't specify amiType, or the node group deployment will fail. If your launch template uses a Windows custom AMI, then add eks:kube-proxy-windows to your Windows nodes rolearn in the aws-auth ConfigMap. For more information about using launch templates with Amazon EKS, see Customizing managed nodes with launch templates in the Amazon EKS User Guide.

Valid Values: AL2_x86_64 | AL2_x86_64_GPU | AL2_ARM_64 | CUSTOM | BOTTLEROCKET_ARM_64 | BOTTLEROCKET_x86_64 | BOTTLEROCKET_ARM_64_FIPS | BOTTLEROCKET_x86_64_FIPS | BOTTLEROCKET_ARM_64_NVIDIA | BOTTLEROCKET_x86_64_NVIDIA | WINDOWS_CORE_2019_x86_64 | WINDOWS_FULL_2019_x86_64 | WINDOWS_CORE_2022_x86_64 | WINDOWS_FULL_2022_x86_64 | AL2023_x86_64_STANDARD | AL2023_ARM_64_STANDARD | AL2023_x86_64_NEURON | AL2023_x86_64_NVIDIA | AL2023_ARM_64_NVIDIA

The capacity type for your node group.

Valid Values: ON_DEMAND | SPOT | CAPACITY_BLOCK

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

The root device disk size (in GiB) for your node group instances. The default disk size is 20 GiB for Linux and Bottlerocket. The default disk size is 50 GiB fo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
POST /clusters/name/node-groups HTTP/1.1
Content-type: application/json

{
   "amiType": "string",
   "capacityType": "string",
   "clientRequestToken": "string",
   "diskSize": number,
   "instanceTypes": [ "string" ],
   "labels": {
      "string" : "string"
   },
   "launchTemplate": {
      "id": "string",
      "name": "string",
      "version": "string"
   },
   "nodegroupName": "string",
   "nodeRepairConfig": {
      "enabled": boolean,
      "maxParallelNodesRepairedCount": number,
      "maxParallelNodesRepairedPercentage": number,
      "maxUnhealthyNodeThresholdCount": number,
    
...
```

Example 2 (unknown):
```unknown
launchTemplate
```

Example 3 (unknown):
```unknown
eks:kube-proxy-windows
```

Example 4 (unknown):
```unknown
AL2_x86_64 | AL2_x86_64_GPU | AL2_ARM_64 | CUSTOM | BOTTLEROCKET_ARM_64 | BOTTLEROCKET_x86_64 | BOTTLEROCKET_ARM_64_FIPS | BOTTLEROCKET_x86_64_FIPS | BOTTLEROCKET_ARM_64_NVIDIA | BOTTLEROCKET_x86_64_NVIDIA | WINDOWS_CORE_2019_x86_64 | WINDOWS_FULL_2019_x86_64 | WINDOWS_CORE_2022_x86_64 | WINDOWS_FULL_2022_x86_64 | AL2023_x86_64_STANDARD | AL2023_ARM_64_STANDARD | AL2023_x86_64_NEURON | AL2023_x86_64_NVIDIA | AL2023_ARM_64_NVIDIA
```

---

## CreateFargateProfile

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateFargateProfile.html

**Contents:**
- CreateFargateProfile
- Request Syntax
- URI Request Parameters
- Request Body
- Response Syntax
- Response Elements
- Errors
- Examples
  - Example
    - Sample Request

Creates an AWS Fargate profile for your Amazon EKS cluster. You must have at least one Fargate profile in a cluster to be able to run pods on Fargate.

The Fargate profile allows an administrator to declare which pods run on Fargate and specify which pods run on which Fargate profile. This declaration is done through the profile's selectors. Each profile can have up to five selectors that contain a namespace and labels. A namespace is required for every selector. The label field consists of multiple optional key-value pairs. Pods that match the selectors are scheduled on Fargate. If a to-be-scheduled pod matches any of the selectors in the Fargate profile, then that pod is run on Fargate.

When you create a Fargate profile, you must specify a pod execution role to use with the pods that are scheduled with the profile. This role is added to the cluster's Kubernetes Role Based Access Control (RBAC) for authorization so that the kubelet that is running on the Fargate infrastructure can register with your Amazon EKS cluster so that it can appear in your cluster as a node. The pod execution role also provides IAM permissions to the Fargate infrastructure to allow read access to Amazon ECR image repositories. For more information, see Pod Execution Role in the Amazon EKS User Guide.

Fargate profiles are immutable. However, you can create a new updated profile to replace an existing profile and then delete the original after the updated profile has finished creating.

If any Fargate profiles in a cluster are in the DELETING status, you must wait for that Fargate profile to finish deleting before you can create any other profiles in that cluster.

For more information, see AWS Fargate profile in the Amazon EKS User Guide.

The request uses the following URI parameters.

The name of your cluster.

The request accepts the following data in JSON format.

A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

The name of the Fargate profile.

The Amazon Resource Name (ARN) of the Pod execution role to use for a Pod that matches the selectors in the Fargate profile. The Pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. For more information, see Pod execution role in the Amazon EKS User Guide.

The selectors to match for a Pod to use this Fargate profile. Each selector must have an associated Kubernetes namespace. Optionally, yo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
POST /clusters/name/fargate-profiles HTTP/1.1
Content-type: application/json

{
   "clientRequestToken": "string",
   "fargateProfileName": "string",
   "podExecutionRoleArn": "string",
   "selectors": [
      {
         "labels": {
            "string" : "string"
         },
         "namespace": "string"
      }
   ],
   "subnets": [ "string" ],
   "tags": {
      "string" : "string"
   }
}
```

Example 2 (unknown):
```unknown
HTTP/1.1 200
Content-type: application/json

{
   "fargateProfile": {
      "clusterName": "string",
      "createdAt": number,
      "fargateProfileArn": "string",
      "fargateProfileName": "string",
      "health": {
         "issues": [
            {
               "code": "string",
               "message": "string",
               "resourceIds": [ "string" ]
            }
         ]
      },
      "podExecutionRoleArn": "string",
      "selectors": [
         {
            "labels": {
               "string" : "string"
            },
            "namespace": "string"
         }
      ],
...
```

Example 3 (unknown):
```unknown
default-with-infrastructure-label
```

Example 4 (unknown):
```unknown
"infrastructure": "fargate"
```

---

## Enable node auto repair and investigate node health issues

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/node-health.html

**Contents:**
- Enable node auto repair and investigate node health issues
        - Important
- Node monitoring agent
- Node auto repair
- Node health issues
  - AcceleratedHardware node health issues
  - ContainerRuntime node health issues
  - Kernel node health issues
  - Networking node health issues
  - Storage node health issues

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Node health refers to the operational status and capability of a node to effectively run workloads. A healthy node maintains expected connectivity, has sufficient resources, and can successfully run Pods without disruption. For information on getting details about your nodes, see View the health status of your nodes and Retrieve node logs for a managed node using kubectl and S3.

To help with maintaining healthy nodes, Amazon EKS offers the node monitoring agent and node auto repair.

The node monitoring agent and node auto repair are only available on Linux. These features aren’t available on Windows.

The node monitoring agent automatically reads node logs to detect certain health issues. It parses through node logs to detect failures and surfaces various status information about worker nodes. A dedicated NodeCondition is applied on the worker nodes for each category of issues detected, such as storage and networking issues. Descriptions of detected health issues are made available in the observability dashboard. For more information, see Node health issues.

The node monitoring agent is included as a capability for all Amazon EKS Auto Mode clusters. For other cluster types, you can add the monitoring agent as an Amazon EKS add-on. For more information, see Create an Amazon EKS add-on.

Node auto repair is an additional feature that continuously monitors the health of nodes, automatically reacting to detected problems and replacing nodes when possible. This helps overall availability of the cluster with minimal manual intervention. If a health check fails, the node is automatically cordoned so that no new Pods are scheduled on the node.

By itself, node auto repair can react to the Ready condition of the kubelet and any node objects that are manually deleted. When paired with the node monitoring agent, node auto repair can react to more conditions that wouldn’t be detected otherwise. These additional conditions include KernelReady, NetworkingReady, and StorageReady.

This automated node recovery automatically addresses intermittent node issues such as failures to join the cluster, unresponsive kubelets, and increased accelerator (device) errors. The improved reliability helps reduce application downtime and improve cluster operations. Node auto repair cannot handle certain problems that are reported such as 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
NodeCondition
```

Example 2 (unknown):
```unknown
KernelReady
```

Example 3 (unknown):
```unknown
NetworkingReady
```

Example 4 (unknown):
```unknown
StorageReady
```

---

## RemoteNodeNetwork

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_RemoteNodeNetwork.html#AmazonEKS-Type-RemoteNodeNetwork-cidrs

**Contents:**
- RemoteNodeNetwork
- Contents
- See Also

A network CIDR that can contain hybrid nodes.

These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator.

Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, 10.2.0.0/16).

It must satisfy the following requirements:

Each block must be within an IPv4 RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.

Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway, AWS Site-to-Site VPN, or AWS Direct Connect.

Each host must allow outbound connection to the EKS cluster control plane on TCP ports 443 and 10250.

Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations.

Each host must allow TCP and UDP network connectivity to and from other hosts that are running CoreDNS on UDP port 53 for service and pod DNS names.

A network CIDR that can contain hybrid nodes.

These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator.

Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, 10.2.0.0/16).

It must satisfy the following requirements:

Each block must be within an IPv4 RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.

Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway, AWS Site-to-Site VPN, or AWS Direct Connect.

Each host must allow outbound connection to the EKS cluster control plane on TCP ports 443 and 10250.

Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations.

Each host must allow TCP and UDP network connectivity to and from other hosts that are running CoreDNS on UDP port 53 for service and pod DNS names.

Ty

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
 10.2.0.0/16
```

Example 2 (unknown):
```unknown
 10.2.0.0/16
```

---

## Prepare operating system for hybrid nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-os.html

**Contents:**
- Prepare operating system for hybrid nodes
- Version compatibility
- Operating system considerations
  - General
  - Bottlerocket
  - Containerd
  - Ubuntu
  - ARM
- Building operating system images
  - Prerequisites

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Bottlerocket, Amazon Linux 2023 (AL2023), Ubuntu, and RHEL are validated on an ongoing basis for use as the node operating system for hybrid nodes. Bottlerocket is supported by AWSin VMware vSphere environments only. AL2023 is not covered by AWS Support Plans when run outside of Amazon EC2. AL2023 can only be used in on-premises virtualized environments, see the Amazon Linux 2023 User Guide for more information. AWS supports the hybrid nodes integration with Ubuntu and RHEL operating systems but does not provide support for the operating system itself.

You are responsible for operating system provisioning and management. When you are testing hybrid nodes for the first time, it is easiest to run the Amazon EKS Hybrid Nodes CLI (nodeadm) on an already provisioned host. For production deployments, we recommend that you include nodeadm in your operating system images with it configured to run as a systemd service to automatically join hosts to Amazon EKS clusters at host startup. If you are using Bottlerocket as your node operating system on vSphere, you do not need to use nodeadm as Bottlerocket already contains the dependencies required for hybrid nodes and will automatically connect to the cluster you configure upon host startup.

The table below represents the operating system versions that are compatible and validated to use as the node operating system for hybrid nodes. If you are using other operating system variants or versions that are not included in this table, then the compatibility of hybrid nodes with your operating system variant or version is not covered by AWS Support. Hybrid nodes are agnostic to the underlying infrastructure and support x86 and ARM architectures.

Amazon Linux 2023 (AL2023)

v1.37.0 and above VMware variants running Kubernetes v1.28 and above

Ubuntu 20.04, Ubuntu 22.04, Ubuntu 24.04

Red Hat Enterprise Linux

The Amazon EKS Hybrid Nodes CLI (nodeadm) can be used to simplify the installation and configuration of the hybrid nodes components and dependencies. You can run the nodeadm install process during your operating system image build pipelines or at runtime on each on-premises host. For more information on the components that nodeadm installs, see the Hybrid nodes nodeadm reference.

If you are using a proxy in your on-premises environment to reach the internet, there is add

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
nodeadm install
```

Example 2 (unknown):
```unknown
nodeadm install
```

Example 3 (unknown):
```unknown
nodeadm install
```

Example 4 (unknown):
```unknown
--containerd-source
```

---

## Enable or Disable Built-in NodePools

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/set-builtin-node-pools.html

**Contents:**
- Enable or Disable Built-in NodePools
- Built-in NodePool Reference
        - Note
- Procedure
  - Prerequisites
  - Enable with AWS CLI
  - Disable with AWS CLI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

EKS Auto Mode has two built-in NodePools. You can enable or disable these NodePools using the AWS console, CLI, or API.

This NodePool has a CriticalAddonsOnly taint. Many EKS add-ons, such as CoreDNS, tolerate this taint. Use this system node pool to separate cluster-critical applications.

Supports both amd64 and arm64 architectures.

This NodePool provides support for launching nodes for general purpose workloads in your cluster.

Uses only amd64 architecture.

Both built-in NodePools:

Use the default EKS NodeClass

Use only on-demand EC2 capacity

Use the C, M, and R EC2 instance families

Require generation 5 or newer EC2 instances

Enabling at least one built-in NodePool is required for EKS to provision the "default" NodeClass. If you disable all built-in NodePools, you’ll need to create a custom NodeClass and configure a NodePool to use it. For more information about NodeClasses, see Create a Node Class for Amazon EKS.

The latest version of the AWS Command Line Interface (AWS CLI) installed and configured on your device. To check your current version, use aws --version. To install the latest version, see Installing and Quick configuration with aws configure in the AWS Command Line Interface User Guide.

Login to the CLI with sufficent IAM permissions to create AWS resources including IAM Policies, IAM Roles, and EKS Clusters.

Use the following command to enable both built-in NodePools:

You can modify the command to selectively enable the NodePools.

Use the following command to disable both built-in NodePools:

**Examples:**

Example 1 (unknown):
```unknown
CriticalAddonsOnly
```

Example 2 (unknown):
```unknown
general-purpose
```

Example 3 (unknown):
```unknown
aws --version
```

Example 4 (unknown):
```unknown
aws eks update-cluster-config \
  --name <cluster-name> \
  --compute-config '{
    "nodeRoleArn": "<node-role-arn>",
    "nodePools": ["general-purpose", "system"],
    "enabled": true
  }' \
  --kubernetes-network-config '{
  "elasticLoadBalancing":{"enabled": true}
  }' \
  --storage-config '{
  "blockStorage":{"enabled": true}
  }'
```

---

## Create self-managed Bottlerocket nodes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/launch-node-bottlerocket.html

**Contents:**
- Create self-managed Bottlerocket nodes
        - Note
        - Important
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Managed node groups might offer some advantages for your use case. For more information, see Simplify node lifecycle with managed node groups.

This topic describes how to launch Auto Scaling groups of Bottlerocket nodes that register with your Amazon EKS cluster. Bottlerocket is a Linux-based open-source operating system from AWS that you can use for running containers on virtual machines or bare metal hosts. After the nodes join the cluster, you can deploy Kubernetes applications to them. For more information about Bottlerocket, see Using a Bottlerocket AMI with Amazon EKS on GitHub and Custom AMI support in the eksctl documentation.

For information about in-place upgrades, see Bottlerocket Update Operator on GitHub.

Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices. For more information, see Amazon EC2 pricing.

You can launch Bottlerocket nodes in Amazon EKS extended clusters on AWS Outposts, but you can’t launch them in local clusters on AWS Outposts. For more information, see Deploy Amazon EKS on-premises with AWS Outposts.

You can deploy to Amazon EC2 instances with x86 or Arm processors. However, you can’t deploy to instances that have Inferentia chips.

Bottlerocket is compatible with AWS CloudFormation. However, there is no official CloudFormation template that can be copied to deploy Bottlerocket nodes for Amazon EKS.

Bottlerocket images don’t come with an SSH server or a shell. You can use out-of-band access methods to allow SSH enabling the admin container and to pass some bootstrapping configuration steps with user data. For more information, see these sections in the bottlerocket README.md on GitHub:

This procedure requires eksctl version 0.215.0 or later. You can check your version with the following command:

For instructions on how to install or upgrade eksctl, see Installation in the eksctl documentation.NOTE: This procedure only works for clusters that were created with eksctl.

Copy the following contents to your device. Replace my-cluster with the name of your cluster. The name can contain only alphanumeric characters (case-sensitive) and hyphens. It must start with an alphanumeric character and can’t be longer than 100 characters. The name must be unique within the AWS Region and AWS account that you’re creatin

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl version
```

Example 2 (unknown):
```unknown
ng-bottlerocket
```

Example 3 (unknown):
```unknown
my-ec2-keypair-name
```

Example 4 (unknown):
```unknown
bottlerocket.yaml
```

---
