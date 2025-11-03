# Aws-Eks - Addons

**Pages:** 4

---

## Community add-ons

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/community-addons.html

**Contents:**
- Community add-ons
        - Note
- Determine add-on type
- Install or update community add-on
- Available community add-ons
  - Kubernetes Metrics Server
  - kube-state-metrics
  - Prometheus Node Exporter
  - Cert Manager
  - External DNS

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use AWS APIs to install community add-ons, such as the Kubernetes Metrics Server. You may choose to install community add-ons as Amazon EKS Add-ons to reduce the complexity of maintaining the software on multiple clusters.

For example, you can use the AWS API, CLI, or Management Console to install community add-ons. You can install a community add-on during cluster creation.

You manage community add-ons just like existing Amazon EKS Add-ons. Community add-ons are different from existing add-ons in that they have a unique scope of support.

Using community add-ons is at your discretion. As part of the shared responsibility model between you and AWS, you are expected to understand what you are installing into your cluster for these third party plugins. You are also responsible for the community add-ons meeting your cluster security needs. For more information, see Support for software deployed to EKS.

Community add-ons are not built by AWS. AWS only validates community add-ons for version compatibility. For example, if you install a community add-on on a cluster, AWS checks if it is compatible with the Kubernetes version of your cluster.

Importantly, AWS does not provide full support for community add-ons. AWS supports only lifecycle operations done using AWS APIs, such as installing add-ons or deleting add-ons.

If you require support for a community add-on, utilize the existing project resources. For example, you may create a GitHub issue on the repo for the project.

You can use the AWS CLI to determine the type of an Amazon EKS Add-on.

Use the following CLI command to retrieve information about an add-on. You can replace metrics-server with the name of any add-on.

Review the CLI output for the owner field.

If the value of owner is community, then the add-on is a community add-on. AWS only provides support for installing, updating, and removing the add-on. If you have questions about the functionality and operation of the add-on itself, use community resources like GitHub issues.

You install or update community add-ons in the same way as other Amazon EKS Add-ons.

Create an Amazon EKS add-on

Update an Amazon EKS add-on

Remove an Amazon EKS add-on from a cluster

The following community add-ons are available from Amazon EKS.

Kubernetes Metrics Server

Prometheus Node Exporter

The Kubernetes

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
metrics-server
```

Example 2 (unknown):
```unknown
aws eks describe-addon-versions --addon-name metrics-server
```

Example 3 (unknown):
```unknown
metrics-server
```

Example 4 (unknown):
```unknown
kube-system
```

---

## Amazon EKS add-ons

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html

**Contents:**
- Amazon EKS add-ons
- Considerations
- Custom namespace for add-ons
  - Get predefined namespace for add-on
- Considerations for Amazon EKS Auto Mode
- Support

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

An add-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage. Add-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third-party vendors. Amazon EKS automatically installs self-managed add-ons such as the Amazon VPC CNI plugin for Kubernetes, kube-proxy, and CoreDNS for every cluster. Note that the VPC CNI add-on isn’t compatible with Amazon EKS Hybrid Nodes and doesn’t deploy to hybrid nodes. You can change the default configuration of the add-ons and update them when desired.

Amazon EKS add-ons provide installation and management of a curated set of add-ons for Amazon EKS clusters. All Amazon EKS add-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS. Amazon EKS add-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to install, configure, and update add-ons. If a self-managed add-on, such as kube-proxy is already running on your cluster and is available as an Amazon EKS add-on, then you can install the kube-proxy Amazon EKS add-on to start benefiting from the capabilities of Amazon EKS add-ons.

You can update specific Amazon EKS managed configuration fields for Amazon EKS add-ons through the Amazon EKS API. You can also modify configuration fields not managed by Amazon EKS directly within the Kubernetes cluster once the add-on starts. This includes defining specific configuration fields for an add-on where applicable. These changes are not overridden by Amazon EKS once they are made. This is made possible using the Kubernetes server-side apply feature. For more information, see Determine fields you can customize for Amazon EKS add-ons.

You can use Amazon EKS add-ons with any Amazon EKS node type. For more information, see Manage compute resources by using nodes.

You can add, update, or delete Amazon EKS add-ons using the Amazon EKS API, AWS Management Console, AWS CLI, and eksctl. You can also create Amazon EKS add-ons using AWS CloudFormation.

Consider the fo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:addon-cluster-admin
```

Example 2 (unknown):
```unknown
ClusterRoleBinding
```

Example 3 (unknown):
```unknown
cluster-admin
```

Example 4 (unknown):
```unknown
ClusterRole
```

---

## Run critical add-ons on dedicated instances

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/critical-workload.html

**Contents:**
- Run critical add-ons on dedicated instances
- Prerequisites
- Procedure

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

In this topic, you will learn how to deploy a workload with a CriticalAddonsOnly toleration so EKS Auto Mode will schedule it onto the system node pool.

EKS Auto Mode’s built-in system node pool is designed for running critical add-ons on dedicated instances. This segregation ensures essential components have dedicated resources and are isolated from general workloads, enhancing overall cluster stability and performance.

This guide demonstrates how to deploy add-ons to the system node pool by utilizing the CriticalAddonsOnly toleration and appropriate node selectors. By following these steps, you can ensure that your critical applications are scheduled onto the dedicated system nodes, leveraging the isolation and resource allocation benefits provided by EKS Auto Mode’s specialized node pool structure.

EKS Auto Mode has two built-in node pools: general-purpose and system. For more information, see Enable or Disable Built-in NodePools.

The purpose of the system node pool is to segregate critical add-ons onto different nodes. Nodes provisioned by the system node pool have a CriticalAddonsOnly Kubernetes taint. Kubernetes will only schedule pods onto these nodes if they have a corresponding toleration. For more information, see Taints and Tolerations in the Kubernetes documentation.

EKS Auto Mode Cluster with the built-in system node pool enabled. For more information, see Enable or Disable Built-in NodePools

kubectl installed and configured. For more information, see Set up to use Amazon EKS.

Review the example yaml below. Note the following configurations:

nodeSelector — This associates the workload with the built-in system node pool. This node pool must be enabled with the AWS API. For more information, see Enable or Disable Built-in NodePools.

tolerations — This toleration overcomes the CriticalAddonsOnly taint on nodes in the system node pool.

To update a workload to run on the system node pool, you need to:

Update the existing workload to add the following configurations described above:

Deploy the updated workload to your cluster with kubectl apply

After updating the workload, it will run on dedicated nodes.

**Examples:**

Example 1 (unknown):
```unknown
CriticalAddonsOnly
```

Example 2 (unknown):
```unknown
CriticalAddonsOnly
```

Example 3 (unknown):
```unknown
general-purpose
```

Example 4 (unknown):
```unknown
CriticalAddonsOnly
```

---

## Amazon EKS add-ons

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html#custom-namespace

**Contents:**
- Amazon EKS add-ons
- Considerations
- Custom namespace for add-ons
  - Get predefined namespace for add-on
- Considerations for Amazon EKS Auto Mode
- Support

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

An add-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage. Add-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third-party vendors. Amazon EKS automatically installs self-managed add-ons such as the Amazon VPC CNI plugin for Kubernetes, kube-proxy, and CoreDNS for every cluster. Note that the VPC CNI add-on isn’t compatible with Amazon EKS Hybrid Nodes and doesn’t deploy to hybrid nodes. You can change the default configuration of the add-ons and update them when desired.

Amazon EKS add-ons provide installation and management of a curated set of add-ons for Amazon EKS clusters. All Amazon EKS add-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS. Amazon EKS add-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to install, configure, and update add-ons. If a self-managed add-on, such as kube-proxy is already running on your cluster and is available as an Amazon EKS add-on, then you can install the kube-proxy Amazon EKS add-on to start benefiting from the capabilities of Amazon EKS add-ons.

You can update specific Amazon EKS managed configuration fields for Amazon EKS add-ons through the Amazon EKS API. You can also modify configuration fields not managed by Amazon EKS directly within the Kubernetes cluster once the add-on starts. This includes defining specific configuration fields for an add-on where applicable. These changes are not overridden by Amazon EKS once they are made. This is made possible using the Kubernetes server-side apply feature. For more information, see Determine fields you can customize for Amazon EKS add-ons.

You can use Amazon EKS add-ons with any Amazon EKS node type. For more information, see Manage compute resources by using nodes.

You can add, update, or delete Amazon EKS add-ons using the Amazon EKS API, AWS Management Console, AWS CLI, and eksctl. You can also create Amazon EKS add-ons using AWS CloudFormation.

Consider the fo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks:addon-cluster-admin
```

Example 2 (unknown):
```unknown
ClusterRoleBinding
```

Example 3 (unknown):
```unknown
cluster-admin
```

Example 4 (unknown):
```unknown
ClusterRole
```

---
