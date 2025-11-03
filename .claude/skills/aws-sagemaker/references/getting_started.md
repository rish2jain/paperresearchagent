# Aws-Sagemaker - Getting Started

**Pages:** 22

---

## Set up Partner AI Apps

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/partner-app-onboard.html

**Contents:**
- Set up Partner AI Apps
- Prerequisites
- Administrative permissions
  - AWS Marketplace subscription for Partner AI Apps
  - Set up Partner AI App execution role
  - Configure Amazon Bedrock integration
        - Important
    - Deepchecks Amazon Bedrock integration
- User permissions
  - Manage user authorization and authentication

The following topics describe the permissions needed to start using Amazon SageMaker Partner AI Apps. The permissions required are split into two parts, depending on the user permissions level:

Administrative permissions – Permissions for administrators setting up data scientist and machine learning (ML) developer environments.

Partner AI Apps management

User permissions – Permissions for data scientists and machine learning developers.

Admins can complete the following prerequisites to set up Partner AI Apps.

(Optional) Onboard to a SageMaker AI domain. Partner AI Apps can be accessed directly from a SageMaker AI domain. For more information, see Amazon SageMaker AI domain overview.

If using Partner AI Apps in a SageMaker AI domain in VPC-only mode, admins must create an endpoint with the following format to connect to the Partner AI Apps. For more information about using Studio in VPC-only mode, see Connect Amazon SageMaker Studio in a VPC to External Resources.

(Optional) If admins are interacting with the domain using the AWS CLI, they must also complete the following prerequisites.

Update the AWS CLI by following the steps in Installing the current AWS CLI Version.

From the local machine, run aws configure and provide AWS credentials. For information about AWS credentials, see Understanding and getting your AWS credentials.

The administrator must add the following permissions to enable Partner AI Apps in SageMaker AI.

Permission to complete AWS Marketplace subscription for Partner AI Apps

Set up Partner AI App execution role

Admins must complete the following steps to add permissions for AWS Marketplace. For information about using AWS Marketplace, see Getting started as a buyer using AWS Marketplace.

Grant permissions for AWS Marketplace. Partner AI Apps administrators require these permissions to purchase subscriptions to Partner AI Apps from AWS Marketplace. To get access to AWS Marketplace, admins must attach the AWSMarketplaceManageSubscriptions managed policy to the IAM role that they're using to access the SageMaker AI console and purchase the app. For details about the AWSMarketplaceManageSubscriptions managed policy, see AWS managed policies for AWS Marketplace buyers. For information about attaching managed policies, see Adding and removing IAM identity permissions.

Grant permissions for SageMaker AI to run operations on the admins behalf using other AWS services. Admins must grant SageMaker AI permissions to use these service

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws.sagemaker.region.partner-app
```

Example 2 (unknown):
```unknown
aws configure
```

Example 3 (unknown):
```unknown
AWSMarketplaceManageSubscriptions
```

Example 4 (unknown):
```unknown
AWSMarketplaceManageSubscriptions
```

---

## Get Started with Data Wrangler

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-getting-started.html

**Contents:**
- Get Started with Data Wrangler
- Prerequisites
- Access Data Wrangler
        - Important
- Update Data Wrangler
- Demo: Data Wrangler Titanic Dataset Walkthrough
  - Upload Dataset to S3 and Import
        - Important
        - Import the Titanic dataset to Data Wrangler
  - Data Flow

Amazon SageMaker Data Wrangler is a feature in Amazon SageMaker Studio Classic. Use this section to learn how to access and get started using Data Wrangler. Do the following:

Complete each step in Prerequisites.

Follow the procedure in Access Data Wrangler to start using Data Wrangler.

To use Data Wrangler, you must complete the following prerequisites.

To use Data Wrangler, you need access to an Amazon Elastic Compute Cloud (Amazon EC2) instance. For more information about the Amazon EC2 instances that you can use, see Instances. To learn how to view your quotas and, if necessary, request a quota increase, see AWS service quotas.

Configure the required permissions described in Security and Permissions.

If your organization is using a firewall that blocks internet traffic, you must have access to the following URLs:

https://ui.prod-1.data-wrangler.sagemaker.aws/

https://ui.prod-2.data-wrangler.sagemaker.aws/

https://ui.prod-3.data-wrangler.sagemaker.aws/

https://ui.prod-4.data-wrangler.sagemaker.aws/

To use Data Wrangler, you need an active Studio Classic instance. To learn how to launch a new instance, see Amazon SageMaker AI domain overview. When your Studio Classic instance is Ready, use the instructions in Access Data Wrangler.

The following procedure assumes you have completed the Prerequisites.

To access Data Wrangler in Studio Classic, do the following.

Sign in to Studio Classic. For more information, see Amazon SageMaker AI domain overview.

From the dropdown list, select Studio.

Choose the Home icon.

Choose Data Wrangler.

You can also create a Data Wrangler flow by doing the following.

In the top navigation bar, select File.

Select Data Wrangler Flow.

(Optional) Rename the new directory and the .flow file.

When you create a new .flow file in Studio Classic, you might see a carousel that introduces you to Data Wrangler.

This may take a few minutes.

This messaging persists as long as the KernelGateway app on your User Details page is Pending. To see the status of this app, in the SageMaker AI console on the Amazon SageMaker Studio Classic page, select the name of the user you are using to access Studio Classic. On the User Details page, you see a KernelGateway app under Apps. Wait until this app status is Ready to start using Data Wrangler. This can take around 5 minutes the first time you launch Data Wrangler.

To get started, choose a data source and use it to import a dataset. See Import to learn more.

When you import a da

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
https://ui.prod-1.data-wrangler.sagemaker.aws/
```

Example 2 (unknown):
```unknown
https://ui.prod-2.data-wrangler.sagemaker.aws/
```

Example 3 (unknown):
```unknown
https://ui.prod-3.data-wrangler.sagemaker.aws/
```

Example 4 (unknown):
```unknown
https://ui.prod-4.data-wrangler.sagemaker.aws/
```

---

## Get Started with Data Wrangler

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-getting-started.html#data-wrangler-getting-started-prerequisite

**Contents:**
- Get Started with Data Wrangler
- Prerequisites
- Access Data Wrangler
        - Important
- Update Data Wrangler
- Demo: Data Wrangler Titanic Dataset Walkthrough
  - Upload Dataset to S3 and Import
        - Important
        - Import the Titanic dataset to Data Wrangler
  - Data Flow

Amazon SageMaker Data Wrangler is a feature in Amazon SageMaker Studio Classic. Use this section to learn how to access and get started using Data Wrangler. Do the following:

Complete each step in Prerequisites.

Follow the procedure in Access Data Wrangler to start using Data Wrangler.

To use Data Wrangler, you must complete the following prerequisites.

To use Data Wrangler, you need access to an Amazon Elastic Compute Cloud (Amazon EC2) instance. For more information about the Amazon EC2 instances that you can use, see Instances. To learn how to view your quotas and, if necessary, request a quota increase, see AWS service quotas.

Configure the required permissions described in Security and Permissions.

If your organization is using a firewall that blocks internet traffic, you must have access to the following URLs:

https://ui.prod-1.data-wrangler.sagemaker.aws/

https://ui.prod-2.data-wrangler.sagemaker.aws/

https://ui.prod-3.data-wrangler.sagemaker.aws/

https://ui.prod-4.data-wrangler.sagemaker.aws/

To use Data Wrangler, you need an active Studio Classic instance. To learn how to launch a new instance, see Amazon SageMaker AI domain overview. When your Studio Classic instance is Ready, use the instructions in Access Data Wrangler.

The following procedure assumes you have completed the Prerequisites.

To access Data Wrangler in Studio Classic, do the following.

Sign in to Studio Classic. For more information, see Amazon SageMaker AI domain overview.

From the dropdown list, select Studio.

Choose the Home icon.

Choose Data Wrangler.

You can also create a Data Wrangler flow by doing the following.

In the top navigation bar, select File.

Select Data Wrangler Flow.

(Optional) Rename the new directory and the .flow file.

When you create a new .flow file in Studio Classic, you might see a carousel that introduces you to Data Wrangler.

This may take a few minutes.

This messaging persists as long as the KernelGateway app on your User Details page is Pending. To see the status of this app, in the SageMaker AI console on the Amazon SageMaker Studio Classic page, select the name of the user you are using to access Studio Classic. On the User Details page, you see a KernelGateway app under Apps. Wait until this app status is Ready to start using Data Wrangler. This can take around 5 minutes the first time you launch Data Wrangler.

To get started, choose a data source and use it to import a dataset. See Import to learn more.

When you import a da

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
https://ui.prod-1.data-wrangler.sagemaker.aws/
```

Example 2 (unknown):
```unknown
https://ui.prod-2.data-wrangler.sagemaker.aws/
```

Example 3 (unknown):
```unknown
https://ui.prod-3.data-wrangler.sagemaker.aws/
```

Example 4 (unknown):
```unknown
https://ui.prod-4.data-wrangler.sagemaker.aws/
```

---

## Amazon SageMaker AI Features

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis-features.html

**Contents:**
- Amazon SageMaker AI Features
        - Topics
- New features for re:Invent 2024
- Machine learning environments
- Major features

Amazon SageMaker AI includes the following features.

New features for re:Invent 2024

Machine learning environments

SageMaker AI includes the following new features for re:Invent 2024.

You can run recipes within Amazon SageMaker HyperPod or as SageMaker training jobs. You use the HyperPod training adapter as the framework to help you run end-to-end training workflows. The training adapter is built on the NVIDIA NeMo framework and Neuronx Distributed Training package.

In Amazon SageMaker Studio, you can launch machine learning workloads on HyperPod clusters and view HyperPod cluster information. The increased visibility into cluster details and hardware metrics can help your team identify the right candidate for your pre-training or fine-tuning workloads.

Amazon SageMaker HyperPod task governance is a robust management system designed to streamline resource allocation and ensure efficient utilization of compute resources across teams and projects for your Amazon EKS clusters. HyperPod task governance also provides Amazon EKS cluster Observability, offering real-time visibility into cluster capacity, compute availability and usage, team allocation and utilization, and task run and wait time information.

With Amazon SageMaker Partner AI Apps, users get access to generative artificial intelligence (AI) and machine learning (ML) development applications built, published, and distributed by industry-leading application providers. Partner AI Apps are certified to run on SageMaker AI. With Partner AI Apps, users can accelerate and improve how they build solutions based on foundation models (FM) and classic ML models without compromising the security of their sensitive data, which stays completely within their trusted security configuration and is never shared with a third party.

You can chat with Amazon Q Developer in Amazon SageMaker Canvas using natural language for generative AI assistance with solving your machine learning problems. You can converse with Q Developer to discuss the steps of a machine learning workflow and leverage Canvas functionality such as data transforms, model building, and deployment.

Amazon SageMaker training plans are a compute reservation capability designed for large-scale AI model training workloads running on SageMaker training jobs and HyperPod clusters. They provide predictable access to high-demand GPU-accelerated computing resources within specified timelines. You can specify a desired timeline, duration, and maximum com

*[Content truncated]*

---

## Use custom setup for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/onboard-custom.html

**Contents:**
- Use custom setup for Amazon SageMaker AI
        - Topics
- Authentication methods
- Setup for organizations (custom setup)
        - Open the Set up SageMaker AI Domain from the SageMaker AI console
- Access the domain after onboarding

The Set up for organizations (custom setup) guides you through an advanced setup for your Amazon SageMaker AI domain. This option provides information and recommendations to help you understand and control all aspects of the account configuration, including permissions, integrations, and encryption. Use this option if you want to set up a custom domain. For information about domains, see Amazon SageMaker AI domain overview.

Authentication methods

Setup for organizations (custom setup)

Access the domain after onboarding

Before you set up the domain consider the authentication methods for your users to access the domain.

Helps simplify administration of access permissions to groups of users. You can grant or deny permissions to groups of users, instead of applying those permissions to each individual user. If a user moves to a different organization, you can move that user to a different AWS Identity and Access Management Identity center (AWS IAM Identity Center) group. The user then automatically receives the permissions that are needed for the new organization.

Note that the IAM Identity Center needs to be in the same AWS Region as the domain.

To set up with IAM Identity Center, use the following instructions from the AWS IAM Identity Center User Guide:

Begin with Enabling AWS IAM Identity Center.

Create a permission set that follows the best practice of applying least-privilege permissions.

Add groups to your IAM Identity Center directory.

Assign single sign-on access to users and groups.

View the basic workflows to get started with common tasks in IAM Identity Center.

The users in IAM Identity Center can access the domain using an AWS access portal URL that is emailed to them. The email provides instructions to create an account to access the domain. For more information, see Sign in to the AWS access portal.

As an administrator you can find the AWS access portal URL by navigating to the IAM Identity Center and finding the AWS access portal URL under Settings summary.

Your domain must use AWS Identity and Access Management (IAM) authentication if you wish to restrict access to your domains exclusively to particular Amazon Virtual Private Clouds (VPCs), interface endpoints, or a predefined set of IP addresses. This feature is not supported for domains that use IAM Identity Center authentication. You can still use IAM Identity Center to enable centralized workforce identity control. For instructions on how to implement these restrictions whi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "license-manager:ExtendLicenseConsumption",
                "license-manager:ListReceivedLicenses",
                "license-manager:GetLicense",
                "license-manager:CheckoutLicense",
                "license-manager:CheckInLicense",
                "logs:CreateLogDelivery",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DeleteLogDelivery",
                "logs:De
...
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "license-manager:ExtendLicenseConsumption",
                "license-manager:ListReceivedLicenses",
                "license-manager:GetLicense",
                "license-manager:CheckoutLicense",
                "license-manager:CheckInLicense",
                "logs:CreateLogDelivery",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DeleteLogDelivery",
                "logs:De
...
```

Example 3 (unknown):
```unknown
aws iam create-role --role-name execution-role-name --assume-role-policy-document file://execution-role-trust-policy.json
aws iam attach-role-policy --role-name execution-role-name --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
```

Example 4 (unknown):
```unknown
execution-role-name
```

---

## Amazon SageMaker AI Features

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis-features.html#whatis-features-alpha-major

**Contents:**
- Amazon SageMaker AI Features
        - Topics
- New features for re:Invent 2024
- Machine learning environments
- Major features

Amazon SageMaker AI includes the following features.

New features for re:Invent 2024

Machine learning environments

SageMaker AI includes the following new features for re:Invent 2024.

You can run recipes within Amazon SageMaker HyperPod or as SageMaker training jobs. You use the HyperPod training adapter as the framework to help you run end-to-end training workflows. The training adapter is built on the NVIDIA NeMo framework and Neuronx Distributed Training package.

In Amazon SageMaker Studio, you can launch machine learning workloads on HyperPod clusters and view HyperPod cluster information. The increased visibility into cluster details and hardware metrics can help your team identify the right candidate for your pre-training or fine-tuning workloads.

Amazon SageMaker HyperPod task governance is a robust management system designed to streamline resource allocation and ensure efficient utilization of compute resources across teams and projects for your Amazon EKS clusters. HyperPod task governance also provides Amazon EKS cluster Observability, offering real-time visibility into cluster capacity, compute availability and usage, team allocation and utilization, and task run and wait time information.

With Amazon SageMaker Partner AI Apps, users get access to generative artificial intelligence (AI) and machine learning (ML) development applications built, published, and distributed by industry-leading application providers. Partner AI Apps are certified to run on SageMaker AI. With Partner AI Apps, users can accelerate and improve how they build solutions based on foundation models (FM) and classic ML models without compromising the security of their sensitive data, which stays completely within their trusted security configuration and is never shared with a third party.

You can chat with Amazon Q Developer in Amazon SageMaker Canvas using natural language for generative AI assistance with solving your machine learning problems. You can converse with Q Developer to discuss the steps of a machine learning workflow and leverage Canvas functionality such as data transforms, model building, and deployment.

Amazon SageMaker training plans are a compute reservation capability designed for large-scale AI model training workloads running on SageMaker training jobs and HyperPod clusters. They provide predictable access to high-demand GPU-accelerated computing resources within specified timelines. You can specify a desired timeline, duration, and maximum com

*[Content truncated]*

---

## Getting started with using Amazon SageMaker Canvas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-getting-started.html#canvas-prerequisites

**Contents:**
- Getting started with using Amazon SageMaker Canvas
        - Topics
- Prerequisites for setting up Amazon SageMaker Canvas
        - Important
  - Onboard with the AWS console
        - Note
  - Give yourself permissions to use specific features in Canvas
        - Note
- Step 1: Log in to SageMaker Canvas
- Step 2: Use SageMaker Canvas to get predictions

This guide tells you how to get started with using SageMaker Canvas. If you're an IT administrator and would like more in-depth details, see Amazon SageMaker Canvas setup and permissions management (for IT administrators) to set up SageMaker Canvas for your users.

Prerequisites for setting up Amazon SageMaker Canvas

Step 1: Log in to SageMaker Canvas

Step 2: Use SageMaker Canvas to get predictions

To set up a SageMaker Canvas application, onboard using one of the following setup methods:

Onboard with the AWS console. To onboard through the AWS console, you first create an Amazon SageMaker AI domain. SageMaker AI domains support the various machine learning (ML) environments such as Canvas and SageMaker Studio. For more information about domains, see Amazon SageMaker AI domain overview.

(Quick) Use quick setup for Amazon SageMaker AI – Choose this option if you’d like to quickly set up a domain. This grants your user all of the default Canvas permissions and basic functionality. Any additional features such as document querying can be enabled later by an admin. If you want to configure more granular permissions, we recommend that you choose the Advanced option instead.

(Standard) Use custom setup for Amazon SageMaker AI – Choose this option if you’d like to complete a more advanced setup of your domain. Maintain granular control over user permissions such as access to data preparation features, generative AI functionality, and model deployments.

Onboard with AWS CloudFormation. AWS CloudFormation automates the provisioning of resources and configurations so that you can set up Canvas for one or more user profiles at the same time. Use this option if you want to automate the onboarding process at scale and make sure that your applications are configured the same way every time. The following CloudFormation template provides a streamlined way to onboard to Canvas, ensuring that all required components are properly set up and allowing you to focus on building and deploying your machine learning models.

The following section describes how to onboard to Canvas by using the AWS console to create a domain.

For you to set up Amazon SageMaker Canvas, your version of Amazon SageMaker Studio must be 3.19.0 or later. For information about updating Amazon SageMaker Studio, see Shut Down and Update Amazon SageMaker Studio Classic.

If you’re doing the quick domain setup, then you can follow the instructions in Use quick setup for Amazon SageMaker AI, skip the r

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
s3://sagemaker-{Region}-{your-account-id}
```

Example 2 (unknown):
```unknown
{your-account-id}
```

Example 3 (unknown):
```unknown
s3://sagemaker-{Region}-{your-account-id}
```

Example 4 (unknown):
```unknown
{your-account-id}
```

---

## What is Amazon SageMaker AI?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html

**Contents:**
- What is Amazon SageMaker AI?
        - Topics
- Amazon SageMaker AI rename
  - Legacy namespaces remain the same
- Amazon SageMaker and Amazon SageMaker AI
- Pricing for Amazon SageMaker AI

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment. It provides a UI experience for running ML workflows that makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own servers. This gives you or your organizations more time to collaboratively build and develop your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently against extremely large data in a distributed environment. With built-in support for bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and scalable environment from the SageMaker AI console.

Amazon SageMaker AI rename

Amazon SageMaker and Amazon SageMaker AI

Pricing for Amazon SageMaker AI

Recommendations for a first-time user of Amazon SageMaker AI

Overview of machine learning with Amazon SageMaker AI

Amazon SageMaker AI Features

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI. This name change does not apply to any of the existing Amazon SageMaker features.

The sagemaker API namespaces, along with the following related namespaces, remain unchanged for backward compatibility purposes.

Managed policies containing AmazonSageMaker prefixes

Service endpoints containing sagemaker

AWS CloudFormation resources containing AWS::SageMaker prefixes

Service-linked role containing AWSServiceRoleForSageMaker

Console URLs containing sagemaker

Documentation URLs containing sagemaker

On December 03, 2024, Amazon released the next generation of Amazon SageMaker.

Amazon SageMaker is a unified platform for data, analytics, and AI. Bringing together AWS machine learning and analytics capabilities, the next generation of SageMaker delivers an integrated experience for analytics and AI with unified access to all your data.

Amazon SageMaker includes the following capabilities:

Amazon SageMaker AI (formerly Amazon SageMaker) - Build, train, and deploy ML and foundation models, with fully managed infrastructure, tools, and workflows

Amazon SageMaker Lakehouse – Unify data access across Amazon S3 data lakes, Amazon Redshift, and othe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker
```

Example 2 (unknown):
```unknown
AWS::SageMaker
```

Example 3 (unknown):
```unknown
AWSServiceRoleForSageMaker
```

---

## Amazon SageMaker AI Features

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis-features.html#whatis-features-alpha-mle

**Contents:**
- Amazon SageMaker AI Features
        - Topics
- New features for re:Invent 2024
- Machine learning environments
- Major features

Amazon SageMaker AI includes the following features.

New features for re:Invent 2024

Machine learning environments

SageMaker AI includes the following new features for re:Invent 2024.

You can run recipes within Amazon SageMaker HyperPod or as SageMaker training jobs. You use the HyperPod training adapter as the framework to help you run end-to-end training workflows. The training adapter is built on the NVIDIA NeMo framework and Neuronx Distributed Training package.

In Amazon SageMaker Studio, you can launch machine learning workloads on HyperPod clusters and view HyperPod cluster information. The increased visibility into cluster details and hardware metrics can help your team identify the right candidate for your pre-training or fine-tuning workloads.

Amazon SageMaker HyperPod task governance is a robust management system designed to streamline resource allocation and ensure efficient utilization of compute resources across teams and projects for your Amazon EKS clusters. HyperPod task governance also provides Amazon EKS cluster Observability, offering real-time visibility into cluster capacity, compute availability and usage, team allocation and utilization, and task run and wait time information.

With Amazon SageMaker Partner AI Apps, users get access to generative artificial intelligence (AI) and machine learning (ML) development applications built, published, and distributed by industry-leading application providers. Partner AI Apps are certified to run on SageMaker AI. With Partner AI Apps, users can accelerate and improve how they build solutions based on foundation models (FM) and classic ML models without compromising the security of their sensitive data, which stays completely within their trusted security configuration and is never shared with a third party.

You can chat with Amazon Q Developer in Amazon SageMaker Canvas using natural language for generative AI assistance with solving your machine learning problems. You can converse with Q Developer to discuss the steps of a machine learning workflow and leverage Canvas functionality such as data transforms, model building, and deployment.

Amazon SageMaker training plans are a compute reservation capability designed for large-scale AI model training workloads running on SageMaker training jobs and HyperPod clusters. They provide predictable access to high-demand GPU-accelerated computing resources within specified timelines. You can specify a desired timeline, duration, and maximum com

*[Content truncated]*

---

## Choose an Amazon VPC

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/onboard-vpc.html

**Contents:**
- Choose an Amazon VPC
        - To specify the Amazon VPC information
        - Note
        - Note

This topic provides detailed information about choosing an Amazon Virtual Private Cloud (Amazon VPC) when you onboard to Amazon SageMaker AI domain. For more information about onboarding to SageMaker AI domain, see Amazon SageMaker AI domain overview.

By default, SageMaker AI domain uses two Amazon VPCs. One Amazon VPC is managed by Amazon SageMaker AI and provides direct internet access. You specify the other Amazon VPC, which provides encrypted traffic between the domain and your Amazon Elastic File System (Amazon EFS) volume.

You can change this behavior so that SageMaker AI sends all traffic over your specified Amazon VPC. When you choose this option, you must provide the subnets, security groups, and interface endpoints that are necessary to communicate with the SageMaker API and SageMaker AI runtime, and various AWS services, such as Amazon Simple Storage Service (Amazon S3) and Amazon CloudWatch, that are used by Studio.

When you onboard to SageMaker AI domain, you tell SageMaker AI to send all traffic over your Amazon VPC by setting the network access type to VPC only.

When you specify the Amazon VPC entities (that is, the Amazon VPC, subnet, or security group) in the following procedure, one of three options is presented based on the number of entities you have in the current AWS Region. The behavior is as follows:

One entity – SageMaker AI uses that entity. This can't be changed.

Multiple entities – You must choose the entities from the dropdown list.

No entities – You must create one or more entities in order to use domain. Choose Create <entity> to open the VPC console in a new browser tab. After you create the entities, return to the domain Get started page to continue the onboarding process.

This procedure is part of the Amazon SageMaker AI domain onboarding process when you choose Set up for organizations. Your Amazon VPC information is specified under the Network section.

Select the network access type.

If VPC only is selected, SageMaker AI automatically applies the security group settings defined for the domain to all shared spaces created in the domain. If Public internet only is selected, SageMaker AI does not apply the security group settings to shared spaces created in the domain.

Public internet only – Non-Amazon EFS traffic goes through a SageMaker AI managed Amazon VPC, which allows internet access. Traffic between the domain and your Amazon EFS volume is through the specified Amazon VPC.

VPC only – All SageMaker AI traf

*[Content truncated]*

---

## Getting started with using Amazon SageMaker Canvas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-getting-started.html

**Contents:**
- Getting started with using Amazon SageMaker Canvas
        - Topics
- Prerequisites for setting up Amazon SageMaker Canvas
        - Important
  - Onboard with the AWS console
        - Note
  - Give yourself permissions to use specific features in Canvas
        - Note
- Step 1: Log in to SageMaker Canvas
- Step 2: Use SageMaker Canvas to get predictions

This guide tells you how to get started with using SageMaker Canvas. If you're an IT administrator and would like more in-depth details, see Amazon SageMaker Canvas setup and permissions management (for IT administrators) to set up SageMaker Canvas for your users.

Prerequisites for setting up Amazon SageMaker Canvas

Step 1: Log in to SageMaker Canvas

Step 2: Use SageMaker Canvas to get predictions

To set up a SageMaker Canvas application, onboard using one of the following setup methods:

Onboard with the AWS console. To onboard through the AWS console, you first create an Amazon SageMaker AI domain. SageMaker AI domains support the various machine learning (ML) environments such as Canvas and SageMaker Studio. For more information about domains, see Amazon SageMaker AI domain overview.

(Quick) Use quick setup for Amazon SageMaker AI – Choose this option if you’d like to quickly set up a domain. This grants your user all of the default Canvas permissions and basic functionality. Any additional features such as document querying can be enabled later by an admin. If you want to configure more granular permissions, we recommend that you choose the Advanced option instead.

(Standard) Use custom setup for Amazon SageMaker AI – Choose this option if you’d like to complete a more advanced setup of your domain. Maintain granular control over user permissions such as access to data preparation features, generative AI functionality, and model deployments.

Onboard with AWS CloudFormation. AWS CloudFormation automates the provisioning of resources and configurations so that you can set up Canvas for one or more user profiles at the same time. Use this option if you want to automate the onboarding process at scale and make sure that your applications are configured the same way every time. The following CloudFormation template provides a streamlined way to onboard to Canvas, ensuring that all required components are properly set up and allowing you to focus on building and deploying your machine learning models.

The following section describes how to onboard to Canvas by using the AWS console to create a domain.

For you to set up Amazon SageMaker Canvas, your version of Amazon SageMaker Studio must be 3.19.0 or later. For information about updating Amazon SageMaker Studio, see Shut Down and Update Amazon SageMaker Studio Classic.

If you’re doing the quick domain setup, then you can follow the instructions in Use quick setup for Amazon SageMaker AI, skip the r

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
s3://sagemaker-{Region}-{your-account-id}
```

Example 2 (unknown):
```unknown
{your-account-id}
```

Example 3 (unknown):
```unknown
s3://sagemaker-{Region}-{your-account-id}
```

Example 4 (unknown):
```unknown
{your-account-id}
```

---

## Use quick setup for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/onboard-quick-start.html

**Contents:**
- Use quick setup for Amazon SageMaker AI
- Setup for single users (Quick setup)
- After quick setup

The Set up for single users (quick setup) procedure gets you set up with default settings. Use this option if you want to get started with SageMaker AI quickly and you do not intend to customize your settings at this time. The default settings include granting access to the common SageMaker AI services for individual users to get started. For example, Amazon SageMaker Studio and Amazon SageMaker Canvas.

After satisfying the prerequisites in Complete Amazon SageMaker AI prerequisites, use the following instructions.

Open the SageMaker AI console.

Open the left navigation pane.

Under Admin configurations, choose Domains.

Choose Create domain.

Choose Set up for single user (Quick setup). Your domain and user profile are created automatically.

The Set up for single user process creates a domain and user profile for you automatically. If you want to learn about how the domain is set up for you when using the quick setup option, expand the following section.

When you onboard to Amazon SageMaker AI domain using the Set up for single user procedure, your domain is automatically set up with the following default settings. For information about domains, see Amazon SageMaker AI domain overview.

Domain name: SageMaker AI automatically assigns the name of the domain with a timestamp in the following format.

User profile name: SageMaker AI automatically assigns the name of the user profile with a timestamp in the following format.

Domain execution role: SageMaker AI creates a new IAM role and attaches the AmazonSageMakerFullAccess policy. When using the quick setup and the updated Amazon SageMaker Studio is your default experience, your IAM role also includes the AmazonSageMakerCanvasFullAccess, AmazonSageMakerCanvasAIServicesAccess, AmazonS3FullAccess policies.

User profile execution role: SageMaker AI sets the user profile execution role to the same IAM role used for the domain execution role.

Shared space execution role: SageMaker AI sets the shared space execution role to the same IAM role used for the domain execution role.

SageMaker Canvas time series forecasting role: SageMaker AI creates a new IAM role with the permissions required to use the SageMaker Canvas time series forecasting feature.

Amazon S3 bucket: SageMaker AI creates an Amazon S3 bucket named with the following format.

Amazon VPC: SageMaker AI selects a public VPC with the following logic.

If there is a default VPC with associated subnets in the Region, SageMaker AI uses it.

If the

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
QuickSetupDomain-YYYYMMDDTHHMMSS
```

Example 2 (unknown):
```unknown
default-YYYYMMDDTHHMMSS
```

Example 3 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 4 (unknown):
```unknown
AmazonSageMakerCanvasFullAccess
```

---

## Amazon SageMaker AI Features

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis-features.html#whatis-features-alpha-new

**Contents:**
- Amazon SageMaker AI Features
        - Topics
- New features for re:Invent 2024
- Machine learning environments
- Major features

Amazon SageMaker AI includes the following features.

New features for re:Invent 2024

Machine learning environments

SageMaker AI includes the following new features for re:Invent 2024.

You can run recipes within Amazon SageMaker HyperPod or as SageMaker training jobs. You use the HyperPod training adapter as the framework to help you run end-to-end training workflows. The training adapter is built on the NVIDIA NeMo framework and Neuronx Distributed Training package.

In Amazon SageMaker Studio, you can launch machine learning workloads on HyperPod clusters and view HyperPod cluster information. The increased visibility into cluster details and hardware metrics can help your team identify the right candidate for your pre-training or fine-tuning workloads.

Amazon SageMaker HyperPod task governance is a robust management system designed to streamline resource allocation and ensure efficient utilization of compute resources across teams and projects for your Amazon EKS clusters. HyperPod task governance also provides Amazon EKS cluster Observability, offering real-time visibility into cluster capacity, compute availability and usage, team allocation and utilization, and task run and wait time information.

With Amazon SageMaker Partner AI Apps, users get access to generative artificial intelligence (AI) and machine learning (ML) development applications built, published, and distributed by industry-leading application providers. Partner AI Apps are certified to run on SageMaker AI. With Partner AI Apps, users can accelerate and improve how they build solutions based on foundation models (FM) and classic ML models without compromising the security of their sensitive data, which stays completely within their trusted security configuration and is never shared with a third party.

You can chat with Amazon Q Developer in Amazon SageMaker Canvas using natural language for generative AI assistance with solving your machine learning problems. You can converse with Q Developer to discuss the steps of a machine learning workflow and leverage Canvas functionality such as data transforms, model building, and deployment.

Amazon SageMaker training plans are a compute reservation capability designed for large-scale AI model training workloads running on SageMaker training jobs and HyperPod clusters. They provide predictable access to high-demand GPU-accelerated computing resources within specified timelines. You can specify a desired timeline, duration, and maximum com

*[Content truncated]*

---

## What is a SageMaker AI Project?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-whatis.html

**Contents:**
- What is a SageMaker AI Project?
- When Should You Use a SageMaker AI Project?
        - Important
- What is in a SageMaker AI Project?
- Do I Need to Create a Project to Use SageMaker AI Pipelines?

SageMaker Projects help organizations set up and standardize developer environments for data scientists and CI/CD systems for MLOps engineers. Projects also help organizations set up dependency management, code repository management, build reproducibility, and artifact sharing.

You can provision SageMaker Projects from the AWS Service Catalog using custom or SageMaker AI-provided templates. For information about the AWS Service Catalog, see What Is AWS Service Catalog. With SageMaker Projects, MLOps engineers and organization admins can define their own templates or use SageMaker AI-provided templates. The SageMaker AI-provided templates bootstrap the ML workflow with source version control, automated ML pipelines, and a set of code to quickly start iterating over ML use cases.

Effective September 9, 2024, project templates that use the AWS CodeCommit repository are no longer supported. For new projects, select from the available project templates that use third-party Git repositories.

While notebooks are helpful for model building and experimentation, a team of data scientists and ML engineers sharing code needs a more scalable way to maintain code consistency and strict version control.

Every organization has its own set of standards and practices that provide security and governance for its AWS environment. SageMaker AI provides a set of first-party templates for organizations that want to quickly get started with ML workflows and CI/CD. The templates include projects that use AWS-native services for CI/CD, such as AWS CodeBuild, AWS CodePipeline, and AWS CodeCommit. The templates also offer the option to create projects that use third-party tools, such as Jenkins and GitHub. For a list of the project templates that SageMaker AI provides, see Use SageMaker AI-Provided Project Templates.

Organizations often need tight control over the MLOps resources that they provision and manage. Such responsibility assumes certain tasks, including configuring IAM roles and policies, enforcing resource tags, enforcing encryption, and decoupling resources across multiple accounts. SageMaker Projects can support all these tasks through custom template offerings where organizations use AWS CloudFormation templates to define the resources needed for an ML workflow. Data Scientists can choose a template to bootstrap and pre-configure their ML workflow. These custom templates are created as Service Catalog products and you can provision them in the Studio or Studio Clas

*[Content truncated]*

---

## What is Amazon SageMaker AI?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html#whatis-rename

**Contents:**
- What is Amazon SageMaker AI?
        - Topics
- Amazon SageMaker AI rename
  - Legacy namespaces remain the same
- Amazon SageMaker and Amazon SageMaker AI
- Pricing for Amazon SageMaker AI

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment. It provides a UI experience for running ML workflows that makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own servers. This gives you or your organizations more time to collaboratively build and develop your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently against extremely large data in a distributed environment. With built-in support for bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and scalable environment from the SageMaker AI console.

Amazon SageMaker AI rename

Amazon SageMaker and Amazon SageMaker AI

Pricing for Amazon SageMaker AI

Recommendations for a first-time user of Amazon SageMaker AI

Overview of machine learning with Amazon SageMaker AI

Amazon SageMaker AI Features

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI. This name change does not apply to any of the existing Amazon SageMaker features.

The sagemaker API namespaces, along with the following related namespaces, remain unchanged for backward compatibility purposes.

Managed policies containing AmazonSageMaker prefixes

Service endpoints containing sagemaker

AWS CloudFormation resources containing AWS::SageMaker prefixes

Service-linked role containing AWSServiceRoleForSageMaker

Console URLs containing sagemaker

Documentation URLs containing sagemaker

On December 03, 2024, Amazon released the next generation of Amazon SageMaker.

Amazon SageMaker is a unified platform for data, analytics, and AI. Bringing together AWS machine learning and analytics capabilities, the next generation of SageMaker delivers an integrated experience for analytics and AI with unified access to all your data.

Amazon SageMaker includes the following capabilities:

Amazon SageMaker AI (formerly Amazon SageMaker) - Build, train, and deploy ML and foundation models, with fully managed infrastructure, tools, and workflows

Amazon SageMaker Lakehouse – Unify data access across Amazon S3 data lakes, Amazon Redshift, and othe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker
```

Example 2 (unknown):
```unknown
AWS::SageMaker
```

Example 3 (unknown):
```unknown
AWSServiceRoleForSageMaker
```

---

## What is Amazon SageMaker AI?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html#first-time-user

**Contents:**
- What is Amazon SageMaker AI?
        - Topics
- Amazon SageMaker AI rename
  - Legacy namespaces remain the same
- Amazon SageMaker and Amazon SageMaker AI
- Pricing for Amazon SageMaker AI

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment. It provides a UI experience for running ML workflows that makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own servers. This gives you or your organizations more time to collaboratively build and develop your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently against extremely large data in a distributed environment. With built-in support for bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and scalable environment from the SageMaker AI console.

Amazon SageMaker AI rename

Amazon SageMaker and Amazon SageMaker AI

Pricing for Amazon SageMaker AI

Recommendations for a first-time user of Amazon SageMaker AI

Overview of machine learning with Amazon SageMaker AI

Amazon SageMaker AI Features

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI. This name change does not apply to any of the existing Amazon SageMaker features.

The sagemaker API namespaces, along with the following related namespaces, remain unchanged for backward compatibility purposes.

Managed policies containing AmazonSageMaker prefixes

Service endpoints containing sagemaker

AWS CloudFormation resources containing AWS::SageMaker prefixes

Service-linked role containing AWSServiceRoleForSageMaker

Console URLs containing sagemaker

Documentation URLs containing sagemaker

On December 03, 2024, Amazon released the next generation of Amazon SageMaker.

Amazon SageMaker is a unified platform for data, analytics, and AI. Bringing together AWS machine learning and analytics capabilities, the next generation of SageMaker delivers an integrated experience for analytics and AI with unified access to all your data.

Amazon SageMaker includes the following capabilities:

Amazon SageMaker AI (formerly Amazon SageMaker) - Build, train, and deploy ML and foundation models, with fully managed infrastructure, tools, and workflows

Amazon SageMaker Lakehouse – Unify data access across Amazon S3 data lakes, Amazon Redshift, and othe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker
```

Example 2 (unknown):
```unknown
AWS::SageMaker
```

Example 3 (unknown):
```unknown
AWSServiceRoleForSageMaker
```

---

## Quickstart: Create a SageMaker AI sandbox domain to launch Amazon EMR clusters in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-emr-cluster-quickstart.html

**Contents:**
- Quickstart: Create a SageMaker AI sandbox domain to launch Amazon EMR clusters in Studio
        - Note
        - To set up your Studio test environment and start running Spark jobs:
- Step 1: Create a SageMaker AI domain for launching Amazon EMR clusters in Studio
        - Note
        - Follow these steps to set up a SageMaker AI domain for launching Amazon EMR clusters from Studio.
- Step 2: Launch a new Amazon EMR cluster from Studio UI
- Step 3: Connect a JupyterLab notebook to the Amazon EMR cluster
        - Launch JupyterLab
        - Create a private space

This section walks you through the quick set up of a complete test environment in Amazon SageMaker Studio. You will be creating a new Studio domain that lets users launch new Amazon EMR clusters directly from Studio. The steps provide an example notebook that you can connect to an Amazon EMR cluster to start running Spark workloads. Using this notebook, you will build a Retrieval Augmented Generation System (RAG) using Amazon EMR Spark distributed processing and OpenSearch vector database.

To get started, sign in to the AWS Management Console using an AWS Identity and Access Management (IAM) user account with admin permissions. For information on how to sign up for an AWS account and create a user with administrative access, see Complete Amazon SageMaker AI prerequisites.

Step 1: Create a SageMaker AI domain for launching Amazon EMR clusters in Studio

Step 2: Launch a new Amazon EMR cluster from Studio UI

Step 3: Connect a JupyterLab notebook to the Amazon EMR cluster

Step 4: Clean up your AWS CloudFormation stack

In the following steps, you apply a AWS CloudFormation stack to automatically create a new SageMaker AI domain. The stack also creates a user profile and configures the needed environment and permissions. The SageMaker AI domain is configured to let you directly launch Amazon EMR clusters from Studio. For this example, the Amazon EMR clusters are created in the same AWS account as SageMaker AI without authentication. You can find additional AWS CloudFormation stacks supporting various authentication methods like Kerberos in the getting_started GitHub repository.

SageMaker AI allows 5 Studio domains per AWS account and AWS Region by default. Ensure your account has no more than 4 domains in your region before you create your stack.

Download the raw file of this AWS CloudFormation template from the sagemaker-studio-emr GitHub repository.

Go to the AWS CloudFormation console: https://console.aws.amazon.com/cloudformation

Choose Create stack and select With new resources (standard) from the drop down menu.

In the Prepare template section, select Choose an existing template.

In the Specify template section, choose Upload a template file.

Upload the downloaded AWS CloudFormation template and choose Next.

In Step 2, enter a Stack name and a SageMakerDomainName then choose Next.

In Step 3, keep all default values and choose Next.

In Step 4, check the box to acknowledge resource creation and choose Create stack. This creates a Studio domai

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-studio-emr
```

Example 2 (unknown):
```unknown
Running/Waiting
```

Example 3 (unknown):
```unknown
wget --no-check-certificate https://raw.githubusercontent.com/aws-samples/sagemaker-studio-foundation-models/main/lab-00-setup/Lab_0_Warm_Up_Deploy_EmbeddingModel_Llama2_on_Nvidia.ipynb
mkdir AWSGuides
cd AWSGuides
wget --no-check-certificate https://raw.githubusercontent.com/aws-samples/sagemaker-studio-foundation-models/main/lab-03-rag/AWSGuides/AmazonSageMakerDeveloperGuide.pdf
wget --no-check-certificate https://raw.githubusercontent.com/aws-samples/sagemaker-studio-foundation-models/main/lab-03-rag/AWSGuides/EC2DeveloperGuide.pdf
wget --no-check-certificate https://raw.githubusercontent.c
...
```

Example 4 (unknown):
```unknown
Lab_0_Warm_Up_Deploy_EmbeddingModel_Llama2_on_Nvidia.ipynb
```

---

## Set up Partner AI Apps

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/partner-app-onboard.html#partner-app-onboard-admin-bedrock

**Contents:**
- Set up Partner AI Apps
- Prerequisites
- Administrative permissions
  - AWS Marketplace subscription for Partner AI Apps
  - Set up Partner AI App execution role
  - Configure Amazon Bedrock integration
        - Important
    - Deepchecks Amazon Bedrock integration
- User permissions
  - Manage user authorization and authentication

The following topics describe the permissions needed to start using Amazon SageMaker Partner AI Apps. The permissions required are split into two parts, depending on the user permissions level:

Administrative permissions – Permissions for administrators setting up data scientist and machine learning (ML) developer environments.

Partner AI Apps management

User permissions – Permissions for data scientists and machine learning developers.

Admins can complete the following prerequisites to set up Partner AI Apps.

(Optional) Onboard to a SageMaker AI domain. Partner AI Apps can be accessed directly from a SageMaker AI domain. For more information, see Amazon SageMaker AI domain overview.

If using Partner AI Apps in a SageMaker AI domain in VPC-only mode, admins must create an endpoint with the following format to connect to the Partner AI Apps. For more information about using Studio in VPC-only mode, see Connect Amazon SageMaker Studio in a VPC to External Resources.

(Optional) If admins are interacting with the domain using the AWS CLI, they must also complete the following prerequisites.

Update the AWS CLI by following the steps in Installing the current AWS CLI Version.

From the local machine, run aws configure and provide AWS credentials. For information about AWS credentials, see Understanding and getting your AWS credentials.

The administrator must add the following permissions to enable Partner AI Apps in SageMaker AI.

Permission to complete AWS Marketplace subscription for Partner AI Apps

Set up Partner AI App execution role

Admins must complete the following steps to add permissions for AWS Marketplace. For information about using AWS Marketplace, see Getting started as a buyer using AWS Marketplace.

Grant permissions for AWS Marketplace. Partner AI Apps administrators require these permissions to purchase subscriptions to Partner AI Apps from AWS Marketplace. To get access to AWS Marketplace, admins must attach the AWSMarketplaceManageSubscriptions managed policy to the IAM role that they're using to access the SageMaker AI console and purchase the app. For details about the AWSMarketplaceManageSubscriptions managed policy, see AWS managed policies for AWS Marketplace buyers. For information about attaching managed policies, see Adding and removing IAM identity permissions.

Grant permissions for SageMaker AI to run operations on the admins behalf using other AWS services. Admins must grant SageMaker AI permissions to use these service

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws.sagemaker.region.partner-app
```

Example 2 (unknown):
```unknown
aws configure
```

Example 3 (unknown):
```unknown
AWSMarketplaceManageSubscriptions
```

Example 4 (unknown):
```unknown
AWSMarketplaceManageSubscriptions
```

---

## What is Amazon SageMaker AI?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html#whatis-rename-unified

**Contents:**
- What is Amazon SageMaker AI?
        - Topics
- Amazon SageMaker AI rename
  - Legacy namespaces remain the same
- Amazon SageMaker and Amazon SageMaker AI
- Pricing for Amazon SageMaker AI

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment. It provides a UI experience for running ML workflows that makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own servers. This gives you or your organizations more time to collaboratively build and develop your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently against extremely large data in a distributed environment. With built-in support for bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and scalable environment from the SageMaker AI console.

Amazon SageMaker AI rename

Amazon SageMaker and Amazon SageMaker AI

Pricing for Amazon SageMaker AI

Recommendations for a first-time user of Amazon SageMaker AI

Overview of machine learning with Amazon SageMaker AI

Amazon SageMaker AI Features

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI. This name change does not apply to any of the existing Amazon SageMaker features.

The sagemaker API namespaces, along with the following related namespaces, remain unchanged for backward compatibility purposes.

Managed policies containing AmazonSageMaker prefixes

Service endpoints containing sagemaker

AWS CloudFormation resources containing AWS::SageMaker prefixes

Service-linked role containing AWSServiceRoleForSageMaker

Console URLs containing sagemaker

Documentation URLs containing sagemaker

On December 03, 2024, Amazon released the next generation of Amazon SageMaker.

Amazon SageMaker is a unified platform for data, analytics, and AI. Bringing together AWS machine learning and analytics capabilities, the next generation of SageMaker delivers an integrated experience for analytics and AI with unified access to all your data.

Amazon SageMaker includes the following capabilities:

Amazon SageMaker AI (formerly Amazon SageMaker) - Build, train, and deploy ML and foundation models, with fully managed infrastructure, tools, and workflows

Amazon SageMaker Lakehouse – Unify data access across Amazon S3 data lakes, Amazon Redshift, and othe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker
```

Example 2 (unknown):
```unknown
AWS::SageMaker
```

Example 3 (unknown):
```unknown
AWSServiceRoleForSageMaker
```

---

## What is Amazon SageMaker AI?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html#whatis-pricing

**Contents:**
- What is Amazon SageMaker AI?
        - Topics
- Amazon SageMaker AI rename
  - Legacy namespaces remain the same
- Amazon SageMaker and Amazon SageMaker AI
- Pricing for Amazon SageMaker AI

Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment. It provides a UI experience for running ML workflows that makes SageMaker AI ML tools available across multiple integrated development environments (IDEs).

With SageMaker AI, you can store and share your data without having to build and manage your own servers. This gives you or your organizations more time to collaboratively build and develop your ML workflow, and do it sooner. SageMaker AI provides managed ML algorithms to run efficiently against extremely large data in a distributed environment. With built-in support for bring-your-own-algorithms and frameworks, SageMaker AI offers flexible distributed training options that adjust to your specific workflows. Within a few steps, you can deploy a model into a secure and scalable environment from the SageMaker AI console.

Amazon SageMaker AI rename

Amazon SageMaker and Amazon SageMaker AI

Pricing for Amazon SageMaker AI

Recommendations for a first-time user of Amazon SageMaker AI

Overview of machine learning with Amazon SageMaker AI

Amazon SageMaker AI Features

On December 03, 2024, Amazon SageMaker was renamed to Amazon SageMaker AI. This name change does not apply to any of the existing Amazon SageMaker features.

The sagemaker API namespaces, along with the following related namespaces, remain unchanged for backward compatibility purposes.

Managed policies containing AmazonSageMaker prefixes

Service endpoints containing sagemaker

AWS CloudFormation resources containing AWS::SageMaker prefixes

Service-linked role containing AWSServiceRoleForSageMaker

Console URLs containing sagemaker

Documentation URLs containing sagemaker

On December 03, 2024, Amazon released the next generation of Amazon SageMaker.

Amazon SageMaker is a unified platform for data, analytics, and AI. Bringing together AWS machine learning and analytics capabilities, the next generation of SageMaker delivers an integrated experience for analytics and AI with unified access to all your data.

Amazon SageMaker includes the following capabilities:

Amazon SageMaker AI (formerly Amazon SageMaker) - Build, train, and deploy ML and foundation models, with fully managed infrastructure, tools, and workflows

Amazon SageMaker Lakehouse – Unify data access across Amazon S3 data lakes, Amazon Redshift, and othe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker
```

Example 2 (unknown):
```unknown
AWS::SageMaker
```

Example 3 (unknown):
```unknown
AWSServiceRoleForSageMaker
```

---

## Quickstart: Query data in Amazon S3

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-sqlexplorer-athena-s3-quickstart.html

**Contents:**
- Quickstart: Query data in Amazon S3
        - Prerequisites
        - To access and query your data in Amazon S3:
- Step 1: Set up an Athena data source and AWS Glue crawler for your Amazon S3 data
        - Note
        - Note
        - Note
- Step 2: Grant Studio the permissions to access Athena
        - Note
- Step 3: Enable Athena default connection in JupyterLab

Users can analyze data stored in Amazon S3 by running SQL queries from JupyterLab notebooks using the SQL extension. The extension integrates with Athena enabling the functionality for data in Amazon S3 with a few extra steps.

This section walks you through the steps to load data from Amazon S3 into Athena and then query that data from JupyterLab using the SQL extension. You will create an Athena data source and AWS Glue crawler to index your Amazon S3 data, configure the proper IAM permissions to enable JupyterLab access to Athena, and connect JupyterLab to Athena to query the data. Following those few steps, you will be able to analyze Amazon S3 data using the SQL extension in JupyterLab notebooks.

Sign in to the AWS Management Console using an AWS Identity and Access Management (IAM) user account with admin permissions. For information on how to sign up for an AWS account and create a user with administrative access, see Complete Amazon SageMaker AI prerequisites.

Have a SageMaker AI domain and user profile to access SageMaker Studio. For information on how to set a SageMaker AI environment, see Use quick setup for Amazon SageMaker AI.

Have an Amazon S3 bucket and folder to store Athena query results, using the same AWS Region and account as your SageMaker AI environment. For information on how to create a bucket in Amazon S3, see Creating a bucket in the Amazon S3 documentation. You will configure this bucket and folder to be your query output location.

Step 1: Set up an Athena data source and AWS Glue crawler for your Amazon S3 data

Step 2: Grant Studio the permissions to access Athena

Step 3: Enable Athena default connection in JupyterLab

Step 4: Query data in Amazon S3 from JupyterLab notebooks using the SQL extension

Follow these steps to index your data in Amazon S3 and create tables in Athena.

To avoid collisions between table names from different Amazon S3 locations, create a separate data source and crawler for each location. Each data source creates a table named after the folder that contain them unless prefixed.

Configure a query result location

Go to the Athena console: https://console.aws.amazon.com/athena/.

From the left menu, choose Workgroups.

Follow the link for the primary workgroup and choose Edit.

In the Query result configuration section, enter the Amazon S3 path for your output directory and then choose Save changes.

Create an Athena data source for your Amazon S3 data

From the left menu in the Athena console, cho

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
s3://dsoaws/nyc-taxi-orig-cleaned-split-parquet-per-year-multiple-files/ride-info/year=2019/
```

Example 2 (unknown):
```unknown
s3://dsoaws/nyc-taxi-orig-cleaned-split-parquet-per-year-multiple-files/ride-info/year=2019/
```

Example 3 (unknown):
```unknown
taxi-ride-year_2019
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "GetS3AndDataSourcesMetadata",
            "Effect": "Allow",
            "Action": [
                "glue:GetDatabases",
                "glue:GetSchema",
                "glue:GetTables",
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetBucketLocation",
                "glue:GetDatabase",
                "glue:GetTable",
                "glue:ListSchemas",
                "glue:GetPartitions"
            ],
            "Resource": [
                "arn:aws:s3:::*",
         
...
```

---

## Amazon SageMaker AI domain overview

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-onboard.html

**Contents:**
- Amazon SageMaker AI domain overview
        - Topics

Amazon SageMaker AI uses domains to organize user profiles, applications, and their associated resources. An Amazon SageMaker AI domain consists of the following:

An associated Amazon Elastic File System (Amazon EFS) volume

A list of authorized users

A variety of security, application, policy, and Amazon Virtual Private Cloud (Amazon VPC) configurations

The following diagram provides an overview of private apps and shared spaces within each domain.

To have access to most Amazon SageMaker AI environments and resources, you must complete the Amazon SageMaker AI domain onboarding process using the SageMaker AI console or the AWS CLI. For a guide describing how to get started using SageMaker AI based on how you want to access SageMaker AI, and if necessary how to set up a domain, see Guide to getting set up with Amazon SageMaker AI.

Amazon SageMaker AI domain entities and statuses

---
