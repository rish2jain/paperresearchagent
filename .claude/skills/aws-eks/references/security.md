# Aws-Eks - Security

**Pages:** 26

---

## Security Groups Per Pod

**URL:** https://docs.aws.amazon.com/eks/latest/best-practices/sgpp.html

**Contents:**
- Security Groups Per Pod
- Recommendations
  - Disable TCP Early Demux for Liveness Probe
  - Use Security Group For Pods to leverage existing AWS configuration investment.
  - Configure Pod Security Group Enforcing Mode
        - Warning
  - Enforcing Mode: Use Strict mode for isolating pod and node traffic:
        - Warning
  - Enforcing Mode: Use Standard mode in the following situations
  - Identify Incompatibilities with Security Groups per Pod

An AWS security group acts as a virtual firewall for EC2 instances to control inbound and outbound traffic. By default, the Amazon VPC CNI will use security groups associated with the primary ENI on the node. More specifically, every ENI associated with the instance will have the same EC2 Security Groups. Thus, every Pod on a node shares the same security groups as the node it runs on.

As seen in the image below, all application Pods operating on worker nodes will have access to the RDS database service (considering RDS inbound allows node security group). Security groups are too coarse grained because they apply to all Pods running on a node. Security groups for Pods provides network segmentation for workloads which is an essential part a good defense in depth strategy.

With security groups for Pods, you can improve compute efficiency by running applications with varying network security requirements on shared compute resources. Multiple types of security rules, such as Pod-to-Pod and Pod-to-External AWS services, can be defined in a single place with EC2 security groups and applied to workloads with Kubernetes native APIs. The image below shows security groups applied at the Pod level and how they simplify your application deployment and node architecture. The Pod can now access Amazon RDS database.

You can enable security groups for Pods by setting ENABLE_POD_ENI=true for VPC CNI. Once enabled, the VPC Resource Controller running on the control plane (managed by EKS) creates and attaches a trunk interface called "`aws-k8s-trunk-eni"` to the node. The trunk interface acts as a standard network interface attached to the instance. To manage trunk interfaces, you must add the AmazonEKSVPCResourceController managed policy to the cluster role that goes with your Amazon EKS cluster.

The controller also creates branch interfaces named "aws-k8s-branch-eni" and associates them with the trunk interface. Pods are assigned a security group using the SecurityGroupPolicy custom resource and are associated with a branch interface. Since security groups are specified with network interfaces, we are now able to schedule Pods requiring specific security groups on these additional network interfaces. Review the EKS User Guide Section on Security Groups for Pods, including deployment prerequisites.

Branch interface capacity is additive to existing instance type limits for secondary IP addresses. Pods that use security groups are not accounted for in the max-pods formul

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ENABLE_POD_ENI=true
```

Example 2 (unknown):
```unknown
AmazonEKSVPCResourceController
```

Example 3 (unknown):
```unknown
initContainer
```

Example 4 (unknown):
```unknown
DISABLE_TCP_EARLY_DEMUX
```

---

## Security in Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security.html

**Contents:**
- Security in Amazon EKS
        - Note
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Cloud security at AWS is the highest priority. As an AWS customer, you benefit from a data center and network architecture that is built to meet the requirements of the most security-sensitive organizations.

Security is a shared responsibility between AWS and you. The shared responsibility model describes this as security of the cloud and security in the cloud:

Security of the cloud – AWS is responsible for protecting the infrastructure that runs AWS services in the AWS Cloud. For Amazon EKS, AWS is responsible for the Kubernetes control plane, which includes the control plane nodes and etcd database. Third-party auditors regularly test and verify the effectiveness of our security as part of the AWS compliance programs. To learn about the compliance programs that apply to Amazon EKS, see AWS Services in Scope by Compliance Program.

Security in the cloud – Your responsibility includes the following areas.

The security configuration of the data plane, including the configuration of the security groups that allow traffic to pass from the Amazon EKS control plane into the customer VPC

The configuration of the nodes and the containers themselves

The node’s operating system (including updates and security patches)

Other associated application software:

Setting up and managing network controls, such as firewall rules

Managing platform-level identity and access management, either with or in addition to IAM

The sensitivity of your data, your company’s requirements, and applicable laws and regulations

Amazon EKS is certified by multiple compliance programs for regulated and sensitive applications. Amazon EKS is compliant with SOC, PCI, ISO, FedRAMP-Moderate, IRAP, C5, K-ISMS, ENS High, OSPAR, HITRUST CSF, and is a HIPAA eligible service. For more information, see Learn how access control works in Amazon EKS.

This documentation helps you understand how to apply the shared responsibility model when using Amazon EKS. The following topics show you how to configure Amazon EKS to meet your security and compliance objectives. You also learn how to use other AWS services that help you to monitor and secure your Amazon EKS resources.

Linux containers are made up of control groups (cgroups) and namespaces that help limit what a container can access, but all containers share the same Linux kernel as the host Amazon EC

*[Content truncated]*

---

## Disable Windows support

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/disable-windows-support.html

**Contents:**
- Disable Windows support

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

If your cluster contains Amazon Linux nodes and you use security groups for Pods with them, then skip this step.

Remove the AmazonVPCResourceController managed IAM policy from your cluster role. Replace eksClusterRole with the name of your cluster role.

Disable Windows IPAM in the amazon-vpc-cni ConfigMap.

**Examples:**

Example 1 (unknown):
```unknown
AmazonVPCResourceController
```

Example 2 (unknown):
```unknown
eksClusterRole
```

Example 3 (unknown):
```unknown
aws iam detach-role-policy \
    --role-name eksClusterRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController
```

Example 4 (unknown):
```unknown
amazon-vpc-cni
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#policy-example1

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

## Grant IAM users and roles access to Kubernetes APIs {#grant-iam-users-and-roles-access-to-kubernetes-apis-canonical}

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/grant-k8s-access.html

**Contents:**
- Grant IAM users and roles access to Kubernetes APIs
- Associate IAM Identities with Kubernetes Permissions
- Set Cluster Authentication Mode
        - Important
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Your cluster has an Kubernetes API endpoint. Kubectl uses this API. You can authenticate to this API using two types of identities:

An AWS Identity and Access Management (IAM) principal (role or user) – This type requires authentication to IAM. Users can sign in to AWS as an IAM user or with a federated identity by using credentials provided through an identity source. Users can only sign in with a federated identity if your administrator previously set up identity federation using IAM roles. When users access AWS by using federation, they’re indirectly assuming a role. When users use this type of identity, you:

Can assign them Kubernetes permissions so that they can work with Kubernetes objects on your cluster. For more information about how to assign permissions to your IAM principals so that they’re able to access Kubernetes objects on your cluster, see Grant IAM users access to Kubernetes with EKS access entries.

Can assign them IAM permissions so that they can work with your Amazon EKS cluster and its resources using the Amazon EKS API, AWS CLI, AWS CloudFormation, AWS Management Console, or eksctl. For more information, see Actions defined by Amazon Elastic Kubernetes Service in the Service Authorization Reference.

Nodes join your cluster by assuming an IAM role. The ability to access your cluster using IAM principals is provided by the AWS IAM Authenticator for Kubernetes, which runs on the Amazon EKS control plane.

A user in your own OpenID Connect (OIDC) provider – This type requires authentication to your OIDC provider. For more information about setting up your own OIDC provider with your Amazon EKS cluster, see Grant users access to Kubernetes with an external OIDC provider. When users use this type of identity, you:

Can assign them Kubernetes permissions so that they can work with Kubernetes objects on your cluster.

Can’t assign them IAM permissions so that they can work with your Amazon EKS cluster and its resources using the Amazon EKS API, AWS CLI, AWS CloudFormation, AWS Management Console, or eksctl.

You can use both types of identities with your cluster. The IAM authentication method cannot be disabled. The OIDC authentication method is optional.

The AWS IAM Authenticator for Kubernetes is installed on your cluster’s control plane. It enables AWS Identity and Access Management (IAM)

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl create iamidentitymapping
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
API_AND_CONFIG_MAP
```

---

## Change authentication mode to use access entries

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/setting-up-access-entries.html

**Contents:**
- Change authentication mode to use access entries
- AWS Console
- AWS CLI
- Required platform version

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To begin using access entries, you must change the authentication mode of the cluster to either the API_AND_CONFIG_MAP or API modes. This adds the API for access entries.

Open the Amazon EKS console.

Choose the name of the cluster that you want to create an access entry in.

Choose the Access tab.

The Authentication mode shows the current authentication mode of the cluster. If the mode says EKS API, you can already add access entries and you can skip the remaining steps.

Choose Manage access.

For Cluster authentication mode, select a mode with the EKS API. Note that you can’t change the authentication mode back to a mode that removes the EKS API and access entries.

Choose Save changes. Amazon EKS begins to update the cluster, the status of the cluster changes to Updating, and the change is recorded in the Update history tab.

Wait for the status of the cluster to return to Active. When the cluster is Active, you can follow the steps in Create access entries to add access to the cluster for IAM principals.

Install the AWS CLI, as described in Installing in the AWS Command Line Interface User Guide.

Run the following command. Replace my-cluster with the name of your cluster. If you want to disable the ConfigMap method permanently, replace API_AND_CONFIG_MAP with API.

Amazon EKS begins to update the cluster, the status of the cluster changes to UPDATING, and the change is recorded in the aws eks list-updates .

Wait for the status of the cluster to return to Active. When the cluster is Active, you can follow the steps in Create access entries to add access to the cluster for IAM principals.

To use access entries, the cluster must have a platform version that is the same or later than the version listed in the following table, or a Kubernetes version that is later than the versions listed in the table. If your Kubernetes version is not listed, all platform versions support access entries.

For more information, see platform-versions.

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
aws eks update-cluster-config --name my-cluster --access-config authenticationMode=API_AND_CONFIG_MAP
```

---

## Learn about identity and access in EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/auto-learn-iam.html

**Contents:**
- Learn about identity and access in EKS Auto Mode
- Cluster IAM role
- Node IAM role
- Service-linked role
- Custom AWS tags for EKS Auto resources
- Access Policy Reference

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes the Identity and Access Management (IAM) roles and permissions required to use EKS Auto Mode. EKS Auto Mode uses two primary IAM roles: a Cluster IAM Role and a Node IAM Role. These roles work in conjunction with EKS Pod Identity and EKS access entries to provide comprehensive access management for your EKS clusters.

When you configure EKS Auto Mode, you will need to set up these IAM roles with specific permissions that allow AWS services to interact with your cluster resources. This includes permissions for managing compute resources, storage volumes, load balancers, and networking components. Understanding these role configurations is essential for proper cluster operation and security.

In EKS Auto Mode, AWS IAM roles are automatically mapped to Kubernetes permissions through EKS access entries, removing the need for manual configuration of aws-auth ConfigMaps or custom bindings. When you create a new auto mode cluster, EKS automatically creates the corresponding Kubernetes permissions using Access entries, ensuring that AWS services and cluster components have the appropriate access levels within both the AWS and Kubernetes authorization systems. This automated integration reduces configuration complexity and helps prevent permission-related issues that commonly occur when managing EKS clusters.

The Cluster IAM role is an AWS Identity and Access Management (IAM) role used by Amazon EKS to manage permissions for Kubernetes clusters. This role grants Amazon EKS the necessary permissions to interact with other AWS services on behalf of your cluster, and is automatically configured with Kubernetes permissions using EKS access entries.

You must attach AWS IAM policies to this role.

EKS Auto Mode attaches Kubernetes permissions to this role automatically using EKS access entries.

With EKS Auto Mode, AWS suggests creating a single Cluster IAM Role per AWS account.

AWS suggests naming this role AmazonEKSAutoClusterRole.

This role requires permissions for multiple AWS services to manage resources including EBS volumes, Elastic Load Balancers, and EC2 instances.

The suggested configuration for this role includes multiple AWS managed IAM policies, related to the different capabilities of EKS Auto Mode.

AmazonEKSComputePolicy

AmazonEKSBlockStoragePolicy

AmazonEKSLoadBalancingPolicy

Ama

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKSAutoClusterRole
```

Example 2 (unknown):
```unknown
AmazonEKSComputePolicy
```

Example 3 (unknown):
```unknown
AmazonEKSBlockStoragePolicy
```

Example 4 (unknown):
```unknown
AmazonEKSLoadBalancingPolicy
```

---

## CreateAccessConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateAccessConfigRequest.html#AmazonEKS-Type-CreateAccessConfigRequest-authenticationMode

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

## Grant IAM users and roles access to Kubernetes APIs (Reference)

For complete details, see the [Grant IAM users and roles access to Kubernetes APIs](#grant-iam-users-and-roles-access-to-kubernetes-apis-canonical) section above.

**Examples:**

Example 1 (unknown):
```unknown
eksctl create iamidentitymapping
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
API_AND_CONFIG_MAP
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#security-iam-id-based-policy-examples-view-own-permissions

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

## Best Practices for Security

**URL:** https://docs.aws.amazon.com/eks/latest/best-practices/security.html

**Contents:**
- Best Practices for Security
- How to use this guide
- Understanding the Shared Responsibility Model
- Introduction
- Feedback
- Further Reading
- Tools and resources

This guide provides advice about protecting information, systems, and assets that are reliant on EKS while delivering business value through risk assessments and mitigation strategies. The guidance herein is part of a series of best practices guides that AWS is publishing to help customers implement EKS in accordance with best practices. Guides for Performance, Operational Excellence, Cost Optimization, and Reliability will be available in the coming months.

This guide is meant for security practitioners who are responsible for implementing and monitoring the effectiveness of security controls for EKS clusters and the workloads they support. The guide is organized into different topic areas for easier consumption. Each topic starts with a brief overview, followed by a list of recommendations and best practices for securing your EKS clusters. The topics do not need to be read in a particular order.

Security and compliance are considered shared responsibilities when using a managed service like EKS. Generally speaking, AWS is responsible for security "of" the cloud whereas you, the customer, are responsible for security "in" the cloud. With EKS, AWS is responsible for managing of the EKS managed Kubernetes control plane. This includes the Kubernetes control plane nodes, the ETCD database, and other infrastructure necessary for AWS to deliver a secure and reliable service. As a consumer of EKS, you are largely responsible for the topics in this guide, e.g. IAM, pod security, runtime security, network security, and so forth.

When it comes to infrastructure security, AWS will assume additional responsibilities as you move from self-managed workers, to managed node groups, to Fargate. For example, with Fargate, AWS becomes responsible for securing the underlying instance/runtime used to run your Pods.

Shared Responsibility Model - Fargate

AWS will also assume responsibility of keeping the EKS optimized AMI up to date with Kubernetes patch versions and security patches. Customers using Managed Node Groups (MNG) are responsible for upgrading their Nodegroups to the latest AMI via EKS API, CLI, Cloudformation or AWS Console. Also unlike Fargate, MNGs will not automatically scale your infrastructure/cluster. That can be handled by the cluster-autoscaler or other technologies such as Karpenter, native AWS autoscaling, SpotInst’s Ocean, or Atlassian’s Escalator.

Shared Responsibility Model - MNG

Before designing your system, it is important to know where the li

*[Content truncated]*

---

## Troubleshooting IAM

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-troubleshoot.html

**Contents:**
- Troubleshooting IAM
- AccessDeniedException
- Can’t see Nodes on the Compute tab or anything on the Resources tab and you receive an error in the AWS Management Console
- aws-auth ConfigMap does not grant access to the cluster
- I am not authorized to perform iam:PassRole
- I want to allow people outside of my AWS account to access my Amazon EKS resources
- Pod containers receive the following error: An error occurred (SignatureDoesNotMatch) when calling the GetCallerIdentity operation: Credential should be scoped to a valid region

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers some common errors that you may see while using Amazon EKS with IAM and how to work around them.

If you receive an AccessDeniedException when calling an AWS API operation, then the IAM principal credentials that you’re using don’t have the required permissions to make that call.

In the previous example message, the user does not have permissions to call the Amazon EKS DescribeCluster API operation. To provide Amazon EKS admin permissions to an IAM principal, see Amazon EKS identity-based policy examples.

For more general information about IAM, see Controlling access using policies in the IAM User Guide.

You may see a console error message that says Your current user or role does not have access to Kubernetes objects on this EKS cluster. Make sure that the IAM principal user that you’re using the AWS Management Console with has the necessary permissions. For more information, see Required permissions.

The AWS IAM Authenticator doesn’t permit a path in the role ARN used in the ConfigMap. Therefore, before you specify rolearn, remove the path. For example, change arn:aws:iam::111122223333:role/team/developers/eks-admin to arn:aws:iam::111122223333:role/eks-admin .

If you receive an error that you’re not authorized to perform the iam:PassRole action, your policies must be updated to allow you to pass a role to Amazon EKS.

Some AWS services allow you to pass an existing role to that service instead of creating a new service role or service-linked role. To do this, you must have permissions to pass the role to the service.

The following example error occurs when an IAM user named marymajor tries to use the console to perform an action in Amazon EKS. However, the action requires the service to have permissions that are granted by a service role. Mary does not have permissions to pass the role to the service.

In this case, Mary’s policies must be updated to allow her to perform the iam:PassRole action.

If you need help, contact your AWS administrator. Your administrator is the person who provided you with your sign-in credentials.

You can create a role that users in other accounts or people outside of your organization can use to access your resources. You can specify who is trusted to assume the role. For services that support resource-based policies or access control lists (ACLs), you ca

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AccessDeniedException
```

Example 2 (unknown):
```unknown
An error occurred (AccessDeniedException) when calling the DescribeCluster operation:
User: arn:aws:iam::111122223333:user/user_name is not authorized to perform:
eks:DescribeCluster on resource: arn:aws:eks:region:111122223333:cluster/my-cluster
```

Example 3 (unknown):
```unknown
DescribeCluster
```

Example 4 (unknown):
```unknown
Your current user or role does not have access to Kubernetes objects on this EKS cluster
```

---

## CreateAccessConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateAccessConfigRequest.html

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

## AccessConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_AccessConfigResponse.html#AmazonEKS-Type-AccessConfigResponse-authenticationMode

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

## Understand Amazon EKS created RBAC roles and users

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/default-roles-users.html

**Contents:**
- Understand Amazon EKS created RBAC roles and users
- AWS Management Console
  - Prerequisite
  - To view Amazon EKS created identities using the AWS Management Console
- Kubectl
  - Prerequisite
  - To view Amazon EKS created identities using kubectl

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you create a Kubernetes cluster, several default Kubernetes identities are created on that cluster for the proper functioning of Kubernetes. Amazon EKS creates Kubernetes identities for each of its default components. The identities provide Kubernetes role-based authorization control (RBAC) for the cluster components. For more information, see Using RBAC Authorization in the Kubernetes documentation.

When you install optional add-ons to your cluster, additional Kubernetes identities might be added to your cluster. For more information about identities not addressed by this topic, see the documentation for the add-on.

You can view the list of Amazon EKS created Kubernetes identities on your cluster using the AWS Management Console or kubectl command line tool. All of the user identities appear in the kube audit logs available to you through Amazon CloudWatch.

The IAM principal that you use must have the permissions described in Required permissions.

Open the Amazon EKS console.

In the Clusters list, choose the cluster that contains the identities that you want to view.

Choose the Resources tab.

Under Resource types, choose Authorization.

Choose, ClusterRoles, ClusterRoleBindings, Roles, or RoleBindings. All resources prefaced with eks are created by Amazon EKS. Additional Amazon EKS created identity resources are:

The ClusterRole and ClusterRoleBinding named aws-node. The aws-node resources support the Amazon VPC CNI plugin for Kubernetes, which Amazon EKS installs on all clusters.

A ClusterRole named vpc-resource-controller-role and a ClusterRoleBinding named vpc-resource-controller-rolebinding. These resources support the Amazon VPC resource controller, which Amazon EKS installs on all clusters.

In addition to the resources that you see in the console, the following special user identities exist on your cluster, though they’re not visible in the cluster’s configuration:

eks:cluster-bootstrap – Used for kubectl operations during cluster bootstrap.

eks:support-engineer – Used for cluster management operations.

Choose a specific resource to view details about it. By default, you’re shown information in Structured view. In the top-right corner of the details page you can choose Raw view to see all information for the resource.

The entity that you use (AWS Identity and Access Management (IAM) o

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:cluster-bootstrap
```

Example 2 (unknown):
```unknown
eks:support-engineer
```

Example 3 (unknown):
```unknown
ClusterRole
```

Example 4 (unknown):
```unknown
RoleBinding
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#security-iam-id-based-policy-examples-console

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

## Infrastructure security in Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/infrastructure-security.html

**Contents:**
- Infrastructure security in Amazon EKS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

As a managed service, Amazon Elastic Kubernetes Service is protected by AWS global network security. For information about AWS security services and how AWS protects infrastructure, see AWS Cloud Security. To design your AWS environment using the best practices for infrastructure security, see Infrastructure Protection in Security Pillar AWS Well‐Architected Framework.

You use AWS published API calls to access Amazon EKS through the network. Clients must support the following:

Transport Layer Security (TLS). We require TLS 1.2 and recommend TLS 1.3.

Cipher suites with perfect forward secrecy (PFS) such as DHE (Ephemeral Diffie-Hellman) or ECDHE (Elliptic Curve Ephemeral Diffie-Hellman). Most modern systems such as Java 7 and later support these modes.

Additionally, requests must be signed by using an access key ID and a secret access key that is associated with an IAM principal. Or you can use the AWS Security Token Service (AWS STS) to generate temporary security credentials to sign requests.

When you create an Amazon EKS cluster, you specify the VPC subnets for your cluster to use. Amazon EKS requires subnets in at least two Availability Zones. We recommend a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to Pods running on nodes that are in private subnets.

For more information about VPC considerations, see View Amazon EKS networking requirements for VPC and subnets.

If you create your VPC and node groups with the AWS CloudFormation templates provided in the Get started with Amazon EKS walkthrough, then your control plane and node security groups are configured with our recommended settings.

For more information about security group considerations, see View Amazon EKS security group requirements for clusters.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster (using Kubernetes management tools such as kubectl). By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management (IAM) and native Kubernetes Role Based Access Control (RBAC).

You can enable private access to the Kubernetes API server so that all communication be

*[Content truncated]*

---

## Security considerations for Amazon EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/auto-security.html

**Contents:**
- Security considerations for Amazon EKS Auto Mode
- API security and authentication
- Network security
- EC2 managed instance security
  - EC2 security
  - Instance lifecycle management
  - Data protection
  - Patch management
        - Note
  - Access controls

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes the security architecture, controls, and best practices for Amazon EKS Auto Mode. As organizations deploy containerized applications at scale, maintaining a strong security posture becomes increasingly complex. EKS Auto Mode implements automated security controls and integrates with AWS security services to help you protect your cluster infrastructure, workloads, and data. Through built-in security features like enforced node lifecycle management and automated patch deployment, EKS Auto Mode helps you maintain security best practices while reducing operational overhead.

Before proceeding with this topic, make sure that you’re familiar with basic EKS Auto Mode concepts and have reviewed the prerequisites for enabling EKS Auto Mode on your clusters. For general information about Amazon EKS security, see Security in Amazon EKS.

Amazon EKS Auto Mode builds upon the existing security foundations of Amazon EKS while introducing additional automated security controls for EC2 managed instances.

Amazon EKS Auto Mode uses AWS platform security mechanisms to secure and authenticate calls to the Amazon EKS API.

Access to the Kubernetes API is secured through EKS access entries, which integrate with AWS IAM identities.

For more information, see Grant IAM users access to Kubernetes with EKS access entries.

Customers can implement fine-grained access control to the Kubernetes API endpoint through configuration of EKS access entries.

Amazon EKS Auto Mode supports multiple layers of network security:

Operates within your Amazon Virtual Private Cloud (VPC)

Supports custom VPC configurations and subnet layouts

Enables private networking between cluster components

For more information, see Managing security responsibilities for Amazon Virtual Private Cloud

Native support for Kubernetes Network Policies

Ability to define granular network traffic rules

For more information, see Limit Pod traffic with Kubernetes network policies

Amazon EKS Auto Mode operates EC2 managed instances with the following security controls:

EC2 managed instances maintain the security features of Amazon EC2.

For more information about EC2 managed instances, see Security in Amazon EC2.

EC2 managed instances operated by EKS Auto Mode have maximum lifetime of 21 days. Amazon EKS Auto Mode automatically terminates instance

*[Content truncated]*

---

## Grant IAM users access to Kubernetes with EKS access entries

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html

**Contents:**
- Grant IAM users access to Kubernetes with EKS access entries
- Overview
- Features
- How to attach permissions
- Considerations
- Get started

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This section is designed to show you how to manage IAM principal access to Kubernetes clusters in Amazon Elastic Kubernetes Service (EKS) using access entries and policies. You’ll find details on changing authentication modes, migrating from legacy aws-auth ConfigMap entries, creating, updating, and deleting access entries, associating policies with entries, reviewing predefined policy permissions, and key prerequisites and considerations for secure access management.

EKS access entries are the best way to grant users access to the Kubernetes API. For example, you can use access entries to grant developers access to use kubectl. Fundamentally, an EKS access entry associates a set of Kubernetes permissions with an IAM identity, such as an IAM role. For example, a developer may assume an IAM role and use that to authenticate to an EKS Cluster.

Centralized Authentication and Authorization: Controls access to Kubernetes clusters directly via Amazon EKS APIs, eliminating the need to switch between AWS and Kubernetes APIs for user permissions.

Granular Permissions Management: Uses access entries and policies to define fine-grained permissions for AWS IAM principals, including modifying or revoking cluster-admin access from the creator.

IaC Tool Integration: Supports infrastructure as code tools like AWS CloudFormation, Terraform, and AWS CDK to define access configurations during cluster creation.

Misconfiguration Recovery: Allows restoring cluster access through the Amazon EKS API without direct Kubernetes API access.

Reduced Overhead and Enhanced Security: Centralizes operations to lower overhead while leveraging AWS IAM features like CloudTrail audit logging and multi-factor authentication.

You can attach Kubernetes permissions to access entries in two ways:

Use an access policy. Access policies are pre-defined Kubernetes permissions templates maintained by AWS. For more information, see Review access policy permissions.

Reference a Kubernetes group. If you associate an IAM Identity with a Kubernetes group, you can create Kubernetes resources that grant the group permissions. For more information, see Using RBAC Authorization in the Kubernetes documentation.

When enabling EKS access entries on existing clusters, keep the following in mind:

Legacy Cluster Behavior: For clusters created before the introd

*[Content truncated]*

---

## Identity and access management for Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam.html

**Contents:**
- Identity and access management for Amazon EKS
- Audience
- Authenticating with identities
  - AWS account root user
  - IAM users and groups
  - IAM roles
- Managing access using policies
  - Identity-based policies
  - Resource-based policies
  - Access control lists (ACLs)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

AWS Identity and Access Management (IAM) is an AWS service that helps an administrator securely control access to AWS resources. IAM administrators control who can be authenticated (signed in) and authorized (have permissions) to use Amazon EKS resources. IAM is an AWS service that you can use with no additional charge.

How you use AWS Identity and Access Management (IAM) differs, depending on the work that you do in Amazon EKS.

Service user – If you use the Amazon EKS service to do your job, then your administrator provides you with the credentials and permissions that you need. As you use more Amazon EKS features to do your work, you might need additional permissions. Understanding how access is managed can help you request the right permissions from your administrator. If you cannot access a feature in Amazon EKS, see Troubleshooting IAM.

Service administrator – If you’re in charge of Amazon EKS resources at your company, you probably have full access to Amazon EKS. It’s your job to determine which Amazon EKS features and resources your service users should access. You must then submit requests to your IAM administrator to change the permissions of your service users. Review the information on this page to understand the basic concepts of IAM. To learn more about how your company can use IAM with Amazon EKS, see How Amazon EKS works with IAM.

IAM administrator – If you’re an IAM administrator, you might want to learn details about how you can write policies to manage access to Amazon EKS. To view example Amazon EKS identity-based policies that you can use in IAM, see Amazon EKS identity-based policy examples.

Authentication is how you sign in to AWS using your identity credentials. You must be authenticated (signed in to AWS) as the AWS account root user, as an IAM user, or by assuming an IAM role.

You can sign in to AWS as a federated identity by using credentials provided through an identity source. AWS IAM Identity Center (IAM Identity Center) users, your company’s single sign-on authentication, and your Google or Facebook credentials are examples of federated identities. When you sign in as a federated identity, your administrator previously set up identity federation using IAM roles. When you access AWS by using federation, you are indirectly assuming a role.

Depending on the type of user you ar

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
iam:GetRole
```

---

## Security considerations for Kubernetes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-k8s.html

**Contents:**
- Security considerations for Kubernetes
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The following are considerations for security in the cloud, as they affect Kubernetes in Amazon EKS clusters. For an in-depth review of security controls and practices in Kubernetes, see Cloud Native Security and Kubernetes in the Kubernetes documentation.

Secure workloads with Kubernetes certificates

Understand Amazon EKS created RBAC roles and users

Encrypt Kubernetes secrets with KMS on existing clusters

Use AWS Secrets Manager secrets with Amazon EKS Pods

Default envelope encryption for all Kubernetes API Data

---

## Identity and Access Management

**URL:** https://docs.aws.amazon.com/eks/latest/best-practices/identity-and-access-management.html#_identities_and_credentials_for_eks_pods_recommendations

**Contents:**
- Identity and Access Management
- Controlling Access to EKS Clusters
  - CloudWatch query to help users identify clients sending requests to global STS endpoint
  - Cluster Access Manager
  - The aws-auth ConfigMap (deprecated)
  - Benefits over ConfigMap-based access management
- Cluster Access Recommendations
  - Combine IAM Identity Center with CAM API
  - Make the EKS Cluster Endpoint private
  - Don’t use a service account token for authentication

Identity and Access Management (IAM) is an AWS service that performs two essential functions: Authentication and Authorization. Authentication involves the verification of a identity whereas authorization governs the actions that can be performed by AWS resources. Within AWS, a resource can be another AWS service, e.g. EC2, or an AWS principal such as an IAM User or Role. The rules governing the actions that a resource is allowed to perform are expressed as IAM policies.

The Kubernetes project supports a variety of different strategies to authenticate requests to the kube-apiserver service, e.g. Bearer Tokens, X.509 certificates, OIDC, etc. EKS currently has native support for webhook token authentication, service account tokens, and as of February 21, 2021, OIDC authentication.

The webhook authentication strategy calls a webhook that verifies bearer tokens. On EKS, these bearer tokens are generated by the AWS CLI or the aws-iam-authenticator client when you run kubectl commands. As you execute commands, the token is passed to the kube-apiserver which forwards it to the authentication webhook. If the request is well-formed, the webhook calls a pre-signed URL embedded in the token’s body. This URL validates the request’s signature and returns information about the user, e.g. the user’s account, Arn, and UserId to the kube-apiserver.

To manually generate a authentication token, type the following command in a terminal window:

The output should resemble this:

You can also get a token programmatically. Below is an example written in Go:

The output should resemble this:

Each token starts with k8s-aws-v1. followed by a base64 encoded string. The string, when decoded, should resemble to something similar to this:

The token consists of a pre-signed URL that includes an Amazon credential and signature. For additional details see https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html.

The token has a time to live (TTL) of 15 minutes after which a new token will need to be generated. This is handled automatically when you use a client like kubectl, however, if you’re using the Kubernetes dashboard, you will need to generate a new token and re-authenticate each time the token expires.

Once the user’s identity has been authenticated by the AWS IAM service, the kube-apiserver reads the aws-auth ConfigMap in the kube-system Namespace to determine the RBAC group to associate with the user. The aws-auth ConfigMap is used to create a static

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws eks get-token --cluster-name <cluster_name> --region <region>
```

Example 2 (unknown):
```unknown
{
    "kind": "ExecCredential",
    "apiVersion": "client.authentication.k8s.io/v1alpha1",
    "spec": {},
    "status": {
        "expirationTimestamp": "2024-12-20T17:38:48Z",
        "token": "k8s-aws-v1.aHR0cHM6Ly9zdHMudXMtd2VzdC0yLmFtYXpvbmF3cy5jb20vP0FjdGlvbj1HZ...."
    }
}
```

Example 3 (unknown):
```unknown
package main

import (
  "fmt"
  "log"
  "sigs.k8s.io/aws-iam-authenticator/pkg/token"
)

func main()  {
  g, _ := token.NewGenerator(false, false)
  tk, err := g.Get("<cluster_name>")
  if err != nil {
    log.Fatal(err)
  }
  fmt.Println(tk)
}
```

Example 4 (unknown):
```unknown
{
  "kind": "ExecCredential",
  "apiVersion": "client.authentication.k8s.io/v1alpha1",
  "spec": {},
  "status": {
    "expirationTimestamp": "2020-02-19T16:08:27Z",
    "token": "k8s-aws-v1.aHR0cHM6Ly9zdHMuYW1hem9uYXdzLmNvbS8_QWN0aW9uPUdldENhbGxlcklkZW50aXR5JlZlcnNpb249MjAxMS0wNi0xNSZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFKTkdSSUxLTlNSQzJXNVFBJTJGMjAyMDAyMTklMkZ1cy1lYXN0LTElMkZzdHMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDIwMDIxOVQxNTU0MjdaJlgtQW16LUV4cGlyZXM9NjAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JTNCeC1rOHMtYXdzLWlkJlgtQW16LVNpZ25hdHVyZT0yMjBmOGYzNTg1ZTMyMGRkYjVlN
...
```

---

## Learn about identity and access in EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/auto-learn-iam.html#tag-prop

**Contents:**
- Learn about identity and access in EKS Auto Mode
- Cluster IAM role
- Node IAM role
- Service-linked role
- Custom AWS tags for EKS Auto resources
- Access Policy Reference

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes the Identity and Access Management (IAM) roles and permissions required to use EKS Auto Mode. EKS Auto Mode uses two primary IAM roles: a Cluster IAM Role and a Node IAM Role. These roles work in conjunction with EKS Pod Identity and EKS access entries to provide comprehensive access management for your EKS clusters.

When you configure EKS Auto Mode, you will need to set up these IAM roles with specific permissions that allow AWS services to interact with your cluster resources. This includes permissions for managing compute resources, storage volumes, load balancers, and networking components. Understanding these role configurations is essential for proper cluster operation and security.

In EKS Auto Mode, AWS IAM roles are automatically mapped to Kubernetes permissions through EKS access entries, removing the need for manual configuration of aws-auth ConfigMaps or custom bindings. When you create a new auto mode cluster, EKS automatically creates the corresponding Kubernetes permissions using Access entries, ensuring that AWS services and cluster components have the appropriate access levels within both the AWS and Kubernetes authorization systems. This automated integration reduces configuration complexity and helps prevent permission-related issues that commonly occur when managing EKS clusters.

The Cluster IAM role is an AWS Identity and Access Management (IAM) role used by Amazon EKS to manage permissions for Kubernetes clusters. This role grants Amazon EKS the necessary permissions to interact with other AWS services on behalf of your cluster, and is automatically configured with Kubernetes permissions using EKS access entries.

You must attach AWS IAM policies to this role.

EKS Auto Mode attaches Kubernetes permissions to this role automatically using EKS access entries.

With EKS Auto Mode, AWS suggests creating a single Cluster IAM Role per AWS account.

AWS suggests naming this role AmazonEKSAutoClusterRole.

This role requires permissions for multiple AWS services to manage resources including EBS volumes, Elastic Load Balancers, and EC2 instances.

The suggested configuration for this role includes multiple AWS managed IAM policies, related to the different capabilities of EKS Auto Mode.

AmazonEKSComputePolicy

AmazonEKSBlockStoragePolicy

AmazonEKSLoadBalancingPolicy

Ama

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonEKSAutoClusterRole
```

Example 2 (unknown):
```unknown
AmazonEKSComputePolicy
```

Example 3 (unknown):
```unknown
AmazonEKSBlockStoragePolicy
```

Example 4 (unknown):
```unknown
AmazonEKSLoadBalancingPolicy
```

---

## Grant IAM users and roles access to Kubernetes APIs (Reference)

For complete details, see the [Grant IAM users and roles access to Kubernetes APIs](#grant-iam-users-and-roles-access-to-kubernetes-apis-canonical) section above.

**Examples:**

Example 1 (unknown):
```unknown
eksctl create iamidentitymapping
```

Example 2 (unknown):
```unknown
API_AND_CONFIG_MAP
```

Example 3 (unknown):
```unknown
API_AND_CONFIG_MAP
```

---

## Amazon EKS identity-based policy examples

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#policy-example2

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

## Retrieve IAM information about an Amazon EKS add-on

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/retreive-iam-info.html

**Contents:**
- Retrieve IAM information about an Amazon EKS add-on
- Procedure
- Pod Identity Support Reference

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Before you create an add-on, use the AWS CLI to determine:

If the add-on requires IAM permissions

The suggested IAM policy to use

Determine the name of the add-on you want to install, and the Kubernetes version of your cluster. For more information about add-ons, see Amazon EKS add-ons.

Use the AWS CLI to determine if the add-on requires IAM permissions.

Review the following sample output. Note that requiresIamPermissions is true, and the default add-on version. You need to specify the add-on version when retrieving the recommended IAM policy.

If the add-on requires IAM permissions, use the AWS CLI to retrieve a recommended IAM policy.

Review the following output. Note the recommendedManagedPolicies.

Create an IAM role and attach the recommended Managed Policy. Alternatively, review the managed policy and scope down the permissions as appropriate. For more information see Create a Pod Identity association (AWS Console).

The following table indicates if certain Amazon EKS add-ons support EKS Pod Identity.

Amazon EBS CSI Driver

Amazon EFS CSI Driver

AWS Distro for OpenTelemetry

Mountpoint for Amazon S3 CSI Driver

Amazon CloudWatch Observability agent

This table was last updated on October 28, 2024.

**Examples:**

Example 1 (unknown):
```unknown
aws eks describe-addon-versions \
--addon-name <addon-name> \
--kubernetes-version <kubernetes-version>
```

Example 2 (unknown):
```unknown
aws eks describe-addon-versions \
--addon-name aws-ebs-csi-driver \
--kubernetes-version 1.30
```

Example 3 (unknown):
```unknown
requiresIamPermissions
```

Example 4 (unknown):
```unknown
{
    "addons": [
        {
            "addonName": "aws-ebs-csi-driver",
            "type": "storage",
            "addonVersions": [
                {
                    "addonVersion": "v1.31.0-eksbuild.1",
                    "architecture": [
                        "amd64",
                        "arm64"
                    ],
                    "compatibilities": [
                        {
                            "clusterVersion": "1.30",
                            "platformVersions": [
                                "*"
                            ],
                       
...
```

---
