# Aws-Eks - Deployment

**Pages:** 10

---

## Deploy Prometheus using Helm

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/deploy-prometheus.html

**Contents:**
- Deploy Prometheus using Helm
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

As an alternative to using Amazon Managed Service for Prometheus, you can deploy Prometheus into your cluster with Helm. If you already have Helm installed, you can check your version with the helm version command. Helm is a package manager for Kubernetes clusters. For more information about Helm and how to install it, see Deploy applications with Helm on Amazon EKS.

After you configure Helm for your Amazon EKS cluster, you can use it to deploy Prometheus with the following steps.

Create a Prometheus namespace.

Add the prometheus-community chart repository.

If you get the error Error: failed to download "stable/prometheus" (hint: running helm repo update may help) when executing this command, run helm repo update prometheus-community, and then try running the Step 2 command again.

If you get the error Error: rendered manifests contain a resource that already exists, run helm uninstall your-release-name -n namespace , then try running the Step 3 command again.

Verify that all of the Pods in the prometheus namespace are in the READY state.

An example output is as follows.

Use kubectl to port forward the Prometheus console to your local machine.

Point a web browser to http://localhost:9090 to view the Prometheus console.

Choose a metric from the - insert metric at cursor menu, then choose Execute. Choose the Graph tab to show the metric over time. The following image shows container_memory_usage_bytes over time.

From the top navigation bar, choose Status, then Targets.

All of the Kubernetes endpoints that are connected to Prometheus using service discovery are displayed.

**Examples:**

Example 1 (unknown):
```unknown
helm version
```

Example 2 (unknown):
```unknown
kubectl create namespace prometheus
```

Example 3 (unknown):
```unknown
prometheus-community
```

Example 4 (unknown):
```unknown
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

---

## Scale pod deployments with Horizontal Pod Autoscaler

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/horizontal-pod-autoscaler.html

**Contents:**
- Scale pod deployments with Horizontal Pod Autoscaler
        - Note
- Run a Horizontal Pod Autoscaler test application
        - Note
        - Note
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Kubernetes Horizontal Pod Autoscaler automatically scales the number of Pods in a deployment, replication controller, or replica set based on that resource’s CPU utilization. This can help your applications scale out to meet increased demand or scale in when resources are not needed, thus freeing up your nodes for other applications. When you set a target CPU utilization percentage, the Horizontal Pod Autoscaler scales your application in or out to try to meet that target.

The Horizontal Pod Autoscaler is a standard API resource in Kubernetes that simply requires that a metrics source (such as the Kubernetes metrics server) is installed on your Amazon EKS cluster to work. You do not need to deploy or install the Horizontal Pod Autoscaler on your cluster to begin scaling your applications. For more information, see Horizontal Pod Autoscaler in the Kubernetes documentation.

Use this topic to prepare the Horizontal Pod Autoscaler for your Amazon EKS cluster and to verify that it is working with a sample application.

This topic is based on the Horizontal Pod autoscaler walkthrough in the Kubernetes documentation.

You have an existing Amazon EKS cluster. If you don’t, see Get started with Amazon EKS.

You have the Kubernetes Metrics Server installed. For more information, see View resource usage with the Kubernetes Metrics Server.

You are using a kubectl client that is configured to communicate with your Amazon EKS cluster.

In this section, you deploy a sample application to verify that the Horizontal Pod Autoscaler is working.

This example is based on the Horizontal Pod autoscaler walkthrough in the Kubernetes documentation.

Deploy a simple Apache web server application with the following command.

This Apache web server Pod is given a 500 millicpu CPU limit and it is serving on port 80.

Create a Horizontal Pod Autoscaler resource for the php-apache deployment.

This command creates an autoscaler that targets 50 percent CPU utilization for the deployment, with a minimum of one Pod and a maximum of ten Pods. When the average CPU load is lower than 50 percent, the autoscaler tries to reduce the number of Pods in the deployment, to a minimum of one. When the load is greater than 50 percent, the autoscaler tries to increase the number of Pods in the deployment, up to a maximum of ten. For more information

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
kubectl apply -f https://k8s.io/examples/application/php-apache.yaml
```

Example 2 (unknown):
```unknown
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

Example 3 (unknown):
```unknown
kubectl get hpa
```

Example 4 (unknown):
```unknown
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   0%/50%    1         10        1          51s
```

---

## Deploy a sample application on Linux

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/sample-deployment.html

**Contents:**
- Deploy a sample application on Linux
- Prerequisites
- Create a namespace
- Create a Kubernetes deployment
- Create a service
- Review resources created
        - Note
        - Tip
- Run a shell on a Pod
- Next Steps

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

In this topic, you deploy a sample application to your cluster on linux nodes.

An existing Kubernetes cluster with at least one node. If you don’t have an existing Amazon EKS cluster, you can deploy one using one of the guides in Get started with Amazon EKS.

Kubectl installed on your computer. For more information, see Set up kubectl and eksctl.

Kubectl configured to communicate with your cluster. For more information, see Connect kubectl to an EKS cluster by creating a kubeconfig file.

If you plan to deploy your sample workload to Fargate, then you must have an existing Fargate profile that includes the same namespace created in this tutorial, which is eks-sample-app, unless you change the name. If you created a cluster with one of the gudes in Get started with Amazon EKS, then you’ll have to create a new profile, or add the namespace to your existing profile, because the profile created in the getting started guides doesn’t specify the namespace used in this tutorial. Your VPC must also have at least one private subnet.

Though many variables are changeable in the following steps, we recommend only changing variable values where specified. Once you have a better understanding of Kubernetes Pods, deployments, and services, you can experiment with changing other values.

A namespace allows you to group resources in Kubernetes. For more information, see Namespaces in the Kubernetes documentation. If you plan to deploy your sample application to Simplify compute management with AWS Fargate, make sure that the value for namespace in your Define which Pods use AWS Fargate when launched is eks-sample-app.

Create a Kubernetes deployment. This sample deployment pulls a container image from a public repository and deploys three replicas (individual Pods) of it to your cluster. To learn more, see Deployments in the Kubernetes documentation.

Save the following contents to a file named eks-sample-deployment.yaml. The containers in the sample application don’t use network storage, but you might have applications that need to. For more information, see Use application data storage for your cluster.

The amd64 or arm64 values under the kubernetes.io/arch key mean that the application can be deployed to either hardware architecture (if you have both in your cluster). This is possible because this image is a multi-archi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
eks-sample-app
```

Example 2 (unknown):
```unknown
eks-sample-app
```

Example 3 (unknown):
```unknown
kubectl create namespace eks-sample-app
```

Example 4 (unknown):
```unknown
eks-sample-deployment.yaml
```

---

## AWS add-ons

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/workloads-add-ons-available-eks.html

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

## Secure workloads with Kubernetes certificates

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/cert-signing.html

**Contents:**
- Secure workloads with Kubernetes certificates
        - Note
- Example CSR generation with signerName

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Kubernetes Certificates API automates X.509 credential provisioning. The API features a command line interface for Kubernetes API clients to request and obtain X.509 certificates from a Certificate Authority (CA). You can use the CertificateSigningRequest (CSR) resource to request that a denoted signer sign the certificate. Your requests are either approved or denied before they’re signed. Kubernetes supports both built-in signers and custom signers with well-defined behaviors. This way, clients can predict what happens to their CSRs. To learn more about certificate signing, see signing requests.

One of the built-in signers is kubernetes.io/legacy-unknown. The v1beta1 API of CSR resource honored this legacy-unknown signer. However, the stable v1 API of CSR doesn’t allow the signerName to be set to kubernetes.io/legacy-unknown.

If you want to use Amazon EKS CA for generating certificates on your clusters, you must use a custom signer. To use the CSR v1 API version and generate a new certificate, you must migrate any existing manifests and API clients. Existing certificates that were created with the existing v1beta1 API are valid and function until the certificate expires. This includes the following:

Trust distribution: None. There’s no standard trust or distribution for this signer in a Kubernetes cluster.

Permitted subjects: Any

Permitted x509 extensions: Honors subjectAltName and key usage extensions and discards other extensions

Permitted key usages: Must not include usages beyond ["key encipherment", "digital signature", "server auth"]

Client certificate signing is not supported.

Expiration/certificate lifetime: 1 year (default and maximum)

CA bit allowed/disallowed: Not allowed

These steps shows how to generate a serving certificate for DNS name myserver.default.svc using signerName: beta.eks.amazonaws.com/app-serving. Use this as a guide for your own environment.

Run the openssl genrsa -out myserver.key 2048 command to generate an RSA private key.

Run the following command to generate a certificate request.

Generate a base64 value for the CSR request and store it in a variable for use in a later step.

Run the following command to create a file named mycsr.yaml. In the following example, beta.eks.amazonaws.com/app-serving is the signerName.

Approve the serving certificate.

Verify that

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CertificateSigningRequest
```

Example 2 (unknown):
```unknown
kubernetes.io/legacy-unknown
```

Example 3 (unknown):
```unknown
kubernetes.io/legacy-unknown
```

Example 4 (unknown):
```unknown
myserver.default.svc
```

---

## View resource usage with the Kubernetes Metrics Server

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html

**Contents:**
- View resource usage with the Kubernetes Metrics Server
        - Important
- Considerations
- Deploy as community add-on with Amazon EKS Add-ons
  - Deploy with AWS console
  - Additional resources
- Deploy with manifest

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Kubernetes Metrics Server is an aggregator of resource usage data in your cluster, and it isn’t deployed by default in Amazon EKS clusters. For more information, see Kubernetes Metrics Server on GitHub. The Metrics Server is commonly used by other Kubernetes add ons, such as the Scale pod deployments with Horizontal Pod Autoscaler or the Kubernetes Dashboard. For more information, see Resource metrics pipeline in the Kubernetes documentation. This topic explains how to deploy the Kubernetes Metrics Server on your Amazon EKS cluster.

The metrics are meant for point-in-time analysis and aren’t an accurate source for historical analysis. They can’t be used as a monitoring solution or for other non-auto scaling purposes. For information about monitoring tools, see Monitor your cluster performance and view logs.

If manually deploying Kubernetes Metrics Server onto Fargate nodes using the manifest, configure the metrics-server deployment to use a port other than its default of 10250. This port is reserved for Fargate. The Amazon EKS add-on version of Metrics Server is pre-configured to use port 10251.

Ensure security groups and network ACLs allow port 10250 between the metrics-server Pods and all other nodes and Pods. The Kubernetes Metrics Server still uses port 10250 to collect metrics from other endpoints in the cluster. If you deploy on Fargate nodes, allow both the configured alternate Metrics Server port and port 10250.

New: You can now deploy Metrics Server as a community add-on using the AWS console or Amazon EKS APIs.

Open your EKS cluster in the AWS console

From the "Add-ons" tab, select Get More Add-ons.

From the "Community add-ons" section, select Metrics Server and then Next

EKS determines the appropriate version of the add-on for your cluster. You can change the version using the Version dropdown menu.

Select Next and then Create to install the add-on.

Learn more about Community add-ons.

You install or update community add-ons in the same way as other Amazon EKS Add-ons.

Create an Amazon EKS add-on

Update an Amazon EKS add-on

Remove an Amazon EKS add-on from a cluster

New: You can now deploy Metrics Server as a community add-on using the AWS console or Amazon EKS APIs. These manifest install instructions will be archived.

Deploy the Metrics Server with the following command:

If you

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
metrics-server
```

Example 2 (unknown):
```unknown
metrics-server
```

Example 3 (unknown):
```unknown
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Example 4 (unknown):
```unknown
metrics-server
```

---

## Deploy applications with Helm on Amazon EKS

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/helm.html

**Contents:**
- Deploy applications with Helm on Amazon EKS
        - Important
        - Note

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

The Helm package manager for Kubernetes helps you install and manage applications on your Kubernetes cluster. For more information, see the Helm documentation. This topic helps you install and run the Helm binaries so that you can install and manage charts using the Helm CLI on your local system.

Before you can install Helm charts on your Amazon EKS cluster, you must configure kubectl to work for Amazon EKS. If you have not already done this, see Connect kubectl to an EKS cluster by creating a kubeconfig file before proceeding. If the following command succeeds for your cluster, you’re properly configured.

Run the appropriate command for your client operating system.

If you’re using macOS with Homebrew, install the binaries with the following command.

For more installation options, see Installing Helm in the Helm Docs.

If you get a message that openssl must first be installed, you can install it with the following command.

To pick up the new binary in your PATH, Close your current terminal window and open a new one.

See the version of Helm that you installed.

An example output is as follows.

Make sure the version installed is compatible with your cluster version. Check Supported Version Skew to learn more. For example, if you are running with 3.17.x, supported Kubernetes version should not out of the range of 1.29.x ~ 1.32.x.

At this point, you can run any Helm commands (such as helm install chart-name ) to install, modify, delete, or query Helm charts in your cluster. If you’re new to Helm and don’t have a specific chart to install, you can:

Experiment by installing an example chart. See Install an example chart in the Helm Quickstart guide.

Create an example chart and push it to Amazon ECR. For more information, see Pushing a Helm chart in the Amazon Elastic Container Registry User Guide.

Install an Amazon EKS chart from the eks-chartsGitHub repo or from ArtifactHub.

**Examples:**

Example 1 (unknown):
```unknown
kubectl get svc
```

Example 2 (unknown):
```unknown
brew install helm
```

Example 3 (unknown):
```unknown
sudo yum install openssl
```

Example 4 (unknown):
```unknown
helm version --template='{{ .Version }}{{ "\n" }}'
```

---

## Scale CoreDNS Pods for high DNS traffic

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/coredns-autoscaling.html

**Contents:**
- Scale CoreDNS Pods for high DNS traffic
- Prerequisites
  - Minimum cluster version
        - Note
  - Minimum EKS Add-on version

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

When you launch an Amazon EKS cluster with at least one node, a Deployment of two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster. The CoreDNS Pods provide name resolution for all Pods in the cluster. Applications use name resolution to connect to pods and services in the cluster as well as connecting to services outside the cluster. As the number of requests for name resolution (queries) from pods increase, the CoreDNS pods can get overwhelmed and slow down, and reject requests that the pods can’t handle.

To handle the increased load on the CoreDNS pods, consider an autoscaling system for CoreDNS. Amazon EKS can manage the autoscaling of the CoreDNS Deployment in the EKS Add-on version of CoreDNS. This CoreDNS autoscaler continuously monitors the cluster state, including the number of nodes and CPU cores. Based on that information, the controller will dynamically adapt the number of replicas of the CoreDNS deployment in an EKS cluster. This feature works for CoreDNS v1.9 and later. For more information about which versions are compatible with CoreDNS Autoscaling, see the following section.

The system automatically manages CoreDNS replicas using a dynamic formula based on both the number of nodes and CPU cores in the cluster, calculated as the maximum of (numberOfNodes divided by 16) and (numberOfCPUCores divided by 256). It evaluates demand over 10-minute peak periods, scaling up immediately when needed to handle increased DNS query load, while scaling down gradually by reducing replicas by 33% every 3 minutes to maintain system stability and avoid disruption.

We recommend using this feature in conjunction with other EKS Cluster Autoscaling best practices to improve overall application availability and cluster scalability.

For Amazon EKS to scale your CoreDNS deployment, there are three prerequisites:

You must be using the EKS Add-on version of CoreDNS.

Your cluster must be running at least the minimum cluster versions and platform versions.

Your cluster must be running at least the minimum version of the EKS Add-on of CoreDNS.

Autoscaling of CoreDNS is done by a new component in the cluster control plane, managed by Amazon EKS. Because of this, you must upgrade your cluster to an EKS release that supports the minimum platform version t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws eks describe-cluster --name my-cluster --query cluster.version --output text
```

Example 2 (unknown):
```unknown
v1.11.1-eksbuild.9
```

Example 3 (unknown):
```unknown
v1.10.1-eksbuild.11
```

Example 4 (unknown):
```unknown
aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
```

---

## Deploy a sample stateful workload to EKS Auto Mode

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/sample-storage-workload.html

**Contents:**
- Deploy a sample stateful workload to EKS Auto Mode
- Prerequisites
- Step 1: Configure your environment
- Step 2: Create the storage class
- Step 3: Create the persistent volume claim
- Step 4: Deploy the Application
- Step 5: Verify the Setup
- Step 6: Cleanup
- What’s Happening Behind the Scenes
- Snapshot Controller

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

This tutorial will guide you through deploying a sample stateful application to your EKS Auto Mode cluster. The application writes timestamps to a persistent volume, demonstrating EKS Auto Mode’s automatic EBS volume provisioning and persistence capabilities.

An EKS Auto Mode cluster

The AWS CLI configured with appropriate permissions

kubectl installed and configured

For more information, see Set up to use Amazon EKS.

Set your environment variables:

Update your kubeconfig:

The StorageClass defines how EKS Auto Mode will provision EBS volumes.

EKS Auto Mode does not create a StorageClass for you. You must create a StorageClass referencing ebs.csi.eks.amazonaws.com to use the storage capability of EKS Auto Mode.

Create a file named storage-class.yaml:

Apply the StorageClass:

provisioner: ebs.csi.eks.amazonaws.com - Uses EKS Auto Mode

volumeBindingMode: WaitForFirstConsumer - Delays volume creation until a pod needs it

type: gp3 - Specifies the EBS volume type

encrypted: "true" - EBS will use the default aws/ebs key to encrypt volumes created with this class. This is optional, but recommended.

storageclass.kubernetes.io/is-default-class: "true" - Kubernetes will use this storage class by default, unless you specify a different volume class on a persistent volume claim. Use caution when setting this value if you are migrating from another storage controller. (optional)

The PVC requests storage from the StorageClass.

Create a file named pvc.yaml:

accessModes: ReadWriteOnce - Volume can be mounted by one node at a time

storage: 8Gi - Requests an 8 GiB volume

storageClassName: auto-ebs-sc - References the StorageClass we created

The Deployment runs a container that writes timestamps to the persistent volume.

Create a file named deployment.yaml:

Apply the Deployment:

Simple bash container that writes timestamps to a file

Mounts the PVC at /data

Uses node selector for EKS managed nodes

Check that the pod is running:

Verify the PVC is bound:

Check the EBS volume:

Verify data is being written:

Run the following command to remove all resources created in this tutorial:

The PVC requests storage from the StorageClass

When the Pod is scheduled:

EKS Auto Mode provisions an EBS volume

Creates a PersistentVolume

Attaches the volume to the node

The Pod mounts the volume and begins writing tim

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export CLUSTER_NAME=my-auto-cluster
export AWS_REGION="us-west-2"
```

Example 2 (unknown):
```unknown
aws eks update-kubeconfig --name "${CLUSTER_NAME}"
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

## Deploy Amazon EKS on-premises with AWS Outposts

**URL:** https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts.html

**Contents:**
- Deploy Amazon EKS on-premises with AWS Outposts
- When to use each deployment option
- Comparing the deployment options
        - Topics

Help improve this page

To contribute to this user guide, choose the Edit this page on GitHub link that is located in the right pane of every page.

You can use Amazon EKS to run on-premises Kubernetes applications on AWS Outposts. You can deploy Amazon EKS on Outposts in the following ways:

Extended clusters – Run the Kubernetes control plane in an AWS Region and nodes on your Outpost.

Local clusters – Run the Kubernetes control plane and nodes on your Outpost.

For both deployment options, the Kubernetes control plane is fully managed by AWS. You can use the same Amazon EKS APIs, tools, and console that you use in the cloud to create and run Amazon EKS on Outposts.

The following diagram shows these deployment options.

Both local and extended clusters are general-purpose deployment options and can be used for a range of applications.

With local clusters, you can run the entire Amazon EKS cluster locally on Outposts. This option can mitigate the risk of application downtime that might result from temporary network disconnects to the cloud. These network disconnects can be caused by fiber cuts or weather events. Because the entire Amazon EKS cluster runs locally on Outposts, applications remain available. You can perform cluster operations during network disconnects to the cloud. For more information, see Prepare local Amazon EKS clusters on AWS Outposts for network disconnects. If you’re concerned about the quality of the network connection from your Outposts to the parent AWS Region and require high availability through network disconnects, use the local cluster deployment option.

With extended clusters, you can conserve capacity on your Outpost because the Kubernetes control plane runs in the parent AWS Region. This option is suitable if you can invest in reliable, redundant network connectivity from your Outpost to the AWS Region. The quality of the network connection is critical for this option. The way that Kubernetes handles network disconnects between the Kubernetes control plane and nodes might lead to application downtime. For more information on the behavior of Kubernetes, see Scheduling, Preemption, and Eviction in the Kubernetes documentation.

The following table compares the differences between the two options.

Kubernetes control plane location

Kubernetes control plane account

Regional availability

see Service endpoints

US East (Ohio), US East (N. Virginia), US West (N. California), US West (Oregon), Asia Pacific (Seoul), Asia Paci

*[Content truncated]*

---
