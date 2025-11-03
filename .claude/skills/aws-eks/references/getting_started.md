# Aws-Eks - Getting Started

**Pages:** 9

---

## Quickstart: Deploy a web app and store data

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/quickstart.html

**Contents:**
- Quickstart: Deploy a web app and store data
- In this tutorial
- Prerequisites
- Configure the cluster
        - Important
- Create IngressClass
- Deploy the 2048 game sample application
        - Note
- Persist Data using Amazon EKS Auto Mode
- Delete your cluster and nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Deploy a game application and persist its data on Amazon EKS

This quickstart tutorial shows the steps to deploy the 2048 game sample application and persist its data on an Amazon EKS Auto Mode cluster using eksctl. Amazon EKS Auto Mode automates routine tasks for cluster block storage, networking, load balancing, and compute autoscaling.

As we progress, we’ll walk you through the cluster setup process. Amazon EKS Auto Mode will automate tasks for creating a node using an EC2 managed instance, creating an application load balancer, and creating an EBS volume.

Overall, you’ll deploy a sample workload with the custom annotations required to fully integrate with AWS services.

Using the eksctl cluster template that follows, you’ll build a cluster with EKS Auto Mode for automated node provisioning.

VPC Configuration When using the eksctl cluster template that follows, eksctl automatically creates an IPv4 Virtual Private Cloud (VPC) for the cluster. By default, eksctl configures a VPC that addresses all networking requirements, in addition to creating both public and private endpoints.

Instance Management EKS Auto Mode dynamically adds or removes nodes in your EKS cluster based on the demands of your Kubernetes applications.

Data Persistence Use the block storage capability of EKS Auto Mode to ensure the persistence of application data, even in scenarios involving pod restarts or failures.

External App Access Use the load balancing capability of EKS Auto Mode to dynamically provision an Application Load Balancer (ALB).

Before you begin, ensure you have the following prerequisites set up to use Amazon EKS:

Set up AWS CLI and configure credentials

For more information, see Set up to use Amazon EKS.

In this section, you’ll create a cluster using EKS Auto Mode for dynamic node provisioning.

Create a cluster-config.yaml file and paste the following contents into it. Replace region-code with a valid Region, such as us-east-1:

Now, we’re ready to create the cluster.

Create the Amazon EKS cluster:

If you do not use eksctl to create the cluster, you need to manually tag the VPC subnets.

Create a Kubernetes IngressClass for EKS Auto Mode. The IngressClass defines how EKS Auto Mode handles Ingress resources. This step configures the load balancing capability of EKS Auto Mode. When you create Ingress resources f

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
cluster-config.yaml
```

Example 2 (unknown):
```unknown
region-code
```

Example 3 (unknown):
```unknown
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: web-quickstart
  region: <region-code>

autoModeConfig:
  enabled: true
```

Example 4 (unknown):
```unknown
eksctl create cluster -f cluster-config.yaml
```

---

## Get started with Amazon EKS – AWS Management Console and AWS CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html#gs-console-next-steps

**Contents:**
- Get started with Amazon EKS – AWS Management Console and AWS CLI
        - Note
- Prerequisites
- Step 1: Create your Amazon EKS cluster
        - Important
        - Tip
        - Note
- Step 2: Configure your computer to communicate with your cluster
        - Note
- Step 3: Create nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers getting started without EKS Auto Mode. It uses Managed Node Groups to deploy nodes.

EKS Auto Mode automates routine tasks for cluster compute, storage, and networking. Learn how to get started with Amazon EKS Auto Mode. EKS Auto Mode is the preferred method of deploying nodes.

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service (Amazon EKS) using the AWS Management Console and the AWS CLI. In this guide, you manually create each resource. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to.

The procedures in this guide give you complete visibility into how each resource is created and how the resources interact with each other. If you’d rather have most of the resources created for you automatically, use the eksctl CLI to create your cluster and nodes. For more information, see Get started with Amazon EKS – eksctl.

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster.

AWS CLI – A command line tool for working with AWS services, including Amazon EKS. For more information, see Installing in the AWS Command Line Interface User Guide. After installing the AWS CLI, we recommend that you also configure it. For more information, see Quick configuration with aws configure in the AWS Command Line Interface User Guide. Note that AWS CLI v2 is required to use the update-kubeconfig option shown in this page.

kubectl – A command line tool for working with Kubernetes clusters. For more information, see Set up kubectl and eksctl.

Required IAM permissions – The IAM security principal that you’re using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources. For more information, see Actions and Using service-linked roles in the IAM User Guide. You must complete all steps in this guide as the same user. To check the current user, run the following command:

We recommend that you complete the steps in this topic in a Bash shell. If you aren’t using a Bash shell, some script commands such as line continuation characters and the way variables are set and used require adjustment for your shell. Additionally, the quoting 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws sts get-caller-identity
```

Example 2 (unknown):
```unknown
region-code
```

Example 3 (unknown):
```unknown
my-eks-vpc-stack
```

Example 4 (unknown):
```unknown
aws cloudformation create-stack \
  --region region-code \
  --stack-name my-eks-vpc-stack \
  --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
```

---

## Get started with Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html

**Contents:**
- Get started with Amazon EKS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Make sure that you are set up to use Amazon EKS before going through the getting started guides. For more information, see Set up to use Amazon EKS.

There are two getting started guides available for creating a new Kubernetes cluster with nodes in Amazon EKS:

Get started with Amazon EKS – eksctl – This getting started guide helps you to install all of the required resources to get started with Amazon EKS using eksctl, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS. At the end of the tutorial, you will have a running Amazon EKS cluster that you can deploy applications to. This is the fastest and simplest way to get started with Amazon EKS.

Get started with Amazon EKS – AWS Management Console and AWS CLI – This getting started guide helps you to create all of the required resources to get started with Amazon EKS using the AWS Management Console and AWS CLI. At the end of the tutorial, you will have a running Amazon EKS cluster that you can deploy applications to. In this guide, you manually create each resource required for an Amazon EKS cluster. The procedures give you visibility into how each resource is created and how they interact with each other.

We also offer the following references:

For a collection of hands-on tutorials, see EKS Cluster Setup on AWS Community.

For code examples, see Code examples for Amazon EKS using AWS SDKs.

---

## Get started with Amazon EKS – eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html#gs-eksctl-next-steps

**Contents:**
- Get started with Amazon EKS – eksctl
        - Note
- Prerequisites
- Step 1: Create your Amazon EKS cluster and nodes
        - Important
- Step 2: View Kubernetes resources
- Step 3: Delete your cluster and nodes
- Next steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers getting started without EKS Auto Mode.

EKS Auto Mode automates routine tasks for cluster compute, storage, and networking. Learn how to get started with Amazon EKS Auto Mode.

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service (Amazon EKS) using eksctl, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to.

The procedures in this guide create several resources for you automatically that you have to create manually when you create your cluster using the AWS Management Console. If you’d rather manually create most of the resources to better understand how they interact with each other, then use the AWS Management Console to create your cluster and compute. For more information, see Get started with Amazon EKS – AWS Management Console and AWS CLI.

Before starting this tutorial, you must install and configure the AWS CLI, kubectl, and eksctl tools as described in Set up to use Amazon EKS.

To get started as simply and quickly as possible, this topic includes steps to create a cluster and nodes with default settings. Before creating a cluster and nodes for production use, we recommend that you familiarize yourself with all settings and deploy a cluster and nodes with the settings that meet your requirements. For more information, see Create an Amazon EKS cluster and Manage compute resources by using nodes. Some settings can only be enabled when creating your cluster and nodes.

You can create a cluster with one of the following node types. To learn more about each type, see Manage compute resources by using nodes. After your cluster is deployed, you can add other node types.

Fargate – Linux – Select this type of node if you want to run Linux applications on Simplify compute management with AWS Fargate. Fargate is a serverless compute engine that lets you deploy Kubernetes Pods without managing Amazon EC2 instances.

Managed nodes – Linux – Select this type of node if you want to run Amazon Linux applications on Amazon EC2 instances. Though not covered in this guide, you can also add Windows self-managed and Bottlerocket nodes to your cluster.

Create your Amazon EKS cluster with the follo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
region-code
```

Example 2 (unknown):
```unknown
eksctl create cluster --name my-cluster --region region-code --fargate
```

Example 3 (unknown):
```unknown
eksctl create cluster --name my-cluster --region region-code
```

Example 4 (unknown):
```unknown
~/.kube/config
```

---

## What is Amazon EKS?

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html

**Contents:**
- What is Amazon EKS?
- Amazon EKS: Simplified Kubernetes Management
- Features of Amazon EKS
- Related services
- Amazon EKS Pricing

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Amazon Elastic Kubernetes Service (EKS) provides a fully managed Kubernetes service that eliminates the complexity of operating Kubernetes clusters. With EKS, you can:

Deploy applications faster with less operational overhead

Scale seamlessly to meet changing workload demands

Improve security through AWS integration and automated updates

Choose between standard EKS or fully automated EKS Auto Mode

Amazon Elastic Kubernetes Service (Amazon EKS) is the premiere platform for running Kubernetes clusters, both in the Amazon Web Services (AWS) cloud and in your own data centers (EKS Anywhere and Amazon EKS Hybrid Nodes).

Amazon EKS simplifies building, securing, and maintaining Kubernetes clusters. It can be more cost effective at providing enough resources to meet peak demand than maintaining your own data centers. Two of the main approaches to using Amazon EKS are as follows:

EKS standard: AWS manages the Kubernetes control plane when you create a cluster with EKS. Components that manage nodes, schedule workloads, integrate with the AWS cloud, and store and scale control plane information to keep your clusters up and running, are handled for you automatically.

EKS Auto Mode: Using the EKS Auto Mode feature, EKS extends its control to manage Nodes (Kubernetes data plane) as well. It simplifies Kubernetes management by automatically provisioning infrastructure, selecting optimal compute instances, dynamically scaling resources, continuously optimizing costs, patching operating systems, and integrating with AWS security services.

The following diagram illustrates how Amazon EKS integrates your Kubernetes clusters with the AWS cloud, depending on which method of cluster creation you choose:

Amazon EKS helps you accelerate time to production, improve performance, availability and resiliency, and enhance system security. For more information, see Amazon Elastic Kubernetes Service.

Amazon EKS provides the following high-level features:

EKS offers multiple interfaces to provision, manage, and maintain clusters, including AWS Management Console, Amazon EKS API/SDKs, CDK, AWS CLI, eksctl CLI, AWS CloudFormation, and Terraform. For more information, see Get started with Amazon EKS and Amazon EKS cluster lifecycle and configuration.

EKS relies on both Kubernetes and AWS Identity and Access Management (AWS IAM) fe

*[Content truncated]*

---

## Get started with Amazon EKS – EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started-automode.html

**Contents:**
- Get started with Amazon EKS – EKS Auto Mode

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

Like other EKS getting started experiences, creating your first cluster with EKS Auto Mode delegates the management of the cluster itself to AWS. However, EKS Auto Mode extends EKS automation by handing responsibility of many essential services needed to set up workload infrastructure (nodes, networks, and various services), making it easier to manage nodes and scale up to meet workload demands.

Choose from one of the following ways to create a cluster with EKS Auto Mode:

Create an EKS Auto Mode Cluster with the AWS CLI: Use the aws command line interface to create a cluster.

Create an EKS Auto Mode Cluster with the AWS Management Console: Use the AWS Management Console to create a cluster.

Create an EKS Auto Mode Cluster with the eksctl CLI: Use the eksctl command line interface to create a cluster.

If you are comparing different approaches to creating your first EKS cluster, you should know that EKS Auto Mode has AWS take over additional cluster management responsibilities that include setting up components to:

Start up and scale nodes as workload demand increases and decreases.

Regularly upgrade the cluster itself (control plane), node operating systems, and services running on nodes.

Choose default settings that determine things like the size and speed of node storage and Pod network configuration.

For details on what you get with EKS Auto Mode clusters, see Automate cluster infrastructure with EKS Auto Mode.

---

## Get started with Amazon EKS – AWS Management Console and AWS CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html

**Contents:**
- Get started with Amazon EKS – AWS Management Console and AWS CLI
        - Note
- Prerequisites
- Step 1: Create your Amazon EKS cluster
        - Important
        - Tip
        - Note
- Step 2: Configure your computer to communicate with your cluster
        - Note
- Step 3: Create nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers getting started without EKS Auto Mode. It uses Managed Node Groups to deploy nodes.

EKS Auto Mode automates routine tasks for cluster compute, storage, and networking. Learn how to get started with Amazon EKS Auto Mode. EKS Auto Mode is the preferred method of deploying nodes.

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service (Amazon EKS) using the AWS Management Console and the AWS CLI. In this guide, you manually create each resource. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to.

The procedures in this guide give you complete visibility into how each resource is created and how the resources interact with each other. If you’d rather have most of the resources created for you automatically, use the eksctl CLI to create your cluster and nodes. For more information, see Get started with Amazon EKS – eksctl.

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster.

AWS CLI – A command line tool for working with AWS services, including Amazon EKS. For more information, see Installing in the AWS Command Line Interface User Guide. After installing the AWS CLI, we recommend that you also configure it. For more information, see Quick configuration with aws configure in the AWS Command Line Interface User Guide. Note that AWS CLI v2 is required to use the update-kubeconfig option shown in this page.

kubectl – A command line tool for working with Kubernetes clusters. For more information, see Set up kubectl and eksctl.

Required IAM permissions – The IAM security principal that you’re using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources. For more information, see Actions and Using service-linked roles in the IAM User Guide. You must complete all steps in this guide as the same user. To check the current user, run the following command:

We recommend that you complete the steps in this topic in a Bash shell. If you aren’t using a Bash shell, some script commands such as line continuation characters and the way variables are set and used require adjustment for your shell. Additionally, the quoting 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws sts get-caller-identity
```

Example 2 (unknown):
```unknown
region-code
```

Example 3 (unknown):
```unknown
my-eks-vpc-stack
```

Example 4 (unknown):
```unknown
aws cloudformation create-stack \
  --region region-code \
  --stack-name my-eks-vpc-stack \
  --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
```

---

## Get started with Amazon EKS – eksctl

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html

**Contents:**
- Get started with Amazon EKS – eksctl
        - Note
- Prerequisites
- Step 1: Create your Amazon EKS cluster and nodes
        - Important
- Step 2: View Kubernetes resources
- Step 3: Delete your cluster and nodes
- Next steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers getting started without EKS Auto Mode.

EKS Auto Mode automates routine tasks for cluster compute, storage, and networking. Learn how to get started with Amazon EKS Auto Mode.

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service (Amazon EKS) using eksctl, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to.

The procedures in this guide create several resources for you automatically that you have to create manually when you create your cluster using the AWS Management Console. If you’d rather manually create most of the resources to better understand how they interact with each other, then use the AWS Management Console to create your cluster and compute. For more information, see Get started with Amazon EKS – AWS Management Console and AWS CLI.

Before starting this tutorial, you must install and configure the AWS CLI, kubectl, and eksctl tools as described in Set up to use Amazon EKS.

To get started as simply and quickly as possible, this topic includes steps to create a cluster and nodes with default settings. Before creating a cluster and nodes for production use, we recommend that you familiarize yourself with all settings and deploy a cluster and nodes with the settings that meet your requirements. For more information, see Create an Amazon EKS cluster and Manage compute resources by using nodes. Some settings can only be enabled when creating your cluster and nodes.

You can create a cluster with one of the following node types. To learn more about each type, see Manage compute resources by using nodes. After your cluster is deployed, you can add other node types.

Fargate – Linux – Select this type of node if you want to run Linux applications on Simplify compute management with AWS Fargate. Fargate is a serverless compute engine that lets you deploy Kubernetes Pods without managing Amazon EC2 instances.

Managed nodes – Linux – Select this type of node if you want to run Amazon Linux applications on Amazon EC2 instances. Though not covered in this guide, you can also add Windows self-managed and Bottlerocket nodes to your cluster.

Create your Amazon EKS cluster with the follo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
region-code
```

Example 2 (unknown):
```unknown
eksctl create cluster --name my-cluster --region region-code --fargate
```

Example 3 (unknown):
```unknown
eksctl create cluster --name my-cluster --region region-code
```

Example 4 (unknown):
```unknown
~/.kube/config
```

---

## Get started with Amazon EKS – AWS Management Console and AWS CLI

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html#eks-create-cluster

**Contents:**
- Get started with Amazon EKS – AWS Management Console and AWS CLI
        - Note
- Prerequisites
- Step 1: Create your Amazon EKS cluster
        - Important
        - Tip
        - Note
- Step 2: Configure your computer to communicate with your cluster
        - Note
- Step 3: Create nodes

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This topic covers getting started without EKS Auto Mode. It uses Managed Node Groups to deploy nodes.

EKS Auto Mode automates routine tasks for cluster compute, storage, and networking. Learn how to get started with Amazon EKS Auto Mode. EKS Auto Mode is the preferred method of deploying nodes.

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service (Amazon EKS) using the AWS Management Console and the AWS CLI. In this guide, you manually create each resource. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to.

The procedures in this guide give you complete visibility into how each resource is created and how the resources interact with each other. If you’d rather have most of the resources created for you automatically, use the eksctl CLI to create your cluster and nodes. For more information, see Get started with Amazon EKS – eksctl.

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster.

AWS CLI – A command line tool for working with AWS services, including Amazon EKS. For more information, see Installing in the AWS Command Line Interface User Guide. After installing the AWS CLI, we recommend that you also configure it. For more information, see Quick configuration with aws configure in the AWS Command Line Interface User Guide. Note that AWS CLI v2 is required to use the update-kubeconfig option shown in this page.

kubectl – A command line tool for working with Kubernetes clusters. For more information, see Set up kubectl and eksctl.

Required IAM permissions – The IAM security principal that you’re using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources. For more information, see Actions and Using service-linked roles in the IAM User Guide. You must complete all steps in this guide as the same user. To check the current user, run the following command:

We recommend that you complete the steps in this topic in a Bash shell. If you aren’t using a Bash shell, some script commands such as line continuation characters and the way variables are set and used require adjustment for your shell. Additionally, the quoting 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws sts get-caller-identity
```

Example 2 (unknown):
```unknown
region-code
```

Example 3 (unknown):
```unknown
my-eks-vpc-stack
```

Example 4 (unknown):
```unknown
aws cloudformation create-stack \
  --region region-code \
  --stack-name my-eks-vpc-stack \
  --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
```

---
