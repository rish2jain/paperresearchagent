# Aws-Eks - Other

**Pages:** 107

---

## OutpostConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_OutpostConfigRequest.html#AmazonEKS-Type-OutpostConfigRequest-controlPlanePlacement

**Contents:**
- OutpostConfigRequest
- Contents
- See Also

The configuration of your local Amazon EKS cluster on an AWS Outpost. Before creating a cluster on an Outpost, review Creating a local cluster on an Outpost in the Amazon EKS User Guide. This API isn't available for Amazon EKS clusters on the AWS cloud.

The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts. Choose an instance type based on the number of nodes that your cluster will have. For more information, see Capacity considerations in the Amazon EKS User Guide.

The instance type that you specify is used for all Kubernetes control plane instances. The instance type can't be changed after cluster creation. The control plane is not automatically scaled by Amazon EKS.

The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts. Only a single Outpost ARN is supported.

Type: Array of strings

An object representing the placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost. For more information, see Capacity considerations in the Amazon EKS User Guide.

Type: ControlPlanePlacementRequest object

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Limit Pod traffic with Kubernetes network policies

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cni-network-policy.html

**Contents:**
- Limit Pod traffic with Kubernetes network policies
- Considerations
        - Warning

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

By default, there are no restrictions in Kubernetes for IP addresses, ports, or connections between any Pods in your cluster or between your Pods and resources in any other network. You can use Kubernetes network policy to restrict network traffic to and from your Pods. For more information, see Network Policies in the Kubernetes documentation.

If you have version 1.13 or earlier of the Amazon VPC CNI plugin for Kubernetes on your cluster, you need to implement a third party solution to apply Kubernetes network policies to your cluster. Version 1.14 or later of the plugin can implement network policies, so you don’t need to use a third party solution. In this topic, you learn how to configure your cluster to use Kubernetes network policy on your cluster without using a third party add-on.

Network policies in the Amazon VPC CNI plugin for Kubernetes are supported in the following configurations.

Version 1.14 or later of the Amazon VPC CNI plugin for Kubernetes on your cluster.

Cluster configured for IPv4 or IPv6 addresses.

You can use network policies with security groups for Pods. With network policies, you can control all in-cluster communication. With security groups for Pods, you can control access to AWS services from applications within a Pod.

You can use network policies with custom networking and prefix delegation.

When applying Amazon VPC CNI plugin for Kubernetes network policies to your cluster with the Amazon VPC CNI plugin for Kubernetes , you can apply the policies to Amazon EC2 Linux nodes only. You can’t apply the policies to Fargate or Windows nodes.

Network policies only apply either IPv4 or IPv6 addresses, but not both. In an IPv4 cluster, the VPC CNI assigns IPv4 address to pods and applies IPv4 policies. In an IPv6 cluster, the VPC CNI assigns IPv6 address to pods and applies IPv6 policies. Any IPv4 network policy rules applied to an IPv6 cluster are ignored. Any IPv6 network policy rules applied to an IPv4 cluster are ignored.

Network Policies are only applied to Pods that are part of a Deployment. Standalone Pods that don’t have a metadata.ownerReferences set can’t have network policies applied to them.

You can apply multiple network policies to the same Pod. When two or more policies that select the same Pod are configured, all policies are applied to the Pod.

The maximum numb

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
metadata.ownerReferences
```

Example 2 (unknown):
```unknown
namespaceSelector
```

Example 3 (unknown):
```unknown
PolicyEndpoint
```

Example 4 (unknown):
```unknown
policyendpoints.networking.k8s.aws
```

---

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## Log API calls as AWS CloudTrail events

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/logging-using-cloudtrail.html

**Contents:**
- Log API calls as AWS CloudTrail events
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS is integrated with AWS CloudTrail. CloudTrail is a service that provides a record of actions by a user, role, or an AWS service in Amazon EKS. CloudTrail captures all API calls for Amazon EKS as events. This includes calls from the Amazon EKS console and from code calls to the Amazon EKS API operations.

If you create a trail, you can enable continuous delivery of CloudTrail events to an Amazon S3 bucket. This includes events for Amazon EKS. If you don’t configure a trail, you can still view the most recent events in the CloudTrail console in Event history. Using the information that CloudTrail collects, you can determine several details about a request. For example, you can determine when the request was made to Amazon EKS, the IP address where the request was made from, and who made the request.

To learn more about CloudTrail, see the AWS CloudTrail User Guide.

View helpful references for AWS CloudTrail

Analyze AWS CloudTrail log file entries

View metrics for Amazon EC2 Auto Scaling groups

---

## Detect threats with Amazon GuardDuty

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/integration-guardduty.html

**Contents:**
- Detect threats with Amazon GuardDuty
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon GuardDuty is a threat detection service that helps protect you accounts, containers, workloads, and the data with your AWS environment. Using machine learning (ML) models, and anomaly and threat detection capabilities, GuardDuty continuously monitors different log sources and runtime activity to identify and prioritize potential security risks and malicious activities in your environment.

Among other features, GuardDuty offers the following two features that detect potential threats to your EKS clusters: EKS Protection and Runtime Monitoring.

New: Amazon EKS Auto Mode integrates with GuardDuty.

This feature provides threat detection coverage to help you protect Amazon EKS clusters by monitoring the associated Kubernetes audit logs. Kubernetes audit logs capture sequential actions within your cluster, including activities from users, applications using the Kubernetes API, and the control plane. For example, GuardDuty can identify that APIs called to potentially tamper with resources in a Kubernetes cluster were invoked by an unauthenticated user.

When you enable EKS Protection, GuardDuty will be able to access your Amazon EKS audit logs only for continuous threat detection. If GuardDuty identifies a potential threat to your cluster, it generates an associated Kubernetes audit log finding of a specific type. For more information about the types of findings available from Kubernetes audit logs, see Kubernetes audit logs finding types in the Amazon GuardDuty User Guide.

For more information, see EKS Protection in the Amazon GuardDuty User Guide.

This feature monitors and analyzes operating system-level, networking, and file events to help you detect potential threats in specific AWS workloads in your environment.

When you enable Runtime Monitoring and install the GuardDuty agent in your Amazon EKS clusters, GuardDuty starts monitoring the runtime events associated with this cluster. Note that the GuardDuty agent and Runtime Monitoring aren’t available for Amazon EKS Hybrid Nodes, so Runtime Monitoring isn’t available for runtime events that occur on your hybrid nodes. If GuardDuty identifies a potential threat to your cluster, it generates an associated Runtime Monitoring finding. For example, a threat can potentially start by compromising a single container that runs a vulnerable web application. Th

*[Content truncated]*

---

## Create an Amazon EKS add-on

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/creating-an-add-on.html

**Contents:**
- Create an Amazon EKS add-on
- Prerequisites
- Procedure
- Create add-on (eksctl)
- Create add-on (AWS Console)
- Create add-on (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS add-ons are add-on software for Amazon EKS clusters. All Amazon EKS add-ons:

Include the latest security patches and bug fixes.

Are validated by AWS to work with Amazon EKS.

Reduce the amount of work required to manage the add-on software.

You can create an Amazon EKS add-on using eksctl, the AWS Management Console, or the AWS CLI. If the add-on requires an IAM role, see the details for the specific add-on in Amazon EKS add-ons for details about creating the role.

Complete the following before you create an add-on:

The cluster must exist before you create an add-on for it. For more information, see Create an Amazon EKS cluster.

Check if your add-on requires an IAM role. For more information, see Verify Amazon EKS add-on version compatibility with a cluster.

Verify that the Amazon EKS add-on version is compatabile with your cluster. For more information, see Verify Amazon EKS add-on version compatibility with a cluster.

Verify that version 0.190.0 or later of the eksctl command line tool installed on your computer or AWS CloudShell. For more information, see Installation on the eksctl website.

You can create an Amazon EKS add-on using eksctl, the AWS Management Console, or the AWS CLI. If the add-on requires an IAM role, see the details for the specific add-on in Available Amazon EKS add-ons from AWS for details about creating the role.

View the names of add-ons available for a cluster version. Replace 1.33 with the version of your cluster.

An example output is as follows.

View the versions available for the add-on that you would like to create. Replace 1.33 with the version of your cluster. Replace name-of-addon with the name of the add-on you want to view the versions for. The name must be one of the names returned in the previous step.

The following output is an example of what is returned for the add-on named vpc-cni. You can see that the add-on has several available versions.

Determine whether the add-on you want to create is an Amazon EKS or AWS Marketplace add-on. The AWS Marketplace has third party add-ons that require you to complete additional steps to create the add-on.

If no output is returned, then the add-on is an Amazon EKS. If output is returned, then the add-on is an AWS Marketplace add-on. The following output is for an add-on named teleport_teleport.

You can learn 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl utils describe-addon-versions --kubernetes-version 1.33 | grep AddonName
```

Example 2 (unknown):
```unknown
"AddonName": "aws-ebs-csi-driver",
                        "AddonName": "coredns",
                        "AddonName": "kube-proxy",
                        "AddonName": "vpc-cni",
                        "AddonName": "adot",
                        "AddonName": "dynatrace_dynatrace-operator",
                        "AddonName": "upbound_universal-crossplane",
                        "AddonName": "teleport_teleport",
                        "AddonName": "factorhouse_kpow",
                        [...]
```

Example 3 (unknown):
```unknown
name-of-addon
```

Example 4 (unknown):
```unknown
eksctl utils describe-addon-versions --kubernetes-version 1.33 --name name-of-addon | grep AddonVersion
```

---

## BlockStorage

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_BlockStorage.html#AmazonEKS-Type-BlockStorage-enabled

**Contents:**
- BlockStorage
- Contents
- See Also

Indicates the current configuration of the block storage capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account. For more information, see EKS Auto Mode block storage capability in the Amazon EKS User Guide.

Indicates if the block storage capability is enabled on your EKS Auto Mode cluster. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Grant users access to Kubernetes with an external OIDC provider

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/authenticate-oidc-identity-provider.html

**Contents:**
- Grant users access to Kubernetes with an external OIDC provider
- Associate an OIDC identity provider
  - Associate an identity provider using eksctl
        - Important
  - Associate an identity provider using the AWS Console
- Example IAM policy

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS supports using OpenID Connect (OIDC) identity providers as a method to authenticate users to your cluster. OIDC identity providers can be used with, or as an alternative to AWS Identity and Access Management (IAM). For more information about using IAM, see Grant IAM users and roles access to Kubernetes APIs. After configuring authentication to your cluster, you can create Kubernetes roles and clusterroles to assign permissions to the roles, and then bind the roles to the identities using Kubernetes rolebindings and clusterrolebindings. For more information, see Using RBAC Authorization in the Kubernetes documentation.

You can associate one OIDC identity provider to your cluster.

Kubernetes doesn’t provide an OIDC identity provider. You can use an existing public OIDC identity provider, or you can run your own identity provider. For a list of certified providers, see OpenID Certification on the OpenID site.

The issuer URL of the OIDC identity provider must be publicly accessible, so that Amazon EKS can discover the signing keys. Amazon EKS doesn’t support OIDC identity providers with self-signed certificates.

You can’t disable IAM authentication to your cluster, because it’s still required for joining nodes to a cluster.

An Amazon EKS cluster must still be created by an AWS IAM principal, rather than an OIDC identity provider user. This is because the cluster creator interacts with the Amazon EKS APIs, rather than the Kubernetes APIs.

OIDC identity provider-authenticated users are listed in the cluster’s audit log if CloudWatch logs are turned on for the control plane. For more information, see Enable or disable control plane logs.

You can’t sign in to the AWS Management Console with an account from an OIDC provider. You can only View Kubernetes resources in the AWS Management Console by signing into the AWS Management Console with an AWS Identity and Access Management account.

Before you can associate an OIDC identity provider with your cluster, you need the following information from your provider:

The URL of the OIDC identity provider that allows the API server to discover public signing keys for verifying tokens. The URL must begin with https:// and should correspond to the iss claim in the provider’s OIDC ID tokens. In accordance with the OIDC standard, path components are allowed but q

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
clusterroles
```

Example 2 (unknown):
```unknown
rolebindings
```

Example 3 (unknown):
```unknown
clusterrolebindings
```

Example 4 (unknown):
```unknown
https://server.example.org
```

---

## Use AWS Secrets Manager secrets with Amazon EKS Pods

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/manage-secrets.html

**Contents:**
- Use AWS Secrets Manager secrets with Amazon EKS Pods
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To show secrets from Secrets Manager and parameters from Parameter Store as files mounted in Amazon EKS Pods, you can use the AWS Secrets and Configuration Provider (ASCP) for the Kubernetes Secrets Store CSI Driver.

With the ASCP, you can store and manage your secrets in Secrets Manager and then retrieve them through your workloads running on Amazon EKS. You can use IAM roles and policies to limit access to your secrets to specific Kubernetes Pods in a cluster. The ASCP retrieves the Pod identity and exchanges the identity for an IAM role. ASCP assumes the IAM role of the Pod, and then it can retrieve secrets from Secrets Manager that are authorized for that role.

If you use Secrets Manager automatic rotation for your secrets, you can also use the Secrets Store CSI Driver rotation reconciler feature to ensure you are retrieving the latest secret from Secrets Manager.

AWS Fargate (Fargate) node groups are not supported.

For more information, see Using Secrets Manager secrets in Amazon EKS in the AWS Secrets Manager User Guide.

---

## Default envelope encryption for all Kubernetes API Data

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/envelope-encryption.html

**Contents:**
- Default envelope encryption for all Kubernetes API Data
- Understanding envelope encryption
- How Amazon EKS enables default envelope encryption with KMS v2 and AWS KMS
- Frequently asked questions
  - How does default envelope encryption improve the security posture of my EKS cluster?
  - Which version of Kubernetes do I need to run in order to have this feature?
  - Is my data still secure if I’m running a Kubernetes cluster version that doesn’t support this feature?
  - How does envelope encryption work in Amazon EKS?
  - Do I have to do anything or change any permissions for this feature to work in my EKS cluster?
  - How can I know if default envelope encryption is enabled on my cluster?

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon Elastic Kubernetes Service (Amazon EKS) provides default envelope encryption for all Kubernetes API data in EKS clusters running Kubernetes version 1.28 or higher.

Envelope encryption protects the data you store with the Kubernetes API server. For example, envelope encryption applies to the configuration of your Kubernetes cluster, such as ConfigMaps. Envelope encryption does not apply to data on nodes or EBS volumes. EKS previously supported encrypting Kubernetes secrets, and now this envelope encryption extends to all Kubernetes API data.

This provides a managed, default experience that implements defense-in-depth for your Kubernetes applications and doesn’t require any action on your part.

Amazon EKS uses AWS Key Management Service (KMS) with Kubernetes KMS provider v2 for this additional layer of security with an Amazon Web Services owned key, and the option for you to bring your own customer managed key (CMK) from AWS KMS.

Envelope encryption is the process of encrypting plain text data with a data encryption key (DEK) before it’s sent to the datastore (etcd), and then encrypting the DEK with a root KMS key that is stored in a remote, centrally managed KMS system (AWS KMS). This is a defense-in-depth strategy because it protects the data with an encryption key (DEK), and then adds another security layer by protecting that DEK with a separate, securely stored encryption key called a key encryption key (KEK).

Amazon EKS uses KMS v2 to implement default envelope encryption for all API data in the managed Kubernetes control plane before it’s persisted in the etcd database. At startup, the cluster API server generates a data encryption key (DEK) from a secret seed combined with randomly generated data. Also at startup, the API server makes a call to the KMS plugin to encrypt the DEK seed using a remote key encryption key (KEK) from AWS KMS. This is a one-time call executed at startup of the API server and on KEK rotation. The API server then caches the encrypted DEK seed. After this, the API server uses the cached DEK seed to generate other single use DEKs based on a Key Derivation Function (KDF). Each of these generated DEKs is then used only once to encrypt a single Kubernetes resource before it’s stored in etcd. With the use of an encrypted cached DEK seed in KMS v2, the process of encrypting Ku

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:kms-storage-migrator
```

Example 2 (unknown):
```unknown
1234abcd-12ab-34cd-56ef-1234567890ab
```

---

## Set up to use Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/setting-up.html

**Contents:**
- Set up to use Amazon EKS
- Next steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To prepare for the command-line management of your Amazon EKS clusters, you need to install several tools. Use the following to set up credentials, create and modify clusters, and work with clusters once they are running:

Set up AWS CLI – Get the AWS CLI to set up and manage the services you need to work with Amazon EKS clusters. In particular, you need AWS CLI to configure credentials, but you also need it with other AWS services.

Set up kubectl and eksctl – The eksctl CLI interacts with AWS to create, modify, and delete Amazon EKS clusters. Once a cluster is up, use the open source kubectl command to manage Kubernetes objects within your Amazon EKS clusters.

Set up a development environment (optional)– Consider adding the following tools:

Local deployment tool – If you’re new to Kubernetes, consider installing a local deployment tool like minikube or kind. These tools allow you to have an Amazon EKS cluster on your local machine for testing applications.

Package manager – helm is a popular package manager for Kubernetes that simplifies the installation and management of complex packages. With Helm, it’s easier to install and manage packages like the AWS Load Balancer Controller on your Amazon EKS cluster.

Set up kubectl and eksctl

Quickstart: Deploy a web app and store data

---

## Send metric and trace data with ADOT Operator

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/opentelemetry.html

**Contents:**
- Send metric and trace data with ADOT Operator

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS supports using the AWS Management Console, AWS CLI and Amazon EKS API to install and manage the AWS Distro for OpenTelemetry (ADOT) Operator. This makes it easier to enable your applications running on Amazon EKS to send metric and trace data to multiple monitoring service options like Amazon CloudWatch, Prometheus, and X-Ray.

For more information, see Getting Started with AWS Distro for OpenTelemetry using EKS Add-Ons in the AWS Distro for OpenTelemetry documentation.

---

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#windows_kubectl

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Add flexibility to plan Kubernetes version upgrades by enabling EKS extended support

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/enable-extended-support.html

**Contents:**
- Add flexibility to plan Kubernetes version upgrades by enabling EKS extended support
        - Important
- Enable EKS extended support (AWS Console)
- Enable EKS extended support (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how to set the upgrade policy of an EKS cluster to enable extended support. The upgrade policy of an EKS cluster determines what happens when a cluster reaches the end of the standard support period. If a cluster upgrade policy has extended support enabled, it will enter the extended support period at the end of the standard support period. The cluster will not be automatically upgraded at the end of the standard support period.

Clusters actually in the extended support period incur higher costs. If a cluster merely has the upgrade policy set to enable extended support, and is otherwise in the standard support period, it incurs standard costs.

If you create a cluster in the AWS console, it will have the upgrade policy set to disable extended support. If you create a cluster in another way, it will have the upgrade policy set to enable extended support. For example, clusters created with the AWS API have extended support enabled.

For more information about upgrade policies, see Cluster upgrade policy.

If you want your cluster to stay on its current Kubernetes version to take advantage of the extended support period, you must enable the extended support upgrade policy before the end of standard support period.

If you do not enable extended support, your cluster will be automatically upgraded.

Navigate to your EKS cluster in the AWS Console. Select the Overview tab on the Cluster Info page.

In the Kubernetes version settings section, select Manage.

Select Extended support and then Save changes.

Verify the AWS CLI is installed and you are logged in. Learn how to update and install the AWS CLI.

Determine the name of your EKS cluster.

Run the following command:

**Examples:**

Example 1 (unknown):
```unknown
aws eks update-cluster-config \
--name <cluster-name> \
--upgrade-policy supportType=EXTENDED
```

---

## OutpostConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_OutpostConfigRequest.html#AmazonEKS-Type-OutpostConfigRequest-outpostArns

**Contents:**
- OutpostConfigRequest
- Contents
- See Also

The configuration of your local Amazon EKS cluster on an AWS Outpost. Before creating a cluster on an Outpost, review Creating a local cluster on an Outpost in the Amazon EKS User Guide. This API isn't available for Amazon EKS clusters on the AWS cloud.

The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts. Choose an instance type based on the number of nodes that your cluster will have. For more information, see Capacity considerations in the Amazon EKS User Guide.

The instance type that you specify is used for all Kubernetes control plane instances. The instance type can't be changed after cluster creation. The control plane is not automatically scaled by Amazon EKS.

The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts. Only a single Outpost ARN is supported.

Type: Array of strings

An object representing the placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost. For more information, see Capacity considerations in the Amazon EKS User Guide.

Type: ControlPlanePlacementRequest object

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Route internet traffic with AWS Load Balancer Controller

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html

**Contents:**
- Route internet traffic with AWS Load Balancer Controller
- Install the controller
- Migrate from deprecated controller versions
- Legacy cloud provider
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The AWS Load Balancer Controller manages AWS Elastic Load Balancers for a Kubernetes cluster. You can use the controller to expose your cluster apps to the internet. The controller provisions AWS load balancers that point to cluster Service or Ingress resources. In other words, the controller creates a single IP address or DNS name that points to multiple pods in your cluster.

The controller watches for Kubernetes Ingress or Service resources. In response, it creates the appropriate AWS Elastic Load Balancing resources. You can configure the specific behavior of the load balancers by applying annotations to the Kubernetes resources. For example, you can attach AWS security groups to load balancers using annotations.

The controller provisions the following resources:

The LBC creates an AWS Application Load Balancer (ALB) when you create a Kubernetes Ingress. Review the annotations you can apply to an Ingress resource.

The LBC creates an AWS Network Load Balancer (NLB)when you create a Kubernetes service of type LoadBalancer. Review the annotations you can apply to a Service resource.

In the past, the Kubernetes network load balancer was used for instance targets, but the LBC was used for IP targets. With the AWS Load Balancer Controller version 2.3.0 or later, you can create NLBs using either target type. For more information about NLB target types, see Target type in the User Guide for Network Load Balancers.

The controller is an open-source project managed on GitHub.

Before deploying the controller, we recommend that you review the prerequisites and considerations in Route application and HTTP traffic with Application Load Balancers and Route TCP and UDP traffic with Network Load Balancers. In those topics, you will deploy a sample app that includes an AWS load balancer.

With the AWS Load Balancer Controller version 2.14.0 or later, the LBC creates an AWS Application Load Balancer (ALB) when you create a Kubernetes Gateway. Kubernetes Gateway standardizes more configuration than Ingress, which needed custom annotations for many common options. Review the configuration that you can apply to an Gateway resource. For more information about the Gateway API, see Gateway API in the Kubernetes documentation.

You can use one of the following procedures to install the AWS Load Balancer Controller:

If you are

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
LoadBalancer
```

Example 2 (unknown):
```unknown
LoadBalancer
```

Example 3 (unknown):
```unknown
type: LoadBalancer
```

Example 4 (unknown):
```unknown
spec.loadBalancerClass
```

---

## EncryptionConfig

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_EncryptionConfig.html#AmazonEKS-Type-EncryptionConfig-provider

**Contents:**
- EncryptionConfig
- Contents
- See Also

The encryption configuration for the cluster.

AWS Key Management Service (AWS KMS) key. Either the ARN or the alias can be used.

Type: Provider object

Specifies the resources to be encrypted. The only supported value is secrets.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Troubleshoot EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/auto-troubleshoot.html

**Contents:**
- Troubleshoot EKS Auto Mode
        - Note
- Node monitoring agent
- Get console output from an EC2 managed instance by using the AWS EC2 CLI
- Get node logs by using debug containers and the kubectl CLI
- View resources associated with EKS Auto Mode in the AWS Console
- View IAM Errors in your AWS account
- Troubleshoot Pod failing to schedule onto Auto Mode node
- Troubleshoot node not joining the cluster
  - Detect node connectivity issues with the VPC Reachability Analyzer

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

With EKS Auto Mode, AWS assumes more responsibility for EC2 Instances in your AWS account. EKS assumes responsibility for the container runtime on nodes, the operating system on the nodes, and certain controllers. This includes a block storage controller, a load balancing controller, and a compute controller.

You must use AWS and Kubernetes APIs to troubleshoot nodes. You can:

Use a Kubernetes NodeDiagnostic resource to retrieve node logs by using the Node monitoring agent. For more steps, see Retrieve node logs for a managed node using kubectl and S3.

Use the AWS EC2 CLI command get-console-output to retrieve console output from nodes. For more steps, see Get console output from an EC2 managed instance by using the AWS EC2 CLI.

Use Kubernetes debugging containers to retrieve node logs. For more steps, see Get node logs by using debug containers and the kubectl CLI.

EKS Auto Mode uses EC2 managed instances. You cannot directly access EC2 managed instances, including by SSH.

You might have the following problems that have solutions specific to EKS Auto Mode components:

Pods stuck in the Pending state, that aren’t being scheduled onto Auto Mode nodes. For solutions see Troubleshoot Pod failing to schedule onto Auto Mode node.

EC2 managed instances that don’t join the cluster as Kubernetes nodes. For solutions see Troubleshoot node not joining the cluster.

Errors and issues with the NodePools, PersistentVolumes, and Services that use the controllers that are included in EKS Auto Mode. For solutions see Troubleshoot included controllers in Auto Mode.

Enhanced Pod security prevents sharing volumes across Pods. For solutions see Sharing Volumes Across Pods.

You can use the following methods to troubleshoot EKS Auto Mode components:

Get console output from an EC2 managed instance by using the AWS EC2 CLI

Get node logs by using debug containers and the kubectl CLI

View resources associated with EKS Auto Mode in the AWS Console

View IAM Errors in your AWS account

Detect node connectivity issues with the VPC Reachability Analyzer

EKS Auto Mode includes the Amazon EKS node monitoring agent. You can use this agent to view troubleshooting and debugging information about nodes. The node monitoring agent publishes Kubernetes events and node conditions. For more information, see Enable node auto repair and in

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
NodeDiagnostic
```

Example 2 (unknown):
```unknown
get-console-output
```

Example 3 (unknown):
```unknown
PersistentVolumes
```

Example 4 (unknown):
```unknown
kubectl get pods -l app=<deployment-name>
```

---

## Review release notes for Kubernetes versions on standard support

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions-standard.html#al2-ami-deprecation

**Contents:**
- Review release notes for Kubernetes versions on standard support
- Kubernetes 1.34
        - Important
- Kubernetes 1.33
        - Important
- Kubernetes 1.32
        - Important
  - Anonymous authentication changes
        - Note
  - Amazon Linux 2 AMI deprecation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic gives important changes to be aware of for each Kubernetes version in standard support. When upgrading, carefully review the changes that have occurred between the old and new versions for your cluster.

Kubernetes 1.34 is now available in Amazon EKS. For more information about Kubernetes 1.34, see the official release announcement.

Containerd updated to 2.1 in Version 1.34 for launch.

If you experience any issues after upgrade, check the containerd 2.1 release notes.

AWS is not releasing an EKS-optimized Amazon Linux 2 AMI for Kubernetes 1.34.

AWS encourages you to migrate to Amazon Linux 2023. Learn how to Upgrade from Amazon Linux 2 to Amazon Linux 2023.

For more information, see Amazon Linux 2 AMI deprecation.

AppArmor is deprecated in Kubernetes 1.34.

We recommend migrating to alternative container security solutions like seccomp or Pod Security Standards.

VolumeAttributesClass (VAC) graduates to GA in Kubernetes 1.34, migrating from the beta API (storage.k8s.io/v1beta1) to the stable API (storage.k8s.io/v1).

If you use the EBS CSI driver with AWS-managed sidecar containers (from CSI Components on the ECR Gallery), volume modification will continue to work seamlessly on EKS 1.31-1.33 clusters. AWS will patch the sidecars to support beta VAC APIs until the end of EKS 1.33 standard support (July 29, 2026).

If you self-manage your CSI sidecar containers, you may need to pin to older sidecar versions on pre-1.34 clusters to maintain VAC functionality.

To use GA VolumeAttributesClass features (such as modification rollback), upgrade to EKS 1.34 or later.

Dynamic Resource Allocation (DRA) Core APIs (GA): Dynamic Resource Allocation has graduated to stable, enabling efficient management of specialized hardware like GPUs through standardized allocation interfaces - simplifying resource management for hardware accelerators and improving utilization of specialized resources.

Projected ServiceAccount Tokens for Kubelet (Beta): This enhancement improves security by using short-lived credentials for container image pulls instead of long-lived secrets - reducing the risk of credential exposure and strengthening the overall security posture of your clusters.

Pod-level Resource Requests and Limits (Beta): This feature simplifies resource management by allowing shared resource pools for multi-cont

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
storage.k8s.io/v1beta1
```

Example 2 (unknown):
```unknown
storage.k8s.io/v1
```

Example 3 (unknown):
```unknown
MutableCSINodeAllocatableCount
```

Example 4 (unknown):
```unknown
--cgroup-driver
```

---

## View Kubernetes resources in the AWS Management Console

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/view-kubernetes-resources.html#view-kubernetes-resources-permissions

**Contents:**
- View Kubernetes resources in the AWS Management Console
        - Note
- Required permissions
        - Important
  - Edit with eksctl
        - Important
  - Edit ConfigMap manually
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can view the Kubernetes resources deployed to your cluster with the AWS Management Console. You can’t view Kubernetes resources with the AWS CLI or eksctl. To view Kubernetes resources using a command-line tool, use kubectl.

To view the Resources tab and Nodes section on the Compute tab in the AWS Management Console, the IAM principal that you’re using must have specific IAM and Kubernetes permissions. For more information, see Required permissions.

Open the Amazon EKS console.

In the Clusters list, select the cluster that contains the Kubernetes resources that you want to view.

Select the Resources tab.

Select a Resource type group that you want to view resources for, such as Workloads. You see a list of resource types in that group.

Select a resource type, such as Deployments, in the Workloads group. You see a description of the resource type, a link to the Kubernetes documentation for more information about the resource type, and a list of resources of that type that are deployed on your cluster. If the list is empty, then there are no resources of that type deployed to your cluster.

Select a resource to view more information about it. Try the following examples:

Select the Workloads group, select the Deployments resource type, and then select the coredns resource. When you select a resource, you are in Structured view, by default. For some resource types, you see a Pods section in Structured view. This section lists the Pods managed by the workload. You can select any Pod listed to view information about the Pod. Not all resource types display information in Structured View. If you select Raw view in the top right corner of the page for the resource, you see the complete JSON response from the Kubernetes API for the resource.

Select the Cluster group and then select the Nodes resource type. You see a list of all nodes in your cluster. The nodes can be any Amazon EKS node type. This is the same list that you see in the Nodes section when you select the Compute tab for your cluster. Select a node resource from the list. In Structured view, you also see a Pods section. This section shows you all Pods running on the node.

To view the Resources tab and Nodes section on the Compute tab in the AWS Management Console, the IAM principal that you’re using must have specific minimum IAM and Kubernetes p

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:AccessKubernetesApi
```

Example 2 (unknown):
```unknown
111122223333
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:ListFargateProfiles",
                "eks:DescribeNodegroup",
                "eks:ListNodegroups",
                "eks:ListUpdates",
                "eks:AccessKubernetesApi",
                "eks:ListAddons",
                "eks:DescribeCluster",
                "eks:DescribeAddonVersions",
                "eks:ListClusters",
                "eks:ListIdentityProviderConfigs",
                "iam:ListRoles"
            ],
            "Resource": "*"
      
...
```

Example 4 (unknown):
```unknown
rolebinding
```

---

## Set up AWS CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-awscli.html

**Contents:**
- Set up AWS CLI
- To create an access key
- To configure the AWS CLI
- To get a security token
- To verify the user identity
- Next steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The AWS CLI is a command line tool for working with AWS services, including Amazon EKS. It is also used to authenticate IAM users or roles for access to the Amazon EKS cluster and other AWS resources from your local machine. To provision resources in AWS from the command line, you need to obtain an AWS access key ID and secret key to use in the command line. Then you need to configure these credentials in the AWS CLI. If you haven’t already installed the AWS CLI, see Install or update the latest version of the AWS CLI in the AWS Command Line Interface User Guide.

Sign into the AWS Management Console.

For single-user or multiple-user accounts:

Single-user account –:: In the top right, choose your AWS user name to open the navigation menu. For example, choose webadmin .

Multiple-user account –:: Choose IAM from the list of services. From the IAM Dashboard, select Users, and choose the name of the user.

Choose Security credentials.

Under Access keys, choose Create access key.

Choose Command Line Interface (CLI), then choose Next.

Choose Create access key.

Choose Download .csv file.

After installing the AWS CLI, do the following steps to configure it. For more information, see Configure the AWS CLI in the AWS Command Line Interface User Guide.

In a terminal window, enter the following command:

Optionally, you can configure a named profile, such as --profile cluster-admin. If you configure a named profile in the AWS CLI, you must always pass this flag in subsequent commands.

Enter your AWS credentials. For example:

If needed, run the following command to get a new security token for the AWS CLI. For more information, see get-session-token in the AWS CLI Command Reference.

By default, the token is valid for 15 minutes. To change the default session timeout, pass the --duration-seconds flag. For example:

This command returns the temporary security credentials for an AWS CLI session. You should see the following response output:

If needed, run the following command to verify the AWS credentials for your IAM user identity (such as ClusterAdmin) for the terminal session.

This command returns the Amazon Resource Name (ARN) of the IAM entity that’s configured for the AWS CLI. You should see the following example response output:

Set up kubectl and eksctl

Quickstart: Deploy a web app and store data

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
--profile cluster-admin
```

Example 3 (unknown):
```unknown
Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: region-code
Default output format [None]: json
```

Example 4 (unknown):
```unknown
--duration-seconds
```

---

## ConnectorConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ConnectorConfigResponse.html#AmazonEKS-Type-ConnectorConfigResponse-activationCode

**Contents:**
- ConnectorConfigResponse
- Contents
- See Also

The full description of your connected cluster.

A unique code associated with the cluster for registration purposes.

The expiration time of the connected cluster. The cluster's YAML file must be applied through the native provider.

A unique ID associated with the cluster for registration purposes.

The cluster's cloud service provider.

The Amazon Resource Name (ARN) of the role to communicate with services from the connected Kubernetes cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Send control plane logs to CloudWatch Logs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html

**Contents:**
- Send control plane logs to CloudWatch Logs
- Enable or disable control plane logs
  - AWS Management Console
  - AWS CLI
        - Note
- View cluster control plane logs
        - Note
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to CloudWatch Logs in your account. These logs make it easy for you to secure and run your clusters. You can select the exact log types you need, and logs are sent as log streams to a group for each Amazon EKS cluster in CloudWatch. You can use CloudWatch subscription filters to do real time analysis on the logs or to forward them to other services (the logs will be Base64 encoded and compressed with the gzip format). For more information, see Amazon CloudWatch logging.

You can start using Amazon EKS control plane logging by choosing which log types you want to enable for each new or existing Amazon EKS cluster. You can enable or disable each log type on a per-cluster basis using the AWS Management Console, AWS CLI (version 1.16.139 or higher), or through the Amazon EKS API. When enabled, logs are automatically sent from the Amazon EKS cluster to CloudWatch Logs in the same account.

When you use Amazon EKS control plane logging, you’re charged standard Amazon EKS pricing for each cluster that you run. You are charged the standard CloudWatch Logs data ingestion and storage costs for any logs sent to CloudWatch Logs from your clusters. You are also charged for any AWS resources, such as Amazon EC2 instances or Amazon EBS volumes, that you provision as part of your cluster.

The following cluster control plane log types are available. Each log type corresponds to a component of the Kubernetes control plane. To learn more about these components, see Kubernetes Components in the Kubernetes documentation.

Your cluster’s API server is the control plane component that exposes the Kubernetes API. If you enable API server logs when you launch the cluster, or shortly thereafter, the logs include API server flags that were used to start the API server. For more information, see kube-apiserver and the audit policy in the Kubernetes documentation.

Kubernetes audit logs provide a record of the individual users, administrators, or system components that have affected your cluster. For more information, see Auditing in the Kubernetes documentation.

Authenticator logs are unique to Amazon EKS. These logs represent the control plane component that Amazon EKS uses for Kubernetes Role Based Access Control (RBAC) auth

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
authenticator
```

Example 2 (unknown):
```unknown
controllerManager
```

Example 3 (unknown):
```unknown
aws --version
```

Example 4 (unknown):
```unknown
aws eks update-cluster-config \
    --region region-code \
    --name my-cluster \
    --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

---

## ControlPlanePlacementRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ControlPlanePlacementRequest.html#AmazonEKS-Type-ControlPlanePlacementRequest-groupName

**Contents:**
- ControlPlanePlacementRequest
- Contents
- See Also

The placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost. For more information, see Capacity considerations in the Amazon EKS User Guide.

The name of the placement group for the Kubernetes control plane instances. This setting can't be changed after cluster creation.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Migrating existing aws-auth ConfigMap entries to access entries

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/migrating-access-entries.html

**Contents:**
- Migrating existing aws-auth ConfigMap entries to access entries
        - Important
- Prerequisites
- eksctl

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

If you’ve added entries to the aws-auth ConfigMap on your cluster, we recommend that you create access entries for the existing entries in your aws-auth ConfigMap. After creating the access entries, you can remove the entries from your ConfigMap. You can’t associate access policies to entries in the aws-auth ConfigMap. If you want to associate access polices to your IAM principals, create access entries.

When a cluster is in API_AND_CONFIGMAP authentication mode and there’s a mapping for the same IAM role in both the aws-auth ConfigMap and in access entries, the role will use the access entry’s mapping for authentication. Access entries take precedence over ConfigMap entries for the same IAM principal.

Before removing existing aws-auth ConfigMap entries that were created by Amazon EKS for managed node group or a Fargate profile to your cluster, double check if the correct access entries for those specific resources exist in your Amazon EKS cluster. If you remove entries that Amazon EKS created in the ConfigMap without having the equivalent access entries, your cluster won’t function properly.

Familiarity with access entries and access policies. For more information, see Grant IAM users access to Kubernetes with EKS access entries and Associate access policies with access entries.

An existing cluster with a platform version that is at or later than the versions listed in the Prerequisites of the Grant IAM users access to Kubernetes with EKS access entries topic.

Version 0.215.0 or later of the eksctl command line tool installed on your device or AWS CloudShell. To install or update eksctl, see Installation in the eksctl documentation.

Kubernetes permissions to modify the aws-auth ConfigMap in the kube-system namespace.

An AWS Identity and Access Management role or user with the following permissions: CreateAccessEntry and ListAccessEntries. For more information, see Actions defined by Amazon Elastic Kubernetes Service in the Service Authorization Reference.

View the existing entries in your aws-auth ConfigMap. Replace my-cluster with the name of your cluster.

An example output is as follows.

Create access entries for any of the ConfigMap entries that you created returned in the previous output. When creating the access entries, make sure to specify the same values for ARN, USERNAME, GROUPS, and ACCOUN

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws-auth ConfigMap
```

Example 2 (unknown):
```unknown
API_AND_CONFIGMAP
```

Example 3 (unknown):
```unknown
kube-system
```

Example 4 (unknown):
```unknown
CreateAccessEntry
```

---

## OIDC

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_OIDC.html#AmazonEKS-Type-OIDC-issuer

**Contents:**
- OIDC
- Contents
- See Also

An object representing the OpenID Connect (OIDC) identity provider information for the cluster.

The issuer URL for the OIDC identity provider.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## RemotePodNetwork

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_RemotePodNetwork.html#AmazonEKS-Type-RemotePodNetwork-cidrs

**Contents:**
- RemotePodNetwork
- Contents
- See Also

A network CIDR that can contain pods that run Kubernetes webhooks on hybrid nodes.

These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations.

Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, 10.2.0.0/16).

It must satisfy the following requirements:

Each block must be within an IPv4 RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.

Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

A network CIDR that can contain pods that run Kubernetes webhooks on hybrid nodes.

These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations.

Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, 10.2.0.0/16).

It must satisfy the following requirements:

Each block must be within an IPv4 RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.

Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

Type: Array of strings

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

## Disable IPv6 in the EKS Pod Identity Agent

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-config-ipv6.html

**Contents:**
- Disable IPv6 in the EKS Pod Identity Agent
- AWS Management Console
- AWS CLI

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To disable IPv6 in the EKS Pod Identity Agent, add the following configuration to the Optional configuration settings of the EKS Add-on.

Open the Amazon EKS console.

In the left navigation pane, select Clusters, and then select the name of the cluster that you want to configure the add-on for.

Choose the Add-ons tab.

Select the box in the top right of the EKS Pod Identity Agent add-on box and then choose Edit.

On the Configure EKS Pod Identity Agent page:

Select the Version that you’d like to use. We recommend that you keep the same version as the previous step, and update the version and configuration in separate actions.

Expand the Optional configuration settings.

Enter the JSON key "agent": and value of a nested JSON object with a key "additionalArgs": in Configuration values. The resulting text must be a valid JSON object. If this key and value are the only data in the text box, surround the key and value with curly braces { }. The following example shows network policy is enabled:

This configuration sets the IPv4 address to be the only address used by the agent.

To apply the new configuration by replacing the EKS Pod Identity Agent pods, choose Save changes.

Amazon EKS applies changes to the EKS Add-ons by using a rollout of the Kubernetes DaemonSet for EKS Pod Identity Agent. You can track the status of the rollout in the Update history of the add-on in the AWS Management Console and with kubectl rollout status daemonset/eks-pod-identity-agent --namespace kube-system.

kubectl rollout has the following commands:

If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of Addon Update and a status of Failed will be added to the Update history of the add-on. To investigate any issues, start from the history of the rollout, and run kubectl logs on a EKS Pod Identity Agent pod to see the logs of EKS Pod Identity Agent.

If the new entry in the Update history has a status of Successful, then the rollout has completed and the add-on is using the new configuration in all of the EKS Pod Identity Agent pods.

To disable IPv6 in the EKS Pod Identity Agent, add the following configuration to the configuration values of the EKS Add-on.

Run the following AWS CLI command. Replace my-cluster with the name of your cluster and the IAM role ARN with the role that you are us

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
"additionalArgs":
```

Example 2 (unknown):
```unknown
{
    "agent": {
        "additionalArgs": {
            "-b": "169.254.170.23"
        }
    }
}
```

Example 3 (unknown):
```unknown
kubectl rollout status daemonset/eks-pod-identity-agent --namespace kube-system
```

Example 4 (unknown):
```unknown
kubectl rollout
```

---

## LogSetup

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_LogSetup.html#AmazonEKS-Type-LogSetup-enabled

**Contents:**
- LogSetup
- Contents
- See Also

An object representing the enabled or disabled Kubernetes control plane logs for your cluster.

If a log type is enabled, that log type exports its control plane logs to CloudWatch Logs . If a log type isn't enabled, that log type doesn't export its control plane logs. Each individual log type can be enabled or disabled independently.

The available cluster control plane log types.

Type: Array of strings

Valid Values: api | audit | authenticator | controllerManager | scheduler

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
api | audit | authenticator | controllerManager | scheduler
```

---

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-resources

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## ZonalShiftConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ZonalShiftConfigRequest.html#AmazonEKS-Type-ZonalShiftConfigRequest-enabled

**Contents:**
- ZonalShiftConfigRequest
- Contents
- See Also

The configuration for zonal shift for the cluster.

If zonal shift is enabled, AWS configures zonal autoshift for the cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Identity

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Identity.html#AmazonEKS-Type-Identity-oidc

**Contents:**
- Identity
- Contents
- See Also

An object representing an identity provider.

An object representing the OpenID Connect identity provider information.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-basics

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## OutpostConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_OutpostConfigRequest.html

**Contents:**
- OutpostConfigRequest
- Contents
- See Also

The configuration of your local Amazon EKS cluster on an AWS Outpost. Before creating a cluster on an Outpost, review Creating a local cluster on an Outpost in the Amazon EKS User Guide. This API isn't available for Amazon EKS clusters on the AWS cloud.

The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts. Choose an instance type based on the number of nodes that your cluster will have. For more information, see Capacity considerations in the Amazon EKS User Guide.

The instance type that you specify is used for all Kubernetes control plane instances. The instance type can't be changed after cluster creation. The control plane is not automatically scaled by Amazon EKS.

The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts. Only a single Outpost ARN is supported.

Type: Array of strings

An object representing the placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost. For more information, see Capacity considerations in the Amazon EKS User Guide.

Type: ControlPlanePlacementRequest object

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Provider

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Provider.html#AmazonEKS-Type-Provider-keyArn

**Contents:**
- Provider
- Contents
- See Also

Identifies the AWS Key Management Service (AWS KMS) key used to encrypt the secrets.

Amazon Resource Name (ARN) or alias of the KMS key. The KMS key must be symmetric and created in the same AWS Region as the cluster. If the KMS key was created in a different account, the IAM principal must have access to the KMS key. For more information, see Allowing users in other accounts to use a KMS key in the AWS Key Management Service Developer Guide.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Upgrade from Amazon Linux 2 to Amazon Linux 2023

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/al2023.html

**Contents:**
- Upgrade from Amazon Linux 2 to Amazon Linux 2023
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon EKS optimized AMIs are available in two families based on AL2 and AL2023. AL2023 is a new Linux-based operating system designed to provide a secure, stable, and high-performance environment for your cloud applications. It’s the next generation of Amazon Linux from Amazon Web Services and is available across all supported Amazon EKS versions.

AL2023 offers several improvements over AL2. For a full comparison, see Comparing AL2 and Amazon Linux 2023 in the Amazon Linux 2023 User Guide. Several packages have been added, upgraded, and removed from AL2. It’s highly recommended to test your applications with AL2023 before upgrading. For a list of all package changes in AL2023, see Package changes in Amazon Linux 2023 in the Amazon Linux 2023 Release Notes.

In addition to these changes, you should be aware of the following:

AL2023 introduces a new node initialization process nodeadm that uses a YAML configuration schema. If you’re using self-managed node groups or an AMI with a launch template, you’ll now need to provide additional cluster metadata explicitly when creating a new node group. An example of the minimum required parameters is as follows, where apiServerEndpoint, certificateAuthority, and service cidr are now required:

In AL2, the metadata from these parameters was discovered from the Amazon EKS DescribeCluster API call. With AL2023, this behavior has changed since the additional API call risks throttling during large node scale ups. This change doesn’t affect you if you’re using managed node groups without a launch template or if you’re using Karpenter. For more information on certificateAuthority and service cidr, see DescribeCluster in the Amazon EKS API Reference.

For AL2023, nodeadm also changes the format to apply parameters to the kubelet for each node using NodeConfigSpec. In AL2, this was done with the --kubelet-extra-args parameter. This is commonly used to add labels and taints to nodes. An example below shows applying maxPods and --node-labels to the node.

Amazon VPC CNI version 1.16.2 or greater is required for AL2023.

AL2023 requires IMDSv2 by default. IMDSv2 has several benefits that help improve security posture. It uses a session-oriented authentication method that requires the creation of a secret token in a simple HTTP PUT request to start the session. A session’s toke

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
apiServerEndpoint
```

Example 2 (unknown):
```unknown
certificateAuthority
```

Example 3 (unknown):
```unknown
---
apiVersion: node.eks.aws/v1alpha1
kind: NodeConfig
spec:
  cluster:
    name: my-cluster
    apiServerEndpoint: https://example.com
    certificateAuthority: Y2VydGlmaWNhdGVBdXRob3JpdHk=
    cidr: 10.100.0.0/16
```

Example 4 (unknown):
```unknown
DescribeCluster
```

---

## View metrics for Amazon EC2 Auto Scaling groups

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/enable-asg-metrics.html

**Contents:**
- View metrics for Amazon EC2 Auto Scaling groups

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS managed node groups have Amazon EC2 Auto Scaling group metrics enabled by default with no additional charge. The Auto Scaling group sends sampled data to Amazon CloudWatch every minute. These metrics can be refined by the name of the Auto Scaling groups. They give you continuous visibility into the history of the Auto Scaling group powering your managed node groups, such as changes in the size of the group over time. Auto Scaling group metrics are available in the Amazon CloudWatch or Auto Scaling console. For more information, see Monitor CloudWatch metrics for your Auto Scaling groups and instances.

With Auto Scaling group metrics collection, you’re able to monitor the scaling of managed node groups. Auto Scaling group metrics report the minimum, maximum, and desired size of an Auto Scaling group. You can create an alarm if the number of nodes in a node group falls below the minimum size, which would indicate an unhealthy node group. Tracking node group size is also useful in adjusting the maximum count so that your data plane doesn’t run out of capacity.

If you would prefer to not have these metrics collected, you can choose to disable all or only some of them. For example, you can do this to avoid noise in your CloudWatch dashboards. For more information, see Amazon CloudWatch metrics for Amazon EC2 Auto Scaling.

---

## Analyze vulnerabilities in Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/configuration-vulnerability-analysis.html

**Contents:**
- Analyze vulnerabilities in Amazon EKS
- The Center for Internet Security (CIS) benchmark for Amazon EKS
- Amazon EKS platform versions
- Operating system vulnerability list
  - AL2023 vulnerability list
  - Amazon Linux 2 vulnerability list
- Node detection with Amazon Inspector
- Cluster and node detection with Amazon GuardDuty

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Security is a critical consideration for configuring and maintaining Kubernetes clusters and applications. The following lists resources for you to analyze the security configuration of your EKS clusters, resources for you to check for vulnerabilities, and integrations with AWS services that can do that analysis for you.

The Center for Internet Security (CIS) Kubernetes Benchmark provides guidance for Amazon EKS security configurations. The benchmark:

Is applicable to Amazon EC2 nodes (both managed and self-managed) where you are responsible for security configurations of Kubernetes components.

Provides a standard, community-approved way to ensure that you have configured your Kubernetes cluster and nodes securely when using Amazon EKS.

Consists of four sections; control plane logging configuration, node security configurations, policies, and managed services.

Supports all of the Kubernetes versions currently available in Amazon EKS and can be run using kube-bench, a standard open source tool for checking configuration using the CIS benchmark on Kubernetes clusters.

To learn more, see Introducing The CIS Amazon EKS Benchmark.

For an automated aws-sample pipeline to update your node group with a CIS benchmarked AMI, see EKS-Optimized AMI Hardening Pipeline.

Amazon EKS platform versions represent the capabilities of the cluster control plane, including which Kubernetes API server flags are enabled and the current Kubernetes patch version. New clusters are deployed with the latest platform version. For details, see EKS platform-versions.

You can update an Amazon EKS cluster to newer Kubernetes versions. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version. For more information about Kubernetes versions in EKS, see Amazon EKS supported versions.

Track security or privacy events for Amazon Linux 2023 at the Amazon Linux Security Center or subscribe to the associated RSS feed. Security and privacy events include an overview of the issue affected, packages, and instructions for updating your instances to correct the issue.

Track security or privacy events for Amazon Linux 2 at the Amazon Linux Security Center or subscribe to the associated RSS feed. Security and privacy events include an overview of the issue a

*[Content truncated]*

---

## Use elastic file system storage with Amazon EFS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

**Contents:**
- Use elastic file system storage with Amazon EFS
- Considerations
- Prerequisites
        - Note
- Step 1: Create an IAM role
        - Note
  - eksctl
    - If using Pod Identities
    - If using IAM roles for service accounts
  - AWS Management Console

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon Elastic File System (Amazon EFS) provides serverless, fully elastic file storage so that you can share file data without provisioning or managing storage capacity and performance. The Amazon EFS Container Storage Interface (CSI) driver provides a CSI interface that allows Kubernetes clusters running on AWS to manage the lifecycle of Amazon EFS file systems. This topic shows you how to deploy the Amazon EFS CSI driver to your Amazon EKS cluster.

The Amazon EFS CSI driver isn’t compatible with Windows-based container images.

You can’t use dynamic provisioning for persistent volumes with Fargate nodes, but you can use static provisioning.

Dynamic provisioning requires 1.2 or later of the driver. You can use static provisioning for persistent volumes using version 1.1 of the driver on any supported Amazon EKS cluster version (see Amazon EKS supported versions).

Version 1.3.2 or later of this driver supports the Arm64 architecture, including Amazon EC2 Graviton-based instances.

Version 1.4.2 or later of this driver supports using FIPS for mounting file systems.

Take note of the resource quotas for Amazon EFS. For example, there’s a quota of 1000 access points that can be created for each Amazon EFS file system. For more information, see Amazon EFS resource quotas that you cannot change.

Starting in version 2.0.0, this driver switched from using stunnel to efs-proxy for TLS connections. When efs-proxy is used, it will open a number of threads equal to one plus the number of cores for the node it’s running on.

The Amazon EFS CSI driver isn’t compatible with Amazon EKS Hybrid Nodes.

The Amazon EFS CSI driver needs AWS Identity and Access Management (IAM) permissions.

AWS suggests using EKS Pod Identities. For more information, see Overview of setting up EKS Pod Identities.

For information about IAM roles for service accounts and setting up an IAM OpenID Connect (OIDC) provider for your cluster, see Create an IAM OIDC provider for your cluster.

Version 2.12.3 or later or version 1.27.160 or later of the AWS Command Line Interface (AWS CLI) installed and configured on your device or AWS CloudShell. To check your current version, use aws --version | cut -d / -f2 | cut -d ' ' -f1. Package managers such yum, apt-get, or Homebrew for macOS are often several versions behind the latest version of the AWS CL

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws --version | cut -d / -f2 | cut -d ' ' -f1
```

Example 2 (unknown):
```unknown
AmazonEKS_EFS_CSI_DriverRole
```

Example 3 (unknown):
```unknown
export cluster_name=my-cluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create podidentityassociation \
    --service-account-name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --permission-policy-arns arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy
```

Example 4 (unknown):
```unknown
AmazonEKS_EFS_CSI_DriverRole
```

---

## Review release notes for Kubernetes versions on extended support

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions-extended.html

**Contents:**
- Review release notes for Kubernetes versions on extended support
- Kubernetes 1.30
        - Important
- Kubernetes 1.29
        - Important
- Kubernetes 1.28

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS supports Kubernetes versions longer than they are supported upstream, with standard support for Kubernetes minor versions for 14 months from the time they are released in Amazon EKS, and extended support for Kubernetes minor versions for an additional 12 months of support (26 total months per version).

This topic gives important changes to be aware of for each Kubernetes version in extended support. When upgrading, carefully review the changes that have occurred between the old and new versions for your cluster.

Kubernetes 1.30 is now available in Amazon EKS. For more information about Kubernetes 1.30, see the official release announcement.

Starting with Amazon EKS version 1.30 or newer, any newly created managed node groups will automatically default to using Amazon Linux 2023 (AL2023) as the node operating system. Previously, new node groups would default to Amazon Linux 2 (AL2). You can continue to use AL2 by choosing it as the AMI type when creating a new node group.

For information about migrating from AL2 to AL2023, see Upgrade from Amazon Linux 2 to Amazon Linux 2023.

For more information about Amazon Linux, see Comparing AL2 and AL2023 in the Amazon Linux User Guide.

For more information about specifiying the operating system for a managed node group, see Create a managed node group for your cluster.

With Amazon EKS 1.30, the topology.k8s.aws/zone-id label is added to worker nodes. You can use Availability Zone IDs (AZ IDs) to determine the location of resources in one account relative to the resources in another account. For more information, see Availability Zone IDs for your AWS resources in the AWS RAM User Guide.

Starting with 1.30, Amazon EKS no longer includes the default annotation on the gp2 StorageClass resource applied to newly created clusters. This has no impact if you are referencing this storage class by name. You must take action if you were relying on having a default StorageClass in the cluster. You should reference the StorageClass by the name gp2. Alternatively, you can deploy the Amazon EBS recommended default storage class by setting the defaultStorageClass.enabled parameter to true when installing version 1.31.0 or later of the aws-ebs-csi-driver add-on.

The minimum required IAM policy for the Amazon EKS cluster IAM role has changed. The action ec2:DescribeAva

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
topology.k8s.aws/zone-id
```

Example 2 (unknown):
```unknown
gp2 StorageClass
```

Example 3 (unknown):
```unknown
StorageClass
```

Example 4 (unknown):
```unknown
StorageClass
```

---

## ConnectorConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ConnectorConfigResponse.html#AmazonEKS-Type-ConnectorConfigResponse-activationExpiry

**Contents:**
- ConnectorConfigResponse
- Contents
- See Also

The full description of your connected cluster.

A unique code associated with the cluster for registration purposes.

The expiration time of the connected cluster. The cluster's YAML file must be applied through the native provider.

A unique ID associated with the cluster for registration purposes.

The cluster's cloud service provider.

The Amazon Resource Name (ARN) of the role to communicate with services from the connected Kubernetes cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#macos_kubectl

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Access Amazon S3 objects with Mountpoint for Amazon S3 CSI driver

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/s3-csi.html

**Contents:**
- Access Amazon S3 objects with Mountpoint for Amazon S3 CSI driver
- Considerations
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

With the Mountpoint for Amazon S3 Container Storage Interface (CSI) driver, your Kubernetes applications can access Amazon S3 objects through a file system interface, achieving high aggregate throughput without changing any application code. Built on Mountpoint for Amazon S3, the CSI driver presents an Amazon S3 bucket as a volume that can be accessed by containers in Amazon EKS and self-managed Kubernetes clusters.

The Mountpoint for Amazon S3 CSI driver isn’t presently compatible with Windows-based container images.

The Mountpoint for Amazon S3 CSI driver isn’t presently compatible with Amazon EKS Hybrid Nodes.

The Mountpoint for Amazon S3 CSI driver doesn’t support AWS Fargate. However, containers that are running in Amazon EC2 (either with Amazon EKS or a custom Kubernetes installation) are supported.

The Mountpoint for Amazon S3 CSI driver supports only static provisioning. Dynamic provisioning, or creation of new buckets, isn’t supported.

Static provisioning refers to using an existing Amazon S3 bucket that is specified as the bucketName in the volumeAttributes in the PersistentVolume object. For more information, see Static Provisioning on GitHub.

Volumes mounted with the Mountpoint for Amazon S3 CSI driver don’t support all POSIX file-system features. For details about file-system behavior, see Mountpoint for Amazon S3 file system behavior on GitHub.

For details on deploying the driver, see Deploy the Mountpoint for Amazon S3 driver. For details on removing the driver, see Remove the Mountpoint for Amazon S3 Amazon EKS add-on.

**Examples:**

Example 1 (unknown):
```unknown
volumeAttributes
```

Example 2 (unknown):
```unknown
PersistentVolume
```

---

## ComputeConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigResponse.html#AmazonEKS-Type-ComputeConfigResponse-enabled

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

## Fetch control plane raw metrics in Prometheus format

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/view-raw-metrics.html

**Contents:**
- Fetch control plane raw metrics in Prometheus format
- Fetch metrics from the API server
- Fetch control plane metrics with metrics.eks.amazonaws.com
        - Note
  - Fetch kube-scheduler metrics
  - Fetch kube-controller-manager metrics
  - Understand the scheduler and controller manager metrics
- Deploy a Prometheus scraper to consistently scrape metrics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Kubernetes control plane exposes a number of metrics that are represented in a Prometheus format. These metrics are useful for monitoring and analysis. They are exposed internally through metrics endpoints, and can be accessed without fully deploying Prometheus. However, deploying Prometheus more easily allows analyzing metrics over time.

To view the raw metrics output, replace endpoint and run the following command.

This command allows you to pass any endpoint path and returns the raw response. The output lists different metrics line-by-line, with each line including a metric name, tags, and a value.

The general API server endpoint is exposed on the Amazon EKS control plane. This endpoint is primarily useful when looking at a specific metric.

An example output is as follows.

This raw output returns verbatim what the API server exposes.

For clusters that are Kubernetes version 1.28 and above, Amazon EKS also exposes metrics under the API group metrics.eks.amazonaws.com. These metrics include control plane components such as kube-scheduler and kube-controller-manager.

If you have a webhook configuration that could block the creation of the new APIService resource v1.metrics.eks.amazonaws.com on your cluster, the metrics endpoint feature might not be available. You can verify that in the kube-apiserver audit log by searching for the v1.metrics.eks.amazonaws.com keyword.

To retrieve kube-scheduler metrics, use the following command.

An example output is as follows.

To retrieve kube-controller-manager metrics, use the following command.

An example output is as follows.

The following table describes the scheduler and controller manager metrics that are made available for Prometheus style scraping. For more information about these metrics, see Kubernetes Metrics Reference in the Kubernetes documentation.

scheduler_pending_pods

The number of Pods that are waiting to be scheduled onto a node for execution.

scheduler_schedule_attempts_total

The number of attempts made to schedule Pods.

scheduler_preemption_attempts_total

The number of attempts made by the scheduler to schedule higher priority Pods by evicting lower priority ones.

scheduler_preemption_victims

The number of Pods that have been selected for eviction to make room for higher priority Pods.

scheduler_pod_scheduling_attempts

The numb

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
kubectl get --raw endpoint
```

Example 2 (unknown):
```unknown
metric_name{tag="value"[,...]} value
```

Example 3 (unknown):
```unknown
kubectl get --raw /metrics
```

Example 4 (unknown):
```unknown
[...]
# HELP rest_client_requests_total Number of HTTP requests, partitioned by status code, method, and host.
# TYPE rest_client_requests_total counter
rest_client_requests_total{code="200",host="127.0.0.1:21362",method="POST"} 4994
rest_client_requests_total{code="200",host="127.0.0.1:443",method="DELETE"} 1
rest_client_requests_total{code="200",host="127.0.0.1:443",method="GET"} 1.326086e+06
rest_client_requests_total{code="200",host="127.0.0.1:443",method="PUT"} 862173
rest_client_requests_total{code="404",host="127.0.0.1:443",method="GET"} 2
rest_client_requests_total{code="409",host="127
...
```

---

## Troubleshoot Amazon EKS Connector issues

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting-connector.html

**Contents:**
- Troubleshoot Amazon EKS Connector issues
- Basic troubleshooting
  - Check Amazon EKS Connector status
  - Inspect Amazon EKS Connector logs
  - Get the effective cluster name
  - Miscellaneous commands
- Helm issue: 403 Forbidden
- Console error: the cluster is stuck in the Pending state
- Console error: User system:serviceaccount:eks-connector:eks-connector can’t impersonate resource users in API group at cluster scope
- Console error: […​] is forbidden: User […​] cannot list resource […​] in API group at the cluster scope

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers some of the common errors that you might encounter while using the Amazon EKS Connector, including instructions on how to resolve them and workarounds.

This section describes steps to diagnose Amazon EKS Connector issues.

To check the Amazon EKS Connector status, type:

The Amazon EKS Connector Pod consists of three containers. To retrieve full logs for all of these containers so that you can inspect them, run the following commands:

Amazon EKS clusters are uniquely identified by clusterName within a single AWS account and AWS Region. If you have multiple connected clusters in Amazon EKS, you can confirm which Amazon EKS cluster that the current Kubernetes cluster is registered to. To do this, enter the following to find out the clusterName of the current cluster.

The following commands are useful to retrieve information that you need to troubleshoot issues.

Use the following command to gather images that’s used by Pods in Amazon EKS Connector.

Use the following command to determine the node names that Amazon EKS Connector is running on.

Run the following command to get your Kubernetes client and server versions.

Run the following command to get information about your nodes.

If you received the following error when running helm install commands:

You can run the following line to fix it:

If the cluster gets stuck in the Pending state on the Amazon EKS console after you’re registered it, it might be because the Amazon EKS Connector didn’t successfully connect the cluster to AWS yet. For a registered cluster, the Pending state means that the connection isn’t successfully established. To resolve this issue, make sure that you have applied the manifest to the target Kubernetes cluster. If you applied it to the cluster, but the cluster is still in the Pending state, then the eks-connector statefulset might be unhealthy. To troubleshoot this issue, see Amazon EKS connector Pods are crash loopingin this topic.

The Amazon EKS Connector uses Kubernetes user impersonation to act on behalf of IAM principals from the AWS Management Console. Each principal that accesses the Kubernetes API from the AWS eks-connector service account must be granted permission to impersonate the corresponding Kubernetes user with an IAM ARN as its Kubernetes user name. In the following examples, the IAM ARN is map

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
kubectl get pods -n eks-connector
```

Example 2 (unknown):
```unknown
connector-init
```

Example 3 (unknown):
```unknown
kubectl logs eks-connector-0 --container connector-init -n eks-connector
kubectl logs eks-connector-1 --container connector-init -n eks-connector
```

Example 4 (unknown):
```unknown
connector-proxy
```

---

## UpgradePolicyRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_UpgradePolicyRequest.html

**Contents:**
- UpgradePolicyRequest
- Contents
- See Also

The support policy to use for the cluster. Extended support allows you to remain on specific Kubernetes versions for longer. Clusters in extended support have higher costs. The default value is EXTENDED. Use STANDARD to disable extended support.

Learn more about EKS Extended Support in the Amazon EKS User Guide.

If the cluster is set to EXTENDED, it will enter extended support at the end of standard support. If the cluster is set to STANDARD, it will be automatically upgraded at the end of standard support.

Learn more about EKS Extended Support in the Amazon EKS User Guide.

Valid Values: STANDARD | EXTENDED

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
STANDARD | EXTENDED
```

---

## Learn about Amazon EKS Auto Mode Managed instances

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/automode-learn-instances.html

**Contents:**
- Learn about Amazon EKS Auto Mode Managed instances
- Comparison table
  - AMI Support
- EKS Auto Mode supported instance reference
- Instance Metadata Service
- Considerations

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic explains how Amazon EKS Auto Mode manages Amazon EC2 instances in your EKS cluster. When you enable EKS Auto Mode, your cluster’s compute resources are automatically provisioned and managed by EKS, changing how you interact with the EC2 instances that serve as nodes in your cluster.

Understanding how Amazon EKS Auto Mode manages instances is essential for planning your workload deployment strategy and operational procedures. Unlike traditional EC2 instances or managed node groups, these instances follow a different lifecycle model where EKS assumes responsibility for many operational aspects, while restricting certain types of access and customization.

Amazon EKS Auto Mode automates routine tasks for creating new EC2 Instances, and attaches them as nodes to your EKS cluster. EKS Auto Mode detects when a workload can’t fit onto existing nodes, and creates a new EC2 Instance.

Amazon EKS Auto Mode is responsible for creating, deleting, and patching EC2 Instances. You are responsible for the containers and pods deployed on the instance.

EC2 Instances created by EKS Auto Mode are different from other EC2 Instances, they are managed instances. These managed instances are owned by EKS and are more restricted. You can’t directly access or install software on instances managed by EKS Auto Mode.

AWS suggests running either EKS Auto Mode or self-managed Karpenter. You can install both during a migration or in an advanced configuration. If you have both installed, configure your node pools so that workloads are associated with either Karpenter or EKS Auto Mode.

For more information, see Amazon EC2 managed instances in the Amazon EC2 user guide.

You are responsible for patching and updating the instance.

AWS automatically patches and updates the instance.

EKS is not responsible for the software on the instance.

EKS is responsible for certain software on the instance, such as kubelet, the container runtime, and the operating system.

You can delete the EC2 Instance using the EC2 API.

EKS determines the number of instances deployed in your account. If you delete a workload, EKS will reduce the number of instances in your account.

You can use SSH to access the EC2 Instance.

You can deploy pods and containers to the managed instance.

You determine the operating system and image (AMI).

AWS determines t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
hostNetwork: true
```

Example 2 (unknown):
```unknown
ephemeralStorage.size
```

Example 3 (unknown):
```unknown
ec2:RebootInstances
```

Example 4 (unknown):
```unknown
ec2:SendSpotInstanceInterruptions
```

---

## StorageConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_StorageConfigRequest.html#AmazonEKS-Type-StorageConfigRequest-blockStorage

**Contents:**
- StorageConfigRequest
- Contents
- See Also

Request to update the configuration of the storage capability of your EKS Auto Mode cluster. For example, enable the capability. For more information, see EKS Auto Mode block storage capability in the Amazon EKS User Guide.

Request to configure EBS Block Storage settings for your EKS Auto Mode cluster.

Type: BlockStorage object

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-resources-console

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## View Amazon EKS platform versions for each Kubernetes version

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html

**Contents:**
- View Amazon EKS platform versions for each Kubernetes version
        - Note
- Kubernetes version 1.34
- Kubernetes version 1.33
- Kubernetes version 1.32
- Kubernetes version 1.31
- Kubernetes version 1.30
- Kubernetes version 1.29
- Kubernetes version 1.28
- Get current platform version

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS platform versions represent the capabilities of the Amazon EKS cluster control plane, such as which Kubernetes API server flags are enabled, as well as the current Kubernetes patch version. Each Kubernetes minor version has one or more associated Amazon EKS platform versions. The platform versions for different Kubernetes minor versions are independent. You can retrieve your cluster’s current platform version using the AWS CLI or AWS Management Console. If you have a local cluster on AWS Outposts, see Learn Kubernetes and Amazon EKS platform versions for AWS Outposts instead of this topic.

When a new Kubernetes minor version is available in Amazon EKS, such as 1.33, the initial Amazon EKS platform version for that Kubernetes minor version starts at eks.1. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes.

When new Amazon EKS platform versions become available for a minor version:

The Amazon EKS platform version number is incremented (eks.<n+1>).

Amazon EKS automatically upgrades all existing clusters to the latest Amazon EKS platform version for their corresponding Kubernetes minor version. Automatic upgrades of existing Amazon EKS platform versions are rolled out incrementally. The roll-out process might take some time. If you need the latest Amazon EKS platform version features immediately, you should create a new Amazon EKS cluster.

If your cluster is more than two platform versions behind the current platform version, then it’s possible that Amazon EKS wasn’t able to automatically update your cluster. For details of what may cause this, see Amazon EKS platform version is more than two versions behind the current platform version.

Amazon EKS might publish a new node AMI with a corresponding patch version. However, all patch versions are compatible between the EKS control plane and node AMIs for a given Kubernetes minor version.

New Amazon EKS platform versions don’t introduce breaking changes or cause service interruptions.

Clusters are always created with the latest available Amazon EKS platform version (eks.<n>) for the specified Kubernetes version. If you update your cluster to a new Kubernetes minor version, your cluster receives the current Amazon EKS platform version for the Kubernetes minor 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
https://github.com/awsdocs/amazon-eks-user-guide/commits/mainline/latest/ug/clusters/platform-versions.adoc.atom
```

Example 2 (unknown):
```unknown
NodeRestriction
```

Example 3 (unknown):
```unknown
ExtendedResourceToleration
```

Example 4 (unknown):
```unknown
NamespaceLifecycle
```

---

## EncryptionConfig

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_EncryptionConfig.html

**Contents:**
- EncryptionConfig
- Contents
- See Also

The encryption configuration for the cluster.

AWS Key Management Service (AWS KMS) key. Either the ARN or the alias can be used.

Type: Provider object

Specifies the resources to be encrypted. The only supported value is secrets.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#eksctl-install-update

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Configure EKS Auto Mode settings

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/settings-auto.html

**Contents:**
- Configure EKS Auto Mode settings

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This chapter describes how to configure specific aspects of your Amazon Elastic Kubernetes Service (EKS) Auto Mode clusters. While EKS Auto Mode manages most infrastructure components automatically, you can customize certain features to meet your workload requirements.

Using the configuration options described in this topic, you can modify networking settings, compute resources, and load balancing behaviors while maintaining the benefits of automated infrastructure management. Before making any configuration changes, review the available options in the following sections to determine which approach best suits your needs.

Node networking and storage

Configure node placement across public and private subnets

Define custom security groups for node access control

Customize network address translation (SNAT) policies

Enable Kubernetes network policies, detailed network policy logging and monitoring

Set ephemeral storage parameters (size, IOPS, throughput)

Configure encrypted ephemeral storage with custom KMS keys

Isolate pod traffic in separate subnets from the nodes

Create a Node Class for Amazon EKS

Node compute resources

Select specific EC2 instance types and families

Define CPU architectures (x86_64, ARM64)

Configure capacity types (On-Demand, Spot)

Specify Availability Zones

Configure node taints and labels

Set resource limits for CPU and memory usage

Create a Node Pool for EKS Auto Mode

Application Load Balancer settings

Deploy internal or internet-facing load balancers

Configure cross-zone load balancing

Set idle timeout periods

Enable HTTP/2 and WebSocket support

Configure health check parameters

Specify TLS certificate settings

Define target group attributes

Set IP address type (IPv4, dual-stack)

Create an IngressClass to configure an Application Load Balancer

Network Load Balancer settings

Configure direct pod IP routing

Enable cross-zone load balancing

Set connection idle timeout

Configure health check parameters

Specify subnet placement

Set IP address type (IPv4, dual-stack)

Configure preserve client source IP

Define target group attributes

Use Service Annotations to configure Network Load Balancers

Storage Class settings

Define EBS volume types (gp3, io1, io2, etc.)

Configure volume encryption and KMS key usage

Set IOPS and throughput parameters

Set as default

*[Content truncated]*

---

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#kubectl-install-update

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Logging

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Logging.html

**Contents:**
- Logging
- Contents
- See Also

An object representing the logging configuration for resources in your cluster.

The cluster control plane logging configuration for your cluster.

Type: Array of LogSetup objects

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-resources-api-sdk

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Enable EKS zonal shift to avoid impaired Availability Zones

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/zone-shift-enable.html

**Contents:**
- Enable EKS zonal shift to avoid impaired Availability Zones
- Considerations
- What is Amazon Application Recovery Controller?
- What is zonal shift?
- What is zonal autoshift?
- What does EKS do during an autoshift?
- Register EKS cluster with Amazon Application Recovery Controller (ARC) (AWS console)
- Next Steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon Application Recovery Controller (ARC) helps you manage and coordinate recovery for your applications across Availability Zones (AZs) and works with many services, including Amazon EKS. With EKS support for ARC zonal shift, you can shift in-cluster network traffic away from an impaired AZ. You can also authorize AWS to monitor the health of your AZs and temporarily shift network traffic away from an unhealthy AZ on your behalf.

How to use EKS zonal shift:

Enable your EKS cluster with Amazon Application Recovery Controller (ARC). This is done at the cluster level using the Amazon EKS Console, the AWS CLI, CloudFormation, or eksctl.

Once enabled, you can manage zonal shifts or zonal autoshifts using the ARC Console, the AWS CLI, or the zonal shift and zonal autoshift APIs.

Note that after you register an EKS cluster with ARC, you still need to configure ARC. For example, you can use the ARC console to configure zonal autoshift.

For more detailed information about how EKS zonal shift works, and how to design your workloads to handle impaired availability zones, see Learn about Amazon Application Recovery Controller (ARC) zonal shift in Amazon EKS.

EKS Auto Mode does not support Amazon Application Recovery Controller, zonal shift, and zonal autoshift.

We recommend waiting at least 60 seconds between zonal shift operations to ensure proper processing of each request.

When attempting to perform zonal shifts in quick succession (within 60 seconds of each other), the Amazon EKS service may not properly process all shift requests. This is due to the current polling mechanism that updates the cluster’s zonal state. If you need to perform multiple zonal shifts, ensure there is adequate time between operations for the system to process each change.

Amazon Application Recovery Controller (ARC) helps you prepare for and accomplish faster recovery for applications running on AWS. Zonal shift enables you to quickly recover from Availability Zone (AZ) impairments, by temporarily moving traffic for a supported resource away from an AZ, to healthy AZs in the AWS Region.

Learn more about Amazon Application Recovery Controller (ARC)

Zonal shift is a capability in ARC that allows you to move traffic for a resource like an EKS cluster or an Elastic Load Balancer away from an Availability Zone in an AWS Region to qui

*[Content truncated]*

---

## RemoteNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_RemoteNetworkConfigRequest.html#AmazonEKS-Type-RemoteNetworkConfigRequest-remotePodNetworks

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

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-restrictions

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## Certificate

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_Certificate.html#AmazonEKS-Type-Certificate-data

**Contents:**
- Certificate
- Contents
- See Also

An object representing the certificate-authority-data for your cluster.

The Base64-encoded certificate data required to communicate with your cluster. Add this to the certificate-authority-data section of the kubeconfig file for your cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
certificate-authority-data
```

Example 2 (unknown):
```unknown
certificate-authority-data
```

---

## Route TCP and UDP traffic with Network Load Balancers

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html

**Contents:**
- Route TCP and UDP traffic with Network Load Balancers
        - Note
- Prerequisites
- Considerations
- Create a network load balancer
  - Create network load balancer — IP Targets
        - Note
        - Note
        - Important
  - Create network load balancer — Instance Targets

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

New: Amazon EKS Auto Mode automates routine tasks for load balancing. For more information, see:

Deploy a Sample Load Balancer Workload to EKS Auto Mode

Use Service Annotations to configure Network Load Balancers

Network traffic is load balanced at L4 of the OSI model. To load balance application traffic at L7, you deploy a Kubernetes ingress, which provisions an AWS Application Load Balancer. For more information, see Route application and HTTP traffic with Application Load Balancers. To learn more about the differences between the two types of load balancing, see Elastic Load Balancing features on the AWS website.

When you create a Kubernetes Service of type LoadBalancer, the AWS cloud provider load balancer controller creates AWS Classic Load Balancers by default, but can also create AWS Network Load Balancers. This controller is only receiving critical bug fixes in the future. For more information about using the AWS cloud provider load balancer , see AWS cloud provider load balancer controller in the Kubernetes documentation. Its use is not covered in this topic.

We recommend that you use version 2.7.2 or later of the AWS Load Balancer Controller instead of the AWS cloud provider load balancer controller. The AWS Load Balancer Controller creates AWS Network Load Balancers, but doesn’t create AWS Classic Load Balancers. The remainder of this topic is about using the AWS Load Balancer Controller.

An AWS Network Load Balancer can load balance network traffic to Pods deployed to Amazon EC2 IP and instance targets, to AWS Fargate IP targets, or to Amazon EKS Hybrid Nodes as IP targets. For more information, see AWS Load Balancer Controller on GitHub.

Before you can load balance network traffic using the AWS Load Balancer Controller, you must meet the following requirements.

Have an existing cluster. If you don’t have an existing cluster, see Get started with Amazon EKS. If you need to update the version of an existing cluster, see Update existing cluster to new Kubernetes version.

Have the AWS Load Balancer Controller deployed on your cluster. For more information, see Route internet traffic with AWS Load Balancer Controller. We recommend version 2.7.2 or later.

At least one subnet. If multiple tagged subnets are found in an Availability Zone, the controller chooses the first subnet whose subnet ID c

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
LoadBalancer
```

Example 2 (unknown):
```unknown
kubernetes.io/cluster/<my-cluster>
```

Example 3 (unknown):
```unknown
kubernetes.io/role/internal-elb
```

Example 4 (unknown):
```unknown
kubernetes.io/role/elb
```

---

## TagResource

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html

**Contents:**
- TagResource
- Request Syntax
- URI Request Parameters
- Request Body
- Response Syntax
- Response Elements
- Errors
- See Also

Associates the specified tags to an Amazon EKS resource with the specified resourceArn. If existing tags on a resource are not specified in the request parameters, they aren't changed. When a resource is deleted, the tags associated with that resource are also deleted. Tags that you create for Amazon EKS resources don't propagate to any other resources associated with the cluster. For example, if you tag a cluster with this operation, that tag doesn't automatically propagate to the subnets and nodes associated with the cluster.

The request uses the following URI parameters.

The Amazon Resource Name (ARN) of the resource to add tags to.

The request accepts the following data in JSON format.

Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

Type: String to string map

Map Entries: Maximum number of 50 items.

Key Length Constraints: Minimum length of 1. Maximum length of 128.

Value Length Constraints: Maximum length of 256.

If the action is successful, the service sends back an HTTP 200 response with an empty HTTP body.

For information about the errors that are common to all actions, see Common Errors.

This exception is thrown if the request contains a semantic error. The precise meaning will depend on the API, and will be documented in the error message.

This exception is thrown if the request contains a semantic error. The precise meaning will depend on the API, and will be documented in the error message.

HTTP Status Code: 400

A service resource associated with the request could not be found. Clients should not retry such requests.

A service resource associated with the request could not be found. Clients should not retry such requests.

HTTP Status Code: 404

For more information about using this API in one of the language-specific AWS SDKs, see the following:

AWS Command Line Interface V2

AWS SDK for JavaScript V3

**Examples:**

Example 1 (unknown):
```unknown
resourceArn
```

Example 2 (unknown):
```unknown
POST /tags/resourceArn HTTP/1.1
Content-type: application/json

{
   "tags": {
      "string" : "string"
   }
}
```

Example 3 (unknown):
```unknown
resourceArn
```

Example 4 (unknown):
```unknown
HTTP/1.1 200
```

---

## KubernetesNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_KubernetesNetworkConfigRequest.html#AmazonEKS-Type-KubernetesNetworkConfigRequest-ipFamily

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

## RemoteNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_RemoteNetworkConfigRequest.html

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

## KubernetesNetworkConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_KubernetesNetworkConfigResponse.html#AmazonEKS-Type-KubernetesNetworkConfigResponse-elasticLoadBalancing

**Contents:**
- KubernetesNetworkConfigResponse
- Contents
- See Also

The Kubernetes network configuration for the cluster. The response contains a value for serviceIpv6Cidr or serviceIpv4Cidr, but not both.

Indicates the current configuration of the load balancing capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled.

Type: ElasticLoadBalancing object

The IP family used to assign Kubernetes Pod and Service objects IP addresses. The IP family is always ipv4, unless you have a 1.21 or later cluster running version 1.10.1 or later of the Amazon VPC CNI plugin for Kubernetes and specified ipv6 when you created the cluster.

Valid Values: ipv4 | ipv6

The CIDR block that Kubernetes Pod and Service object IP addresses are assigned from. Kubernetes assigns addresses from an IPv4 CIDR block assigned to a subnet that the node is in. If you didn't specify a CIDR block when you created the cluster, then Kubernetes assigns addresses from either the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks. If this was specified, then it was specified when the cluster was created and it can't be changed.

The CIDR block that Kubernetes pod and service IP addresses are assigned from if you created a 1.21 or later cluster with version 1.10.1 or later of the Amazon VPC CNI add-on and specified ipv6 for ipFamily when you created the cluster. Kubernetes assigns service addresses from the unique local address range (fc00::/7) because you can't specify a custom IPv6 CIDR block when you create the cluster.

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

---

## View Kubernetes resources in the AWS Management Console

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/view-kubernetes-resources.html

**Contents:**
- View Kubernetes resources in the AWS Management Console
        - Note
- Required permissions
        - Important
  - Edit with eksctl
        - Important
  - Edit ConfigMap manually
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can view the Kubernetes resources deployed to your cluster with the AWS Management Console. You can’t view Kubernetes resources with the AWS CLI or eksctl. To view Kubernetes resources using a command-line tool, use kubectl.

To view the Resources tab and Nodes section on the Compute tab in the AWS Management Console, the IAM principal that you’re using must have specific IAM and Kubernetes permissions. For more information, see Required permissions.

Open the Amazon EKS console.

In the Clusters list, select the cluster that contains the Kubernetes resources that you want to view.

Select the Resources tab.

Select a Resource type group that you want to view resources for, such as Workloads. You see a list of resource types in that group.

Select a resource type, such as Deployments, in the Workloads group. You see a description of the resource type, a link to the Kubernetes documentation for more information about the resource type, and a list of resources of that type that are deployed on your cluster. If the list is empty, then there are no resources of that type deployed to your cluster.

Select a resource to view more information about it. Try the following examples:

Select the Workloads group, select the Deployments resource type, and then select the coredns resource. When you select a resource, you are in Structured view, by default. For some resource types, you see a Pods section in Structured view. This section lists the Pods managed by the workload. You can select any Pod listed to view information about the Pod. Not all resource types display information in Structured View. If you select Raw view in the top right corner of the page for the resource, you see the complete JSON response from the Kubernetes API for the resource.

Select the Cluster group and then select the Nodes resource type. You see a list of all nodes in your cluster. The nodes can be any Amazon EKS node type. This is the same list that you see in the Nodes section when you select the Compute tab for your cluster. Select a node resource from the list. In Structured view, you also see a Pods section. This section shows you all Pods running on the node.

To view the Resources tab and Nodes section on the Compute tab in the AWS Management Console, the IAM principal that you’re using must have specific minimum IAM and Kubernetes p

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:AccessKubernetesApi
```

Example 2 (unknown):
```unknown
111122223333
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:ListFargateProfiles",
                "eks:DescribeNodegroup",
                "eks:ListNodegroups",
                "eks:ListUpdates",
                "eks:AccessKubernetesApi",
                "eks:ListAddons",
                "eks:DescribeCluster",
                "eks:DescribeAddonVersions",
                "eks:ListClusters",
                "eks:ListIdentityProviderConfigs",
                "iam:ListRoles"
            ],
            "Resource": "*"
      
...
```

Example 4 (unknown):
```unknown
rolebinding
```

---

## ElasticLoadBalancing

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ElasticLoadBalancing.html#AmazonEKS-Type-ElasticLoadBalancing-enabled

**Contents:**
- ElasticLoadBalancing
- Contents
- See Also

Indicates the current configuration of the load balancing capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. For more information, see EKS Auto Mode load balancing capability in the Amazon EKS User Guide.

Indicates if the load balancing capability is enabled on your EKS Auto Mode cluster. If the load balancing capability is enabled, EKS Auto Mode will create and delete load balancers in your AWS account.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## EncryptionConfig

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_EncryptionConfig.html#AmazonEKS-Type-EncryptionConfig-resources

**Contents:**
- EncryptionConfig
- Contents
- See Also

The encryption configuration for the cluster.

AWS Key Management Service (AWS KMS) key. Either the ARN or the alias can be used.

Type: Provider object

Specifies the resources to be encrypted. The only supported value is secrets.

Type: Array of strings

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Use high-performance app storage with FSx for NetApp ONTAP

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/fsx-ontap.html

**Contents:**
- Use high-performance app storage with FSx for NetApp ONTAP
        - Important

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The NetApp Trident provides dynamic storage orchestration using a Container Storage Interface (CSI) compliant driver. This allows Amazon EKS clusters to manage the lifecycle of persistent volumes (PVs) backed by Amazon FSx for NetApp ONTAP file systems. Note that the Amazon FSx for NetApp ONTAP CSI driver is not compatible with Amazon EKS Hybrid Nodes. To get started, see Use Trident with Amazon FSx for NetApp ONTAP in the NetApp Trident documentation.

Amazon FSx for NetApp ONTAP is a storage service that allows you to launch and run fully managed ONTAP file systems in the cloud. ONTAP is NetApp’s file system technology that provides a widely adopted set of data access and data management capabilities. FSx for ONTAP provides the features, performance, and APIs of on-premises NetApp file systems with the agility, scalability, and simplicity of a fully managed AWS service. For more information, see the FSx for ONTAP User Guide.

If you are using Amazon FSx for NetApp ONTAP alongside the Amazon EBS CSI driver to provision EBS volumes, you must specify to not use EBS devices in the multipath.conf file. For supported methods, see Configuration File Blacklist. Here is an example.

**Examples:**

Example 1 (unknown):
```unknown
multipath.conf
```

Example 2 (unknown):
```unknown
 defaults {
        user_friendly_names yes
        find_multipaths no
      }
      blacklist {
        device {
          vendor "NVME"
          product "Amazon Elastic Block Store"
        }
      }
```

---

## KubernetesNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_KubernetesNetworkConfigRequest.html

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

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#linux_arm64_kubectl

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Send control plane logs to CloudWatch Logs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html#control-plane-cli

**Contents:**
- Send control plane logs to CloudWatch Logs
- Enable or disable control plane logs
  - AWS Management Console
  - AWS CLI
        - Note
- View cluster control plane logs
        - Note
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to CloudWatch Logs in your account. These logs make it easy for you to secure and run your clusters. You can select the exact log types you need, and logs are sent as log streams to a group for each Amazon EKS cluster in CloudWatch. You can use CloudWatch subscription filters to do real time analysis on the logs or to forward them to other services (the logs will be Base64 encoded and compressed with the gzip format). For more information, see Amazon CloudWatch logging.

You can start using Amazon EKS control plane logging by choosing which log types you want to enable for each new or existing Amazon EKS cluster. You can enable or disable each log type on a per-cluster basis using the AWS Management Console, AWS CLI (version 1.16.139 or higher), or through the Amazon EKS API. When enabled, logs are automatically sent from the Amazon EKS cluster to CloudWatch Logs in the same account.

When you use Amazon EKS control plane logging, you’re charged standard Amazon EKS pricing for each cluster that you run. You are charged the standard CloudWatch Logs data ingestion and storage costs for any logs sent to CloudWatch Logs from your clusters. You are also charged for any AWS resources, such as Amazon EC2 instances or Amazon EBS volumes, that you provision as part of your cluster.

The following cluster control plane log types are available. Each log type corresponds to a component of the Kubernetes control plane. To learn more about these components, see Kubernetes Components in the Kubernetes documentation.

Your cluster’s API server is the control plane component that exposes the Kubernetes API. If you enable API server logs when you launch the cluster, or shortly thereafter, the logs include API server flags that were used to start the API server. For more information, see kube-apiserver and the audit policy in the Kubernetes documentation.

Kubernetes audit logs provide a record of the individual users, administrators, or system components that have affected your cluster. For more information, see Auditing in the Kubernetes documentation.

Authenticator logs are unique to Amazon EKS. These logs represent the control plane component that Amazon EKS uses for Kubernetes Role Based Access Control (RBAC) auth

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
authenticator
```

Example 2 (unknown):
```unknown
controllerManager
```

Example 3 (unknown):
```unknown
aws --version
```

Example 4 (unknown):
```unknown
aws eks update-cluster-config \
    --region region-code \
    --name my-cluster \
    --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

---

## Create an Amazon EKS add-on

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/creating-an-add-on.html#_create_add_on_console

**Contents:**
- Create an Amazon EKS add-on
- Prerequisites
- Procedure
- Create add-on (eksctl)
- Create add-on (AWS Console)
- Create add-on (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS add-ons are add-on software for Amazon EKS clusters. All Amazon EKS add-ons:

Include the latest security patches and bug fixes.

Are validated by AWS to work with Amazon EKS.

Reduce the amount of work required to manage the add-on software.

You can create an Amazon EKS add-on using eksctl, the AWS Management Console, or the AWS CLI. If the add-on requires an IAM role, see the details for the specific add-on in Amazon EKS add-ons for details about creating the role.

Complete the following before you create an add-on:

The cluster must exist before you create an add-on for it. For more information, see Create an Amazon EKS cluster.

Check if your add-on requires an IAM role. For more information, see Verify Amazon EKS add-on version compatibility with a cluster.

Verify that the Amazon EKS add-on version is compatabile with your cluster. For more information, see Verify Amazon EKS add-on version compatibility with a cluster.

Verify that version 0.190.0 or later of the eksctl command line tool installed on your computer or AWS CloudShell. For more information, see Installation on the eksctl website.

You can create an Amazon EKS add-on using eksctl, the AWS Management Console, or the AWS CLI. If the add-on requires an IAM role, see the details for the specific add-on in Available Amazon EKS add-ons from AWS for details about creating the role.

View the names of add-ons available for a cluster version. Replace 1.33 with the version of your cluster.

An example output is as follows.

View the versions available for the add-on that you would like to create. Replace 1.33 with the version of your cluster. Replace name-of-addon with the name of the add-on you want to view the versions for. The name must be one of the names returned in the previous step.

The following output is an example of what is returned for the add-on named vpc-cni. You can see that the add-on has several available versions.

Determine whether the add-on you want to create is an Amazon EKS or AWS Marketplace add-on. The AWS Marketplace has third party add-ons that require you to complete additional steps to create the add-on.

If no output is returned, then the add-on is an Amazon EKS. If output is returned, then the add-on is an AWS Marketplace add-on. The following output is for an add-on named teleport_teleport.

You can learn 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eksctl utils describe-addon-versions --kubernetes-version 1.33 | grep AddonName
```

Example 2 (unknown):
```unknown
"AddonName": "aws-ebs-csi-driver",
                        "AddonName": "coredns",
                        "AddonName": "kube-proxy",
                        "AddonName": "vpc-cni",
                        "AddonName": "adot",
                        "AddonName": "dynatrace_dynatrace-operator",
                        "AddonName": "upbound_universal-crossplane",
                        "AddonName": "teleport_teleport",
                        "AddonName": "factorhouse_kpow",
                        [...]
```

Example 3 (unknown):
```unknown
name-of-addon
```

Example 4 (unknown):
```unknown
eksctl utils describe-addon-versions --kubernetes-version 1.33 --name name-of-addon | grep AddonVersion
```

---

## Review release notes for Kubernetes versions on standard support

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions-standard.html

**Contents:**
- Review release notes for Kubernetes versions on standard support
- Kubernetes 1.34
        - Important
- Kubernetes 1.33
        - Important
- Kubernetes 1.32
        - Important
  - Anonymous authentication changes
        - Note
  - Amazon Linux 2 AMI deprecation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic gives important changes to be aware of for each Kubernetes version in standard support. When upgrading, carefully review the changes that have occurred between the old and new versions for your cluster.

Kubernetes 1.34 is now available in Amazon EKS. For more information about Kubernetes 1.34, see the official release announcement.

Containerd updated to 2.1 in Version 1.34 for launch.

If you experience any issues after upgrade, check the containerd 2.1 release notes.

AWS is not releasing an EKS-optimized Amazon Linux 2 AMI for Kubernetes 1.34.

AWS encourages you to migrate to Amazon Linux 2023. Learn how to Upgrade from Amazon Linux 2 to Amazon Linux 2023.

For more information, see Amazon Linux 2 AMI deprecation.

AppArmor is deprecated in Kubernetes 1.34.

We recommend migrating to alternative container security solutions like seccomp or Pod Security Standards.

VolumeAttributesClass (VAC) graduates to GA in Kubernetes 1.34, migrating from the beta API (storage.k8s.io/v1beta1) to the stable API (storage.k8s.io/v1).

If you use the EBS CSI driver with AWS-managed sidecar containers (from CSI Components on the ECR Gallery), volume modification will continue to work seamlessly on EKS 1.31-1.33 clusters. AWS will patch the sidecars to support beta VAC APIs until the end of EKS 1.33 standard support (July 29, 2026).

If you self-manage your CSI sidecar containers, you may need to pin to older sidecar versions on pre-1.34 clusters to maintain VAC functionality.

To use GA VolumeAttributesClass features (such as modification rollback), upgrade to EKS 1.34 or later.

Dynamic Resource Allocation (DRA) Core APIs (GA): Dynamic Resource Allocation has graduated to stable, enabling efficient management of specialized hardware like GPUs through standardized allocation interfaces - simplifying resource management for hardware accelerators and improving utilization of specialized resources.

Projected ServiceAccount Tokens for Kubelet (Beta): This enhancement improves security by using short-lived credentials for container image pulls instead of long-lived secrets - reducing the risk of credential exposure and strengthening the overall security posture of your clusters.

Pod-level Resource Requests and Limits (Beta): This feature simplifies resource management by allowing shared resource pools for multi-cont

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
storage.k8s.io/v1beta1
```

Example 2 (unknown):
```unknown
storage.k8s.io/v1
```

Example 3 (unknown):
```unknown
MutableCSINodeAllocatableCount
```

Example 4 (unknown):
```unknown
--cgroup-driver
```

---

## Organize Amazon EKS resources with tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html#tag-resources-for-billing

**Contents:**
- Organize Amazon EKS resources with tags
        - Topics
        - Note
- Tag basics
- Tagging your resources
- Tag restrictions
- Tagging your resources for billing
        - Note
- Working with tags using the console
  - Adding tags on a resource on creation

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use tags to help you manage your Amazon EKS resources. This topic provides an overview of the tags function and shows how you can create tags.

Tagging your resources

Tagging your resources for billing

Working with tags using the console

Working with tags using the CLI, API, or eksctl

Tags are a type of metadata that’s separate from Kubernetes labels and annotations. For more information about these other metadata types, see the following sections in the Kubernetes documentation:

A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value.

With tags, you can categorize your AWS resources. For example, you can categorize resources by purpose, owner, or environment. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster’s owner and stack level. We recommend that you devise a consistent set of tag keys for each resource type. You can then search and filter the resources based on the tags that you add.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time. If you delete a resource, any tags for the resource are also deleted.

Tags don’t have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters. You can set the value of a tag to an empty string. However, you can’t set the value of a tag to null. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value.

If you use AWS Identity and Access Management (IAM), you can control which users in your AWS account have permission to manage tags.

The following Amazon EKS resources support tags:

You can tag these resources using the following:

If you’re using the Amazon EKS console, you can apply tags to new or existing resources at any time. You can do this by using the Tags tab on the relevant resource page. For more information, see Working with tags using the console.

If you’re using eksctl, you can apply tags to resources when they’re created using the --tags option.

If you’re using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the tags parame

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TagResource
```

Example 2 (unknown):
```unknown
aws:eks:cluster-name
```

Example 3 (unknown):
```unknown
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

Example 4 (unknown):
```unknown
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

---

## Learn about Amazon Application Recovery Controller (ARC) zonal shift in Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/zone-shift.html

**Contents:**
- Learn about Amazon Application Recovery Controller (ARC) zonal shift in Amazon EKS
- Understanding east-west network traffic flow between Pods
  - Understanding ARC zonal shift in Amazon EKS
- EKS zonal shift requirements
  - Provision your EKS worker nodes across multiple Availability Zones
  - Provision enough compute capacity to withstand removal of a single Availability Zone
  - Run and spread multiple Pod replicas across Availability Zones
  - Colocate interdependent Pods in the same Availability Zone
  - Test that your cluster environment can handle the loss of an AZ
- Frequently asked questions

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Kubernetes has native features that enable you to make your applications more resilient to events such as the degraded health or impairment of an Availability Zone (AZ). When you run your workloads in an Amazon EKS cluster, you can further improve your application environment’s fault tolerance and application recovery by using Amazon Application Recovery Controller (ARC) zonal shift or zonal autoshift. ARC zonal shift is designed to be a temporary measure that enables you to move traffic for a resource away from an impaired AZ until the zonal shift expires or you cancel it. You can extend the zonal shift, if necessary.

You can start a zonal shift for an EKS cluster, or you can allow AWS to shift traffic for you by enabling zonal autoshift. This shift updates the flow of east-to-west network traffic in your cluster to only consider network endpoints for Pods running on worker nodes in healthy AZs. Additionally, any ALB or NLB handling ingress traffic for applications in your EKS cluster will automatically route traffic to targets in the healthy AZs. For those customers seeking the highest availability goals, in the case that an AZ becomes impaired, it can be important to be able to steer all traffic away from the impaired AZ until it recovers. For this, you can also enable an ALB or NLB with ARC zonal shift.

The following diagram illustrates two example workloads, Orders, and Products. The purpose of this example is to show how workloads and Pods in different AZs communicate.

For Orders to communicate with Products, Orders must first resolve the DNS name of the destination service. Orders communicates with CoreDNS to fetch the virtual IP address (Cluster IP) for that service. After Orders resolves the Products service name, it sends traffic to that target IP address.

The kube-proxy runs on every node in the cluster and continuously watches EndpointSlices for services. When a service is created, an EndpointSlice is created and managed in the background by the EndpointSlice controller. Each EndpointSlice has a list or table of endpoints that contains a subset of Pod addresses, along with the nodes that they’re running on. The kube-proxy sets up routing rules for each of these Pod endpoints using iptables on the nodes. The kube-proxy is also responsible for a basic form of load balancing, redirecting traffic d

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders
spec:
  replicas: 9
  selector:
    matchLabels:
      app:orders
  template:
    metadata:
      labels:
        app: orders
        tier: backend
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: "topology.kubernetes.io/zone"
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app: orders
```

Example 2 (unknown):
```unknown
replicaCount
```

Example 3 (unknown):
```unknown
topologySpreadConstraints
```

Example 4 (unknown):
```unknown
values.yaml
```

---

## ConnectorConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ConnectorConfigResponse.html#AmazonEKS-Type-ConnectorConfigResponse-provider

**Contents:**
- ConnectorConfigResponse
- Contents
- See Also

The full description of your connected cluster.

A unique code associated with the cluster for registration purposes.

The expiration time of the connected cluster. The cluster's YAML file must be applied through the native provider.

A unique ID associated with the cluster for registration purposes.

The cluster's cloud service provider.

The Amazon Resource Name (ARN) of the role to communicate with services from the connected Kubernetes cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Route application and HTTP traffic with Application Load Balancers

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html

**Contents:**
- Route application and HTTP traffic with Application Load Balancers
        - Note
- Prerequisites
        - Note
        - Note
- Reuse ALBs with Ingress Groups
        - Warning
        - Important
- (Optional) Deploy a sample application
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

New: Amazon EKS Auto Mode automates routine tasks for load balancing. For more information, see:

Deploy a Sample Load Balancer Workload to EKS Auto Mode

Create an IngressClass to configure an Application Load Balancer

When you create a Kubernetes ingress, an AWS Application Load Balancer (ALB) is provisioned that load balances application traffic. To learn more, see What is an Application Load Balancer? in the Application Load Balancers User Guide and Ingress in the Kubernetes documentation. ALBs can be used with Pods that are deployed to nodes or to AWS Fargate. You can deploy an ALB to public or private subnets.

Application traffic is balanced at L7 of the OSI model. To load balance network traffic at L4, you deploy a Kubernetes service of the LoadBalancer type. This type provisions an AWS Network Load Balancer. For more information, see Route TCP and UDP traffic with Network Load Balancers. To learn more about the differences between the two types of load balancing, see Elastic Load Balancing features on the AWS website.

Before you can load balance application traffic to an application, you must meet the following requirements.

Have an existing cluster. If you don’t have an existing cluster, see Get started with Amazon EKS. If you need to update the version of an existing cluster, see Update existing cluster to new Kubernetes version.

Have the AWS Load Balancer Controller deployed on your cluster. For more information, see Route internet traffic with AWS Load Balancer Controller. We recommend version 2.7.2 or later.

At least two subnets in different Availability Zones. The AWS Load Balancer Controller chooses one subnet from each Availability Zone. When multiple tagged subnets are found in an Availability Zone, the controller chooses the subnet whose subnet ID comes first lexicographically. Each subnet must have at least eight available IP addresses.

If you’re using multiple security groups attached to worker node, exactly one security group must be tagged as follows. Replace my-cluster with your cluster name.

Key – kubernetes.io/cluster/<my-cluster>

Value – shared or owned

If you’re using the AWS Load Balancer Controller version 2.1.1 or earlier, subnets must be tagged in the format that follows. If you’re using version 2.1.2 or later, tagging is optional. However, we recommend that you tag a s

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
LoadBalancer
```

Example 2 (unknown):
```unknown
kubernetes.io/cluster/<my-cluster>
```

Example 3 (unknown):
```unknown
kubernetes.io/cluster/<my-cluster>
```

Example 4 (unknown):
```unknown
kubernetes.io/role/internal-elb
```

---

## ComputeConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigRequest.html#AmazonEKS-Type-ComputeConfigRequest-enabled

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

## StorageConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_StorageConfigRequest.html

**Contents:**
- StorageConfigRequest
- Contents
- See Also

Request to update the configuration of the storage capability of your EKS Auto Mode cluster. For example, enable the capability. For more information, see EKS Auto Mode block storage capability in the Amazon EKS User Guide.

Request to configure EBS Block Storage settings for your EKS Auto Mode cluster.

Type: BlockStorage object

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Understand the Kubernetes version lifecycle on EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html

**Contents:**
- Understand the Kubernetes version lifecycle on EKS
- Available versions on standard support
- Available versions on extended support
- Amazon EKS Kubernetes release calendar
        - Note
- Get version information with AWS CLI
  - To retrieve information about available Kubernetes versions on EKS using the AWS CLI
- Amazon EKS version FAQs
        - Important
- Amazon EKS extended support FAQs

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Kubernetes rapidly evolves with new features, design updates, and bug fixes. The community releases new Kubernetes minor versions (such as 1.33) on average once every four months. Amazon EKS follows the upstream release and deprecation cycle for minor versions. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version.

A minor version is under standard support in Amazon EKS for the first 14 months after it’s released. Once a version is past the end of standard support date, it enters extended support for the next 12 months. Extended support allows you to stay at a specific Kubernetes version for longer at an additional cost per cluster hour. If you haven’t updated your cluster before the extended support period ends, your cluster is auto-upgraded to the oldest currently supported extended version.

Extended support is enabled by default. To disable, see Disable EKS extended support.

We recommend that you create your cluster with the latest available Kubernetes version supported by Amazon EKS. If your application requires a specific version of Kubernetes, you can select older versions. You can create new Amazon EKS clusters on any version offered in standard or extended support.

The following Kubernetes versions are currently available in Amazon EKS standard support:

For important changes to be aware of for each version in standard support, see Kubernetes versions standard support.

The following Kubernetes versions are currently available in Amazon EKS extended support:

For important changes to be aware of for each version in extended support, see Kubernetes versions extended support.

The following table shows important release and support dates to consider for each Kubernetes version. Billing for extended support starts at the beginning of the day that the version reaches end of standard support, in the UTC+0 timezone. The dates in the following table use the UTC+0 timezone.

Dates with only a month and a year are approximate and are updated with an exact date when it’s known.

To receive notifications of all source file changes to this specific documentation page, you can subscribe to the following URL with an RSS reader:

You can use the AWS CLI to get information about Kubernetes versions available on EKS, suc

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
https://github.com/awsdocs/amazon-eks-user-guide/commits/mainline/latest/ug/clusters/kubernetes-versions.adoc.atom
```

Example 2 (unknown):
```unknown
{
    "clusterVersions": [
        {
            "clusterVersion": "1.31",
            "clusterType": "eks",
            "defaultPlatformVersion": "eks.21",
            "defaultVersion": true,
            "releaseDate": "2024-09-25T17:00:00-07:00",
            "endOfStandardSupportDate": "2025-11-25T16:00:00-08:00",
            "endOfExtendedSupportDate": "2026-11-25T16:00:00-08:00",
            "status": "STANDARD_SUPPORT",
            "kubernetesPatchVersion": "1.31.3"
        }
    ]
}
```

Example 3 (unknown):
```unknown
clusterVersion
```

Example 4 (unknown):
```unknown
clusterType
```

---

## Install Kubecost

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cost-monitoring-kubecost.html#kubecost-overview

**Contents:**
- Install Kubecost
        - Note
- Install Amazon EKS optimized Kubecost bundle
- Access Kubecost dashboard

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS supports Kubecost, which you can use to monitor your costs broken down by Kubernetes resources including Pods, nodes, namespaces, and labels. This topic covers installing Kubecost, and accessing the Kubecost dashboard.

Amazon EKS provides an AWS optimized bundle of Kubecost for cluster cost visibility. You can use your existing AWS support agreements to obtain support. For more information about the available versions of Kubecost, see Learn more about Kubecost.

Kubecost v2 introduces several major new features. Learn more about Kubecost v2.

For more information about Kubecost, see the Kubecost documentation and Frequently asked questions.

You can use one of the following procedures to install the Amazon EKS optimized Kubecost bundle:

Before start, it is recommended to review Kubecost - Architecture Overview to understand how Kubecost works on Amazon EKS.

If you are new to Amazon EKS, we recommend that you use the Amazon EKS add-on for the installation because it simplifies the Amazon EKS optimized Kubecost bundle installation. For more information, see Deploying Kubecost on an Amazon EKS cluster using Amazon EKS add-on.

To customize the installation, you might configure your Amazon EKS optimized Kubecost bundle with Helm. For more information, see Deploying Kubecost on an Amazon EKS cluster using Helm in the Kubecost documentation.

Once the Amazon EKS optimized Kubecost bundle setup done, you should have access to Kubecost dashboard. For more information, see Access Kubecost Dashboard.

---

## Use high-performance app storage with Amazon FSx for Lustre

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/fsx-csi.html

**Contents:**
- Use high-performance app storage with Amazon FSx for Lustre

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Amazon FSx for Lustre Container Storage Interface (CSI) driver provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of Amazon FSx for Lustre file systems. For more information, see the Amazon FSx for Lustre User Guide.

For details on how to deploy the Amazon FSx for Lustre CSI driver to your Amazon EKS cluster and verify that it works, see Deploy the FSx for Lustre driver.

---

## ZonalShiftConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ZonalShiftConfigRequest.html

**Contents:**
- ZonalShiftConfigRequest
- Contents
- See Also

The configuration for zonal shift for the cluster.

If zonal shift is enabled, AWS configures zonal autoshift for the cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Use AWS Inferentia instances with Amazon EKS for Machine Learning

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/inferentia-support.html

**Contents:**
- Use AWS Inferentia instances with Amazon EKS for Machine Learning
        - Note
- Prerequisites
- Create a cluster
        - Note
        - Note
- (Optional) Deploy a TensorFlow Serving application image
- (Optional) Make predictions against your TensorFlow Serving service

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic describes how to create an Amazon EKS cluster with nodes running Amazon EC2 Inf1 instances and (optionally) deploy a sample application. Amazon EC2 Inf1 instances are powered by AWS Inferentia chips, which are custom built by AWS to provide high performance and lowest cost inference in the cloud. Machine learning models are deployed to containers using AWS Neuron, a specialized software development kit (SDK) consisting of a compiler, runtime, and profiling tools that optimize the machine learning inference performance of Inferentia chips. AWS Neuron supports popular machine learning frameworks such as TensorFlow, PyTorch, and MXNet.

Neuron device logical IDs must be contiguous. If a Pod requesting multiple Neuron devices is scheduled on an inf1.6xlarge or inf1.24xlarge instance type (which have more than one Neuron device), that Pod will fail to start if the Kubernetes scheduler selects non-contiguous device IDs. For more information, see Device logical IDs must be contiguous on GitHub.

Have eksctl installed on your computer. If you don’t have it installed, see Installation in the eksctl documentation.

Have kubectl installed on your computer. For more information, see Set up kubectl and eksctl.

(Optional) Have python3 installed on your computer. If you don’t have it installed, then see Python downloads for installation instructions.

Create a cluster with Inf1 Amazon EC2 instance nodes. You can replace inf1.2xlarge with any Inf1 instance type. The eksctl utility detects that you are launching a node group with an Inf1 instance type and will start your nodes using one of the Amazon EKS optimized accelerated Amazon Linux AMIs.

You can’t use IAM roles for service accounts with TensorFlow Serving.

Note the value of the following line of the output. It’s used in a later (optional) step.

When launching a node group with Inf1 instances, eksctl automatically installs the AWS Neuron Kubernetes device plugin. This plugin advertises Neuron devices as a system resource to the Kubernetes scheduler, which can be requested by a container. In addition to the default Amazon EKS node IAM policies, the Amazon S3 read only access policy is added so that the sample application, covered in a later step, can load a trained model from Amazon S3.

Make sure that all Pods have started correctly.

A trained model must 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
inf1.6xlarge
```

Example 2 (unknown):
```unknown
inf1.24xlarge
```

Example 3 (unknown):
```unknown
inf1.2xlarge
```

Example 4 (unknown):
```unknown
eksctl create cluster \
    --name inferentia \
    --region region-code \
    --nodegroup-name ng-inf1 \
    --node-type inf1.2xlarge \
    --nodes 2 \
    --nodes-min 1 \
    --nodes-max 4 \
    --ssh-access \
    --ssh-public-key your-key \
    --with-oidc
```

---

## Set up kubectl and eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#linux_amd64_kubectl

**Contents:**
- Set up kubectl and eksctl
- Install or update kubectl
        - Note
- Step 1: Check if kubectl is installed
- Step 2: Install or update kubectl
        - Note
  - macOS
  - Linux (amd64)
        - Note
  - Linux (arm64)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Once the AWS CLI is installed, there are two other tools you should install to create and manage your Kubernetes clusters:

kubectl: The kubectl command line tool is the main tool you will use to manage resources within your Kubernetes cluster. This page describes how to download and set up the kubectl binary that matches the version of your Kubernetes cluster. See Install or update kubectl.

eksctl: The eksctl command line tool is made for creating EKS clusters in the AWS cloud or on-premises (with EKS Anywhere), as well as modifying and deleting those clusters. See Install eksctl.

This topic helps you to download and install, or update, the kubectl binary on your device. The binary is identical to the upstream community versions. The binary is not unique to Amazon EKS or AWS. Use the steps below to get the specific version of kubectl that you need, although many builders simply run brew install kubectl to install it.

You must use a kubectl version that is within one minor version difference of your Amazon EKS cluster control plane. For example, a 1.32 kubectl client works with Kubernetes 1.31, 1.32, and 1.33 clusters.

Determine whether you already have kubectl installed on your device.

If you have kubectl installed in the path of your device, the example output includes information similar to the following. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in.

If you receive no output, then you either don’t have kubectl installed, or it’s not installed in a location that’s in your device’s path.

Install or update kubectl on one of the following operating systems:

If downloads are slow to your AWS Region from the AWS Regions used in this section, consider setting up CloudFront to front the content. For further information, see Get started with a basic CloudFront distribution.

Follow the steps below to install kubectl on macOS. The steps include:

Choosing and downloading the binary for the Kubernetes version you want.

Optionally checking the binary’s checksum.

Adding execute to the binary’s permissions.

Copying the binary to a folder in your PATH.

Optionally adding the binary’s directory to your PATH.

Download the binary for your cluster’s Kubern

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
brew install kubectl
```

Example 2 (unknown):
```unknown
kubectl version --client
```

Example 3 (unknown):
```unknown
Client Version: v1.31.X-eks-1234567
```

Example 4 (unknown):
```unknown
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/darwin/amd64/kubectl
```

---

## Send control plane logs to CloudWatch Logs

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html#control-plane-console

**Contents:**
- Send control plane logs to CloudWatch Logs
- Enable or disable control plane logs
  - AWS Management Console
  - AWS CLI
        - Note
- View cluster control plane logs
        - Note
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to CloudWatch Logs in your account. These logs make it easy for you to secure and run your clusters. You can select the exact log types you need, and logs are sent as log streams to a group for each Amazon EKS cluster in CloudWatch. You can use CloudWatch subscription filters to do real time analysis on the logs or to forward them to other services (the logs will be Base64 encoded and compressed with the gzip format). For more information, see Amazon CloudWatch logging.

You can start using Amazon EKS control plane logging by choosing which log types you want to enable for each new or existing Amazon EKS cluster. You can enable or disable each log type on a per-cluster basis using the AWS Management Console, AWS CLI (version 1.16.139 or higher), or through the Amazon EKS API. When enabled, logs are automatically sent from the Amazon EKS cluster to CloudWatch Logs in the same account.

When you use Amazon EKS control plane logging, you’re charged standard Amazon EKS pricing for each cluster that you run. You are charged the standard CloudWatch Logs data ingestion and storage costs for any logs sent to CloudWatch Logs from your clusters. You are also charged for any AWS resources, such as Amazon EC2 instances or Amazon EBS volumes, that you provision as part of your cluster.

The following cluster control plane log types are available. Each log type corresponds to a component of the Kubernetes control plane. To learn more about these components, see Kubernetes Components in the Kubernetes documentation.

Your cluster’s API server is the control plane component that exposes the Kubernetes API. If you enable API server logs when you launch the cluster, or shortly thereafter, the logs include API server flags that were used to start the API server. For more information, see kube-apiserver and the audit policy in the Kubernetes documentation.

Kubernetes audit logs provide a record of the individual users, administrators, or system components that have affected your cluster. For more information, see Auditing in the Kubernetes documentation.

Authenticator logs are unique to Amazon EKS. These logs represent the control plane component that Amazon EKS uses for Kubernetes Role Based Access Control (RBAC) auth

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
authenticator
```

Example 2 (unknown):
```unknown
controllerManager
```

Example 3 (unknown):
```unknown
aws --version
```

Example 4 (unknown):
```unknown
aws eks update-cluster-config \
    --region region-code \
    --name my-cluster \
    --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

---

## ConnectorConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ConnectorConfigResponse.html#AmazonEKS-Type-ConnectorConfigResponse-activationId

**Contents:**
- ConnectorConfigResponse
- Contents
- See Also

The full description of your connected cluster.

A unique code associated with the cluster for registration purposes.

The expiration time of the connected cluster. The cluster's YAML file must be applied through the native provider.

A unique ID associated with the cluster for registration purposes.

The cluster's cloud service provider.

The Amazon Resource Name (ARN) of the role to communicate with services from the connected Kubernetes cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## Use data storage with Amazon FSx for OpenZFS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/fsx-openzfs-csi.html

**Contents:**
- Use data storage with Amazon FSx for OpenZFS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon FSx for OpenZFS is a fully managed file storage service that makes it easy to move data to AWS from on-premises ZFS or other Linux-based file servers. You can do this without changing your application code or how you manage data. It offers highly reliable, scalable, efficient, and feature-rich file storage built on the open-source OpenZFS file system. It combines these capabilities with the agility, scalability, and simplicity of a fully managed AWS service. For more information, see the Amazon FSx for OpenZFS User Guide.

The FSx for OpenZFS Container Storage Interface (CSI) driver provides a CSI interface that allows Amazon EKS clusters to manage the life cycle of FSx for OpenZFS volumes. Note that the Amazon FSx for OpenZFS CSI driver is not compatible with Amazon EKS Hybrid Nodes. To deploy the FSx for OpenZFS CSI driver to your Amazon EKS cluster, see aws-fsx-openzfs-csi-driver on GitHub.

---

## UpgradePolicyRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_UpgradePolicyRequest.html#AmazonEKS-Type-UpgradePolicyRequest-supportType

**Contents:**
- UpgradePolicyRequest
- Contents
- See Also

The support policy to use for the cluster. Extended support allows you to remain on specific Kubernetes versions for longer. Clusters in extended support have higher costs. The default value is EXTENDED. Use STANDARD to disable extended support.

Learn more about EKS Extended Support in the Amazon EKS User Guide.

If the cluster is set to EXTENDED, it will enter extended support at the end of standard support. If the cluster is set to STANDARD, it will be automatically upgraded at the end of standard support.

Learn more about EKS Extended Support in the Amazon EKS User Guide.

Valid Values: STANDARD | EXTENDED

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
STANDARD | EXTENDED
```

---

## LogSetup

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_LogSetup.html#AmazonEKS-Type-LogSetup-types

**Contents:**
- LogSetup
- Contents
- See Also

An object representing the enabled or disabled Kubernetes control plane logs for your cluster.

If a log type is enabled, that log type exports its control plane logs to CloudWatch Logs . If a log type isn't enabled, that log type doesn't export its control plane logs. Each individual log type can be enabled or disabled independently.

The available cluster control plane log types.

Type: Array of strings

Valid Values: api | audit | authenticator | controllerManager | scheduler

For more information about using this API in one of the language-specific AWS SDKs, see the following:

**Examples:**

Example 1 (unknown):
```unknown
api | audit | authenticator | controllerManager | scheduler
```

---

## Use pod identity with the AWS SDK

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-minimum-sdk.html

**Contents:**
- Use pod identity with the AWS SDK
- Using EKS Pod Identity credentials

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

To use the credentials from a EKS Pod Identity association, your code can use any AWS SDK to create a client for an AWS service with an SDK, and by default the SDK searches in a chain of locations for AWS Identity and Access Management credentials to use. The EKS Pod Identity credentials will be used if you don’t specify a credential provider when you create the client or otherwise initialized the SDK.

This works because EKS Pod Identities have been added to the Container credential provider which is searched in a step in the default credential chain. If your workloads currently use credentials that are earlier in the chain of credentials, those credentials will continue to be used even if you configure an EKS Pod Identity association for the same workload.

For more information about how EKS Pod Identities work, see Understand how EKS Pod Identity works.

When using Learn how EKS Pod Identity grants pods access to AWS services, the containers in your Pods must use an AWS SDK version that supports assuming an IAM role from the EKS Pod Identity Agent. Make sure that you’re using the following versions, or later, for your AWS SDK:

Java (Version 2) – 2.21.30

Go v2 – release-2023-11-14

Python (Boto3) – 1.34.41

Python (botocore) – 1.34.41

JavaScript v2 – 2.1550.0

JavaScript v3 – v3.458.0

Rust – release-2024-03-13

To ensure that you’re using a supported SDK, follow the installation instructions for your preferred SDK at Tools to Build on AWS when you build your containers.

For a list of add-ons that support EKS Pod Identity, see Pod Identity Support Reference.

---

## Minimize latency with Amazon File Cache

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/file-cache-csi.html

**Contents:**
- Minimize latency with Amazon File Cache

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon File Cache is a fully managed, high-speed cache on AWS that’s used to process file data, regardless of where the data is stored. Amazon File Cache automatically loads data into the cache when it’s accessed for the first time and releases data when it’s not used. For more information, see the Amazon File Cache User Guide.

The Amazon File Cache Container Storage Interface (CSI) driver provides a CSI interface that allows Amazon EKS clusters to manage the life cycle of Amazon file caches. Note that the Amazon File Cache CSI driver is not compatible with Amazon EKS Hybrid Nodes. To deploy the Amazon File Cache CSI driver to your Amazon EKS cluster, see aws-file-cache-csi-driver on GitHub.

---

## Set up the Amazon EKS Pod Identity Agent

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html

**Contents:**
- Set up the Amazon EKS Pod Identity Agent
        - Tip
- Considerations
- Creating the Amazon EKS Pod Identity Agent
  - Agent prerequisites
  - Setup agent with AWS console
  - Setup agent with AWS CLI
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances.

Amazon EKS Pod Identity provides credentials to your workloads with an additional EKS Auth API and an agent pod that runs on each node.

You do not need to install the EKS Pod Identity Agent on EKS Auto Mode Clusters. This capability is built into EKS Auto Mode.

By default, the EKS Pod Identity Agent is pre-installed on EKS Auto Mode clusters. To learn more, see Automate cluster infrastructure with EKS Auto Mode.

By default, the EKS Pod Identity Agent listens on an IPv4 and IPv6 address for pods to request credentials. The agent uses the loopback (localhost) IP address 169.254.170.23 for IPv4 and the localhost IP address [fd00:ec2::23] for IPv6.

If you disable IPv6 addresses, or otherwise prevent localhost IPv6 IP addresses, the agent can’t start. To start the agent on nodes that can’t use IPv6, follow the steps in Disable IPv6 in the EKS Pod Identity Agent to disable the IPv6 configuration.

An existing Amazon EKS cluster. To deploy one, see Get started with Amazon EKS. The cluster version and platform version must be the same or later than the versions listed in EKS Pod Identity cluster versions.

The node role has permissions for the agent to do the AssumeRoleForPodIdentity action in the EKS Auth API. You can use the AWS managed policy: AmazonEKSWorkerNodePolicy or add a custom policy similar to the following:

This action can be limited by tags to restrict which roles can be assumed by pods that use the agent.

The nodes can reach and download images from Amazon ECR. The container image for the add-on is in the registries listed in View Amazon container image registries for Amazon EKS add-ons.

Note that you can change the image location and provide imagePullSecrets for EKS add-ons in the Optional configuration settings in the AWS Management Console, and in the --configuration-values in the AWS CLI.

The nodes can reach the Amazon EKS Auth API. For private clusters, the eks-auth endpoint in AWS PrivateLink is required.

Open the Amazon EKS console.

In the left navigation pane, select Clusters, and then select the name of the cluster that you want to configure the EKS Pod Identity Agent add-on for.

Choose

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
169.254.170.23
```

Example 2 (unknown):
```unknown
[fd00:ec2::23]
```

Example 3 (unknown):
```unknown
AssumeRoleForPodIdentity
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks-auth:AssumeRoleForPodIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

---

## Enable snapshot functionality for CSI volumes

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/csi-snapshot-controller.html

**Contents:**
- Enable snapshot functionality for CSI volumes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Snapshot functionality allows for point-in-time copies of your data. For this capability to work in Kubernetes, you need both a CSI driver with snapshot support (such as the Amazon EBS CSI driver) and a CSI snapshot controller. The snapshot controller is available either as an Amazon EKS managed add-on or as a self-managed installation.

Here are some things to consider when using the CSI snapshot controller.

The snapshot controller must be installed alongside a CSI driver with snapshot functionality. For installation instructions of the Amazon EBS CSI driver, see Use Kubernetes volume storage with Amazon EBS.

Kubernetes doesn’t support snapshots of volumes being served via CSI migration, such as Amazon EBS volumes using a StorageClass with provisioner kubernetes.io/aws-ebs. Volumes must be created with a StorageClass that references the CSI driver provisioner, ebs.csi.aws.com.

Amazon EKS Auto Mode does not include the snapshot controller. The storage capability of EKS Auto Mode is compatible with the snapshot controller.

We recommend that you install the CSI snapshot controller through the Amazon EKS managed add-on. This add-on includes the custom resource definitions (CRDs) that are needed to create and manage snapshots on Amazon EKS. To add an Amazon EKS add-on to your cluster, see Create an Amazon EKS add-on. For more information about add-ons, see Amazon EKS add-ons.

Alternatively, if you want a self-managed installation of the CSI snapshot controller, see Usage in the upstream Kubernetes external-snapshotter on GitHub.

**Examples:**

Example 1 (unknown):
```unknown
StorageClass
```

Example 2 (unknown):
```unknown
kubernetes.io/aws-ebs
```

Example 3 (unknown):
```unknown
StorageClass
```

Example 4 (unknown):
```unknown
ebs.csi.aws.com
```

---

## Create a storage class

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/create-storage-class.html

**Contents:**
- Create a storage class
- Use self-managed KMS key to encrypt EBS volumes
  - Sample self-managed KMS IAM Policy
  - Sample self-managed KMS StorageClass
- StorageClass Parameters Reference
- Considerations
        - Note
- Install CSI Snapshot Controller add-on
  - To install snapshot controller in system node pool

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

A StorageClass in Amazon EKS Auto Mode defines how Amazon EBS volumes are automatically provisioned when applications request persistent storage. This page explains how to create and configure a StorageClass that works with the Amazon EKS Auto Mode to provision EBS volumes.

By configuring a StorageClass, you can specify default settings for your EBS volumes including volume type, encryption, IOPS, and other storage parameters. You can also configure the StorageClass to use AWS KMS keys for encryption management.

EKS Auto Mode does not create a StorageClass for you. You must create a StorageClass referencing ebs.csi.eks.amazonaws.com to use the storage capability of EKS Auto Mode.

First, create a file named storage-class.yaml:

Second, apply the storage class to your cluster.

provisioner: ebs.csi.eks.amazonaws.com - Uses EKS Auto Mode

allowedTopologies - Specifying matchLabelExpressions to match on eks.amazonaws.com/compute-type:auto will ensure that if your pods need a volume to be automatically provisioned using Auto Mode then the pods will not be scheduled on non-Auto nodes.

volumeBindingMode: WaitForFirstConsumer - Delays volume creation until a pod needs it

type: gp3 - Specifies the EBS volume type

encrypted: "true" - EBS will encrypt any volumes created using the StorageClass. EBS will use the default aws/ebs key alias. For more information, see How Amazon EBS encryption works in the Amazon EBS User Guide. This value is optional but suggested.

storageclass.kubernetes.io/is-default-class: "true" - Kubernetes will use this storage class by default, unless you specify a different volume class on a persistent volume claim. This value is optional. Use caution when setting this value if you are migrating from a different storage controller.

To use a self-managed KMS key to encrypt EBS volumes automated by EKS Auto Mode, you need to:

Create a self-managed KMS key.

For more information, see Create a symmetric encryption KMS key or How Amazon Elastic Block Store (Amazon EBS) uses KMS in the KMS User Guide.

Create a new policy that permits access to the KMS key.

Use the sample IAM policy below to create the policy. Insert the ARN of the new self-managed KMS key. For more information, see Creating roles and attaching policies (console) in the AWS IAM User Guide.

Attach the policy to the EKS Cluster Ro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
StorageClass
```

Example 2 (unknown):
```unknown
StorageClass
```

Example 3 (unknown):
```unknown
StorageClass
```

Example 4 (unknown):
```unknown
StorageClass
```

---

## Understand how EKS Pod Identity works

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-how-it-works.html

**Contents:**
- Understand how EKS Pod Identity works
- Using EKS Pod Identities in your code
- How EKS Pod Identity Agent works with a Pod
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances.

Amazon EKS Pod Identity provides credentials to your workloads with an additional EKS Auth API and an agent pod that runs on each node.

In your add-ons, such as Amazon EKS add-ons and self-managed controller, operators, and other add-ons, the author needs to update their software to use the latest AWS SDKs. For the list of compatibility between EKS Pod Identity and the add-ons produced by Amazon EKS, see the previous section EKS Pod Identity restrictions.

In your code, you can use the AWS SDKs to access AWS services. You write code to create a client for an AWS service with an SDK, and by default the SDK searches in a chain of locations for AWS Identity and Access Management credentials to use. After valid credentials are found, the search is stopped. For more information about the default locations used, see the Credential provider chain in the AWS SDKs and Tools Reference Guide.

EKS Pod Identities have been added to the Container credential provider which is searched in a step in the default credential chain. If your workloads currently use credentials that are earlier in the chain of credentials, those credentials will continue to be used even if you configure an EKS Pod Identity association for the same workload. This way you can safely migrate from other types of credentials by creating the association first, before removing the old credentials.

The container credentials provider provides temporary credentials from an agent that runs on each node. In Amazon EKS, the agent is the Amazon EKS Pod Identity Agent and on Amazon Elastic Container Service the agent is the amazon-ecs-agent. The SDKs use environment variables to locate the agent to connect to.

In contrast, IAM roles for service accounts provides a web identity token that the AWS SDK must exchange with AWS Security Token Service by using AssumeRoleWithWebIdentity.

When Amazon EKS starts a new pod that uses a service account with an EKS Pod Identity association, the cluster adds the following content to the Pod manifest:

Kubernetes selects which node to run the pod on. Then, the Amazon EKS Pod Identity Agent on the node uses the AssumeRoleForPodI

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
amazon-ecs-agent
```

Example 2 (unknown):
```unknown
AssumeRoleWithWebIdentity
```

Example 3 (unknown):
```unknown
    env:
    - name: AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE
      value: "/var/run/secrets/pods.eks.amazonaws.com/serviceaccount/eks-pod-identity-token"
    - name: AWS_CONTAINER_CREDENTIALS_FULL_URI
      value: "http://169.254.170.23/v1/credentials"
    volumeMounts:
    - mountPath: "/var/run/secrets/pods.eks.amazonaws.com/serviceaccount/"
      name: eks-pod-identity-token
  volumes:
  - name: eks-pod-identity-token
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          audience: pods.eks.amazonaws.com
          expirationSeconds: 86400 # 24 hours
     
...
```

---

## OutpostConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_OutpostConfigRequest.html#AmazonEKS-Type-OutpostConfigRequest-controlPlaneInstanceType

**Contents:**
- OutpostConfigRequest
- Contents
- See Also

The configuration of your local Amazon EKS cluster on an AWS Outpost. Before creating a cluster on an Outpost, review Creating a local cluster on an Outpost in the Amazon EKS User Guide. This API isn't available for Amazon EKS clusters on the AWS cloud.

The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts. Choose an instance type based on the number of nodes that your cluster will have. For more information, see Capacity considerations in the Amazon EKS User Guide.

The instance type that you specify is used for all Kubernetes control plane instances. The instance type can't be changed after cluster creation. The control plane is not automatically scaled by Amazon EKS.

The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts. Only a single Outpost ARN is supported.

Type: Array of strings

An object representing the placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost. For more information, see Capacity considerations in the Amazon EKS User Guide.

Type: ControlPlanePlacementRequest object

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## UntagResource

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_UntagResource.html

**Contents:**
- UntagResource
- Request Syntax
- URI Request Parameters
- Request Body
- Response Syntax
- Response Elements
- Errors
- See Also

Deletes specified tags from an Amazon EKS resource.

The request uses the following URI parameters.

The Amazon Resource Name (ARN) of the resource to delete tags from.

The keys of the tags to remove.

Array Members: Minimum number of 1 item. Maximum number of 50 items.

Length Constraints: Minimum length of 1. Maximum length of 128.

The request does not have a request body.

If the action is successful, the service sends back an HTTP 200 response with an empty HTTP body.

For information about the errors that are common to all actions, see Common Errors.

This exception is thrown if the request contains a semantic error. The precise meaning will depend on the API, and will be documented in the error message.

This exception is thrown if the request contains a semantic error. The precise meaning will depend on the API, and will be documented in the error message.

HTTP Status Code: 400

A service resource associated with the request could not be found. Clients should not retry such requests.

A service resource associated with the request could not be found. Clients should not retry such requests.

HTTP Status Code: 404

For more information about using this API in one of the language-specific AWS SDKs, see the following:

AWS Command Line Interface V2

AWS SDK for JavaScript V3

**Examples:**

Example 1 (unknown):
```unknown
DELETE /tags/resourceArn?tagKeys=tagKeys HTTP/1.1
```

Example 2 (unknown):
```unknown
resourceArn
```

Example 3 (unknown):
```unknown
HTTP/1.1 200
```

---

## ComputeConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ComputeConfigRequest.html

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

## ConnectorConfigResponse

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_ConnectorConfigResponse.html#AmazonEKS-Type-ConnectorConfigResponse-roleArn

**Contents:**
- ConnectorConfigResponse
- Contents
- See Also

The full description of your connected cluster.

A unique code associated with the cluster for registration purposes.

The expiration time of the connected cluster. The cluster's YAML file must be applied through the native provider.

A unique ID associated with the cluster for registration purposes.

The cluster's cloud service provider.

The Amazon Resource Name (ARN) of the role to communicate with services from the connected Kubernetes cluster.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

---

## KubernetesNetworkConfigRequest

**URL:** https://docs.aws.amazon.com/eks/latest/APIReference/API_KubernetesNetworkConfigRequest.html#AmazonEKS-Type-KubernetesNetworkConfigRequest-elasticLoadBalancing

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

## Update an Amazon EKS add-on

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/updating-an-add-on.html

**Contents:**
- Update an Amazon EKS add-on
- Prerequisites
- Procedure
- Update add-on (eksctl)
- Update add-on (AWS Console)
        - Note
- Update add-on (AWS CLI)

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon EKS doesn’t automatically update an add-on when new versions are released or after you update your cluster to a new Kubernetes minor version. To update an add-on for an existing cluster, you must initiate the update. After you initiate the update, Amazon EKS updates the add-on for you. Before updating an add-on, review the current documentation for the add-on. For a list of available add-ons, see AWS add-ons. If the add-on requires an IAM role, see the details for the specific add-on in Available Amazon EKS add-ons from AWS for details about creating the role.

Complete the following before you create an add-on:

Check if your add-on requires an IAM role. For more information, see Amazon EKS add-ons.

Verify that the Amazon EKS add-on version is compatible with your cluster. For more information, see Verify Amazon EKS add-on version compatibility with a cluster.

You can update an Amazon EKS add-on using eksctl, the AWS Management Console, or the AWS CLI.

Determine the current add-ons and add-on versions installed on your cluster. Replace my-cluster with the name of your cluster.

An example output is as follows.

Your output might look different, depending on which add-ons and versions that you have on your cluster. You can see that in the previous example output, two existing add-ons on the cluster have newer versions available in the UPDATE AVAILABLE column.

Copy the command that follows to your device. Make the following modifications to the command as needed:

Replace my-cluster with the name of your cluster.

Replace region-code with the AWS Region that your cluster is in.

Replace vpc-cni with the name of an add-on returned in the output of the previous step that you want to update.

If you want to update to a version earlier than the latest available version, then replace latest with the version number returned in the output of the previous step that you want to use. Some add-ons have recommended versions. For more information, see the documentation for the add-on that you’re updating. For a list of add-ons, see AWS add-ons.* If the add-on uses a Kubernetes service account and IAM role, replace 111122223333 with your account ID and role-name with the name of an existing IAM role that you’ve created. For instructions on creating the role, see the documentation for the add-on that you’re creatin

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
kube-proxy  v1.23.7-eksbuild.1   ACTIVE  0                v1.23.8-eksbuild.2
vpc-cni     v1.10.4-eksbuild.1   ACTIVE  0                v1.12.0-eksbuild.1,v1.11.4-eksbuild.1,v1.11.3-eksbuild.1,v1.11.2-eksbuild.1,v1.11.0-eksbuild.1
```

Example 3 (unknown):
```unknown
UPDATE AVAILABLE
```

Example 4 (unknown):
```unknown
region-code
```

---

## Use Kubernetes volume storage with Amazon EBS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html

**Contents:**
- Use Kubernetes volume storage with Amazon EBS
        - Note
- Considerations
        - Important
- Prerequisites
- Step 1: Create an IAM role
        - Note
        - Note
        - Note
  - eksctl

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

New: Amazon EKS Auto Mode automates routine tasks for block storage. Learn how to Deploy a sample stateful workload to EKS Auto Mode.

The Amazon Elastic Block Store (Amazon EBS) Container Storage Interface (CSI) driver manages the lifecycle of Amazon EBS volumes as storage for the Kubernetes Volumes that you create. The Amazon EBS CSI driver makes Amazon EBS volumes for these types of Kubernetes volumes: generic ephemeral volumes and persistent volumes.

You do not need to install the Amazon EBS CSI controller on EKS Auto Mode clusters.

You can’t mount Amazon EBS volumes to Fargate Pods.

You can run the Amazon EBS CSI controller on Fargate nodes, but the Amazon EBS CSI node DaemonSet can only run on Amazon EC2 instances.

Amazon EBS volumes and the Amazon EBS CSI driver are not compatible with Amazon EKS Hybrid Nodes.

Support will be provided for the latest add-on version and one prior version. Bugs or vulnerabilities found in the latest version will be backported to the previous release in a new minor version.

EKS Auto Mode requires storage classes to use ebs.csi.eks.amazonaws.com as the provisioner. The standard Amazon EBS CSI Driver (ebs.csi.aws.com) manages its own volumes separately. To use existing volumes with EKS Auto Mode, migrate them using volume snapshots to a storage class that uses the Auto Mode provisioner.

To use the snapshot functionality of the Amazon EBS CSI driver, you must first install the CSI snapshot controller. For more information, see Enable snapshot functionality for CSI volumes.

An existing cluster. To see the required platform version, run the following command.

The EBS CSI driver needs AWS IAM Permissions.

AWS suggests using EKS Pod Identities. For more information, see Overview of setting up EKS Pod Identities.

For information about IAM Roles for Service Accounts, see Create an IAM OIDC provider for your cluster.

The Amazon EBS CSI plugin requires IAM permissions to make calls to AWS APIs on your behalf. If you don’t do these steps, attempting to install the add-on and running kubectl describe pvc will show failed to provision volume with StorageClass along with a could not create volume in EC2: UnauthorizedOperation error. For more information, see Set up driver permission on GitHub.

Pods will have access to the permissions that are assigned to the IAM role unless y

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ebs.csi.eks.amazonaws.com
```

Example 2 (unknown):
```unknown
ebs.csi.aws.com
```

Example 3 (unknown):
```unknown
aws eks describe-addon-versions --addon-name aws-ebs-csi-driver
```

Example 4 (unknown):
```unknown
kubectl describe pvc
```

---

## Grant Pods access to AWS resources based on tags

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/pod-id-abac.html

**Contents:**
- Grant Pods access to AWS resources based on tags
- Sample policy with tags
- Enable or disable session tags
  - Enable session tags
  - Disable session tags
- Cross-account tags
- Custom tags
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Attribute-based access control (ABAC) grants rights to users through policies which combine attributes together. EKS Pod Identity attaches tags to the temporary credentials to each Pod with attributes such as cluster name, namespace, and service account name. These role session tags enable administrators to author a single role that can work across service accounts by allowing access to AWS resources based on matching tags. By adding support for role session tags, you can enforce tighter security boundaries between clusters, and workloads within clusters, while reusing the same IAM roles and IAM policies.

Below is an IAM policy example that grants s3:GetObject permissions when the corresponding object is tagged with the EKS cluster name.

EKS Pod Identity adds a pre-defined set of session tags when it assumes the role. These session tags enable administrators to author a single role that can work across resources by allowing access to AWS resources based on matching tags.

Session tags are automatically enabled with EKS Pod Identity—​no action is required on your part. By default, EKS Pod Identity attaches a set of predefined tags to your session. To reference these tags in policies, use the syntax ${aws:PrincipalTag/ followed by the tag key. For example, ${aws:PrincipalTag/kubernetes-namespace}.

kubernetes-service-account

AWS compresses inline session policies, managed policy ARNs, and session tags into a packed binary format that has a separate limit. If you receive a PackedPolicyTooLarge error indicating the packed binary format has exceeded the size limit, you can attempt to reduce the size by disabling the session tags added by EKS Pod Identity. To disable these session tags, follow these steps:

Open the Amazon EKS console.

In the left navigation pane, select Clusters, and then select the name of the cluster that you want to modify.

Choose the Access tab.

In the Pod Identity associations, choose the association ID you would like to modify in Association ID, then choose Edit.

Under Session tags, choose Disable session tags.

All of the session tags that are added by EKS Pod Identity are transitive; the tag keys and values are passed to any AssumeRole actions that your workloads use to switch roles into another account. You can use these tags in policies in other accounts to limit access in cross-ac

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
s3:GetObject
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectTagging"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "s3:ExistingObjectTag/eks-cluster-name": "${aws:PrincipalTag/eks-cluster-name}"
                }
            }
        }
    ]
}
```

Example 3 (unknown):
```unknown
${aws:PrincipalTag/
```

Example 4 (unknown):
```unknown
${aws:PrincipalTag/kubernetes-namespace}
```

---
