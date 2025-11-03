# Aws-Sagemaker - Studio

*This file summarizes Amazon SageMaker Studio documentation and includes links to canonical AWS pages. Content adapted from Amazon Web Services SageMaker documentation. For complete documentation, see the official [Amazon SageMaker Studio documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html).*

---

## Amazon SageMaker notebook instances

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html

**Contents:**
- Amazon SageMaker notebook instances
- Maintenance
- Machine Learning with the SageMaker Python SDK
        - Topics

An Amazon SageMaker notebook instance is a machine learning (ML) compute instance running the Jupyter Notebook application. One of the best ways for machine learning (ML) practitioners to use Amazon SageMaker AI is to train and deploy ML models using SageMaker notebook instances. The SageMaker notebook instances help create the environment by initiating Jupyter servers on Amazon Elastic Compute Cloud (Amazon EC2) and providing preconfigured kernels with the following packages: the Amazon SageMaker Python SDK, AWS SDK for Python (Boto3), AWS Command Line Interface (AWS CLI), Conda, Pandas, deep learning framework libraries, and other libraries for data science and machine learning.

Use Jupyter notebooks in your notebook instance to:

prepare and process data

write code to train models

deploy models to SageMaker hosting

test or validate your models

For information about pricing with Amazon SageMaker notebook instance, see Amazon SageMaker Pricing.

SageMaker AI updates the underlying software for Amazon SageMaker Notebook Instances at least once every 90 days. Some maintenance updates, such as operating system upgrades, may require your application to be taken offline for a short period of time. It is not possible to perform any operations during this period while the underlying software is being updated. We recommend that you restart your notebooks at least once every 30 days to automatically consume patches.

If the notebook instance isn't updated and is running unsecure software, SageMaker AI might periodically update the instance as part of regular maintenance. During these updates, data outside of the folder /home/ec2-user/SageMaker is not persisted.

For more information, contact AWS Support.

To train, validate, deploy, and evaluate an ML model in a SageMaker notebook instance, use the SageMaker Python SDK. The SageMaker Python SDK abstracts AWS SDK for Python (Boto3) and SageMaker API operations. It enables you to integrate with and orchestrate other AWS services, such as Amazon Simple Storage Service (Amazon S3) for saving data and model artifacts, Amazon Elastic Container Registry (ECR) for importing and servicing the ML models, Amazon Elastic Compute Cloud (Amazon EC2) for training and inference.

You can also take advantage of SageMaker AI features that help you deal with every stage of a complete ML cycle: data labeling, data preprocessing, model training, model deployment, evaluation on prediction performance, and monitoring the quality of

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
/home/ec2-user/SageMaker
```

---

## Data preparation with SQL in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-sql-extension.html

**Contents:**
- Data preparation with SQL in Studio
        - Important
        - Important
        - Note
        - Topics

Amazon SageMaker Studio provides a built-in SQL extension. This extension allows data scientists to perform tasks such as sampling, exploratory analysis, and feature engineering directly within their JupyterLab notebooks. It leverages AWS Glue connections to maintain a centralized data source catalog. The catalog stores metadata about various data sources. Through this SQL environment, data scientists can browse data catalogs, explore their data, author complex SQL queries, and further process the results in Python.

This section walks through configuring the SQL extension in Studio. It describes the capabilities enabled by this SQL integration and provides instructions for running SQL queries in JupyterLab notebooks.

To enable SQL data analysis, administrators must first configure AWS Glue connections to the relevant data sources. These connections allow data scientists to seamlessly access authorized datasets from within JupyterLab.

In addition to the administrator-configured AWS Glue connections, the SQL extension allows individual data scientists to create their own data source connections. These user-created connections can be managed independently and scoped to the user's profile through tag-based access control policies. This dual-level connection model - with both administrator-configured and user-created connections - provides data scientists with broader access to the data they need for their analysis and modeling tasks. Users can set up the necessary connections to their own data sources within the JupyterLab environment user interface (UI), without relying solely on the centralized connections established by the administrator.

The user-defined connections creation capability is available as a set of standalone libraries in PyPI. To use this functionality, you need to install the following libraries in your JupyterLab environment:

amazon-sagemaker-sql-editor

amazon-sagemaker-sql-execution

amazon-sagemaker-sql-magic

You can install these libraries by running the following commands in your JupyterLab terminal:

After installing the libraries, you will need to restart the JupyterLab server for the changes to take effect.

With access set up, JupyterLab users can:

View and browse pre-configured data sources.

Search, filter, and inspect database information elements such as tables, schemas, and columns.

Auto-generate the connection parameters to a data source.

Create complex SQL queries using the syntax-highlighting, auto-completion, and S

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
pip install amazon-sagemaker-sql-editor>=0.1.13
pip install amazon-sagemaker-sql-execution>=0.1.6
pip install amazon-sagemaker-sql-magic>=0.1.3
```

Example 2 (unknown):
```unknown
restart-jupyter-server
```

Example 3 (unknown):
```unknown
%load_ext
              amazon_sagemaker_sql_magic
```

---

## Provide Feedback on Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-provide-feedback.html

**Contents:**
- Provide Feedback on Amazon SageMaker Studio Classic
        - Important
        - To provide feedback

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker AI takes your feedback seriously. We encourage you to provide feedback.

At the right of SageMaker Studio Classic, find the Feedback icon ( ).

Choose a smiley emoji to let us know how satisfied you are with SageMaker Studio Classic and add any feedback you'd care to share with us.

Decide whether to share your identity with us, then choose Submit.

---

## Example HyperPod task governance AWS CLI commands

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-cli.html

**Contents:**
- Example HyperPod task governance AWS CLI commands
        - Topics
- Get cluster accelerator device quota information
- Submit a job to SageMaker AI-managed queue and namespace
- List jobs
- Get job detailed information
- Suspend and unsuspend jobs
- Debugging jobs

You can use HyperPod with EKS through Kubectl or through HyperPod custom CLI. You can use these commands through Studio or AWS CLI. The following provides SageMaker HyperPod task governance examples, on how to view cluster details using the HyperPod AWS CLI commands. For more information, including how to install, see the HyperPod CLI Github repository.

Get cluster accelerator device quota information

Submit a job to SageMaker AI-managed queue and namespace

Get job detailed information

Suspend and unsuspend jobs

The following example command gets the information on the cluster accelerator device quota.

The namespace in this example, hyperpod-ns-test-team, is created in Kubernetes based on the team name provided, test-team, when the compute allocation is created. For more information, see Edit policies.

The following example command submits a job to your HyperPod cluster. If you have access to only one team, the HyperPod AWS CLI will automatically assign the queue for you in this case. Otherwise if multiple queues are discovered, we will display all viable options for you to select.

The priority classes are defined in the Cluster policy, which defines how tasks are prioritized and idle compute is allocated. When a data scientist submits a job, they use one of the priority class names with the format priority-class-name-priority. In this example, training-priority refers to the priority class named “training”. For more information on policy concepts, see Policies.

If a priority class is not specified, the job is treated as a low priority job, with a task ranking value of 0.

If a priority class is specified, but does not correspond to one of the priority classes defined in the Cluster policy, the submission fails and an error message provides the defined set of priority classes.

You can also submit the job using a YAML configuration file using the following command:

The following is an example YAML configuration file that is equivalent to submitting a job as discussed above.

Alternatively, you can submit a job using kubectl to ensure the task appears in the Dashboard tab. The following is an example kubectl command.

When submitting the job, include your queue name and priority class labels. For example, with the queue name hyperpod-ns-team-name-localqueue and priority class priority-class-name-priority, you must include the following labels:

kueue.x-k8s.io/queue-name: hyperpod-ns-team-name-localqueue

kueue.x-k8s.io/priority-class: priority-class

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
hyperpod get-clusters -n hyperpod-ns-test-team
```

Example 2 (unknown):
```unknown
hyperpod-ns-test-team
```

Example 3 (unknown):
```unknown
[
    {
        "Cluster": "hyperpod-eks-test-cluster-id",
        "InstanceType": "ml.g5.xlarge",
        "TotalNodes": 2,
        "AcceleratorDevicesAvailable": 1,
        "NodeHealthStatus=Schedulable": 2,
        "DeepHealthCheckStatus=Passed": "N/A",
        "Namespaces": {
            "hyperpod-ns-test-team": {
                "TotalAcceleratorDevices": 1,
                "AvailableAcceleratorDevices": 1
            }
        }
    }
]
```

Example 4 (unknown):
```unknown
hyperpod start-job --job-name hyperpod-cli-test --job-kind kubeflow/PyTorchJob --image docker.io/kubeflowkatib/pytorch-mnist-cpu:v1beta1-bc09cfd --entry-script /opt/pytorch-mnist/mnist.py --pull-policy IfNotPresent --instance-type ml.g5.xlarge --node-count 1 --tasks-per-node 1 --results-dir ./result --priority training-priority
```

---

## Applications supported in Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-apps.html

**Contents:**
- Applications supported in Amazon SageMaker Studio
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

Amazon SageMaker Studio supports the following applications:

Code Editor, based on Code-OSS, Visual Studio Code - Open Source– Code Editor offers a lightweight and powerful integrated development environment (IDE) with familiar shortcuts, terminal, and advanced debugging capabilities and refactoring tools. It is a fully managed, browser-based application in Studio. For more information, see Code Editor in Amazon SageMaker Studio.

Amazon SageMaker Studio Classic– Amazon SageMaker Studio Classic is a web-based IDE for machine learning. With Studio Classic, you can build, train, debug, deploy, and monitor your machine learning models. For more information, see Amazon SageMaker Studio Classic.

JupyterLab–JupyterLab offers a set of capabilities that augment the fully managed notebook offering. It includes kernels that start in seconds, a pre-configured runtime with popular data science, machine learning frameworks, and high performance block storage. For more information, see SageMaker JupyterLab.

Amazon SageMaker Canvas– With SageMaker Canvas, you can use machine learning to generate predictions without writing code. With Canvas, you can chat with popular large language models (LLMs), access ready-to-use models, or build a custom model that's trained on your data. For more information, see Amazon SageMaker Canvas.

RStudio– RStudio is an integrated development environment for R. It includes a console and syntax-highlighting editor that supports running code directly. It also includes tools for plotting, history, debugging, and workspace management. For more information, see RStudio on Amazon SageMaker AI.

---

## Use the Amazon SageMaker Studio Classic Launcher

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launcher.html#studio-launcher-other

**Contents:**
- Use the Amazon SageMaker Studio Classic Launcher
        - Important
        - Topics
- Notebooks and compute resources
        - Note
        - Note
- Utilities and files
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can use the Amazon SageMaker Studio Classic Launcher to create notebooks and text files, and to launch terminals and interactive Python shells.

You can open Studio Classic Launcher in any of the following ways:

Choose Amazon SageMaker Studio Classic at the top left of the Studio Classic interface.

Use the keyboard shortcut Ctrl + Shift + L.

From the Studio Classic menu, choose File and then choose New Launcher.

If the SageMaker AI file browser is open, choose the plus (+) sign in the Studio Classic file browser menu.

In the Quick actions section of the Home tab, choose Open Launcher. The Launcher opens in a new tab. The Quick actions section is visible by default but can be toggled off. Choose Customize Layout to turn this section back on.

The Launcher consists of the following two sections:

Notebooks and compute resources

In this section, you can create a notebook, open an image terminal, or open a Python console.

To create or launch one of those items:

Choose Change environment to select a SageMaker image, a kernel, an instance type, and, optionally, add a lifecycle configuration script that runs on image start-up. For more information on lifecycle configuration scripts, see Use Lifecycle Configurations to Customize Amazon SageMaker Studio Classic. For more information about kernel updates, see Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook.

When you choose an item from this section, you might incur additional usage charges. For more information, see Usage Metering for Amazon SageMaker Studio Classic Notebooks.

The following items are available:

Launches the notebook in a kernel session on the chosen SageMaker image.

Creates the notebook in the folder that you have currently selected in the file browser. To view the file browser, in the left sidebar of Studio Classic, choose the File Browser icon.

Launches the shell in a kernel session on the chosen SageMaker image.

**Examples:**

Example 1 (unknown):
```unknown
Ctrl + Shift + L
```

Example 2 (unknown):
```unknown
ml.t3.medium
```

Example 3 (unknown):
```unknown
ml.g4dn.xlarge
```

Example 4 (unknown):
```unknown
Experiment.create
```

---

## Attach Suggested Git Repos to Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-git-attach.html

**Contents:**
- Attach Suggested Git Repos to Amazon SageMaker Studio Classic
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic offers a Git extension for you to enter the URL of a Git repository (repo), clone it into your environment, push changes, and view commit history. In addition to this Git extension, you can also attach suggested Git repository URLs at the Amazon SageMaker AI domain or user profile level. Then, you can select the repo URL from the list of suggestions and clone that into your environment using the Git extension in Studio Classic.

The following topics show how to attach Git repo URLs to a domain or user profile from the AWS CLI and SageMaker AI console. You'll also learn how to detach these repository URLs.

Attach a Git Repository from the AWS CLI for Amazon SageMaker Studio Classic

Attach a Git Repository from the SageMaker AI Console for Amazon SageMaker Studio Classic

Detach Git Repos from Amazon SageMaker Studio Classic

---

## Create and Associate a Lifecycle Configuration with Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lcc-create.html

**Contents:**
- Create and Associate a Lifecycle Configuration with Amazon SageMaker Studio Classic
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker AI provides interactive applications that enable Studio Classic's visual interface, code authoring, and run experience. This series shows how to create a lifecycle configuration and associate it with a SageMaker AI domain.

Application types can be either JupyterServer or KernelGateway.

JupyterServer applications: This application type enables access to the visual interface for Studio Classic. Every user and shared space in Studio Classic gets its own JupyterServer application.

KernelGateway applications: This application type enables access to the code run environment and kernels for your Studio Classic notebooks and terminals. For more information, see Jupyter Kernel Gateway.

For more information about Studio Classic's architecture and Studio Classic applications, see Use Amazon SageMaker Studio Classic Notebooks.

Create a Lifecycle Configuration from the AWS CLI for Amazon SageMaker Studio Classic

Create a Lifecycle Configuration from the SageMaker AI Console for Amazon SageMaker Studio Classic

**Examples:**

Example 1 (unknown):
```unknown
JupyterServer
```

Example 2 (unknown):
```unknown
KernelGateway
```

Example 3 (unknown):
```unknown
JupyterServer
```

Example 4 (unknown):
```unknown
KernelGateway
```

---

## HyperPod tabs in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-studio-tabs.html

**Contents:**
- HyperPod tabs in Studio
- Tasks
- Metrics
- Settings
- Details

In Amazon SageMaker Studio you can navigate to one of your clusters in HyperPod clusters (under Compute) and view your list of clusters. The displayed clusters contain information like tasks, hardware metrics, settings, and metadata details. This visibility can help your team identify the right candidate for your pre-training or finetuning workloads. The following sections provide information on each type of information.

Amazon SageMaker HyperPod provides a view of your cluster tasks. Tasks are operations or jobs that are sent to the cluster. These can be machine learning operations, like training, running experiments, or inference. The following section provides information on your HyperPod cluster tasks.

In Amazon SageMaker Studio, you can navigate to one of your clusters in HyperPod clusters (under Compute) and view the Tasks information on your cluster. If you are having any issues with viewing tasks, see Troubleshooting.

The task table includes:

For Slurm clusters, the tasks currently in the Slurm job scheduler queue are shown in the table. The information shown for each task includes the task name, status, job ID, partition, run time, nodes, created by, and actions.

For a list and details about past jobs, use the sacct command in JupyterLab or a Code Editor terminal. The sacct command is used to view historical information about jobs that have finished or are complete in the system. It provides accounting information, including job resources usage like memory and exit status.

By default, all Studio users can view, manage, and interact with all available Slurm tasks. To restrict the viewable tasks to Studio users, see Restrict task view in Studio for Slurm clusters.

For Amazon EKS clusters, kubeflow (PyTorch, MPI, TensorFlow) tasks are shown in the table. PyTorch tasks are shown by default. You can sort for PyTorch, MPI, and TensorFlow under Task type. The information that is shown for each task includes the task name, status, namespace, priority class, and creation time.

By default, all users can view jobs across all namespaces. To restrict the viewable Kubernetes namespaces available to Studio users, see Restrict task view in Studio for EKS clusters. If a user cannot view the tasks and is asked to provide a namespace, they need to get that information from the administrator.

Amazon SageMaker HyperPod provides a view of your Slurm or Amazon EKS cluster utilization metrics. The following provides information on your HyperPod cluster metrics.


*[Content truncated]*

---

## Get Notebook Differences in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-diff.html

**Contents:**
- Get Notebook Differences in Amazon SageMaker Studio Classic
        - Important
        - Important
        - Topics
- Get the Difference Between the Last Checkpoint
- Get the Difference Between the Last Commit

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can display the difference between the current notebook and the last checkpoint or the last Git commit using the Amazon SageMaker AI UI.

The following screenshot shows the menu from a Studio Classic notebook.

Get the Difference Between the Last Checkpoint

Get the Difference Between the Last Commit

When you create a notebook, a hidden checkpoint file that matches the notebook is created. You can view changes between the notebook and the checkpoint file or revert the notebook to match the checkpoint file.

By default, a notebook is auto-saved every 120 seconds and also when you close the notebook. However, the checkpoint file isn't updated to match the notebook. To save the notebook and update the checkpoint file to match, you must choose the Save notebook and create checkpoint icon ( ) on the left of the notebook menu or use the Ctrl + S keyboard shortcut.

To view the changes between the notebook and the checkpoint file, choose the Checkpoint diff icon ( ) in the center of the notebook menu.

To revert the notebook to the checkpoint file, from the main Studio Classic menu, choose File then Revert Notebook to Checkpoint.

If a notebook is opened from a Git repository, you can view the dif

*[Content truncated]*

---

## Idle shutdown

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-idle-shutdown.html

**Contents:**
- Idle shutdown
        - Note
- Definition of idle

Amazon SageMaker AI supports shutting down idle resources to manage costs and prevent cost overruns due to cost accrued by idle, billable resources. It accomplishes this by detecting an app’s idle state and performing an app shutdown when idle criteria are met.

SageMaker AI supports idle shutdown for the following applications. Idle shutdown must be set for each application type independently.

Code Editor, based on Code-OSS, Visual Studio Code - Open Source

Idle shutdown can be set at either the domain or user profile level. When idle shutdown is set at the domain level, the idle shutdown settings apply to all applications created in the domain. When set at the user profile level, the idle shutdown settings apply only to the specific users that they are set for. User profile settings override domain settings.

Idle shutdown requires the usage of the SageMaker-distribution (SMD) image with v2.0 or newer. Domains using an older SMD version can’t use the feature. These users must use an LCC to manage auto-shutdown instead.

Idle shutdown settings only apply when the application becomes idle with no jobs running. SageMaker AI doesn’t start the idle shutdown timing until the instance becomes idle. The definition on idle differs based on whether the application type is JupyterLab or Code Editor.

For JupyterLab applications, the instance is considered idle when the following conditions are met:

No active Jupyter kernel sessions

No active Jupyter terminal sessions

For Code Editor applications, the instance is considered idle when the following conditions are met:

No text file or notebook changes

No files being viewed

No interaction with the terminal

**Examples:**

Example 1 (unknown):
```unknown
SageMaker-distribution
```

---

## Guide to getting set up with Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/gs.html

**Contents:**
- Guide to getting set up with Amazon SageMaker AI
        - Note
        - Topics

To use the features in Amazon SageMaker AI, you must have access to Amazon SageMaker AI. To set up Amazon SageMaker AI and its features, use one of the following options.

Use quick setup: Fastest setup for individual users with default settings.

Use custom setup: Advanced setup for enterprise Machine Learning (ML) administrators. Ideal option for ML administrators setting up SageMaker AI for many users or an organization.

You do not need to set up SageMaker AI if:

An email is sent to you inviting you to create a password to use the IAM Identity Center authentication. The email also contains the AWS access portal URL you use to sign in. For more information about signing in to the AWS access portal, see Sign in to the AWS access portal.

You intend to use the Amazon SageMaker Studio Lab ML environment. Studio Lab does not require you to have an AWS account. For information about Studio Lab, see Amazon SageMaker Studio Lab.

If you are using the AWS CLI, SageMaker APIs, or SageMaker SDKs

You do not need to set up SageMaker AI if any of the prior situations apply. You can skip the rest of this Guide to getting set up with Amazon SageMaker AI chapter and navigate to the following:

Automated ML, no-code, or low-code

Machine learning environments offered by Amazon SageMaker AI

Complete Amazon SageMaker AI prerequisites

Use quick setup for Amazon SageMaker AI

Use custom setup for Amazon SageMaker AI

Amazon SageMaker AI domain overview

Supported Regions and Quotas

---

## Granting SageMaker Studio Permissions Required to Use Projects

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-studio-updates.html

**Contents:**
- Granting SageMaker Studio Permissions Required to Use Projects
        - Important
- Grant new domain roles access to projects
        - To grant new domain roles access to projects
        - Important
        - To confirm that your SageMaker AI Domain has active project template permissions:
        - To view a list of your roles:
        - Important

The Amazon SageMaker Studio (or Studio Classic) administrator and Studio (or Studio Classic) users that you add to your domain can view project templates provided by SageMaker AI and create projects with those templates. By default, the administrator can view the SageMaker AI templates in the Service Catalog console. The administrator can see what another user creates if the user has permission to use SageMaker Projects. The administrator can also view the AWS CloudFormation template that the SageMaker AI project templates define in the Service Catalog console. For information about using the Service Catalog console, see What Is Service Catalog in the Service Catalog User Guide.

Studio (and Studio Classic) users of the domain who are configured to use the same execution role as the domain by default have permission to create projects using SageMaker AI project templates.

Do not manually create your roles. Always create roles through Studio Settings using the steps described in the following procedure.

For users who use any role other than the domain's execution role to view and use SageMaker AI-provided project templates, you need to grant Projects permissions to the individual user profiles by turning on Enable Amazon SageMaker AI project templates and Amazon SageMaker JumpStart for Studio users when you add them to your domain. For more information about this step, see Add user profiles.

Since SageMaker Projects is backed by Service Catalog, you must add each role that requires access to SageMaker Projects to the Amazon SageMaker AI Solutions and ML Ops products Portfolio in the service catalog. You can do this in the Groups, roles, and users tab, as shown in the following image. If each user profile in Studio Classic has a different role, you should add each of those roles to the service catalog. You can also do this while creating a user profile in Studio Classic.

When you change your domain's execution role or add user profiles with different roles, you must grant these new roles access to the Service Catalog portfolio to use SageMaker Projects. Follow these steps to ensure all roles have the necessary permissions:

Open the Service Catalog console.

In the left navigation menu, choose Portfolios.

Select the Imported section.

Select Amazon SageMaker Solutions and ML Ops products.

Choose the Access tab.

In the Grant access dialog, select Roles.

Grant access for all roles that are used by the domain's user profiles, including:

The domain's ex

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerServiceCatalogProductsLaunchRole
```

Example 2 (unknown):
```unknown
AmazonSageMakerServiceCatalogProductsUseRole
```

Example 3 (unknown):
```unknown
AmazonSageMakerServiceCatalogProductsApiGatewayRole
```

Example 4 (unknown):
```unknown
AmazonSageMakerServiceCatalogProductsCloudformationRole
```

---

## Amazon SageMaker Studio pricing

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-cost.html

**Contents:**
- Amazon SageMaker Studio pricing
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

There is no additional charge for using the Amazon SageMaker Studio UI.

The following do incur costs:

Amazon Elastic Block Store or Amazon Elastic File System volumes that are mounted with your applications.

Any jobs and resources that users launch from Studio applications.

Launching a JupyterLab application, even if no resources or jobs launched in the application.

For information about how Amazon SageMaker Studio Classic is billed, see Amazon SageMaker Studio Classic Pricing.

For more information about billing along with pricing examples, see Amazon SageMaker Pricing.

---

## Amazon SageMaker Studio spaces

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-spaces.html

**Contents:**
- Amazon SageMaker Studio spaces
        - Important
        - Important
        - Topics

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

Spaces are used to manage the storage and resource needs of some Amazon SageMaker Studio applications. Each space is composed of multiple resources and can be either private or shared. Each space has a 1:1 relationship with an instance of an application. Every supported application that is created gets its own space. The following applications in Studio run on spaces:

Code Editor in Amazon SageMaker Studio

Amazon SageMaker Studio Classic

A space is composed of the following resources:

For Studio Classic, the space is connected to the shared Amazon Elastic File System (Amazon EFS) volume for the domain.

For other applications, a distinct Amazon Elastic Block Store (Amazon EBS) volume is attached to the space. All applications are given their own Amazon EBS volume. Applications do not have access to the Amazon EBS volume of other applications. For more information about Amazon EBS volumes, see Amazon Elastic Block Store (Amazon EBS).

The application type of the space.

The image that the application is based on.

Spaces can be either private or shared:

Private: Private spaces are scoped to a single user in a domain. Private spaces cannot be shared with other users. All applications that support spaces also support private spaces.

Shared: Shared spaces are accessible by all users in the domain. For more information about shared spaces, see Collaboration with shared spaces.

Spaces can be created in domains that use either AWS IAM Identity Center 

*[Content truncated]*

---

## JupyterLab Versioning in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jl.html#studio-jl-view

**Contents:**
- JupyterLab Versioning in Amazon SageMaker Studio Classic
        - Important
        - Important
- JupyterLab 3
  - Important changes to JupyterLab 3
- Restricting default JupyterLab version using an IAM policy condition key
- Setting a default JupyterLab version
  - From the console
  - From the AWS CLI
    - Create or update domain

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The Amazon SageMaker Studio Classic interface is based on JupyterLab, which is a web-based interactive development environment for notebooks, code, and data. Studio Classic only supports using JupyterLab 3.

If you created your domain and user profile using the AWS Management Console before 08/31/2022 or using the AWS Command Line Interface before 02/22/23, then your Studio Classic instance defaulted to JupyterLab 1. After 07/01/2024, you cannot create any Studio Classic applications that run JupyterLab 1.

JupyterLab 3 includes the following features that are not available in previous versions. For more information about these features, see JupyterLab 3.0 is released!.

Visual debugger when using the Base Python 2.0 and Data Science 2.0 kernels.

Table of Contents (TOC)

Multi-language support

Single interface mode

Consider the following when using JupyterLab 3:

When setting the JupyterLab version using the AWS CLI, select the corresponding image for your Region and JupyterLab version from the image list in From the AWS CLI.

In JupyterLab 3, you must activate the studio conda environment before installing extensions. For more information, see Installing JupyterLab and Jupyter Server extensi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 3 (unknown):
```unknown
111122223333
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockUsersFromCreatingJupyterLab3Apps",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateUserProfile",
                "sagemaker:UpdateUserProfile"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

---

## Migrate the UI from Studio Classic to Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-ui.html#studio-updated-migrate-revert

**Contents:**
- Migrate the UI from Studio Classic to Studio
- Prerequisites
- Step 1: Update application creation permissions
        - Note
        - Note
- Step 2: Update VPC configuration
- Step 3: Upgrade to the Studio UI
    - Test Studio functionality
    - Clean up test domain resources
        - Note

The first phase for migrating an existing domain involves migrating the UI from Amazon SageMaker Studio Classic to Amazon SageMaker Studio. This phase does not include the migration of data. Users can continue working with their data the same way as they were before migration. For information about migrating data, see (Optional) Migrate data from Studio Classic to Studio.

Phase 1 consists of the following steps:

Update application creation permissions for new applications available in Studio.

Update the VPC configuration for the domain.

Upgrade the domain to use the Studio UI.

Before running these steps, complete the prerequisites in Complete prerequisites to migrate the Studio experience.

Before migrating the domain, update the domain's execution role to grant users permissions to create applications.

Create an AWS Identity and Access Management policy with one of the following contents by following the steps in Creating IAM policies:

Use the following policy to grant permissions for all application types and spaces.

If the domain uses the SageMakerFullAccess policy, you do not need to perform this action. SageMakerFullAccess grants permissions to create all applications.

Because Studio shows an expanded set of applications, users may have access to applications that weren't displayed before. Administrators can limit access to these default applications by creating an AWS Identity and Access Management (IAM) policy that grants denies permissions for some applications to specific users.

Application type can be either jupyterlab or codeeditor.

Attach the policy to the execution role of the domain. For instructions, follow the steps in Adding IAM identity permissions (console).

If you use your domain in VPC-Only mode, ensure your VPC configuration meets the requirements for using Studio in VPC-Only mode. For more information, see Connect Amazon SageMaker Studio in a VPC to External Resources.

Before you migrate your existing domain from Studio Classic to Studio, we recommend creating a test domain using Studio with the same configurations as your existing domain.

Use this test domain to interact with Studio, test out networking configurations, and launch applications, before migrating the existing domain.

Get the domain ID of your existing domain.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

From the left navigation pane, expand Admin configurations and choose Domains.

Choose the existing domain.

On t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
SageMakerFullAccess
```

Example 2 (unknown):
```unknown
SageMakerFullAccess
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "SMStudioUserProfileAppPermissionsCreateAndDelete",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateApp",
                "sagemaker:DeleteApp"
            ],
            "Resource": "arn:aws:sagemaker:us-east-1:111122223333:app/*",
            "Condition": {
                "Null": {
                    "sagemaker:OwnerUserProfileArn": "true"
                }
            }
        },
        {
            "Sid": "SMStudioCreatePresignedDomainUrlForUserProfile",
            "E
...
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "SMStudioUserProfileAppPermissionsCreateAndDelete",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateApp",
                "sagemaker:DeleteApp"
            ],
            "Resource": "arn:aws:sagemaker:us-east-1:111122223333:app/*",
            "Condition": {
                "Null": {
                    "sagemaker:OwnerUserProfileArn": "true"
                }
            }
        },
        {
            "Sid": "SMStudioCreatePresignedDomainUrlForUserProfile",
            "E
...
```

---

## Complete prerequisites to migrate the Studio experience

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-prereq.html

**Contents:**
- Complete prerequisites to migrate the Studio experience
        - Note

Migration of the default experience from Studio Classic to Studio is managed by the administrator of the existing domain. If you do not have permissions to set Studio as the default experience for the existing domain, contact your administrator. To migrate your default experience, you must have administrator permissions or at least have permissions to update the existing domain, AWS Identity and Access Management (IAM), and Amazon Simple Storage Service (Amazon S3). Complete the following prerequisites before migrating an existing domain from Studio Classic to Studio.

The AWS Identity and Access Management role used to complete migration must have a policy attached with at least the following permissions. For information about creating an IAM policy, see Creating IAM policies.

The release of Studio includes updates to the AWS managed policies. For more information, see SageMaker AI Updates to AWS Managed Policies.

Phase 1 required permissions:

iam:CreateServiceLinkedRole

sagemaker:DescribeDomain

sagemaker:UpdateDomain

sagemaker:CreateDomain

sagemaker:CreateUserProfile

sagemaker:DeleteSpace

sagemaker:UpdateSpace

sagemaker:DeleteUserProfile

sagemaker:DeleteDomain

Phase 2 required permissions (Optional, only if using lifecycle configuration scripts):

No additional permissions needed. If the existing domain has lifecycle configurations and custom images, the admin will already have the required permissions.

Phase 3 using custom Amazon Elastic File System required permissions (Optional, only if transfering data):

efs:CreateMountTarget

efs:DescribeFileSystems

efs:DescribeMountTargets

efs:DescribeMountTargetSecurityGroups

efs:ModifyMountTargetSecurityGroups

ec2:DescribeSecurityGroups

ec2:DescribeNetworkInterfaceAttribute

ec2:DescribeNetworkInterfaces

ec2:AuthorizeSecurityGroupEgress

ec2:AuthorizeSecurityGroupIngress

ec2:CreateNetworkInterface

ec2:CreateNetworkInterfacePermission

ec2:RevokeSecurityGroupIngress

ec2:RevokeSecurityGroupEgress

ec2:DeleteSecurityGroup

datasync:CreateLocationEfs

datasync:StartTaskExecution

datasync:DeleteLocation

sagemaker:ListUserProfiles

sagemaker:DescribeUserProfile

sagemaker:UpdateDomain

sagemaker:UpdateUserProfile

Phase 3 using Amazon Simple Storage Service required permissions (Optional, only if transfering data):

efs:DescribeFileSystems

efs:DescribeMountTargets

efs:DescribeMountTargetSecurityGroups

ec2:CreateSecurityGroup

ec2:DescribeSecurityGroups

ec2:DescribeNetworkInterfaces

ec2:Cre

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
iam:CreateServiceLinkedRole
```

Example 2 (unknown):
```unknown
iam:PassRole
```

Example 3 (unknown):
```unknown
sagemaker:DescribeDomain
```

Example 4 (unknown):
```unknown
sagemaker:UpdateDomain
```

---

## Track the lineage of a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-lineage-tracking.html

**Contents:**
- Track the lineage of a pipeline
        - To track the lineage of a pipeline
        - To track the lineage of a pipeline
        - Note

In this tutorial, you use Amazon SageMaker Studio to track the lineage of an Amazon SageMaker AI ML Pipeline.

The pipeline was created by the Orchestrating Jobs with Amazon SageMaker Model Building Pipelines notebook in the Amazon SageMaker example GitHub repository. For detailed information on how the pipeline was created, see Define a pipeline.

Lineage tracking in Studio is centered around a directed acyclic graph (DAG). The DAG represents the steps in a pipeline. From the DAG you can track the lineage from any step to any other step. The following diagram displays the steps in the pipeline. These steps appear as a DAG in Studio.

To track the lineage of a pipeline in the Amazon SageMaker Studio console, complete the following steps based on whether you use Studio or Studio Classic.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, select Pipelines.

(Optional) To filter the list of pipelines by name, enter a full or partial pipeline name in the search field.

In the Name column, select a pipeline name to view details about the pipeline.

Choose the Executions tab.

In the Name column of the Executions table, select the name of a pipeline execution to view.

At the top right of the Executions page, choose the vertical ellipsis and choose Download pipeline definition (JSON). You can view the file to see how the pipeline graph was defined.

Choose Edit to open the Pipeline Designer.

Use the resizing and zoom controls at the top right corner of the canvas to zoom in and out of the graph, fit the graph to screen, or expand the graph to full screen.

To view your training, validation, and test datasets, complete the following steps:

Choose the Processing step in your pipeline graph.

In the right sidebar, choose the Overview tab.

In the Files section, find the Amazon S3 paths to the training, validation, and test datasets.

To view your model artifacts, complete the following steps:

Choose the Training step in your pipeline graph.

In the right sidebar, choose the Overview tab.

In the Files section, find the Amazon S3 paths to the model artifact.

To find the model package ARN, complete the following steps:

Choose the Register model step.

In the right sidebar, choose the Overview tab.

In the Files section, find the ARN of the model package.

Sign in to Amazon SageMaker Studio Classic. For more information, see Launch Amazon SageMaker Studio Classic.

In the left sidebar 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AbalonePipeline
```

Example 2 (unknown):
```unknown
AbaloneProcess
```

Example 3 (unknown):
```unknown
s3://sagemaker-eu-west-1-acct-id/sklearn-abalone-process-2020-12-05-17-28-28-509/output/train
s3://sagemaker-eu-west-1-acct-id/sklearn-abalone-process-2020-12-05-17-28-28-509/output/validation
s3://sagemaker-eu-west-1-acct-id/sklearn-abalone-process-2020-12-05-17-28-28-509/output/test
```

Example 4 (unknown):
```unknown
AbaloneTrain
```

---

## Get Amazon SageMaker Studio Classic Notebook and App Metadata

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-run-and-manage-metadata.html

**Contents:**
- Get Amazon SageMaker Studio Classic Notebook and App Metadata
        - Important
        - Topics
- Get Studio Classic Notebook Metadata
        - To view the notebook metadata:
- Get App Metadata
        - To get the App metadata

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can access notebook metadata and App metadata using the Amazon SageMaker Studio Classic UI.

Get Studio Classic Notebook Metadata

Jupyter notebooks contain optional metadata that you can access through the Amazon SageMaker Studio Classic UI.

In the right sidebar, choose the Property Inspector icon ( ).

Open the Advanced Tools section.

The metadata should look similar to the following.

When you create a notebook in Amazon SageMaker Studio Classic, the App metadata is written to a file named resource-metadata.json in the folder /opt/ml/metadata/. You can get the App metadata by opening an Image terminal from within the notebook. The metadata gives you the following information, which includes the SageMaker image and instance type the notebook runs in:

AppType – KernelGateway

DomainId – Same as the Studio ClassicID

UserProfileName – The profile name of the current user

ResourceArn – The Amazon Resource Name (ARN) of the App, which includes the instance type

ResourceName – The name of the SageMaker image

Additional metadata might be included for internal use by Studio Classic and is subject to change.

In the center of the notebook menu, choose the Launch Terminal icon ( ). This opens a terminal in the SageMaker image that the notebook runs in.

Run the following commands to display the contents of the resource-metadata.json file.

The file should look similar to the following.

**Examples:**

Example 1 (unknown):
```unknown
{
    "instance_type": "ml.t3.medium",
    "kernelspec": {
        "display_name": "Python 3 (Data Science)",
        "language": "python",
        "name": "python3__SAGEMAKER_INTERNAL__arn:aws:sagemaker:us-west-2:<acct-id>:image/datascience-1.0"
    },
    "language_info": {
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.7.10"
    }
}
```

Example 2 (unknown):
```unknown
resource-metadata.json
```

Example 3 (unknown):
```unknown
/opt/ml/metadata/
```

Example 4 (unknown):
```unknown
KernelGateway
```

---

## Using Amazon SageMaker Feature Store in the console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-use-with-studio.html#feature-store-create-feature-group-studio

**Contents:**
- Using Amazon SageMaker Feature Store in the console
        - Important
        - Topics
- Create a feature group from the console
- View feature group details from the console
- Update a feature group from the console
- View pipeline executions from the console
- View lineage from the console

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

You can use Amazon SageMaker Feature Store on the console to create, view, update, and monitor your feature groups. Monitoring in this guide includes viewing pipeline executions and lineage of your feature groups. This guide provides instructions on how to achieve these tasks from the console.

For Feature Store examples and resources using the Amazon SageMaker APIs and AWS SDK for Python (Boto3), see Amazon SageMaker Feature Store resources.

Create a feature group from the console

View feature group details from the console

Update a feature group from the console

View pipeline executions from the console

View lineage from the console

The create feature group process has four steps:

Enter feature group information.

Enter feature definitions.

Enter required features.

Enter feature group tags.

Consider which of the following options fits your use case:

Create an online store, an offline store, or both. For more information about the differences between online and offline stores, see Feature Store concepts.

Use a default AWS Key Management Service key or your own KMS key. The default key is AWS KMS key (SSE-KMS). You can reduce AWS KMS request costs by configuring use of Amazon S3 Bucket Keys on the offline store Amazon S3 bucket. The Amazon S3 Bucket Key must be enabled before using the bucket for your feature groups. For more information about reducing the cost by using Amazon S3 Bucket Keys, see Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys.

You can use the same key for both online and offline stores, or have a unique key for each. For more information about AWS KMS, see AWS Key Management Service.

If you create an offline store:

Decide if you want to create an Amazon S3 bucket or use an existing one. When usin

*[Content truncated]*

---

## Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html#studio-features

**Contents:**
- Amazon SageMaker Studio Classic
        - Important
- Amazon SageMaker Studio Classic maintenance phase plan
        - Note
        - Topics
- Amazon SageMaker Studio Classic Features

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic is a web-based integrated development environment (IDE) for machine learning (ML). Studio Classic lets you build, train, debug, deploy, and monitor your ML models. Studio Classic includes all of the tools you need to take your models from data preparation to experimentation to production with increased productivity. In a single visual interface, you can do the following tasks:

Write and run code in Jupyter notebooks

Prepare data for machine learning

Build and train ML models

Deploy the models and monitor the performance of their predictions

Track and debug ML experiments

Collaborate with other users in real time

For information on the onboarding steps for Studio Classic, see Amazon SageMaker AI domain overview.

For information about collaborating with other users in real time, see Collaboration with shared spaces.

For the AWS Regions supported by Studio Classic, see Supported Regions and Quotas.

The following table gives information about the timeline for when Amazon SageMaker Studio Classic entered its extended maintenance phase.

Starting December 31st, Studio Classic reaches end of maintenance. At this point, Studio Classic will no longer receive updates and security fixes. All new domains will be created with Amazon SageMaker Studio as the default.

Starting January 31st, users will no longer be able to create new JupyterLab 3 notebooks in Studio Classic. Users will also not be able to restart or update existing notebooks. Users will be able to access existing Studio Classic applications from Studio only to delete or stop existing notebooks.

Your existing Studio Classic domain is not automatically migrated to Studio. For information about migrating, see Migration from Amazon SageMaker Studio Classic.

Amazon SageMaker Studio Classic Features

Amazon SageMaker Studio Classic UI Overview

Launch Amazon SageMaker Studio Classic

JupyterLab Versioning in Amazon SageMaker S

*[Content truncated]*

---

## Manage Your Amazon EFS Storage Volume in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-manage-storage.html

**Contents:**
- Manage Your Amazon EFS Storage Volume in Amazon SageMaker Studio Classic
        - Important
        - Important
        - To find your Amazon EFS volume

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The first time a user on your team onboards to Amazon SageMaker Studio Classic, Amazon SageMaker AI creates an Amazon Elastic File System (Amazon EFS) volume for the team. A home directory is created in the volume for each user who onboards to Studio Classic as part of your team. Notebook files and data files are stored in these directories. Users don't have access to other team member's home directories. Amazon SageMaker AI domain does not support mounting custom or additional Amazon EFS volumes.

Don't delete the Amazon EFS volume. If you delete it, the domain will no longer function and all of your users will lose their work.

Open the SageMaker AI console.

On the left navigation pane, choose Admin configurations.

Under Admin configurations, choose domains.

From the Domains page, select the domain to find the ID for.

From the Domain details page, select the Domain settings tab.

Under General settings, find the Domain ID. The ID will be in the following format: d-xxxxxxxxxxxx.

Pass the Domain ID, as DomainId, to the describe_domain method.

In the response from describe_domain, note the value for the HomeEfsFileSystemId key. This is the Amazon EFS file system ID.

Open the Amazon EFS console. Make sure the AWS Region is the same Region that's used by Studio Classic.

Under File systems, choose the file system ID from the previous step.

To verify that you've chosen the correct file system, select the Tags heading. The value corresponding to the ManagedByAmazonSageMakerResource key should match the Studio Classic ID.

For information on how to access the Amazon EFS volume, see Using file systems in Amazon EFS.

To delete the Amazon EFS volume, see Deleting an Amazon EFS file system.

**Examples:**

Example 1 (unknown):
```unknown
d-xxxxxxxxxxxx
```

Example 2 (unknown):
```unknown
describe_domain
```

Example 3 (unknown):
```unknown
HomeEfsFileSystemId
```

Example 4 (unknown):
```unknown
ManagedByAmazonSageMakerResource
```

---

## Set up SageMaker Assets (administrator guide)

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sm-assets-set-up.html

**Contents:**
- Set up SageMaker Assets (administrator guide)
        - Important
        - Important
        - Note
        - Note
- Viewing and modifying your users' permissions
        - Important
        - To view or edit the permissions of your users

SageMaker Assets is only available in Amazon SageMaker Studio. If you're using Amazon SageMaker Studio Classic, you must migrate to Studio. For more information about Studio and Studio Classic, see Machine learning environments offered by Amazon SageMaker AI. For information about migrating, see Migration from Amazon SageMaker Studio Classic.

As business needs change, your users need to collaborate effectively to solve business problems as they arise. To solve them, users must share data and models with each other.

SageMaker Assets integrates Amazon SageMaker Studio with Amazon DataZone, a data management service. SageMaker Assets is a platform that helps your users share models and data with each other. You can use the following information to set up the integration between SageMaker Assets and Amazon DataZone.

You create an Amazon DataZone domain for your business line or organization. The domain is the core feature of Amazon DataZone. All of your users' data and models exist within the domain.

Within the Amazon DataZone domain, a subset of your users work on specific projects. A project typically corresponds to a particular business problem. Within the project, members can create datasets and models. By default, project members only have access to the data and models within the project. They can provide access to their data and models to other users within the organization.

Within the project, you create environments. For SageMaker Assets specifically, an environment is a collection of configured resources used to launch Amazon SageMaker Studio. For more information about the terminology used in Amazon DataZone, see Terminology and concepts.

Depending on the set up you choose, Amazon SageMaker Studio uses one of the following:

An Amazon SageMaker AI domain that Amazon DataZone creates as part of your SageMaker AI environment.

Your existing Amazon SageMaker AI domain that you migrate to Amazon DataZone

You can access Studio from the Amazon SageMaker AI domain, but we recommend accessing it from the project you've created. For information about accessing Studio, see Work with assets (user guide).

Use the steps in the following list and the documentation it references to set up Amazon DataZone with an Amazon SageMaker AI domain that it creates.

Create an Amazon DataZone domain that corresponds to your users' organization or business line. For information about creating an Amazon DataZone domain, see Create domains.

Enable the SageMaker AI bluep

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
python example-script AWS Region 111122223333
```

Example 2 (unknown):
```unknown
example-script
```

Example 3 (unknown):
```unknown
111122223333
```

---

## Access Spark UI from Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-access-spark-ui.html

**Contents:**
- Access Spark UI from Studio or Studio Classic
- Set up SSH tunneling for Spark UI access
        - Note
- Presigned URLs
        - Note

The following sections give instructions for accessing the Spark UI from SageMaker AI Studio or Studio Classic notebooks. The Spark UI allows you to monitor and debug your Spark Jobs submitted to run on Amazon EMR from Studio or Studio Classic notebooks. SSH tunneling and presigned URLs are two ways for accessing the Spark UI.

To set up SSH tunneling to access the Spark UI, follow one of the two options in this section.

Options for setting up SSH tunneling:

Option 1: Set up an SSH tunnel to the master node using local port forwarding

Option 2, part 1: Set up an SSH tunnel to the master node using dynamic port forwarding

Option 2, part 2: Configure proxy settings to view websites hosted on the master node

For information about viewing web interfaces hosted on Amazon EMR clusters, see View web interfaces hosted on Amazon EMR Clusters. You can also visit your Amazon EMR console to get access to the Spark UI.

You can set up an SSH tunnel even if presigned URLs are not available to you.

To create one-click URLs that can access Spark UI on Amazon EMR from SageMaker Studio or Studio Classic notebooks, you must enable the following IAM permissions. Choose the option that applies to you:

For Amazon EMR clusters that are in the same account as the SageMaker Studio or Studio Classic notebook: Add the following permissions to the SageMaker Studio or Studio Classic IAM execution role.

For Amazon EMR clusters that are in a different account (not SageMaker Studio or Studio Classic notebook): Add the following permissions to the cross-account role that you created for List Amazon EMR clusters from Studio or Studio Classic.

You can access presigned URLs from the console in the following regions:

US East (N. Virginia) Region

US West (N. California) Region

Canada (Central) Region

Europe (Frankfurt) Region

Europe (Stockholm) Region

Europe (Ireland) Region

Europe (London) Region

Europe (Paris) Region

Asia Pacific (Tokyo) Region

Asia Pacific (Seoul) Region

Asia Pacific (Sydney) Region

Asia Pacific (Mumbai) Region

Asia Pacific (Singapore) Region

South America (São Paulo)

The following policy gives access to presigned URLs for your execution role.

**Examples:**

Example 1 (unknown):
```unknown
{
        "Sid": "AllowPresignedUrl",
        "Effect": "Allow",
        "Action": [
            "elasticmapreduce:DescribeCluster",
            "elasticmapreduce:ListInstanceGroups",
            "elasticmapreduce:CreatePersistentAppUI",
            "elasticmapreduce:DescribePersistentAppUI",
            "elasticmapreduce:GetPersistentAppUIPresignedURL",
            "elasticmapreduce:GetOnClusterAppUIPresignedURL"
        ],
        "Resource": [
            "arn:aws:elasticmapreduce:region:account-id:cluster/*"
        ]
}
```

---

## Troubleshooting Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-troubleshooting.html

**Contents:**
- Troubleshooting Amazon SageMaker Studio Classic
        - Important
        - Important
- Studio Classic application issues
        - To verify or create mount targets.
        - To resolve lifecycle configuration issues
- KernelGateway application issues
        - To verify the security group rules

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

This topic describes how to troubleshoot common Amazon SageMaker Studio Classic issues during setup and use. The following are common errors that might occur while using Amazon SageMaker Studio Classic. Each error is followed by its solution.

The following issues occur when launching and using the Studio Classic application.

Screen not loading: Clearing workspace and waiting doesn't help

When launching the Studio Classic application, a pop-up displays the following message. No matter which option is selected, Studio Classic does not load.

The Studio Classic application can have a launch delay if multiple tabs are open in the Studio Classic workspace or several files are on Amazon EFS. This pop-up should disappear in a few seconds after the Studio Classic workspace is ready.

If you continue to see a loading screen with a spinner after selecting either of the options, there could be connectivity issues with the Amazon Virtual Private Cloud used by Studio Classic.

To resolve connectivity issues with the Amazon Virtual Private Cloud (Amazon VPC) used by Studio Classic, verify the following networking configurations:

If your domain is set up in VpcOnly mode: Verify that there is an Amazon VPC 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Loading...
The loading screen is taking a long time. Would you like to clear the workspace or keep waiting?
```

Example 2 (unknown):
```unknown
Amazon SageMaker Studio
The JupyterServer app default encountered a problem and was stopped.
```

Example 3 (unknown):
```unknown
!pip install
```

Example 4 (unknown):
```unknown
pip install --user
```

---

## Connect to an Amazon EMR cluster from SageMaker Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/connect-emr-clusters.html

**Contents:**
- Connect to an Amazon EMR cluster from SageMaker Studio or Studio Classic
        - Important
- Connect to an Amazon EMR cluster using the Studio UI
        - To connect an Amazon EMR cluster to a new JupyterLab notebook from the Studio UI:
        - Note
        - Note
        - Important
        - Alternatively, you can connect to a cluster from a JupyterLab or Studio Classic notebook.
        - Note
        - Important

Data scientists and data engineers can discover and then connect to an Amazon EMR cluster directly from the Studio user interface. Before you begin, ensure that you have configured the necessary permissions as described in the Step 4: Set up the permissions to enable listing and launching Amazon EMR clusters from Studio section. These permissions grant Studio the ability to create, start, view, access, and terminate clusters.

You can connect an Amazon EMR cluster to a new JupyterLab notebook directly from the Studio UI, or choose to initiate the connection in a notebook of a running JupyterLab application.

You can only discover and connect to Amazon EMR clusters for JupyterLab and Studio Classic applications that are launched from private spaces. Ensure that the Amazon EMR clusters are located in the same AWS region as your Studio environment. Your JupyterLab space must use a SageMaker Distribution image version 1.10 or higher.

To connect to your cluster using the Studio or Studio Classic UI, you can either initiate a connection from the list of clusters accessed in List Amazon EMR clusters from Studio or Studio Classic, or from a notebook in SageMaker Studio or Studio Classic.

In the Studio UI's left-side panel, select the Data node in the left navigation menu. Navigate down to Amazon EMR applications and clusters. This opens up a page listing the Amazon EMR clusters that you can access from Studio in the Amazon EMR clusters tab.

If you or your administrator have configured the permissions to allow cross-account access to Amazon EMR clusters, you can view a consolidated list of clusters across all accounts that you have granted access to Studio.

Select an Amazon EMR cluster you want to connect to a new notebook, and then choose Attach to notebook. This opens up a modal window displaying the list of your JupyterLab spaces.

Select the space from which you want to launch a JupyterLab application, and then choose Open notebook. This launches a JupyterLab application from your chosen space and opens a new notebook.

Users of Studio Classic need to select an image and kernel. For a list of supported images, see Supported images and kernels to connect to an Amazon EMR cluster from Studio or Studio Classic or refer to Bring your own image.

Alternatively, you can create a new private space by choosing the Create new space button at the top of the modal window. Enter a name for your space and then choose Create space and open notebook. This creates a privat

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
--assumable-role-arn
```

Example 2 (unknown):
```unknown
--verify-certificate
```

Example 3 (unknown):
```unknown
%load_ext sagemaker_studio_analytics_extension.magics
%sm_analytics emr connect --cluster-id cluster_id \
--auth-type Kerberos --language python
[--assumable-role-arn EMR_access_role_ARN ]
[--verify-certificate /home/user/certificateKey.pem]
```

Example 4 (unknown):
```unknown
EMR_access_role_ARN
```

---

## SageMaker JumpStart pretrained models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html

**Contents:**
- SageMaker JumpStart pretrained models
- Open and use JumpStart in Studio
        - Important
  - Open JumpStart in Studio
        - Important
  - Use JumpStart in Studio
  - Manage JumpStart in Studio
- Open and use JumpStart in Studio Classic
        - Important
  - Open JumpStart in Studio Classic

Amazon SageMaker JumpStart provides pretrained, open-source models for a wide range of problem types to help you get started with machine learning. You can incrementally train and tune these models before deployment. JumpStart also provides solution templates that set up infrastructure for common use cases, and executable example notebooks for machine learning with SageMaker AI.

You can deploy, fine-tune, and evaluate pretrained models from popular models hubs through the JumpStart landing page in the updated Studio experience.

You can also access pretrained models, solution templates, and examples through the JumpStart landing page in Amazon SageMaker Studio Classic.

The following steps show how to access JumpStart models using Amazon SageMaker Studio and Amazon SageMaker Studio Classic.

You can also access JumpStart models using the SageMaker Python SDK. For information about how to use JumpStart models programmatically, see Use SageMaker JumpStart Algorithms with Pretrained Models.

The following sections give information on how to open, use, and manage JumpStart from the Studio UI.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

In Amazon SageMaker Studio, open the JumpStart landing page either through the Home page or the Home menu on the left-side panel. This opens the SageMaker JumpStart landing page where you can explore model hubs and search for models.

From the Home page, choose JumpStart in the Prebuilt and automated solutions pane.

From the Home menu in the left panel, navigate to the SageMaker JumpStart node.

For more information on getting started with Amazon SageMaker Studio, see Amazon SageMaker Studio.

Before downloading or using third-party content: You are responsible for reviewing and complying with any applicable license terms and making sure that they are acceptable for your use case.

From the SageMaker JumpStart landing page in Studio, you can explore model hubs from providers of both proprietary and publicly available models.

You can find specific hubs or models using the search bar. Within each model hub, you can search directly for models, sort by provided attributes, or filter based on a list of provided model tasks.

Choose a model to see its model detail card. In the upper right

*[Content truncated]*

---

## Update a MLOps Project in Amazon SageMaker Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-update.html

**Contents:**
- Update a MLOps Project in Amazon SageMaker Studio or Studio Classic
        - To update a project in Studio Classic

This procedure demonstrates how to update a MLOps project in Amazon SageMaker Studio or Studio Classic. Updating the project gives you the option to modify your end-to-end ML solution. You can update the Description, template version, and template parameters.

An IAM account or IAM Identity Center to sign in to Studio or Studio Classic. For information, see Amazon SageMaker AI domain overview.

Basic familiarity with the Studio or Studio Classic user interface. For information about the Studio UI, see Amazon SageMaker Studio. For information about Studio Classic, see Amazon SageMaker Studio Classic UI Overview.

Add the following custom inline policies to the specified roles:

User-created role having AmazonSageMakerFullAccess

AmazonSageMakerServiceCatalogProductsLaunchRole

To update your project in Studio or Studio Classic, complete the following steps.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, choose Deployments, and then choose Projects.

Choose the radio button next to the project you want to update.

Choose the vertical ellipsis above the upper-right corner of the projects list, and choose Update.

Review the project updates in the summary table, and choose Update. It may take a few minutes for the project to update.

Sign in to Studio Classic. For more information, see Amazon SageMaker AI domain overview.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Deployments from the menu, and then select Projects. A list of your projects appears.

Select the name of the project you want to update in the projects list.

Choose Update from the Actions menu in the upper-right corner of the project tab.

In the Update project dialog box, you can edit the Description and listed template parameters.

Choose View difference.

A dialog box displays your original and updated project settings. Any change in your project settings can modify or delete resources in the current project. The dialog box displays these changes as well.

You may need to wait a few minutes for the Update button to become active. Choose Update.

The project update may take a few minutes to complete. Select Settings in the project tab and ensure the parameters have been updated correctly.

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "servicecatalog:CreateProvisionedProductPlan",
                "servicecatalog:DescribeProvisionedProductPlan",
                "servicecatalog:DeleteProvisionedProductPlan"
            ],
            "Resource": "*"
        }
    ]
}
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "servicecatalog:CreateProvisionedProductPlan",
                "servicecatalog:DescribeProvisionedProductPlan",
                "servicecatalog:DeleteProvisionedProductPlan"
            ],
            "Resource": "*"
        }
    ]
}
```

Example 4 (unknown):
```unknown
AmazonSageMakerServiceCatalogProductsLaunchRole
```

---

## Shut Down Resources from Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-run-and-manage-shut-down.html

**Contents:**
- Shut Down Resources from Amazon SageMaker Studio Classic
        - Important
        - Note
        - Topics
- Shut down an open notebook
        - To shut down an open notebook from the File menu
- Shut down resources
        - To shut down resources
        - Note
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can shut down individual Amazon SageMaker AI resources, including notebooks, terminals, kernels, apps, and instances from Studio Classic. You can also shut down all of the resources in one of these categories at the same time. Amazon SageMaker Studio Classic does not support shutting down resources from within a notebook.

When you shut down a Studio Classic notebook instance, additional resources that you created in Studio Classic are not deleted. For example, additional resources can include SageMaker AI endpoints, Amazon EMR clusters, and Amazon S3 buckets. To stop the accrual of charges, you must manually delete these resources. For information about finding resources that are accruing charges, see Analyzing your costs with AWS Cost Explorer.

The following topics demonstrate how to delete these SageMaker AI resources.

Shut down an open notebook

When you shut down a Studio Classic notebook, the notebook is not deleted. The kernel that the notebook is running on is shut down and any unsaved information in the notebook is lost. You can shut down an open notebook from the Studio Classic File menu or from the Running Terminal and Kernels pane. The following procedure shows how to shut down an open notebook from the Studio Classic File menu.

Launch Studio Classic by following the steps in Launch Amazon SageMaker Studio Classic.

(Optional) Save the notebook contents by choosing File, then Save Notebook.

Choose Close and Shutdown Notebook. This opens a pop-up window.

From the pop-up window, choose OK.

You can reach the Running Terminals and Kernels pane of Amazon SageMaker Studio Classic by selecting the Running Terminals and Kernels icon ( ). The Running Terminals and Kernels pane consists of four sections. Each section lists all the resources of that type. You can shut down each resource individually or shut down all the resources in a section at the same time.

When you choose to shut down all resources 

*[Content truncated]*

---

## Perform Common Tasks in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks.html

**Contents:**
- Perform Common Tasks in Amazon SageMaker Studio Classic
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The following sections describe how to perform common tasks in Amazon SageMaker Studio Classic. For an overview of the Studio Classic interface, see Amazon SageMaker Studio Classic UI Overview.

Upload Files to Amazon SageMaker Studio Classic

Clone a Git Repository in Amazon SageMaker Studio Classic

Stop a Training Job in Amazon SageMaker Studio Classic

Use TensorBoard in Amazon SageMaker Studio Classic

Use Amazon Q Developer with Amazon SageMaker Studio Classic

Manage Your Amazon EFS Storage Volume in Amazon SageMaker Studio Classic

Provide Feedback on Amazon SageMaker Studio Classic

Shut Down and Update Amazon SageMaker Studio Classic and Apps

---

## Integrate MLflow with your environment

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-track-experiments.html

**Contents:**
- Integrate MLflow with your environment
        - Important
- Install MLflow and the AWS MLflow plugin
- Connect to your MLflow Tracking Server

The following page describes how to get started with the MLflow SDK and the AWS MLflow plugin within your development environment. This can include local IDEs or a Jupyter Notebook environment within Studio or Studio Classic.

Amazon SageMaker AI uses an MLflow plugin to customize the behavior of the MLflow Python client and integrate AWS tooling. The AWS MLflow plugin authenticates API calls made with MLflow using AWS Signature Version 4. The AWS MLflow plugin allows you to connect to your MLflow tracking server using the tracking server ARN. For more information about plugins, see AWS MLflow plugin and MLflow plugins.

Your user IAM permissions within your development environment must have access to any relevant MLflow API actions to successfully run provided examples. For more information, see Set up IAM permissions for MLflow.

For more information about using the MLflow SDK, see Python API in the MLflow documentation.

Within your development environment, install both MLflow and the AWS MLflow plugin.

To ensure compatibility between your MLflow client and tracking server, use the corresponding MLflow version based on your tracking server version:

For tracking server 2.13.x, use mlflow==2.13.2

For tracking server 2.16.x, use mlflow==2.16.2

For tracking server 3.0.x, use mlflow==3.0.0

To see which versions of MLflow are available to use with SageMaker AI, see Tracking server versions.

Use mlflow.set_tracking_uri to connect to a your tracking server from your development environment using its ARN:

**Examples:**

Example 1 (unknown):
```unknown
pip install sagemaker-mlflow
```

Example 2 (unknown):
```unknown
mlflow==2.13.2
```

Example 3 (unknown):
```unknown
mlflow==2.16.2
```

Example 4 (unknown):
```unknown
mlflow==3.0.0
```

---

## Shut down the Amazon SageMaker Debugger Insights instance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-on-studio-insights-close.html

**Contents:**
- Shut down the Amazon SageMaker Debugger Insights instance

When you are not using the SageMaker Debugger Insights dashboard, you should shut down the app instance to avoid incurring additional fees.

To shut down the SageMaker Debugger Insights app instance in Studio Classic

In Studio Classic, select the Running Instances and Kernels icon ( ).

Under the RUNNING APPS list, look for the sagemaker-debugger-1.0 app. Select the shutdown icon ( ) next to the app. The SageMaker Debugger Insights dashboards run on an ml.m5.4xlarge instance. This instance also disappears from the RUNNING INSTANCES when you shut down the sagemaker-debugger-1.0 app.

**Examples:**

Example 1 (unknown):
```unknown
ml.m5.4xlarge
```

---

## JupyterLab Versioning in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jl.html#studio-jl-set-cli

**Contents:**
- JupyterLab Versioning in Amazon SageMaker Studio Classic
        - Important
        - Important
- JupyterLab 3
  - Important changes to JupyterLab 3
- Restricting default JupyterLab version using an IAM policy condition key
- Setting a default JupyterLab version
  - From the console
  - From the AWS CLI
    - Create or update domain

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The Amazon SageMaker Studio Classic interface is based on JupyterLab, which is a web-based interactive development environment for notebooks, code, and data. Studio Classic only supports using JupyterLab 3.

If you created your domain and user profile using the AWS Management Console before 08/31/2022 or using the AWS Command Line Interface before 02/22/23, then your Studio Classic instance defaulted to JupyterLab 1. After 07/01/2024, you cannot create any Studio Classic applications that run JupyterLab 1.

JupyterLab 3 includes the following features that are not available in previous versions. For more information about these features, see JupyterLab 3.0 is released!.

Visual debugger when using the Base Python 2.0 and Data Science 2.0 kernels.

Table of Contents (TOC)

Multi-language support

Single interface mode

Consider the following when using JupyterLab 3:

When setting the JupyterLab version using the AWS CLI, select the corresponding image for your Region and JupyterLab version from the image list in From the AWS CLI.

In JupyterLab 3, you must activate the studio conda environment before installing extensions. For more information, see Installing JupyterLab and Jupyter Server extensi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 3 (unknown):
```unknown
111122223333
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockUsersFromCreatingJupyterLab3Apps",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateUserProfile",
                "sagemaker:UpdateUserProfile"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

---

## Code Editor in Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/code-editor.html

**Contents:**
- Code Editor in Amazon SageMaker Studio
        - Important
        - Topics

Code Editor, based on Code-OSS, Visual Studio Code - Open Source, helps you write, test, debug, and run your analytics and machine learning code. Code Editor extends and is fully integrated with Amazon SageMaker Studio. It also supports integrated development environment (IDE) extensions available in the Open VSX Registry. The following page gives information about Code Editor and key details for using it.

Code Editor has the AWS Toolkit for VS Code extension pre-installed, which enables connections to AWS services such as Amazon CodeWhisperer, a general purpose, machine learning-powered code generator that provides code recommendations in real time. For more information about extensions, see Code Editor Connections and Extensions.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

To launch Code Editor, create a Code Editor private space. The Code Editor space uses a single Amazon Elastic Compute Cloud (Amazon EC2) instance for your compute and a single Amazon Elastic Block Store (Amazon EBS) volume for your storage. Everything in your space such as your code, Git profile, and environment variables are stored on the same Amazon EBS volume. The volume has 3000 IOPS and a throughput of 125 MBps. Your administrator has configured the default Amazon EBS storage settings for your space.

The default storage size is 5 GB, but your administrator can increase the amount of space you get. For more information, see Change the default storage size.

The working directory of your users within the storage volume is /home/sagemaker-user. If you specify your own AWS KMS key to encrypt the volume, everything in the working directory is encrypted using your customer managed key. If you don't specify an AWS KMS key, the data inside /home/sagemaker-user is encrypted with an AWS managed key. Regardless of whether you specify an AWS KMS key, all of the data outside of the working directory is encrypted with an AWS Managed Key.

You can scale your compute up or down by changing the Amazon EC2 instance type that runs your Code Editor application. Before you change the associated instance type, you must first stop your Code Editor space. For more information, see Code Editor application instances and images.

Your administrator might provide

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
/home/sagemaker-user
```

Example 2 (unknown):
```unknown
/home/sagemaker-user
```

---

## (Optional) Migrate custom images and lifecycle configurations

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-lcc.html

**Contents:**
- (Optional) Migrate custom images and lifecycle configurations
- Migrate custom images
- Migrate lifecycle configurations
        - Note
  - Considerations when refactoring LCCs

You must update your custom images and lifecycle configuration (LCC) scripts to work with the simplified local run model in Amazon SageMaker Studio. If you have not created custom images or lifecycle configurations in your domain, skip this phase.

Amazon SageMaker Studio Classic operates in a split environment with:

A JupyterServer application running the Jupyter Server.

Studio Classic notebooks running on one or more KernelGateway applications.

Studio has shifted away from a split environment. Studio runs the JupyterLab and Code Editor, based on Code-OSS, Visual Studio Code - Open Source applications in a local runtime model. For more information about the change in architecture, see Boost productivity on Amazon SageMaker Studio.

Your existing Studio Classic custom images may not work in Studio. We recommend creating a new custom image that satisfies the requirements for use in Studio. The release of Studio simplifies the process to build custom images by providing SageMaker Studio image support policy. SageMaker AI Distribution images include popular libraries and packages for machine learning, data science, and data analytics visualization. For a list of base SageMaker Distribution images and Amazon Elastic Container Registry account information, see Amazon SageMaker Images Available for Use With Studio Classic Notebooks.

To build a custom image, complete one of the following.

Extend a SageMaker Distribution image with custom packages and modules. These images are pre-configured with JupyterLab and Code Editor, based on Code-OSS, Visual Studio Code - Open Source.

Build a custom Dockerfile file by following the instructions in Bring your own image (BYOI). You must install JupyterLab and the open source CodeServer on the image to make it compatible with Studio.

Because of the simplified local runtime model in Studio, we recommend migrating the structure of your existing Studio Classic LCCs. In Studio Classic, you often have to create separate lifecycle configurations for both KernelGateway and JupyterServer applications. Because the JupyterServer and KernelGateway applications run on separate compute resources within Studio Classic, Studio Classic LCCs can be one of either type:

JupyterServer LCC: These LCCs mostly govern a user’s home actions, including setting proxy, creating environment variables, and auto-shutdown of resources.

KernelGateway LCC: These LCCs govern Studio Classic notebook environment optimizations. This includes updating num

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
JupyterServer
```

Example 2 (unknown):
```unknown
KernelGateway
```

Example 3 (unknown):
```unknown
Data Science 3.0
```

Example 4 (unknown):
```unknown
Pytorch 2.0 GPU
```

---

## Delete a MLOps Project using Amazon SageMaker Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-delete.html

**Contents:**
- Delete a MLOps Project using Amazon SageMaker Studio or Studio Classic
        - Note

This procedure demonstrates how to delete a MLOps project using Amazon SageMaker Studio or Studio Classic.

You can only delete projects in Studio or Studio Classic that you have created. This condition is part of the service catalog permission servicecatalog:TerminateProvisionedProduct in the AmazonSageMakerFullAccess policy. If needed, you can update this policy to remove this condition.

An IAM account or IAM Identity Center to sign in to Studio or Studio Classic. For information, see Amazon SageMaker AI domain overview.

Basic familiarity with the Studio or Studio Classic user interface. For information about the Studio UI, see Amazon SageMaker Studio. For information about Studio Classic, see Amazon SageMaker Studio Classic UI Overview.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, choose Deployments, and then choose Projects.

Choose the radio button next to the project you want to delete.

Choose the vertical ellipsis above the upper-right corner of the projects list, and choose Delete.

Review the information in the Delete project dialog box, and choose Yes, delete the project if you still want to delete the project.

Your projects list appears. Confirm that your project no longer appears in the list.

Sign in to Studio Classic. For more information, see Amazon SageMaker AI domain overview.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Deployments from the menu, and then select Projects.

Select the target project from the dropdown list. If you don’t see your project, type the project name and apply the filter to find your project.

Once you've found your project, select the project name to view details.

Choose Delete from the Actions menu.

Confirm your choice by choosing Delete from the Delete Project window.

**Examples:**

Example 1 (unknown):
```unknown
servicecatalog:TerminateProvisionedProduct
```

Example 2 (unknown):
```unknown
AmazonSageMakerFullAccess
```

---

## Change the Instance Type for an Amazon SageMaker Studio Classic Notebook

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-run-and-manage-switch-instance-type.html

**Contents:**
- Change the Instance Type for an Amazon SageMaker Studio Classic Notebook
        - Important
        - To change the instance type

When you open a new Studio Classic notebook for the first time, you are assigned a default Amazon Elastic Compute Cloud (Amazon EC2) instance type to run the notebook. When you open additional notebooks on the same instance type, the notebooks run on the same instance as the first notebook, even if the notebooks use different kernels.

You can change the instance type that your Studio Classic notebook runs on from within the notebook.

The following information only applies to Studio Classic notebooks. For information about how to change the instance type of a Amazon SageMaker notebook instance, see Update a Notebook Instance.

If you change the instance type, unsaved information and existing settings for the notebook are lost, and installed packages must be re-installed.

The previous instance type continues to run even if no kernel sessions or apps are active. You must explicitly stop the instance to stop accruing charges. To stop the instance, see Shut down resources.

The following screenshot shows the menu from a Studio Classic notebook. The processor and memory of the instance type powering the notebook are displayed as 2 vCPU + 4 GiB.

Choose the processor and memory of the instance type powering the notebook. This opens a pop up window.

From the Set up notebook environment pop up window, select the Instance type dropdown menu.

From the Instance type dropdown, choose one of the instance types that are listed.

After choosing a type, choose Select.

Wait for the new instance to become enabled, and then the new instance type information is displayed.

For a list of the available instance types, see Instance Types Available for Use With Amazon SageMaker Studio Classic Notebooks.

---

## Terminate an Amazon EMR cluster from Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/terminate-emr-clusters.html

**Contents:**
- Terminate an Amazon EMR cluster from Studio or Studio Classic
        - To terminate a cluster in a Running state, navigate to the list of available Amazon EMR clusters.

The following procedure shows how to terminate an Amazon EMR cluster from a Studio or Studio Classic notebook.

In the Studio UI, scroll down to the Data node in the left navigation menu.

Navigate down to the EMR Clusters node. This opens up a page listing the Amazon EMR clusters that you have access to.

Select the name of the cluster that you want to terminate, and then choose Terminate.

This opens up a confirmation window informing you that any pending work or data on your cluster will be lost permanently after termination. Confirm by choosing Terminate again.

---

## Download a pipeline definition file

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-studio-download.html

**Contents:**
- Download a pipeline definition file

You can download the definition file for your SageMaker AI pipeline directly from the Amazon SageMaker Studio UI. You can use this pipeline definition file for:

Backup and restoration: Use the downloaded file to create a backup of your pipeline configuration, which you can restore in case of infrastructure failures or accidental changes.

Version control: Store the pipeline definition file in a source control system to track changes to the pipeline and revert to previous versions if needed.

Programmatic interactions: Use the pipeline definition file as input to the SageMaker SDK or AWS CLI.

Integration with automation processes: Integrate the pipeline definition into your CI/CD workflows or other automation processes.

To download the definition file of a pipeline, complete the following steps based on whether you use Studio or Studio Classic.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, select Pipelines.

(Optional) To filter the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name. The Executions page opens and displays a list of pipeline executions.

Stay on the Executions page or choose the Graph, Information, or Parameters page to the left of the pipeline executions table. You can download the pipeline definition from any of these pages.

At the top right of the page, choose the vertical ellipsis and choose Download pipeline definition (JSON).

Sign in to Amazon SageMaker Studio Classic. For more information, see Launch Amazon SageMaker Studio Classic.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Pipelines from the menu.

To narrow the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name.

Choose the Settings tab.

Choose Download pipeline definition file.

---

## Configure Amazon EMR CloudFormation templates in the Service Catalog

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-set-up-emr-templates.html

**Contents:**
- Configure Amazon EMR CloudFormation templates in the Service Catalog
        - Note
- Step 0: Check your networking and prepare your CloudFormation stack
- Step 1: Associate your Service Catalog portfolio with SageMaker AI
- Step 2: Reference an Amazon EMR template in a Service Catalog product
        - Note
- Step 3: Parameterize the Amazon EMR CloudFormation template
- Step 4: Set up the permissions to enable listing and launching Amazon EMR clusters from Studio
        - Important
        - Note

This topic assumes administrators are familiar with AWS CloudFormation, portfolios and products in AWS Service Catalog, as well as Amazon EMR.

To simplify the creation of Amazon EMR clusters from Studio, administrators can register an Amazon EMR CloudFormation template as a product in an AWS Service Catalog portfolio. To make the template available to data scientists, they must associate the portfolio with the SageMaker AI execution role used in Studio or Studio Classic. Finally, to allow users to discover templates, provision clusters, and connect to Amazon EMR clusters from Studio or Studio Classic, administrators need to set appropriate access permissions.

The Amazon EMR AWS CloudFormation templates can allow end-users to customize various cluster aspects. For example, administrators can define an approved list of instance types that users can choose from when creating a cluster.

The following instructions use end-to-end CloudFormation stacks to setup a Studio or Studio Classic domain, a user profile, a Service Catalog portfolio, and populate an Amazon EMR launch template. The following steps highlight the specific settings that administrators must apply in their end-to-end stack to enable Studio or Studio Classic to access Service Catalog products and provision Amazon EMR clusters.

The GitHub repository aws-samples/sagemaker-studio-emr contains example end-to-end CloudFormation stacks that deploy the necessary IAM roles, networking, SageMaker domain, user profile, Service Catalog portfolio, and add an Amazon EMR launch CloudFormation template. The templates provide different authentication options between Studio or Studio Classic and the Amazon EMR cluster. In these example templates, the parent CloudFormation stack passes SageMaker AI VPC, security group, and subnet parameters to the Amazon EMR cluster template.

The sagemaker-studio-emr/cloudformation/emr_servicecatalog_templates repository contains various sample Amazon EMR CloudFormation launch templates, including options for single account and cross-account deployments.

Refer to Connect to an Amazon EMR cluster from SageMaker Studio or Studio Classic for details on the authentication methods you can use to connect to an Amazon EMR cluster.

To let data scientists discover Amazon EMR CloudFormation templates and provision clusters from Studio or Studio Classic, follow these steps.

Ensure that you have reviewed the networking and security requirements in Configure network access for your Amaz

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
SageMakerExecutionRole.Arn
```

Example 2 (unknown):
```unknown
SageMakerStudioEMRProductPortfolio.ID
```

Example 3 (unknown):
```unknown
SageMakerStudioEMRProductPortfolioPrincipalAssociation:
    Type: AWS::ServiceCatalog::PortfolioPrincipalAssociation
    Properties:
      PrincipalARN: SageMakerExecutionRole.Arn
      PortfolioId: SageMakerStudioEMRProductPortfolio.ID
      PrincipalType: IAM
```

Example 4 (unknown):
```unknown
SageMakerExecutionRole.Arn
```

---

## Security and Permissions

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-security.html

**Contents:**
- Security and Permissions
- Add a Bucket Policy To Restrict Access to Datasets Imported to Data Wrangler
        - To set up a bucket policy on the S3 bucket that stores your Data Wrangler resources:
- Create an Allowlist for Data Wrangler
        - Note
        - Important
- Grant an IAM Role Permission to Use Data Wrangler
- Snowflake and Data Wrangler
- Data Encryption with AWS KMS
  - Amazon S3 customer managed key setup for Data Wrangler imported data storage

When you query data from Athena or Amazon Redshift, the queried dataset is automatically stored in the default SageMaker AI S3 bucket for the AWS Region in which you are using Studio Classic. Additionally, when you export a Jupyter Notebook from Amazon SageMaker Data Wrangler and run it, your data flows, or .flow files, are saved to the same default bucket, under the prefix data_wrangler_flows.

For high-level security needs, you can configure a bucket policy that restricts the AWS roles that have access to this default SageMaker AI S3 bucket. Use the following section to add this type of policy to an S3 bucket. To follow the instructions on this page, use the AWS Command Line Interface (AWS CLI). To learn how, see Configuring the AWS CLI in the IAM User Guide.

Additionally, you need to grant each IAM role that uses Data Wrangler permissions to access required resources. If you do not require granular permissions for the IAM role you use to access Data Wrangler, you can add the IAM managed policy, AmazonSageMakerFullAccess, to an IAM role that you use to create your Studio Classic user. This policy grants you full permission to use Data Wrangler. If you require more granular permissions, refer to the section, Grant an IAM Role Permission to Use Data Wrangler.

You can add a policy to the S3 bucket that contains your Data Wrangler resources using an Amazon S3 bucket policy. Resources that Data Wrangler uploads to your default SageMaker AI S3 bucket in the AWS Region you are using Studio Classic in include the following:

Queried Amazon Redshift results. These are stored under the redshift/ prefix.

Queried Athena results. These are stored under the athena/ prefix.

The .flow files uploaded to Amazon S3 when you run an exported Jupyter Notebook Data Wrangler produces. These are stored under the data_wrangler_flows/ prefix.

Use the following procedure to create an S3 bucket policy that you can add to restrict IAM role access to that bucket. To learn how to add a policy to an S3 bucket, see How do I add an S3 Bucket policy?.

Configure one or more IAM roles that you want to be able to access Data Wrangler.

Open a command prompt or shell. For each role that you create, replace role-name with the name of the role and run the following:

In the response, you see a RoleId string which begins with AROA. Copy this string.

Add the following policy to the SageMaker AI default bucket in the AWS Region in which you are using Data Wrangler. Replace region with the AW

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 2 (unknown):
```unknown
$ aws iam get-role --role-name role-name
```

Example 3 (unknown):
```unknown
AROAEXAMPLEID
```

Example 4 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::sagemaker-us-east-1-111122223333/data_wrangler_flows/",
        "arn:aws:s3:::sagemaker-us-east-1-111122223333/data_wrangler_flows/*",
        "arn:aws:s3:::sagemaker-us-east-1-111122223333/athena",
        "arn:aws:s3:::sagemaker-us-east-1-111122223333/athena/*",
        "arn:aws:s3:::sagemaker-us-east-1-111122223333/redshift",
        "arn:aws:s3:::sagemaker-us-east-1-111122223333/redshift/*"

      ],
      "Condition": {
      
...
```

---

## Connect your local Visual Studio Code to SageMaker spaces with remote access

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/remote-access.html

**Contents:**
- Connect your local Visual Studio Code to SageMaker spaces with remote access
        - Note
        - Topics
- Key concepts
- Connection methods
- Supported IDEs
- VS Code version requirement
- Operating system requirements
- Local machine prerequisites
        - Important

You can remotely connect from Visual Studio Code to Amazon SageMaker Studio spaces. You can use your customized local VS Code setup, including AI-assisted development tools and custom extensions, with the scalable compute resources in Amazon SageMaker AI. This guide provides concepts and setup instructions for administrators and users.

A remote VS Code connection establishes a secure connection between your local VS Code and SageMaker spaces. This connection lets you:

Access SageMaker AI compute resources — Run code on scalable SageMaker AI infrastructure from your local environment

Maintain security boundaries — Work within the same security framework as SageMaker AI

Keep your familiar Visual Studio Code experience — Use compatible local extensions, themes, and configurations that support Microsoft Remote Development

Not all VS Code extensions are compatible with remote development. Extensions that require local GUI components, have architecture dependencies, or need specific client-server interactions may not work properly in the remote environment. Verify that your required extensions support Microsoft Remote Development before use.

VS Code version requirement

Operating system requirements

Local machine prerequisites

Instance requirements

Set up local Visual Studio Code

Remote connection — A secure tunnel between your local VS Code and a SageMaker space. This connection enables interactive development and code execution in VS Code using SageMaker AI compute resources.

Amazon SageMaker Studio space — A dedicated environment within Amazon SageMaker Studio where you can manage your storage and resources for your Studio applications.

Deep link — A button (direct URL) from the SageMaker UI that initiates a remote connection to your local IDE.

There are three main ways to connect your local VS Code to SageMaker spaces:

Deep link access — You can connect directly to a specific space by using the Open in VS Code button available in SageMaker AI. This uses URL patterns to establish a remote connection and open your SageMaker space in VS Code.

AWS Toolkit for Visual Studio Code — You can authenticate with AWS Toolkit for Visual Studio Code. This allows you to connect to spaces and open a remotely connected window from VS Code.

SSH terminal connection — You can connect via command line using SSH configuration.

Remote connection to Studio spaces supports:

VS Code version v1.90 or greater is required. We recommend using the latest stable version o

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ml.t3.medium
```

Example 2 (unknown):
```unknown
ml.c7i.large
```

Example 3 (unknown):
```unknown
ml.c6i.large
```

Example 4 (unknown):
```unknown
ml.c6id.large
```

---

## Launch Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-launch.html

**Contents:**
- Launch Amazon SageMaker Studio
        - Important
        - Important
        - Topics
- Prerequisites
- Launch from the Amazon SageMaker AI console
- Launch using the AWS CLI

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

This page's topics demonstrate how to launch Amazon SageMaker Studio from the Amazon SageMaker AI console and the AWS Command Line Interface (AWS CLI).

Launch from the Amazon SageMaker AI console

Launch using the AWS CLI

Before you begin, complete the following prerequisites:

Onboard to a SageMaker AI domain with Studio access. If you don't have permissions to set Studio as the default experience for your domain, contact your administrator. For more information, see Amazon SageMaker AI domain overview.

Update the AWS CLI by following the steps in Installing the current AWS CLI Version.

From your local machine, run aws configure and provide your AWS credentials. For information about AWS credentials, see Understanding and getting your AWS credentials.

Complete the following procedure to launch Studio from the Amazon SageMaker AI console.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

From the left navigation pane, choose Studio.

From the Studio landing page, select the domain and user profile for launching Studio.

To launch Studio, choose Launch personal Studio.

This section demonstrates how to launch Studio using the AWS CLI. The procedure to access Studio using the AWS CLI depends if the domain uses AWS Identity and Access Management (IAM) authentication or AWS IAM Identity Center authentication. You can use the AWS CLI to launch Studio by creating a presigned domain URL when your domain uses IAM authen

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200
```

Example 3 (unknown):
```unknown
user-profile-name
```

Example 4 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200 \
--landing-uri studio::
```

---

## SageMaker Studio image support policy

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-distribution.html

**Contents:**
- SageMaker Studio image support policy
        - Important
- Versioning, release cadence, and support policy
- Supported image versions
  - Supported major versions
  - CPU image minor versions
  - GPU image minor versions
  - Unsupported images
  - Frequently asked questions
        - Important

Currently, all packages in SageMaker Distribution images are licensed for use with Amazon SageMaker AI and do not require additional commercial licenses. However, this might be subject to change in the future, and we recommend reviewing the licensing terms regularly for any updates.

Amazon SageMaker Distribution is a set of Docker images available on SageMaker Studio that include popular frameworks for machine learning, data science, and visualization.

The images include deep learning frameworks like PyTorch, TensorFlow and Keras; popular Python packages like numpy, scikit-learn and pandas; and IDEs like JupyterLab and Code Editor, based on Code-OSS, Visual Studio Code - Open Source. The distribution contains the latest versions of all these packages such that they are mutually compatible.

This page details the support policy and availability for SageMaker Distribution Images on SageMaker Studio.

The table below outlines the release schedule for SageMaker Distribution Image versions and their planned support. AWS provides ongoing functionality and security updates for supported image versions. New minor versions are released for major versions for 12 months, and supported minor versions receive ongoing functionality and security patches. In some cases, an image version may need to be designated end of support earlier than originally planned if (a) security issues cannot be addressed while maintaining semantic versioning guidelines or (b) any of our major dependencies, like Python, reach end-of-life. AWS releases ad-hoc major or minor versions on an as-needed basis.

Each major version of the Amazon SageMaker Distribution is available for 18 months. During the first 12 months, new minor versions are released monthly. For the remaining 6 months, the existing minor versions continue to be supported.

The tables below list the supported SageMaker Distribution image versions, their planned end of support dates, and their availability on SageMaker Studio. For image versions where support ends sooner than the planned end of support date, the versions continue to be available on Studio until the designated availability date. You can continue using the image to launch applications for up to 90 days or until the availability date on Studio, whichever comes first. For more information about such cases, reach out to Support.

You can migrate to a newer supported version as soon as possible to ensure that you receive ongoing functionality and security updates. When

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
build_artifacts
```

---

## Blogs and whitepapers

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-emr-resources.html

**Contents:**
- Blogs and whitepapers

The following blogs use a case study of sentiment prediction for a movie review to illustrate the process of executing a complete machine learning workflow. This includes data preparation, monitoring Spark jobs, and training and deploying a ML model to get predictions directly from your Studio or Studio Classic notebook.

Create and manage Amazon EMR clusters from SageMaker Studio or Studio Classic to run interactive Spark and ML workloads.

To extend the use case to a cross-account configuration where SageMaker Studio or Studio Classic and your Amazon EMR cluster are deployed in separate AWS accounts, see Create and manage Amazon EMR clusters from SageMaker Studio or Studio Classic to run interactive Spark and ML workloads - Part 2.

A walkthrough of the configuration of Access Apache Livy using a Network Load Balancer on a Kerberos-enabled Amazon EMR cluster.

AWS whitepapers for SageMaker Studio or Studio Classic best practices.

---

## RStudio on Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/rstudio.html

**Contents:**
- RStudio on Amazon SageMaker AI
- Region availability
- RStudio components
- Differences from Posit Workbench

RStudio is an integrated development environment for R, with a console, syntax-highlighting editor that supports direct code execution, and tools for plotting, history, debugging and workspace management. Amazon SageMaker AI supports RStudio as a fully-managed integrated development environment (IDE) integrated with Amazon SageMaker AI domain through Posit Workbench. RStudio allows customers to create data science insights using an R environment. With RStudio integration, you can launch an RStudio environment in the domain to run your RStudio workflows on SageMaker AI resources. For more information about Posit Workbench, see the Posit website. This page gives information about important RStudio concepts.

SageMaker AI integrates RStudio through the creation of a RStudioServerPro app.

The following are supported by RStudio on SageMaker AI.

R developers use the RStudio IDE interface with popular developer tools from the R ecosystem. Users can launch new RStudio sessions, write R code, install dependencies from RStudio Package Manager, and publish Shiny apps using RStudio Connect.

R developers can quickly scale underlying compute resources to run large scale data processing and statistical analysis.

Platform administrators can set up user identities, authorization, networking, storage, and security for their data science teams through AWS IAM Identity Center and AWS Identity and Access Management integration. This includes connection to private Amazon Virtual Private Cloud (Amazon VPC) resources and internet-free mode with AWS PrivateLink.

Integration with AWS License Manager.

For information on the onboarding steps to create a domain with RStudio enabled, see Amazon SageMaker AI domain overview.

The following table gives information about the AWS Regions that RStudio on SageMaker AI is supported in.

US East (N. Virginia)

US West (N. California)

Asia Pacific (Mumbai)

Asia Pacific (Singapore)

Asia Pacific (Sydney)

South America (São Paulo)

RStudioServerPro: The RStudioServerPro app is a multiuser app that is a shared resource among all user profiles in the domain. Once an RStudio app is created in a domain, the admin can give permissions to users in the domain.

RStudio user: RStudio users are users within the domain that are authorized to use the RStudio license.

RStudio admin: An RStudio on Amazon SageMaker AI admin can access the RStudio administrative dashboard. RStudio on Amazon SageMaker AI admins differ from "stock" Posit Workbench admin

*[Content truncated]*

---

## SageMaker Autopilot

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development.html

**Contents:**
- SageMaker Autopilot
        - Important
        - Note
        - Note
        - Topics

As of November 30, 2023, Autopilot's UI is migrating to Amazon SageMaker Canvas as part of the updated Amazon SageMaker Studio experience. SageMaker Canvas provides analysts and citizen data scientists no-code capabilities for tasks such as data preparation, feature engineering, algorithm selection, training and tuning, inference, and more. Users can leverage built-in visualizations and what-if analysis to explore their data and different scenarios, with automated predictions enabling them to easily productionize their models. Canvas supports a variety of use cases, including computer vision, demand forecasting, intelligent search, and generative AI.

Users of Amazon SageMaker Studio Classic, the previous experience of Studio, can continue using the Autopilot UI in Studio Classic. Users with coding experience can continue using all API references in any supported SDK for technical implementation.

If you have been using Autopilot in Studio Classic until now and want to migrate to SageMaker Canvas, you might have to grant additional permissions to your user profile or IAM role so that you can create and use the SageMaker Canvas application. For more information, see (Optional) Migrate from Autopilot in Studio Classic to SageMaker Canvas.

All UI-related instructions in this guide pertain to Autopilot's standalone features before migrating to Amazon SageMaker Canvas. Users following these instructions should use Studio Classic.

Amazon SageMaker Autopilot is a feature set that simplifies and accelerates various stages of the machine learning workflow by automating the process of building and deploying machine learning models (AutoML). The following page explains key information about Amazon SageMaker Autopilot.

Autopilot performs the following key tasks that you can use on autopilot or with various degrees of human guidance:

Data analysis and preprocessing: Autopilot identifies your specific problem type, handles missing values, normalizes your data, selects features, and overall prepares the data for model training.

Model selection: Autopilot explores a variety of algorithms and uses a cross-validation resampling technique to generate metrics that evaluate the predictive quality of the algorithms based on predefined objective metrics.

Hyperparameter optimization: Autopilot automates the search for optimal hyperparameter configurations.

Model training and evaluation: Autopilot automates the process of training and evaluating various model candidates. It

*[Content truncated]*

---

## Perform common UI tasks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-common.html

**Contents:**
- Perform common UI tasks
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

The following sections describe how to perform common tasks in the Amazon SageMaker Studio UI. For an overview of the Studio user interface, see Amazon SageMaker Studio UI overview.

Set cookie preferences

Launch Studio following the steps in Launch Amazon SageMaker Studio.

At the bottom of the Studio user interface, choose Cookie Preferences.

Select the check box for each type of cookie that you want Amazon SageMaker AI to use.

Choose Save preferences.

Notifications give information about important changes to Studio, updates to applications, and issues to resolve.

Launch Studio following the steps in Launch Amazon SageMaker Studio.

On the top navigation bar, choose the Notifications icon ( ).

From the list of notifications, select the notification to get information about it.

We take your feedback seriously. We encourage you to provide feedback.

At the top navigation of Studio, choose Provide feedback.

Signing out of the Studio UI is different than closing the browser window. Signing out clears session data from the browser and deletes unsaved changes.

This same behavior also happens when the Studio session times out. This happens after 5 minutes.

Launch Studio following the steps in Launch Amazon SageMaker Studio.

Choose the User options icon ( ).

In the pop-up window, choose Sign out.

---

## Custom Images in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-byoi.html

**Contents:**
- Custom Images in Amazon SageMaker Studio Classic
        - Important
- Key terminology
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

A SageMaker image is a file that identifies the kernels, language packages, and other dependencies required to run a Jupyter notebook in Amazon SageMaker Studio Classic. These images are used to create an environment that you then run Jupyter notebooks from. Amazon SageMaker AI provides many built-in images for you to use. For the list of built-in images, see Amazon SageMaker Images Available for Use With Studio Classic Notebooks.

If you need different functionality, you can bring your own custom images to Studio Classic. You can create images and image versions, and attach image versions to your domain or shared space, using the SageMaker AI control panel, the AWS SDK for Python (Boto3), and the AWS Command Line Interface (AWS CLI). You can also create images and image versions using the SageMaker AI console, even if you haven't onboarded to a SageMaker AI domain. SageMaker AI provides sample Dockerfiles to use as a starting point for your custom SageMaker images in the SageMaker Studio Classic Custom Image Samples repository.

The following topics explain how to bring your own image using the SageMaker AI console or AWS CLI, then launch the image in Studio Classic. For a similar blog article, see Bringing your own R environment to Amazon SageMaker Studio Classic. For notebooks that show how to bring your own image for use in training and inference, see Amazon SageMaker Studio Classic Container Build CLI.

The following section defines key terms for bringing your own image to use with Studio Classic.

Dockerfile: A Dockerfile is a file that identifies the language packages and other dependencies for your Docker image.

Docker image: The Docker image is a built Dockerfile. This image is checked into Amazon ECR and serves as the basis of the SageMaker AI image.

SageMaker image: A SageMaker image is a holder for a set of SageMaker AI image versions based on Docker images. Each image version is immutable.

Image ver

*[Content truncated]*

---

## Connect Studio notebooks in a VPC to external resources

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-and-internet-access.html

**Contents:**
- Connect Studio notebooks in a VPC to external resources
- Default communication with the internet
- VPC only communication with the internet
  - Requirements to use VPC only mode
        - Note
        - Warning
        - Note
        - For more information

The following topic gives information about how to connect Studio Notebooks in a VPC to external resources.

By default, SageMaker Studio provides a network interface that allows communication with the internet through a VPC managed by SageMaker AI. Traffic to AWS services, like Amazon S3 and CloudWatch, goes through an internet gateway. Traffic that accesses the SageMaker API and SageMaker AI runtime also goes through an internet gateway. Traffic between the domain and Amazon EFS volume goes through the VPC that you identified when you onboarded to Studio or called the CreateDomain API. The following diagram shows the default configuration.

To stop SageMaker AI from providing internet access to your Studio notebooks, disable internet access by specifying the VPC only network access type. Specify this network access type when you onboard to Studio or call the CreateDomain API. As a result, you won't be able to run a Studio notebook unless:

your VPC has an interface endpoint to the SageMaker API and runtime, or a NAT gateway with internet access

your security groups allow outbound connections

The following diagram shows a configuration for using VPC-only mode.

When you choose VpcOnly, follow these steps:

You must use private subnets only. You cannot use public subnets in VpcOnly mode.

Ensure your subnets have the required number of IP addresses needed. The expected number of IP addresses needed per user can vary based on use case. We recommend between 2 and 4 IP addresses per user. The total IP address capacity for a Studio domain is the sum of available IP addresses for each subnet provided when the domain is created. Make sure that your IP address usage isn't more than the capacity supported by the number of subnets you provide. Additionally, using subnets distributed across many availability zones can help with IP address availability. For more information, see VPC and subnet sizing for IPv4.

You can configure only subnets with a default tenancy VPC in which your instance runs on shared hardware. For more information on the tenancy attribute for VPCs, see Dedicated Instances.

When using VpcOnly mode, you partly own the networking configuration for the domain. We recommend the security best practice of applying least-privilege permissions to the inbound and outbound access that security group rules provide. Overly permissive inbound rule configurations could allow users with access to the VPC to interact with the applications of other user profil

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
com.amazonaws.region.sagemaker.api
```

Example 2 (unknown):
```unknown
com.amazonaws.region.sagemaker.runtime
```

Example 3 (unknown):
```unknown
com.amazonaws.region.s3
```

Example 4 (unknown):
```unknown
com.amazonaws.region.servicecatalog
```

---

## Amazon SageMaker Studio Classic UI Overview

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-ui.html#studio-ui-home

**Contents:**
- Amazon SageMaker Studio Classic UI Overview
        - Important
        - Note
        - Topics
- Amazon SageMaker Studio Classic home page
- Amazon SageMaker Studio Classic layout
  - Left sidebar
  - Left navigation panel
  - Main working area
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic extends the capabilities of JupyterLab with custom resources that can speed up your Machine Learning (ML) process by harnessing the power of AWS compute. Previous users of JupyterLab will notice the similarity of the user interface. The most prominent additions are detailed in the following sections. For an overview of the original JupyterLab interface, see The JupyterLab Interface.

The following image shows the default view upon launching Amazon SageMaker Studio Classic. The left navigation panel displays all top-level categories of features, and a Amazon SageMaker Studio Classic home page is open in the main working area. Come back to this central point of orientation by choosing the Home icon ( ) at any time, then selecting the Home node in the navigation menu.

Try the Getting started notebook for an in-product hands-on guide on how to set up and get familiar with Amazon SageMaker Studio Classic features. On the Quick actions section of the Studio Classic Home page, choose Open the Getting started notebook.

This chapter is based on Studio Classic's updated user interface (UI) available on version v5.38.x and above on JupyterLab3.

To retrieve your version of Studio Classic UI, from the Studio Classic Launcher, open a System Terminal, then

Run conda activate studio

Run jupyter labextension list

Search for the version displayed after @amzn/sagemaker-ui version in the output.

For information about updating Amazon SageMaker Studio Classic, see Shut Down and Update Amazon SageMaker Studio Classic.

Amazon SageMaker Studio Classic home page

Amazon SageMaker Studio Classic layout

The Home page provides access to common tasks and workflows. In particular, it includes a list of Quick actions for common tasks such as Open Launcher to create notebooks and other resources and Import & prepare data visually to create a new flow in Data Wrangler.The Home page also offers tooltips on ke

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
conda activate studio
```

Example 2 (unknown):
```unknown
jupyter labextension list
```

Example 3 (unknown):
```unknown
@amzn/sagemaker-ui version
```

Example 4 (unknown):
```unknown
[user_name]
```

---

## Amazon SageMaker Studio Classic UI Overview

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-ui.html

**Contents:**
- Amazon SageMaker Studio Classic UI Overview
        - Important
        - Note
        - Topics
- Amazon SageMaker Studio Classic home page
- Amazon SageMaker Studio Classic layout
  - Left sidebar
  - Left navigation panel
  - Main working area
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic extends the capabilities of JupyterLab with custom resources that can speed up your Machine Learning (ML) process by harnessing the power of AWS compute. Previous users of JupyterLab will notice the similarity of the user interface. The most prominent additions are detailed in the following sections. For an overview of the original JupyterLab interface, see The JupyterLab Interface.

The following image shows the default view upon launching Amazon SageMaker Studio Classic. The left navigation panel displays all top-level categories of features, and a Amazon SageMaker Studio Classic home page is open in the main working area. Come back to this central point of orientation by choosing the Home icon ( ) at any time, then selecting the Home node in the navigation menu.

Try the Getting started notebook for an in-product hands-on guide on how to set up and get familiar with Amazon SageMaker Studio Classic features. On the Quick actions section of the Studio Classic Home page, choose Open the Getting started notebook.

This chapter is based on Studio Classic's updated user interface (UI) available on version v5.38.x and above on JupyterLab3.

To retrieve your version of Studio Classic UI, from the Studio Classic Launcher, open a System Terminal, then

Run conda activate studio

Run jupyter labextension list

Search for the version displayed after @amzn/sagemaker-ui version in the output.

For information about updating Amazon SageMaker Studio Classic, see Shut Down and Update Amazon SageMaker Studio Classic.

Amazon SageMaker Studio Classic home page

Amazon SageMaker Studio Classic layout

The Home page provides access to common tasks and workflows. In particular, it includes a list of Quick actions for common tasks such as Open Launcher to create notebooks and other resources and Import & prepare data visually to create a new flow in Data Wrangler.The Home page also offers tooltips on ke

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
conda activate studio
```

Example 2 (unknown):
```unknown
jupyter labextension list
```

Example 3 (unknown):
```unknown
@amzn/sagemaker-ui version
```

Example 4 (unknown):
```unknown
[user_name]
```

---

## Pipelines actions

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-studio.html

**Contents:**
- Pipelines actions
        - Topics

You can use either the Amazon SageMaker Pipelines Python SDK or the drag-and-drop visual designer in Amazon SageMaker Studio to author, view, edit, execute, and monitor your ML workflows.

The following screenshot shows the visual designer that you can use to create and manage your Amazon SageMaker Pipelines.

After your pipeline is deployed, you can view the directed acyclic graph (DAG) for your pipeline and manage your executions using Amazon SageMaker Studio. Using SageMaker Studio, you can get information about your current and historical pipelines, compare executions, see the DAG for your executions, get metadata information, and more. To learn about how to view pipelines from Studio, see View the details of a pipeline.

View the details of a pipeline

View the details of a pipeline run

Download a pipeline definition file

Access experiment data from a pipeline

Track the lineage of a pipeline

---

## View the details of a pipeline run

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-studio-view-execution.html

**Contents:**
- View the details of a pipeline run

You can review the details of a particular SageMaker AI pipeline run. This can help you:

Identify and resolve problems that may have occurred during the run, such as failed steps or unexpected errors.

Compare the results of different pipeline executions to understand how changes in input data or parameters impact the overall workflow.

Identify bottlenecks and opportunities for optimization.

To view the details of a pipeline run, complete the following steps based on whether you use Studio or Studio Classic.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, select Pipelines.

(Optional) To filter the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name to view details about the pipeline.

Choose the Executions tab.

Select the name of a pipeline execution to view. The pipeline graph for that execution appears.

Choose any of the pipeline steps in the graph to see step settings in the right sidebar.

Choose one of the following tabs to view more pipeline details:

Definition — The pipeline graph, including all steps.

Parameters – Includes the model approval status.

Details – The metadata associated with the pipeline, such as tags, the pipeline Amazon Resource Name (ARN), and role ARN. You can also edit the pipeline description from this page.

Sign in to Amazon SageMaker Studio Classic. For more information, see Launch Amazon SageMaker Studio Classic.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Pipelines from the menu.

To narrow the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name. The pipeline's Executions page opens.

In the Executions page, select an execution name to view details about the execution. The execution details tab opens and displays a graph of the steps in the pipeline.

To search for a step by name, type characters that match a step name in the search field. Use the resizing icons on the lower-right side of the graph to zoom in and out of the graph, fit the graph to screen, and expand the graph to full screen. To focus on a specific part of the graph, you can select a blank area of the graph and drag the graph to center on that area.

Choose one of the pipeline steps in the graph to see details about the step. In the preceding screenshot, a training step is chosen and displays the following tabs:

Input – The training 

*[Content truncated]*

---

## List Amazon EMR clusters from Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/discover-emr-clusters.html

**Contents:**
- List Amazon EMR clusters from Studio or Studio Classic

Data scientists and data engineers can discover, and then connect to Amazon EMR clusters from Studio. The Amazon EMR clusters may be in the same AWS account as Studio or in a different AWS account.

Before users can list or connect to clusters, administrators must have configured the necessary settings in the Studio environment. For information on how administrators can configure a Studio environment to allow discovering running Amazon EMR clusters, see Admin guide. If your administrator configured the cross-account discovery of Amazon EMR clusters, you can view a consolidated list of clusters. The list includes clusters from the AWS account used by Studio as well as clusters from remote accounts that you have been granted access to.

To view the list of available Amazon EMR clusters from within Studio:

In the Studio UI's left navigation menu, scroll down to EMR Clusters. This opens up a page listing the Amazon EMR clusters that you have access to.

The list displays clusters in the following stages: Bootstrapping, Starting Running, Waiting. You can narrow down the displayed clusters by their current status using the filter icon.

Choose a particular Running cluster you want to connect to, and then refer to Connect to an Amazon EMR cluster from SageMaker Studio or Studio Classic.

---

## Stop and delete your Studio running applications and spaces

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-running-stop.html

**Contents:**
- Stop and delete your Studio running applications and spaces
        - Important
        - Topics
- Stop your Amazon SageMaker Studio application
        - Note
        - Note
        - To delete your applications (Studio UI)
        - To stop your applications (SageMaker AI console)
        - Important
        - To get example-domain-id

The following page includes information and instructions on how to stop and delete unused Amazon SageMaker Studio resources to avoid unwanted additional costs. For the Studio resources you no longer you wish to use, you will need to both:

Stop the application: This stops both the application and deletes the instance that the application is running on. Once you stop an application you can start it back up again.

Delete the space: This deletes the Amazon EBS volume that was created for the application and instance.

If you delete the space, you will lose access to the data within that space. Do not delete the space unless you're sure that you want to.

For more information about the differences between Studio spaces and applications, see View your Studio running instances, applications, and spaces.

Stop your Amazon SageMaker Studio application

Delete a Studio space

To avoid additional charges from unused running applications, you must stop them. The following includes information on what stopping an application does and how to do it.

The following instructions uses the DeleteApp API to stop the application. This also stops the instance that the application is running on.

After you stop an application, you can start up the application again later.

When you stop an application, the files in the space will persist. You can run the application again and expect to have access to the same files that are stored in the space, as you did before deleting the application.

When you stop an application, the metadata for the application will be deleted within 24 hours. For more information, see the note in the CreationTime response element for the DescribeApp API.

If the service detects that an application is unhealthy, it assumes the AmazonSageMakerNotebooksServiceRolePolicy service linked role and deletes the application using the DeleteApp API.

The following tabs provide instructions to stop an application from your domain using the Studio UI, the SageMaker AI console, or the AWS CLI.

To view and stop all of your Studio running instances in one location, we recommend the Stop applications using the Studio UI workflow from the following options.

To stop your Studio applications using the Studio UI, use the following instructions.

Launch Studio. This process may differ depending on your setup. For information about launching Studio, see Launch Amazon SageMaker Studio.

From the left navigation pane, choose Running instances.

If the table on the page is emp

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreationTime
```

Example 2 (unknown):
```unknown
aws sagemaker delete-app \
--domain-id example-domain-id \
--region AWS Region \
--app-name default \
--app-type example-app-type \
--space-name example-space-name
```

Example 3 (unknown):
```unknown
example-domain-id
```

Example 4 (unknown):
```unknown
example-app-type
```

---

## Amazon SageMaker Experiments in Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html

**Contents:**
- Amazon SageMaker Experiments in Studio Classic
        - Important
- Migrate from Experiments Classic to Amazon SageMaker AI with MLflow

Experiment tracking using the SageMaker Experiments Python SDK is only available in Studio Classic. We recommend using the new Studio experience and creating experiments using the latest SageMaker AI integrations with MLflow. There is no MLflow UI integration with Studio Classic. If you want to use MLflow with Studio, you must launch the MLflow UI using the AWS CLI. For more information, see Launch the MLflow UI using the AWS CLI.

Amazon SageMaker Experiments Classic is a capability of Amazon SageMaker AI that lets you create, manage, analyze, and compare your machine learning experiments in Studio Classic. Use SageMaker Experiments to view, manage, analyze, and compare both custom experiments that you programmatically create and experiments automatically created from SageMaker AI jobs.

Experiments Classic automatically tracks the inputs, parameters, configurations, and results of your iterations as runs. You can assign, group, and organize these runs into experiments. SageMaker Experiments is integrated with Amazon SageMaker Studio Classic, providing a visual interface to browse your active and past experiments, compare runs on key performance metrics, and identify the best performing models. SageMaker Experiments tracks all of the steps and artifacts that went into creating a model, and you can quickly revisit the origins of a model when you are troubleshooting issues in production, or auditing your models for compliance verifications.

Past experiments created using Experiments Classic are still available to view in Studio Classic. If you want to maintain and use past experiment code with MLflow, you must update your training code to use the MLflow SDK and run the training experiments again. For more information on getting started with the MLflow SDK and the AWS MLflow plugin, see Integrate MLflow with your environment.

---

## AWS Managed Policies for SageMaker Notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-notebooks.html

**Contents:**
- AWS Managed Policies for SageMaker Notebooks
        - Topics
- AWS managed policy: AmazonSageMakerNotebooksServiceRolePolicy
- Amazon SageMaker AI updates to SageMaker AI Notebooks managed policies

These AWS managed policies add permissions required to use SageMaker Notebooks. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerNotebooksServiceRolePolicy

Amazon SageMaker AI updates to SageMaker AI Notebooks managed policies

This AWS managed policy grants permissions commonly needed to use Amazon SageMaker Notebooks. The policy is added to the AWSServiceRoleForAmazonSageMakerNotebooks that is created when you onboard to Amazon SageMaker Studio Classic. For more information on service-linked roles, see Service-linked roles. For more information, see AmazonSageMakerNotebooksServiceRolePolicy

This policy includes the following permissions.

elasticfilesystem – Allows principals to create and delete Amazon Elastic File System (EFS) file systems, access points, and mount targets. These are limited to those tagged with the key ManagedByAmazonSageMakerResource. Allows principals to describe all EFS file systems, access points, and mount targets. Allows principals to create or overwrite tags for EFS access points and mount targets.

ec2 – Allows principals to create network interfaces and security groups for Amazon Elastic Compute Cloud (EC2) instances. Also allows principals to create and overwrite tags for these resources.

sso – Allows principals to add and delete managed application instances to AWS IAM Identity Center.

sagemaker – Allows principals to create and read SageMaker AI user profiles and SageMaker AI spaces; delete SageMaker AI spaces and SageMaker AI apps; and add and list tags.

fsx – Allows principals to describe Amazon FSx for Lustre file system, and use the metadata to mount it on notebook.

View details about updates to AWS managed policies for Amazon SageMaker AI since this service began tracking these changes.

AmazonSageMakerNotebooksServiceRolePolicy - Update to an existing policy

Add fsx:DescribeFileSystems permission.

AmazonSageMakerNotebooksServiceRolePolicy - Update to an existing policy

Add sagemaker:DeleteApp permission.

AmazonSageMakerNotebooksServiceRolePolicy - Update to an existing policy

Add sagemaker:CreateSpace, sagemaker:DescribeSpace, sagemaker:DeleteSpace, sagemaker:ListTags, and sagemaker:AddTags permissions.

AmazonSageMakerNotebooksServiceRolePolicy - Update to an existing policy

Add elasticfilesystem:TagResource permission.

AmazonSageMakerNotebooksServiceRolePolicy - Update to an existing policy

Add ela

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AWSServiceRoleForAmazonSageMakerNotebooks
```

Example 2 (unknown):
```unknown
elasticfilesystem
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AllowFSxDescribe",
            "Effect": "Allow",
            "Action": [
                "fsx:DescribeFileSystems"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "${aws:PrincipalAccount}"
                }
            }
        },
        {
            "Sid": "AllowSageMakerDeleteApp",
            "Effect": "Allow",
            "Action": [
                "sagemaker:DeleteApp"
            ],
            "Resource": 
...
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AllowFSxDescribe",
            "Effect": "Allow",
            "Action": [
                "fsx:DescribeFileSystems"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "${aws:PrincipalAccount}"
                }
            }
        },
        {
            "Sid": "AllowSageMakerDeleteApp",
            "Effect": "Allow",
            "Action": [
                "sagemaker:DeleteApp"
            ],
            "Resource": 
...
```

---

## (Optional) Migrate data from Studio Classic to Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-data.html

**Contents:**
- (Optional) Migrate data from Studio Classic to Studio
- Manually migrate all of your data from Studio Classic
  - Prerequisites
  - Choosing an approach
        - Note
- Migrate data flows from Data Wrangler
  - Prerequisites
  - One-click migration method
        - Warning
  - Manual migration method

Studio Classic and Studio use two different types of storage volumes. Studio Classic uses a single Amazon Elastic File System (Amazon EFS) volume to store data across all users and shared spaces in the domain. In Studio, each space gets its own Amazon Elastic Block Store (Amazon EBS) volume. When you update the default experience of an existing domain, SageMaker AI automatically mounts a folder in an Amazon EFS volume for each user in a domain. As a result, users are able to access files from Studio Classic in their Studio applications. For more information, see Amazon EFS auto-mounting in Studio.

You can also opt out of Amazon EFS auto-mounting and manually migrate the data to give users access to files from Studio Classic in Studio applications. To accomplish this, you must transfer the files from the user home directories to the Amazon EBS volumes associated with those spaces. The following section gives information about this workflow. For more information about opting out of Amazon EFS auto-mounting, see Opt out of Amazon EFS auto-mounting.

The following section describes how to migrate all of the data from your Studio Classic storage volume to the new Studio experience.

When manually migrating a user's data, code, and artifacts from Studio Classic to Studio, we recommend one of the following approaches:

Using a custom Amazon EFS volume

Using Amazon Simple Storage Service (Amazon S3)

If you used Amazon SageMaker Data Wrangler in Studio Classic and want to migrate your data flow files, then choose one of the following options for migration:

If you want to migrate all of the data from your Studio Classic storage volume, including your data flow files, go to Manually migrate all of your data from Studio Classic and complete the section Use Amazon S3 to migrate data. Then, skip to the Import the flow files into Canvas section.

If you only want to migrate your data flow files and no other data from your Studio Classic storage volume, skip to the Migrate data flows from Data Wrangler section.

Before running these steps, complete the prerequisites in Complete prerequisites to migrate the Studio experience. You must also complete the steps in Migrate the UI from Studio Classic to Studio.

Consider the following when choosing an approach to migrate your Studio Classic data.

Pros and cons of using a custom Amazon EFS volume

In this approach, you use an Amazon EFS-to-Amazon EFS AWS DataSync task (one time or cadence) to copy data, then mount the targe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export SOURCE_DOMAIN_ID="domain-id"
export AWS_REGION="region"

export TARGET_EFS=$(aws efs create-file-system --performance-mode generalPurpose --throughput-mode bursting --encrypted --region $REGION | jq -r '.FileSystemId')

echo "Target EFS volume Created: $TARGET_EFS"
```

Example 2 (unknown):
```unknown
export SOURCE_EFS=$(aws sagemaker describe-domain --domain-id $SOURCE_DOMAIN_ID | jq -r '.HomeEfsFileSystemId')
export VPC_ID=$(aws sagemaker describe-domain --domain-id $SOURCE_DOMAIN_ID | jq -r '.VpcId')

echo "EFS managed by SageMaker: $SOURCE_EFS | VPC: $VPC_ID"
```

Example 3 (unknown):
```unknown
export EFS_VPC_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].VpcId")
export EFS_AZ_NAME=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].AvailabilityZoneName")
export EFS_AZ_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].AvailabilityZoneId")
export EFS_SUBNET_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].SubnetId")
export EFS_MOUNT_TARG_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[
...
```

Example 4 (unknown):
```unknown
export SOURCE_EFS_ARN=$(aws efs describe-file-systems --file-system-id $SOURCE_EFS | jq -r ".FileSystems[0].FileSystemArn")
export TARGET_EFS_ARN=$(aws efs describe-file-systems --file-system-id $TARGET_EFS | jq -r ".FileSystems[0].FileSystemArn")
export EFS_SUBNET_ID_ARN=$(aws ec2 describe-subnets --subnet-ids $EFS_SUBNET_ID | jq -r ".Subnets[0].SubnetArn")
export ACCOUNT_ID=$(aws ec2 describe-security-groups --group-id $EFS_SG_IDS | jq -r ".SecurityGroups[0].OwnerId")
export EFS_SG_ID_ARN=arn:aws:ec2:$REGION:$ACCOUNT_ID:security-group/$EFS_SG_IDS

export SOURCE_LOCATION_ARN=$(aws datasync cr
...
```

---

## Amazon SageMaker Debugger Insights dashboard controller

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-on-studio-insights-controllers.html

**Contents:**
- Amazon SageMaker Debugger Insights dashboard controller
        - Note
        - Important
- SageMaker Debugger Insights controller UI
        - Note

There are different components of the Debugger controller for monitoring and profiling. In this guide, you learn about the Debugger controller components.

The SageMaker Debugger Insights dashboard runs a Studio Classic app on an ml.m5.4xlarge instance to process and render the visualizations. Each SageMaker Debugger Insights tab runs one Studio Classic kernel session. Multiple kernel sessions for multiple SageMaker Debugger Insights tabs run on the single instance. When you close a SageMaker Debugger Insights tab, the corresponding kernel session is also closed. The Studio Classic app remains active and accrues charges for the ml.m5.4xlarge instance usage. For information about pricing, see the Amazon SageMaker Pricing page.

When you are done using the SageMaker Debugger Insights dashboard, shut down the ml.m5.4xlarge instance to avoid accruing charges. For instructions on how to shut down the instance, see Shut down the Amazon SageMaker Debugger Insights instance.

Using the Debugger controller located at the upper-left corner of the Insights dashboard, you can refresh the dashboard, configure or update Debugger settings for monitoring system metrics, stop a training job, and download a Debugger profiling report.

If you want to manually refresh the dashboard, choose the refresh button (the round arrow at the upper-left corner) as shown in the preceding screenshot.

The Monitoring toggle button is on by default for any SageMaker training job initiated using the SageMaker Python SDK. If not activated, you can use the toggle button to start monitoring. During monitoring, Debugger only collects resource utilization metrics to detect computational problems such as CPU bottlenecks and GPU underutilization. For a complete list of resource utilization problems that Debugger monitors, see Debugger built-in rules for profiling hardware system resource utilization (system metrics).

The Configure monitoring button opens a pop-up window that you can use to set or update the data collection frequency and the S3 path to save the data.

You can specify values for the following fields.

S3 bucket URI: Specify the base S3 bucket URI.

Collect monitoring data every: Select a time interval to collect system metrics. You can choose one of the monitoring intervals from the dropdown list. Available intervals are 100 milliseconds, 200 milliseconds, 500 milliseconds (default), 1 second, 5 seconds, and 1 minute.

If you choose one of the lower time intervals, you increase the 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ml.m5.4xlarge
```

Example 2 (unknown):
```unknown
ml.m5.4xlarge
```

Example 3 (unknown):
```unknown
ml.m5.4xlarge
```

---

## Manage Resources for Amazon SageMaker Studio Classic Notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-run-and-manage.html

**Contents:**
- Manage Resources for Amazon SageMaker Studio Classic Notebooks
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can change the instance type, and SageMaker image and kernel from within an Amazon SageMaker Studio Classic notebook. To create a custom kernel to use with your notebooks, see Custom Images in Amazon SageMaker Studio Classic.

Change the Instance Type for an Amazon SageMaker Studio Classic Notebook

Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook

Shut Down Resources from Amazon SageMaker Studio Classic

---

## How Are Amazon SageMaker Studio Classic Notebooks Different from Notebook Instances?

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-comparison.html

**Contents:**
- How Are Amazon SageMaker Studio Classic Notebooks Different from Notebook Instances?
        - Important
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

When you're starting a new notebook, we recommend that you create the notebook in Amazon SageMaker Studio Classic instead of launching a notebook instance from the Amazon SageMaker AI console. There are many benefits to using a Studio Classic notebook, including the following:

Faster: Starting a Studio Classic notebook is faster than launching an instance-based notebook. Typically, it is 5-10 times faster than instance-based notebooks.

Easy notebook sharing: Notebook sharing is an integrated feature in Studio Classic. Users can generate a shareable link that reproduces the notebook code and also the SageMaker image required to execute it, in just a few clicks.

Latest Python SDK: Studio Classic notebooks come pre-installed with the latest Amazon SageMaker Python SDK.

Access all Studio Classic features: Studio Classic notebooks are accessed from within Studio Classic. This enables you to build, train, debug, track, and monitor your models without leaving Studio Classic.

Persistent user directories: Each member of a Studio team gets their own home directory to store their notebooks and other files. The directory is automatically mounted onto all instances and kernels as they're started, so their notebooks and other files are always available. The home directories are stored in Amazon Elastic File System (Amazon EFS) so that you can access them from other services.

Direct access: When using IAM Identity Center, you use your IAM Identity Center credentials through a unique URL to directly access Studio Classic. You don't have to interact with the AWS Management Console to run your notebooks.

Optimized images: Studio Classic notebooks are equipped with a set of predefined SageMaker image settings to get you started faster.

Studio Classic notebooks don't support local mode. However, you can use a notebook instance to train a sample of your dataset locally, and then use the same code in a Studio Classic notebook to

*[Content truncated]*

---

## Use foundation models in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models-use-studio-updated.html

**Contents:**
- Use foundation models in Studio
        - Important
        - Topics

Amazon SageMaker Studio allows you to fine-tune, deploy, and evaluate both publicly available and proprietary JumpStart foundation models directly through the Studio UI.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

To get started, navigate to the JumpStart landing page in Amazon SageMaker Studio. You can access it from the Home page or the left-side panel menu. On the JumpStart landing page, you can explore model hubs from providers of both publicly available and proprietary models, and search for models.

Within each model hub, you can sort models by Most likes, Most downloads, Recently updated, or filter them by task. Choose a model to view its detail card. On the model detail card, you can choose to Fine-tune, Deploy, or Evaluate the model, depending on the available option. Note that not all models are available for fine-tuning or evaluation.

For more information on getting started with Amazon SageMaker Studio, see Amazon SageMaker Studio.

Fine-tune a model in Studio

Deploy a model in Studio

Evaluate a model in Studio

Use your SageMaker JumpStart Models in Amazon Bedrock

---

## Using Amazon SageMaker Feature Store in the console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-use-with-studio.html#feature-store-update-feature-group-studio

**Contents:**
- Using Amazon SageMaker Feature Store in the console
        - Important
        - Topics
- Create a feature group from the console
- View feature group details from the console
- Update a feature group from the console
- View pipeline executions from the console
- View lineage from the console

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

You can use Amazon SageMaker Feature Store on the console to create, view, update, and monitor your feature groups. Monitoring in this guide includes viewing pipeline executions and lineage of your feature groups. This guide provides instructions on how to achieve these tasks from the console.

For Feature Store examples and resources using the Amazon SageMaker APIs and AWS SDK for Python (Boto3), see Amazon SageMaker Feature Store resources.

Create a feature group from the console

View feature group details from the console

Update a feature group from the console

View pipeline executions from the console

View lineage from the console

The create feature group process has four steps:

Enter feature group information.

Enter feature definitions.

Enter required features.

Enter feature group tags.

Consider which of the following options fits your use case:

Create an online store, an offline store, or both. For more information about the differences between online and offline stores, see Feature Store concepts.

Use a default AWS Key Management Service key or your own KMS key. The default key is AWS KMS key (SSE-KMS). You can reduce AWS KMS request costs by configuring use of Amazon S3 Bucket Keys on the offline store Amazon S3 bucket. The Amazon S3 Bucket Key must be enabled before using the bucket for your feature groups. For more information about reducing the cost by using Amazon S3 Bucket Keys, see Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys.

You can use the same key for both online and offline stores, or have a unique key for each. For more information about AWS KMS, see AWS Key Management Service.

If you create an offline store:

Decide if you want to create an Amazon S3 bucket or use an existing one. When usin

*[Content truncated]*

---

## Share and Use an Amazon SageMaker Studio Classic Notebook

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-sharing.html

**Contents:**
- Share and Use an Amazon SageMaker Studio Classic Notebook
        - Important
        - Important
        - Topics
- Share a Notebook
        - To share a notebook
        - Note
- Use a Shared Notebook
- Shared spaces and realtime collaboration

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can share your Amazon SageMaker Studio Classic notebooks with your colleagues. The shared notebook is a copy. After you share your notebook, any changes you make to your original notebook aren't reflected in the shared notebook and any changes your colleague's make in their shared copies of the notebook aren't reflected in your original notebook. If you want to share your latest version, you must create a new snapshot and then share it.

Use a Shared Notebook

Shared spaces and realtime collaboration

The following screenshot shows the menu from a Studio Classic notebook.

In the upper-right corner of the notebook, choose Share.

(Optional) In Create shareable snapshot, choose any of the following items:

Include Git repo information – Includes a link to the Git repository that contains the notebook. This enables you and your colleague to collaborate and contribute to the same Git repository.

Include output – Includes all notebook output that has been saved.

If you're an user in IAM Identity Center and you don't see these options, your IAM Identity Center administrator probably disabled the feature. Contact your administrator.

After the snapshot is created, choose Copy link and then choos

*[Content truncated]*

---

## API Reference guide for Autopilot

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-reference.html

**Contents:**
- API Reference guide for Autopilot
- AutoML API Actions
        - Note
- AutoML API Data Types

This section provides a subset of the HTTP service REST APIs for creating and managing Amazon SageMaker Autopilot resources (AutoML jobs) programmatically.

If your language of choice is Python, you can refer to AWS SDK for Python (Boto3) or the AutoMLV2 object of the Amazon SageMaker Python SDK directly.

This list details the operations available in the Reference API to manage AutoML jobs programmatically.

ListCandidatesForAutoMLJob

CreateAutoMLJobV2 and DescribeAutoMLJobV2 are new versions of CreateAutoMLJob and DescribeAutoMLJob which offer backward compatibility.

We recommend using the CreateAutoMLJobV2. CreateAutoMLJobV2 can manage tabular problem types identical to those of its previous version CreateAutoMLJob, as well as non-tabular problem types such as image or text classification, or time-series forecasting.

Find guidelines about how to migrate a CreateAutoMLJob to CreateAutoMLJobV2 in Migrate a CreateAutoMLJob to CreateAutoMLJobV2.

This list details the API AutoML objects used by the actions above as inbound requests or outbound responses.

AutoMLAlgorithmConfig

AutoMLCandidateGenerationConfig

AutoMLContainerDefinition

AutoMLDataSplitConfig

AutoMLInferenceContainerDefinitions

AutoMLJobCompletionCriteria

AutoMLJobInputDataConfig

AutoMLJobStepMetadata

AutoMLOutputDataConfig

AutoMLProblemTypeConfig

AutoMLJobCompletionCriteria

AutoMLOutputDataConfig

AutoMLPartialFailureReason

AutoMLProblemTypeConfig

AutoMLProblemTypeResolvedAttributes

AutoMLResolvedAttributes

CandidateArtifactLocations

CandidateGenerationConfig

FinalAutoMLJobObjectiveMetric

HolidayConfigAttributes

ImageClassificationJobConfig

TabularResolvedAttributes

TextGenerationJobConfig

TextGenerationResolvedAttribute

TimeSeriesForecastingJobConfig

TimeSeriesTransformations

TuningJobCompletionCriteria

**Examples:**

Example 1 (unknown):
```unknown
CreateAutoMLJob
```

Example 2 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 3 (unknown):
```unknown
DescribeAutoMLJob
```

Example 4 (unknown):
```unknown
DescribeAutoMLJobV2
```

---

## Access experiment data from a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-studio-experiments.html

**Contents:**
- Access experiment data from a pipeline
        - Note
        - Note

SageMaker Experiments is a feature provided in Studio Classic only.

When you create a pipeline and specify pipeline_experiment_config, Pipelines creates the following SageMaker Experiments entities by default if they don't exist:

An experiment for the pipeline

A run group for every execution of the pipeline

A run for each SageMaker AI job created in a pipeline step

For information about how experiments are integrated with pipelines, see Amazon SageMaker Experiments Integration. For more information about SageMaker Experiments, see Amazon SageMaker Experiments in Studio Classic.

You can get to the list of runs associated with a pipeline from either the pipeline executions list or the experiments list.

To view the runs list from the pipeline executions list

To view the pipeline executions list, follow the first five steps in the Studio Classic tab of View the details of a pipeline.

On the top right of the screen, choose the Filter icon ( ).

Choose Experiment. If experiment integration wasn't deactivated when the pipeline was created, the experiment name is displayed in the executions list.

Experiments integration was introduced in v2.41.0 of the Amazon SageMaker Python SDK. Pipelines created with an earlier version of the SDK aren't integrated with experiments by default.

Select the experiment of your choice to view run groups and runs related to that experiment.

To view the runs list from the experiments list

In the left sidebar of Studio Classic, choose the Home icon ( ).

Select Experiments from the menu.

Use search bar or Filter icon ( ) to filter the list to experiments created by a pipeline.

Open an experiment name and view a list of runs created by the pipeline.

---

## SageMaker JumpStart pretrained models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html#jumpstart-models

**Contents:**
- SageMaker JumpStart pretrained models
- Open and use JumpStart in Studio
        - Important
  - Open JumpStart in Studio
        - Important
  - Use JumpStart in Studio
  - Manage JumpStart in Studio
- Open and use JumpStart in Studio Classic
        - Important
  - Open JumpStart in Studio Classic

Amazon SageMaker JumpStart provides pretrained, open-source models for a wide range of problem types to help you get started with machine learning. You can incrementally train and tune these models before deployment. JumpStart also provides solution templates that set up infrastructure for common use cases, and executable example notebooks for machine learning with SageMaker AI.

You can deploy, fine-tune, and evaluate pretrained models from popular models hubs through the JumpStart landing page in the updated Studio experience.

You can also access pretrained models, solution templates, and examples through the JumpStart landing page in Amazon SageMaker Studio Classic.

The following steps show how to access JumpStart models using Amazon SageMaker Studio and Amazon SageMaker Studio Classic.

You can also access JumpStart models using the SageMaker Python SDK. For information about how to use JumpStart models programmatically, see Use SageMaker JumpStart Algorithms with Pretrained Models.

The following sections give information on how to open, use, and manage JumpStart from the Studio UI.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

In Amazon SageMaker Studio, open the JumpStart landing page either through the Home page or the Home menu on the left-side panel. This opens the SageMaker JumpStart landing page where you can explore model hubs and search for models.

From the Home page, choose JumpStart in the Prebuilt and automated solutions pane.

From the Home menu in the left panel, navigate to the SageMaker JumpStart node.

For more information on getting started with Amazon SageMaker Studio, see Amazon SageMaker Studio.

Before downloading or using third-party content: You are responsible for reviewing and complying with any applicable license terms and making sure that they are acceptable for your use case.

From the SageMaker JumpStart landing page in Studio, you can explore model hubs from providers of both proprietary and publicly available models.

You can find specific hubs or models using the search bar. Within each model hub, you can search directly for models, sort by provided attributes, or filter based on a list of provided model tasks.

Choose a model to see its model detail card. In the upper right

*[Content truncated]*

---

## Get Started with Amazon SageMaker Studio Classic Notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-get-started.html

**Contents:**
- Get Started with Amazon SageMaker Studio Classic Notebooks
        - Important
- Launch Amazon SageMaker AI
- Next Steps

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

To get started, you or your organization's administrator need to complete the SageMaker AI domain onboarding process. For more information, see Amazon SageMaker AI domain overview.

You can access a Studio Classic notebook in any of the following ways:

You receive an email invitation to access Studio Classic through your organization's IAM Identity Center, which includes a direct link to login to Studio Classic without having to use the Amazon SageMaker AI console. You can proceed to the Next Steps.

You receive a link to a shared Studio Classic notebook, which includes a direct link to log in to Studio Classic without having to use the SageMaker AI console. You can proceed to the Next Steps.

You onboard to a domain and then log in to the SageMaker AI console. For more information, see Amazon SageMaker AI domain overview.

Complete the steps in Launch Amazon SageMaker Studio Classic to launch Studio Classic.

Now that you're in Studio Classic, you can try any of the following options:

To create a Studio Classic notebook or explore Studio Classic end-to-end tutorial notebooks – See Amazon SageMaker Studio Classic Tour in the next section.

To familiarize yourself with the Studio Classic interface – See Amazon SageMaker Studio Classic UI Overview or try the Getting started notebook by selecting Open the Getting started notebook in the Quick actions section of the Studio Classic Home page.

---

## Stop a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-studio-stop.html

**Contents:**
- Stop a pipeline

You can stop a pipeline run in the Amazon SageMaker Studio console.

To stop a pipeline execution in the Amazon SageMaker Studio console, complete the following steps based on whether you use Studio or Studio Classic.

In the left navigation pane, select Pipelines.

(Optional) To filter the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name.

Choose the Executions tab.

Select the execution to stop.

Choose Stop. To resume the execution from where it was stopped, choose Resume

Sign in to Amazon SageMaker Studio Classic. For more information, see Launch Amazon SageMaker Studio Classic.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Pipelines from the menu.

To narrow the list of pipelines by name, enter a full or partial pipeline name in the search field.

To stop a pipeline run, choose View details on the status banner of the pipeline, and then choose Stop. To resume the execution from where it was stopped, choose Resume.

---

## Troubleshooting

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-studio-troubleshoot.html

**Contents:**
- Troubleshooting
        - Topics
- Tasks tab
- Metrics tab

The following section lists troubleshooting solutions for HyperPod in Studio.

If you get Custom Resource Definition (CRD) is not configured on the cluster while in the Tasks tab.

Grant EKSAdminViewPolicy and ClusterAccessRole policies to your domain execution role.

For information on how to add tags to your execution role, see Tag IAM roles.

To learn how to attach policies to an IAM user or group, see Adding and removing IAM identity permissions.

If the tasks grid for Slurm metrics doesn’t stop loading in the Tasks tab.

Ensure that RunAs enabled in your AWS Session Manager preferences and the role you are using has the SSMSessionRunAs tag attached.

To enable RunAs, navigate to the Preference tab in the Systems Manager console.

Turn on Run As support for Linux and macOS managed nodes

For restricted task view in Studio for EKS clusters:

If your execution role doesn’t have permissions to list namespaces for EKS clusters.

See Restrict task view in Studio for EKS clusters.

If users are experiencing issues with access for EKS clusters.

Verify RBAC is enabled by running the following AWS CLI command.

This should return rbac.authorization.k8s.io/v1.

Check if the ClusterRole and ClusterRoleBinding exist by running the following commands.

Verify user group membership. Ensure the user is correctly assigned to the pods-events-crd-cluster-level group in your identity provider or IAM.

If user can't see any resources.

Verify group membership and ensure the ClusterRoleBinding is correctly applied.

If users can see resources in all namespaces.

If namespace restriction is required, consider using Role and RoleBinding instead of ClusterRole and ClusterRoleBinding.

If configuration appears correct, but permissions aren't applied.

Check if there are any NetworkPolicies or PodSecurityPolicies interfering with access.

If there are no Amazon CloudWatch metrics are displayed in the Metrics tab.

The Metrics section of HyperPod cluster details uses CloudWatch to fetch the data. In order to see the metrics in this section, you need to have enabled Cluster and task observability. Contact your administrator to configure metrics.

**Examples:**

Example 1 (unknown):
```unknown
Custom Resource Definition (CRD) is not configured on the
     cluster
```

Example 2 (unknown):
```unknown
EKSAdminViewPolicy
```

Example 3 (unknown):
```unknown
ClusterAccessRole
```

Example 4 (unknown):
```unknown
SSMSessionRunAs
```

---

## Data preparation using AWS Glue interactive sessions

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-glue.html

**Contents:**
- Data preparation using AWS Glue interactive sessions

AWS Glue interactive sessions is a serverless service that you can enlist to collect, transform, clean, and prepare data for storage in your data lakes and data pipelines. AWS Glue interactive sessions provides an on-demand, serverless Apache Spark runtime environment that you can initialize in seconds on a dedicated Data Processing Unit (DPU) without having to provision and manage complex compute cluster infrastructure. After initialization, you can browse the AWS Glue data catalog, run large queries, access data governed by AWS Lake Formation, and interactively analyze and prepare data using Spark, right in your Studio or Studio Classic notebooks. You can then use the prepared data to train, tune, and deploy models using the purpose-built ML tools within SageMaker Studio or Studio Classic. You should consider AWS Glue Interactive Sessions for your data preparation workloads when you want a serverless Spark service with moderate control of configurability and flexibility.

You can initiate an AWS Glue interactive session by starting a JupyterLab notebook in Studio or Studio Classic. When starting your notebook, choose the built-in Glue PySpark and Ray or Glue Spark kernel. This automatically starts an interactive, serverless Spark session. You do not need to provision or manage any compute cluster or infrastructure. After initialization, you can explore and interact with your data from within your Studio or Studio Classic notebooks.

Before starting your AWS Glue interactive session in Studio or Studio Classic, you need to set the appropriate roles and policies. Additionally, you may need to provide access to additional resources, such as a storage Amazon S3 bucket. For more information about required IAM policies, see Permissions for AWS Glue interactive sessions in Studio or Studio Classic.

Studio and Studio Classic provide a default configuration for your AWS Glue interactive session, however, you can use AWS Glue’s full catalog of Jupyter magic commands to further customize your environment. For information about the default and additional Jupyter magics that you can use in your AWS Glue interactive session, see Configure your AWS Glue interactive session in Studio or Studio Classic.

For Studio Classic users initiating an AWS Glue interactive session, they can select from the following images and kernels:

Images: SparkAnalytics 1.0, SparkAnalytics 2.0

Kernel: Glue Python [PySpark and Ray] and Glue Spark

For Studio users, use the default SageMaker

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Glue
            PySpark and Ray
```

Example 2 (unknown):
```unknown
SparkAnalytics 1.0
```

Example 3 (unknown):
```unknown
SparkAnalytics
                        2.0
```

Example 4 (unknown):
```unknown
Glue Python [PySpark and Ray]
```

---

## Troubleshoot

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-trouble-shooting.html

**Contents:**
- Troubleshoot
- Troubleshooting issues with Amazon EMR
- Troubleshooting with Salesforce
  - Lifecycle configuration error
        - To create a configuration file
  - Unable to access Salesforce Data Cloud from the Data Wrangler flow
  - Blank page showing redirect_uri_mismatch
        - Note
  - Shared spaces
  - OAuth Redirect Error

If an issue arises when using Amazon SageMaker Data Wrangler, we recommend you do the following:

If an error message is provided, read the message and resolve the issue it reports if possible.

Make sure the IAM role of your Studio Classic user has the required permissions to perform the action. For more information, see Security and Permissions.

If the issue occurs when you are trying to import from another AWS service, such as Amazon Redshift or Athena, make sure that you have configured the necessary permissions and resources to perform the data import. For more information, see Import.

If you're still having issues, choose Get help at the top right of your screen to reach out to the Data Wrangler team. For more information, see the following images.

As a last resort, you can try restarting the kernel on which Data Wrangler is running.

Save and exit the .flow file for which you want to restart the kernel.

Select the Running Terminals and Kernels icon, as shown in the following image.

Select the Stop icon to the right of the .flow file for which you want to terminate the kernel, as shown in the following image.

Reopen the .flow file on which you were working.

Use the following information to help you troubleshoot errors that might come up when you're using Amazon EMR.

Connection failure – If the connection fails with the following message The IP address of the EMR cluster isn't private error message, your Amazon EMR cluster might not have been launched in a private subnet. As a security best practice, Data Wrangler only supports connecting to private Amazon EMR clusters. Choose a private EC2 subnet you launch an EMR cluster.

Connection hanging and timing out – The issue is most likely due to a network connectivity issue. After you start connecting to the cluster, the screen doesn't refresh. After about 2 minutes, you might see the following error JdbcAddConnectionError: An error occurred when trying to connect to presto: xxx: Connect to xxx failed: Connection timed out (Connection timed out) will display on top of the screen..

The errors might have two root causes:

The Amazon EMR and Amazon SageMaker Studio Classic are in different VPCs. We recommend launching both Amazon EMR and Studio Classic in the same VPC. You can also use VPC peering. For more information, see What is VPC peering?.

The Amazon EMR master security group lacks the inbound traffic rule for the security group of Amazon SageMaker Studio Classic on the port used for Presto. 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
The IP address of the EMR cluster isn't private error message
```

Example 2 (unknown):
```unknown
JdbcAddConnectionError: An error occurred when trying to connect to presto: xxx: Connect to xxx failed: Connection timed out (Connection timed out) will display on top of the screen.
```

Example 3 (unknown):
```unknown
                    Data Wrangler couldn't create a connection to {connection_source} successfully.
                    Try connecting to {connection_source} again. For more information, see Troubleshoot.
                    If you’re still experiencing issues, contact support.
```

Example 4 (unknown):
```unknown
hdfs dfs -mkdir /user/USERNAME
hdfs dfs -chown USERNAME:USERNAME /user/USERNAME
```

---

## Use Amazon Q Developer with Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sm-q.html

**Contents:**
- Use Amazon Q Developer with Amazon SageMaker Studio Classic
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic is an integrated machine learning environment where you can build, train, deploy, and analyze your models all in the same application. You can generate code recommendations and suggest improvements related to code issues by using Amazon Q Developer with Amazon SageMaker AI.

Amazon Q Developer is a generative artificial intelligence (AI) powered conversational assistant that can help you understand, build, extend, and operate AWS applications. In the context of an integrated AWS coding environment, Amazon Q can generate code recommendations based on developers' code, as well as their comments in natural language.

Amazon Q has the most support for Java, Python, JavaScript, TypeScript, C#, Go, PHP, Rust, Kotlin, and SQL, as well as the Infrastructure as Code (IaC) languages JSON (AWS CloudFormation), YAML (AWS CloudFormation), HCL (Terraform), and CDK (Typescript, Python). It also supports code generation for Ruby, C++, C, Shell, and Scala. For examples of how Amazon Q integrates with Amazon SageMaker AI and displays code suggestions in the Amazon SageMaker Studio Classic IDE, see Code Examples in the Amazon Q Developer User Guide.

For more information on using Amazon Q with Amazon SageMaker Studio Classic, see the Amazon Q Developer User Guide.

---

## Troubleshooting

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-emr-troubleshooting.html

**Contents:**
- Troubleshooting
- Troubleshoot Livy connections hanging or failing

When working with Amazon EMR clusters from Studio or Studio Classic notebooks, you may encounter various potential issues or challenges during the connection or usage process. To help you troubleshoot and resolve these errors, this section provides guidance on common problems that can arise.

The following are common errors that might occur while connecting or using Amazon EMR clusters from Studio or Studio Classic notebooks.

The following are Livy connectivity issues that might occur while using Amazon EMR clusters from Studio or Studio Classic notebooks.

Your Amazon EMR cluster encountered an out-of-memory error.

A possible reason for a Livy connection via sparkmagic hanging or failing is if your Amazon EMR cluster encountered an out-of-memory error.

By default, the Java configuration parameter of the Apache Spark driver, spark.driver.defaultJavaOptions, is set to -XX:OnOutOfMemoryError='kill -9 %p'. This means that the default action taken when the driver program encounters an OutOfMemoryError is to terminate the driver program by sending a SIGKILL signal. When the Apache Spark driver is terminated, any Livy connection via sparkmagic that depends on that driver hangs or fails. This is because the Spark driver is responsible for managing the Spark application's resources, including task scheduling and execution. Without the driver, the Spark application cannot function, and any attempts to interact with it fails.

If you suspect that your Spark cluster is experiencing memory issues, you can check Amazon EMR logs. Containers killed due to out-of-memory errors typically exit with a code of 137. In such cases, you need to restart the Spark application and establish a new Livy connection to resume interaction with the Spark cluster.

You can refer to the knowledge base article How do I resolve the error "Container killed by YARN for exceeding memory limits" in Spark on Amazon EMR? on AWS re:Post to learn about various strategies and parameters that can be used to address an out-of-memory issue.

We recommend reviewing the Amazon EMR Best Practices Guides for best practices and tuning guidance on running Apache Spark workloads on your Amazon EMR clusters.

Your Livy session times out when connecting to an Amazon EMR cluster for the first time.

When you initially connect to an Amazon EMR cluster using sagemaker-studio-analytics-extension, which enables connection to a remote Spark (Amazon EMR) cluster via the SparkMagic library using Apache Livy, you may 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
spark.driver.defaultJavaOptions
```

Example 2 (unknown):
```unknown
-XX:OnOutOfMemoryError='kill -9 %p'
```

Example 3 (unknown):
```unknown
OutOfMemoryError
```

Example 4 (unknown):
```unknown
An error was encountered: Session 0 did not start up in 60
                            seconds.
```

---

## Customize Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-customize.html

**Contents:**
- Customize Amazon SageMaker Studio Classic
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

There are four options for customizing your Amazon SageMaker Studio Classic environment. You bring your own SageMaker image, use a lifecycle configuration script, attach suggested Git repos to Studio Classic, or create kernels using persistent Conda environments in Amazon EFS. Use each option individually, or together.

Bring your own SageMaker image: A SageMaker image is a file that identifies the kernels, language packages, and other dependencies required to run a Jupyter notebook in Amazon SageMaker Studio Classic. Amazon SageMaker AI provides many built-in images for you to use. If you need different functionality, you can bring your own custom images to Studio Classic.

Use lifecycle configurations with Amazon SageMaker Studio Classic: Lifecycle configurations are shell scripts triggered by Amazon SageMaker Studio Classic lifecycle events, such as starting a new Studio Classic notebook. You can use lifecycle configurations to automate customization for your Studio Classic environment. For example, you can install custom packages, configure notebook extensions, preload datasets, and set up source code repositories.

Attach suggested Git repos to Studio Classic: You can attach suggested Git repository URLs at the Amazon SageMaker AI domain or user profile level. Then, you can select the repo URL from the list of suggestions and clone that into your environment using the Git extension in Studio Classic.

Persist Conda environments to the Studio Classic Amazon EFS volume: Studio Classic uses an Amazon EFS volume as a persistent storage layer. You can save your Conda environment on this Amazon EFS volume, then use the saved environment to create kernels. Studio Classic automatically picks up all valid environments saved in Amazon EFS as KernelGateway kernels. These kernels persist through restart of the kernel, app, and Studio Classic. For more information, see the Persist Conda environments to the Studio Classic E

*[Content truncated]*

---

## Configure listing Amazon EMR clusters

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-configure-discoverability-emr-cluster.html

**Contents:**
- Configure listing Amazon EMR clusters
        - Important
        - Note
        - Note

Administrators can configure permissions for the SageMaker Studio execution role to grant users the ability to view the list of Amazon EMR clusters they have access to, allowing them to connect to these clusters. The clusters to which you want access can be deployed in the same AWS account as Studio (choose Single account) or in separate accounts (choose Cross account). The following page describes how to grant the permissions for viewing Amazon EMR clusters from Studio or Studio Classic.

You can only discover and connect to Amazon EMR clusters for JupyterLab and Studio Classic applications that are launched from private spaces. Ensure that the Amazon EMR clusters are located in the same AWS region as your Studio environment.

To let data scientists discover and then connect to Amazon EMRclusters from Studio or Studio Classic, follow these steps.

If your Amazon EMR clusters and Studio or Studio Classic are deployed in the same AWS account, attach the following permissions to the SageMaker AI execution role accessing your cluster.

Step 1: Retrieve the ARN of the SageMaker AI execution role used by your private space.

For information on spaces and execution roles in SageMaker AI, see Understanding domain space permissions and execution roles.

For more information about how to retrieve the ARN of SageMaker AI's execution role, see Get your execution role.

Step 2: Attach the following permissions to the SageMaker AI execution role accessing your Amazon EMR clusters.

Navigate to the IAM console.

Choose Roles and then search for your execution role by name in the Search field. The role name is the last part of the ARN, after the last forward slash (/).

Follow the link to your role.

Choose Add permissions and then Create inline policy.

In the JSON tab, add the Amazon EMR permissions allowing Amazon EMR access and operations. For details on the policy document, see List Amazon EMR policies in Reference policies. Replace the region, and accountID with their actual values before copying the list of statements to the inline policy of your role.

Choose Next and then provide a Policy name.

Choose Create policy.

Users of role-based access control (RBAC) connectivity to Amazon EMR clusters should also refer to Configure runtime role authentication when your Amazon EMR cluster and Studio are in the same account.

Before you get started, retrieve the ARN of the SageMaker AI execution role used by your private space.

For information on spaces and execution ro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AssumableRole
```

Example 2 (unknown):
```unknown
AssumableRole
```

Example 3 (unknown):
```unknown
AssumableRole
```

Example 4 (unknown):
```unknown
SageMakerExecutionRole
```

---

## Generative AI in SageMaker notebook environments

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jupyterai.html

**Contents:**
- Generative AI in SageMaker notebook environments
        - Topics

Jupyter AI is an open-source extension of JupyterLab integrating generative AI capabilities into Jupyter notebooks. Through the Jupyter AI chat interface and magic commands, users experiment with code generated from natural language instructions, explain existing code, ask questions about their local files, generate entire notebooks, and more. The extension connects Jupyter notebooks with large language models (LLMs) that users can use to generate text, code, or images, and to ask questions about their own data. Jupyter AI supports generative model providers such as AI21, Anthropic, AWS (JumpStart and Amazon Bedrock), Cohere, and OpenAI.

You can also use Amazon Q Developer as an out of the box solution. Instead of having to manually set up a connection to a model, you can start using Amazon Q Developer with minimal configuration. When you enable Amazon Q Developer, it becomes the default solution provider within Jupyter AI. For more information about using Amazon Q Developer, see SageMaker JupyterLab.

The extension's package is included in Amazon SageMaker Distribution version 1.2 and onwards. Amazon SageMaker Distribution is a Docker environment for data science and scientific computing used as the default image of JupyterLab notebook instances. Users of different IPython environments can install Jupyter AI manually.

In this section, we provide an overview of Jupyter AI capabilities and demonstrate how to configure models provided by JumpStart or Amazon Bedrock from JupyterLab or Studio Classic notebooks. For more in-depth information on the Jupyter AI project, refer to its documentation. Alternatively, you can refer to the blog post Generative AI in Jupyter for an overview and examples of key Jupyter AI capabilities.

Before using Jupyter AI and interacting with your LLMs, make sure that you satisfy the following prerequisites:

For models hosted by AWS, you should have the ARN of your SageMaker AI endpoint or have access to Amazon Bedrock. For other model providers, you should have the API key used to authenticate and authorize requests to your model. Jupyter AI supports a wide range of model providers and language models, refer to the list of its supported models to stay updated on the latest available models. For information on how to deploy a model in JumpStart, see Deploy a Model in the JumpStart documentation. You need to request access to Amazon Bedrock to use it as your model provider.

Ensure that Jupyter AI libraries are present in your envi

*[Content truncated]*

---

## Use Amazon SageMaker Studio Classic Notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks.html

**Contents:**
- Use Amazon SageMaker Studio Classic Notebooks
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic notebooks are collaborative notebooks that you can launch quickly because you don't need to set up compute instances and file storage beforehand. Studio Classic notebooks provide persistent storage, which enables you to view and share notebooks even if the instances that the notebooks run on are shut down.

You can share your notebooks with others, so that they can easily reproduce your results and collaborate while building models and exploring your data. You provide access to a read-only copy of the notebook through a secure URL. Dependencies for your notebook are included in the notebook's metadata. When your colleagues copy the notebook, it opens in the same environment as the original notebook.

A Studio Classic notebook runs in an environment defined by the following:

Amazon EC2 instance type – The hardware configuration the notebook runs on. The configuration includes the number and type of processors (vCPU and GPU), and the amount and type of memory. The instance type determines the pricing rate.

SageMaker image – A container image that is compatible with SageMaker Studio Classic. The image consists of the kernels, language packages, and other files required to run a notebook in Studio Classic. There can be multiple images in an instance. For more information, see Custom Images in Amazon SageMaker Studio Classic.

KernelGateway app – A SageMaker image runs as a KernelGateway app. The app provides access to the kernels in the image. There is a one-to-one correspondence between a SageMaker AI image and a KernelGateway app.

Kernel – The process that inspects and runs the code contained in the notebook. A kernel is defined by a kernel spec in the image. There can be multiple kernels in an image.

You can change any of these resources from within the notebook.

The following diagram outlines how a notebook kernel runs in relation to the KernelGateway App, User, and domain.

Sam

*[Content truncated]*

---

## JupyterLab Versioning in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jl.html#studio-jl-install

**Contents:**
- JupyterLab Versioning in Amazon SageMaker Studio Classic
        - Important
        - Important
- JupyterLab 3
  - Important changes to JupyterLab 3
- Restricting default JupyterLab version using an IAM policy condition key
- Setting a default JupyterLab version
  - From the console
  - From the AWS CLI
    - Create or update domain

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The Amazon SageMaker Studio Classic interface is based on JupyterLab, which is a web-based interactive development environment for notebooks, code, and data. Studio Classic only supports using JupyterLab 3.

If you created your domain and user profile using the AWS Management Console before 08/31/2022 or using the AWS Command Line Interface before 02/22/23, then your Studio Classic instance defaulted to JupyterLab 1. After 07/01/2024, you cannot create any Studio Classic applications that run JupyterLab 1.

JupyterLab 3 includes the following features that are not available in previous versions. For more information about these features, see JupyterLab 3.0 is released!.

Visual debugger when using the Base Python 2.0 and Data Science 2.0 kernels.

Table of Contents (TOC)

Multi-language support

Single interface mode

Consider the following when using JupyterLab 3:

When setting the JupyterLab version using the AWS CLI, select the corresponding image for your Region and JupyterLab version from the image list in From the AWS CLI.

In JupyterLab 3, you must activate the studio conda environment before installing extensions. For more information, see Installing JupyterLab and Jupyter Server extensi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 3 (unknown):
```unknown
111122223333
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockUsersFromCreatingJupyterLab3Apps",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateUserProfile",
                "sagemaker:UpdateUserProfile"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

---

## Use an Interactive Data Preparation Widget in an Amazon SageMaker Studio Classic Notebook to Get Data Insights

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-interactively-prepare-data-notebook.html

**Contents:**
- Use an Interactive Data Preparation Widget in an Amazon SageMaker Studio Classic Notebook to Get Data Insights
- Getting started with running the widget
        - Important
        - Note
- Reference for the insights and transforms in the widget

Use the Data Wrangler data preparation widget to interact with your data, get visualizations, explore actionable insights, and fix data quality issues.

You can access the data preparation widget from an Amazon SageMaker Studio Classic notebook. For each column, the widget creates a visualization that helps you better understand its distribution. If a column has data quality issues, a warning appears in its header.

To see the data quality issues, select the column header showing the warning. You can use the information that you get from the insights and the visualizations to apply the widget's built-in transformations to help you fix the issues.

For example, the widget might detect that you have a column that only has one unique value and show you a warning. The warning provides the option to drop the column from the dataset.

Use the following information to help you get started with running a notebook.

Open a notebook in Amazon SageMaker Studio Classic. For information about opening a notebook, see Create or Open an Amazon SageMaker Studio Classic Notebook.

To run the widget, the notebook must use one of the following images:

Python 3 (Data Science) with Python 3.7

Python 3 (Data Science 2.0) with Python 3.8

Python 3 (Data Science 3.0) with Python 3.10

For more information about images, see Amazon SageMaker Images Available for Use With Studio Classic Notebooks.

Use the following code to import the data preparation widget and pandas. The widget uses pandas dataframes to analyze your data.

The following example code loads a file into the dataframe called df.

You can use a dataset in any format that you can load as a pandas dataframe object. For more information about pandas formats, see IO tools (text, CSV, HDF5, …).

The following cell runs the df variable to start the widget.

The top of the dataframe has the following options:

View the Pandas table – Switches between the interactive visualization and a pandas table.

Use all of the rows in your dataset to compute the insights. Using the entire dataset might increase the time it takes to generate the insights. – If you don't select the option, Data Wrangler computes the insights for the first 10,000 rows of the dataset.

The dataframe shows the first 1000 rows of the dataset. Each column header has a stacked bar chart that shows the column's characteristics. It shows the proportion of valid values, invalid values, and missing values. You can hover over the different portions of the stacked b

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
import pandas as pd
import sagemaker_datawrangler
```

Example 2 (unknown):
```unknown
df = pd.read_csv("example-dataset.csv")
```

Example 3 (unknown):
```unknown
Placeholder
```

---

## View the details of a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-studio-list.html

**Contents:**
- View the details of a pipeline
        - Note

You can view the details of a SageMaker AI pipeline to understand its parameters, the dependencies of its steps, or monitor its progress and status. This can help you troubleshoot or optimize your workflow. You can access the details of a given pipeline using the Amazon SageMaker Studio console and explore its execution history, definition, parameters, and metadata.

Alternatively, if your pipeline is associated with a SageMaker AI Project, you can access the pipeline details from the project's details page. For more information, see View Project Resources.

To view the details of a SageMaker AI pipeline, complete the following steps based on whether you use Studio or Studio Classic.

Model repacking happens when the pipeline needs to include a custom script in the compressed model file (model.tar.gz) to be uploaded to Amazon S3 and used to deploy a model to a SageMaker AI endpoint. When SageMaker AI pipeline trains a model and registers it to the model registry, it introduces a repack step if the trained model output from the training job needs to include a custom inference script. The repack step uncompresses the model, adds a new script, and recompresses the model. Running the pipeline adds the repack step as a training job.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, select Pipelines.

(Optional) To filter the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name to view details about the pipeline.

Choose one of the following tabs to view pipeline details:

Executions – Details about the executions.

Graph – The pipeline graph, including all steps.

Parameters – The run parameters and metrics related to the pipeline.

Information – The metadata associated with the pipeline, such as tags, the pipeline Amazon Resource Name (ARN), and role ARN. You can also edit the pipeline description from this page.

Sign in to Amazon SageMaker Studio Classic. For more information, see Launch Amazon SageMaker Studio Classic.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Pipelines from the menu.

To narrow the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name to view details about the pipeline. The pipeline details tab opens and displays a list of pipeline executions. You can start an execution or choose one of the other tabs for more information abou

*[Content truncated]*

---

## APIs, CLI, and SDKs

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/api-and-sdk-reference-overview.html

**Contents:**
- APIs, CLI, and SDKs

Amazon SageMaker AI provides APIs, SDKs, and a command line interface that you can use to create and manage notebook instances and train and deploy models.

Amazon SageMaker Python SDK (Recommended)

Amazon SageMaker API Reference

Amazon Augmented AI API Reference

AWS Command Line Interface

AWS SDK for JavaScript

AWS SDK for Python (Boto)

Amazon SageMaker AI Spark

You can also get code examples from the Amazon SageMaker AI example notebooks GitHub repository.

---

## SageMaker JupyterLab

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-jl.html

**Contents:**
- SageMaker JupyterLab
        - Topics

Create a JupyterLab space within Amazon SageMaker Studio to launch the JupyterLab application. A JupyterLab space is a private or shared space within Studio that manages the storage and compute resources needed to run the JupyterLab application. The JupyterLab application is a web-based interactive development environment (IDE) for notebooks, code, and data. Use the JupyterLab application's flexible and extensive interface to configure and arrange machine learning (ML) workflows.

By default, the JupyterLab application comes with the SageMaker Distribution image. The distribution image has popular packages, such as the following:

You can use shared spaces to collaborate on your Jupyter notebooks with other users in real time. For more information about shared spaces, see Collaboration with shared spaces.

Within the JupyterLab application, you can use Amazon Q Developer, a generative AI powered code companion to generate, debug, and explain your code. For information about using Amazon Q Developer, see JupyterLab user guide. For information about setting up Amazon Q Developer, see JupyterLab administrator guide.

Build unified analytics and ML workflows in same Jupyter notebook. Run interactive Spark jobs on Amazon EMR and AWS Glue serverless infrastructure, right from your notebook. Monitor and debug jobs faster using the inline Spark UI. In a few steps, you can automate your data prep by scheduling the notebook as a job.

The JupyterLab application helps you work collaboratively with your peers. Use the built-in Git integration within the JupyterLab IDE to share and version code. Bring your own file storage system if you have an Amazon EFS volume.

The JupyterLab application runs on a single Amazon Elastic Compute Cloud (Amazon EC2) instance and uses a single Amazon Elastic Block Store (Amazon EBS) volume for storage. You can switch faster instances or increase the Amazon EBS volume size for your needs.

The JupyterLab 4 application runs in a JupyterLab space within Studio. Studio Classic uses the JupyterLab 3 application. JupyterLab 4 provides the following benefits:

A faster IDE than Amazon SageMaker Studio Classic, especially with large notebooks

Improved document search

A more performant and accessible text editor

For more information about JupyterLab, see JupyterLab Documentation.

JupyterLab user guide

JupyterLab administrator guide

---

## Trusted identity propagation with Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/trustedidentitypropagation.html

**Contents:**
- Trusted identity propagation with Studio
        - Topics

Trusted identity propagation is an AWS IAM Identity Center feature that administrators of connected AWS services can use to grant and audit access to service data. Access to this data is based on user attributes such as group associations. Setting up trusted identity propagation requires collaboration between the administrators of connected AWS services and the IAM Identity Center administrator. For more information, see Prerequisites and considerations.

The Amazon SageMaker Studio and IAM Identity Center administrators can collaborate to connect the services for trusted identity propagation. Trusted identity propagation addresses enterprise authentication needs across AWS services by simplifying:

Enhanced auditing that tracks actions to specific users

Access management for data science and machine learning workloads through integration with compatible AWS services

Compliance requirements in regulated industries

Studio supports trusted identity propagation for audit purposes and access control with connected AWS services. Trusted identity propagation in Studio does not directly handle authentication or authorization decisions within Studio itself. Instead, it propagates identity context information to compatible services that can use this information for access control.

When you use trusted identity propagation with Studio, your IAM Identity Center identity propagates to connected AWS services, creating more granular permissions and security governance.

Trusted identity propagation architecture and compatibility

Setting up trusted identity propagation for Studio

Monitoring and auditing with CloudTrail

User background sessions

How to connect with other AWS services with trusted identity propagation enabled

---

## Amazon EFS auto-mounting in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-automount.html

**Contents:**
- Amazon EFS auto-mounting in Studio

Amazon SageMaker AI supports automatically mounting a folder in an Amazon EFS volume for each user in a domain. Using this folder, users can share data between their own private spaces. However, users cannot share data with other users in the domain. Users only have access to their own folder.

The user’s folder can be accessed through a folder named user-default-efs . This folder is present in the $HOME directory of the Studio application.

For information about opting out of Amazon EFS auto-mounting, see Opt out of Amazon EFS auto-mounting.

Amazon EFS auto-mounting also facilitates the migration of data from Studio Classic to Studio. For more information, see (Optional) Migrate data from Studio Classic to Studio.

Access point information

When auto-mounting is activated, SageMaker AI uses an Amazon EFS access point to facilitate access to the data in the Amazon EFS volume. For more information about access points, see Working with Amazon EFS access points SageMaker AI creates a unique access point for each user profile in the domain during user profile creation or during application creation for an existing user profile. The POSIX user value of the access point matches the HomeEfsFileSystemUid value of the user profile that SageMaker AI creates the access point for. To get the value of the user, see DescribeUserProfile. The root directory path is also set to the same value as the POSIX user value.

SageMaker AI sets the permissions of the new directory to the following values:

Owner user ID: POSIX user value

The access point is required to access the Amazon EFS volume. As a result, you cannot delete or update the access point without losing access to the Amazon EFS volume.

If SageMaker AI encounters an issue when auto-mounting the Amazon EFS user folder during application creation, the application is still created. However, in this case, SageMaker AI creates a file named error.txt instead of mounting the Amazon EFS folder. This file describes the error encountered, as well as steps to resolve it. SageMaker AI creates the error.txt file in the user-default-efs folder located in the $HOME directory of the application.

**Examples:**

Example 1 (unknown):
```unknown
user-default-efs
```

Example 2 (unknown):
```unknown
HomeEfsFileSystemUid
```

Example 3 (unknown):
```unknown
POSIX user value
```

Example 4 (unknown):
```unknown
POSIX user value
```

---

## Amazon SageMaker Studio UI overview

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-ui.html

**Contents:**
- Amazon SageMaker Studio UI overview
        - Important
        - Topics
- Amazon SageMaker Studio navigation bar
- Amazon SageMaker Studio navigation pane
- Studio content pane

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

The Amazon SageMaker Studio user interface is split into three distinct parts. This page gives information about the distinct parts and their components.

Navigation bar– This section of the UI includes the URL, breadcrumbs, notifications, and user options.

Navigation pane– This section of the UI includes a list of the applications that are supported in Studio and options for the main workflows in Studio.

Content pane– The main working area that displays the current page of the Studio UI that you have open.

Amazon SageMaker Studio navigation bar

Amazon SageMaker Studio navigation pane

The navigation bar of the Studio UI includes the URL, breadcrumbs, notifications, and user options.

The URL of Studio changes as you navigate the UI. When you navigate to a different page in the UI, the URL changes to reflect that page. With the updated URL, you open any page in the Studio UI directly without navigating to the landing page first.

As you navigate through the Studio UI, the breadcrumbs keep track of the parent pages of the current page. By choosing one of these breadcrumbs, you can navigate to parent pages in the UI.

The notifications section of the UI gives information about important changes to Studio, updates to applications, and issues to resolve.

Choose the user options icon ( ) to get information about the user profile that is currently using Studio, and gives the option to sign out of Studio.

The navigation pane of the UI includes a list of the applications that are supported in Studio. It also provides options for the main workflows in Studio.

This section of the UI can be used in an expanded or collapsed state. To change whether the section is expanded or collapsed, select the Collapse icon ( ).

The applications section lists the applications that are available in Studio. If you choose one of the application types, you are directed to the landing page for that application.

The list of workflows includes all of the available actions that you can take in Studio. Choose one of the options to navigate to the landing page for that workflow. If there are multiple workflows available for that option, choosing the option opens a dropdown menu where you can selec

*[Content truncated]*

---

## View your Studio running instances, applications, and spaces

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-running.html

**Contents:**
- View your Studio running instances, applications, and spaces
        - Important
- View your Studio running instances and applications
        - To view running instances
- View your Studio spaces
        - View your Studio spaces in a domain

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

The following topics include information and instructions about how to view your Studio running instances, applications, and spaces. For more information about Studio spaces, see Amazon SageMaker Studio spaces.

The Running instances page gives information about all running application instances that were created in Amazon SageMaker Studio by the user, or were shared with the user.

You can view and stop running instances for all of your applications and spaces. If an instance is stopped, it does not appear on this page. Stopped instances can be viewed from the landing page for their respective application types.

You can view a list of running applications and their details in Studio.

Launch Studio following the steps in Launch Amazon SageMaker Studio.

On the left navigation pane, choose Running instances.

From the Running instances page, you can view a list of running applications and details about those applications.

To view non-running instances, from the left navigation pane choose, the relevant application under Applications. The non-running applications will have the Stopped status under the Status column.

The Spaces section within your Domain details page gives information about Studio spaces within your domain. You can view, create, and delete spaces on this page.

The spaces that you can view in the Spaces section are running spaces for the following:

JupyterLab private space. For information about JupyterLab, see SageMaker JupyterLab.

Code Editor private space. For information about Code Editor, based on Code-OSS, Visual Studio Code - Open Source, see Code Editor in Amazon SageMaker Studio.

Studio Classic shared space. For information about Studio Classic shared space, see Collaboration with shared spaces.

There are no spaces for SageMaker Canvas, Studio Classic (private), or RStudio.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

From the left navigation pane, expand Admin configurations and choose Domains.

Choose the domain where you want to view the spaces.

On the Domain details page, choose the Space management tab to open the Spaces section.

View your Studio spaces using the AWS CLI

Use the following comm

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws sagemaker list-spaces --region us-east-1 --domain-id domain-id
```

---

## Update and Detach Lifecycle Configurations in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lcc-delete.html

**Contents:**
- Update and Detach Lifecycle Configurations in Amazon SageMaker Studio Classic
        - Important
        - Topics
- Prerequisites
- Detach using the AWS CLI

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

A lifecycle configuration script can't be changed after it's created. To update your script, you must create a new lifecycle configuration script and attach it to the respective domain, user profile, or shared space. For more information about creating and attaching the lifecycle configuration, see Create and Associate a Lifecycle Configuration with Amazon SageMaker Studio Classic.

The following topic shows how to detach a lifecycle configuration using the AWS CLI and SageMaker AI console.

Detach using the AWS CLI

Before detaching a lifecycle configuration, you must complete the following prerequisite.

To successfully detach a lifecycle configuration, no running application can be using the lifecycle configuration. You must first shut down the running applications as shown in Shut Down and Update Amazon SageMaker Studio Classic and Apps.

To detach a lifecycle configuration using the AWS CLI, remove the desired lifecycle configuration from the list of lifecycle configurations attached to the resource and pass the list as part of the respective command:

For example, the following command removes all lifecycle configurations for KernelGateways attached to the domain.

**Examples:**

Example 1 (unknown):
```unknown
aws sagemaker update-domain --domain-id domain-id \
--region region \
--default-user-settings '{
"KernelGatewayAppSettings": {
  "LifecycleConfigArns":
    []
  }
}'
```

---

## Use the Amazon SageMaker Studio Classic Launcher

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launcher.html

**Contents:**
- Use the Amazon SageMaker Studio Classic Launcher
        - Important
        - Topics
- Notebooks and compute resources
        - Note
        - Note
- Utilities and files
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can use the Amazon SageMaker Studio Classic Launcher to create notebooks and text files, and to launch terminals and interactive Python shells.

You can open Studio Classic Launcher in any of the following ways:

Choose Amazon SageMaker Studio Classic at the top left of the Studio Classic interface.

Use the keyboard shortcut Ctrl + Shift + L.

From the Studio Classic menu, choose File and then choose New Launcher.

If the SageMaker AI file browser is open, choose the plus (+) sign in the Studio Classic file browser menu.

In the Quick actions section of the Home tab, choose Open Launcher. The Launcher opens in a new tab. The Quick actions section is visible by default but can be toggled off. Choose Customize Layout to turn this section back on.

The Launcher consists of the following two sections:

Notebooks and compute resources

In this section, you can create a notebook, open an image terminal, or open a Python console.

To create or launch one of those items:

Choose Change environment to select a SageMaker image, a kernel, an instance type, and, optionally, add a lifecycle configuration script that runs on image start-up. For more information on lifecycle configuration scripts, see Use Lifecycle Configurations to Customize Amazon SageMaker Studio Classic. For more information about kernel updates, see Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook.

When you choose an item from this section, you might incur additional usage charges. For more information, see Usage Metering for Amazon SageMaker Studio Classic Notebooks.

The following items are available:

Launches the notebook in a kernel session on the chosen SageMaker image.

Creates the notebook in the folder that you have currently selected in the file browser. To view the file browser, in the left sidebar of Studio Classic, choose the File Browser icon.

Launches the shell in a kernel session on the chosen SageMaker image.

**Examples:**

Example 1 (unknown):
```unknown
Ctrl + Shift + L
```

Example 2 (unknown):
```unknown
ml.t3.medium
```

Example 3 (unknown):
```unknown
ml.g4dn.xlarge
```

Example 4 (unknown):
```unknown
Experiment.create
```

---

## Create a MLOps Project using Amazon SageMaker Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-create.html

**Contents:**
- Create a MLOps Project using Amazon SageMaker Studio or Studio Classic
        - Important

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

This procedure demonstrates how to create an MLOps project using Amazon SageMaker Studio Classic.

An IAM account or IAM Identity Center to sign in to Studio or Studio Classic. For more information, see Amazon SageMaker AI domain overview.

Permission to use SageMaker AI-provided project templates. For more information, see Granting SageMaker Studio Permissions Required to Use Projects.

Basic familiarity with the Studio Classic user interface. For nore information, see Amazon SageMaker Studio Classic UI Overview.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, choose Deployments, and then choose Projects.

In the upper-right corner above the projects list, choose Create project.

In the Templates page, choose a template to use for your project. For more information about project templates, see MLOps Project Templates.

In the Project details page, enter the following information:

Name: A name for your project.

Description: An optional description for your project.

The values for the Service Catalog provisioning parameters related to your chosen template.

Choose Create project and wait for the project to appear in the Projects list.

(Optional) In the Studio sidebar, choose Pipelines to view the pipeline created from your project. For more information about Pipelines, see Pipelines.

Sign in to Studio Classic. For more information, see Amazon SageMaker AI domain overview.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Deployments from the menu, and then select Projects.

Choose Create project.

The Create project tab opens displaying a list of available templates.

If not selected already, choose SageMaker AI templates. For more info

*[Content truncated]*

---

## Open the Amazon SageMaker Debugger Insights dashboard

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-on-studio-insights.html

**Contents:**
- Open the Amazon SageMaker Debugger Insights dashboard
        - Note
        - Important

In the SageMaker Debugger Insights dashboard in Studio Classic, you can see the compute resource utilization, resource utilization, and system bottleneck information of your training job that runs on Amazon EC2 instances in real time and after trainings

The SageMaker Debugger Insights dashboard runs a Studio Classic application on an ml.m5.4xlarge instance to process and render the visualizations. Each SageMaker Debugger Insights tab runs one Studio Classic kernel session. Multiple kernel sessions for multiple SageMaker Debugger Insights tabs run on the single instance. When you close a SageMaker Debugger Insights tab, the corresponding kernel session is also closed. The Studio Classic application remains active and accrues charges for the ml.m5.4xlarge instance usage. For information about pricing, see the Amazon SageMaker Pricing page.

When you are done using the SageMaker Debugger Insights dashboard, you must shut down the ml.m5.4xlarge instance to avoid accruing charges. For instructions on how to shut down the instance, see Shut down the Amazon SageMaker Debugger Insights instance.

To open the SageMaker Debugger Insights dashboard

On the Studio Classic Home page, choose Experiments in the left navigation pane.

Search your training job in the Experiments page. If your training job is set up with an Experiments run, the job should appear in the Experiments tab; if you didn't set up an Experiments run, the job should appear in the Unassigned runs tab.

Choose (click) the link of the training job name to see the job details.

Under the OVERVIEW menu, choose Debuggger. This should show the following two sections.

In the Debugger rules section, you can browse the status of the Debugger built-in rules associated with the training job.

In the Debugger insights section, you can find links to open SageMaker Debugger Insights on the dashboard.

In the SageMaker Debugger Insights section, choose the link of the training job name to open the SageMaker Debugger Insights dashboard. This opens a Debug [your-training-job-name] window. In this window, Debugger provides an overview of the computational performance of your training job on Amazon EC2 instances and helps you identify issues in compute resource utilization.

You can also download an aggregated profiling report by adding the built-in ProfilerReport rule of SageMaker Debugger. For more information, see Configure Built-in Profiler Rules and Profiling Report Generated Using SageMaker Debugger.

**Examples:**

Example 1 (unknown):
```unknown
ml.m5.4xlarge
```

Example 2 (unknown):
```unknown
ml.m5.4xlarge
```

Example 3 (unknown):
```unknown
ml.m5.4xlarge
```

---

## Create a Regression or Classification Autopilot experiment for tabular data using the Studio Classic UI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development-create-experiment-ui.html

**Contents:**
- Create a Regression or Classification Autopilot experiment for tabular data using the Studio Classic UI
        - Important
        - To create an Autopilot experiment using Studio Classic UI
        - Note
        - Note
        - Note
        - Note

As of November 30, 2023, Autopilot's UI is migrating to Amazon SageMaker Canvas as part of the updated Amazon SageMaker Studio experience. SageMaker Canvas provides analysts and citizen data scientists no-code capabilities for tasks such as data preparation, feature engineering, algorithm selection, training and tuning, inference, and more. Users can leverage built-in visualizations and what-if analysis to explore their data and different scenarios, with automated predictions enabling them to easily productionize their models. Canvas supports a variety of use cases, including computer vision, demand forecasting, intelligent search, and generative AI.

Users of Amazon SageMaker Studio Classic, the previous experience of Studio, can continue using the Autopilot UI in Studio Classic. Users with coding experience can continue using all API references in any supported SDK for technical implementation.

If you have been using Autopilot in Studio Classic until now and want to migrate to SageMaker Canvas, you might have to grant additional permissions to your user profile or IAM role so that you can create and use the SageMaker Canvas application. For more information, see (Optional) Migrate from Autopilot in Studio Classic to SageMaker Canvas.

All UI-related instructions in this guide pertain to Autopilot's standalone features before migrating to Amazon SageMaker Canvas. Users following these instructions should use Studio Classic.

You can use the Amazon SageMaker Studio Classic UI to create Autopilot experiments for classification or regression problems on tabular data. The UI helps you specify the name of your experiment, provide locations for the input and output data, and specify which target data to predict. Optionally, you can also specify the type of problem that you want to solve (regression, classification, multiclass classification), choose your modeling strategy (stacked ensembles or hyperparameters optimization), select the list of algorithms used by the Autopilot job to train the data, and more.

The UI has descriptions, toggle switches, dropdown menus, radio buttons, and more to help you navigate creating your model candidates. After the experiment runs, you can compare trials and delve into the details of the pre-processing steps, algorithms, and hyperparameter ranges of each model. Optionally, you can download their explainability and performance reports. Use the provided notebooks to see the results of the automated data exploration or the cand

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Categorical
```

Example 2 (unknown):
```unknown
concatenate
```

---

## Upload Files to Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-files.html

**Contents:**
- Upload Files to Amazon SageMaker Studio Classic
        - Important
        - Note
        - To upload files to your home directory

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

When you onboard to Amazon SageMaker Studio Classic, a home directory is created for you in the Amazon Elastic File System (Amazon EFS) volume that was created for your team. Studio Classic can only open files that have been uploaded to your directory. The Studio Classic file browser maps to your home directory.

Studio Classic does not support uploading folders. While you can only upload individual files, you can upload multiple files at the same time.

In the left sidebar, choose the File Browser icon ( ).

In the file browser, choose the Upload Files icon ( ).

Select the files you want to upload and then choose Open.

Double-click a file to open the file in a new tab in Studio Classic.

---

## JupyterLab Versioning in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jl.html

**Contents:**
- JupyterLab Versioning in Amazon SageMaker Studio Classic
        - Important
        - Important
- JupyterLab 3
  - Important changes to JupyterLab 3
- Restricting default JupyterLab version using an IAM policy condition key
- Setting a default JupyterLab version
  - From the console
  - From the AWS CLI
    - Create or update domain

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The Amazon SageMaker Studio Classic interface is based on JupyterLab, which is a web-based interactive development environment for notebooks, code, and data. Studio Classic only supports using JupyterLab 3.

If you created your domain and user profile using the AWS Management Console before 08/31/2022 or using the AWS Command Line Interface before 02/22/23, then your Studio Classic instance defaulted to JupyterLab 1. After 07/01/2024, you cannot create any Studio Classic applications that run JupyterLab 1.

JupyterLab 3 includes the following features that are not available in previous versions. For more information about these features, see JupyterLab 3.0 is released!.

Visual debugger when using the Base Python 2.0 and Data Science 2.0 kernels.

Table of Contents (TOC)

Multi-language support

Single interface mode

Consider the following when using JupyterLab 3:

When setting the JupyterLab version using the AWS CLI, select the corresponding image for your Region and JupyterLab version from the image list in From the AWS CLI.

In JupyterLab 3, you must activate the studio conda environment before installing extensions. For more information, see Installing JupyterLab and Jupyter Server extensi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockJupyterLab3DomainLevelAppCreation",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateDomain",
                "sagemaker:UpdateDomain"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

Example 3 (unknown):
```unknown
111122223333
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "BlockUsersFromCreatingJupyterLab3Apps",
            "Effect": "Deny",
            "Action": [
                "sagemaker:CreateUserProfile",
                "sagemaker:UpdateUserProfile"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:ArnLike": {
                    "sagemaker:ImageArns": "arn:aws:sagemaker:us-east-1:111122223333:image/jupyter-server-3"
                }
            }
        }
    ]
}
```

---

## Using Amazon SageMaker Feature Store in the console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-use-with-studio.html#feature-store-view-feature-group-detail-studio

**Contents:**
- Using Amazon SageMaker Feature Store in the console
        - Important
        - Topics
- Create a feature group from the console
- View feature group details from the console
- Update a feature group from the console
- View pipeline executions from the console
- View lineage from the console

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

You can use Amazon SageMaker Feature Store on the console to create, view, update, and monitor your feature groups. Monitoring in this guide includes viewing pipeline executions and lineage of your feature groups. This guide provides instructions on how to achieve these tasks from the console.

For Feature Store examples and resources using the Amazon SageMaker APIs and AWS SDK for Python (Boto3), see Amazon SageMaker Feature Store resources.

Create a feature group from the console

View feature group details from the console

Update a feature group from the console

View pipeline executions from the console

View lineage from the console

The create feature group process has four steps:

Enter feature group information.

Enter feature definitions.

Enter required features.

Enter feature group tags.

Consider which of the following options fits your use case:

Create an online store, an offline store, or both. For more information about the differences between online and offline stores, see Feature Store concepts.

Use a default AWS Key Management Service key or your own KMS key. The default key is AWS KMS key (SSE-KMS). You can reduce AWS KMS request costs by configuring use of Amazon S3 Bucket Keys on the offline store Amazon S3 bucket. The Amazon S3 Bucket Key must be enabled before using the bucket for your feature groups. For more information about reducing the cost by using Amazon S3 Bucket Keys, see Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys.

You can use the same key for both online and offline stores, or have a unique key for each. For more information about AWS KMS, see AWS Key Management Service.

If you create an offline store:

Decide if you want to create an Amazon S3 bucket or use an existing one. When usin

*[Content truncated]*

---

## Launch Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launch.html#studio-launch-cli

**Contents:**
- Launch Amazon SageMaker Studio Classic
        - Important
        - Important
        - Topics
- Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console
        - Topics
  - Prerequisite
    - Launch Studio Classic from the domain details page
    - Launch Studio Classic from the Studio Classic landing page
- Launch Amazon SageMaker Studio Classic Using the AWS CLI

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

After you have onboarded to an Amazon SageMaker AI domain, you can launch an Amazon SageMaker Studio Classic application from either the SageMaker AI console or the AWS CLI. For more information about onboarding to a domain, see Amazon SageMaker AI domain overview.

Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console

Launch Amazon SageMaker Studio Classic Using the AWS CLI

The process to navigate to Studio Classic from the Amazon SageMaker AI Console differs depending on if Studio Classic or Amazon SageMaker Studio are set as the default experience for your domain. For more information about setting the default experience for your domain, see Migration from Amazon SageMaker Studio Classic.

To complete this procedure, you must onboard to a domain by following the steps in Onboard to Amazon SageMaker AI domain.

Navigate to Studio following the steps in Launch Amazon SageMaker Studio.

From the Studio UI, find the applications pane on the left side.

From the applications pane, select Studio Classic.

From the Studio Classic landing page, select the Studio Classic instance to open.

When Studio Classic is your default experience, you can launch a Amazon SageMaker Studio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--space-name space-name \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200
```

Example 3 (unknown):
```unknown
user-profile-name
```

---

## Automated ML, no-code, or low-code

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/use-auto-ml.html

**Contents:**
- Automated ML, no-code, or low-code
        - Note
        - Topics

Amazon SageMaker AI offers the following features to automate key machine learning tasks and use no-code or low-code solutions.

Amazon SageMaker Canvas: For a UI-based, no-code AutoML experience, new users should use the Amazon SageMaker Canvas application in Amazon SageMaker Studio.

Amazon SageMaker Canvas provides analysts and citizen data scientists no-code capabilities for tasks such as data preparation, feature engineering, algorithm selection, training and tuning, inference, and more. Users can leverage built-in visualizations and what-if analysis to explore their data and different scenarios, with automated predictions enabling them to easily productionize their models. SageMaker Canvas supports a variety of use cases, including computer vision, demand forecasting, intelligent search, and generative AI.

Amazon SageMaker Autopilot: Amazon SageMaker Autopilot is an automated machine learning (AutoML) feature-set that automates the end-to-end process of building, training, tuning, and deploying machine learning models. Amazon SageMaker Autopilot analyzes your data, selects algorithms suitable for your problem type, preprocesses the data to prepare it for training, handles automatic model training, and performs hyperparameter optimization to find the best performing model for your dataset.

As of November 30, 2023, the user interface (UI) for Autopilot is integrated into the Amazon SageMaker Canvas application in Studio.

Users of Amazon SageMaker Studio Classic, the previous experience of Studio, can continue using the Autopilot UI in Studio Classic. Users with coding experience can continue using the AutoML API references in any supported SDK for technical implementation.

If you have been using Autopilot in Studio Classic until now and want to migrate to SageMaker Canvas, you might have to grant additional permissions to your user profile or IAM role so that you can create and use the SageMaker Canvas application. For more information, see (Optional) Migrate from Autopilot in Studio Classic to SageMaker Canvas.

Amazon SageMaker JumpStart: SageMaker JumpStart provides pretrained, open-source models for a wide range of problem types to help you get started with machine learning. You can incrementally train and tune these models before deployment. JumpStart also provides solution templates that set up infrastructure for common use cases, and executable example notebooks for machine learning with SageMaker AI.

SageMaker JumpStart pretrained models

---

## Considerations

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/cluster-specific-configurations-special-considerations.html

**Contents:**
- Considerations

When you're using a Amazon SageMaker HyperPod recipes, there are some factors that can impact the process of model training.

The transformers version must be 4.45.2 or greater for Llama 3.2. If you're using a Slurm or K8s workflow, the version is automatically updated.

Mixtral does not support 8-bit floating point precision (FP8)

Amazon EC2 p4 instance does not support FP8

**Examples:**

Example 1 (unknown):
```unknown
transformers
```

---

## Migrate the UI from Studio Classic to Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-ui.html

**Contents:**
- Migrate the UI from Studio Classic to Studio
- Prerequisites
- Step 1: Update application creation permissions
        - Note
        - Note
- Step 2: Update VPC configuration
- Step 3: Upgrade to the Studio UI
    - Test Studio functionality
    - Clean up test domain resources
        - Note

The first phase for migrating an existing domain involves migrating the UI from Amazon SageMaker Studio Classic to Amazon SageMaker Studio. This phase does not include the migration of data. Users can continue working with their data the same way as they were before migration. For information about migrating data, see (Optional) Migrate data from Studio Classic to Studio.

Phase 1 consists of the following steps:

Update application creation permissions for new applications available in Studio.

Update the VPC configuration for the domain.

Upgrade the domain to use the Studio UI.

Before running these steps, complete the prerequisites in Complete prerequisites to migrate the Studio experience.

Before migrating the domain, update the domain's execution role to grant users permissions to create applications.

Create an AWS Identity and Access Management policy with one of the following contents by following the steps in Creating IAM policies:

Use the following policy to grant permissions for all application types and spaces.

If the domain uses the SageMakerFullAccess policy, you do not need to perform this action. SageMakerFullAccess grants permissions to create all applications.

Because Studio shows an expanded set of applications, users may have access to applications that weren't displayed before. Administrators can limit access to these default applications by creating an AWS Identity and Access Management (IAM) policy that grants denies permissions for some applications to specific users.

Application type can be either jupyterlab or codeeditor.

Attach the policy to the execution role of the domain. For instructions, follow the steps in Adding IAM identity permissions (console).

If you use your domain in VPC-Only mode, ensure your VPC configuration meets the requirements for using Studio in VPC-Only mode. For more information, see Connect Amazon SageMaker Studio in a VPC to External Resources.

Before you migrate your existing domain from Studio Classic to Studio, we recommend creating a test domain using Studio with the same configurations as your existing domain.

Use this test domain to interact with Studio, test out networking configurations, and launch applications, before migrating the existing domain.

Get the domain ID of your existing domain.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

From the left navigation pane, expand Admin configurations and choose Domains.

Choose the existing domain.

On t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
SageMakerFullAccess
```

Example 2 (unknown):
```unknown
SageMakerFullAccess
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "SMStudioUserProfileAppPermissionsCreateAndDelete",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateApp",
                "sagemaker:DeleteApp"
            ],
            "Resource": "arn:aws:sagemaker:us-east-1:111122223333:app/*",
            "Condition": {
                "Null": {
                    "sagemaker:OwnerUserProfileArn": "true"
                }
            }
        },
        {
            "Sid": "SMStudioCreatePresignedDomainUrlForUserProfile",
            "E
...
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "SMStudioUserProfileAppPermissionsCreateAndDelete",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateApp",
                "sagemaker:DeleteApp"
            ],
            "Resource": "arn:aws:sagemaker:us-east-1:111122223333:app/*",
            "Condition": {
                "Null": {
                    "sagemaker:OwnerUserProfileArn": "true"
                }
            }
        },
        {
            "Sid": "SMStudioCreatePresignedDomainUrlForUserProfile",
            "E
...
```

---

## Amazon SageMaker Debugger UI in Amazon SageMaker Studio Classic Experiments

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-on-studio.html

**Contents:**
- Amazon SageMaker Debugger UI in Amazon SageMaker Studio Classic Experiments
        - Important
        - Topics

Use the Amazon SageMaker Debugger Insights dashboard in Amazon SageMaker Studio Classic Experiments to analyze your model performance and system bottlenecks while running training jobs on Amazon Elastic Compute Cloud (Amazon EC2) instances. Gain insights into your training jobs and improve your model training performance and accuracy with the Debugger dashboards. By default, Debugger monitors system metrics (CPU, GPU, GPU memory, network, and data I/O) every 500 milliseconds and basic output tensors (loss and accuracy) every 500 iterations for training jobs. You can also further customize Debugger configuration parameter values and adjust the saving intervals through the Studio Classic UI or using the Amazon SageMaker Python SDK.

If you're using an existing Studio Classic app, delete the app and restart to use the latest Studio Classic features. For instructions on how to restart and update your Studio Classic environment, see Update Amazon SageMaker AI Studio Classic.

Open the Amazon SageMaker Debugger Insights dashboard

Amazon SageMaker Debugger Insights dashboard controller

Explore the Amazon SageMaker Debugger Insights dashboard

Shut down the Amazon SageMaker Debugger Insights instance

---

## Visualize results for real-time endpoints in Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-interpreting-visualize-results.html

**Contents:**
- Visualize results for real-time endpoints in Amazon SageMaker Studio
        - To view the detailed results of a monitoring job
        - To create a chart in SageMaker Studio to visualize monitoring results

If you are monitoring a real-time endpoint, you can also visualize the results in Amazon SageMaker Studio. You can view the details of any monitoring job run, and you can create charts that show the baseline and captured values for any metric that the monitoring job calculates.

Sign in to Studio. For more information, see Amazon SageMaker AI domain overview.

In the left navigation pane, choose the Components and registries icon ( ).

Choose Endpoints in the drop-down menu.

On the endpoint tab, choose the monitoring type for which you want to see job details.

Choose the name of the monitoring job run for which you want to view details from the list of monitoring jobs.

The MONITORING JOB DETAILS tab opens with a detailed report of the monitoring job.

You can create a chart that displays the baseline and captured metrics for a time period.

Sign in to Studio. For more information, see Amazon SageMaker AI domain overview.

In the left navigation pane, choose the Components and registries icon ( ).

Choose Endpoints in the drop-down menu.

On the Endpoint tab, choose the monitoring type you want to create a chart for. This example shows a chart for the Model quality monitoring type.

On the CHART PROPERTIES tab, choose the time period, statistic, and metric that you want to chart. This example shows a chart for a Timeline of 1 week, the Average Statistic of, and the F1 Metric.

The chart that shows the baseline and current metric statistic you chose in the previous step shows up in the Endpoint tab.

---

## HyperPod in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-studio.html

**Contents:**
- HyperPod in Studio
        - Topics

You can launch machine learning workloads on Amazon SageMaker HyperPod clusters and view HyperPod cluster information in Amazon SageMaker Studio. The increased visibility into cluster details and hardware metrics can help your team identify the right candidate for your pre-training or fine-tuning workloads.

A set of commands are available to help you get started when you launch Studio IDEs on a HyperPod cluster. You can work on your training scripts, use Docker containers for the training scripts, and submit jobs to the cluster, all from within the Studio IDEs. The following sections provide information on how to set this up, how to discover clusters and monitor their tasks, how to view cluster information, and how to connect to HyperPod clusters in IDEs within Studio.

Setting up HyperPod in Studio

HyperPod tabs in Studio

Connecting to HyperPod clusters and submitting tasks to clusters

---

## Prepare ML Data with Amazon SageMaker Data Wrangler

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html

**Contents:**
- Prepare ML Data with Amazon SageMaker Data Wrangler
        - Important
        - Important
        - Important
        - Topics

Amazon SageMaker Data Wrangler has been integrated into Amazon SageMaker Canvas. Within the new Data Wrangler experience in SageMaker Canvas, you can use a natural language interface to explore and transform your data in addition to the visual interface. For more information about Data Wrangler in SageMaker Canvas, see Data preparation.

Amazon SageMaker Data Wrangler (Data Wrangler) is a feature of Amazon SageMaker Studio Classic that provides an end-to-end solution to import, prepare, transform, featurize, and analyze data. You can integrate a Data Wrangler data preparation flow into your machine learning (ML) workflows to simplify and streamline data pre-processing and feature engineering using little to no coding. You can also add your own Python scripts and transformations to customize workflows.

Data Wrangler provides the following core functionalities to help you analyze and prepare data for machine learning applications.

Import – Connect to and import data from Amazon Simple Storage Service (Amazon S3), Amazon Athena (Athena), Amazon Redshift, Snowflake, and Databricks.

Data Flow – Create a data flow to define a series of ML data prep steps. You can use a flow to combine datasets from different data sources, identify the number and types of transformations you want to apply to datasets, and define a data prep workflow that can be integrated into an ML pipeline.

Transform – Clean and transform your dataset using standard transforms like string, vector, and numeric data formatting tools. Featurize your data using transforms like text and date/time embedding and categorical encoding.

Generate Data Insights – Automatically verify data quality and detect abnormalities in your data with Data Wrangler Data Insights and Quality Report.

Analyze – Analyze features in your dataset at any point in your flow. Data Wrangler includes built-in data visualization tools like scatter plots and histograms, as well as data analysis tools like target leakage analysis and quick modeling to understand feature correlation.

Export – Export your data preparation workflow to a different location. The following are example locations:

Amazon Simple Storage Service (Amazon S3) bucket

Amazon SageMaker Pipelines – Use Pipelines to automate model deployment. You can export the data that you've transformed directly to the pipelines.

Amazon SageMaker Feature Store – Store the features and their data in a centralized store.

Python script – Store the data and their transform

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
cat /opt/conda/share/jupyter/lab/staging/yarn.lock | grep -A 1
                "@amzn/sagemaker-ui-data-prep-plugin@"
```

---

## Install External Libraries and Kernels in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-add-external.html

**Contents:**
- Install External Libraries and Kernels in Amazon SageMaker Studio Classic
        - Important
- Package installation tools
        - Important
        - Note
  - Conda
        - Note
        - Supported conda operations
  - Pip
        - Supported pip operations

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic notebooks come with multiple images already installed. These images contain kernels and Python packages including scikit-learn, Pandas, NumPy, TensorFlow, PyTorch, and MXNet. You can also install your own images that contain your choice of packages and kernels. For more information on installing your own image, see Custom Images in Amazon SageMaker Studio Classic.

The different Jupyter kernels in Amazon SageMaker Studio Classic notebooks are separate conda environments. For information about conda environments, see Managing environments.

Currently, all packages in Amazon SageMaker notebooks are licensed for use with Amazon SageMaker AI and do not require additional commercial licenses. However, this might be subject to change in the future, and we recommend reviewing the licensing terms regularly for any updates.

The method that you use to install Python packages from the terminal differs depending on the image. Studio Classic supports the following package installation tools:

Notebooks – The following commands are supported. If one of the following does not work on your image, try the other one.

The Jupyter terminal – You can install packages using pip and conda directly. You can also use apt-get install to install system packages from the terminal.

We do not recommend using pip install -u or pip install --user, because those commands install packages on the user's Amazon EFS volume and can potentially block JupyterServer app restarts. Instead, use a lifecycle configuration to reinstall the required packages on app restarts as shown in Install packages using lifecycle configurations.

We recommend using %pip and %conda to install packages from within a notebook because they correctly take into account the active environment or interpreter being used. For more information, see Add %pip and %conda magic functions. You can also use the system command syntax (lines starting with !

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
%conda install
```

Example 2 (unknown):
```unknown
%pip install
```

Example 3 (unknown):
```unknown
apt-get install
```

Example 4 (unknown):
```unknown
pip install -u
```

---

## Admin guide

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-emr-admin-guide.html

**Contents:**
- Admin guide
        - Topics

This section provides prerequisites, networking instructions for allowing the communication between Studio or Studio Classic and Amazon EMR clusters. It covers different deployment scenarios - when Studio and Amazon EMR are provisioned within private Amazon VPCs without public internet access, as well as when they need to communicate over the internet.

It walks through how administrators can use the AWS Service Catalog to make AWS CloudFormation templates available to Studio, allowing data scientists to discover and self-provision Amazon EMR clusters directly from within Studio. This involves creating a Service Catalog portfolio, granting requisite permissions, referencing the Amazon EMR templates, and parameterizing them to enable customizations during cluster creation.

Last, it provides guidance on configuring discoverability of existing running Amazon EMR clusters from Studio, and Studio Classic, covering single account and cross-account access scenarios along with the necessary IAM permissions.

Configure Amazon EMR CloudFormation templates in the Service Catalog

Configure listing Amazon EMR clusters

Configure IAM runtime roles for Amazon EMR cluster access in Studio

---

## Clone a Git Repository in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-git.html

**Contents:**
- Clone a Git Repository in Amazon SageMaker Studio Classic
        - Important
        - To clone the repo

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic can only connect only to a local Git repository (repo). This means that you must clone the Git repo from within Studio Classic to access the files in the repo. Studio Classic offers a Git extension for you to enter the URL of a Git repo, clone it into your environment, push changes, and view commit history. If the repo is private and requires credentials to access, then you are prompted to enter your user credentials. This includes your username and personal access token. For more information about personal access tokens, see Managing your personal access tokens.

Admins can also attach suggested Git repository URLs at the Amazon SageMaker AI domain or user profile level. Users can then select the repo URL from the list of suggestions and clone that into Studio Classic. For more information about attaching suggested repos, see Attach Suggested Git Repos to Amazon SageMaker Studio Classic.

The following procedure shows how to clone a GitHub repo from Studio Classic.

In the left sidebar, choose the Git icon ( ).

Choose Clone a Repository. This opens a new window.

In the Clone Git Repository window, enter the URL in the following format for the Git repo that you want to clone or select a repository from the list of Suggested repositories.

If you entered the URL of the Git repo manually, select Clone "git-url" from the dropdown menu.

Under Project directory to clone into, enter the path to the local directory that you want to clone the Git repo into. If this value is left empty, Studio Classic clones the repo into JupyterLab's root directory.

Choose Clone. This opens a new terminal window.

If the repo requires credentials, you are prompted to enter your username and personal access token. This prompt does not accept passwords, you must use a personal access token. For more information about personal access tokens, see Managing your personal access tokens.

Wait for the download t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
https://github.com/path-to-git-repo/repo.git
```

Example 2 (unknown):
```unknown
path-to-git-repo
```

---

## Bring your own image (BYOI)

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-byoi.html

**Contents:**
- Bring your own image (BYOI)
- Key terminology
        - Topics

An image is a file that identifies the kernels, language packages, and other dependencies required to run your applications. It includes:

Programming languages (like Python or R)

Libraries and packages

Other necessary software

Amazon SageMaker Distribution (sagemaker-distribution) is a set of Docker images that include popular frameworks and packages for machine learning, data science, and visualization. For more information, see SageMaker Studio image support policy.

If you need different functionality, you can bring your own image (BYOI). You may want to create a custom image if:

You need a specific version of a programming language or library

You want to include custom tools or packages

You're working with specialized software not available in the standard images

The following section defines key terms for bringing your own image to use with SageMaker AI.

Dockerfile: A text-based document with instructions for building a Docker image. This identifies the language packages and other dependencies for your Docker image.

Docker image: A packaged set of software and dependencies built from a Dockerfile.

SageMaker AI image store: A storage of your custom images in SageMaker AI.

Custom image specifications

How to bring your own image

Launch a custom image in Studio

View your custom image details

Detach and clean up custom image resources

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-distribution
```

---

## Available Resources for Amazon SageMaker Studio Classic Notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-resources.html

**Contents:**
- Available Resources for Amazon SageMaker Studio Classic Notebooks
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The following sections list the available resources for Amazon SageMaker Studio Classic notebooks.

Instance Types Available for Use With Amazon SageMaker Studio Classic Notebooks

Amazon SageMaker Images Available for Use With Studio Classic Notebooks

---

## Use the Studio Classic Notebook Toolbar

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-menu.html

**Contents:**
- Use the Studio Classic Notebook Toolbar
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic notebooks extend the JupyterLab interface. For an overview of the original JupyterLab interface, see The JupyterLab Interface.

The following image shows the toolbar and an empty cell from a Studio Classic notebook.

When you pause on a toolbar icon, a tooltip displays the icon function. Additional notebook commands are found in the Studio Classic main menu. The toolbar includes the following icons:

Saves the notebook and updates the checkpoint file. For more information, see Get the Difference Between the Last Checkpoint.

Inserts a code cell below the current cell. The current cell is noted by the blue vertical marker in the left margin.

Cut, copy, and paste cells

Cuts, copies, and pastes the selected cells.

Runs the selected cells and then makes the cell that follows the last selected cell the new selected cell.

Interrupts the kernel, which cancels the currently running operation. The kernel remains active.

Restarts the kernel. Variables are reset. Unsaved information is not affected.

Restart kernel and run all cells

Restarts the kernel, then run all the cells of the notebook.

Displays or changes the current cell type. The cell types are:

Code – Code that the kernel runs.

Markdown – Text rendered as markdown.

Raw – Content, including Markdown markup, that's displayed as text.

Launches a terminal in the SageMaker image hosting the notebook. For an example, see Get App Metadata.

Opens a new tab that displays the difference between the notebook and the checkpoint file. For more information, see Get the Difference Between the Last Checkpoint.

Only enabled if the notebook is opened from a Git repository. Opens a new tab that displays the difference between the notebook and the last Git commit. For more information, see Get the Difference Between the Last Commit.

Displays or changes the instance type the notebook runs in. The format is as follows:

number of vCPUs + amou

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
number of vCPUs + amount of memory + number of GPUs
```

Example 2 (unknown):
```unknown
Kernel (SageMaker Image)
```

---

## Amazon Q Developer

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-amazon-q.html

**Contents:**
- Amazon Q Developer
        - Topics

Amazon Q Developer is a generative AI conversational assistant that helps you write better code. Amazon Q Developer is available in the following IDEs within Amazon SageMaker Studio:

Code Editor, based on Code-OSS, Visual Studio Code - Open Source

Use the following sections to set up Amazon Q Developer and use it within your environment.

Set up Amazon Q Developer for your users

Use Amazon Q to Expedite Your Machine Learning Workflows

Customize Amazon Q Developer in Amazon SageMaker Studio applications

---

## Amazon SageMaker AI identity-based policy examples

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security_iam_id-based-policy-examples.html#grant-tagging-permissions

**Contents:**
- Amazon SageMaker AI identity-based policy examples
        - Topics
- Policy best practices
- Using the SageMaker AI console
        - Topics
  - Permissions required to use the Amazon SageMaker AI console
  - Permissions required to use the Amazon SageMaker Ground Truth console
  - Permissions required to use the Amazon Augmented AI (Preview) console
- Allow users to view their own permissions
- Control creation of SageMaker AI resources with condition keys

By default, IAM users and roles don't have permission to create or modify SageMaker AI resources. They also can't perform tasks using the AWS Management Console, AWS CLI, or AWS API. An IAM administrator must create IAM policies that grant users and roles permission to perform specific API operations on the specified resources they need. The administrator must then attach those policies to the IAM users or groups that require those permissions. To learn how to attach policies to an IAM user or group, see Adding and Removing IAM Identity Permissions in the Service Authorization Reference.

To learn how to create an IAM identity-based policy using these example JSON policy documents, see Creating Policies on the JSON Tab.

Policy best practices

Using the SageMaker AI console

Allow users to view their own permissions

Control creation of SageMaker AI resources with condition keys

Control access to the SageMaker AI API by using identity-based policies

Limit access to SageMaker AI API and runtime calls by IP address

Limit access to a notebook instance by IP address

Control access to SageMaker AI resources by using tags

Provide permissions for tagging SageMaker AI resources

Limit access to searchable resources with visibility conditions

Identity-based policies determine whether someone can create, access, or delete SageMaker AI resources in your account. These actions can incur costs for your AWS account. When you create or edit identity-based policies, follow these guidelines and recommendations:

Get started with AWS managed policies and move toward least-privilege permissions – To get started granting permissions to your users and workloads, use the AWS managed policies that grant permissions for many common use cases. They are available in your AWS account. We recommend that you reduce permissions further by defining AWS customer managed policies that are specific to your use cases. For more information, see AWS managed policies or AWS managed policies for job functions in the IAM User Guide.

Apply least-privilege permissions – When you set permissions with IAM policies, grant only the permissions required to perform a task. You do this by defining the actions that can be taken on specific resources under specific conditions, also known as least-privilege permissions. For more information about using IAM to apply permissions, see Policies and permissions in IAM in the IAM User Guide.

Use conditions in IAM policies to further restrict access – You 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateNotebook
```

Example 2 (unknown):
```unknown
CreateTrainingJob
```

Example 3 (unknown):
```unknown
CreateModel
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
          "Sid": "SageMakerApis",
          "Effect": "Allow",
          "Action": [
            "sagemaker:*"
          ],
          "Resource": "*"
        },
        {
          "Sid": "VpcConfigurationForCreateForms",
          "Effect": "Allow",
          "Action": [
            "ec2:DescribeVpcs",
            "ec2:DescribeSubnets",
            "ec2:DescribeSecurityGroups"
          ],
          "Resource": "*"
        },
        {
            "Sid":"KmsKeysForCreateForms",
            "Effect":"Allow",
            "Action":[
    
...
```

---

## Setting up HyperPod in Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-studio-setup.html

**Contents:**
- Setting up HyperPod in Studio
        - Topics

You need to set up the clusters depending on your choice of the cluster orchestrator to access your clusters through Amazon SageMaker Studio. In the following sections, choose the setup that matches with your orchestrator.

The instructions assume that you already have your cluster set up. For information on the cluster orchestrators and how to set up, start with the HyperPod orchestrator pages:

Orchestrating SageMaker HyperPod clusters with Slurm

Orchestrating SageMaker HyperPod clusters with Amazon EKS

Setting up a Slurm cluster in Studio

Setting up an Amazon EKS cluster in Studio

---

## Data transformation workloads with SageMaker Processing

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html

**Contents:**
- Data transformation workloads with SageMaker Processing
        - Note
        - Note
        - Tip
- Use Amazon SageMaker Processing Sample Notebooks
- Monitor Amazon SageMaker Processing Jobs with CloudWatch Logs and Metrics

SageMaker Processing refers to SageMaker AI’s capabilities to run data pre and post processing, feature engineering, and model evaluation tasks on SageMaker AI's fully-managed infrastructure. These tasks are executed as processing jobs. The following provides information and resources to learn about SageMaker Processing.

Using SageMaker Processing API, data scientists can run scripts and notebooks to process, transform, and analyze datasets to prepare them for machine learning. When combined with the other critical machine learning tasks provided by SageMaker AI, such as training and hosting, Processing provides you with the benefits of a fully managed machine learning environment, including all the security and compliance support built into SageMaker AI. You have the flexibility to use the built-in data processing containers or to bring your own containers for custom processing logic and then submit jobs to run on SageMaker AI managed infrastructure.

You can create a processing job programmatically by calling the CreateProcessingJob API action in any language supported by SageMaker AI or by using the AWS CLI. For information on how this API action translates into a function in the language of your choice, see the See Also section of CreateProcessingJob and choose an SDK. As an example, for Python users, refer to the Amazon SageMaker Processing section of SageMaker Python SDK. Alternatively, see the full request syntax of create_processing_job in the AWS SDK for Python (Boto3).

The following diagram shows how Amazon SageMaker AI spins up a Processing job. Amazon SageMaker AI takes your script, copies your data from Amazon Simple Storage Service (Amazon S3), and then pulls a processing container. The underlying infrastructure for a Processing job is fully managed by Amazon SageMaker AI. After you submit a processing job, SageMaker AI launches the compute instances, processes and analyzes the input data, and releases the resources upon completion. The output of the Processing job is stored in the Amazon S3 bucket you specified.

Your input data must be stored in an Amazon S3 bucket. Alternatively, you can use Amazon Athena or Amazon Redshift as input sources.

To learn best practices for distributed computing of machine learning (ML) training and processing jobs in general, see Distributed computing with SageMaker AI best practices.

We provide two sample Jupyter notebooks that show how to perform data preprocessing, model evaluation, or both.

For a samp

*[Content truncated]*

---

## Shut Down and Update Amazon SageMaker Studio Classic and Apps

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-update.html

**Contents:**
- Shut Down and Update Amazon SageMaker Studio Classic and Apps
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The following topics show how to shut down and update SageMaker Studio Classic and Studio Classic Apps.

Studio Classic provides a notification icon ( ) in the upper-right corner of the Studio Classic UI. This notification icon displays the number of unread notices. To read the notices, select the icon.

Studio Classic provides two types of notifications:

Upgrade – Displayed when Studio Classic or one of the Studio Classic apps have released a new version. To update Studio Classic, see Shut Down and Update Amazon SageMaker Studio Classic. To update Studio Classic apps, see Shut Down and Update Amazon SageMaker Studio Classic Apps.

Information – Displayed for new features and other information.

To reset the notification icon, you must select the link in each notice. Read notifications may still display in the icon. This does not indicate that updates are still needed after you have updated Studio Classic and Studio Classic Apps.

To learn how to update Amazon SageMaker Data Wrangler, see Shut Down and Update Amazon SageMaker Studio Classic Apps.

To ensure that you have the most recent software updates, update Amazon SageMaker Studio Classic and your Studio Classic apps using the methods outlined in the following topics.

Shut Down and Update Amazon SageMaker Studio Classic

Shut Down and Update Amazon SageMaker Studio Classic Apps

---

## Local mode support in Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-local.html

**Contents:**
- Local mode support in Amazon SageMaker Studio
        - Important
        - Note
- Docker support
  - Docker operations supported
        - Topics

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

Amazon SageMaker Studio applications support the use of local mode to create estimators, processors, and pipelines, then deploy them to a local environment. With local mode, you can test machine learning scripts before running them in Amazon SageMaker AI managed training or hosting environments. Studio supports local mode in the following applications:

Amazon SageMaker Studio Classic

Code Editor, based on Code-OSS, Visual Studio Code - Open Source

Local mode in Studio applications is invoked using the SageMaker Python SDK. In Studio applications, local mode functions similarly to how it functions in Amazon SageMaker notebook instances, with some differences. With the Rootless Docker configuration enabled, you can also access additional Docker registries through your VPC configuration, including on-premises repositories, and public registries. For more information about using local mode with the SageMaker Python SDK, see Local Mode.

Studio applications do not support multi-container jobs in local mode. Local mode jobs are limited to a single instance for training, inference, and processing jobs. When creating a local mode job, the instance count configuration must be 1.

As part of local mode support, Studio applications support limited Docker access capabilities. With this support, users can interact with the Docker API from Jupyter notebooks or the image terminal of the application. Customers can interact with Docker using one of the following:

Language specific Docker SDK clients

Studio also supports limited Docker access capabilities with the following restrictions:

Usage of Docker networks is not supported.

Docker volume usage is not supported during container run. Only volume bind mount inputs are allowed during container o

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
http://localhost:port
```

Example 2 (unknown):
```unknown
docker run --net sagemaker parameter-values
```

Example 3 (unknown):
```unknown
parameter-values
```

Example 4 (unknown):
```unknown
docker build --network sagemaker parameter-values
```

---

## Amazon SageMaker Studio Classic UI Overview

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-ui.html#studio-ui-layout

**Contents:**
- Amazon SageMaker Studio Classic UI Overview
        - Important
        - Note
        - Topics
- Amazon SageMaker Studio Classic home page
- Amazon SageMaker Studio Classic layout
  - Left sidebar
  - Left navigation panel
  - Main working area
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic extends the capabilities of JupyterLab with custom resources that can speed up your Machine Learning (ML) process by harnessing the power of AWS compute. Previous users of JupyterLab will notice the similarity of the user interface. The most prominent additions are detailed in the following sections. For an overview of the original JupyterLab interface, see The JupyterLab Interface.

The following image shows the default view upon launching Amazon SageMaker Studio Classic. The left navigation panel displays all top-level categories of features, and a Amazon SageMaker Studio Classic home page is open in the main working area. Come back to this central point of orientation by choosing the Home icon ( ) at any time, then selecting the Home node in the navigation menu.

Try the Getting started notebook for an in-product hands-on guide on how to set up and get familiar with Amazon SageMaker Studio Classic features. On the Quick actions section of the Studio Classic Home page, choose Open the Getting started notebook.

This chapter is based on Studio Classic's updated user interface (UI) available on version v5.38.x and above on JupyterLab3.

To retrieve your version of Studio Classic UI, from the Studio Classic Launcher, open a System Terminal, then

Run conda activate studio

Run jupyter labextension list

Search for the version displayed after @amzn/sagemaker-ui version in the output.

For information about updating Amazon SageMaker Studio Classic, see Shut Down and Update Amazon SageMaker Studio Classic.

Amazon SageMaker Studio Classic home page

Amazon SageMaker Studio Classic layout

The Home page provides access to common tasks and workflows. In particular, it includes a list of Quick actions for common tasks such as Open Launcher to create notebooks and other resources and Import & prepare data visually to create a new flow in Data Wrangler.The Home page also offers tooltips on ke

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
conda activate studio
```

Example 2 (unknown):
```unknown
jupyter labextension list
```

Example 3 (unknown):
```unknown
@amzn/sagemaker-ui version
```

Example 4 (unknown):
```unknown
[user_name]
```

---

## Launch Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launch.html#studio-launch-console-prerequisites

**Contents:**
- Launch Amazon SageMaker Studio Classic
        - Important
        - Important
        - Topics
- Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console
        - Topics
  - Prerequisite
    - Launch Studio Classic from the domain details page
    - Launch Studio Classic from the Studio Classic landing page
- Launch Amazon SageMaker Studio Classic Using the AWS CLI

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

After you have onboarded to an Amazon SageMaker AI domain, you can launch an Amazon SageMaker Studio Classic application from either the SageMaker AI console or the AWS CLI. For more information about onboarding to a domain, see Amazon SageMaker AI domain overview.

Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console

Launch Amazon SageMaker Studio Classic Using the AWS CLI

The process to navigate to Studio Classic from the Amazon SageMaker AI Console differs depending on if Studio Classic or Amazon SageMaker Studio are set as the default experience for your domain. For more information about setting the default experience for your domain, see Migration from Amazon SageMaker Studio Classic.

To complete this procedure, you must onboard to a domain by following the steps in Onboard to Amazon SageMaker AI domain.

Navigate to Studio following the steps in Launch Amazon SageMaker Studio.

From the Studio UI, find the applications pane on the left side.

From the applications pane, select Studio Classic.

From the Studio Classic landing page, select the Studio Classic instance to open.

When Studio Classic is your default experience, you can launch a Amazon SageMaker Studio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--space-name space-name \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200
```

Example 3 (unknown):
```unknown
user-profile-name
```

---

## Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-run-and-manage-change-image.html

**Contents:**
- Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook
        - Important
        - To change a notebook's image or kernel

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

With Amazon SageMaker Studio Classic notebooks, you can change the notebook's image or kernel from within the notebook.

The following screenshot shows the menu from a Studio Classic notebook. The current SageMaker AI kernel and image are displayed as Python 3 (Data Science), where Python 3 denotes the kernel and Data Science denotes the SageMaker AI image that contains the kernel. The color of the circle to the right indicates the kernel is idle or busy. The kernel is busy when the center and the edge of the circle are the same color.

Choose the image/kernel name in the notebook menu.

From the Set up notebook environment pop up window, select the Image or Kernel dropdown menu.

From the dropdown menu, choose one of the images or kernels that are listed.

After choosing an image or kernel, choose Select.

Wait for the kernel's status to show as idle, which indicates the kernel has started.

For a list of available SageMaker images and kernels, see Amazon SageMaker Images Available for Use With Studio Classic Notebooks.

**Examples:**

Example 1 (unknown):
```unknown
Data Science
```

---

## Amazon SageMaker JumpStart in Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-studio-classic.html

**Contents:**
- Amazon SageMaker JumpStart in Studio Classic
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The following JumpStart features are only available in Amazon SageMaker Studio Classic.

Shared Models and Notebooks

End-to-end JumpStart solution templates

Amazon SageMaker JumpStart Industry: Financial

---

## Prepare data using EMR Serverless

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-emr-serverless.html

**Contents:**
- Prepare data using EMR Serverless
        - Important
- Prerequisites
        - Note
        - List of topics

Beginning with SageMaker distribution image version 1.10, Amazon SageMaker Studio integrates with EMR Serverless. Within JupyterLab notebooks in SageMaker Studio, data scientists and data engineers can discover and connect to EMR Serverless applications, then interactively explore, visualize, and prepare large-scale Apache Spark or Apache Hive workloads. This integration allows to perform interactive data preprocessing at scale in preparation for ML model training and deployment.

Specifically, the updated version of the sagemaker-studio-analytics-extension in SageMaker AI distribution image version 1.10 leverages the integration between Apache Livy and EMR Serverless, allowing the connection to an Apache Livy endpoint through JupyterLab notebooks. This section assumes prior knowledge of EMR Serverless interactive applications.

When using Studio, you can only discover and connect to EMR Serverless applications for JupyterLab applications that are launched from private spaces. Ensure that the EMR Serverless applications are located in the same AWS region as your Studio environment.

Before you get started running interactive workloads with EMR Serverless from your JupyterLab notebooks, make sure you meet the following prerequisites:

Your JupyterLab space must use a SageMaker Distribution image version 1.10 or higher.

Create an EMR Serverless interactive application with Amazon EMR version 6.14.0 or higher. You can create an EMR Serverless application from the Studio user interface by following the steps in Create EMR Serverless applications from Studio.

For the simplest setup, you can create your EMR Serverless application in the Studio UI without changing any default settings for the Virtual private cloud (VPC) option. This allows the application to be created within your domain VPC without requiring any networking configuration. In this case, you can skip the following networking setup step.

Review the networking and security requirements in Configure network access for your Amazon EMR cluster. Specifically, ensure that you:

Establish a VPC peering connection between your Studio account and your EMR Serverless account.

Add routes to the private subnet route tables in both accounts.

Set up the security group attached to your Studio domain to allow outbound traffic, and configure the security group of the VPC where you plan to run the EMR Serverless applications to allow inbound TCP traffic from the Studio instance's security group.

To access your 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-studio-analytics-extension
```

---

## Amazon SageMaker Studio Lab

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lab.html

**Contents:**
- Amazon SageMaker Studio Lab
        - Note
        - Topics

As of August 8, 2025, Amazon SageMaker Studio Lab uses JupyterLab 4 instead of JupyterLab 3. If you experience dependency issues, reinstall any extensions that you added to your environments.

Amazon SageMaker Studio Lab is a free service that gives customers access to AWS compute resources, in an environment based on open-source JupyterLab 4. It is based on the same architecture and user interface as Amazon SageMaker Studio Classic, but with a subset of Studio Classic capabilities.

With Studio Lab, you can use AWS compute resources to create and run your Jupyter notebooks without signing up for an AWS account. Because Studio Lab is based on open-source JupyterLab, you can take advantage of open-source Jupyter extensions to run your Jupyter notebooks.

Studio Lab compared to Amazon SageMaker Studio Classic

While Studio Lab provides free access to AWS compute resources, Amazon SageMaker Studio Classic provides the following advanced machine learning capabilities that Studio Lab does not support.

Continuous integration and continuous delivery (Pipelines)

Real-time predictions

Large-scale distributed training

Data preparation (Amazon SageMaker Data Wrangler)

Data labeling (Amazon SageMaker Ground Truth)

Bias analysis (Clarify)

Studio Classic also supports fine-grained access control and security by using AWS Identity and Access Management (IAM), Amazon Virtual Private Cloud (Amazon VPC), and AWS Key Management Service (AWS KMS). Studio Lab does not support these Studio Classic features, nor does it support the use of estimators and built-in SageMaker AI algorithms.

To export your Studio Lab projects for use with Studio Classic, see Export an Amazon SageMaker Studio Lab environment to Amazon SageMaker Studio Classic.

The following topics give information about Studio Lab and how to use it

Amazon SageMaker Studio Lab components overview

Onboard to Amazon SageMaker Studio Lab

Launch your Amazon SageMaker Studio Lab project runtime

Use Amazon SageMaker Studio Lab starter assets

Studio Lab pre-installed environments

Use the Amazon SageMaker Studio Lab project runtime

---

## Lifecycle configurations within Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lifecycle-configurations.html

**Contents:**
- Lifecycle configurations within Amazon SageMaker Studio
        - Important

Lifecycle configurations (LCCs) are scripts that administrators and users can use to automate the customization of the following applications within your Amazon SageMaker Studio environment:

Amazon SageMaker AI JupyterLab

Code Editor, based on Code-OSS, Visual Studio Code - Open Source

Customizing your application includes:

Installing custom packages

Configuring extensions

Setting up source code repositories

Users create and attach built-in lifecycle configurations to their own user profiles. Administrators create and attach default or built-in lifecycle configurations at the domain, space, or user profile level.

Amazon SageMaker Studio first runs the built-in lifecycle configuration and then runs the default LCC. Amazon SageMaker AI won't resolve package conflicts between the user and administrator LCCs. For example, if the built-in LCC installs python3.11 and the default LCC installs python3.12, Studio installs python3.12.

---

## Use Lifecycle Configurations to Customize Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lcc.html

**Contents:**
- Use Lifecycle Configurations to Customize Amazon SageMaker Studio Classic
        - Important
        - Note
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic triggers lifecycle configurations shell scripts during important lifecycle events, such as starting a new Studio Classic notebook. You can use lifecycle configurations to automate customization for your Studio Classic environment. This customization includes installing custom packages, configuring notebook extensions, preloading datasets, and setting up source code repositories.

Using lifecycle configurations gives you flexibility and control to configure Studio Classic to meet your specific needs. For example, you can use customized container images with lifecycle configuration scripts to modify your environment. First, create a minimal set of base container images, then install the most commonly used packages and libraries in those images. After you have completed your images, use lifecycle configurations to install additional packages for specific use cases. This gives you the flexibility to modify your environment across your data science and machine learning teams based on need.

Users can only select lifecycle configuration scripts that they are given access to. While you can give access to multiple lifecycle configuration scripts, you can also set default lifecycle configuration scripts for resources. Based on the resource that the default lifecycle configuration is set for, the default either runs automatically or is the first option shown.

For example lifecycle configuration scripts, see the Studio Classic Lifecycle Configuration examples GitHub repository. For a blog on implementing lifecycle configuration, see Customize Amazon SageMaker Studio Classic using Lifecycle Configurations.

Each script has a limit of 16384 characters.

Create and Associate a Lifecycle Configuration with Amazon SageMaker Studio Classic

Set Default Lifecycle Configurations for Amazon SageMaker Studio Classic

Debug Lifecycle Configurations in Amazon SageMaker Studio Classic

Update and Detach Li

*[Content truncated]*

---

## Debug Lifecycle Configurations in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lcc-debug.html#studio-lcc-debug-logs

**Contents:**
- Debug Lifecycle Configurations in Amazon SageMaker Studio Classic
        - Important
        - Topics
- Verify lifecycle configuration process from CloudWatch Logs
- JupyterServer app failure
- KernelGateway app failure
        - Note
- Lifecycle configuration timeout

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The following topics show how to get information about and debug your lifecycle configurations.

Verify lifecycle configuration process from CloudWatch Logs

JupyterServer app failure

KernelGateway app failure

Lifecycle configuration timeout

Lifecycle configurations only log STDOUT and STDERR.

STDOUT is the default output for bash scripts. You can write to STDERR by appending >&2 to the end of a bash command. For example, echo 'hello'>&2.

Logs for your lifecycle configurations are published to your AWS account using Amazon CloudWatch. These logs can be found in the /aws/sagemaker/studio log stream in the CloudWatch console.

Open the CloudWatch console at https://console.aws.amazon.com/cloudwatch/.

Choose Logs from the left side. From the dropdown menu, select Log groups.

On the Log groups page, search for aws/sagemaker/studio.

Select the log group.

On the Log group details page, choose the Log streams tab.

To find the logs for a specific app, search the log streams using the following format:

For example, to find the lifecycle configuration logs for domain d-m85lcu8vbqmz, space name i-sonic-js, and application type JupyterLab, use the following search string:

If your JupyterServer app crashes because of an issue with the attached lifecycle configuration, Studio Classic displays the following error message on the Studio Classic startup screen.

Select the View script logs link to view the CloudWatch logs for your JupyterServer app.

In the case where the faulty lifecycle configuration is specified in the DefaultResourceSpec of your domain, user profile, or shared space, Studio Classic continues to use the lifecycle configuration even after restarting Studio Classic.

To resolve this error, follow the steps in Set Default Lifecycle Configurations for Amazon SageMaker Studio Classic to remove the lifecycle configuration script from the DefaultResourceSpec or select another script as the default. Then laun

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
echo 'hello'>&2
```

Example 2 (unknown):
```unknown
/aws/sagemaker/studio
```

Example 3 (unknown):
```unknown
aws/sagemaker/studio
```

Example 4 (unknown):
```unknown
domain-id/space-name/app-type/default/LifecycleConfigOnStart
```

---

## Launch Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launch.html

**Contents:**
- Launch Amazon SageMaker Studio Classic
        - Important
        - Important
        - Topics
- Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console
        - Topics
  - Prerequisite
    - Launch Studio Classic from the domain details page
    - Launch Studio Classic from the Studio Classic landing page
- Launch Amazon SageMaker Studio Classic Using the AWS CLI

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

After you have onboarded to an Amazon SageMaker AI domain, you can launch an Amazon SageMaker Studio Classic application from either the SageMaker AI console or the AWS CLI. For more information about onboarding to a domain, see Amazon SageMaker AI domain overview.

Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console

Launch Amazon SageMaker Studio Classic Using the AWS CLI

The process to navigate to Studio Classic from the Amazon SageMaker AI Console differs depending on if Studio Classic or Amazon SageMaker Studio are set as the default experience for your domain. For more information about setting the default experience for your domain, see Migration from Amazon SageMaker Studio Classic.

To complete this procedure, you must onboard to a domain by following the steps in Onboard to Amazon SageMaker AI domain.

Navigate to Studio following the steps in Launch Amazon SageMaker Studio.

From the Studio UI, find the applications pane on the left side.

From the applications pane, select Studio Classic.

From the Studio Classic landing page, select the Studio Classic instance to open.

When Studio Classic is your default experience, you can launch a Amazon SageMaker Studio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--space-name space-name \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200
```

Example 3 (unknown):
```unknown
user-profile-name
```

---

## Amazon SageMaker Autopilot example notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-example-notebooks.html

**Contents:**
- Amazon SageMaker Autopilot example notebooks
        - Note

The following notebooks serve as practical, hands-on examples that address various use cases of Autopilot.

You can find all of Autopilot's notebooks in the autopilot directory of SageMaker AI GitHub examples repository.

We recommend cloning the full Git repository within Studio Classic to access and run the notebooks directly. For information on how to clone a Git repository in Studio Classic, see Clone a Git Repository in Amazon SageMaker Studio Classic.

By default, Autopilot allows deploying generated models to real-time inference endpoints. In this repository, the notebook illustrates how to deploy Autopilot models trained with ENSEMBLING and HYPERPARAMETER OPTIMIZATION (HPO) modes to serverless endpoints. Serverless endpoints automatically launch compute resources and scale them in and out depending on traffic, eliminating the need to choose instance types or manage scaling policies.

Custom feature selection

Autopilot inspects your data set, and runs a number of candidates to figure out the optimal combination of data preprocessing steps, machine learning algorithms, and hyperparameters. You can easily deploy either on a real-time endpoint or for batch processing.

In some cases, you might want to have the flexibility to bring custom data processing code to Autopilot. For example, your datasets might contain a large number of independent variables, and you may wish to incorporate a custom feature selection step to remove irrelevant variables first. The resulting smaller dataset can then be used to launch an Autopilot job. Ultimately, you would also want to include both the custom processing code and models from Autopilot for real-time or batch processing.

While Autopilot streamlines the process of building ML models, MLOps engineers are still responsible for creating, automating, and managing end-to-end ML workflows in production. SageMaker Pipelines can assist in automating various steps of the ML lifecycle, such as data preprocessing, model training, hyperparameter tuning, model evaluation, and deployment. This notebook serves as a demonstration of how to incorporate Autopilot into a SageMaker Pipelines end-to-end AutoML training workflow. To launch an Autopilot experiment within Pipelines, you must create a model-building workflow by writing custom integration code using Pipelines Lambda or Processing steps. For more information, refer to Move Amazon SageMaker Autopilot ML models from experimentation to production using Amazon SageMaker Pipeli

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
HYPERPARAMETER OPTIMIZATION
                (HPO)
```

---

## Data preparation using Amazon EMR

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-emr-cluster.html

**Contents:**
- Data preparation using Amazon EMR
        - Important
        - List of topics

Amazon SageMaker Studio and Amazon SageMaker Studio Classic are two of the machine learning environments that you can use to interact with SageMaker AI.

If your domain was created after November 30, 2023, Studio is your default experience.

If your domain was created before November 30, 2023, Amazon SageMaker Studio Classic is your default experience. To use Studio if Amazon SageMaker Studio Classic is your default experience, see Migration from Amazon SageMaker Studio Classic.

When you migrate from Amazon SageMaker Studio Classic to Amazon SageMaker Studio, there is no loss in feature availability. Studio Classic also exists as an application within Amazon SageMaker Studio to help you run your legacy machine learning workflows.

Amazon SageMaker Studio and Studio Classic come with built-in integration with Amazon EMR. Within JupyterLab and Studio Classic notebooks, data scientists and data engineers can discover and connect to existing Amazon EMR clusters, then interactively explore, visualize, and prepare large-scale data for machine learning using Apache Spark, Apache Hive, or Presto. With a single click, they can access the Spark UI to monitor the status and metrics of their Spark jobs without leaving their notebook.

Administrators can create AWS CloudFormation templates that define Amazon EMR clusters. They can then make those cluster templates available in the AWS Service Catalog for Studio and Studio Classic users to launch. Data scientists can then choose a predefined template to self-provision an Amazon EMR cluster directly from their Studio environment. Administrators can further parameterize the templates to let users choose aspects of the cluster within predefined values. For example, users may want to specify the number of core nodes or select the instance type of a node from a dropdown menu.

Using AWS CloudFormation, administrators can control the organizational, security, and networking setup of Amazon EMR clusters. Data scientists and data engineers can then customize those templates for their workloads to create on-demand Amazon EMR clusters directly from Studio and Studio Classic without setting up complex configurations. Users can terminate Amazon EMR clusters after use.

If you are an administrator:

Ensure that you have enabled communication between Studio or Studio Classic and Amazon EMR clusters. For instructions, see the Configure network access for your Amazon EMR cluster section. Once this communication is enabled, you can:

C

*[Content truncated]*

---

## Use the Amazon SageMaker Studio Classic Launcher

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launcher.html#studio-launcher-launch

**Contents:**
- Use the Amazon SageMaker Studio Classic Launcher
        - Important
        - Topics
- Notebooks and compute resources
        - Note
        - Note
- Utilities and files
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can use the Amazon SageMaker Studio Classic Launcher to create notebooks and text files, and to launch terminals and interactive Python shells.

You can open Studio Classic Launcher in any of the following ways:

Choose Amazon SageMaker Studio Classic at the top left of the Studio Classic interface.

Use the keyboard shortcut Ctrl + Shift + L.

From the Studio Classic menu, choose File and then choose New Launcher.

If the SageMaker AI file browser is open, choose the plus (+) sign in the Studio Classic file browser menu.

In the Quick actions section of the Home tab, choose Open Launcher. The Launcher opens in a new tab. The Quick actions section is visible by default but can be toggled off. Choose Customize Layout to turn this section back on.

The Launcher consists of the following two sections:

Notebooks and compute resources

In this section, you can create a notebook, open an image terminal, or open a Python console.

To create or launch one of those items:

Choose Change environment to select a SageMaker image, a kernel, an instance type, and, optionally, add a lifecycle configuration script that runs on image start-up. For more information on lifecycle configuration scripts, see Use Lifecycle Configurations to Customize Amazon SageMaker Studio Classic. For more information about kernel updates, see Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook.

When you choose an item from this section, you might incur additional usage charges. For more information, see Usage Metering for Amazon SageMaker Studio Classic Notebooks.

The following items are available:

Launches the notebook in a kernel session on the chosen SageMaker image.

Creates the notebook in the folder that you have currently selected in the file browser. To view the file browser, in the left sidebar of Studio Classic, choose the File Browser icon.

Launches the shell in a kernel session on the chosen SageMaker image.

**Examples:**

Example 1 (unknown):
```unknown
Ctrl + Shift + L
```

Example 2 (unknown):
```unknown
ml.t3.medium
```

Example 3 (unknown):
```unknown
ml.g4dn.xlarge
```

Example 4 (unknown):
```unknown
Experiment.create
```

---

## Migrate the UI from Studio Classic to Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-ui.html#studio-updated-migrate-autopilot

**Contents:**
- Migrate the UI from Studio Classic to Studio
- Prerequisites
- Step 1: Update application creation permissions
        - Note
        - Note
- Step 2: Update VPC configuration
- Step 3: Upgrade to the Studio UI
    - Test Studio functionality
    - Clean up test domain resources
        - Note

The first phase for migrating an existing domain involves migrating the UI from Amazon SageMaker Studio Classic to Amazon SageMaker Studio. This phase does not include the migration of data. Users can continue working with their data the same way as they were before migration. For information about migrating data, see (Optional) Migrate data from Studio Classic to Studio.

Phase 1 consists of the following steps:

Update application creation permissions for new applications available in Studio.

Update the VPC configuration for the domain.

Upgrade the domain to use the Studio UI.

Before running these steps, complete the prerequisites in Complete prerequisites to migrate the Studio experience.

Before migrating the domain, update the domain's execution role to grant users permissions to create applications.

Create an AWS Identity and Access Management policy with one of the following contents by following the steps in Creating IAM policies:

Use the following policy to grant permissions for all application types and spaces.

If the domain uses the SageMakerFullAccess policy, you do not need to perform this action. SageMakerFullAccess grants permissions to create all applications.

Because Studio shows an expanded set of applications, users may have access to applications that weren't displayed before. Administrators can limit access to these default applications by creating an AWS Identity and Access Management (IAM) policy that grants denies permissions for some applications to specific users.

Application type can be either jupyterlab or codeeditor.

Attach the policy to the execution role of the domain. For instructions, follow the steps in Adding IAM identity permissions (console).

If you use your domain in VPC-Only mode, ensure your VPC configuration meets the requirements for using Studio in VPC-Only mode. For more information, see Connect Amazon SageMaker Studio in a VPC to External Resources.

Before you migrate your existing domain from Studio Classic to Studio, we recommend creating a test domain using Studio with the same configurations as your existing domain.

Use this test domain to interact with Studio, test out networking configurations, and launch applications, before migrating the existing domain.

Get the domain ID of your existing domain.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

From the left navigation pane, expand Admin configurations and choose Domains.

Choose the existing domain.

On t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
SageMakerFullAccess
```

Example 2 (unknown):
```unknown
SageMakerFullAccess
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "SMStudioUserProfileAppPermissionsCreateAndDelete",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateApp",
                "sagemaker:DeleteApp"
            ],
            "Resource": "arn:aws:sagemaker:us-east-1:111122223333:app/*",
            "Condition": {
                "Null": {
                    "sagemaker:OwnerUserProfileArn": "true"
                }
            }
        },
        {
            "Sid": "SMStudioCreatePresignedDomainUrlForUserProfile",
            "E
...
```

Example 4 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "SMStudioUserProfileAppPermissionsCreateAndDelete",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateApp",
                "sagemaker:DeleteApp"
            ],
            "Resource": "arn:aws:sagemaker:us-east-1:111122223333:app/*",
            "Condition": {
                "Null": {
                    "sagemaker:OwnerUserProfileArn": "true"
                }
            }
        },
        {
            "Sid": "SMStudioCreatePresignedDomainUrlForUserProfile",
            "E
...
```

---

## Launch Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-launch.html#studio-updated-launch-prereq

**Contents:**
- Launch Amazon SageMaker Studio
        - Important
        - Important
        - Topics
- Prerequisites
- Launch from the Amazon SageMaker AI console
- Launch using the AWS CLI

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

This page's topics demonstrate how to launch Amazon SageMaker Studio from the Amazon SageMaker AI console and the AWS Command Line Interface (AWS CLI).

Launch from the Amazon SageMaker AI console

Launch using the AWS CLI

Before you begin, complete the following prerequisites:

Onboard to a SageMaker AI domain with Studio access. If you don't have permissions to set Studio as the default experience for your domain, contact your administrator. For more information, see Amazon SageMaker AI domain overview.

Update the AWS CLI by following the steps in Installing the current AWS CLI Version.

From your local machine, run aws configure and provide your AWS credentials. For information about AWS credentials, see Understanding and getting your AWS credentials.

Complete the following procedure to launch Studio from the Amazon SageMaker AI console.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

From the left navigation pane, choose Studio.

From the Studio landing page, select the domain and user profile for launching Studio.

To launch Studio, choose Launch personal Studio.

This section demonstrates how to launch Studio using the AWS CLI. The procedure to access Studio using the AWS CLI depends if the domain uses AWS Identity and Access Management (IAM) authentication or AWS IAM Identity Center authentication. You can use the AWS CLI to launch Studio by creating a presigned domain URL when your domain uses IAM authen

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200
```

Example 3 (unknown):
```unknown
user-profile-name
```

Example 4 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200 \
--landing-uri studio::
```

---

## Amazon SageMaker Studio Classic Pricing

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-pricing.html

**Contents:**
- Amazon SageMaker Studio Classic Pricing
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

When the first member of your team onboards to Amazon SageMaker Studio Classic, Amazon SageMaker AI creates an Amazon Elastic File System (Amazon EFS) volume for the team. When this member, or any member of the team, opens Studio Classic, a home directory is created in the volume for the member. A storage charge is incurred for this directory. Subsequently, additional storage charges are incurred for the notebooks and data files stored in the member's home directory. For pricing information on Amazon EFS, see Amazon EFS Pricing.

Additional costs are incurred when other operations are run inside Studio Classic, for example, running a notebook, running training jobs, and hosting a model.

For information on the costs associated with using Studio Classic notebooks, see Usage Metering for Amazon SageMaker Studio Classic Notebooks.

For information about billing along with pricing examples, see Amazon SageMaker Pricing.

If Amazon SageMaker Studio is your default experience, see Amazon SageMaker Studio pricing for more pricing information.

---

## Amazon SageMaker Studio Classic Tour

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-end-to-end.html

**Contents:**
- Amazon SageMaker Studio Classic Tour
        - Important
        - To clone the repository
        - To navigate to the sample notebook
        - Note

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

For a walkthrough that takes you on a tour of the main features of Amazon SageMaker Studio Classic, see the xgboost_customer_churn_studio.ipynb sample notebook from the aws/amazon-sagemaker-examples GitHub repository. The code in the notebook trains multiple models and sets up the SageMaker Debugger and SageMaker Model Monitor. The walkthrough shows you how to view the trials, compare the resulting models, show the debugger results, and deploy the best model using the Studio Classic UI. You don't need to understand the code to follow this walkthrough.

To run the notebook for this tour, you need:

An IAM account to sign in to Studio. For information, see Amazon SageMaker AI domain overview.

Basic familiarity with the Studio user interface and Jupyter notebooks. For information, see Amazon SageMaker Studio Classic UI Overview.

A copy of the aws/amazon-sagemaker-examples repository in your Studio environment.

Launch Studio Classic following the steps in Launch Amazon SageMaker Studio Classic For users in IAM Identity Center, sign in using the URL from your invitation email.

On the top menu, choose File, then New, then Terminal.

At the command prompt, run the following command to clone the aws/amazon-sagemaker-examples GitHub repository.

From the File Browser on the left menu, select amazon-sagemaker-examples.

Navigate to the example notebook with the following path.

~/amazon-sagemaker-examples/aws_sagemaker_studio/getting_started/xgboost_customer_churn_studio.ipynb

Follow the notebook to learn about Studio Classic's main features.

If you encounter an error when you run the sample notebook, and some time has passed from when you cloned the repository, review the notebook on the remote repository for updates.

**Examples:**

Example 1 (unknown):
```unknown
$ git clone https://github.com/aws/amazon-sagemaker-examples.git
```

Example 2 (unknown):
```unknown
~/amazon-sagemaker-examples/aws_sagemaker_studio/getting_started/xgboost_customer_churn_studio.ipynb
```

---

## Stop a Training Job in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-stop-training-job.html

**Contents:**
- Stop a Training Job in Amazon SageMaker Studio Classic
        - Important
        - To stop a training job

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

You can stop a training job with the Amazon SageMaker Studio Classic UI. When you stop a training job, its status changes to Stopping at which time billing ceases. An algorithm can delay termination in order to save model artifacts after which the job status changes to Stopped. For more information, see the stop_training_job method in the AWS SDK for Python (Boto3).

Follow the View experiments and runs procedure on this page until you open the Describe Trial Component tab.

At the upper-right side of the tab, choose Stop training job. The Status at the top left of the tab changes to Stopped.

To view the training time and billing time, choose AWS Settings.

---

## Using Amazon SageMaker Feature Store in the console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-use-with-studio.html#feature-store-view-feature-processor-pipeline-lineage-studio

**Contents:**
- Using Amazon SageMaker Feature Store in the console
        - Important
        - Topics
- Create a feature group from the console
- View feature group details from the console
- Update a feature group from the console
- View pipeline executions from the console
- View lineage from the console

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

You can use Amazon SageMaker Feature Store on the console to create, view, update, and monitor your feature groups. Monitoring in this guide includes viewing pipeline executions and lineage of your feature groups. This guide provides instructions on how to achieve these tasks from the console.

For Feature Store examples and resources using the Amazon SageMaker APIs and AWS SDK for Python (Boto3), see Amazon SageMaker Feature Store resources.

Create a feature group from the console

View feature group details from the console

Update a feature group from the console

View pipeline executions from the console

View lineage from the console

The create feature group process has four steps:

Enter feature group information.

Enter feature definitions.

Enter required features.

Enter feature group tags.

Consider which of the following options fits your use case:

Create an online store, an offline store, or both. For more information about the differences between online and offline stores, see Feature Store concepts.

Use a default AWS Key Management Service key or your own KMS key. The default key is AWS KMS key (SSE-KMS). You can reduce AWS KMS request costs by configuring use of Amazon S3 Bucket Keys on the offline store Amazon S3 bucket. The Amazon S3 Bucket Key must be enabled before using the bucket for your feature groups. For more information about reducing the cost by using Amazon S3 Bucket Keys, see Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys.

You can use the same key for both online and offline stores, or have a unique key for each. For more information about AWS KMS, see AWS Key Management Service.

If you create an offline store:

Decide if you want to create an Amazon S3 bucket or use an existing one. When usin

*[Content truncated]*

---

## Explore the Amazon SageMaker Debugger Insights dashboard

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-on-studio-insights-walkthrough.html

**Contents:**
- Explore the Amazon SageMaker Debugger Insights dashboard
        - Note
        - Important
        - Important
        - Topics
- System metrics
  - Resource utilization summary
  - Resource utilization time series plots
- Rules

When you initiate a SageMaker training job, SageMaker Debugger starts monitoring the resource utilization of the Amazon EC2 instances by default. You can track the system utilization rates, statistics overview, and built-in rule analysis through the Insights dashboard. This guide walks you through the content of the SageMaker Debugger Insights dashboard under the following tabs: System Metrics and Rules.

The SageMaker Debugger Insights dashboard runs a Studio Classic application on an ml.m5.4xlarge instance to process and render the visualizations. Each SageMaker Debugger Insights tab runs one Studio Classic kernel session. Multiple kernel sessions for multiple SageMaker Debugger Insights tabs run on the single instance. When you close a SageMaker Debugger Insights tab, the corresponding kernel session is also closed. The Studio Classic application remains active and accrues charges for the ml.m5.4xlarge instance usage. For information about pricing, see the Amazon SageMaker Pricing page.

When you are done using the SageMaker Debugger Insights dashboard, shut down the ml.m5.4xlarge instance to avoid accruing charges. For instructions on how to shut down the instance, see Shut down the Amazon SageMaker Debugger Insights instance.

In the reports, plots and recommendations are provided for informational purposes and are not definitive. You are responsible for making your own independent assessment of the information.

In the System Metrics tab, you can use the summary table and timeseries plots to understand resource utilization.

This summary table shows the statistics of compute resource utilization metrics of all nodes (denoted as algo-n). The resource utilization metrics include the total CPU utilization, the total GPU utilization, the total CPU memory utilization, the total GPU memory utilization, the total I/O wait time, and the total network in bytes. The table shows the minimum and the maximum values, and p99, p90, and p50 percentiles.

Use the time series graphs to see more details of resource utilization and identify at what time interval each instance shows any undesired utilization rate, such as low GPU utilization and CPU bottlenecks that can cause a waste of the expensive instance.

The time series graph controller UI

The following screenshot shows the UI controller for adjusting the time series graphs.

algo-1: Use this dropdown menu to choose the node that you want to look into.

Zoom In: Use this button to zoom in the time series graphs a

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ml.m5.4xlarge
```

Example 2 (unknown):
```unknown
ml.m5.4xlarge
```

Example 3 (unknown):
```unknown
ml.m5.4xlarge
```

Example 4 (unknown):
```unknown
ml.p3.16xlarge
```

---

## Migration from Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate.html

**Contents:**
- Migration from Amazon SageMaker Studio Classic
        - Important
        - Note
- Automatic migration
        - Topics

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

When you open Amazon SageMaker Studio, the web-based UI is based on the chosen default experience. Amazon SageMaker AI currently supports two different default experiences: the Amazon SageMaker Studio experience and the Amazon SageMaker Studio Classic experience. To access the latest Amazon SageMaker Studio features, you must migrate existing domains from the Amazon SageMaker Studio Classic experience. When you migrate your default experience from Studio Classic to Studio, you don't lose any features, and can still access the Studio Classic IDE within Studio. For information about the added benefits of the Studio experience, see Amazon SageMaker Studio.

For existing customers that created their accounts before November 30, 2023, Studio Classic may be the default experience. You can enable Studio as your default experience using the AWS Command Line Interface (AWS CLI) or the Amazon SageMaker AI console. For more information about Studio Classic, see Amazon SageMaker Studio Classic.

For customers that created their accounts after November 30, 2023, we recommend using Studio as the default experience because it contains various integrated development environments (IDEs), including the Studio Classic IDE, and other new features.

JupyterLab 3 reached its end of maintenance date on May 15, 2024. After December 31, 2024, you can only create new Studio Classic notebooks on JupyterLab 3 for a limited period. However after December 31, 2024, SageMaker AI will no longer provide fixes for critical issues on Studio Classic notebooks on JupyterLab 3. We recommend that you migrate your workloads to the new Studio experience, which supports JupyterLab 4.

If Studio is your default experience, the UI is similar to the images found in Amazon SageMake

*[Content truncated]*

---

## Configure network access for your Amazon EMR cluster

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-emr-networking.html

**Contents:**
- Configure network access for your Amazon EMR cluster
        - Note
- Studio and Amazon EMR are in separate VPCs
        - VPC peering
        - Routing tables
        - Security groups
- Studio and Amazon EMR are in the same VPC
- Studio and Amazon EMR communicate over public internet
        - Note

Before you get started with using Amazon EMR or EMR Serverless for your data preparation tasks in Studio, ensure that you or your administrator have configured your network to allow communication between Studio and Amazon EMR. Once this communication is enabled, you can choose to:

Prepare data using EMR Serverless

Data preparation using Amazon EMR

For EMR Serverless users, the simplest setup involves creating your application in the Studio UI without modifying the default settings for the Virtual private cloud (VPC) option. This approach allows the application to be created within your SageMaker domain's VPC, eliminating the need for additional networking configuration. If you choose this option, you can skip the following networking setup section.

The networking instructions vary based on whether Studio and Amazon EMR are deployed within a private Amazon Virtual Private Cloud (VPC) or communicate over the internet.

By default, Studio or Studio Classic run in an AWS managed VPC with internet access. When using an internet connection, Studio and Studio Classic access AWS resources, such as Amazon S3 buckets, over the internet. However, if you have security requirements to control access to your data and job containers, we recommend that you configure Studio or Studio Classic and Amazon EMR so that your data and containers aren’t accessible over the internet. To control access to your resources or run Studio or Studio Classic without public internet access, you can specify the VPC only network access type when you onboard to Amazon SageMaker AI domain. In this scenario, both Studio and Studio Classic establish connections with other AWS services via private VPC endpoints. For information about configuring Studio or Studio Classic in VPC only mode, see Connect SageMaker Studio or Studio Classic notebooks in a VPC to external resources..

The first two sections describe how to ensure communication between Studio or Studio Classic and Amazon EMR in VPCs without public internet access. The last section covers how to ensure communication between Studio or Studio Classic and Amazon EMR using an internet connection. Prior to connecting Studio or Studio Classic and Amazon EMR without internet access, make sure to establish endpoints for Amazon Simple Storage Service (data storage), Amazon CloudWatch (logging and monitoring), and Amazon SageMaker Runtime (fine-grained role-based access control (RBAC)).

To connect Studio or Studio Classic and Amazon EMR:

If Stu

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
10.0.20.0/24
```

---

## (Optional) Migrate data from Studio Classic to Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-migrate-data.html#studio-updated-migrate-flows

**Contents:**
- (Optional) Migrate data from Studio Classic to Studio
- Manually migrate all of your data from Studio Classic
  - Prerequisites
  - Choosing an approach
        - Note
- Migrate data flows from Data Wrangler
  - Prerequisites
  - One-click migration method
        - Warning
  - Manual migration method

Studio Classic and Studio use two different types of storage volumes. Studio Classic uses a single Amazon Elastic File System (Amazon EFS) volume to store data across all users and shared spaces in the domain. In Studio, each space gets its own Amazon Elastic Block Store (Amazon EBS) volume. When you update the default experience of an existing domain, SageMaker AI automatically mounts a folder in an Amazon EFS volume for each user in a domain. As a result, users are able to access files from Studio Classic in their Studio applications. For more information, see Amazon EFS auto-mounting in Studio.

You can also opt out of Amazon EFS auto-mounting and manually migrate the data to give users access to files from Studio Classic in Studio applications. To accomplish this, you must transfer the files from the user home directories to the Amazon EBS volumes associated with those spaces. The following section gives information about this workflow. For more information about opting out of Amazon EFS auto-mounting, see Opt out of Amazon EFS auto-mounting.

The following section describes how to migrate all of the data from your Studio Classic storage volume to the new Studio experience.

When manually migrating a user's data, code, and artifacts from Studio Classic to Studio, we recommend one of the following approaches:

Using a custom Amazon EFS volume

Using Amazon Simple Storage Service (Amazon S3)

If you used Amazon SageMaker Data Wrangler in Studio Classic and want to migrate your data flow files, then choose one of the following options for migration:

If you want to migrate all of the data from your Studio Classic storage volume, including your data flow files, go to Manually migrate all of your data from Studio Classic and complete the section Use Amazon S3 to migrate data. Then, skip to the Import the flow files into Canvas section.

If you only want to migrate your data flow files and no other data from your Studio Classic storage volume, skip to the Migrate data flows from Data Wrangler section.

Before running these steps, complete the prerequisites in Complete prerequisites to migrate the Studio experience. You must also complete the steps in Migrate the UI from Studio Classic to Studio.

Consider the following when choosing an approach to migrate your Studio Classic data.

Pros and cons of using a custom Amazon EFS volume

In this approach, you use an Amazon EFS-to-Amazon EFS AWS DataSync task (one time or cadence) to copy data, then mount the targe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export SOURCE_DOMAIN_ID="domain-id"
export AWS_REGION="region"

export TARGET_EFS=$(aws efs create-file-system --performance-mode generalPurpose --throughput-mode bursting --encrypted --region $REGION | jq -r '.FileSystemId')

echo "Target EFS volume Created: $TARGET_EFS"
```

Example 2 (unknown):
```unknown
export SOURCE_EFS=$(aws sagemaker describe-domain --domain-id $SOURCE_DOMAIN_ID | jq -r '.HomeEfsFileSystemId')
export VPC_ID=$(aws sagemaker describe-domain --domain-id $SOURCE_DOMAIN_ID | jq -r '.VpcId')

echo "EFS managed by SageMaker: $SOURCE_EFS | VPC: $VPC_ID"
```

Example 3 (unknown):
```unknown
export EFS_VPC_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].VpcId")
export EFS_AZ_NAME=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].AvailabilityZoneName")
export EFS_AZ_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].AvailabilityZoneId")
export EFS_SUBNET_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[0].SubnetId")
export EFS_MOUNT_TARG_ID=$(aws efs describe-mount-targets --file-system-id $SOURCE_EFS | jq -r ".MountTargets[
...
```

Example 4 (unknown):
```unknown
export SOURCE_EFS_ARN=$(aws efs describe-file-systems --file-system-id $SOURCE_EFS | jq -r ".FileSystems[0].FileSystemArn")
export TARGET_EFS_ARN=$(aws efs describe-file-systems --file-system-id $TARGET_EFS | jq -r ".FileSystems[0].FileSystemArn")
export EFS_SUBNET_ID_ARN=$(aws ec2 describe-subnets --subnet-ids $EFS_SUBNET_ID | jq -r ".Subnets[0].SubnetArn")
export ACCOUNT_ID=$(aws ec2 describe-security-groups --group-id $EFS_SG_IDS | jq -r ".SecurityGroups[0].OwnerId")
export EFS_SG_ID_ARN=arn:aws:ec2:$REGION:$ACCOUNT_ID:security-group/$EFS_SG_IDS

export SOURCE_LOCATION_ARN=$(aws datasync cr
...
```

---

## Create or Open an Amazon SageMaker Studio Classic Notebook

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-create-open.html

**Contents:**
- Create or Open an Amazon SageMaker Studio Classic Notebook
        - Important
        - Important
        - Note
        - Topics
- Open a notebook in Studio Classic
        - To open a notebook
- Create a Notebook from the File Menu
        - To create a notebook from the File menu
- Create a Notebook from the Launcher

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

When you Create a Notebook from the File Menu in Amazon SageMaker Studio Classic or Open a notebook in Studio Classic for the first time, you are prompted to set up your environment by choosing a SageMaker image, a kernel, an instance type, and, optionally, a lifecycle configuration script that runs on image start-up. SageMaker AI launches the notebook on an instance of the chosen type. By default, the instance type is set to ml.t3.medium (available as part of the AWS Free Tier) for CPU-based images. For GPU-based images, the default instance type is ml.g4dn.xlarge.

If you create or open additional notebooks that use the same instance type, whether or not the notebooks use the same kernel, the notebooks run on the same instance of that instance type.

After you launch a notebook, you can change its instance type, SageMaker image, and kernel from within the notebook. For more information, see Change the Instance Type for an Amazon SageMaker Studio Classic Notebook and Change the Image or a Kernel for an Amazon SageMaker Studio Classic Notebook.

You can have only one instance of each instance type. Each instance can have multiple SageMaker images running on it. Each SageMaker image can run multi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ml.t3.medium
```

Example 2 (unknown):
```unknown
ml.g4dn.xlarge
```

Example 3 (unknown):
```unknown
Ctrl + Shift +
            L
```

---

## Launch an Amazon EMR cluster from Studio or Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-launch-emr-cluster-from-template.html

**Contents:**
- Launch an Amazon EMR cluster from Studio or Studio Classic

Data scientists and data engineers can self-provision Amazon EMR clusters from Studio or Studio Classic using AWS CloudFormation templates set up by their administrators. Before users can launch a cluster, administrators must have configured the necessary settings in the Studio environment. For information on how administrators can configure a Studio environment to allow self-provisioning Amazon EMR clusters, see Configure Amazon EMR CloudFormation templates in the Service Catalog.

To provision a new Amazon EMR cluster from Studio or Studio Classic:

In the Studio or Studio Classic UI's left-side panel, select the Data node in the left navigation menu. Navigate down to Amazon EMR Clusters. This opens up a page listing the Amazon EMR clusters that you can access from Studio or Studio Classic.

Choose the Create button at the top right corner. This opens up a new modal listing the cluster templates available to you.

Select a cluster template by choosing a template name and then choose Next.

Enter the cluster's details, such as a cluster name and any specific configurable parameter set by your administrator, and then choose Create cluster. The creation of the cluster might take a couple of minutes.

Once the cluster is provisioned, the Studio or Studio Classic UI displays a The cluster has been successfully created message.

To connect to your cluster, see Connect to an Amazon EMR cluster from SageMaker Studio or Studio Classic

---

## Videos: Use Autopilot to automate and explore the machine learning process

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-videos.html

**Contents:**
- Videos: Use Autopilot to automate and explore the machine learning process
        - Topics
- Start an AutoML job with Amazon SageMaker Autopilot
- Review data exploration and feature engineering automated in Autopilot.
- Tune models to optimize performance
- Choose and deploy the best model
- Amazon SageMaker Autopilot tutorial

Here is a video series that provides a tour of Amazon SageMaker Autopilot capabilities using Studio Classic. They show how to start an AutoML job, analyze and preprocess data, how to do feature engineering and hyperparameter optimization on candidate models, and how to visualize and compare the resulting model metrics.

Start an AutoML job with Amazon SageMaker Autopilot

Review data exploration and feature engineering automated in Autopilot.

Tune models to optimize performance

Choose and deploy the best model

Amazon SageMaker Autopilot tutorial

This video shows you to how to start an AutoML job with Autopilot. (Length: 8:41)

This video shows you how to review the data exploration and candidate definition notebooks generated by Amazon SageMaker Autopilot. (Length: 10:04)

This video shows you how to optimize model performance during training using hyperparameter tuning. (Length: 4:59)

This video shows you how to use job metrics to choose the best model and then how to deploy it. (Length: 5:20)

This video walks you through an end to end demo where we first build a binary classification model automatically with Amazon SageMaker Autopilot. We see how candidate models have been built and optimized using auto-generated notebooks. We also look at the top candidates with Amazon SageMaker Experiments. Finally, we deploy the top candidate (based on XGBoost), and configure data capture with SageMaker Model Monitor.

---

## Connecting to HyperPod clusters and submitting tasks to clusters

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-studio-open.html

**Contents:**
- Connecting to HyperPod clusters and submitting tasks to clusters

You can launch machine learning workloads on HyperPod clusters within Amazon SageMaker Studio IDEs. When you launch Studio IDEs on a HyperPod cluster, a set of commands are available to help you get started. You can work on your training scripts, use Docker containers for the training scripts, and submit jobs to the cluster, all from within the Studio IDEs. The following section provides information on how to connect your cluster to Studio IDEs.

In Amazon SageMaker Studio you can navigate to one of your clusters in HyperPod clusters (under Compute) and view your list of clusters. You can connect your cluster to an IDE listed under Actions.

You can also choose your custom file system from the list of options. For information on how to get this set up, see Setting up HyperPod in Studio.

Alternatively, you can create a space and launch an IDE using the AWS CLI. Use the following commands to do so. The following example creates a Private JupyterLab space for user-profile-name with the fs-id FSx for Lustre file system attached.

Create a space using the create-space AWS CLI.

Create the app using the create-app AWS CLI.

Once you have your applications open, you can submit tasks directly to the clusters you are connected to.

**Examples:**

Example 1 (unknown):
```unknown
user-profile-name
```

Example 2 (unknown):
```unknown
user-profile-name
```

Example 3 (unknown):
```unknown
create-space
```

Example 4 (unknown):
```unknown
aws sagemaker create-space \
--region your-region \
--ownership-settings "OwnerUserProfileName=user-profile-name" \
--space-sharing-settings "SharingType=Private" \
--space-settings "AppType=JupyterLab,CustomFileSystems=[{FSxLustreFileSystem={FileSystemId=fs-id}}]"
```

---

## Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html

**Contents:**
- Amazon SageMaker Studio Classic
        - Important
- Amazon SageMaker Studio Classic maintenance phase plan
        - Note
        - Topics
- Amazon SageMaker Studio Classic Features

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker Studio Classic is a web-based integrated development environment (IDE) for machine learning (ML). Studio Classic lets you build, train, debug, deploy, and monitor your ML models. Studio Classic includes all of the tools you need to take your models from data preparation to experimentation to production with increased productivity. In a single visual interface, you can do the following tasks:

Write and run code in Jupyter notebooks

Prepare data for machine learning

Build and train ML models

Deploy the models and monitor the performance of their predictions

Track and debug ML experiments

Collaborate with other users in real time

For information on the onboarding steps for Studio Classic, see Amazon SageMaker AI domain overview.

For information about collaborating with other users in real time, see Collaboration with shared spaces.

For the AWS Regions supported by Studio Classic, see Supported Regions and Quotas.

The following table gives information about the timeline for when Amazon SageMaker Studio Classic entered its extended maintenance phase.

Starting December 31st, Studio Classic reaches end of maintenance. At this point, Studio Classic will no longer receive updates and security fixes. All new domains will be created with Amazon SageMaker Studio as the default.

Starting January 31st, users will no longer be able to create new JupyterLab 3 notebooks in Studio Classic. Users will also not be able to restart or update existing notebooks. Users will be able to access existing Studio Classic applications from Studio only to delete or stop existing notebooks.

Your existing Studio Classic domain is not automatically migrated to Studio. For information about migrating, see Migration from Amazon SageMaker Studio Classic.

Amazon SageMaker Studio Classic Features

Amazon SageMaker Studio Classic UI Overview

Launch Amazon SageMaker Studio Classic

JupyterLab Versioning in Amazon SageMaker S

*[Content truncated]*

---

## Shut Down and Update Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tasks-update-studio.html

**Contents:**
- Shut Down and Update Amazon SageMaker Studio Classic
        - Important
        - Important
        - Note

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

To update Amazon SageMaker Studio Classic to the latest release, you must shut down the JupyterServer app. You can shut down the JupyterServer app from the SageMaker AI console, from Amazon SageMaker Studio or from within Studio Classic. After the JupyterServer app is shut down, you must reopen Studio Classic through the SageMaker AI console or from Studio which creates a new version of the JupyterServer app.

You cannot delete the JupyterServer application while the Studio Classic UI is still open in the browser. If you delete the JupyterServer application while the Studio Classic UI is still open in the browser, SageMaker AI automatically re-creates the JupyterServer application.

Any unsaved notebook information is lost in the process. The user data in the Amazon EFS volume isn't impacted.

Some of the services within Studio Classic, like Data Wrangler, run on their own app. To update these services you must delete the app for that service. To learn more, see Shut Down and Update Amazon SageMaker Studio Classic Apps.

A JupyterServer app is associated with a single Studio Classic user. When you update the app for one user it doesn't affect other users.

The following page shows how to update 

*[Content truncated]*

---

## Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated.html

**Contents:**
- Amazon SageMaker Studio
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

Amazon SageMaker Studio is the latest web-based experience for running ML workflows. Studio offers a suite of integrated development environments (IDEs). These include Code Editor, based on Code-OSS, Visual Studio Code - Open Source, a new JupyterLab application, RStudio, and Amazon SageMaker Studio Classic. For more information, see Applications supported in Amazon SageMaker Studio.

The new web-based UI in Studio is faster and provides access to all SageMaker AI resources, including jobs and endpoints, in one interface. ML practitioners can also choose their preferred IDE to accelerate ML development. A data scientist can use JupyterLab to explore data and tune models. In addition, a machine learning operations (MLOps) engineer can use Code Editor with the pipelines tool in Studio to deploy and monitor models in production.

The previous Studio experience is still being supported as Amazon SageMaker Studio Classic. Studio Classic is the default experience for existing customers, and is available as an application in Studio. For more information about Studio Classic, see Amazon SageMaker Studio Classic. For information about how to migrate from Studio Classic to Studio, see Migration from Amazon SageMaker Studio Classic.

Studio offers the following benefits:

A new JupyterLab application that has a faster start-up time and is more reliable than the existing Studio Classic application. For more information, see SageMaker JupyterLab.

A suite of IDEs that open in a separate tab, including the new Code Editor, based on Code-OSS, Visual Studio Code - Open Source application. Users can interact with supported IDEs in a full screen experience. For more information, see Applications supported in Amazon SageMaker Studio.

Access to all of your SageMaker AI resources in one place. Studio displays running instances across all of your applications.

Access to all training jobs in a single view, regardless of whether they were scheduled from notebooks or initiated from Amazon SageMaker JumpStart.

Simplified model deployment workflows and endpoint management and monitoring directly from Studio. You don't need to access the SageMaker AI console.

Automatic creation of all configure

*[Content truncated]*

---

## Usage Metering for Amazon SageMaker Studio Classic Notebooks

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebooks-usage-metering.html

**Contents:**
- Usage Metering for Amazon SageMaker Studio Classic Notebooks
        - Important
        - From the Studio Classic Launcher
        - From the File menu
        - Important

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

There is no additional charge for using Amazon SageMaker Studio Classic. The costs incurred for running Amazon SageMaker Studio Classic notebooks, interactive shells, consoles, and terminals are based on Amazon Elastic Compute Cloud (Amazon EC2) instance usage.

When you run the following resources, you must choose a SageMaker image and kernel:

When launched, the resource is run on an Amazon EC2 instance of the chosen instance type. If an instance of that type was previously launched and is available, the resource is run on that instance.

For CPU based images, the default suggested instance type is ml.t3.medium. For GPU based images, the default suggested instance type is ml.g4dn.xlarge.

The costs incurred are based on the instance type. You are billed separately for each instance.

Metering starts when an instance is created. Metering ends when all the apps on the instance are shut down, or the instance is shut down. For information about how to shut down an instance, see Shut Down Resources from Amazon SageMaker Studio Classic.

You must shut down the instance to stop incurring charges. If you shut down the notebook running on the instance but don't shut down the instance, you will still incur charges. When you shut down the Studio Classic notebook instances, any additional resources, such as SageMaker AI endpoints, Amazon EMR clusters, and Amazon S3 buckets created from Studio Classic are not deleted. Delete those resources to stop accrual of charges.

When you open multiple notebooks on the same instance type, the notebooks run on the same instance even if they are using different kernels. You are billed only for the time that one instance is running.

You can change the instance type from within the notebook after you open it. For more information, see Change the Instance Type for an Amazon SageMaker Studio Classic Notebook.

For information about billing along with pricing examples, see Amazon SageMaker Pr

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ml.t3.medium
```

Example 2 (unknown):
```unknown
ml.g4dn.xlarge
```

---

## Use TensorBoard in Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-tensorboard.html

**Contents:**
- Use TensorBoard in Amazon SageMaker Studio Classic
        - Important
        - Note
- Prerequisites
- Set Up TensorBoardCallback
- Install TensorBoard
- Launch TensorBoard

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

The following doc outlines how to install and run TensorBoard in Amazon SageMaker Studio Classic.

This guide shows how to open the TensorBoard application through a SageMaker Studio Classic notebook server of an individual SageMaker AI domain user profile. For a more comprehensive TensorBoard experience integrated with SageMaker Training and the access control functionalities of SageMaker AI domain, see TensorBoard in Amazon SageMaker AI.

This tutorial requires a SageMaker AI domain. For more information, see Amazon SageMaker AI domain overview

Launch Studio Classic, and open the Launcher. For more information, see Use the Amazon SageMaker Studio Classic Launcher

In the Amazon SageMaker Studio Classic Launcher, under Notebooks and compute resources, choose the Change environment button.

On the Change environment dialog, use the dropdown menus to select the TensorFlow 2.6 Python 3.8 CPU Optimized Studio Classic Image.

Back to the Launcher, click the Create notebook tile. Your notebook launches and opens in a new Studio Classic tab.

Run this code from within your notebook cells.

Import the required packages.

Create a Keras model.

Create a directory for your TensorBoard logs

Run training with TensorBoard.

Generate the EFS path for the TensorBoard logs. You use this path to set up your logs from the terminal.

Retrieve the EFS_PATH_LOG_DIR. You will need it in the TensorBoard installation section.

Click on the Amazon SageMaker Studio Classic button on the top left corner of Studio Classic to open the Amazon SageMaker Studio Classic Launcher. This launcher must be opened from your root directory. For more information, see Use the Amazon SageMaker Studio Classic Launcher

In the Launcher, under Utilities and files, click System terminal.

From the terminal, run the following commands. Copy EFS_PATH_LOG_DIR from the Jupyter notebook. You must run this from the /home/sagemaker-user root directory.

To launch T

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TensorBoardCallback
```

Example 2 (unknown):
```unknown
Notebooks and compute resources
```

Example 3 (unknown):
```unknown
TensorFlow 2.6 Python 3.8 CPU Optimized
```

Example 4 (unknown):
```unknown
import os
import datetime
import tensorflow as tf
```

---

## User guide

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-emr-user-guide.html

**Contents:**
- User guide
        - Topics
- Supported images and kernels to connect to an Amazon EMR cluster from Studio or Studio Classic
- Bring your own image

This section covers how data scientist and data engineers can launch, discover, connect to, or terminate an Amazon EMR cluster from Studio or Studio Classic.

Before users can list or launch clusters, administrators must have configured the necessary settings in the Studio environment. For information on how administrators can configure a Studio environment to allow self-provisioning and listing of Amazon EMR clusters, see Admin guide.

Supported images and kernels to connect to an Amazon EMR cluster from Studio or Studio Classic

Launch an Amazon EMR cluster from Studio or Studio Classic

List Amazon EMR clusters from Studio or Studio Classic

Connect to an Amazon EMR cluster from SageMaker Studio or Studio Classic

Terminate an Amazon EMR cluster from Studio or Studio Classic

Access Spark UI from Studio or Studio Classic

The following images and kernels come with sagemaker-studio-analytics-extension, the JupyterLab extension that connects to a remote Spark (Amazon EMR) cluster via the SparkMagic library using Apache Livy.

For Studio users: SageMaker Distribution is a Docker environment for data science used as the default image of JupyterLab notebook instances. All versions of SageMaker AI Distribution come with sagemaker-studio-analytics-extension pre-installed.

For Studio Classic users: The following images come pre-installed with sagemaker-studio-analytics-extension:

DataScience – Python 3 kernel

DataScience 2.0 – Python 3 kernel

DataScience 3.0 – Python 3 kernel

SparkAnalytics 1.0 – SparkMagic and PySpark kernels

SparkAnalytics 2.0 – SparkMagic and PySpark kernels

SparkMagic – SparkMagic and PySpark kernels

PyTorch 1.8 – Python 3 kernels

TensorFlow 2.6 – Python 3 kernel

TensorFlow 2.11 – Python 3 kernel

To connect to Amazon EMR clusters using another built-in image or your own image, follow the instructions in Bring your own image.

To bring your own image in Studio or Studio Classic and allow your notebooks to connect to Amazon EMR clusters, install the following sagemaker-studio-analytics-extension extension to your kernel. It supports connecting SageMaker Studio or Studio Classic notebooks to Spark(Amazon EMR) clusters through the SparkMagic library.

Additionally, to connect to Amazon EMR with Kerberos authentication, you must install the kinit client. Depending on your OS, the command to install the kinit client can vary. To bring an Ubuntu (Debian based) image, use the apt-get install -y -qq krb5-user command.

For more informatio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-studio-analytics-extension
```

Example 2 (unknown):
```unknown
sagemaker-studio-analytics-extension
```

Example 3 (unknown):
```unknown
pip install sparkmagic
pip install sagemaker-studio-sparkmagic-lib
pip install sagemaker-studio-analytics-extension
```

Example 4 (unknown):
```unknown
apt-get
                install -y -qq krb5-user
```

---

## Using Amazon SageMaker Feature Store in the console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-use-with-studio.html#feature-store-view-feature-processor-pipeline-executions-studio

**Contents:**
- Using Amazon SageMaker Feature Store in the console
        - Important
        - Topics
- Create a feature group from the console
- View feature group details from the console
- Update a feature group from the console
- View pipeline executions from the console
- View lineage from the console

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

You can use Amazon SageMaker Feature Store on the console to create, view, update, and monitor your feature groups. Monitoring in this guide includes viewing pipeline executions and lineage of your feature groups. This guide provides instructions on how to achieve these tasks from the console.

For Feature Store examples and resources using the Amazon SageMaker APIs and AWS SDK for Python (Boto3), see Amazon SageMaker Feature Store resources.

Create a feature group from the console

View feature group details from the console

Update a feature group from the console

View pipeline executions from the console

View lineage from the console

The create feature group process has four steps:

Enter feature group information.

Enter feature definitions.

Enter required features.

Enter feature group tags.

Consider which of the following options fits your use case:

Create an online store, an offline store, or both. For more information about the differences between online and offline stores, see Feature Store concepts.

Use a default AWS Key Management Service key or your own KMS key. The default key is AWS KMS key (SSE-KMS). You can reduce AWS KMS request costs by configuring use of Amazon S3 Bucket Keys on the offline store Amazon S3 bucket. The Amazon S3 Bucket Key must be enabled before using the bucket for your feature groups. For more information about reducing the cost by using Amazon S3 Bucket Keys, see Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys.

You can use the same key for both online and offline stores, or have a unique key for each. For more information about AWS KMS, see AWS Key Management Service.

If you create an offline store:

Decide if you want to create an Amazon S3 bucket or use an existing one. When usin

*[Content truncated]*

---

## Using Amazon SageMaker Feature Store in the console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-use-with-studio.html

**Contents:**
- Using Amazon SageMaker Feature Store in the console
        - Important
        - Topics
- Create a feature group from the console
- View feature group details from the console
- Update a feature group from the console
- View pipeline executions from the console
- View lineage from the console

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

You can use Amazon SageMaker Feature Store on the console to create, view, update, and monitor your feature groups. Monitoring in this guide includes viewing pipeline executions and lineage of your feature groups. This guide provides instructions on how to achieve these tasks from the console.

For Feature Store examples and resources using the Amazon SageMaker APIs and AWS SDK for Python (Boto3), see Amazon SageMaker Feature Store resources.

Create a feature group from the console

View feature group details from the console

Update a feature group from the console

View pipeline executions from the console

View lineage from the console

The create feature group process has four steps:

Enter feature group information.

Enter feature definitions.

Enter required features.

Enter feature group tags.

Consider which of the following options fits your use case:

Create an online store, an offline store, or both. For more information about the differences between online and offline stores, see Feature Store concepts.

Use a default AWS Key Management Service key or your own KMS key. The default key is AWS KMS key (SSE-KMS). You can reduce AWS KMS request costs by configuring use of Amazon S3 Bucket Keys on the offline store Amazon S3 bucket. The Amazon S3 Bucket Key must be enabled before using the bucket for your feature groups. For more information about reducing the cost by using Amazon S3 Bucket Keys, see Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys.

You can use the same key for both online and offline stores, or have a unique key for each. For more information about AWS KMS, see AWS Key Management Service.

If you create an offline store:

Decide if you want to create an Amazon S3 bucket or use an existing one. When usin

*[Content truncated]*

---

## Adapting your own training container

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/adapt-training-container.html#byoc-training-step2

**Contents:**
- Adapting your own training container
- Step 1: Create a SageMaker notebook instance
- Step 2: Create and upload the Dockerfile and Python training scripts
- Step 3: Build the container
        - Note
- Step 4: Test the container
- Step 5: Push the container to Amazon Elastic Container Registry (Amazon ECR)
        - Note
        - Tip
- Step 6: Clean up resources

To run your own training model, build a Docker container using the Amazon SageMaker Training Toolkit through an Amazon SageMaker notebook instance.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

In the left navigation pane, choose Notebook, choose Notebook instances, and then choose Create notebook instance.

On the Create notebook instance page, provide the following information:

For Notebook instance name, enter RunScriptNotebookInstance.

For Notebook Instance type, choose ml.t2.medium.

In the Permissions and encryption section, do the following:

For IAM role, choose Create a new role. This opens a new window.

On the Create an IAM role page, choose Specific S3 buckets, specify an Amazon S3 bucket named sagemaker-run-script, and then choose Create role.

SageMaker AI creates an IAM role named AmazonSageMaker-ExecutionRole-YYYYMMDDTHHmmSS. For example, AmazonSageMaker-ExecutionRole-20190429T110788. Note that the execution role naming convention uses the date and time at which the role was created, separated by a T.

For Root Access, choose Enable.

Choose Create notebook instance.

On the Notebook instances page, the Status is Pending. It can take a few minutes for Amazon SageMaker AI to launch a machine learning compute instance—in this case, it launches a notebook instance—and attach an ML storage volume to it. The notebook instance has a preconfigured Jupyter notebook server and a set of Anaconda libraries. For more information, see CreateNotebookInstance.

Click on the Name of the notebook you just created. This opens a new page.

In the Permissions and encryption section, copy the IAM role ARN number, and paste it into a notepad file to save it temporarily. You use this IAM role ARN number later to configure a local training estimator in the notebook instance. The IAM role ARN number looks like the following: 'arn:aws:iam::111122223333:role/service-role/AmazonSageMaker-ExecutionRole-20190429T110788'

After the status of the notebook instance changes to InService, choose Open JupyterLab.

After JupyterLab opens, create a new folder in the home directory of your JupyterLab. In the upper-left corner, choose the New Folder icon, and then enter the folder name docker_test_folder.

Create a Dockerfile text file in the docker_test_folder directory.

Choose the New Launcher icon (+) in the upper-left corner.

In the right pane under the Other section, choose Text File.

Paste the following Dockerfile sample code into

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
RunScriptNotebookInstance
```

Example 2 (unknown):
```unknown
ml.t2.medium
```

Example 3 (unknown):
```unknown
sagemaker-run-script
```

Example 4 (unknown):
```unknown
AmazonSageMaker-ExecutionRole-YYYYMMDDTHHmmSS
```

---

## NVMe stores with Amazon SageMaker Studio

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-nvme.html

**Contents:**
- NVMe stores with Amazon SageMaker Studio
- Considerations
- Access NVMe instance stores

Amazon SageMaker Studio applications and their associated notebooks run on Amazon Elastic Compute Cloud (Amazon EC2) instances. Some of the Amazon EC2 instance types, such as the ml.m5d instance family, offer non-volatile memory express (NVMe) solid state drives (SSD) instance stores. NVMe instance stores are local ephemeral disk stores that are physically connected to an instance for fast temporary storage. Studio applications support NVMe instance stores for supported instance types. For more information about instance types and their associated NVMe store volumes, see the Amazon Elastic Compute Cloud Instance Type Details. This topic provides information about accessing and using NVMe instance stores, as well as considerations when using NVMe instance stores with Studio.

The following considerations apply when using NVMe instance stores with Studio.

An NVMe instance store is temporary storage. The data stored on the NVMe store is deleted when the instance is terminated, stopped, or hibernated. When using NVMe stores with Studio applications, the data on the NVMe instance store is lost whenever the application is deleted, restarted, or patched. We recommend that you back up valuable data to persistent storage solutions, such as Amazon Elastic Block Store, Amazon Elastic File System, or Amazon Simple Storage Service.

Studio patches instances periodically to install new security updates. When an instance is patched, the instance is restarted. This restart results in the deletion of data stored in the NVMe instance store. We recommend that you frequently back up necessary data from the NVMe instance store to persistent storage solutions, such as Amazon Elastic Block Store, Amazon Elastic File System, or Amazon Simple Storage Service.

The following Studio applications support using NVMe storage:

Code Editor, based on Code-OSS, Visual Studio Code - Open Source

When you select an instance type with attached NVMe instance stores to host a Studio application, the NVMe instance store directory is mounted to the application container at the following location:

If an instance has more than 1 NVMe instance store attached to it, Studio creates a striped logical volume that spans all of the local disks attached. Studio then mounts this striped logical volume to the /mnt/sagemaker-nvme directory. As a result, the directory storage size is the sum of all NVMe instance store volume sizes attached to the instance.

If the /mnt/sagemaker-nvme directory does not exis

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
/mnt/sagemaker-nvme
```

Example 2 (unknown):
```unknown
/mnt/sagemaker-nvme
```

Example 3 (unknown):
```unknown
/mnt/sagemaker-nvme
```

---

## SageMaker Notebook Jobs

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-auto-run.html

**Contents:**
- SageMaker Notebook Jobs
        - Prerequisites

You can use Amazon SageMaker AI to interactively build, train, and deploy machine learning models from your Jupyter notebook in any JupyterLab environment. However, there are various scenarios in which you might want to run your notebook as a noninteractive, scheduled job. For example, you might want to create regular audit reports that analyze all training jobs run over a certain time frame and analyze the business value of deploying those models into production. Or you might want to scale up a feature engineering job after testing the data transformation logic on a small subset of data. Other common use cases include:

Scheduling jobs for model drift monitoring

Exploring the parameter space for better models

In these scenarios, you can use SageMaker Notebook Jobs to create a noninteractive job (which SageMaker AI runs as an underlying training job) to either run on demand or on a schedule. SageMaker Notebook Jobs provides an intuitive user interface so you can schedule your jobs right from JupyterLab by choosing the Notebook Jobs widget ( ) in your notebook. You can also schedule your jobs using the SageMaker AI Python SDK, which offers the flexibility of scheduling multiple notebook jobs in a pipeline workflow. You can run multiple notebooks in parallel, and parameterize cells in your notebooks to customize the input parameters.

This feature leverages the Amazon EventBridge, SageMaker Training and Pipelines services and is available for use in your Jupyter notebook in any of the following environments:

Studio, Studio Lab, Studio Classic, or Notebook Instances

Local setup, such as your local machine, where you run JupyterLab

To schedule a notebook job, make sure you meet the following criteria:

Ensure your Jupyter notebook and any initialization or startup scripts are self-contained with respect to code and software packages. Otherwise, your noninteractive job may incur errors.

Review Constraints and considerations to make sure you properly configured your Jupyter notebook, network settings, and container settings.

Ensure your notebook can access needed external resources, such as Amazon EMR clusters.

If you are setting up Notebook Jobs in a local Jupyter notebook, complete the installation. For instructions, see Installation guide.

If you connect to an Amazon EMR cluster in your notebook and want to parameterize your Amazon EMR connection command, you must apply a workaround using environment variables to pass parameters. For details, see Con

*[Content truncated]*

---

## Troubleshooting

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-troubleshooting.html

**Contents:**
- Troubleshooting
        - Important
        - Important
- Recovery mode
        - Note
- Cannot delete the Code Editor or JupyterLab application
- EC2InsufficientCapacityError
        - Note
- Insufficient limit (quota increase required)
- Failure to load custom image

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

This section shows how to troubleshoot common problems in Amazon SageMaker Studio.

Recovery mode allows you to access your Studio application when a configuration issue prevents your normal start up. It provides a simplified environment with essential functionality to help you diagnose and fix the issue.

When an application fails to launch, you may see an error message about accessing recovery mode to address one of the following configuration issues.

Corrupted .condarc file.

For information on troubleshooting your .condarc file, see the troubleshooting page in the Conda user guide.

Insufficient storage volume available.

You can increase the Amazon EBS space storage available for the application or enter recovery mode to remove unnecessary data.

For information on increasing the Amazon EBS volume size, see request a quota size in the Service Quotas Developer Guide.

Your home directory will differ from your normal start up. This directory is temporary and ensures that any corrupted configurations in your standard home directory does not impact your recovery mode operations. You can navigate to your standard home directory by using the command cd /home/sagemaker-user.

Standard mode: /home/sagemaker-user

Recovery mode: /tmp/sagemaker-recovery-mode-home

The conda environment uses a minimal base conda environment with essential packages only. The simplified conda setup helps isolate environment-related issues and provides basic functionality for

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
cd
                        /home/sagemaker-user
```

Example 2 (unknown):
```unknown
/home/sagemaker-user
```

Example 3 (unknown):
```unknown
/tmp/sagemaker-recovery-mode-home
```

Example 4 (unknown):
```unknown
application
```

---

## SageMaker JumpStart pretrained models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html#jumpstart-solutions

**Contents:**
- SageMaker JumpStart pretrained models
- Open and use JumpStart in Studio
        - Important
  - Open JumpStart in Studio
        - Important
  - Use JumpStart in Studio
  - Manage JumpStart in Studio
- Open and use JumpStart in Studio Classic
        - Important
  - Open JumpStart in Studio Classic

Amazon SageMaker JumpStart provides pretrained, open-source models for a wide range of problem types to help you get started with machine learning. You can incrementally train and tune these models before deployment. JumpStart also provides solution templates that set up infrastructure for common use cases, and executable example notebooks for machine learning with SageMaker AI.

You can deploy, fine-tune, and evaluate pretrained models from popular models hubs through the JumpStart landing page in the updated Studio experience.

You can also access pretrained models, solution templates, and examples through the JumpStart landing page in Amazon SageMaker Studio Classic.

The following steps show how to access JumpStart models using Amazon SageMaker Studio and Amazon SageMaker Studio Classic.

You can also access JumpStart models using the SageMaker Python SDK. For information about how to use JumpStart models programmatically, see Use SageMaker JumpStart Algorithms with Pretrained Models.

The following sections give information on how to open, use, and manage JumpStart from the Studio UI.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the updated Studio experience. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

In Amazon SageMaker Studio, open the JumpStart landing page either through the Home page or the Home menu on the left-side panel. This opens the SageMaker JumpStart landing page where you can explore model hubs and search for models.

From the Home page, choose JumpStart in the Prebuilt and automated solutions pane.

From the Home menu in the left panel, navigate to the SageMaker JumpStart node.

For more information on getting started with Amazon SageMaker Studio, see Amazon SageMaker Studio.

Before downloading or using third-party content: You are responsible for reviewing and complying with any applicable license terms and making sure that they are acceptable for your use case.

From the SageMaker JumpStart landing page in Studio, you can explore model hubs from providers of both proprietary and publicly available models.

You can find specific hubs or models using the search bar. Within each model hub, you can search directly for models, sort by provided attributes, or filter based on a list of provided model tasks.

Choose a model to see its model detail card. In the upper right

*[Content truncated]*

---

## Launch Amazon SageMaker Studio Classic

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launch.html#studio-launch-console

**Contents:**
- Launch Amazon SageMaker Studio Classic
        - Important
        - Important
        - Topics
- Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console
        - Topics
  - Prerequisite
    - Launch Studio Classic from the domain details page
    - Launch Studio Classic from the Studio Classic landing page
- Launch Amazon SageMaker Studio Classic Using the AWS CLI

Custom IAM policies that allow Amazon SageMaker Studio or Amazon SageMaker Studio Classic to create Amazon SageMaker resources must also grant permissions to add tags to those resources. The permission to add tags to resources is required because Studio and Studio Classic automatically tag any resources they create. If an IAM policy allows Studio and Studio Classic to create resources but does not allow tagging, "AccessDenied" errors can occur when trying to create resources. For more information, see Provide permissions for tagging SageMaker AI resources.

AWS managed policies for Amazon SageMaker AI that give permissions to create SageMaker resources already include permissions to add tags while creating those resources.

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

After you have onboarded to an Amazon SageMaker AI domain, you can launch an Amazon SageMaker Studio Classic application from either the SageMaker AI console or the AWS CLI. For more information about onboarding to a domain, see Amazon SageMaker AI domain overview.

Launch Amazon SageMaker Studio Classic Using the Amazon SageMaker AI Console

Launch Amazon SageMaker Studio Classic Using the AWS CLI

The process to navigate to Studio Classic from the Amazon SageMaker AI Console differs depending on if Studio Classic or Amazon SageMaker Studio are set as the default experience for your domain. For more information about setting the default experience for your domain, see Migration from Amazon SageMaker Studio Classic.

To complete this procedure, you must onboard to a domain by following the steps in Onboard to Amazon SageMaker AI domain.

Navigate to Studio following the steps in Launch Amazon SageMaker Studio.

From the Studio UI, find the applications pane on the left side.

From the applications pane, select Studio Classic.

From the Studio Classic landing page, select the Studio Classic instance to open.

When Studio Classic is your default experience, you can launch a Amazon SageMaker Studio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
aws configure
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-domain-url \
--region region \
--domain-id domain-id \
--space-name space-name \
--user-profile-name user-profile-name \
--session-expiration-duration-in-seconds 43200
```

Example 3 (unknown):
```unknown
user-profile-name
```

---
