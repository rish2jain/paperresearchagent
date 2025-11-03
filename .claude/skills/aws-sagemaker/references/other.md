# Aws-Sagemaker - Other

**Pages:** 131

---

## Adding policies to your IAM role

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-adding-policies.html

**Contents:**
- Adding policies to your IAM role

To get started with Amazon SageMaker Feature Store you must have a role and add the required policy to your role, AmazonSageMakerFeatureStoreAccess. The following is a walkthrough on how to view the policies attached to a role and how to add a policy to your role. For information on how to create a role, see How to use SageMaker AI execution roles. For information on how to get your execution role, see Get your execution role.

Open the IAM console at https://console.aws.amazon.com/iam/.

In the navigation pane on the left of the IAM console, choose Roles.

In the search bar enter the role you are using for Amazon SageMaker Feature Store.

For examples on how to find your execution role ARN for a notebook within SageMaker AI, see Get your execution role. The role is at the end of the execution role ARN.

After you enter the role in the search bar, choose the role.

Under Permissions policies you can view the policies attached to the role.

After you choose the role, choose Add permissions, then choose Attach policies.

In the search bar under Other permissions policies enter AmazonSageMakerFeatureStoreAccess and press enter. If the policy does not show, you may already have the policy attached, listed under your Current permissions policies.

After you press enter, select the check box next to the policy and then choose Add permissions.

After you have attached the policy to your role, the policy will appear under Permissions policies for your IAM role.

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerFeatureStoreAccess
```

Example 2 (unknown):
```unknown
AmazonSageMakerFeatureStoreAccess
```

---

## K-Means Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/k-means.html

**Contents:**
- K-Means Algorithm
        - Topics
- Input/Output Interface for the K-Means Algorithm
- EC2 Instance Recommendation for the K-Means Algorithm
- K-Means Sample Notebooks

K-means is an unsupervised learning algorithm. It attempts to find discrete groupings within data, where members of a group are as similar as possible to one another and as different as possible from members of other groups. You define the attributes that you want the algorithm to use to determine similarity.

Amazon SageMaker AI uses a modified version of the web-scale k-means clustering algorithm. Compared with the original version of the algorithm, the version used by Amazon SageMaker AI is more accurate. Like the original algorithm, it scales to massive datasets and delivers improvements in training time. To do this, the version used by Amazon SageMaker AI streams mini-batches (small, random subsets) of the training data. For more information about mini-batch k-means, see Web-scale k-means Clustering.

The k-means algorithm expects tabular data, where rows represent the observations that you want to cluster, and the columns represent attributes of the observations. The n attributes in each row represent a point in n-dimensional space. The Euclidean distance between these points represents the similarity of the corresponding observations. The algorithm groups observations with similar attribute values (the points corresponding to these observations are closer together). For more information about how k-means works in Amazon SageMaker AI, see How K-Means Clustering Works.

Input/Output Interface for the K-Means Algorithm

EC2 Instance Recommendation for the K-Means Algorithm

K-Means Sample Notebooks

How K-Means Clustering Works

K-Means Hyperparameters

K-Means Response Formats

For training, the k-means algorithm expects data to be provided in the train channel (recommended S3DataDistributionType=ShardedByS3Key), with an optional test channel (recommended S3DataDistributionType=FullyReplicated) to score the data on. Both recordIO-wrapped-protobuf and CSV formats are supported for training. You can use either File mode or Pipe mode to train models on data that is formatted as recordIO-wrapped-protobuf or as CSV.

For inference, text/csv, application/json, and application/x-recordio-protobuf are supported. k-means returns a closest_cluster label and the distance_to_cluster for each observation.

For more information on input and output file formats, see K-Means Response Formats for inference and the K-Means Sample Notebooks. The k-means algorithm does not support multiple instance learning, in which the training set consists of labeled “bags”, each of w

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
S3DataDistributionType=ShardedByS3Key
```

Example 2 (unknown):
```unknown
S3DataDistributionType=FullyReplicated
```

Example 3 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 4 (unknown):
```unknown
recordIO-wrapped-protobuf
```

---

## Model Monitor FAQs

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-faqs.html

**Contents:**
- Model Monitor FAQs
        - Note
        - Note

Refer to the following FAQs for more information about Amazon SageMaker Model Monitor.

Q: How do Model Monitor and SageMaker Clarify help customers monitor model behavior?

Customers can monitor model behavior along four dimensions - Data quality, Model quality, Bias drift, and Feature Attribution drift through Amazon SageMaker Model Monitor and SageMaker Clarify. Model Monitor continuously monitors the quality of Amazon SageMaker AI machine learning models in production. This includes monitoring drift in data quality and model quality metrics such as accuracy and RMSE. SageMaker Clarify bias monitoring helps data scientists and ML engineers monitor bias in model’s prediction and feature attribution drift.

Q: What happens in the background when Sagemaker Model monitor is enabled?

Amazon SageMaker Model Monitor automates model monitoring alleviating the need to monitor the models manually or building any additional tooling. In order to automate the process, Model Monitor provides you with the ability to create a set of baseline statistics and constraints using the data with which your model was trained, then set up a schedule to monitor the predictions made on your endpoint. Model Monitor uses rules to detect drift in your models and alerts you when it happens. The following steps describe what happens when you enable model monitoring:

Enable model monitoring: For a real-time endpoint, you have to enable the endpoint to capture data from incoming requests to a deployed ML model and the resulting model predictions. For a batch transform job, enable data capture of the batch transform inputs and outputs.

Baseline processing job: You then create a baseline from the dataset that was used to train the model. The baseline computes metrics and suggests constraints for the metrics. For example, the recall score for the model shouldn't regress and drop below 0.571, or the precision score shouldn't fall below 1.0. Real-time or batch predictions from your model are compared to the constraints and are reported as violations if they are outside the constrained values.

Monitoring job: Then, you create a monitoring schedule specifying what data to collect, how often to collect it, how to analyze it, and which reports to produce.

Merge job: This is only applicable if you are leveraging Amazon SageMaker Ground Truth. Model Monitor compares the predictions your model makes with Ground Truth labels to measure the quality of the model. For this to work, you periodically

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
DataCaptureConfig
```

Example 2 (unknown):
```unknown
s3:///{endpoint-name}/{variant-name}/yyyy/mm/dd/hh/filename.jsonl
```

Example 3 (python):
```python
import random

def ground_truth_with_id(inference_id):
    random.seed(inference_id)  # to get consistent results
    rand = random.random()
    # format required by the merge container
    return {
        "groundTruthData": {
            "data": "1" if rand < 0.7 else "0",  # randomly generate positive labels 70% of the time
            "encoding": "CSV",
        },
        "eventMetadata": {
            "eventId": str(inference_id),
        },
        "eventVersion": "0",
    }


def upload_ground_truth(upload_time):
    records = [ground_truth_with_id(i) for i in range(test_dataset_size)]

...
```

Example 4 (unknown):
```unknown
inferenceId
```

---

## View Project Resources

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-resources.html

**Contents:**
- View Project Resources

After you create a project, view the resources associated with the project in Amazon SageMaker Studio Classic.

Open the SageMaker Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, choose Deployments, and then choose Projects.

Select the name of the project for which you want to view details. A page with the project details appears.

On the project details page, you can view the following entities can open any of the following tabs corresponding to the entity associated with the project.

Repositories: Code repositories (repos) associated with this project. If you use a SageMaker AI-provided template when you create your project, it creates a AWS CodeCommit repo or a third-party Git repo. For more information about CodeCommit, see What is AWS CodeCommit.

Pipelines: SageMaker AI ML pipelines that define steps to prepare data, train, and deploy models. For information about SageMaker AI ML pipelines, see Pipelines actions.

Experiments: One or more Amazon SageMaker Autopilot experiments associated with the project. For information about Autopilot, see SageMaker Autopilot.

Model groups: Groups of model versions that were created by pipeline executions in the project. For information about model groups, see Create a Model Group.

Endpoints: SageMaker AI endpoints that host deployed models for real-time inference. When a model version is approved, it is deployed to an endpoint.

Tags: All the tags associated with the project. For more information about tags, see Tagging AWS resources in the AWS General Reference.

Metadata: Metadata associated with the project. This includes the template and version used, and the template launch path.

Sign in to Studio Classic. For more information, see Amazon SageMaker AI domain overview.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Deployments from the menu, and then select Projects.

Select the name of the project for which you want to view details.

A tab with the project details appears.

On the project details tab, you can view the following entities associated with the project.

Repositories: Code repositories (repos) associated with this project. If you use a SageMaker AI-provided template when you create your project, it creates a AWS CodeCommit repo or a third-party Git repo. For more information about CodeCommit, see What is AWS CodeCommit.

Pipelines: SageMaker AI ML pipelines that define steps to prepare data, train, and deploy mod

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
SourceModelPackageGroupName
```

---

## AWS Managed Policies for SageMaker AI Model Governance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-governance.html

**Contents:**
- AWS Managed Policies for SageMaker AI Model Governance
        - Topics
- AWS managed policy: AmazonSageMakerModelGovernanceUseAccess
- Amazon SageMaker AI updates to SageMaker AI Model Governance managed policies

This AWS managed policy adds permissions required to use SageMaker AI Model Governance. The policy is available in your AWS account and is used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerModelGovernanceUseAccess

Amazon SageMaker AI updates to SageMaker AI Model Governance managed policies

This AWS managed policy grants permissions needed to use all Amazon SageMaker AI Governance features. The policy is available in your AWS account.

This policy includes the following permissions.

s3 – Retrieve objects from Amazon S3 buckets. Retrievable objects are limited to those whose case-insensitive name contains the string "sagemaker".

kms – List the AWS KMS keys to use for content encryption.

View details about updates to AWS managed policies for SageMaker AI Model Governance since this service began tracking these changes. For automatic alerts about changes to this page, subscribe to the RSS feed on the SageMaker AI Document history page.

AmazonSageMakerModelGovernanceUseAccess - Update to an existing policy

Add statement IDs (Sid).

AmazonSageMakerModelGovernanceUseAccess - Update to an existing policy

Add sagemaker:DescribeModelPackage and DescribeModelPackageGroup permissions.

AmazonSageMakerModelGovernanceUseAccess - New policy

**Examples:**

Example 1 (unknown):
```unknown
"sagemaker"
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSMMonitoringModelCards",
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListMonitoringAlerts",
                "sagemaker:ListMonitoringExecutions",
                "sagemaker:UpdateMonitoringAlert",
                "sagemaker:StartMonitoringSchedule",
                "sagemaker:StopMonitoringSchedule",
                "sagemaker:ListMonitoringAlertHistory",
                "sagemaker:DescribeModelPackage",
                "sagemaker:DescribeModelPackageGroup",
               
...
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSMMonitoringModelCards",
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListMonitoringAlerts",
                "sagemaker:ListMonitoringExecutions",
                "sagemaker:UpdateMonitoringAlert",
                "sagemaker:StartMonitoringSchedule",
                "sagemaker:StopMonitoringSchedule",
                "sagemaker:ListMonitoringAlertHistory",
                "sagemaker:DescribeModelPackage",
                "sagemaker:DescribeModelPackageGroup",
               
...
```

Example 4 (unknown):
```unknown
sagemaker:DescribeModelPackage
```

---

## Troubleshoot

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-troubleshoot.html

**Contents:**
- Troubleshoot
        - Topics
- Dashboard tab
- Tasks tab
- Policies
- Deleting clusters

The following page contains known solutions for troubleshooting your HyperPod EKS clusters.

The EKS add-on fails to install

For the EKS add-on installation to succeed, you will need to have a Kubernetes version >= 1.30. To update, see Update Kubernetes version.

For the EKS add-on installation to succeed, all of the nodes need to be in Ready status and all of the pods need to be in Running status.

To check the status of your nodes, use the list-cluster-nodes AWS CLI command or navigate to your EKS cluster in the EKS console and view the status of your nodes. Resolve the issue for each node or reach out to your administrator. If the node status is Unknown, delete the node. Once all node statuses are Ready, retry installing the EKS add-on in HyperPod from the Amazon SageMaker AI console.

To check the status of your pods, use the Kubernetes CLI command `kubectl get pods -n cloudwatch-agent` or navigate to your EKS cluster in the EKS console and view the status of your pods with the namespace cloudwatch-agent. Resolve the issue for the pods or reach out to your administrator to resolve the issues. Once all pod statuses are Running, retry installing the EKS add-on in HyperPod from the Amazon SageMaker AI console.

For more troubleshooting, see Troubleshooting the Amazon CloudWatch Observability EKS add-on.

If you see the error message about how the Custom Resource Definition (CRD) is not configured on the cluster, grant EKSAdminViewPolicy and ClusterAccessRole policies to your domain execution role.

For information on how to get your execution role, see Get your execution role.

To learn how to attach policies to an IAM user or group, see Adding and removing IAM identity permissions.

The following lists solutions to errors relating to policies using the HyperPod APIs or console.

If the policy is in CreateFailed or CreateRollbackFailed status, you need to delete the failed policy and create a new one.

If the policy is in UpdateFailed status, retry the update with the same policy ARN.

If the policy is in UpdateRollbackFailed status, you need to delete the failed policy and then create a new one.

If the policy is in DeleteFailed or DeleteRollbackFailed status, retry the delete with the same policy ARN.

If you ran into an error while trying to delete the Compute prioritization, or cluster policy, using the HyperPod console, try to delete the cluster-scheduler-config using the API. To check the status of the resource, go to the details page of a compute al

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
list-cluster-nodes
```

Example 2 (unknown):
```unknown
kubectl get pods -n cloudwatch-agent
```

Example 3 (unknown):
```unknown
cloudwatch-agent
```

Example 4 (unknown):
```unknown
EKSAdminViewPolicy
```

---

## Dashboard setup

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-metrics.html

**Contents:**
- Dashboard setup
        - Topics
- HyperPod Amazon CloudWatch Observability EKS add-on prerequisites
- HyperPod Amazon CloudWatch Observability EKS add-on setup

Use the following information to get set up with Amazon SageMaker HyperPod Amazon CloudWatch Observability EKS add-on. This sets you up with a detailed visual dashboard that provides a view into metrics for your EKS cluster hardware, team allocation, and tasks.

If you are having issues setting up, please see Troubleshoot for known troubleshooting solutions.

HyperPod Amazon CloudWatch Observability EKS add-on prerequisites

HyperPod Amazon CloudWatch Observability EKS add-on setup

The following section includes the prerequisites needed before installing the Amazon EKS Observability add-on.

Ensure that you have the minimum permission policy for HyperPod cluster administrators, in IAM users for cluster admin.

Attach the CloudWatchAgentServerPolicy IAM policy to your worker nodes. To do so, enter the following command. Replace my-worker-node-role with the IAM role used by your Kubernetes worker nodes.

Use the following options to set up the Amazon SageMaker HyperPod Amazon CloudWatch Observability EKS add-on.

The following permissions are required for setup and visualizing the HyperPod task governance dashboard. This section expands upon the permissions listed in IAM users for cluster admin.

To manage task governance, use the sample policy:

To grant permissions to manage Amazon CloudWatch Observability Amazon EKS and view the HyperPod cluster dashboard through the SageMaker AI console, use the sample policy below:

Navigate to the Dashboard tab in the SageMaker HyperPod console to install the Amazon CloudWatch Observability EKS. To ensure task governance related metrics are included in the Dashboard, enable the Kueue metrics checkbox. Enabling the Kueue metrics enables CloudWatch Metrics costs, after free-tier limit is reached. For more information, see Metrics in Amazon CloudWatch Pricing.

Use the following EKS AWS CLI command to install the add-on:

Below is an example of the JSON of the configuration values:

Navigate to the EKS console.

Find the Amazon CloudWatch Observability add-on and install. Install version >= 2.4.0 for the add-on.

Include the following JSON, Configuration values:

Once the EKS Observability add-on has been successfully installed, you can view your EKS cluster metrics under the HyperPod console Dashboard tab.

**Examples:**

Example 1 (unknown):
```unknown
CloudWatchAgentServerPolicy
```

Example 2 (unknown):
```unknown
my-worker-node-role
```

Example 3 (unknown):
```unknown
my-worker-node-role
```

Example 4 (unknown):
```unknown
aws iam attach-role-policy \
--role-name my-worker-node-role \
--policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
```

---

## Run a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/run-pipeline.html

**Contents:**
- Run a pipeline
        - Note
        - Note
        - Topics
  - Prerequisites
  - Step 1: Start the Pipeline
        - To start the pipeline
  - Step 2: Examine a Pipeline Execution
        - To examine a pipeline execution
  - Step 3: Override Default Parameters for a Pipeline Execution

After defining the steps of your pipeline as a directed acyclic graph (DAG), you can run your pipeline, which executes the steps defined in your DAG. The following walkthroughs show you how to run an Amazon SageMaker AI pipeline using either the drag-and-drop visual editor in Amazon SageMaker Studio or the Amazon SageMaker Python SDK.

To start a new execution of your pipeline, do the following:

Open SageMaker Studio by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, choose Pipelines.

(Optional) To filter the list of pipelines by name, enter a full or partial pipeline name in the search field.

Choose a pipeline name to open the pipeline details view.

Choose Visual Editor on the top right.

To start an execution from the latest version, choose Executions.

To start an execution from a specific version, follow these steps:

Choose the version icon in the bottom toolbar to open the version panel.

Choose the pipeline version you want to execute.

Hover over the version item to reveal the three-dot menu, choose Execute.

(Optional) To view a previous version of the pipeline, choose Preview from the three-dot menu in the version panel. You can also edit the version by choosing Edit in the notification bar.

If your pipeline fails, the status banner will show a Failed status. After troubleshooting the failed step, choose Retry on the status banner to resume running the pipeline from that step.

Sign in to Amazon SageMaker Studio Classic. For more information, see Launch Amazon SageMaker Studio Classic.

In the Studio Classic sidebar, choose the Home icon ( ).

Select Pipelines from the menu.

To narrow the list of pipelines by name, enter a full or partial pipeline name in the search field.

Select a pipeline name.

From the Executions or Graph tab in the execution list, choose Create execution.

Enter or update the following required information:

Name – Must be unique to your account in the AWS Region.

ProcessingInstanceCount – The number of instances to use for processing.

ModelApprovalStatus – For your convenience.

InputDataUrl – The Amazon S3 URI of the input data.

Once your pipeline is running, you can view the details of the execution by choosing View details on the status banner.

To stop the run, choose Stop on the status banner. To resume the execution from where it was stopped, choose Resume on the status banner.

If your pipeline fails, the status banner will show a Failed status. After troubleshoot

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
import json

json.loads(pipeline.definition())
```

Example 2 (unknown):
```unknown
pipeline.upsert(role_arn=role)
```

Example 3 (unknown):
```unknown
execution = pipeline.start()
```

Example 4 (unknown):
```unknown
execution.describe()
```

---

## CreateUserProfile

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateUserProfile.html

**Contents:**
- CreateUserProfile
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

Creates a user profile. A user profile represents a single user within a domain, and is the main way to reference a "person" for the purposes of sharing, reporting, and other user-oriented features. This entity is created when a user onboards to a domain. If an administrator invites a person by email or imports them from IAM Identity Center, a user profile is automatically created. A user profile is the primary holder of settings for an individual user and has a reference to the user's private Amazon Elastic File System home directory.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

The ID of the associated Domain.

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: d-(-*[a-z0-9]){1,61}

A specifier for the type of value specified in SingleSignOnUserValue. Currently, the only supported value is "UserName". If the Domain's AuthMode is IAM Identity Center, this field is required. If the Domain's AuthMode is not IAM Identity Center, this field cannot be specified.

The username of the associated AWS Single Sign-On User for this UserProfile. If the Domain's AuthMode is IAM Identity Center, this field is required, and must match a valid username of a user in your directory. If the Domain's AuthMode is not IAM Identity Center, this field cannot be specified.

Length Constraints: Minimum length of 0. Maximum length of 256.

Each tag consists of a key and an optional value. Tag keys must be unique per resource.

Tags that you specify for the User Profile are also added to all Apps that the User Profile launches.

Type: Array of Tag objects

Array Members: Minimum number of 0 items. Maximum number of 50 items.

A name for the UserProfile. This value is not case sensitive.

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

A collection of settings.

Type: UserSettings object

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

The user profile Amazon Resource Name (ARN).

Length Constraints: Minimum length of 0. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:user-profile/.*

For information about the errors that are common to all actions, see Common Errors.

Resource being accessed is in use.

HTTP Status Code: 400

You have exceeded an SageMaker resource limit. For exam

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
   "DomainId": "string",
   "SingleSignOnUserIdentifier": "string",
   "SingleSignOnUserValue": "string",
   "Tags": [
      {
         "Key": "string",
         "Value": "string"
      }
   ],
   "UserProfileName": "string",
   "UserSettings": {
      "AutoMountHomeEFS": "string",
      "CanvasAppSettings": {
         "DirectDeploySettings": {
            "Status": "string"
         },
         "EmrServerlessSettings": {
            "ExecutionRoleArn": "string",
            "Status": "string"
         },
         "GenerativeAiSettings": {
            "AmazonBedrockRoleArn": "string"
       
...
```

Example 2 (unknown):
```unknown
d-(-*[a-z0-9]){1,61}
```

Example 3 (unknown):
```unknown
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

Example 4 (unknown):
```unknown
{
   "UserProfileArn": "string"
}
```

---

## Time to live (TTL) duration for records

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-time-to-live.html

**Contents:**
- Time to live (TTL) duration for records
        - Important

Amazon SageMaker Feature Store provides the option for records to be hard deleted from the online store after a time duration is reached, with time to live (TTL) duration (TtlDuration). The record will expire after the record’s EventTime plus the TtlDuration is reached, or ExpiresAt = EventTime + TtlDuration. The TtlDuration can be applied at a feature group level, where all records within the feature group will have the TtlDuration by default, or at an individual record level. If TtlDuration is unspecified, the default value is null and the record will remain in the online store until it is overwritten.

A record deleted using TtlDuration is hard deleted, or completely removed from the online store, and the deleted record is added to the offline store. For more information on hard delete and deletion modes, see DeleteRecord in the Amazon SageMaker API Reference guide. When a record is hard deleted it immediately becomes inaccessible using Feature Store APIs.

TTL typically deletes expired items within a few days. Depending on the size and activity level of a table, the actual delete operation of an expired item can vary. Because TTL is meant to be a background process, the nature of the capacity used to expire and delete items via TTL is variable (but free of charge). For more information on how items are deleted from a DynamoDB table, see How it works: DynamoDB Time to Live (TTL).

TtlDuration must be a dictionary containing a Unit and a Value, where the Unit must be a string with values "Seconds", "Minutes", "Hours", "Days", or "Weeks" and Value must be an integer greater than or equal to 1. TtlDuration can be applied while using the CreateFeatureGroup, UpdateFeatureGroup, and PutRecord APIs. See the request and response syntax in the SDK for Python (Boto3) documentation for CreateFeatureGroup, UpdateFeatureGroup, and PutRecord APIs.

When TtlDuration is applied at a feature group level (using the CreateFeatureGroup or UpdateFeatureGroup APIs), the applied TtlDuration becomes the default TtlDuration for all records that are added to the feature group from the point in time that the API is called. When applying TtlDuration with the UpdateFeatureGroup API, this will not become the default TtlDuration for records that were created before the API is called.

To remove the default TtlDuration from an existing feature group, use the UpdateFeatureGroup API and set the TtlDuration Unit and Value to null.

When TtlDuration is applied at a record level (for examp

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
TtlDuration
```

Example 2 (unknown):
```unknown
TtlDuration
```

Example 3 (unknown):
```unknown
TtlDuration
```

Example 4 (unknown):
```unknown
TtlDuration
```

---

## AWS managed policies for Amazon SageMaker geospatial

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-geospatial.html

**Contents:**
- AWS managed policies for Amazon SageMaker geospatial
        - Topics
- AWS managed policy: AmazonSageMakerGeospatialFullAccess
- AWS managed policy: AmazonSageMakerGeospatialExecutionRole
- Amazon SageMaker AI updates to Amazon SageMaker geospatial managed policies

These AWS managed policies add permissions required to use SageMaker geospatial. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerGeospatialFullAccess

AWS managed policy: AmazonSageMakerGeospatialExecutionRole

Amazon SageMaker AI updates to Amazon SageMaker geospatial managed policies

This policy grants permissions that allow full access to Amazon SageMaker geospatial through the AWS Management Console and SDK.

This AWS managed policy includes the following permissions.

sagemaker-geospatial – Allows principals full access to all SageMaker geospatial resources.

iam – Allows principals to pass an IAM role to SageMaker geospatial.

This policy grants permissions commonly needed to use SageMaker geospatial.

This AWS managed policy includes the following permissions.

s3 – Allows principals to add and retrieve objects from Amazon S3 buckets. These objects are limited to those whose name contains "SageMaker", "Sagemaker", or "sagemaker".

sagemaker-geospatial – Allows principals to access Earth observation jobs through the GetEarthObservationJob API.

View details about updates to AWS managed policies for SageMaker geospatial since this service began tracking these changes.

AmazonSageMakerGeospatialExecutionRole - Updated policy

Add sagemaker-geospatial:GetRasterDataCollection permission.

AmazonSageMakerGeospatialFullAccess - New policy

AmazonSageMakerGeospatialExecutionRole - New policy

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-geospatial
```

Example 2 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sagemaker-geospatial:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["iam:PassRole"],
      "Resource": "arn:aws:iam::*:role/*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": [
            "sagemaker-geospatial.amazonaws.com"
           ]
        }
      }
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
      "Action": "sagemaker-geospatial:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["iam:PassRole"],
      "Resource": "arn:aws:iam::*:role/*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": [
            "sagemaker-geospatial.amazonaws.com"
           ]
        }
      }
    }
  ]
}
```

Example 4 (unknown):
```unknown
sagemaker-geospatial
```

---

## Object Detection - MXNet

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/object-detection.html

**Contents:**
- Object Detection - MXNet
        - Topics
- Input/Output Interface for the Object Detection Algorithm
        - Note
  - Train with the RecordIO Format
  - Train with the Image Format
  - Train with Augmented Manifest Image Format
  - Incremental Training
- EC2 Instance Recommendation for the Object Detection Algorithm
- Object Detection Sample Notebooks

The Amazon SageMaker AI Object Detection - MXNet algorithm detects and classifies objects in images using a single deep neural network. It is a supervised learning algorithm that takes images as input and identifies all instances of objects within the image scene. The object is categorized into one of the classes in a specified collection with a confidence score that it belongs to the class. Its location and scale in the image are indicated by a rectangular bounding box. It uses the Single Shot multibox Detector (SSD) framework and supports two base networks: VGG and ResNet. The network can be trained from scratch, or trained with models that have been pre-trained on the ImageNet dataset.

Input/Output Interface for the Object Detection Algorithm

EC2 Instance Recommendation for the Object Detection Algorithm

Object Detection Sample Notebooks

How Object Detection Works

Object Detection Hyperparameters

Tune an Object Detection Model

Object Detection Request and Response Formats

The SageMaker AI Object Detection algorithm supports both RecordIO (application/x-recordio) and image (image/png, image/jpeg, and application/x-image) content types for training in file mode and supports RecordIO (application/x-recordio) for training in pipe mode. However you can also train in pipe mode using the image files (image/png, image/jpeg, and application/x-image), without creating RecordIO files, by using the augmented manifest format. The recommended input format for the Amazon SageMaker AI object detection algorithms is Apache MXNet RecordIO. However, you can also use raw images in .jpg or .png format. The algorithm supports only application/x-image for inference.

To maintain better interoperability with existing deep learning frameworks, this differs from the protobuf data formats commonly used by other Amazon SageMaker AI algorithms.

See the Object Detection Sample Notebooks for more details on data formats.

If you use the RecordIO format for training, specify both train and validation channels as values for the InputDataConfig parameter of the CreateTrainingJob request. Specify one RecordIO (.rec) file in the train channel and one RecordIO file in the validation channel. Set the content type for both channels to application/x-recordio. An example of how to generate RecordIO file can be found in the object detection sample notebook. You can also use tools from the MXNet's GluonCV to generate RecordIO files for popular datasets like the PASCAL Visual Object Clas

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application/x-recordio
```

Example 2 (unknown):
```unknown
application/x-image
```

Example 3 (unknown):
```unknown
application/x-recordio
```

Example 4 (unknown):
```unknown
application/x-image
```

---

## Welcome

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/Welcome.html

**Contents:**
- Welcome
- Amazon SageMaker Service
- Amazon SageMaker Runtime
- Amazon Sagemaker Edge Manager
- Amazon SageMaker Feature Store Runtime
- Amazon SageMaker geospatial capabilities
- Amazon SageMaker Metrics Service

Provides APIs for creating and managing SageMaker resources.

SageMaker Developer Guide

Amazon Augmented AI Runtime API Reference

The Amazon SageMaker AI runtime API.

SageMaker Edge Manager dataplane service for communicating with active agents.

Contains all data plane API operations and data types for the Amazon SageMaker Feature Store. Use this API to put, delete, and retrieve (get) features from a feature store.

Use the following operations to configure your OnlineStore and OfflineStore features, and to create and manage feature groups:

Provides APIs for creating and managing SageMaker geospatial resources.

Contains all data plane API operations and data types for Amazon SageMaker Metrics. Use these APIs to put and retrieve (get) features related to your training run.

**Examples:**

Example 1 (unknown):
```unknown
OnlineStore
```

Example 2 (unknown):
```unknown
OfflineStore
```

---

## Complete Amazon SageMaker AI prerequisites

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/gs-set-up.html

**Contents:**
- Complete Amazon SageMaker AI prerequisites
        - Topics
- Sign up for an AWS account
        - To sign up for an AWS account
- Create a user with administrative access
        - Secure your AWS account root user
        - Create a user with administrative access
        - Sign in as the user with administrative access
        - Assign access to additional users
- (Optional) Configure the AWS CLI

Before you can set up Amazon SageMaker AI, you must complete the following prerequisites.

Required: You will need to create an Amazon Web Services (AWS) account to get access to all of the AWS services and resources for the account.

Highly recommended: We highly recommend that you create an administrative user to manage AWS resources for the account, to adhere to the Security best practices in IAM. It is assumed that you have an administrative user for many of the administrative tasks throughout the SageMaker AI developer guide.

Optional: Configure the AWS Command Line Interface (AWS CLI) if you intend to manage your AWS services and resources for the account using the AWS CLI.

Sign up for an AWS account

Create a user with administrative access

(Optional) Configure the AWS CLI

If you do not have an AWS account, complete the following steps to create one.

Open https://portal.aws.amazon.com/billing/signup.

Follow the online instructions.

Part of the sign-up procedure involves receiving a phone call or text message and entering a verification code on the phone keypad.

When you sign up for an AWS account, an AWS account root user is created. The root user has access to all AWS services and resources in the account. As a security best practice, assign administrative access to a user, and use only the root user to perform tasks that require root user access.

AWS sends you a confirmation email after the sign-up process is complete. At any time, you can view your current account activity and manage your account by going to https://aws.amazon.com/ and choosing My Account.

After you sign up for an AWS account, secure your AWS account root user, enable AWS IAM Identity Center, and create an administrative user so that you don't use the root user for everyday tasks.

Sign in to the AWS Management Console as the account owner by choosing Root user and entering your AWS account email address. On the next page, enter your password.

For help signing in by using root user, see Signing in as the root user in the AWS Sign-In User Guide.

Turn on multi-factor authentication (MFA) for your root user.

For instructions, see Enable a virtual MFA device for your AWS account root user (console) in the IAM User Guide.

Enable IAM Identity Center.

For instructions, see Enabling AWS IAM Identity Center in the AWS IAM Identity Center User Guide.

In IAM Identity Center, grant administrative access to a user.

For a tutorial about using the IAM Identity Center directory 

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
                "sagemaker:*"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:domain/*",
                "arn:aws:sagemaker:*:*:user-profile/*",
                "arn:aws:sagemaker:*:*:app/*",
                "arn:aws:sagemaker:*:*:flow-definition/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "servicecatalog:*"
            ],
            "Resource": [
       
...
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sagemaker:*"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:domain/*",
                "arn:aws:sagemaker:*:*:user-profile/*",
                "arn:aws:sagemaker:*:*:app/*",
                "arn:aws:sagemaker:*:*:flow-definition/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "servicecatalog:*"
            ],
            "Resource": [
       
...
```

---

## Edit a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/edit-pipeline-before-execution.html

**Contents:**
- Edit a pipeline

To make changes to a pipeline before running it, do the following:

Open SageMaker Studio by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane of Studio, select Pipelines.

Select a pipeline name to view details about the pipeline.

Choose the Executions tab.

Select the name of a pipeline execution.

Choose Edit to open the Pipeline Designer.

Update the edges between steps or the step configuration as required and click Save.

Saving a pipeline after editing automatically generates a new version number.

---

## Neural Topic Model (NTM) Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/ntm.html

**Contents:**
- Neural Topic Model (NTM) Algorithm
        - Topics
- Input/Output Interface for the NTM Algorithm
- EC2 Instance Recommendation for the NTM Algorithm
- NTM Sample Notebooks

Amazon SageMaker AI NTM is an unsupervised learning algorithm that is used to organize a corpus of documents into topics that contain word groupings based on their statistical distribution. Documents that contain frequent occurrences of words such as "bike", "car", "train", "mileage", and "speed" are likely to share a topic on "transportation" for example. Topic modeling can be used to classify or summarize documents based on the topics detected or to retrieve information or recommend content based on topic similarities. The topics from documents that NTM learns are characterized as a latent representation because the topics are inferred from the observed word distributions in the corpus. The semantics of topics are usually inferred by examining the top ranking words they contain. Because the method is unsupervised, only the number of topics, not the topics themselves, are prespecified. In addition, the topics are not guaranteed to align with how a human might naturally categorize documents.

Topic modeling provides a way to visualize the contents of a large document corpus in terms of the learned topics. Documents relevant to each topic might be indexed or searched for based on their soft topic labels. The latent representations of documents might also be used to find similar documents in the topic space. You can also use the latent representations of documents that the topic model learns for input to another supervised algorithm such as a document classifier. Because the latent representations of documents are expected to capture the semantics of the underlying documents, algorithms based in part on these representations are expected to perform better than those based on lexical features alone.

Although you can use both the Amazon SageMaker AI NTM and LDA algorithms for topic modeling, they are distinct algorithms and can be expected to produce different results on the same input data.

For more information on the mathematics behind NTM, see Neural Variational Inference for Text Processing.

Input/Output Interface for the NTM Algorithm

EC2 Instance Recommendation for the NTM Algorithm

Amazon SageMaker AI Neural Topic Model supports four data channels: train, validation, test, and auxiliary. The validation, test, and auxiliary data channels are optional. If you specify any of these optional channels, set the value of the S3DataDistributionType parameter for them to FullyReplicated. If you provide validation data, the loss on this data is logged at ever

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
S3DataDistributionType
```

Example 2 (unknown):
```unknown
FullyReplicated
```

Example 3 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 4 (unknown):
```unknown
recordIO-wrapped-protobuf
```

---

## Data preparation

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-data-prep.html

**Contents:**
- Data preparation
        - Note

Previously, Amazon SageMaker Data Wrangler was part of the SageMaker Studio Classic experience. Now, if you update to using the new Studio experience, you must use SageMaker Canvas to access Data Wrangler and receive the latest feature updates. If you have been using Data Wrangler in Studio Classic until now and want to migrate to Data Wrangler in Canvas, you might have to grant additional permissions so that you can create and use a Canvas application. For more information, see (Optional) Migrate from Data Wrangler in Studio Classic to SageMaker Canvas.

To learn how to migrate your data flows from Data Wrangler in Studio Classic, see (Optional) Migrate data from Studio Classic to Studio.

Use Amazon SageMaker Data Wrangler in Amazon SageMaker Canvas to prepare, featurize and analyze your data. You can integrate a Data Wrangler data preparation flow into your machine learning (ML) workflows to simplify and streamline data pre-processing and feature engineering using little to no coding. You can also add your own Python scripts and transformations to customize workflows.

Data Flow – Create a data flow to define a series of ML data prep steps. You can use a flow to combine datasets from different data sources, identify the number and types of transformations you want to apply to datasets, and define a data prep workflow that can be integrated into an ML pipeline.

Transform – Clean and transform your dataset using standard transforms like string, vector, and numeric data formatting tools. Featurize your data using transforms like text and date/time embedding and categorical encoding.

Generate Data Insights – Automatically verify data quality and detect abnormalities in your data with Data Wrangler Data Quality and Insights Report.

Analyze – Analyze features in your dataset at any point in your flow. Data Wrangler includes built-in data visualization tools like scatter plots and histograms, as well as data analysis tools like target leakage analysis and quick modeling to understand feature correlation.

Export – Export your data preparation workflow to a different location. The following are example locations:

Amazon Simple Storage Service (Amazon S3) bucket

Amazon SageMaker Feature Store – Store the features and their data in a centralized store.

Automate data preparation – Create machine learning workflows from your data flow.

Amazon SageMaker Pipelines – Build workflows that manage your SageMaker AI data preparation, model training, and model deplo

*[Content truncated]*

---

## Online store

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-storage-configurations-online-store.html

**Contents:**
- Online store
- Standard tier storage type
- In-memory tier storage type

The online store is a low-latency, high-availability data store that provides real-time lookup of features. It is typically used for machine learning (ML) model serving. You can chose between the standard online store (Standard) or an in-memory tier online store (InMemory), at the point when you create a feature group. In this way, you can select the storage type that best matches the read and write patterns for a particular application, while considering performance and cost. For more details about pricing, see Amazon SageMaker Pricing.

The online store contains the following StorageType options. For more information about the online store contents, see OnlineStoreConfig.

The Standard tier is a managed low-latency data store for online store feature groups. It provides fast data retrieval for ML model service for your applications. Standard is the default storage type.

The InMemory tier is a managed data store for online store feature groups that supports very low-latency retrieval. It provides large-scale real-time data retrieval for ML model serving used for high throughput applications. The InMemory tier is powered by Amazon ElastiCache (Redis OSS). For more information, see What is Amazon ElastiCache (Redis OSS)?.

The online store InMemory tier supports collection types, namely list, set, and vector. For more information about the InMemory collection types, see Collection types.

Feature Store provides low latency read and writes to the online store. The application latency is primarily made up of two primary components: infrastructure or network latency and Feature Store API latency. Reduction of network latency helps with getting the lowest latency reads and writes to Feature Store. You can reduce the network latency to Feature Store by deploying AWS PrivateLink to Feature Store Runtime endpoint. With AWS PrivateLink, you can privately access all Feature Store Runtime API operations from your Amazon Virtual Private Cloud (VPC) in a scalable manner by using interface VPC endpoints. An AWS PrivateLink deployment with the privateDNSEnabled option set as true:

It keeps all Feature Store read/write traffic within your VPC.

It keeps traffic in the same AZ as the client that originated it when using Feature Store. This avoids the “hops” between AZs reducing the network latency.

Follow the steps in Access an AWS service using an interface VPC endpoint to setup AWS PrivateLink to Feature Store. The service name for Feature Store Runtime in AWS Private

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
StorageType
```

Example 2 (unknown):
```unknown
OnlineStoreConfig
```

Example 3 (unknown):
```unknown
privateDNSEnabled
```

Example 4 (unknown):
```unknown
com.amazonaws.region.sagemaker.featurestore-runtime
```

---

## Use the SageMaker AI DeepAR forecasting algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html

**Contents:**
- Use the SageMaker AI DeepAR forecasting algorithm
        - Topics
- Input/Output Interface for the DeepAR Algorithm
- Best Practices for Using the DeepAR Algorithm
- EC2 Instance Recommendations for the DeepAR Algorithm
- DeepAR Sample Notebooks

The Amazon SageMaker AI DeepAR forecasting algorithm is a supervised learning algorithm for forecasting scalar (one-dimensional) time series using recurrent neural networks (RNN). Classical forecasting methods, such as autoregressive integrated moving average (ARIMA) or exponential smoothing (ETS), fit a single model to each individual time series. They then use that model to extrapolate the time series into the future.

In many applications, however, you have many similar time series across a set of cross-sectional units. For example, you might have time series groupings for demand for different products, server loads, and requests for webpages. For this type of application, you can benefit from training a single model jointly over all of the time series. DeepAR takes this approach. When your dataset contains hundreds of related time series, DeepAR outperforms the standard ARIMA and ETS methods. You can also use the trained model to generate forecasts for new time series that are similar to the ones it has been trained on.

The training input for the DeepAR algorithm is one or, preferably, more target time series that have been generated by the same process or similar processes. Based on this input dataset, the algorithm trains a model that learns an approximation of this process/processes and uses it to predict how the target time series evolves. Each target time series can be optionally associated with a vector of static (time-independent) categorical features provided by the cat field and a vector of dynamic (time-dependent) time series provided by the dynamic_feat field. SageMaker AI trains the DeepAR model by randomly sampling training examples from each target time series in the training dataset. Each training example consists of a pair of adjacent context and prediction windows with fixed predefined lengths. To control how far in the past the network can see, use the context_length hyperparameter. To control how far in the future predictions can be made, use the prediction_length hyperparameter. For more information, see How the DeepAR Algorithm Works.

Input/Output Interface for the DeepAR Algorithm

Best Practices for Using the DeepAR Algorithm

EC2 Instance Recommendations for the DeepAR Algorithm

DeepAR Sample Notebooks

How the DeepAR Algorithm Works

DeepAR Hyperparameters

DeepAR Inference Formats

DeepAR supports two data channels. The required train channel describes the training dataset. The optional test channel describes a dataset that

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
dynamic_feat
```

Example 2 (unknown):
```unknown
context_length
```

Example 3 (unknown):
```unknown
prediction_length
```

Example 4 (unknown):
```unknown
content_type
```

---

## Create and Use a Data Wrangler Flow

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-data-flow.html

**Contents:**
- Create and Use a Data Wrangler Flow
- Instances
- The Data Flow UI
- Add a Step to Your Data Flow
- Delete a Step from Your Data Flow
- Edit a Step in Your Data Wrangler Flow
        - Note

Use an Amazon SageMaker Data Wrangler flow, or a data flow, to create and modify a data preparation pipeline. The data flow connects the datasets, transformations, and analyses, or steps, you create and can be used to define your pipeline.

When you create a Data Wrangler flow in Amazon SageMaker Studio Classic, Data Wrangler uses an Amazon EC2 instance to run the analyses and transformations in your flow. By default, Data Wrangler uses the m5.4xlarge instance. m5 instances are general purpose instances that provide a balance between compute and memory. You can use m5 instances for a variety of compute workloads.

Data Wrangler also gives you the option of using r5 instances. r5 instances are designed to deliver fast performance that processes large datasets in memory.

We recommend that you choose an instance that is best optimized around your workloads. For example, the r5.8xlarge might have a higher price than the m5.4xlarge, but the r5.8xlarge might be better optimized for your workloads. With better optimized instances, you can run your data flows in less time at lower cost.

The following table shows the instances that you can use to run your Data Wrangler flow.

For more information about r5 instances, see Amazon EC2 R5 Instances. For more information about m5 instances, see Amazon EC2 M5 Instances.

Each Data Wrangler flow has an Amazon EC2 instance associated with it. You might have multiple flows that are associated with a single instance.

For each flow file, you can seamlessly switch the instance type. If you switch the instance type, the instance that you used to run the flow continues to run.

To switch the instance type of your flow, do the following.

Choose the Running Terminals and Kernels icon ( ).

Navigate to the instance that you're using and choose it.

Choose the instance type that you want to use.

You are charged for all running instances. To avoid incurring additional charges, shut down the instances that you aren't using manually. To shut down an instance that is running, use the following procedure.

To shut down a running instance.

Choose the instance icon. The following image shows you where to select the RUNNING INSTANCES icon.

Choose Shut down next to the instance that you want to shut down.

If you shut down an instance used to run a flow, you temporarily can't access the flow. If you get an error while attempting to open the flow running an instance you previously shut down, wait for 5 minutes and try opening it again.


*[Content truncated]*

---

## CatBoost

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/catboost.html

**Contents:**
- CatBoost
- Amazon EC2 instance recommendation for the CatBoost algorithm
- CatBoost sample notebooks

CatBoost is a popular and high-performance open-source implementation of the Gradient Boosting Decision Tree (GBDT) algorithm. GBDT is a supervised learning algorithm that attempts to accurately predict a target variable by combining an ensemble of estimates from a set of simpler and weaker models.

CatBoost introduces two critical algorithmic advances to GBDT:

The implementation of ordered boosting, a permutation-driven alternative to the classic algorithm

An innovative algorithm for processing categorical features

Both techniques were created to fight a prediction shift caused by a special kind of target leakage present in all currently existing implementations of gradient boosting algorithms. This page includes information about Amazon EC2 instance recommendations and sample notebooks for CatBoost.

SageMaker AI CatBoost currently only trains using CPUs. CatBoost is a memory-bound (as opposed to compute-bound) algorithm. So, a general-purpose compute instance (for example, M5) is a better choice than a compute-optimized instance (for example, C5). Further, we recommend that you have enough total memory in selected instances to hold the training data.

The following table outlines a variety of sample notebooks that address different use cases of Amazon SageMaker AI CatBoost algorithm.

Tabular classification with Amazon SageMaker AI LightGBM and CatBoost algorithm

This notebook demonstrates the use of the Amazon SageMaker AI CatBoost algorithm to train and host a tabular classification model.

Tabular regression with Amazon SageMaker AI LightGBM and CatBoost algorithm

This notebook demonstrates the use of the Amazon SageMaker AI CatBoost algorithm to train and host a tabular regression model.

For instructions on how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, choose the SageMaker AI Examples tab to see a list of all of the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

---

## Amazon SageMaker Model Cards

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html

**Contents:**
- Amazon SageMaker Model Cards
        - Important
        - Topics
- Prerequisites
- Intended uses of a model
- Risk ratings
- Model card JSON schema

Amazon SageMaker Model Card is integrated with SageMaker Model Registry. If you're registering a model within Model Registry, you can use the integration to add auditing information. For more information, see Update the Details of a Model Version.

Use Amazon SageMaker Model Cards to document critical details about your machine learning (ML) models in a single place for streamlined governance and reporting. Model cards can help you to capture key information about your models throughout their lifecycle and implement responsible AI practices.

Catalog details such as the intended use and risk rating of a model, training details and metrics, evaluation results and observations, and additional call-outs such as considerations, recommendations, and custom information. By creating model cards, you can do the following:

Provide guidance on how a model should be used.

Support audit activities with detailed descriptions of model training and performance.

Communicate how a model is intended to support business goals.

Model cards provide prescriptive guidance on what information to document and include fields for custom information. After creating a model card, you can export it to a PDF or download it to share with relevant stakeholders. Any edits other than an approval status update made to a model card result in additional model card versions in order to have an immutable record of model changes.

Intended uses of a model

Model card JSON schema

Set up cross-account support for Amazon SageMaker Model Cards

Low-level SageMaker APIs for model cards

To get started with Amazon SageMaker Model Cards, you must have permission to create, edit, view, and export model cards.

Specifying the intended uses of a model helps ensure that model developers and users have the information they need to train or deploy the model responsibly. The intended uses of a model should describe the scenarios in which the model is appropriate to use as well as the scenarios in which the model is not recommended to use.

We recommend including:

The general purpose of the model

Use cases for which the model was intended

Use cases for which the model was not intended

Assumptions made when developing the model

The intended uses of a model go beyond technical details and describe how a model should be used in production, the scenarios in which is appropriate to use a model, and additional considerations such as the type of data to use with the model or any assumptions made during devel

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://json-schema.org/draft-07/schema#",
  "title": "SageMakerModelCardSchema",
  "description": "Internal model card schema for SageMakerRepositoryService without model_package_details",
  "version": "0.1.0",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "model_overview": {
      "description": "Overview about the model",
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "model_description": {
          "description": "description of model",
          "typ
...
```

---

## Use Reinforcement Learning with Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/reinforcement-learning.html

**Contents:**
- Use Reinforcement Learning with Amazon SageMaker AI
- What are the differences between reinforcement, supervised, and unsupervised learning paradigms?
        - Topics
- Why is Reinforcement Learning Important?
- Markov Decision Process (MDP)
- Key Features of Amazon SageMaker AI RL
- Reinforcement Learning Sample Notebooks

Reinforcement learning (RL) combines fields such as computer science, neuroscience, and psychology to determine how to map situations to actions to maximize a numerical reward signal. This notion of a reward signal in RL stems from neuroscience research into how the human brain makes decisions about which actions maximize reward and minimize punishment. In most situations, humans are not given explicit instructions on which actions to take, but instead must learn both which actions yield the most immediate rewards, and how those actions influence future situations and consequences.

The problem of RL is formalized using Markov decision processes (MDPs) that originate from dynamical systems theory. MDPs aim to capture high-level details of a real problem that a learning agent encounters over some period of time in attempting to achieve some ultimate goal. The learning agent should be able to determine the current state of its environment and identify possible actions that affect the learning agent’s current state. Furthermore, the learning agent’s goals should correlate strongly to the state of the environment. A solution to a problem formulated in this way is known as a reinforcement learning method.

Machine learning can be divided into three distinct learning paradigms: supervised, unsupervised, and reinforcement.

In supervised learning, an external supervisor provides a training set of labeled examples. Each example contains information about a situation, belongs to a category, and has a label identifying the category to which it belongs. The goal of supervised learning is to generalize in order to predict correctly in situations that are not present in the training data.

In contrast, RL deals with interactive problems, making it infeasible to gather all possible examples of situations with correct labels that an agent might encounter. This type of learning is most promising when an agent is able to accurately learn from its own experience and adjust accordingly.

In unsupervised learning, an agent learns by uncovering structure within unlabeled data. While a RL agent might benefit from uncovering structure based on its experiences, the sole purpose of RL is to maximize a reward signal.

Why is Reinforcement Learning Important?

Markov Decision Process (MDP)

Key Features of Amazon SageMaker AI RL

Reinforcement Learning Sample Notebooks

Sample RL Workflow Using Amazon SageMaker AI RL

RL Environments in Amazon SageMaker AI

Distributed Training with

*[Content truncated]*

---

## Add user profiles

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/domain-user-profile-add.html

**Contents:**
- Add user profiles
- Add user profiles from the console
- Create user profiles from the AWS CLI

The following section shows how to add user profiles to a domain using the SageMaker AI console or the AWS CLI.

After you add a user profile to the domain, users can login using a URL. If the domain uses AWS IAM Identity Center for authentication, users receive an email that contains the URL to sign in to the domain. If the domain uses AWS Identity and Access Management, you can create a URL for a user profile using CreatePresignedDomainUrl

You can add user profiles to a domain from the SageMaker AI console by following this procedure.

Open the Amazon SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

On the left navigation pane, choose Admin configurations.

Under Admin configurations, choose domains.

From the list of domains, select the domain that you want to add a user profile to.

On the domain details page, choose the User profiles tab.

Choose Add user. This opens a new page.

Use the default name for your user profile or add a custom name.

For Execution role, choose an option from the role selector. If you choose Enter a custom IAM role ARN, the role must have, at a minimum, an attached trust policy that grants SageMaker AI permission to assume the role. For more information, see SageMaker AI Roles.

If you choose Create a new role, the Create an IAM role dialog box opens:

For S3 buckets you specify, specify additional Amazon S3 buckets that users of your notebooks can access. If you don't want to add access to more buckets, choose None.

Choose Create role. SageMaker AI creates a new IAM role, AmazonSageMaker-ExecutionPolicy, with the AmazonSageMakerFullAccess policy attached.

(Optional) Add tags to the user profile. All resources that the user profile creates will have a domain ARN tag and a user profile ARN tag. The domain ARN tag is based on domain ID, while the user profile ARN tag is based on the user profile name.

In the SageMaker Studio section, you have the option to choose between the newer and classic version of Studio as your default experience.

If you choose SageMaker Studio (recommended) as your default experience, the Studio Classic IDE has default settings. For information on the default settings, see Default settings.

For information on Studio, see Amazon SageMaker Studio.

If you choose Studio Classic as your default experience, you can choose to enable or disable notebook resource sharing. Notebook resources include artifacts such as cell output and Git repositories. For more information on Notebook res

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker-ExecutionPolicy
```

Example 2 (unknown):
```unknown
aws --region region \
sagemaker create-user-profile \
--domain-id domain-id \
--user-profile-name user-name \
--user-settings '{
  "JupyterServerAppSettings": {
    "DefaultResourceSpec": {
      "SageMakerImageArn": "sagemaker-image-arn",
      "InstanceType": "system"
    }
  }
}'
```

Example 3 (unknown):
```unknown
sagemaker-image-arn
```

Example 4 (unknown):
```unknown
HiddenAppTypes
```

---

## AWS managed policies for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol.html

**Contents:**
- AWS managed policies for Amazon SageMaker AI
        - Important
        - Topics
- AWS managed policy: AmazonSageMakerFullAccess
- AWS managed policy: AmazonSageMakerReadOnly
- SageMaker AI Updates to AWS Managed Policies

To add permissions to users, groups, and roles, it is easier to use AWS managed policies than to write policies yourself. It takes time and expertise to create IAM customer managed policies that provide your team with only the permissions they need. To get started quickly, you can use our AWS managed policies. These policies cover common use cases and are available in your AWS account. For more information about AWS managed policies, see AWS managed policies in the IAM User Guide.

AWS services maintain and update AWS managed policies. You can't change the permissions in AWS managed policies. Services occasionally add additional permissions to an AWS managed policy to support new features. This type of update affects all identities (users, groups, and roles) to which the policy is attached. Services are most likely to update an AWS managed policy when a new feature is launched or when new operations become available. Services do not remove permissions from an AWS managed policy, so policy updates won't break your existing permissions.

Additionally, AWS supports managed policies for job functions that span multiple services. For example, the ReadOnlyAccess AWS managed policy provides read-only access to all AWS services and resources. When a service launches a new feature, AWS adds read-only permissions for new operations and resources. For a list and descriptions of job function policies, see AWS managed policies for job functions in the IAM User Guide.

We recommend that you use the most restricted policy that allows you to perform your use case.

The following AWS managed policies, which you can attach to users in your account, are specific to Amazon SageMaker AI:

AmazonSageMakerFullAccess – Grants full access to Amazon SageMaker AI and SageMaker AI geospatial resources and the supported operations. This does not provide unrestricted Amazon S3 access, but supports buckets and objects with specific sagemaker tags. This policy allows all IAM roles to be passed to Amazon SageMaker AI, but only allows IAM roles with "AmazonSageMaker" in them to be passed to the AWS Glue, AWS Step Functions, and AWS RoboMaker services.

AmazonSageMakerReadOnly – Grants read-only access to Amazon SageMaker AI resources.

The following AWS managed policies can be attached to users in your account but are not recommended:

AdministratorAccess – Grants all actions for all AWS services and for all resources in the account.

DataScientist – Grants a wide range of permissions to c

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ReadOnlyAccess
```

Example 2 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 3 (unknown):
```unknown
AmazonSageMakerReadOnly
```

Example 4 (unknown):
```unknown
AdministratorAccess
```

---

## Autopilot quotas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-quotas.html

**Contents:**
- Autopilot quotas
        - Note
        - Topics
- Quotas that you can increase
        - Note
        - To request a quota increase:
- Resource quotas

There are quotas that limit the resources available to you when using Amazon SageMaker Autopilot. Some of these limits are increasable and some are not.

The resource quotas documented in the following sections are valid for versions of Amazon SageMaker Studio Classic 3.22.2 and higher. For information on updating your version of SageMaker Studio Classic, see Shut Down and Update Amazon SageMaker Studio Classic and Apps.

Quotas that you can increase

The following table contains the resource limits for quotas you can increase:

*This 2 GB size limit is for a single compressed Parquet file. You can provide a Parquet dataset that includes multiple compressed Parquet files up to the input dataset maximum size. After the files are decompressed, they may each expand to a larger size.

**Autopilot automatically subsamples input datasets that are larger than the target dataset size while accounting for class imbalance and preserving rare class labels.

Open the Service Quotas console.

Select your quota increase, then choose Request increase at account level.

In the Increase quota value, enter the new limit value that you are requesting.

The following table contains the runtime resource limits for an Amazon SageMaker Autopilot job in an AWS Region.

---

## Private curated hubs for foundation model access control in JumpStart

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-curated-hubs.html

**Contents:**
- Private curated hubs for foundation model access control in JumpStart

Curate pretrained JumpStart foundation models for your organization with private hubs. Use the latest publicly available and proprietary foundation models while enforcing governance guardrails and ensuring that your organization can only access approved models.

Use private model hubs to share models and notebooks, centralize model artifacts, improve model discoverability, and streamline model use within your organization. Administrators can create private hubs that include subsets of models tailored to different teams, use cases, or security requirements. Administrators can create a JumpStart private model hub using the SageMaker Python SDK. Users can then browse, train, and deploy the curated set of models using Amazon SageMaker Studio or the SageMaker Python SDK.

For more information on creating a private model hub, see Admin guide for private model hubs in Amazon SageMaker JumpStart.

For more information on sharing private model hubs across accounts, see Cross-account sharing for private model hubs with AWS Resource Access Manager.

For more information on accessing a private model hub, see User guide.

---

## ProcessingJob

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ProcessingJob.html

**Contents:**
- ProcessingJob
- Contents
- See Also

An Amazon SageMaker processing job that is used to analyze data and evaluate models. For more information, see Process Data and Evaluate Models.

Configuration to run a processing job in a specified container image.

Type: AppSpecification object

The Amazon Resource Name (ARN) of the AutoML job associated with this processing job.

Length Constraints: Minimum length of 1. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:automl-job/.*

The time the processing job was created.

Sets the environment variables in the Docker container.

Type: String to string map

Map Entries: Minimum number of 0 items. Maximum number of 100 items.

Key Length Constraints: Minimum length of 0. Maximum length of 256.

Key Pattern: [a-zA-Z_][a-zA-Z0-9_]*

Value Length Constraints: Minimum length of 0. Maximum length of 256.

Value Pattern: [\S\s]*

A string, up to one KB in size, that contains metadata from the processing container when the processing job exits.

Length Constraints: Minimum length of 0. Maximum length of 1024.

Associates a SageMaker job as a trial component with an experiment and trial. Specified when you call the following APIs:

Type: ExperimentConfig object

A string, up to one KB in size, that contains the reason a processing job failed, if it failed.

Length Constraints: Minimum length of 0. Maximum length of 1024.

The time the processing job was last modified.

The ARN of a monitoring schedule for an endpoint associated with this processing job.

Length Constraints: Minimum length of 0. Maximum length of 256.

Networking options for a job, such as network traffic encryption between containers, whether to allow inbound and outbound network calls to and from containers, and the VPC subnets and security groups to use for VPC-enabled jobs.

Type: NetworkConfig object

The time that the processing job ended.

List of input configurations for the processing job.

Type: Array of ProcessingInput objects

Array Members: Minimum number of 0 items. Maximum number of 10 items.

The ARN of the processing job.

Length Constraints: Minimum length of 0. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:processing-job/[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

The name of the processing job.

Length Constraints: Minimum length of 1. Maximum length of 63.

Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

The status of the processing job.

Valid Values: InProgress | Completed | Failed | Stopping | Stopped

Configuration for u

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:automl-job/.*
```

Example 2 (unknown):
```unknown
[a-zA-Z_][a-zA-Z0-9_]*
```

Example 3 (unknown):
```unknown
arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:processing-job/[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

Example 4 (unknown):
```unknown
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

---

## AWS managed policies for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol.html#security-iam-awsmanpol-AmazonSageMakerReadOnly

**Contents:**
- AWS managed policies for Amazon SageMaker AI
        - Important
        - Topics
- AWS managed policy: AmazonSageMakerFullAccess
- AWS managed policy: AmazonSageMakerReadOnly
- SageMaker AI Updates to AWS Managed Policies

To add permissions to users, groups, and roles, it is easier to use AWS managed policies than to write policies yourself. It takes time and expertise to create IAM customer managed policies that provide your team with only the permissions they need. To get started quickly, you can use our AWS managed policies. These policies cover common use cases and are available in your AWS account. For more information about AWS managed policies, see AWS managed policies in the IAM User Guide.

AWS services maintain and update AWS managed policies. You can't change the permissions in AWS managed policies. Services occasionally add additional permissions to an AWS managed policy to support new features. This type of update affects all identities (users, groups, and roles) to which the policy is attached. Services are most likely to update an AWS managed policy when a new feature is launched or when new operations become available. Services do not remove permissions from an AWS managed policy, so policy updates won't break your existing permissions.

Additionally, AWS supports managed policies for job functions that span multiple services. For example, the ReadOnlyAccess AWS managed policy provides read-only access to all AWS services and resources. When a service launches a new feature, AWS adds read-only permissions for new operations and resources. For a list and descriptions of job function policies, see AWS managed policies for job functions in the IAM User Guide.

We recommend that you use the most restricted policy that allows you to perform your use case.

The following AWS managed policies, which you can attach to users in your account, are specific to Amazon SageMaker AI:

AmazonSageMakerFullAccess – Grants full access to Amazon SageMaker AI and SageMaker AI geospatial resources and the supported operations. This does not provide unrestricted Amazon S3 access, but supports buckets and objects with specific sagemaker tags. This policy allows all IAM roles to be passed to Amazon SageMaker AI, but only allows IAM roles with "AmazonSageMaker" in them to be passed to the AWS Glue, AWS Step Functions, and AWS RoboMaker services.

AmazonSageMakerReadOnly – Grants read-only access to Amazon SageMaker AI resources.

The following AWS managed policies can be attached to users in your account but are not recommended:

AdministratorAccess – Grants all actions for all AWS services and for all resources in the account.

DataScientist – Grants a wide range of permissions to c

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ReadOnlyAccess
```

Example 2 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 3 (unknown):
```unknown
AmazonSageMakerReadOnly
```

Example 4 (unknown):
```unknown
AdministratorAccess
```

---

## Launch the MLflow UI using a presigned URL

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-launch-ui.html#mlflow-launch-ui-cli

**Contents:**
- Launch the MLflow UI using a presigned URL
- Launch the MLflow UI using Studio
- Launch the MLflow UI using the AWS CLI

You can access the MLflow UI to view your experiments using a presigned URL. You can launch the MLflow UI either through Studio or using the AWS CLI in a terminal of your choice.

After creating your tracking server, you can launch the MLflow UI directly from Studio.

Navigate to Studio from the SageMaker AI console. Be sure that you are using the new Studio experience and have updated from Studio Classic. For more information, see Migration from Amazon SageMaker Studio Classic.

Choose MLflow in the Applications pane of the Studio UI.

(Optional) If have not already created a tracking server or if you need to create a new one, you can choose Create. Then provide a unique tracking server name and S3 URI for artifact storage and create a tracking server. You can optionally choose Configure for more granular tracking server customization.

Find the tracking server of your choice in the MLflow Tracking Servers pane. If the tracking server is Off, start the tracking server.

Choose the vertical menu icon in the right corner of the tracking server pane. Then, choose Open MLflow. This launches a presigned URL in a new tab in your current browser.

You can access the MLflow UI to view your experiments using a presigned URL.

Within your terminal, use the create-presigned-mlflow-tracking-server-url API to generate a presigned URL.

The output should look similar to the following:

Copy the entire presigned URL into the browser of your choice. You can use a new tab or a new private window. Press q to exit the prompt.

The --session-expiration-duration-in-seconds parameter determines the length of time that your MLflow UI session remains valid. The session duration time is the amount of time that the MLflow UI can be loaded in the browser before a new presigned URL must be created. The minimum session duration is 30 minutes (1800 seconds) and the maximum session duration is 12 hours (43200 seconds). The default session duration is 12 hours if no other duration is specified.

The --expires-in-seconds parameter determines the length of time that your presigned URL remains valid. The minimum URL expiration length is 5 seconds and the maximum URL expiration length is 5 minutes (300 seconds). The default URL expiration length is 300 seconds. The presigned URL can be used only once.

The window should look similar to the following.

**Examples:**

Example 1 (unknown):
```unknown
create-presigned-mlflow-tracking-server-url
```

Example 2 (unknown):
```unknown
aws sagemaker create-presigned-mlflow-tracking-server-url \
  --tracking-server-name $ts_name \
  --session-expiration-duration-in-seconds 1800 \
  --expires-in-seconds 300 \
  --region $region
```

Example 3 (unknown):
```unknown
{
    "AuthorizedUrl": "https://unique-key.us-west-2.experiments.sagemaker.aws.a2z.com/auth?authToken=example_token"
}
```

Example 4 (unknown):
```unknown
example_token
```

---

## Machine learning environments offered by Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/machine-learning-environments.html

**Contents:**
- Machine learning environments offered by Amazon SageMaker AI
        - Important
        - Topics

Amazon SageMaker Studio and Amazon SageMaker Studio Classic are two of the machine learning environments that you can use to interact with SageMaker AI.

If your domain was created after November 30, 2023, Studio is your default experience.

If your domain was created before November 30, 2023, Amazon SageMaker Studio Classic is your default experience. To use Studio if Amazon SageMaker Studio Classic is your default experience, see Migration from Amazon SageMaker Studio Classic.

When you migrate from Amazon SageMaker Studio Classic to Amazon SageMaker Studio, there is no loss in feature availability. Studio Classic also exists as an IDE within Amazon SageMaker Studio to help you run your legacy machine learning workflows.

SageMaker AI supports the following machine learning environments:

Amazon SageMaker Studio (Recommended): The latest web-based experience for running ML workflows with a suite of IDEs. Studio supports the following applications:

Amazon SageMaker Studio Classic

Code Editor, based on Code-OSS, Visual Studio Code - Open Source

Amazon SageMaker Canvas

Amazon SageMaker Studio Classic: Lets you build, train, debug, deploy, and monitor your machine learning models.

Amazon SageMaker Notebook Instances: Lets you prepare and process data, and train and deploy machine learning models from a compute instance running the Jupyter Notebook application.

Amazon SageMaker Studio Lab: Studio Lab is a free service that gives you access to AWS compute resources, in an environment based on open-source JupyterLab, without requiring an AWS account.

Amazon SageMaker Canvas: Gives you the ability to use machine learning to generate predictions without needing to code.

Amazon SageMaker geospatial: Gives you the ability to build, train, and deploy geospatial models.

RStudio on Amazon SageMaker AI: RStudio is an IDE for R, with a console, syntax-highlighting editor that supports direct code execution, and tools for plotting, history, debugging and workspace management.

SageMaker HyperPod: SageMaker HyperPod lets you provision resilient clusters for running machine learning (ML) workloads and developing state-of-the-art models such as large language models (LLMs), diffusion models, and foundation models (FMs).

To use these machine learning environments, you or your organization's administrator must create an Amazon SageMaker AI domain. The exceptions are Studio Lab, SageMaker Notebook Instances, and SageMaker HyperPod.

Instead of manually provisioning r

*[Content truncated]*

---

## Factorization Machines Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/fact-machines.html

**Contents:**
- Factorization Machines Algorithm
        - Note
        - Topics
- Input/Output Interface for the Factorization Machines Algorithm
- EC2 Instance Recommendation for the Factorization Machines Algorithm
- Factorization Machines Sample Notebooks

The Factorization Machines algorithm is a general-purpose supervised learning algorithm that you can use for both classification and regression tasks. It is an extension of a linear model that is designed to capture interactions between features within high dimensional sparse datasets economically. For example, in a click prediction system, the Factorization Machines model can capture click rate patterns observed when ads from a certain ad-category are placed on pages from a certain page-category. Factorization machines are a good choice for tasks dealing with high dimensional sparse datasets, such as click prediction and item recommendation.

The Amazon SageMaker AI implementation of the Factorization Machines algorithm considers only pair-wise (2nd order) interactions between features.

Input/Output Interface for the Factorization Machines Algorithm

EC2 Instance Recommendation for the Factorization Machines Algorithm

Factorization Machines Sample Notebooks

How Factorization Machines Work

Factorization Machines Hyperparameters

Tune a Factorization Machines Model

Factorization Machines Response Formats

The Factorization Machines algorithm can be run in either in binary classification mode or regression mode. In each mode, a dataset can be provided to the test channel along with the train channel dataset. The scoring depends on the mode used. In regression mode, the testing dataset is scored using Root Mean Square Error (RMSE). In binary classification mode, the test dataset is scored using Binary Cross Entropy (Log Loss), Accuracy (at threshold=0.5) and F1 Score (at threshold =0.5).

For training, the Factorization Machines algorithm currently supports only the recordIO-protobuf format with Float32 tensors. Because their use case is predominantly on sparse data, CSV is not a good candidate. Both File and Pipe mode training are supported for recordIO-wrapped protobuf.

For inference, the Factorization Machines algorithm supports the application/json and x-recordio-protobuf formats.

For the binary classification problem, the algorithm predicts a score and a label. The label is a number and can be either 0 or 1. The score is a number that indicates how strongly the algorithm believes that the label should be 1. The algorithm computes score first and then derives the label from the score value. If the score is greater than or equal to 0.5, the label is 1.

For the regression problem, just a score is returned and it is the predicted value. For example, 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
recordIO-protobuf
```

Example 2 (unknown):
```unknown
application/json
```

Example 3 (unknown):
```unknown
x-recordio-protobuf
```

---

## Shadow tests

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/shadow-tests.html

**Contents:**
- Shadow tests
        - Note

With Amazon SageMaker AI you can evaluate any changes to your model serving infrastructure by comparing its performance against the currently deployed infrastructure. This practice is known as shadow testing. Shadow testing can help you catch potential configuration errors and performance issues before they impact end users. With SageMaker AI, you don't need to invest in building your shadow testing infrastructure, so you can focus on model development.

You can use this capability to validate changes to any component of your production variant, namely the model, the container, or the instance, without any end user impact. It is useful in situations including but not limited to the following:

You are considering promoting a new model that has been validated offline to production, but want to evaluate operational performance metrics such as latency and error rate before making this decision.

You are considering changes to your serving infrastructure container, such as patching vulnerabilities or upgrading to newer versions, and want to assess the impact of these changes prior to promotion to production.

You are considering changing your ML instance and want to evaluate how the new instance would perform with live inference requests.

The SageMaker AI console provides a guided experience to manage the workflow of shadow testing. You can set up shadow tests for a predefined duration of time, monitor the progress of the test through a live dashboard, clean up upon completion, and act on the results. Select a production variant you want to test against, and SageMaker AI automatically deploys the new variant in shadow mode and routes a copy of the inference requests to it in real time within the same endpoint. Only the responses of the production variant are returned to the calling application. You can choose to discard or log the responses of the shadow variant for offline comparison. For more information on production and shadow variants, see Validation of models in production.

See Create a shadow test for instructions on creating a shadow test.

Certain endpoint features may make your endpoint incompatible with shadow tests. If your endpoint uses any of the following features, you cannot use shadow tests on your endpoint, and your request to set up shadow tests will lead to validation errors.

Asynchronous inference

Marketplace containers

Multiple-container endpoints

Multi-model endpoints

Endpoints that use Inf1 (Inferentia-based) instances

---

## Amazon SageMaker Model Monitor prebuilt container

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-pre-built-container.html

**Contents:**
- Amazon SageMaker Model Monitor prebuilt container
        - Note

SageMaker AI provides a built-in image called sagemaker-model-monitor-analyzer that provides you with a range of model monitoring capabilities, including constraint suggestion, statistics generation, constraint validation against a baseline, and emitting Amazon CloudWatch metrics. This image is based on Spark version 3.3.0 and is built with Deequ version 2.0.2.

You can not pull the built-in sagemaker-model-monitor-analyzer image directly. You can use the sagemaker-model-monitor-analyzer image when you submit a baseline processing or monitoring job using one of the AWS SDKs.

Use the SageMaker Python SDK (see image_uris.retrieve in the SageMaker AI Python SDK reference guide) to generate the ECR image URI for you, or specify the ECR image URI directly. The prebuilt image for SageMaker Model Monitor can be accessed as follows:

<ACCOUNT_ID>.dkr.ecr.<REGION_NAME>.amazonaws.com/sagemaker-model-monitor-analyzer

For example: 159807026194.dkr.ecr.us-west-2.amazonaws.com/sagemaker-model-monitor-analyzer

If you are in an AWS region in China, the prebuilt images for SageMaker Model Monitor can be accessed as follows:

<ACCOUNT_ID>.dkr.ecr.<REGION_NAME>.amazonaws.com.cn/sagemaker-model-monitor-analyzer

For account IDs and AWS Region names, see Docker Registry Paths and Example Code.

To write your own analysis container, see the container contract described in Custom monitoring schedules.

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-model-monitor-analyzer
```

Example 2 (unknown):
```unknown
sagemaker-model-monitor-analyzer
```

Example 3 (unknown):
```unknown
sagemaker-model-monitor-analyzer
```

Example 4 (unknown):
```unknown
image_uris.retrieve
```

---

## Chat for data prep

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-chat-for-data-prep.html

**Contents:**
- Chat for data prep
        - Important
        - To chat with your data

Chat for data prep requires the AmazonSageMakerCanvasAIServicesAccess policy. For more information, see AWS managed policy: AmazonSageMakerCanvasAIServicesAccess

Chat for data prep requires access to Amazon Bedrock and the Anthropic Claude model within it. For more information, see Add model access.

You must run SageMaker Canvas data prep in the same AWS Region as the Region where you're running your model. Chat for data prep is available in the US East (N. Virginia), US West (Oregon), and Europe (Frankfurt) AWS Regions.

In addition to using the built-in transforms and analyses, you can use natural language to explore, visualize, and transform your data in a conversational interface. Within the conversational interface, you can use natural language queries to understand and prepare your data to build ML models.

The following are examples of some prompts that you can use:

Drop column example-column-name

Replace missing values with median

Plot histogram of prices

What is the most expensive item sold?

How many distinct items were sold?

When you’re transforming your data using your prompts, you can view a preview that shows how data is being transformed. You can choose to add it as step in your Data Wrangler flow based on what you see in the preview.

The responses to your prompts generate code for your transformations and analyses. You can modify the code to update the output from the prompt. For example, you can modify the code for an analysis to change the values of the axes of a graph.

Use the following procedure to start chatting with your data:

Open the SageMaker Canvas data flow.

Choose the speech bubble.

(Optional) If an analysis has been generated by your query, choose Add to analyses to reference it for later.

(Optional) If you've transformed your data using a prompt, do the following.

Choose Preview to view the results.

(Optional) Modify the code in the transform and choose Update.

(Optional) If you're happy with the results of the transform, choose Add to steps to add it to the steps panel on the right-hand navigation.

After you’ve prepared your data using natural language, you can create a model using your transformed data. For more information about creating a model, see How custom models work.

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerCanvasAIServicesAccess
```

Example 2 (unknown):
```unknown
example-column-name
```

Example 3 (unknown):
```unknown
example-column-name
```

---

## Reusing Data Flows for Different Datasets

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-parameterize.html

**Contents:**
- Reusing Data Flows for Different Datasets
        - Note
        - Note
        - Important
        - Note
        - Note
        - Note

For Amazon Simple Storage Service (Amazon S3) data sources, you can create and use parameters. A parameter is a variable that you've saved in your Data Wrangler flow. Its value can be any portion of the data source's Amazon S3 path. Use parameters to quickly change the data that you're importing into a Data Wrangler flow or exporting to a processing job. You can also use parameters to select and import a specific subset of your data.

After you created a Data Wrangler flow, you might have trained a model on the data that you've transformed. For datasets that have the same schema, you can use parameters to apply the same transformations on a different dataset and train a different model. You can use the new datasets to perform inference with your model or you could be using them to retrain your model.

In general, parameters have the following attributes:

Name – The name you specify for the parameter

Type – The type of value that the parameter represents

Default value – The value of the parameter when you don't specify a new value

Datetime parameters have a time range attribute that they use as the default value.

Data Wrangler uses curly braces, {{}}, to indicate that a parameter is being used in the Amazon S3 path. For example, you can have a URL such as s3://amzn-s3-demo-bucket1/{{example_parameter_name}}/example-dataset.csv.

You create a parameter when you're editing the Amazon S3 data source that you've imported. You can set any portion of the file path to a parameter value. You can set the parameter value to either a value or a pattern. The following are the available parameter value types in the Data Wrangler flow:

You can't create a pattern parameter or a datetime parameter for the name of the bucket in the Amazon S3 path.

You must set a number as the default value of a number parameter. You can change the value of the parameter to a different number when you're editing a parameter or when you're launching a processing job. For example, in the S3 path, s3://amzn-s3-demo-bucket/example-prefix/example-file-1.csv, you can create a number parameter named number_parameter in the place of 1. Your S3 path now appears as s3://amzn-s3-demo-bucket/example-prefix/example-file-{{number_parameter}}.csv. The path continues to point to the example-file-1.csv dataset until you change the value of the parameter. If you change the value of number_parameter to 2 the path is now s3://amzn-s3-demo-bucket/example-prefix/example-file-2.csv. You can import example-f

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
s3://amzn-s3-demo-bucket1/{{example_parameter_name}}/example-dataset.csv
```

Example 2 (unknown):
```unknown
{{example_parameter_name}}
```

Example 3 (unknown):
```unknown
s3://amzn-s3-demo-bucket/example-prefix/example-file-1.csv
```

Example 4 (unknown):
```unknown
number_parameter
```

---

## AWS Managed Policies for SageMaker Projects and JumpStart

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-sc.html

**Contents:**
- AWS Managed Policies for SageMaker Projects and JumpStart
        - Topics
- AWS managed policy: AmazonSageMakerAdmin-ServiceCatalogProductsServiceRolePolicy
- AWS managed policy: AmazonSageMakerPartnerServiceCatalogProductsApiGatewayServiceRolePolicy
- AWS managed policy: AmazonSageMakerPartnerServiceCatalogProductsCloudFormationServiceRolePolicy
- AWS managed policy: AmazonSageMakerPartnerServiceCatalogProductsLambdaServiceRolePolicy
- AWS managed policy: AmazonSageMakerServiceCatalogProductsApiGatewayServiceRolePolicy
- AWS managed policy: AmazonSageMakerServiceCatalogProductsCloudformationServiceRolePolicy
- AWS managed policy: AmazonSageMakerServiceCatalogProductsCodeBuildServiceRolePolicy
- AWS managed policy: AmazonSageMakerServiceCatalogProductsCodePipelineServiceRolePolicy

These AWS managed policies add permissions to use built-in Amazon SageMaker AI project templates and JumpStart solutions. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

SageMaker Projects and JumpStart use AWS Service Catalog to provision AWS resources in customers' accounts. Some created resources need to assume an execution role. For example, if AWS Service Catalog creates a CodePipeline pipeline on behalf of a customer for a SageMaker AI machine learning CI/CD project, then that pipeline requires an IAM role.

The AmazonSageMakerServiceCatalogProductsLaunchRole role has the permissions required to launch the SageMaker AI portfolio of products from AWS Service Catalog. The AmazonSageMakerServiceCatalogProductsUseRole role has the permissions required to use the SageMaker AI portfolio of products from AWS Service Catalog. The AmazonSageMakerServiceCatalogProductsLaunchRole role passes an AmazonSageMakerServiceCatalogProductsUseRole role to the provisioned AWS Service Catalog product resources.

AWS managed policy: AmazonSageMakerAdmin-ServiceCatalogProductsServiceRolePolicy

AWS managed policy: AmazonSageMakerPartnerServiceCatalogProductsApiGatewayServiceRolePolicy

AWS managed policy: AmazonSageMakerPartnerServiceCatalogProductsCloudFormationServiceRolePolicy

AWS managed policy: AmazonSageMakerPartnerServiceCatalogProductsLambdaServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsApiGatewayServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsCloudformationServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsCodeBuildServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsCodePipelineServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsEventsServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsFirehoseServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsGlueServiceRolePolicy

AWS managed policy: AmazonSageMakerServiceCatalogProductsLambdaServiceRolePolicy

Amazon SageMaker AI updates to AWS Service Catalog AWS managed policies

This service role policy is used by the AWS Service Catalog service to provision products from the Amazon SageMaker AI portfolio. The policy grants permissions to a set of related AWS services including AWS CodePipeline, AWS CodeBuild, AWS CodeCommit, AWS Glue, AWS CloudFormation, and others.

The AmazonS

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
AmazonSageMakerAdmin-ServiceCatalogProductsServiceRolePolicy
```

Example 4 (unknown):
```unknown
AmazonSageMakerServiceCatalogProductsLaunchRole
```

---

## Task governance setup

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-tasks.html

**Contents:**
- Task governance setup
        - Topics
- Kueue Settings
        - Note
- HyperPod Task governance prerequisites
- HyperPod task governance setup

This section includes information on how to set up the Amazon SageMaker HyperPod task governance EKS add-on. This includes granting permissions that allows you to set task prioritization, compute allocation for teams, how idle compute is shared, and task preemption for teams.

If you are having issues setting up, please see Troubleshoot for known troubleshooting solutions.

HyperPod Task governance prerequisites

HyperPod task governance setup

HyperPod task governance EKS add-on installs Kueue for your HyperPod EKS clusters. Kueue is a kubernetes-native system that manages quotas and how jobs consume them.

Kueue v.012.0 and higher don't include kueue-rbac-proxy as part of the installation. Previous versions might have kueue-rbac-proxy installed. For example, if you're using Kueue v0.8.1, you might have kueue-rbac-proxy v0.18.1.

HyperPod task governance leverages Kueue for Kubernetes-native job queueing, scheduling, and quota management, and is installed with the HyperPod task governance EKS add-on. When installed, HyperPod creates and modifies SageMaker AI-managed Kubernetes resources such as KueueManagerConfig, ClusterQueues, LocalQueues, WorkloadPriorityClasses, ResourceFlavors, and ValidatingAdmissionPolicies. While Kubernetes administrators have the flexibility to modify the state of these resources, it is possible that any changes made to a SageMaker AI-managed resource may be updated and overwritten by the service.

The following information outlines the configuration settings utilized by the HyperPod task governance add-on for setting up Kueue.

For more information about each configuration entry, see Configuration in the Kueue documentation.

Ensure that you have the minimum permission policy for HyperPod cluster administrators, in IAM users for cluster admin. This includes permissions to run the SageMaker HyperPod core APIs, manage SageMaker HyperPod clusters within your AWS account, and performing the tasks in Managing SageMaker HyperPod clusters orchestrated by Amazon EKS.

You will need to have your Kubernetes version >= 1.30. For instructions, see Update existing clusters to the new Kubernetes version.

If you already have Kueue installed in their clusters, uninstall Kueue before installing the EKS add-on.

A HyperPod node must already exist in the EKS cluster before installing the HyperPod task governance add-on.

The following provides information on how to get set up with HyperPod task governance.

The following provides information on h

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
KueueManagerConfig
```

Example 2 (unknown):
```unknown
ClusterQueues
```

Example 3 (unknown):
```unknown
LocalQueues
```

Example 4 (unknown):
```unknown
WorkloadPriorityClasses
```

---

## Import

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-import.html

**Contents:**
- Import
        - Topics
        - Important
        - Important
- Import data from Amazon S3
        - Important
        - Important
        - Important
        - To import a dataset into Data Wrangler from a single file that you've stored in Amazon S3:
        - To import a dataset into Data Wrangler from multiple files that you've stored in an Amazon S3 directory

You can use Amazon SageMaker Data Wrangler to import data from the following data sources: Amazon Simple Storage Service (Amazon S3), Amazon Athena, Amazon Redshift, and Snowflake. The dataset that you import can include up to 1000 columns.

Import data from Amazon S3

Import data from Athena

Import data from Amazon Redshift

Import data from Amazon EMR

Import data from Databricks (JDBC)

Import data from Salesforce Data Cloud

Import data from Snowflake

Import Data From Software as a Service (SaaS) Platforms

Imported Data Storage

Some data sources allow you to add multiple data connections:

You can connect to multiple Amazon Redshift clusters. Each cluster becomes a data source.

You can query any Athena database in your account to import data from that database.

When you import a dataset from a data source, it appears in your data flow. Data Wrangler automatically infers the data type of each column in your dataset. To modify these types, select the Data types step and select Edit data types.

When you import data from Athena or Amazon Redshift, the imported data is automatically stored in the default SageMaker AI S3 bucket for the AWS Region in which you are using Studio Classic. Additionally, Athena stores data you preview in Data Wrangler in this bucket. To learn more, see Imported Data Storage.

The default Amazon S3 bucket may not have the least permissive security settings, such as bucket policy and server-side encryption (SSE). We strongly recommend that you Add a Bucket Policy To Restrict Access to Datasets Imported to Data Wrangler.

In addition, if you use the managed policy for SageMaker AI, we strongly recommend that you scope it down to the most restrictive policy that allows you to perform your use case. For more information, see Grant an IAM Role Permission to Use Data Wrangler.

All data sources except for Amazon Simple Storage Service (Amazon S3) require you to specify a SQL query to import your data. For each query, you must specify the following:

You can specify the name of the database or the data catalog in either the drop down menus or within the query. The following are example queries:

select * from example-data-catalog-name.example-database-name.example-table-name – The query doesn't use anything specified in the dropdown menus of the user-interface (UI) to run. It queries example-table-name within example-database-name within example-data-catalog-name.

select * from example-database-name.example-table-name – The query 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
select * from example-data-catalog-name.example-database-name.example-table-name
```

Example 2 (unknown):
```unknown
example-data-catalog-name
```

Example 3 (unknown):
```unknown
example-database-name
```

Example 4 (unknown):
```unknown
example-table-name
```

---

## Analyze and Visualize

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-analyses.html

**Contents:**
- Analyze and Visualize
- Histogram
- Scatter Plot
- Table Summary
- Quick Model
- Target Leakage
- Multicollinearity
        - Note
- Detect Anomalies In Time Series Data
- Seasonal Trend Decomposition In Time Series Data

Amazon SageMaker Data Wrangler includes built-in analyses that help you generate visualizations and data analyses in a few clicks. You can also create custom analyses using your own code.

You add an analysis to a dataframe by selecting a step in your data flow, and then choosing Add analysis. To access an analysis you've created, select the step that contains the analysis, and select the analysis.

All analyses are generated using 100,000 rows of your dataset.

You can add the following analysis to a dataframe:

Data visualizations, including histograms and scatter plots.

A quick summary of your dataset, including number of entries, minimum and maximum values (for numeric data), and most and least frequent categories (for categorical data).

A quick model of the dataset, which can be used to generate an importance score for each feature.

A target leakage report, which you can use to determine if one or more features are strongly correlated with your target feature.

A custom visualization using your own code.

Use the following sections to learn more about these options.

Use histograms to see the counts of feature values for a specific feature. You can inspect the relationships between features using the Color by option. For example, the following histogram charts the distribution of user ratings of the best-selling books on Amazon from 2009–2019, colored by genre.

You can use the Facet by feature to create histograms of one column, for each value in another column. For example, the following diagram shows histograms of user reviews of best-selling books on Amazon if faceted by year.

Use the Scatter Plot feature to inspect the relationship between features. To create a scatter plot, select a feature to plot on the X axis and the Y axis. Both of these columns must be numeric typed columns.

You can color scatter plots by an additional column. For example, the following example shows a scatter plot comparing the number of reviews against user ratings of top-selling books on Amazon between 2009 and 2019. The scatter plot is colored by book genre.

Additionally, you can facet scatter plots by features. For example, the following image shows an example of the same review versus user rating scatter plot, faceted by year.

Use the Table Summary analysis to quickly summarize your data.

For columns with numerical data, including log and float data, a table summary reports the number of entries (count), minimum (min), maximum (max), mean, and standard deviati

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
import altair as alt
df = df.iloc[:30]
df = df.rename(columns={"Age": "value"})
df = df.assign(count=df.groupby('value').value.transform('count'))
df = df[["value", "count"]]
base = alt.Chart(df)
bar = base.mark_bar().encode(x=alt.X('value', bin=True, axis=None), y=alt.Y('count'))
rule = base.mark_rule(color='red').encode(
    x='mean(value):Q',
    size=alt.value(5))
chart = bar + rule
```

Example 2 (unknown):
```unknown
import altair as alt

# Specify the number of top rows for plotting
rows_number = 1000
df = df.head(rows_number)
# You can also choose bottom rows or randomly sampled rows
# df = df.tail(rows_number)
# df = df.sample(rows_number)


chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        # Specify the column names for binning and number of bins for X and Y axis
        x=alt.X("col1:Q", bin=alt.Bin(maxbins=20)),
        y=alt.Y("col2:Q", bin=alt.Bin(maxbins=20)),
        size="count()",
    )
)

# :Q specifies that label column has quantitative type.
# For more details on Altair typ
...
```

---

## Amazon SageMaker ML Lineage Tracking

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html

**Contents:**
- Amazon SageMaker ML Lineage Tracking
        - Important
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

Amazon SageMaker ML Lineage Tracking creates and stores information about the steps of a machine learning (ML) workflow from data preparation to model deployment. With the tracking information, you can reproduce the workflow steps, track model and dataset lineage, and establish model governance and audit standards.

SageMaker AI’s Lineage Tracking feature works in the backend to track all the metadata associated with your model training and deployment workflows. This includes your training jobs, datasets used, pipelines, endpoints, and the actual models. You can query the lineage service at any point to find the exact artifacts used to train a model. Using those artifacts, you can recreate the same ML workflow to reproduce the model as long as you have access to the exact dataset that was used. A trial component tracks the training job. This trial component has all the parameters used as part of the training job. If you don’t need to rerun the entire workflow, you can reproduce the training job to derive the same model.

With SageMaker AI Lineage Tracking data scientists and model builders can do the following:

Keep a running history of model discovery experiments.

Establish model governance by tracking model lineage artifacts for auditing and compliance verification.

The following diagram shows an example lineage graph that Amazon SageMaker AI automatically creates in an end-to-end model training and deployment ML workflow.

Lineage Tracking Entities

Amazon SageMaker AI–Created Tracking Entities

Manually Create Tracking Entities

Querying Lineage Entities

Tracking Cross-Account Lineage

---

## IP Insights

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/ip-insights.html

**Contents:**
- IP Insights
        - Topics
- Input/Output Interface for the IP Insights Algorithm
- EC2 Instance Recommendation for the IP Insights Algorithm
  - GPU Instances for the IP Insights Algorithm
  - CPU Instances for the IP Insights Algorithm
- IP Insights Sample Notebooks

Amazon SageMaker AI IP Insights is an unsupervised learning algorithm that learns the usage patterns for IPv4 addresses. It is designed to capture associations between IPv4 addresses and various entities, such as user IDs or account numbers. You can use it to identify a user attempting to log into a web service from an anomalous IP address, for example. Or you can use it to identify an account that is attempting to create computing resources from an unusual IP address. Trained IP Insight models can be hosted at an endpoint for making real-time predictions or used for processing batch transforms.

SageMaker AI IP insights ingests historical data as (entity, IPv4 Address) pairs and learns the IP usage patterns of each entity. When queried with an (entity, IPv4 Address) event, a SageMaker AI IP Insights model returns a score that infers how anomalous the pattern of the event is. For example, when a user attempts to log in from an IP address, if the IP Insights score is high enough, a web login server might decide to trigger a multi-factor authentication system. In more advanced solutions, you can feed the IP Insights score into another machine learning model. For example, you can combine the IP Insight score with other features to rank the findings of another security system, such as those from Amazon GuardDuty.

The SageMaker AI IP Insights algorithm can also learn vector representations of IP addresses, known as embeddings. You can use vector-encoded embeddings as features in downstream machine learning tasks that use the information observed in the IP addresses. For example, you can use them in tasks such as measuring similarities between IP addresses in clustering and visualization tasks.

Input/Output Interface for the IP Insights Algorithm

EC2 Instance Recommendation for the IP Insights Algorithm

IP Insights Sample Notebooks

How IP Insights Works

IP Insights Hyperparameters

Tune an IP Insights Model

IP Insights Data Formats

Training and Validation

The SageMaker AI IP Insights algorithm supports training and validation data channels. It uses the optional validation channel to compute an area-under-curve (AUC) score on a predefined negative sampling strategy. The AUC metric validates how well the model discriminates between positive and negative samples. Training and validation data content types need to be in text/csv format. The first column of the CSV data is an opaque string that provides a unique identifier for the entity. The second column i

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application/json
```

Example 2 (unknown):
```unknown
application/jsonlines
```

Example 3 (unknown):
```unknown
application/json
```

Example 4 (unknown):
```unknown
application/jsonlines
```

---

## Create Regression or Classification Jobs for Tabular Data Using the AutoML API

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development-create-experiment.html

**Contents:**
- Create Regression or Classification Jobs for Tabular Data Using the AutoML API
        - Note
- Required parameters
- Optional parameters
    - Features selection
        - Note
    - Algorithms selection
        - Note
- Migrate a CreateAutoMLJob to CreateAutoMLJobV2

You can create an Autopilot regression or classification job for tabular data programmatically by calling the CreateAutoMLJobV2 API action in any language supported by Autopilot or the AWS CLI. The following is a collection of mandatory and optional input request parameters for the CreateAutoMLJobV2 API action. You can find the alternative information for the previous version of this action, CreateAutoMLJob. However, we recommend using CreateAutoMLJobV2.

For information on how this API action translates into a function in the language of your choice, see the See Also section of CreateAutoMLJobV2 and choose an SDK. As an example, for Python users, see the full request syntax of create_auto_ml_job_v2 in AWS SDK for Python (Boto3).

CreateAutoMLJobV2 and DescribeAutoMLJobV2 are new versions of CreateAutoMLJob and DescribeAutoMLJob which offer backward compatibility.

We recommend using the CreateAutoMLJobV2. CreateAutoMLJobV2 can manage tabular problem types identical to those of its previous version CreateAutoMLJob, as well as non-tabular problem types such as image or text classification, or time-series forecasting.

At a minimum, all experiments on tabular data require the specification of the experiment name, providing locations for the input and output data, and specifying which target data to predict. Optionally, you can also specify the type of problem that you want to solve (regression, classification, multiclass classification), choose your modeling strategy (stacked ensembles or hyperparameters optimization), select the list of algorithms used by the Autopilot job to train the data, and more.

After the experiment runs, you can compare trials and delve into the details of the pre-processing steps, algorithms, and hyperparameter ranges of each model. You also have the option to download their explainability and performance reports. Use the provided notebooks to see the results of the automated data exploration or the candidate model definitions.

Find guidelines on how to migrate a CreateAutoMLJob to CreateAutoMLJobV2 in Migrate a CreateAutoMLJob to CreateAutoMLJobV2.

When calling CreateAutoMLJobV2 to create an Autopilot experiment for tabular data, you must provide the following values:

An AutoMLJobName to specify the name of your job.

At least one AutoMLJobChannel in AutoMLJobInputDataConfig to specify your data source.

Both an AutoMLJobObjective metric and your chosen type of supervised learning problem (binary classification, multiclass clas

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 2 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 3 (unknown):
```unknown
CreateAutoMLJob
```

Example 4 (unknown):
```unknown
CreateAutoMLJobV2
```

---

## Create a model in Amazon SageMaker AI with ModelBuilder

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-modelbuilder-creation.html

**Contents:**
- Create a model in Amazon SageMaker AI with ModelBuilder
- Build your model with ModelBuilder
- Define serialization and deserialization methods
        - Topics
- Customize model loading and handling of requests
- Build your model and deploy
- Bring your own container (BYOC)
- Using ModelBuilder in local mode
  - Troubleshooting local mode
- ModelBuilder examples

Preparing your model for deployment on a SageMaker AI endpoint requires multiple steps, including choosing a model image, setting up the endpoint configuration, coding your serialization and deserialization functions to transfer data to and from server and client, identifying model dependencies, and uploading them to Amazon S3. ModelBuilder can reduce the complexity of initial setup and deployment to help you create a deployable model in a single step.

ModelBuilder performs the following tasks for you:

Converts machine learning models trained using various frameworks like XGBoost or PyTorch into deployable models in one step.

Performs automatic container selection based on the model framework so you don’t have to manually specify your container. You can still bring your own container by passing your own URI to ModelBuilder.

Handles the serialization of data on the client side before sending it to the server for inference and deserialization of the results returned by the server. Data is correctly formatted without manual processing.

Enables automatic capture of dependencies and packages the model according to model server expectations. ModelBuilder's automatic capture of dependencies is a best-effort approach to dynamically load dependencies. (We recommend that you test the automated capture locally and update the dependencies to meet your needs.)

For large language model (LLM) use cases, optionally performs local parameter tuning of serving properties that can be deployed for better performance when hosting on a SageMaker AI endpoint.

Supports most of the popular model servers and containers like TorchServe, Triton, DJLServing and TGI container.

ModelBuilder is a Python class that takes a framework model, such as XGBoost or PyTorch, or a user-specified inference specification and converts it into a deployable model. ModelBuilder provides a build function that generates the artifacts for deployment. The model artifact generated is specific to the model server, which you can also specify as one of the inputs. For more details about the ModelBuilder class, see ModelBuilder.

The following diagram illustrates the overall model creation workflow when you use ModelBuilder. ModelBuilder accepts a model or inference specification along with your schema to create a deployable model that you can test locally before deployment.

ModelBuilder can handle any customization you want to apply. However, to deploy a framework model, the model builder expects at min

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ModelBuilder
```

Example 2 (unknown):
```unknown
ModelBuilder
```

Example 3 (unknown):
```unknown
ModelBuilder
```

Example 4 (unknown):
```unknown
ModelBuilder
```

---

## ListFeatureGroups

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ListFeatureGroups.html

**Contents:**
- ListFeatureGroups
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

List FeatureGroups based on given filter and order.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Use this parameter to search for FeatureGroupss created after a specific date and time.

Use this parameter to search for FeatureGroupss created before a specific date and time.

A FeatureGroup status. Filters by FeatureGroup status.

Valid Values: Creating | Created | CreateFailed | Deleting | DeleteFailed

The maximum number of results returned by ListFeatureGroups.

Valid Range: Minimum value of 1. Maximum value of 100.

A string that partially matches one or more FeatureGroups names. Filters FeatureGroups by name.

Length Constraints: Minimum length of 1. Maximum length of 64.

A token to resume pagination of ListFeatureGroups results.

Length Constraints: Minimum length of 0. Maximum length of 8192.

An OfflineStore status. Filters by OfflineStore status.

Valid Values: Active | Blocked | Disabled

The value on which the feature group list is sorted.

Valid Values: Name | FeatureGroupStatus | OfflineStoreStatus | CreationTime

The order in which feature groups are listed.

Valid Values: Ascending | Descending

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

A summary of feature groups.

Type: Array of FeatureGroupSummary objects

A token to resume pagination of ListFeatureGroups results.

Length Constraints: Minimum length of 0. Maximum length of 8192.

For information about the errors that are common to all actions, see Common Errors.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

AWS Command Line Interface V2

AWS SDK for JavaScript V3

**Examples:**

Example 1 (unknown):
```unknown
FeatureGroup
```

Example 2 (unknown):
```unknown
{
   "CreationTimeAfter": number,
   "CreationTimeBefore": number,
   "FeatureGroupStatusEquals": "string",
   "MaxResults": number,
   "NameContains": "string",
   "NextToken": "string",
   "OfflineStoreStatusEquals": "string",
   "SortBy": "string",
   "SortOrder": "string"
}
```

Example 3 (unknown):
```unknown
FeatureGroups
```

Example 4 (unknown):
```unknown
FeatureGroups
```

---

## AWS managed policies for Amazon SageMaker Partner AI Apps

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-partner-apps.html

**Contents:**
- AWS managed policies for Amazon SageMaker Partner AI Apps
        - Topics
- AWS managed policy: AmazonSageMakerPartnerAppsFullAccess
- Amazon SageMaker AI updates to Partner AI Apps managed policies

These AWS managed policies add permissions required to use Amazon SageMaker Partner AI Apps. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerPartnerAppsFullAccess

Amazon SageMaker AI updates to Partner AI Apps managed policies

Allows full administrative access to Amazon SageMaker Partner AI Apps.

This AWS managed policy includes the following permissions.

sagemaker – Gives Amazon SageMaker Partner AI App users permission to access applications, list available applications, launch application web UIs, and connect using the application SDK.

View details about updates to AWS managed policies for Partner AI Apps since this service began tracking these changes. For automatic alerts about changes to this page, subscribe to the RSS feed on the SageMaker AI Document history page.

AmazonSageMakerPartnerAppsFullAccess - New policy

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AmazonSageMakerPartnerListAppsPermission",
            "Effect": "Allow",
            "Action": "sagemaker:ListPartnerApps",
            "Resource": "*"
        },
        {
            "Sid": "AmazonSageMakerPartnerAppsPermission",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreatePartnerAppPresignedUrl",
                "sagemaker:DescribePartnerApp",
                "sagemaker:CallPartnerAppApi"
            ],
            "Condition": {
                "StringEquals": {
     
...
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "AmazonSageMakerPartnerListAppsPermission",
            "Effect": "Allow",
            "Action": "sagemaker:ListPartnerApps",
            "Resource": "*"
        },
        {
            "Sid": "AmazonSageMakerPartnerAppsPermission",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreatePartnerAppPresignedUrl",
                "sagemaker:DescribePartnerApp",
                "sagemaker:CallPartnerAppApi"
            ],
            "Condition": {
                "StringEquals": {
     
...
```

---

## Shut Down Data Wrangler

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-shut-down.html

**Contents:**
- Shut Down Data Wrangler
        - To shut down the Data Wrangler instance in Studio Classic
        - Important

When you are not using Data Wrangler, it is important to shut down the instance on which it runs to avoid incurring additional fees.

To avoid losing work, save your data flow before shutting Data Wrangler down. To save your data flow in Studio Classic, choose File and then choose Save Data Wrangler Flow. Data Wrangler automatically saves your data flow every 60 seconds.

In Studio Classic, select the Running Instances and Kernels icon ( ).

Under RUNNING APPS is the sagemaker-data-wrangler-1.0 app. Select the shutdown icon ( ) next to this app .

Data Wrangler runs on an ml.m5.4xlarge instance. This instance disappears from RUNNING INSTANCES when you shut down the Data Wrangler app.

If you open Data Wrangler again, an Amazon EC2 instance starts running the application and you will be charged for the compute. In addition to compute, you are also charged for the storage that you use. For example, you're charged for any Amazon S3 buckets that you're using with Data Wrangler.

If you find that you're still getting charged for Data Wrangler after shutting down your applications, there's a Jupyter extension that you can use to automatically shut down idle sessions. For information about the extension, see SageMaker-Studio-Autoshutdown-Extension.

After you shut down the Data Wrangler app, it has to restart the next time you open a Data Wrangler flow file. This can take a few minutes.

---

## Monitoring a Model in Production

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-model-monitor.html

**Contents:**
- Monitoring a Model in Production

After you deploy a model into your production environment, use Amazon SageMaker Model Monitor to continuously monitor the quality of your machine learning models in real time. Amazon SageMaker Model Monitor enables you to set up an automated alert triggering system when there are deviations in the model quality, such as data drift and anomalies. Amazon CloudWatch Logs collects log files of monitoring the model status and notifies when the quality of your model hits certain thresholds that you preset. CloudWatch stores the log files to an Amazon S3 bucket you specify. Early and pro-active detection of model deviations through AWS model monitor products enables you to take prompt actions to maintain and improve the quality of your deployed model.

For more information about SageMaker Model Monitoring products, see Data and model quality monitoring with Amazon SageMaker Model Monitor.

To start your machine learning journey with SageMaker AI, sign up for an AWS account at Set Up SageMaker AI.

---

## Advanced model building configurations

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-advanced-settings.html

**Contents:**
- Advanced model building configurations
        - Note
- Advanced numeric and categorical prediction model settings
  - Objective metric
  - Training method
  - Algorithms
  - Data split
  - Max candidates
        - Note
  - Max job runtime

Amazon SageMaker Canvas supports various advanced settings that you can configure when building a model. The following page lists all of the advanced settings along with additional information about their options and configurations.

The following advanced settings are currently only supported for numeric, categorical, and time series forecasting model types.

Canvas supports the following advanced settings for numeric and categorical prediction model types.

The objective metric is the metric that you want Canvas to optimize while building your model. If you don’t select a metric, Canvas chooses one for you by default. For descriptions of the available metrics, see the Metrics reference.

Canvas can automatically select the training method based on the dataset size, or you can select it manually. The following training methods are available for you to choose from:

Ensembling – SageMaker AI leverages the AutoGluon library to train several base models. To find the best combination for your dataset, ensemble mode runs 5–10 trials with different model and meta parameter settings. Then, these models are combined using a stacking ensemble method to create an optimal predictive model. For a list of algorithms supported by ensemble mode for tabular data, see the following Algorithms section.

Hyperparameter optimization (HPO) – SageMaker AI finds the best version of a model by tuning hyperparameters using Bayesian optimization or multi-fidelity optimization while running training jobs on your dataset. HPO mode selects the algorithms that are most relevant to your dataset and selects the best range of hyperparameters to tune your models. To tune your models, HPO mode runs up to 100 trials (default) to find the optimal hyperparameters settings within the selected range. If your dataset size is less than 100 MB, SageMaker AI uses Bayesian optimization. SageMaker AI chooses multi-fidelity optimization if your dataset is larger than 100 MB.

For a list of algorithms supported by HPO mode for tabular data, see the following Algorithms section.

Auto – SageMaker AI automatically chooses either ensembling mode or HPO mode based on your dataset size. If your dataset is larger than 100 MB, SageMaker AI chooses HPO mode. Otherwise, it chooses ensembling mode.

In Ensembling mode, Canvas supports the following machine learning algorithms:

LightGBM – An optimized framework that uses tree-based algorithms with gradient boosting. This algorithm uses trees that grow in breadth

*[Content truncated]*

---

## Create an Image Classification Job using the AutoML API

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-create-experiment-image-classification.html

**Contents:**
- Create an Image Classification Job using the AutoML API
        - Note
- Required parameters
- Optional parameters

The following instructions show how to create an Amazon SageMaker Autopilot job as a pilot experiment for image classification problem types using SageMaker API Reference.

Tasks such as text and image classification, time-series forecasting, and fine-tuning of large language models are exclusively available through the version 2 of the AutoML REST API. If your language of choice is Python, you can refer to AWS SDK for Python (Boto3) or the AutoMLV2 object of the Amazon SageMaker Python SDK directly.

Users who prefer the convenience of a user interface can use Amazon SageMaker Canvas to access pre-trained models and generative AI foundation models, or create custom models tailored for specific text, image classification, forecasting needs, or generative AI.

You can create an Autopilot image classification experiment programmatically by calling the CreateAutoMLJobV2 API action in any language supported by Amazon SageMaker Autopilot or the AWS CLI.

For information on how this API action translates into a function in the language of your choice, see the See Also section of CreateAutoMLJobV2 and choose an SDK. As an example, for Python users, see the full request syntax of create_auto_ml_job_v2 in AWS SDK for Python (Boto3).

The following is a collection of mandatory and optional input request parameters for the CreateAutoMLJobV2 API action used in image classification.

When calling CreateAutoMLJobV2 to create an Autopilot experiment for image classification, you must provide the following values:

An AutoMLJobName to specify the name of your job.

At least one AutoMLJobChannel in AutoMLJobInputDataConfig to specify your data source.

An AutoMLProblemTypeConfig of type ImageClassificationJobConfig.

An OutputDataConfig to specify the Amazon S3 output path to store the artifacts of your AutoML job.

A RoleArn to specify the ARN of the role used to access your data.

All other parameters are optional.

The following sections provide details of some optional parameters that you can pass to your image classification AutoML job.

You can provide your own validation dataset and custom data split ratio, or let Autopilot split the dataset automatically.

Each AutoMLJobChannel object (see the required parameter AutoMLJobInputDataConfig) has a ChannelType, which can be set to either training or validation values that specify how the data is to be used when building a machine learning model.

At least one data source must be provided and a maximum of two data source

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 2 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 3 (unknown):
```unknown
create_auto_ml_job_v2
```

Example 4 (unknown):
```unknown
CreateAutoMLJobV2
```

---

## AWS managed policies for Amazon SageMaker Canvas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-canvas.html#security-iam-awsmanpol-AmazonSageMakerCanvasSMDataScienceAssistantAccess

**Contents:**
- AWS managed policies for Amazon SageMaker Canvas
        - Topics
- AWS managed policy: AmazonSageMakerCanvasFullAccess
- AWS managed policy: AmazonSageMakerCanvasDataPrepFullAccess
- AWS managed policy: AmazonSageMakerCanvasDirectDeployAccess
- AWS managed policy: AmazonSageMakerCanvasAIServicesAccess
- AWS managed policy: AmazonSageMakerCanvasBedrockAccess
- AWS managed policy: AmazonSageMakerCanvasForecastAccess
- AWS managed policy: AmazonSageMakerCanvasEMRServerlessExecutionRolePolicy
- AWS managed policy: AmazonSageMakerCanvasSMDataScienceAssistantAccess

These AWS managed policies add permissions required to use Amazon SageMaker Canvas. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerCanvasFullAccess

AWS managed policy: AmazonSageMakerCanvasDataPrepFullAccess

AWS managed policy: AmazonSageMakerCanvasDirectDeployAccess

AWS managed policy: AmazonSageMakerCanvasAIServicesAccess

AWS managed policy: AmazonSageMakerCanvasBedrockAccess

AWS managed policy: AmazonSageMakerCanvasForecastAccess

AWS managed policy: AmazonSageMakerCanvasEMRServerlessExecutionRolePolicy

AWS managed policy: AmazonSageMakerCanvasSMDataScienceAssistantAccess

Amazon SageMaker AI updates to Amazon SageMaker Canvas managed policies

This policy grants permissions that allow full access to Amazon SageMaker Canvas through the AWS Management Console and SDK. The policy also provides select access to related services [for example, Amazon Simple Storage Service (Amazon S3), AWS Identity and Access Management (IAM), Amazon Virtual Private Cloud (Amazon VPC), Amazon Elastic Container Registry (Amazon ECR), Amazon CloudWatch Logs, Amazon Redshift, AWS Secrets Manager, Amazon SageMaker Autopilot, SageMaker Model Registry, and Amazon Forecast].

This policy is intended to help customers experiment and get started with all the capabilities of SageMaker Canvas. For more fine-grained control, we suggest customers build their own scoped down versions as they move to production workloads. For more information, see IAM policy types: How and when to use them.

This AWS managed policy includes the following permissions.

sagemaker – Allows principals to create and host SageMaker AI models on resources whose ARN contains "Canvas", "canvas", or "model-compilation-". Additionally, users can register their SageMaker Canvas model to SageMaker AI Model Registry in the same AWS account. Also allows principals to create and manage SageMaker training, transform, and AutoML jobs.

application-autoscaling – Allows principals to automatically scale a SageMaker AI inference endpoint.

athena – Allows principals to query a list of data catalogs, databases, and table metadata from Amazon Athena, and access the tables in the catalogs.

cloudwatch – Allows principals to create and manage Amazon CloudWatch alarms.

ec2 – Allows principals to create Amazon VPC endpoints.

ecr – Allows principals to get information about a container image.

emr-serverless – Allows pri

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application-autoscaling
```

Example 2 (unknown):
```unknown
emr-serverless
```

Example 3 (unknown):
```unknown
Source:SageMakerCanvas
```

Example 4 (unknown):
```unknown
redshift-data
```

---

## SageMaker HyperPod task governance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance.html

**Contents:**
- SageMaker HyperPod task governance
        - Topics

SageMaker HyperPod task governance is a robust management system designed to streamline resource allocation and ensure efficient utilization of compute resources across teams and projects for your Amazon EKS clusters. This provides administrators with the capability to set:

Priority levels for various tasks

Compute allocation for each team

How each team lends and borrows idle compute

If a team preempts their own tasks

HyperPod task governance also provides Amazon EKS cluster Observability, offering real-time visibility into cluster capacity. This includes compute availability and usage, team allocation and utilization, and task run and wait time information, setting you up for informed decision-making and proactive resource management.

The following sections cover how to set up, understand key concepts, and use HyperPod task governance for your Amazon EKS clusters.

Setup for SageMaker HyperPod task governance

Example HyperPod task governance AWS CLI commands

Attribution document for Amazon SageMaker HyperPod task governance

---

## XGBoost algorithm with Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html

**Contents:**
- XGBoost algorithm with Amazon SageMaker AI
- Supported versions
        - Warning
        - Important
        - Warning
        - Note
        - Note
- EC2 instance recommendation for the XGBoost algorithm
  - Training
    - CPU training

The XGBoost (eXtreme Gradient Boosting) is a popular and efficient open-source implementation of the gradient boosted trees algorithm. Gradient boosting is a supervised learning algorithm that tries to accurately predict a target variable by combining multiple estimates from a set of simpler models. The XGBoost algorithm performs well in machine learning competitions for the following reasons:

Its robust handling of a variety of data types, relationships, distributions.

The variety of hyperparameters that you can fine-tune.

You can use XGBoost for regression, classification (binary and multiclass), and ranking problems.

You can use the new release of the XGBoost algorithm as either:

A Amazon SageMaker AI built-in algorithm.

A framework to run training scripts in your local environments.

This implementation has a smaller memory footprint, better logging, improved hyperparameter validation, and an bigger set of metrics than the original versions. It provides an XGBoost estimator that runs a training script in a managed XGBoost environment. The current release of SageMaker AI XGBoost is based on the original XGBoost versions 1.0, 1.2, 1.3, 1.5, and 1.7.

For more information about the Amazon SageMaker AI XGBoost algorithm, see the following blog posts:

Introducing the open-source Amazon SageMaker AI XGBoost algorithm container

Amazon SageMaker AI XGBoost now offers fully distributed GPU training

Framework (open source) mode: 1.2-1, 1.2-2, 1.3-1, 1.5-1, 1.7-1

Algorithm mode: 1.2-1, 1.2-2, 1.3-1, 1.5-1, 1.7-1

Due to required compute capacity, version 1.7-1 of SageMaker AI XGBoost is not compatible with GPU instances from the P2 instance family for training or inference.

When you retrieve the SageMaker AI XGBoost image URI, do not use :latest or :1 for the image URI tag. You must specify one of the Supported versions to choose the SageMaker AI-managed XGBoost container with the native XGBoost package version that you want to use. To find the package version migrated into the SageMaker AI XGBoost containers, see Docker Registry Paths and Example Code. Then choose your AWS Region, and navigate to the XGBoost (algorithm) section.

The XGBoost 0.90 versions are deprecated. Supports for security updates or bug fixes for XGBoost 0.90 is discontinued. We highly recommend that you upgrade the XGBoost version to one of the newer versions.

XGBoost v1.1 is not supported on SageMaker AI. XGBoost 1.1 has a broken capability to run prediction when the test input

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
tree_method
```

Example 2 (unknown):
```unknown
instance_count
```

Example 3 (unknown):
```unknown
ShardedByS3Key
```

Example 4 (unknown):
```unknown
distribution
```

---

## AWS managed policies for Amazon SageMaker Feature Store

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-feature-store.html

**Contents:**
- AWS managed policies for Amazon SageMaker Feature Store
        - Topics
- AWS managed policy: AmazonSageMakerFeatureStoreAccess
- Amazon SageMaker AI updates to Amazon SageMaker Feature Store managed policies

These AWS managed policies add permissions required to use Feature Store. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerFeatureStoreAccess

Amazon SageMaker AI updates to Amazon SageMaker Feature Store managed policies

This policy grants permissions required to enable the offline store for an Amazon SageMaker Feature Store feature group.

This AWS managed policy includes the following permissions.

s3 – Allows principals to write data into an offline store Amazon S3 bucket. These buckets are limited to those whose name includes "SageMaker", "Sagemaker", or "sagemaker".

s3 – Allows principals to read existing manifest files maintained in the metadata folder of an offline store S3 bucket.

glue – Allows principals to read and update AWS Glue tables. These permissions are limited to tables in the sagemaker_featurestore folder.

View details about updates to AWS managed policies for Feature Store since this service began tracking these changes. For automatic alerts about changes to this page, subscribe to the RSS feed on the SageMaker AI Document history page.

AmazonSageMakerFeatureStoreAccess - Update to an existing policy

Add s3:GetObject, glue:GetTable, and glue:UpdateTable permissions.

AmazonSageMakerFeatureStoreAccess - Update to an existing policy

Add s3:PutObjectAcl permission.

AmazonSageMakerFeatureStoreAccess - New policy

**Examples:**

Example 1 (unknown):
```unknown
sagemaker_featurestore
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetBucketAcl",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::*SageMaker*",
                "arn:aws:s3:::*Sagemaker*",
                "arn:aws:s3:::*sagemaker*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::*SageMaker*/metadata/
...
```

Example 3 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetBucketAcl",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::*SageMaker*",
                "arn:aws:s3:::*Sagemaker*",
                "arn:aws:s3:::*sagemaker*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::*SageMaker*/metadata/
...
```

Example 4 (unknown):
```unknown
s3:GetObject
```

---

## Linear Learner Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/linear-learner.html

**Contents:**
- Linear Learner Algorithm
        - Topics
- Input/Output interface for the linear learner algorithm
- EC2 instance recommendation for the linear learner algorithm
- Linear learner sample notebooks

Linear models are supervised learning algorithms used for solving either classification or regression problems. For input, you give the model labeled examples (x, y). x is a high-dimensional vector and y is a numeric label. For binary classification problems, the label must be either 0 or 1. For multiclass classification problems, the labels must be from 0 to num_classes - 1. For regression problems, y is a real number. The algorithm learns a linear function, or, for classification problems, a linear threshold function, and maps a vector x to an approximation of the label y.

The Amazon SageMaker AI linear learner algorithm provides a solution for both classification and regression problems. With the SageMaker AI algorithm, you can simultaneously explore different training objectives and choose the best solution from a validation set. You can also explore a large number of models and choose the best. The best model optimizes either of the following:

Continuous objectives, such as mean square error, cross entropy loss, absolute error.

Discrete objectives suited for classification, such as F1 measure, precision, recall, or accuracy.

Compared with methods that provide a solution for only continuous objectives, the SageMaker AI linear learner algorithm provides a significant increase in speed over naive hyperparameter optimization techniques. It is also more convenient.

The linear learner algorithm requires a data matrix, with rows representing the observations, and columns representing the dimensions of the features. It also requires an additional column that contains the labels that match the data points. At a minimum, Amazon SageMaker AI linear learner requires you to specify input and output data locations, and objective type (classification or regression) as arguments. The feature dimension is also required. For more information, see CreateTrainingJob. You can specify additional parameters in the HyperParameters string map of the request body. These parameters control the optimization procedure, or specifics of the objective function that you train on. For example, the number of epochs, regularization, and loss type.

If you're using Managed Spot Training, the linear learner algorithm supports using checkpoints to take a snapshot of the state of the model.

Input/Output interface for the linear learner algorithm

EC2 instance recommendation for the linear learner algorithm

Linear learner sample notebooks

How linear learner works

Linear learner hype

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
num_classes
```

Example 2 (unknown):
```unknown
CreateTrainingJob
```

Example 3 (unknown):
```unknown
HyperParameters
```

Example 4 (unknown):
```unknown
S3DataDistributionType
```

---

## Get Insights On Data and Data Quality

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-data-insights.html

**Contents:**
- Get Insights On Data and Data Quality
        - To create a Data Quality and Insights report
        - Note
        - Topics
- Summary
- Target column
- Quick model
- Feature summary
- Samples
- Definitions

Use the Data Quality and Insights Report to perform an analysis of the data that you've imported into Data Wrangler. We recommend that you create the report after you import your dataset. You can use the report to help you clean and process your data. It gives you information such as the number of missing values and the number of outliers. If you have issues with your data, such as target leakage or imbalance, the insights report can bring those issues to your attention.

Use the following procedure to create a Data Quality and Insights report. It assumes that you've already imported a dataset into your Data Wrangler flow.

Choose a + next to a node in your Data Wrangler flow.

Select Get data insights.

For Analysis name, specify a name for the insights report.

(Optional) For Target column, specify the target column.

For Problem type, specify Regression or Classification.

For Data size, specify one of the following:

50 K – Uses the first 50000 rows of the dataset that you've imported to create the report.

Entire dataset – Uses the entire dataset that you've imported to create the report.

Creating a Data Quality and Insights report on the entire dataset uses an Amazon SageMaker processing job. A SageMaker Processing job provisions the additional compute resources required to get insights for all of your data. For more information about SageMaker Processing jobs, see Data transformation workloads with SageMaker Processing.

The following topics show the sections of the report:

You can either download the report or view it online. To download the report, choose the download button at the top right corner of the screen. The following image shows the button.

The insights report has a brief summary of the data that includes general information such as missing values, invalid values, feature types, outlier counts, and more. It can also include high severity warnings that point to probable issues with the data. We recommend that you investigate the warnings.

The following is an example of a report summary.

When you create the data quality and insights report, Data Wrangler gives you the option to select a target column. A target column is a column that you're trying to predict. When you choose a target column, Data Wrangler automatically creates a target column analysis. It also ranks the features in the order of their predictive power. When you select a target column, you must specify whether you’re trying to solve a regression or a classification prob

*[Content truncated]*

---

## Setup for SageMaker HyperPod task governance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-setup.html

**Contents:**
- Setup for SageMaker HyperPod task governance
        - Topics

The following section provides information on how to get set up with the Amazon CloudWatch Observability EKS and SageMaker HyperPod task governance add-ons.

Ensure that you have the minimum permission policy for HyperPod cluster administrators with Amazon EKS, in IAM users for cluster admin. This includes permissions to run the SageMaker HyperPod core APIs and manage SageMaker HyperPod clusters within your AWS account, performing the tasks in Managing SageMaker HyperPod clusters orchestrated by Amazon EKS.

Task governance setup

---

## Advanced topics

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-advanced-topics.html

**Contents:**
- Advanced topics
        - Topics

The following sections contain more advanced tasks that explain how to customize monitoring using preprocessing and postprocessing scripts, how to build your own container, and how to use AWS CloudFormation to create a monitoring schedule.

Custom monitoring schedules

Create a Monitoring Schedule for a Real-time Endpoint with an AWS CloudFormation Custom Resource

---

## Attribution document for Amazon SageMaker HyperPod task governance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-attributions.html

**Contents:**
- Attribution document for Amazon SageMaker HyperPod task governance
        - Topics
- base-files
- netbase
- golang-lru

In the following you can learn about attributions and third-party licenses for material used in Amazon SageMaker HyperPod task governance.

**Examples:**

Example 1 (unknown):
```unknown
This is the Debian prepackaged version of the Debian Base System
Miscellaneous files. These files were written by Ian Murdock
<imurdock@debian.org> and Bruce Perens <bruce@pixar.com>.

This package was first put together by Bruce Perens <Bruce@Pixar.com>,
from his own sources.

The GNU Public Licenses in /usr/share/common-licenses were taken from
ftp.gnu.org and are copyrighted by the Free Software Foundation, Inc.

The Artistic License in /usr/share/common-licenses is the one coming
from Perl and its SPDX name is "Artistic License 1.0 (Perl)".


Copyright © 1995-2011 Software in the Public In
...
```

Example 2 (unknown):
```unknown
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Comment:
 This package was created by Peter Tobias tobias@et-inf.fho-emden.de on
 Wed, 24 Aug 1994 21:33:28 +0200 and maintained by Anthony Towns
 <ajt@debian.org> until 2001.
 It is currently maintained by Marco d'Itri <md@linux.it>.

Files: *
Copyright:
 Copyright © 1994-1998 Peter Tobias
 Copyright © 1998-2001 Anthony Towns
 Copyright © 2002-2022 Marco d'Itri
License: GPL-2
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License, version 2, as
 publi
...
```

Example 3 (unknown):
```unknown
Copyright © 2014 HashiCorp, Inc.

Mozilla Public License, version 2.0

1. Definitions

1.1. "Contributor"

     means each individual or legal entity that creates, contributes to the
     creation of, or owns Covered Software.

1.2. "Contributor Version"

     means the combination of the Contributions of others (if any) used by a
     Contributor and that particular Contributor's Contribution.

1.3. "Contribution"

     means Covered Software of a particular Contributor.

1.4. "Covered Software"

     means Source Code Form to which the initial Contributor has attached the
     notice in Exhi
...
```

---

## Configure Amazon SageMaker Canvas in a VPC without internet access

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-vpc.html

**Contents:**
- Configure Amazon SageMaker Canvas in a VPC without internet access
- Configure Amazon SageMaker Canvas in a VPC without internet access
  - Step 1: Onboard to Amazon SageMaker AI domain
  - Step 2: Configure VPC endpoints and access
        - Note
        - Note
        - Note
  - Step 3: Grant IAM permissions
  - (Optional) Step 4: Override security group settings for specific users

The Amazon SageMaker Canvas application runs in a container in an AWS managed Amazon Virtual Private Cloud (VPC). If you want to further control access to your resources or run SageMaker Canvas without public internet access, you can configure your Amazon SageMaker AI domain and VPC settings. Within your own VPC, you can configure settings such as security groups (virtual firewalls that control inbound and outbound traffic from Amazon EC2 instances) and subnets (ranges of IP addresses in your VPC). To learn more about VPCs, see How Amazon VPC works.

When the SageMaker Canvas application is running in the AWS managed VPC, it can interact with other AWS services using either an internet connection or through VPC endpoints created in a customer-managed VPC (without public internet access). SageMaker Canvas applications can access these VPC endpoints through a Studio Classic-created network interface that provides connectivity to the customer-managed VPC. The default behavior of the SageMaker Canvas application is to have internet access. When using an internet connection, the containers for the preceding jobs access AWS resources over the internet, such as the Amazon S3 buckets where you store training data and model artifacts.

However, if you have security requirements to control access to your data and job containers, we recommend that you configure SageMaker Canvas and your VPC so that your data and containers aren’t accessible over the internet. SageMaker AI uses the VPC configuration settings you specify when setting up your domain for SageMaker Canvas.

If you want to configure your SageMaker Canvas application without internet access, you must configure your VPC settings when you onboard to Amazon SageMaker AI domain, set up VPC endpoints, and grant the necessary AWS Identity and Access Management permissions. For information about configuring a VPC in Amazon SageMaker AI, see Choose an Amazon VPC. The following sections describe how to run SageMaker Canvas in a VPC without public internet access.

You can send traffic from SageMaker Canvas to other AWS services through your own VPC. If your own VPC doesn't have public internet access and you've set up your domain in VPC only mode, then SageMaker Canvas won't have public internet access as well. This includes all requests, such as accessing datasets in Amazon S3 or training jobs for standard builds, and the requests go through VPC endpoints in your VPC instead of the public internet. When you onboard

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
com.amazonaws.Region.bedrock
```

Example 2 (unknown):
```unknown
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:CreateBucket",
                "s3:GetBucketCors",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::*SageMaker*",
                "arn:aws:s3:::*Sagemaker*",
                "arn:aws:s3:::*sagemaker*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:ListAllMyBu
...
```

Example 3 (unknown):
```unknown
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:CreateBucket",
                "s3:GetBucketCors",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::*SageMaker*",
                "arn:aws:s3:::*Sagemaker*",
                "arn:aws:s3:::*sagemaker*",
                "arn:aws:s3:::*fmeval/datasets*",
                "arn:aws:s3:::*jumpstart-cache-prod*"
            ]
        },
        {
            "E
...
```

Example 4 (unknown):
```unknown
AmazonSageMakerFullAccess
```

---

## Resilience in Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/disaster-recovery-resiliency.html

**Contents:**
- Resilience in Amazon SageMaker AI

The AWS global infrastructure is built around AWS Regions and Availability Zones. AWS Regions provide multiple physically separated and isolated Availability Zones, which are connected with low-latency, high-throughput, and highly redundant networking. With Availability Zones, you can design and operate applications and databases that automatically fail over between Availability Zones without interruption. Availability Zones are more highly available, fault tolerant, and scalable than traditional single or multiple data center infrastructures.

For more information about AWS Regions and Availability Zones, see AWS Global Infrastructure.

In addition to the AWS global infrastructure, Amazon SageMaker AI offers several features to help support your data resiliency and backup needs.

---

## AWS managed policies for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol.html#security-iam-awsmanpol-AmazonSageMakerFullAccess

**Contents:**
- AWS managed policies for Amazon SageMaker AI
        - Important
        - Topics
- AWS managed policy: AmazonSageMakerFullAccess
- AWS managed policy: AmazonSageMakerReadOnly
- SageMaker AI Updates to AWS Managed Policies

To add permissions to users, groups, and roles, it is easier to use AWS managed policies than to write policies yourself. It takes time and expertise to create IAM customer managed policies that provide your team with only the permissions they need. To get started quickly, you can use our AWS managed policies. These policies cover common use cases and are available in your AWS account. For more information about AWS managed policies, see AWS managed policies in the IAM User Guide.

AWS services maintain and update AWS managed policies. You can't change the permissions in AWS managed policies. Services occasionally add additional permissions to an AWS managed policy to support new features. This type of update affects all identities (users, groups, and roles) to which the policy is attached. Services are most likely to update an AWS managed policy when a new feature is launched or when new operations become available. Services do not remove permissions from an AWS managed policy, so policy updates won't break your existing permissions.

Additionally, AWS supports managed policies for job functions that span multiple services. For example, the ReadOnlyAccess AWS managed policy provides read-only access to all AWS services and resources. When a service launches a new feature, AWS adds read-only permissions for new operations and resources. For a list and descriptions of job function policies, see AWS managed policies for job functions in the IAM User Guide.

We recommend that you use the most restricted policy that allows you to perform your use case.

The following AWS managed policies, which you can attach to users in your account, are specific to Amazon SageMaker AI:

AmazonSageMakerFullAccess – Grants full access to Amazon SageMaker AI and SageMaker AI geospatial resources and the supported operations. This does not provide unrestricted Amazon S3 access, but supports buckets and objects with specific sagemaker tags. This policy allows all IAM roles to be passed to Amazon SageMaker AI, but only allows IAM roles with "AmazonSageMaker" in them to be passed to the AWS Glue, AWS Step Functions, and AWS RoboMaker services.

AmazonSageMakerReadOnly – Grants read-only access to Amazon SageMaker AI resources.

The following AWS managed policies can be attached to users in your account but are not recommended:

AdministratorAccess – Grants all actions for all AWS services and for all resources in the account.

DataScientist – Grants a wide range of permissions to c

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ReadOnlyAccess
```

Example 2 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 3 (unknown):
```unknown
AmazonSageMakerReadOnly
```

Example 4 (unknown):
```unknown
AdministratorAccess
```

---

## Amazon SageMaker AI metrics in Amazon CloudWatch

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html

**Contents:**
- Amazon SageMaker AI metrics in Amazon CloudWatch
        - SageMaker AI Metrics and Dimensions
- SageMaker AI endpoint metrics
        - Note
- SageMaker AI endpoint invocation metrics
- SageMaker AI inference component metrics
- SageMaker AI multi-model endpoint metrics
- SageMaker AI job metrics
        - Note
        - Tip

You can monitor Amazon SageMaker AI using Amazon CloudWatch, which collects raw data and processes it into readable, near real-time metrics. These statistics are kept for 15 months. With them, you can access historical information and gain a better perspective on how your web application or service is performing. However, the Amazon CloudWatch console limits the search to metrics that were updated in the last 2 weeks. This limitation ensures that the most current jobs are shown in your namespace.

To graph metrics without using a search, specify its exact name in the source view. You can also set alarms that watch for certain thresholds, and send notifications or take actions when those thresholds are met. For more information, see the Amazon CloudWatch User Guide.

SageMaker AI endpoint metrics

SageMaker AI endpoint invocation metrics

SageMaker AI inference component metrics

SageMaker AI multi-model endpoint metrics

SageMaker AI job metrics

SageMaker Inference Recommender jobs metrics

SageMaker Ground Truth metrics

Amazon SageMaker Feature Store metrics

SageMaker pipelines metrics

The /aws/sagemaker/Endpoints namespace includes the following metrics for endpoint instances.

Metrics are available at a 1-minute frequency.

Amazon CloudWatch supports high-resolution custom metrics and its finest resolution is 1 second. However, the finer the resolution, the shorter the lifespan of the CloudWatch metrics. For the 1-second frequency resolution, the CloudWatch metrics are available for 3 hours. For more information about the resolution and the lifespan of the CloudWatch metrics, see GetMetricStatistics in the Amazon CloudWatch API Reference.

The sum of CPUs reserved by containers on an instance.

This metric is provided only for endpoints that host active inference components.

The value ranges between 0%–100%. In the settings for an inference component, you set the CPU reservation with the NumberOfCpuCoresRequired parameter. For example, if there 4 CPUs, and 2 are reserved, the CPUReservation metric is 50%.

The sum of each individual CPU core's utilization. The CPU utilization of each core range is 0–100. For example, if there are four CPUs, the CPUUtilization range is 0%–400%.

For endpoint variants, the value is the sum of the CPU utilization of the primary and supplementary containers on the instance.

The normalized sum of the utilization of each individual CPU core.

This metric is provided only for endpoints that host active inference componen

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
/aws/sagemaker/Endpoints
```

Example 2 (unknown):
```unknown
CPUReservation
```

Example 3 (unknown):
```unknown
NumberOfCpuCoresRequired
```

Example 4 (unknown):
```unknown
CPUReservation
```

---

## Increase Amazon EC2 Instance Limit

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-increase-instance-limit.html

**Contents:**
- Increase Amazon EC2 Instance Limit
        - Note

You might see the following error message when you're using Data Wrangler: The following instance type is not available: ml.m5.4xlarge. Try selecting a different instance below.

The message can indicate that you need to select a different instance type, but it can also indicate that you don't have enough Amazon EC2 instances to successfully run Data Wrangler on your workflow. You can increase the number of instances by using the following procedure.

To increase the number of instances, do the following.

Open the AWS Management Console.

In the search bar, specify Services Quotas.

Choose Service Quotas.

In the search bar, specify Amazon SageMaker AI.

Choose Amazon SageMaker AI.

Under Service quotas, specify Studio KernelGateway Apps running on ml.m5.4xlarge instance.

ml.m5.4xlarge is the default instance type for Data Wrangler. You can use other instance types and request quota increases for them. For more information, see Instances.

Select Studio KernelGateway Apps running on ml.m5.4xlarge instance.

Choose Request quota increase.

For Change quota value, specify a value greater than Applied quota value.

If your request is approved, AWS sends a notification to the email address associated with your account. You can also check the status of your request by choosing Quota request history on the Service Quotas page. Processed requests have a Status of Closed.

**Examples:**

Example 1 (unknown):
```unknown
The following instance type is not available: ml.m5.4xlarge. Try selecting a different instance below.
```

Example 2 (unknown):
```unknown
Services Quotas
```

Example 3 (unknown):
```unknown
Amazon SageMaker AI
```

Example 4 (unknown):
```unknown
Studio KernelGateway Apps running on ml.m5.4xlarge instance
```

---

## Model performance optimization with SageMaker Neo

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html

**Contents:**
- Model performance optimization with SageMaker Neo
- What is SageMaker Neo?
- How it Works
        - Topics

Neo is a capability of Amazon SageMaker AI that enables machine learning models to train once and run anywhere in the cloud and at the edge.

If you are a first time user of SageMaker Neo, we recommend you check out the Getting Started with Edge Devices section to get step-by-step instructions on how to compile and deploy to an edge device.

Generally, optimizing machine learning models for inference on multiple platforms is difficult because you need to hand-tune models for the specific hardware and software configuration of each platform. If you want to get optimal performance for a given workload, you need to know the hardware architecture, instruction set, memory access patterns, and input data shapes, among other factors. For traditional software development, tools such as compilers and profilers simplify the process. For machine learning, most tools are specific to the framework or to the hardware. This forces you into a manual trial-and-error process that is unreliable and unproductive.

Neo automatically optimizes Gluon, Keras, MXNet, PyTorch, TensorFlow, TensorFlow-Lite, and ONNX models for inference on Android, Linux, and Windows machines based on processors from Ambarella, ARM, Intel, Nvidia, NXP, Qualcomm, Texas Instruments, and Xilinx. Neo is tested with computer vision models available in the model zoos across the frameworks. SageMaker Neo supports compilation and deployment for two main platforms: cloud instances (including Inferentia) and edge devices.

For more information about supported frameworks and cloud instance types you can deploy to, see Supported Instance Types and Frameworks for cloud instances.

For more information about supported frameworks, edge devices, operating systems, chip architectures, and common machine learning models tested by SageMaker AI Neo for edge devices, see Supported Frameworks, Devices, Systems, and Architectures for edge devices.

Neo consists of a compiler and a runtime. First, the Neo compilation API reads models exported from various frameworks. It converts the framework-specific functions and operations into a framework-agnostic intermediate representation. Next, it performs a series of optimizations. Then it generates binary code for the optimized operations, writes them to a shared object library, and saves the model definition and parameters into separate files. Neo also provides a runtime for each target platform that loads and executes the compiled model.

You can create a Neo compilation job fro

*[Content truncated]*

---

## Overview of machine learning with Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html

**Contents:**
- Overview of machine learning with Amazon SageMaker AI

This section describes a typical machine learning (ML) workflow and describes how to accomplish those tasks with Amazon SageMaker AI.

In machine learning, you teach a computer to make predictions or inferences. First, you use an algorithm and example data to train a model. Then, you integrate your model into your application to generate inferences in real time and at scale.

The following diagram shows the typical workflow for creating an ML model. It includes three stages in a circular flow that we cover in more detail proceeding the diagram:

Generate example data

The diagram shows how to perform the following tasks in most typical scenarios:

Generate example data – To train a model, you need example data. The type of data that you need depends on the business problem that you want the model to solve. This relates to the inferences that you want the model to generate. For example, if you want to create a model that predicts a number from an input image of a handwritten digit. To train this model, you need example images of handwritten numbers.

Data scientists often devote time exploring and preprocessing example data before using it for model training. To preprocess data, you typically do the following:

Fetch the data – You might have in-house example data repositories, or you might use datasets that are publicly available. Typically, you pull the dataset or datasets into a single repository.

Clean the data – To improve model training, inspect the data and clean it, as needed. For example, if your data has a country name attribute with values United States and US, you can edit the data to be consistent.

Prepare or transform the data – To improve performance, you might perform additional data transformations. For example, you might choose to combine attributes for a model that predicts the conditions that require de-icing an aircraft. Instead of using temperature and humidity attributes separately, you can combine those attributes into a new attribute to get a better model.

In SageMaker AI, you can preprocess example data using SageMaker APIs with the SageMaker Python SDK in an integrated development environment (IDE). With SDK for Python (Boto3) you can fetch, explore, and prepare your data for model training. For information about data preparation, processing, and transforming your data, see Recommendations for choosing the right data preparation tool in SageMaker AI, Data transformation workloads with SageMaker Processing, and Create, store, an

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
country name
```

Example 2 (unknown):
```unknown
United
                            States
```

---

## Logging Amazon SageMaker AI API calls using AWS CloudTrail

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/logging-using-cloudtrail.html

**Contents:**
- Logging Amazon SageMaker AI API calls using AWS CloudTrail
- Amazon SageMaker AI data events in CloudTrail
        - Note
- Amazon SageMaker AI management events in CloudTrail
- Operations Performed by Automatic Model Tuning
- Amazon SageMaker AI event examples

Amazon SageMaker AI is integrated with AWS CloudTrail, a service that provides a record of actions taken by a user, role, or an AWS service. CloudTrail captures all API calls for Amazon SageMaker AI as events. The calls captured include calls from the Amazon SageMaker AI console and code calls to the Amazon SageMaker AI API operations. Using the information collected by CloudTrail, you can determine the request that was made to Amazon SageMaker AI, the IP address from which the request was made, when it was made, and additional details.

Every event or log entry contains information about who generated the request. The identity information helps you determine the following:

Whether the request was made with root user or user credentials.

Whether the request was made on behalf of an IAM Identity Center user.

Whether the request was made with temporary security credentials for a role or federated user.

Whether the request was made by another AWS service.

CloudTrail is active in your AWS account when you create the account and you automatically have access to the CloudTrail Event history. The CloudTrail Event history provides a viewable, searchable, downloadable, and immutable record of the past 90 days of recorded management events in an AWS Region. For more information, see Working with CloudTrail Event history in the AWS CloudTrail User Guide. There are no CloudTrail charges for viewing the Event history.

For an ongoing record of events in your AWS account past 90 days, create a trail or a CloudTrail Lake event data store.

A trail enables CloudTrail to deliver log files to an Amazon S3 bucket. All trails created using the AWS Management Console are multi-Region. You can create a single-Region or a multi-Region trail by using the AWS CLI. Creating a multi-Region trail is recommended because you capture activity in all AWS Regions in your account. If you create a single-Region trail, you can view only the events logged in the trail's AWS Region. For more information about trails, see Creating a trail for your AWS account and Creating a trail for an organization in the AWS CloudTrail User Guide.

You can deliver one copy of your ongoing management events to your Amazon S3 bucket at no charge from CloudTrail by creating a trail, however, there are Amazon S3 storage charges. For more information about CloudTrail pricing, see AWS CloudTrail Pricing. For information about Amazon S3 pricing, see Amazon S3 Pricing.

CloudTrail Lake lets you run SQL-based que

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
resources.type
```

Example 2 (unknown):
```unknown
AWS::SageMaker::Endpoint
```

Example 3 (unknown):
```unknown
InvokeEndpoint
```

Example 4 (unknown):
```unknown
InvokeEndpointAsync
```

---

## Transform Data

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-transform.html

**Contents:**
- Transform Data
- Transform UI
- Join Datasets
- Concatenate Datasets
        - Concatenate two datasets:
- Balance Data
        - Note
- Custom Transforms
        - Important
- Custom Formula

Amazon SageMaker Data Wrangler provides numerous ML data transforms to streamline cleaning, transforming, and featurizing your data. When you add a transform, it adds a step to the data flow. Each transform you add modifies your dataset and produces a new dataframe. All subsequent transforms apply to the resulting dataframe.

Data Wrangler includes built-in transforms, which you can use to transform columns without any code. You can also add custom transformations using PySpark, Python (User-Defined Function), pandas, and PySpark SQL. Some transforms operate in place, while others create a new output column in your dataset.

You can apply transforms to multiple columns at once. For example, you can delete multiple columns in a single step.

You can apply the Process numeric and Handle missing transforms only to a single column.

Use this page to learn more about these built-in and custom transforms.

Most of the built-in transforms are located in the Prepare tab of the Data Wrangler UI. You can access the join and concatenate transforms through the data flow view. Use the following table to preview these two views.

You can add a transform to any step in your data flow. Use the following procedure to add a transform to your data flow.

To add a step to your data flow, do the following.

Choose the + next to the step in the data flow.

Choose Add transform.

(Optional) You can search for the transform that you want to use. Data Wrangler highlights the query in the results.

To join two datasets, select the first dataset in your data flow and choose Join. When you choose Join, you see results similar to those shown in the following image. Your left and right datasets are displayed in the left panel. The main panel displays your data flow, with the newly joined dataset added.

When you choose Configure to configure your join, you see results similar to those shown in the following image. Your join configuration is displayed in the left panel. You can use this panel to choose the joined dataset name, join type, and columns to join. The main panel displays three tables. The top two tables display the left and right datasets on the left and right respectively. Under this table, you can preview the joined dataset.

See Join Datasets to learn more.

To concatenate two datasets, you select the first dataset in your data flow and choose Concatenate. When you select Concatenate, you see results similar to those shown in the following image. Your left and right datase

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
A
                    column
```

Example 2 (unknown):
```unknown
df.rename(columns={"A column": "A_column", "B column": "B_column"})
```

Example 3 (python):
```python
from pyspark.sql.functions import from_unixtime, to_date, date_format
df = df.withColumn('DATE_TIME', from_unixtime('TIMESTAMP'))
df = df.withColumn( 'EVENT_DATE', to_date('DATE_TIME')).withColumn(
'EVENT_TIME', date_format('DATE_TIME', 'HH:mm:ss'))
```

Example 4 (unknown):
```unknown
SELECT name, fare, pclass, survived FROM df
```

---

## UpdateUserProfile

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_UpdateUserProfile.html

**Contents:**
- UpdateUserProfile
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

Updates a user profile.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: d-(-*[a-z0-9]){1,61}

The user profile name.

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

A collection of settings.

Type: UserSettings object

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

The user profile Amazon Resource Name (ARN).

Length Constraints: Minimum length of 0. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:user-profile/.*

For information about the errors that are common to all actions, see Common Errors.

Resource being accessed is in use.

HTTP Status Code: 400

You have exceeded an SageMaker resource limit. For example, you might have too many training jobs created.

HTTP Status Code: 400

Resource being access is not found.

HTTP Status Code: 400

For more information about using this API in one of the language-specific AWS SDKs, see the following:

AWS Command Line Interface V2

AWS SDK for JavaScript V3

**Examples:**

Example 1 (unknown):
```unknown
{
   "DomainId": "string",
   "UserProfileName": "string",
   "UserSettings": {
      "AutoMountHomeEFS": "string",
      "CanvasAppSettings": {
         "DirectDeploySettings": {
            "Status": "string"
         },
         "EmrServerlessSettings": {
            "ExecutionRoleArn": "string",
            "Status": "string"
         },
         "GenerativeAiSettings": {
            "AmazonBedrockRoleArn": "string"
         },
         "IdentityProviderOAuthSettings": [
            {
               "DataSourceName": "string",
               "SecretArn": "string",
               "Status": 
...
```

Example 2 (unknown):
```unknown
d-(-*[a-z0-9]){1,61}
```

Example 3 (unknown):
```unknown
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

Example 4 (unknown):
```unknown
{
   "UserProfileArn": "string"
}
```

---

## Recommendations for a first-time user of Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/first-time-user.html

**Contents:**
- Recommendations for a first-time user of Amazon SageMaker AI

If you're a first-time user of SageMaker AI, we recommend that you complete the following:

Overview of machine learning with Amazon SageMaker AI – Get an overview of the machine learning (ML) lifecycle and learn about solutions that are offered. This page explains key concepts and describes the core components involved in building AI solutions with SageMaker AI.

Guide to getting set up with Amazon SageMaker AI – Learn how to set up and use SageMaker AI based on your needs.

Automated ML, no-code, or low-code – Learn about low-code and no-code ML options that simplify a ML workflow by automating machine learning tasks. These options are helpful ML learning tools because they provide visibility into the code by generating notebooks for each of the automated ML tasks.

Machine learning environments offered by Amazon SageMaker AI – Familiarize yourself with the ML environments that you can use to develop your ML workflow, such as information and examples about ready-to-use and custom models.

Explore other topics – Use the SageMaker AI Developer Guide's table of contents to explore more topics. For example, you can find information about ML lifecycle stages, in Overview of machine learning with Amazon SageMaker AI, and various solutions that SageMaker AI offers.

Amazon SageMaker AI resources – Refer to the various developer resources that SageMaker AI offers.

---

## Pipelines actions

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-build.html

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

## UpdateDomain

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_UpdateDomain.html

**Contents:**
- UpdateDomain
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

Updates the default settings for new user profiles in the domain.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Specifies the VPC used for non-EFS traffic.

PublicInternetOnly - Non-EFS traffic is through a VPC managed by Amazon SageMaker AI, which allows direct internet access.

VpcOnly - All Studio traffic is through the specified VPC and subnets.

This configuration can only be modified if there are no apps in the InService, Pending, or Deleting state. The configuration cannot be updated if DomainSettings.RStudioServerProDomainSettings.DomainExecutionRoleArn is already set or DomainSettings.RStudioServerProDomainSettings.DomainExecutionRoleArn is provided as part of the same request.

Valid Values: PublicInternetOnly | VpcOnly

The entity that creates and manages the required security groups for inter-app communication in VPCOnly mode. Required when CreateDomain.AppNetworkAccessType is VPCOnly and DomainSettings.RStudioServerProDomainSettings.DomainExecutionRoleArn is provided. If setting up the domain for use with RStudio, this value must be set to Service.

Valid Values: Service | Customer

The default settings for shared spaces that users create in the domain.

Type: DefaultSpaceSettings object

A collection of settings.

Type: UserSettings object

The ID of the domain to be updated.

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: d-(-*[a-z0-9]){1,61}

A collection of DomainSettings configuration values to update.

Type: DomainSettingsForUpdate object

The VPC subnets that Studio uses for communication.

If removing subnets, ensure there are no apps in the InService, Pending, or Deleting state.

Type: Array of strings

Array Members: Minimum number of 1 item. Maximum number of 16 items.

Length Constraints: Minimum length of 0. Maximum length of 32.

Pattern: [-0-9a-zA-Z]+

Indicates whether custom tag propagation is supported for the domain. Defaults to DISABLED.

Valid Values: ENABLED | DISABLED

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

The Amazon Resource Name (ARN) of the domain.

Length Constraints: Minimum length of 0. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:domain/.*

For information about the errors that are common to all actions, see Common Errors.

Resource being accessed is in

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
   "AppNetworkAccessType": "string",
   "AppSecurityGroupManagement": "string",
   "DefaultSpaceSettings": {
      "CustomFileSystemConfigs": [
         { ... }
      ],
      "CustomPosixUserConfig": {
         "Gid": number,
         "Uid": number
      },
      "ExecutionRole": "string",
      "JupyterLabAppSettings": {
         "AppLifecycleManagement": {
            "IdleSettings": {
               "IdleTimeoutInMinutes": number,
               "LifecycleManagement": "string",
               "MaxIdleTimeoutInMinutes": number,
               "MinIdleTimeoutInMinutes": number
            
...
```

Example 2 (unknown):
```unknown
PublicInternetOnly
```

Example 3 (unknown):
```unknown
DomainSettings.RStudioServerProDomainSettings.DomainExecutionRoleArn
```

Example 4 (unknown):
```unknown
DomainSettings.RStudioServerProDomainSettings.DomainExecutionRoleArn
```

---

## MLOps Project Templates

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-templates.html

**Contents:**
- MLOps Project Templates
        - Topics

An Amazon SageMaker AI project template automates the setup and implementation of MLOps for your projects. A SageMaker AI project template is an Service Catalog product that SageMaker AI makes available to Amazon SageMaker Studio (or Studio Classic) users. These Service Catalog products are visible in your Service Catalog console after you enable permissions when you onboard or update Amazon SageMaker Studio (or Studio Classic). For information about enabling permissions to use SageMaker AI project templates, see Granting SageMaker Studio Permissions Required to Use Projects. Use SageMaker AI project templates to create a project that is an end-to-end MLOps solution.

You can use a SageMaker Projects template to implement image-building CI/CD. With this template, you can automate the CI/CD of images that are built and pushed to Amazon ECR. Changes in the container files in your project’s source control repositories initiate the ML pipeline and deploy the latest version for your container. For more information, see the blog Create Amazon SageMaker Projects with image building CI/CD pipelines.

If you are an administrator, you can create custom project templates from scratch or modify one of the project templates provided by SageMaker AI. Studio (or Studio Classic) users in your organization can use these custom project templates to create their projects.

Use SageMaker AI-Provided Project Templates

Create Custom Project Templates

---

## SageMaker Clarify explainability with SageMaker AI Autopilot

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-explainability.html

**Contents:**
- SageMaker Clarify explainability with SageMaker AI Autopilot

Autopilot uses tools provided by Amazon SageMaker Clarify to help provide insights into how machine learning (ML) models make predictions. These tools can help ML engineers, product managers, and other internal stakeholders understand model characteristics. To trust and interpret decisions made on model predictions, both consumers and regulators rely on transparency in machine learning in order.

The Autopilot explanatory functionality uses a model-agnostic feature attribution approach. This approach determines the contribution of individual features or inputs to the model's output, providing insights into the relevance of different features. You can use it to understand why a model made a prediction after training, or use it to provide per-instance explanation during inference. The implementation includes a scalable implementation of SHAP (Shapley Additive Explanations). This implementation is based on the concept of a Shapley value from cooperative game theory, which assigns each feature an importance value for a particular prediction.

You can use SHAP explanations for the following: auditing and meeting regulatory requirements, building trust in the model, supporting human decision-making, or debugging and improving model performance.

For additional information on Shapley values and baselines, see SHAP Baselines for Explainability.

For a guide to the Amazon SageMaker Clarify documentation, see Guide to the SageMaker Clarify Documentation.

---

## Pipelines steps

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html

**Contents:**
- Pipelines steps
        - Topics
- Step properties
- Step parallelism
- Data dependency between steps
- Custom dependency between steps
- Custom images in a step

Pipelines are composed of steps. These steps define the actions that the pipeline takes and the relationships between steps using properties. The following page describes the types of steps, their properties, and the relationships between them.

Data dependency between steps

Custom dependency between steps

Custom images in a step

Use the properties attribute to add data dependencies between steps in the pipeline. Pipelines use these data dependencies to construct the DAG from the pipeline definition. These properties can be referenced as placeholder values and are resolved at runtime.

The properties attribute of a Pipelines step matches the object returned by a Describe call for the corresponding SageMaker AI job type. For each job type, the Describe call returns the following response object:

ProcessingStep – DescribeProcessingJob

TrainingStep – DescribeTrainingJob

TransformStep – DescribeTransformJob

To check which properties are referrable for each step type during data dependency creation, see Data Dependency - Property Reference in the Amazon SageMaker Python SDK.

When a step does not depend on any other step, it runs immediately upon pipeline execution. However, executing too many pipeline steps in parallel can quickly exhaust available resources. Control the number of concurrent steps for a pipeline execution with ParallelismConfiguration.

The following example uses ParallelismConfiguration to set the concurrent step limit to five.

You define the structure of your DAG by specifying the data relationships between steps. To create data dependencies between steps, pass the properties of one step as the input to another step in the pipeline. The step receiving the input isn't started until after the step providing the input finishes running.

A data dependency uses JsonPath notation in the following format. This format traverses the JSON property file. This means you can append as many <property> instances as needed to reach the desired nested property in the file. For more information on JsonPath notation, see the JsonPath repo.

The following shows how to specify an Amazon S3 bucket using the ProcessingOutputConfig property of a processing step.

To create the data dependency, pass the bucket to a training step as follows.

To check which properties are referrable for each step type during data dependency creation, see Data Dependency - Property Reference in the Amazon SageMaker Python SDK.

When you specify a data dependency, Pipelines pro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ProcessingStep
```

Example 2 (unknown):
```unknown
TrainingStep
```

Example 3 (unknown):
```unknown
TransformStep
```

Example 4 (unknown):
```unknown
ParallelismConfiguration
```

---

## Pipelines

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html

**Contents:**
- Pipelines
        - Topics

Amazon SageMaker Pipelines is a purpose-built workflow orchestration service to automate machine learning (ML) development.

Pipelines provide the following advantages over other AWS workflow offerings:

Auto-scaling serverless infrastructure You don't need to manage the underlying orchestration infrastructure to run Pipelines, which allows you to focus on core ML tasks. SageMaker AI automatically provisions, scales, and shuts down the pipeline orchestration compute resources as your ML workload demands.

Intuitive user experience Pipelines can be created and managed through your interface of choice: visual editor, SDK, APIs, or JSON. You can drag-and-drop the various ML steps to author your pipelines in the Amazon SageMaker Studio visual interface. The following screenshot shows the Studio visual editor for pipelines.

If you prefer managing your ML workflows programmatically, the SageMaker Python SDK offers advanced orchestration features. For more information, see Amazon SageMaker Pipelines in the SageMaker Python SDK documentation.

AWS integrations Pipelines provide seamless integration with all SageMaker AI features and other AWS services to automate data processing, model training, fine-tuning, evaluation, deployment, and monitoring jobs. You can incorporate the SageMaker AI features in your Pipelines and navigate across them using deep links to create, monitor, and debug your ML workflows at scale.

Reduced costs With Pipelines, you only pay for the SageMaker Studio environment and the underlying jobs that are orchestrated by Pipelines (for example, SageMaker Training, SageMaker Processing, SageMaker AI Inference, and Amazon S3 data storage).

Auditability and lineage tracking With Pipelines, you can track the history of pipeline updates and executions using built-in versioning. Amazon SageMaker ML Lineage Tracking helps you analyze the data sources and data consumers in the end-to-end ML development lifecycle.

---

## AWS Managed Policies for SageMaker Pipelines

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-pipelines.html

**Contents:**
- AWS Managed Policies for SageMaker Pipelines
        - Topics
- AWS managed policy: AmazonSageMakerPipelinesIntegrations
- Amazon SageMaker AI updates to SageMaker AI Pipelines managed policies

These AWS managed policies add permissions required to use SageMaker Pipelines. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerPipelinesIntegrations

Amazon SageMaker AI updates to SageMaker AI Pipelines managed policies

This AWS managed policy grants permissions commonly needed to use Callback steps and Lambda steps in SageMaker Pipelines. The policy is added to the AmazonSageMaker-ExecutionRole that is created when you onboard to Amazon SageMaker Studio Classic. The policy can be attached to any role used for authoring or executing a pipeline.

This policy grants appropriate AWS Lambda, Amazon Simple Queue Service (Amazon SQS), Amazon EventBridge, and IAM permissions needed when building pipelines that invoke Lambda functions or include callback steps, which can be used for manual approval steps or running custom workloads.

The Amazon SQS permissions allow you to create the Amazon SQS queue needed for receiving callback messages, and also to send messages to that queue.

The Lambda permissions allow you to create, read, update, and delete the Lambda functions used in the pipeline steps, and also to invoke those Lambda functions.

This policy grants the Amazon EMR permissions needed to run a pipelines Amazon EMR step.

This policy includes the following permissions.

elasticmapreduce – Read, add, and cancel steps in a running Amazon EMR cluster. Read, create, and terminate a new Amazon EMR cluster.

events – Read, create, update, and add targets to an EventBridge rule named SageMakerPipelineExecutionEMRStepStatusUpdateRule and SageMakerPipelineExecutionEMRClusterStatusUpdateRule.

iam – Pass an IAM role to the AWS Lambda service, Amazon EMR and Amazon EC2.

lambda – Create, read, update, delete, and invoke Lambda functions. These permissions are limited to functions whose name includes "sagemaker".

sqs – Create an Amazon SQS queue; send an Amazon SQS message. These permissions are limited to queues whose name includes "sagemaker".

View details about updates to AWS managed policies for Amazon SageMaker AI since this service began tracking these changes.

AmazonSageMakerPipelinesIntegrations - Update to an existing policy

Added permissions for elasticmapreduce:RunJobFlows, elasticmapreduce:TerminateJobFlows, elasticmapreduce:ListSteps, and elasticmapreduce:DescribeCluster.

AmazonSageMakerPipelinesIntegrations - Update to an existing policy

Added

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMaker-ExecutionRole
```

Example 2 (unknown):
```unknown
elasticmapreduce
```

Example 3 (unknown):
```unknown
SageMakerPipelineExecutionEMRStepStatusUpdateRule
```

Example 4 (unknown):
```unknown
SageMakerPipelineExecutionEMRClusterStatusUpdateRule
```

---

## CreateProcessingJob

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateProcessingJob.html

**Contents:**
- CreateProcessingJob
- Request Syntax
- Request Parameters
        - Important
        - Important
- Response Syntax
- Response Elements
- Errors
- See Also

Creates a processing job.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Configures the processing job to run a specified Docker container image.

Type: AppSpecification object

The environment variables to set in the Docker container. Up to 100 key and values entries in the map are supported.

Do not include any security-sensitive information including account access IDs, secrets, or tokens in any environment fields. As part of the shared responsibility model, you are responsible for any potential exposure, unauthorized access, or compromise of your sensitive data if caused by security-sensitive information included in the request environment variable or plain text fields.

Type: String to string map

Map Entries: Minimum number of 0 items. Maximum number of 100 items.

Key Length Constraints: Minimum length of 0. Maximum length of 256.

Key Pattern: [a-zA-Z_][a-zA-Z0-9_]*

Value Length Constraints: Minimum length of 0. Maximum length of 256.

Value Pattern: [\S\s]*

Associates a SageMaker job as a trial component with an experiment and trial. Specified when you call the following APIs:

Type: ExperimentConfig object

Networking options for a processing job, such as whether to allow inbound and outbound network calls to and from processing containers, and the VPC subnets and security groups to use for VPC-enabled processing jobs.

Type: NetworkConfig object

An array of inputs configuring the data to download into the processing container.

Type: Array of ProcessingInput objects

Array Members: Minimum number of 0 items. Maximum number of 10 items.

The name of the processing job. The name must be unique within an AWS Region in the AWS account.

Length Constraints: Minimum length of 1. Maximum length of 63.

Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

Output configuration for the processing job.

Type: ProcessingOutputConfig object

Identifies the resources, ML compute instances, and ML storage volumes to deploy for a processing job. In distributed training, you specify more than one instance.

Type: ProcessingResources object

The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.

Length Constraints: Minimum length of 20. Maximum length of 2048.

Pattern: arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+

The time limit for how long the processing job is allowed to run.

Type: ProcessingSto

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
   "AppSpecification": {
      "ContainerArguments": [ "string" ],
      "ContainerEntrypoint": [ "string" ],
      "ImageUri": "string"
   },
   "Environment": {
      "string" : "string"
   },
   "ExperimentConfig": {
      "ExperimentName": "string",
      "RunName": "string",
      "TrialComponentDisplayName": "string",
      "TrialName": "string"
   },
   "NetworkConfig": {
      "EnableInterContainerTrafficEncryption": boolean,
      "EnableNetworkIsolation": boolean,
      "VpcConfig": {
         "SecurityGroupIds": [ "string" ],
         "Subnets": [ "string" ]
      }
   },
   "Proc
...
```

Example 2 (unknown):
```unknown
[a-zA-Z_][a-zA-Z0-9_]*
```

Example 3 (unknown):
```unknown
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

Example 4 (unknown):
```unknown
arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+
```

---

## AWS managed policies for Amazon SageMaker Canvas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-canvas.html

**Contents:**
- AWS managed policies for Amazon SageMaker Canvas
        - Topics
- AWS managed policy: AmazonSageMakerCanvasFullAccess
- AWS managed policy: AmazonSageMakerCanvasDataPrepFullAccess
- AWS managed policy: AmazonSageMakerCanvasDirectDeployAccess
- AWS managed policy: AmazonSageMakerCanvasAIServicesAccess
- AWS managed policy: AmazonSageMakerCanvasBedrockAccess
- AWS managed policy: AmazonSageMakerCanvasForecastAccess
- AWS managed policy: AmazonSageMakerCanvasEMRServerlessExecutionRolePolicy
- AWS managed policy: AmazonSageMakerCanvasSMDataScienceAssistantAccess

These AWS managed policies add permissions required to use Amazon SageMaker Canvas. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerCanvasFullAccess

AWS managed policy: AmazonSageMakerCanvasDataPrepFullAccess

AWS managed policy: AmazonSageMakerCanvasDirectDeployAccess

AWS managed policy: AmazonSageMakerCanvasAIServicesAccess

AWS managed policy: AmazonSageMakerCanvasBedrockAccess

AWS managed policy: AmazonSageMakerCanvasForecastAccess

AWS managed policy: AmazonSageMakerCanvasEMRServerlessExecutionRolePolicy

AWS managed policy: AmazonSageMakerCanvasSMDataScienceAssistantAccess

Amazon SageMaker AI updates to Amazon SageMaker Canvas managed policies

This policy grants permissions that allow full access to Amazon SageMaker Canvas through the AWS Management Console and SDK. The policy also provides select access to related services [for example, Amazon Simple Storage Service (Amazon S3), AWS Identity and Access Management (IAM), Amazon Virtual Private Cloud (Amazon VPC), Amazon Elastic Container Registry (Amazon ECR), Amazon CloudWatch Logs, Amazon Redshift, AWS Secrets Manager, Amazon SageMaker Autopilot, SageMaker Model Registry, and Amazon Forecast].

This policy is intended to help customers experiment and get started with all the capabilities of SageMaker Canvas. For more fine-grained control, we suggest customers build their own scoped down versions as they move to production workloads. For more information, see IAM policy types: How and when to use them.

This AWS managed policy includes the following permissions.

sagemaker – Allows principals to create and host SageMaker AI models on resources whose ARN contains "Canvas", "canvas", or "model-compilation-". Additionally, users can register their SageMaker Canvas model to SageMaker AI Model Registry in the same AWS account. Also allows principals to create and manage SageMaker training, transform, and AutoML jobs.

application-autoscaling – Allows principals to automatically scale a SageMaker AI inference endpoint.

athena – Allows principals to query a list of data catalogs, databases, and table metadata from Amazon Athena, and access the tables in the catalogs.

cloudwatch – Allows principals to create and manage Amazon CloudWatch alarms.

ec2 – Allows principals to create Amazon VPC endpoints.

ecr – Allows principals to get information about a container image.

emr-serverless – Allows pri

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application-autoscaling
```

Example 2 (unknown):
```unknown
emr-serverless
```

Example 3 (unknown):
```unknown
Source:SageMakerCanvas
```

Example 4 (unknown):
```unknown
redshift-data
```

---

## Using Amazon Augmented AI for Human Review

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html

**Contents:**
- Using Amazon Augmented AI for Human Review
        - What is Amazon Augmented AI?
        - Amazon A2I Use Case Examples
        - Topics

When you use AI applications such as Amazon Rekognition, Amazon Textract, or your custom machine learning (ML) models, you can use Amazon Augmented AI to get human review of low-confidence predictions or random prediction samples.

Amazon Augmented AI (Amazon A2I) is a service that brings human review of ML predictions to all developers by removing the heavy lifting associated with building human review systems or managing large numbers of human reviewers.

Many ML applications require humans to review low-confidence predictions to ensure the results are correct. For example, extracting information from scanned mortgage application forms can require human review due to low-quality scans or poor handwriting. Building human review systems can be time-consuming and expensive because it involves implementing complex processes or workflows, writing custom software to manage review tasks and results, and managing large groups of reviewers.

Amazon A2I streamlines building and managing human reviews for ML applications. Amazon A2I provides built-in human review workflows for common ML use cases, such as content moderation and text extraction from documents. You can also create your own workflows for ML models built on SageMaker AI or any other tools. Using Amazon A2I, you can allow human reviewers to step in when a model is unable to make a high-confidence prediction or to audit its predictions on an ongoing basis.

The following examples demonstrate how you can use Amazon A2I to integrate a human review loop into your ML application. For each of these examples, you can find a Jupyter Notebook that demonstrates that workflow in Use Cases and Examples Using Amazon A2I.

Use Amazon A2I with Amazon Textract – Have humans review important key-value pairs in single-page documents or have Amazon Textract randomly sample and send documents from your dataset to humans for review.

Use Amazon A2I with Amazon Rekognition – Have humans review unsafe images for explicit adult or violent content if Amazon Rekognition returns a low-confidence score, or have Amazon Rekognition randomly sample and send images from your dataset to humans for review.

Use Amazon A2I to review real-time ML inferences – Use Amazon A2I to review real-time, low-confidence inferences made by a model deployed to a SageMaker AI hosted endpoint and incrementally train your model using Amazon A2I output data.

Use Amazon A2I with Amazon Comprehend – Have humans review Amazon Comprehend inferences about tex

*[Content truncated]*

---

## DescribeFeatureGroup

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_DescribeFeatureGroup.html

**Contents:**
- DescribeFeatureGroup
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

Use this operation to describe a FeatureGroup. The response includes information on the creation time, FeatureGroup name, the unique identifier for each FeatureGroup, and more.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

The name or Amazon Resource Name (ARN) of the FeatureGroup you want described.

Length Constraints: Minimum length of 1. Maximum length of 256.

Pattern: (arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:feature-group\/)?([a-zA-Z0-9]([_-]*[a-zA-Z0-9]){0,63})

A token to resume pagination of the list of Features (FeatureDefinitions). 2,500 Features are returned by default.

Length Constraints: Minimum length of 0. Maximum length of 8192.

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

A timestamp indicating when SageMaker created the FeatureGroup.

A free form description of the feature group.

Length Constraints: Minimum length of 0. Maximum length of 128.

The name of the feature that stores the EventTime of a Record in a FeatureGroup.

An EventTime is a point in time when a new event occurs that corresponds to the creation or update of a Record in a FeatureGroup. All Records in the FeatureGroup have a corresponding EventTime.

Length Constraints: Minimum length of 1. Maximum length of 64.

Pattern: [a-zA-Z0-9]([-_]*[a-zA-Z0-9]){0,63}

The reason that the FeatureGroup failed to be replicated in the OfflineStore. This is failure can occur because:

The FeatureGroup could not be created in the OfflineStore.

The FeatureGroup could not be deleted from the OfflineStore.

Length Constraints: Minimum length of 0. Maximum length of 1024.

A list of the Features in the FeatureGroup. Each feature is defined by a FeatureName and FeatureType.

Type: Array of FeatureDefinition objects

Array Members: Minimum number of 1 item. Maximum number of 2500 items.

The Amazon Resource Name (ARN) of the FeatureGroup.

Length Constraints: Minimum length of 0. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:feature-group/.*

he name of the FeatureGroup.

Length Constraints: Minimum length of 1. Maximum length of 64.

Pattern: [a-zA-Z0-9]([_-]*[a-zA-Z0-9]){0,63}

The status of the feature group.

Valid Values: Creating | Created | CreateFailed | Deleting | DeleteFailed

A timestamp indicating when the feature group was last updated.

A va

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
FeatureGroup
```

Example 2 (unknown):
```unknown
FeatureGroup
```

Example 3 (unknown):
```unknown
FeatureGroup
```

Example 4 (unknown):
```unknown
{
   "FeatureGroupName": "string",
   "NextToken": "string"
}
```

---

## Collaboration with shared spaces

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/domain-space.html

**Contents:**
- Collaboration with shared spaces
        - Note

An Amazon SageMaker Studio Classic shared space consists of a shared JupyterServer application and a shared directory. A JupyterLab shared space consists of a shared JupyterLab application and a shared directory within Amazon SageMaker Studio. All user profiles in a domain have access to all shared spaces in the domain. Amazon SageMaker AI automatically scopes resources in a shared space within the context of the Amazon SageMaker Studio Classic application that you launch in that shared space. Resources in a shared space include notebooks, files, experiments, and models. Use shared spaces to collaborate with other users in real-time using features like automatic tagging, real time co-editing of notebooks, and customization.

Shared spaces are available in:

Amazon SageMaker Studio Classic

A Studio Classic shared space only supports Studio Classic and KernelGateway applications. A shared space only supports the use of a JupyterLab 3 image Amazon Resource Name (ARN). For more information, see JupyterLab Versioning in Amazon SageMaker Studio Classic.

Amazon SageMaker AI automatically tags all SageMaker AI resources that you create within the scope of a shared space. You can use these tags to monitor costs and plan budgets using tools, such as AWS Budgets.

A shared space uses the same VPC settings as the domain that it's created in.

Shared spaces do not support the use of Amazon SageMaker Data Wrangler or Amazon EMR cross-account clusters.

All resources created in a shared space are automatically tagged with a domain ARN tag and shared space ARN tag. The domain ARN tag is based on the domain ID, while the shared space ARN tag is based on the shared space name.

You can use these tags to monitor AWS CloudTrail usage. For more information, see Log Amazon SageMaker API Calls with AWS CloudTrail.

You can also use these tags to monitor costs with AWS Billing and Cost Management. For more information, see Using AWS cost allocation tags.

Real time co-editing of notebooks

A key benefit of a shared space is that it facilitates collaboration between members of the shared space in real time. Users collaborating in a workspace get access to a shared Studio Classic application where they can access, read, and edit their notebooks in real time. Real time collaboration is only supported for JupyterServer applications within a shared space.

Users with access to a shared space can simultaneously open, view, edit, and execute Jupyter notebooks in the shared Studio Clas

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
conda activate studio
pip install jupyter-server==2.0.0rc3
```

---

## Principal Component Analysis (PCA) Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/pca.html

**Contents:**
- Principal Component Analysis (PCA) Algorithm
        - Topics
- Input/Output Interface for the PCA Algorithm
- EC2 Instance Recommendation for the PCA Algorithm
- PCA Sample Notebooks

PCA is an unsupervised machine learning algorithm that attempts to reduce the dimensionality (number of features) within a dataset while still retaining as much information as possible. This is done by finding a new set of features called components, which are composites of the original features that are uncorrelated with one another. They are also constrained so that the first component accounts for the largest possible variability in the data, the second component the second most variability, and so on.

In Amazon SageMaker AI, PCA operates in two modes, depending on the scenario:

regular: For datasets with sparse data and a moderate number of observations and features.

randomized: For datasets with both a large number of observations and features. This mode uses an approximation algorithm.

PCA uses tabular data.

The rows represent observations you want to embed in a lower dimensional space. The columns represent features that you want to find a reduced approximation for. The algorithm calculates the covariance matrix (or an approximation thereof in a distributed manner), and then performs the singular value decomposition on this summary to produce the principal components.

Input/Output Interface for the PCA Algorithm

EC2 Instance Recommendation for the PCA Algorithm

For training, PCA expects data provided in the train channel, and optionally supports a dataset passed to the test dataset, which is scored by the final algorithm. Both recordIO-wrapped-protobuf and CSV formats are supported for training. You can use either File mode or Pipe mode to train models on data that is formatted as recordIO-wrapped-protobuf or as CSV.

For inference, PCA supports text/csv, application/json, and application/x-recordio-protobuf. Results are returned in either application/json or application/x-recordio-protobuf format with a vector of "projections."

For more information on input and output file formats, see PCA Response Formats for inference and the PCA Sample Notebooks.

PCA supports CPU and GPU instances for training and inference. Which instance type is most performant depends heavily on the specifics of the input data. For GPU instances, PCA supports P2, P3, G4dn, and G5.

For a sample notebook that shows how to use the SageMaker AI Principal Component Analysis algorithm to analyze the images of handwritten digits from zero to nine in the MNIST dataset, see An Introduction to PCA with MNIST. For instructions how to create and access Jupyter notebook instanc

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 2 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 3 (unknown):
```unknown
application/json
```

Example 4 (unknown):
```unknown
application/x-recordio-protobuf
```

---

## Amazon SageMaker Canvas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html

**Contents:**
- Amazon SageMaker Canvas
        - Topics
- Are you a first-time SageMaker Canvas user?

Amazon SageMaker Canvas gives you the ability to use machine learning to generate predictions without needing to write any code. The following are some use cases where you can use SageMaker Canvas:

Predict customer churn

Plan inventory efficiently

Optimize price and revenue

Improve on-time deliveries

Classify text or images based on custom categories

Identify objects and text in images

Extract information from documents

With Canvas, you can chat with popular large language models (LLMs), access Ready-to-use models, or build a custom model trained on your data.

Canvas chat is a functionality that leverages open-source and Amazon LLMs to help you boost your productivity. You can prompt the models to get assistance with tasks such as generating content, summarizing or categorizing documents, and answering questions. To learn more, see Generative AI foundation models in SageMaker Canvas.

The Ready-to-use models in Canvas can extract insights from your data for a variety of use cases. You don’t have to build a model to use Ready-to-use models because they are powered by Amazon AI services, including Amazon Rekognition, Amazon Textract, and Amazon Comprehend. You only have to import your data and start using a solution to generate predictions.

If you want a model that is customized to your use case and trained with your data, you can build a model. You can get predictions customized to your data by doing the following:

Import your data from one or more data sources.

Build a predictive model.

Evaluate the model's performance.

Generate predictions with the model.

Canvas supports the following types of custom models:

Numeric prediction (also known as regression)

Categorical prediction for 2 and 3+ categories (also known as binary and multi-class classification)

Time series forecasting

Single-label image prediction (also known as image classification)

Multi-category text prediction (also known as multi-class text classification)

To learn more about pricing, see the SageMaker Canvas pricing page. You can also see Billing and cost in SageMaker Canvas for more information.

SageMaker Canvas is currently available in the following Regions:

US East (N. Virginia)

US West (N. California)

Asia Pacific (Mumbai)

Asia Pacific (Singapore)

Asia Pacific (Sydney)

South America (São Paulo)

Are you a first-time SageMaker Canvas user?

Getting started with using Amazon SageMaker Canvas

Tutorial: Build an end-to-end machine learning workflow in SageMaker 

*[Content truncated]*

---

## Supported Regions and Quotas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/appendix.html

**Contents:**
- Supported Regions and Quotas
- Quotas

This page gives information about the AWS Regions supported by Amazon SageMaker AI and the Amazon Elastic Compute Cloud (Amazon EC2) instance types, as well as quotas for Amazon SageMaker AI resources.

For information about the instance types that are available in each Region, see Amazon SageMaker Pricing.

For a list of the SageMaker AI service endpoints for each Region, see Amazon SageMaker AI endpoints and quotas in the AWS General Reference.

For a list of SageMaker AI quotas, see Amazon SageMaker AI endpoints and quotas in the AWS General Reference.

The Service Quotas console provides information about your service quotas. You can use the Service Quotas console to view your default service quotas or to request quota increases. To request a quota increase for adjustable quotas, see Requesting a quota increase.

You can set up a quota request template for your AWS Organization that automatically requests quota increases during account creation. For more information, see Using Service Quotas request templates.

---

## AWS Managed Policies for Amazon SageMaker Ground Truth

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-ground-truth.html

**Contents:**
- AWS Managed Policies for Amazon SageMaker Ground Truth
        - Topics
- AWS managed policy: AmazonSageMakerGroundTruthExecution
- Amazon SageMaker AI updates to SageMaker AI Ground Truth managed policies

These AWS managed policies add permissions required to use SageMaker AI Ground Truth. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console.

AWS managed policy: AmazonSageMakerGroundTruthExecution

Amazon SageMaker AI updates to SageMaker AI Ground Truth managed policies

This AWS managed policy grants permissions commonly needed to use SageMaker AI Ground Truth.

This policy includes the following permissions.

lambda – Allows principals to invoke Lambda functions whose name includes "sagemaker" (case-insensitive), "GtRecipe", or "LabelingFunction".

s3 – Allows principals to add and retrieve objects from Amazon S3 buckets. These objects are limited to those whose case-insensitive name contains "groundtruth" or "sagemaker", or are tagged with "SageMaker".

cloudwatch – Allows principals to post CloudWatch metrics.

logs – Allows principals to create and access log streams, and post log events.

sqs – Allows principals to create Amazon SQS queues, and send and receive Amazon SQS messages. These permissions are limited to queues whose name includes "GroundTruth".

sns – Allows principals to subscribe to and publish messages to Amazon SNS topics whose case-insensitive name contains "groundtruth" or "sagemaker".

ec2 – Allows principals to create, describe, and delete Amazon VPC endpoints whose VPC endpoint service name contains "sagemaker-task-resources" or "labeling".

View details about updates to AWS managed policies for Amazon SageMaker AI Ground Truth since this service began tracking these changes.

AmazonSageMakerGroundTruthExecution - Update to an existing policy

Add ec2:CreateVpcEndpoint, ec2:DescribeVpcEndpoints, and ec2:DeleteVpcEndpoints permissions.

AmazonSageMakerGroundTruthExecution - Update to an existing policy

Remove sqs:SendMessageBatch permission.

AmazonSageMakerGroundTruthExecution - New policy

**Examples:**

Example 1 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "CustomLabelingJobs",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:*:*:function:*GtRecipe*",
                "arn:aws:lambda:*:*:function:*LabelingFunction*",
                "arn:aws:lambda:*:*:function:*SageMaker*",
                "arn:aws:lambda:*:*:function:*sagemaker*",
                "arn:aws:lambda:*:*:function:*Sagemaker*"
            ]
        },
        {
            "Effect": "Allow"
...
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "CustomLabelingJobs",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:*:*:function:*GtRecipe*",
                "arn:aws:lambda:*:*:function:*LabelingFunction*",
                "arn:aws:lambda:*:*:function:*SageMaker*",
                "arn:aws:lambda:*:*:function:*sagemaker*",
                "arn:aws:lambda:*:*:function:*Sagemaker*"
            ]
        },
        {
            "Effect": "Allow"
...
```

Example 3 (unknown):
```unknown
ec2:CreateVpcEndpoint
```

Example 4 (unknown):
```unknown
ec2:DescribeVpcEndpoints
```

---

## Object2Vec Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/object2vec.html

**Contents:**
- Object2Vec Algorithm
        - Topics
- I/O Interface for the Object2Vec Algorithm
- EC2 Instance Recommendation for the Object2Vec Algorithm
- Object2Vec Sample Notebooks

The Amazon SageMaker AI Object2Vec algorithm is a general-purpose neural embedding algorithm that is highly customizable. It can learn low-dimensional dense embeddings of high-dimensional objects. The embeddings are learned in a way that preserves the semantics of the relationship between pairs of objects in the original space in the embedding space. You can use the learned embeddings to efficiently compute nearest neighbors of objects and to visualize natural clusters of related objects in low-dimensional space, for example. You can also use the embeddings as features of the corresponding objects in downstream supervised tasks, such as classification or regression.

Object2Vec generalizes the well-known Word2Vec embedding technique for words that is optimized in the SageMaker AI BlazingText algorithm. For a blog post that discusses how to apply Object2Vec to some practical use cases, see Introduction to Amazon SageMaker AI Object2Vec.

I/O Interface for the Object2Vec Algorithm

EC2 Instance Recommendation for the Object2Vec Algorithm

Object2Vec Sample Notebooks

Object2Vec Hyperparameters

Tune an Object2Vec Model

Data Formats for Object2Vec Training

Data Formats for Object2Vec Inference

Encoder Embeddings for Object2Vec

You can use Object2Vec on many input data types, including the following examples.

Sentence-sentence pairs

Labels-sequence pairs

Customer-customer pairs

The customer ID of Jane and customer ID of Jackie.

Product-product pairs

The product ID of football and product ID of basketball.

Item review user-item pairs

A user's ID and the items she has bought, such as apple, pear, and orange.

To transform the input data into the supported formats, you must preprocess it. Currently, Object2Vec natively supports two types of input:

A discrete token, which is represented as a list of a single integer-id. For example, [10].

A sequences of discrete tokens, which is represented as a list of integer-ids. For example, [0,12,10,13].

The object in each pair can be asymmetric. For example, the pairs can be (token, sequence) or (token, token) or (sequence, sequence). For token inputs, the algorithm supports simple embeddings as compatible encoders. For sequences of token vectors, the algorithm supports the following as encoders:

Average-pooled embeddings

Hierarchical convolutional neural networks (CNNs),

Multi-layered bidirectional long short-term memory (BiLSTMs)

The input label for each pair can be one of the following:

A categorical l

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
integer-ids
```

Example 2 (unknown):
```unknown
[0,12,10,13]
```

Example 3 (unknown):
```unknown
output_layer
```

Example 4 (unknown):
```unknown
INFERENCE_PREFERRED_MODE
```

---

## Generative AI assistance for solving ML problems in Canvas using Amazon Q Developer

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-q.html

**Contents:**
- Generative AI assistance for solving ML problems in Canvas using Amazon Q Developer
        - Note
- How it works
        - Important
- Supported regions
- Amazon Q Developer capabilities available in Canvas
- Prerequisites
        - Note
- Getting started

While using Amazon SageMaker Canvas, you can chat with Amazon Q Developer in natural language to leverage generative AI and solve problems. Q Developer is an assistant that helps you translate your goals into machine learning (ML) tasks and describes each step of the ML workflow. Q Developer helps Canvas users reduce the amount of time, effort, and data science expertise required to leverage ML and make data-driven decisions for their organizations.

Through a conversation with Q Developer, you can initiate actions in Canvas such as preparing data, building an ML model, making predictions, and deploying a model. Q Developer makes suggestions for next steps and provides you with context as you complete each step. It also informs you of results; for example, Canvas can transform your dataset according to best practices, and Q Developer can list the transforms that were used and why.

Amazon Q Developer is available in SageMaker Canvas at no additional cost to both Amazon Q Developer Pro Tier and Free Tier users. However, standard charges apply for resources such as the SageMaker Canvas workspace instance and any resources used for building or deploying models. For more information about pricing, see Amazon SageMaker Canvas pricing.

Use of Amazon Q is licensed to you under MIT's 0 License and subject to the AWS Responsible AI Policy. When you use Q Developer from outside the US, Q Developer processes data across US regions. For more information, see Cross region inference in Amazon Q Developer.

Amazon Q Developer in SageMaker Canvas doesn't use user content to improve the service, regardless of whether you use the Free-tier or Pro-tier subscription. For service telemetry purposes, Q Developer might track your usage, such as the number of questions asked and whether recommendations were accepted or rejected. This telemetry data doesn't include personally identifiable information such as IP address.

Amazon Q Developer is a generative AI powered assistant available in SageMaker Canvas that you can query using natural language. Q Developer makes suggestions for each step of the machine learning workflow, explaining concepts and providing you with options and more details as needed. You can use Q Developer for help with regression, binary classification, and multi-class classification use cases.

For example, to predict customer churn, upload a dataset of historical customer churn information to Canvas through Q Developer. Q Developer suggests an appropriate ML

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
number of valid values
```

Example 2 (unknown):
```unknown
feature type
```

Example 3 (unknown):
```unknown
standard deviation
```

Example 4 (unknown):
```unknown
25th percentile
```

---

## Configure the default parameters of an Autopilot experiment (for administrators)

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-set-default-parameters-create-experiment.html

**Contents:**
- Configure the default parameters of an Autopilot experiment (for administrators)
        - Note
        - Topics
- List of default parameters supported
- Set default Autopilot experiment parameters

Autopilot supports setting default values to simplify the configuration of Amazon SageMaker Autopilot when you create an Autopilot experiment using the Studio Classic UI. Administrators can use Studio Classic lifecycle configurations (LCC) to set infrastructure, networking, and security values in configuration files and pre-populate the advanced settings of AutoML jobs.

By doing so, they can fully control network connectivity and access permissions for the resources associated with Amazon SageMaker Studio Classic, including SageMaker AI instances, data sources, output data, and other related services. Specifically, administrators can configure a desired network architecture, such as Amazon VPC, subnets, and security groups, for a Studio Classic domain or individual user profiles. Data scientists can focus on data science specific parameters when creating their Autopilot experiments using the Studio Classic UI. Furthermore, administrators can manage the encryption of data on the instance in which Autopilot experiments run by setting default encryption keys.

This feature is currently not available in the Asia Pacific (Hong Kong) and Middle East (Bahrain) opt-in Regions.

In the following sections, you can find the full list of parameters supporting the setting of defaults when creating an Autopilot experiment using the Studio Classic UI, and learn how to set those default values.

List of default parameters supported

Set default Autopilot experiment parameters

The following parameters support setting default values with a configuration file for creating an Autopilot experiment using the Studio Classic UI. Once set, the values automatically fill in their corresponding field in the Autopilot' Create Experiment tab in the Studio Classic UI. See Advanced settings (optional) for a full description of each field.

Security: Amazon VPC, subnets, and security groups.

Access: AWS IAM role ARNs.

Encryption: AWS KMS key IDs.

Tags: Key-value pairs used to label and organize SageMaker AI resources.

Administrators can set default values in a configuration file, then manually place the file in a recommended location within the Studio Classic environment of specific users, or they can pass the file to a lifecycle configuration script (LCC) to automate the customization of the Studio Classic environment for a given domain or user profile.

To set up the configuration file, start by filling in its default parameters.

To configure any or all default values listed in L

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
config.yaml
```

Example 2 (unknown):
```unknown
SchemaVersion: '1.0'
SageMaker:
  AutoMLJob:
    # https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateAutoMLJob.html
    AutoMLJobConfig:
      SecurityConfig:
        EnableInterContainerTrafficEncryption: true
        VolumeKmsKeyId: 'kms-key-id'
        VpcConfig:
          SecurityGroupIds:
            - 'security-group-id-1'
            - 'security-group-id-2'
          Subnets:
            - 'subnet-1'
            - 'subnet-2'
    OutputDataConfig:
      KmsKeyId: 'kms-key-id'
    RoleArn: 'arn:aws:iam::111222333444:role/Admin'
    Tags:
    - Key: 'tag_key'
      Value:
...
```

Example 3 (unknown):
```unknown
security-group-id-1
```

Example 4 (unknown):
```unknown
security-group-id-2
```

---

## Supported Regions and Quotas

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/regions-quotas.html

**Contents:**
- Supported Regions and Quotas
- Quotas

This page gives information about the AWS Regions supported by Amazon SageMaker AI and the Amazon Elastic Compute Cloud (Amazon EC2) instance types, as well as quotas for Amazon SageMaker AI resources.

For information about the instance types that are available in each Region, see Amazon SageMaker Pricing.

For a list of the SageMaker AI service endpoints for each Region, see Amazon SageMaker AI endpoints and quotas in the AWS General Reference.

For a list of SageMaker AI quotas, see Amazon SageMaker AI endpoints and quotas in the AWS General Reference.

The Service Quotas console provides information about your service quotas. You can use the Service Quotas console to view your default service quotas or to request quota increases. To request a quota increase for adjustable quotas, see Requesting a quota increase.

You can set up a quota request template for your AWS Organization that automatically requests quota increases during account creation. For more information, see Using Service Quotas request templates.

---

## DeleteFeatureGroup

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_DeleteFeatureGroup.html

**Contents:**
- DeleteFeatureGroup
- Request Syntax
- Request Parameters
- Response Elements
- Errors
- See Also

Delete the FeatureGroup and any data that was written to the OnlineStore of the FeatureGroup. Data cannot be accessed from the OnlineStore immediately after DeleteFeatureGroup is called.

Data written into the OfflineStore will not be deleted. The AWS Glue database and tables that are automatically created for your OfflineStore are not deleted.

Note that it can take approximately 10-15 minutes to delete an OnlineStore FeatureGroup with the InMemory StorageType.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

The name of the FeatureGroup you want to delete. The name must be unique within an AWS Region in an AWS account.

Length Constraints: Minimum length of 1. Maximum length of 64.

Pattern: [a-zA-Z0-9]([_-]*[a-zA-Z0-9]){0,63}

If the action is successful, the service sends back an HTTP 200 response with an empty HTTP body.

For information about the errors that are common to all actions, see Common Errors.

Resource being access is not found.

HTTP Status Code: 400

For more information about using this API in one of the language-specific AWS SDKs, see the following:

AWS Command Line Interface V2

AWS SDK for JavaScript V3

**Examples:**

Example 1 (unknown):
```unknown
FeatureGroup
```

Example 2 (unknown):
```unknown
OnlineStore
```

Example 3 (unknown):
```unknown
FeatureGroup
```

Example 4 (unknown):
```unknown
OnlineStore
```

---

## Create an AutoML job for text classification using the API

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-create-experiment-text-classification.html

**Contents:**
- Create an AutoML job for text classification using the API
        - Note
- Required parameters
- Optional parameters

The following instructions show how to create an Amazon SageMaker Autopilot job as a pilot experiment for text classification problem types using SageMaker API Reference.

Tasks such as text and image classification, time-series forecasting, and fine-tuning of large language models are exclusively available through the version 2 of the AutoML REST API. If your language of choice is Python, you can refer to AWS SDK for Python (Boto3) or the AutoMLV2 object of the Amazon SageMaker Python SDK directly.

Users who prefer the convenience of a user interface can use Amazon SageMaker Canvas to access pre-trained models and generative AI foundation models, or create custom models tailored for specific text, image classification, forecasting needs, or generative AI.

You can create an Autopilot text classification experiment programmatically by calling the CreateAutoMLJobV2 API action in any language supported by Amazon SageMaker Autopilot or the AWS CLI.

For information on how this API action translates into a function in the language of your choice, see the See Also section of CreateAutoMLJobV2 and choose an SDK. As an example, for Python users, see the full request syntax of create_auto_ml_job_v2 in AWS SDK for Python (Boto3).

The following is a collection of mandatory and optional input request parameters for the CreateAutoMLJobV2 API action used in text classification.

When calling CreateAutoMLJobV2 to create an Autopilot experiment for text classification, you must provide the following values:

An AutoMLJobName to specify the name of your job.

At least one AutoMLJobChannel in AutoMLJobInputDataConfig to specify your data source.

An AutoMLProblemTypeConfig of type TextClassificationJobConfig.

An OutputDataConfig to specify the Amazon S3 output path to store the artifacts of your AutoML job.

A RoleArn to specify the ARN of the role used to access your data.

All other parameters are optional.

The following sections provide details of some optional parameters that you can pass to your text classification AutoML job.

You can provide your own validation dataset and custom data split ratio, or let Autopilot split the dataset automatically.

Each AutoMLJobChannel object (see the required parameter AutoMLJobInputDataConfig) has a ChannelType, which can be set to either training or validation values that specify how the data is to be used when building a machine learning model.

At least one data source must be provided and a maximum of two data sources is a

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 2 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 3 (unknown):
```unknown
create_auto_ml_job_v2
```

Example 4 (unknown):
```unknown
CreateAutoMLJobV2
```

---

## Feature Store concepts

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-concepts.html

**Contents:**
- Feature Store concepts
        - Topics
- Concepts overview diagram
- Ingestion diagrams

We list common terms used in Amazon SageMaker Feature Store, followed by example diagrams to visualize a few concepts:

Feature Store: Storage and data management layer for machine learning (ML) features. Serves as the single source of truth to store, retrieve, remove, track, share, discover, and control access to features. In the following example diagram, the Feature Store is a store for your feature groups, which contains your ML data, and provides additional services.

Online store: Low latency, high availability store for a feature group that enables real-time lookup of records. The online store allows quick access to the latest record via the GetRecord API.

Offline store: Stores historical data in your Amazon S3 bucket. The offline store is used when low (sub-second) latency reads are not needed. For example, the offline store can be used when you want to store and serve features for exploration, model training, and batch inference.

Feature group: The main resource of Feature Store that contains the data and metadata used for training or predicting with a ML model. A feature group is a logical grouping of features used to describe records. In the following example diagram, a feature group contains your ML data.

Feature: A property that is used as one of the inputs to train or predict using your ML model. In the Feature Store API a feature is an attribute of a record. In the following example diagram, a feature describes a column in your ML data table.

Feature definition: Consists of a name and one of the data types: integral, string or fractional. A feature group contains a list of feature definitions. For more information on Feature Store data types, see Data types.

Record: Collection of values for features for a single record identifier. A combination of record identifier and event time values uniquely identify a record within a feature group. In the following example diagram, a record is a row in your ML data table.

Record identifier name: The record identifier name is the name of the feature that identifies the records. It must refer to one of the names of a feature defined in the feature group's feature definitions. Each feature group is defined with a record identifier name.

Event time: Timestamp that you provide corresponding to when the record event occurred. All records in a feature group must have a corresponding event time. The online store only contains the record corresponding to the latest event time, whereas the offline store co

*[Content truncated]*

---

## Use Feature Store with SDK for Python (Boto3)

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-create-feature-group.html

**Contents:**
- Use Feature Store with SDK for Python (Boto3)
        - Important
        - Topics

The feature group is the main Feature Store resource that contains your machine learning (ML) data and metadata stored in Amazon SageMaker Feature Store. A feature group is a logical grouping of features and records. A feature group’s definition is composed of a configurations for its online and offline store and a list of feature definitions that are used to describe the values of your records. The feature definitions must include a record identifier name and an event time name. For more information on feature store concepts, see Feature Store concepts.

Prior to using a feature store you typically load your dataset, run transformations, and set up your features for ingestion. This process has a lot of variation and is highly dependent on your data. The example code in the following topics refer to the Introduction to Feature Store and Fraud Detection with Amazon SageMaker Feature Store example notebooks, respectively. Both use the AWS SDK for Python (Boto3). For more Feature Store examples and resources, see Amazon SageMaker Feature Store resources.

Feature Store supports the following feature types: String, Fractional (IEEE 64-bit floating point value), and Integral (Int64 - 64 bit signed integral value). The default type is set to String. This means that, if a column in your dataset is not of a float or long feature type, it defaults to String in your feature store.

You may use a schema to describe your data’s columns and data types. You pass this schema into FeatureDefinitions, a required parameter for a FeatureGroup. You can use the SDK for Python (Boto3), which has automatic data type detection when you use the load_feature_definitions function.

The default behavior when a new feature record is added with an already existing record ID is as follows. In the offline store, the new record will be appended. In the online store, if the event time of the new record is less than the existing event time then nothing will happen, but if the event time of the new record is greater than or equal to the existing event time, the record will be overwritten.

When you create a new feature group you can choose one of the following table formats:

Ingesting data, especially when streaming, can result in a large number of small files deposited into the offline store. This can negatively impact query performance due the higher number of file operations required. To avoid potential performance issues, use the Apache Iceberg table format when creating new feature gro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
FeatureDefinitions
```

Example 2 (unknown):
```unknown
FeatureGroup
```

Example 3 (unknown):
```unknown
load_feature_definitions
```

---

## AWS managed policies for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol.html#security-iam-awsmanpol-updates

**Contents:**
- AWS managed policies for Amazon SageMaker AI
        - Important
        - Topics
- AWS managed policy: AmazonSageMakerFullAccess
- AWS managed policy: AmazonSageMakerReadOnly
- SageMaker AI Updates to AWS Managed Policies

To add permissions to users, groups, and roles, it is easier to use AWS managed policies than to write policies yourself. It takes time and expertise to create IAM customer managed policies that provide your team with only the permissions they need. To get started quickly, you can use our AWS managed policies. These policies cover common use cases and are available in your AWS account. For more information about AWS managed policies, see AWS managed policies in the IAM User Guide.

AWS services maintain and update AWS managed policies. You can't change the permissions in AWS managed policies. Services occasionally add additional permissions to an AWS managed policy to support new features. This type of update affects all identities (users, groups, and roles) to which the policy is attached. Services are most likely to update an AWS managed policy when a new feature is launched or when new operations become available. Services do not remove permissions from an AWS managed policy, so policy updates won't break your existing permissions.

Additionally, AWS supports managed policies for job functions that span multiple services. For example, the ReadOnlyAccess AWS managed policy provides read-only access to all AWS services and resources. When a service launches a new feature, AWS adds read-only permissions for new operations and resources. For a list and descriptions of job function policies, see AWS managed policies for job functions in the IAM User Guide.

We recommend that you use the most restricted policy that allows you to perform your use case.

The following AWS managed policies, which you can attach to users in your account, are specific to Amazon SageMaker AI:

AmazonSageMakerFullAccess – Grants full access to Amazon SageMaker AI and SageMaker AI geospatial resources and the supported operations. This does not provide unrestricted Amazon S3 access, but supports buckets and objects with specific sagemaker tags. This policy allows all IAM roles to be passed to Amazon SageMaker AI, but only allows IAM roles with "AmazonSageMaker" in them to be passed to the AWS Glue, AWS Step Functions, and AWS RoboMaker services.

AmazonSageMakerReadOnly – Grants read-only access to Amazon SageMaker AI resources.

The following AWS managed policies can be attached to users in your account but are not recommended:

AdministratorAccess – Grants all actions for all AWS services and for all resources in the account.

DataScientist – Grants a wide range of permissions to c

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
ReadOnlyAccess
```

Example 2 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 3 (unknown):
```unknown
AmazonSageMakerReadOnly
```

Example 4 (unknown):
```unknown
AdministratorAccess
```

---

## XGBoost algorithm with Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html#xgboost-modes

**Contents:**
- XGBoost algorithm with Amazon SageMaker AI
- Supported versions
        - Warning
        - Important
        - Warning
        - Note
        - Note
- EC2 instance recommendation for the XGBoost algorithm
  - Training
    - CPU training

The XGBoost (eXtreme Gradient Boosting) is a popular and efficient open-source implementation of the gradient boosted trees algorithm. Gradient boosting is a supervised learning algorithm that tries to accurately predict a target variable by combining multiple estimates from a set of simpler models. The XGBoost algorithm performs well in machine learning competitions for the following reasons:

Its robust handling of a variety of data types, relationships, distributions.

The variety of hyperparameters that you can fine-tune.

You can use XGBoost for regression, classification (binary and multiclass), and ranking problems.

You can use the new release of the XGBoost algorithm as either:

A Amazon SageMaker AI built-in algorithm.

A framework to run training scripts in your local environments.

This implementation has a smaller memory footprint, better logging, improved hyperparameter validation, and an bigger set of metrics than the original versions. It provides an XGBoost estimator that runs a training script in a managed XGBoost environment. The current release of SageMaker AI XGBoost is based on the original XGBoost versions 1.0, 1.2, 1.3, 1.5, and 1.7.

For more information about the Amazon SageMaker AI XGBoost algorithm, see the following blog posts:

Introducing the open-source Amazon SageMaker AI XGBoost algorithm container

Amazon SageMaker AI XGBoost now offers fully distributed GPU training

Framework (open source) mode: 1.2-1, 1.2-2, 1.3-1, 1.5-1, 1.7-1

Algorithm mode: 1.2-1, 1.2-2, 1.3-1, 1.5-1, 1.7-1

Due to required compute capacity, version 1.7-1 of SageMaker AI XGBoost is not compatible with GPU instances from the P2 instance family for training or inference.

When you retrieve the SageMaker AI XGBoost image URI, do not use :latest or :1 for the image URI tag. You must specify one of the Supported versions to choose the SageMaker AI-managed XGBoost container with the native XGBoost package version that you want to use. To find the package version migrated into the SageMaker AI XGBoost containers, see Docker Registry Paths and Example Code. Then choose your AWS Region, and navigate to the XGBoost (algorithm) section.

The XGBoost 0.90 versions are deprecated. Supports for security updates or bug fixes for XGBoost 0.90 is discontinued. We highly recommend that you upgrade the XGBoost version to one of the newer versions.

XGBoost v1.1 is not supported on SageMaker AI. XGBoost 1.1 has a broken capability to run prediction when the test input

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
tree_method
```

Example 2 (unknown):
```unknown
instance_count
```

Example 3 (unknown):
```unknown
ShardedByS3Key
```

Example 4 (unknown):
```unknown
distribution
```

---

## Create an AutoML job for time-series forecasting using the API

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-create-experiment-timeseries-forecasting.html

**Contents:**
- Create an AutoML job for time-series forecasting using the API
        - Note
        - Note
- Prerequisites
        - Note
- Required parameters
- Optional parameters

Forecasting in machine learning refers to the process of predicting future outcomes or trends based on historical data and patterns. By analyzing past time-series data and identifying underlying patterns, machine learning algorithms can make predictions and provide valuable insights into future behavior. In forecasting, the goal is to develop models that can accurately capture the relationship between input variables and the target variable over time. This involves examining various factors such as trends, seasonality, and other relevant patterns within the data. The collected information is then used to train a machine learning model. The trained model is capable of generating predictions by taking new input data and applying the learned patterns and relationships. It can provide forecasts for a wide range of use cases, such as sales projections, stock market trends, weather forecasts, demand forecasting, and many more.

The following instructions show how to create an Amazon SageMaker Autopilot job as a pilot experiment for time-series forecasting problem types using SageMaker API Reference.

Tasks such as text and image classification, time-series forecasting, and fine-tuning of large language models are exclusively available through the version 2 of the AutoML REST API. If your language of choice is Python, you can refer to AWS SDK for Python (Boto3) or the AutoMLV2 object of the Amazon SageMaker Python SDK directly.

Users who prefer the convenience of a user interface can use Amazon SageMaker Canvas to access pre-trained models and generative AI foundation models, or create custom models tailored for specific text, image classification, forecasting needs, or generative AI.

You can create an Autopilot time-series forecasting experiment programmatically by calling the CreateAutoMLJobV2 API in any language supported by Amazon SageMaker Autopilot or the AWS CLI.

For information on how this API action translates into a function in the language of your choice, see the See Also section of CreateAutoMLJobV2 and choose an SDK. As an example, for Python users, see the full request syntax of create_auto_ml_job_v2 in AWS SDK for Python (Boto3).

Autopilot trains several model candidates with your target time-series, then selects an optimal forecasting model for a given objective metric. When your model candidates have been trained, you can find the best candidate metrics in the response to DescribeAutoMLJobV2 at BestCandidate.

The following sections define th

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 2 (unknown):
```unknown
CreateAutoMLJobV2
```

Example 3 (unknown):
```unknown
create_auto_ml_job_v2
```

Example 4 (unknown):
```unknown
DescribeAutoMLJobV2
```

---

## Controlled access to assets with Amazon SageMaker Assets

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sm-assets.html

**Contents:**
- Controlled access to assets with Amazon SageMaker Assets
        - Topics

Use Amazon SageMaker Assets to provide controlled and regulated access to assets, models or data tables, belonging to your organization. Within SageMaker Assets, users from different AWS accounts can create and share assets related to specific business problems without additional administrator overhead. Instead of having permissions being statically tied to their identity, users can provide permissions to assets that they’re using for their active workflows.

Assets are ML assets or data assets. ML assets are metadata that point to Amazon SageMaker Feature Store feature groups or SageMaker Model Registry Model Groups. Data assets are metadata that point to Amazon Redshift tables or AWS Glue tables.

For example, the asset for a model group contains the model group name and the Amazon Resource Name (ARN) for the model package group. The asset points to the underlying collection of models. The asset itself can be shared between users.

Users can create assets for their own projects. They can make them visible to users who aren't members of those projects. The users who aren't project members can search through the assets and read their metadata. They can use the metadata to determine whether they want to access to the underlying source of data.

To understand the SageMaker Assets workflow better, imagine that you have two groups of users in your organization, Group A and Group B. The users in Group A are looking to predict home prices. They’re looking to collaborate with the users in Group B who are in a different AWS account. They have housing data stored in AWS Glue tables. They also have different models saved as model packages within a model group. With SageMaker Assets, the users in Group A can share their AWS Glue tables and model packages with the users in Group B in a few clicks. Without administrator intervention, the users in Group A provided precisely scoped permissions to the users in Group B.

Users can create assets and publish them to make them visible throughout the organization. Other users can request access to those assets.

Set up SageMaker Assets (administrator guide)

Work with assets (user guide)

---

## Model evaluation

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-evaluate-model.html

**Contents:**
- Model evaluation

After you’ve built your model, you can evaluate how well your model performed on your data before using it to make predictions. You can use information, such as the model’s accuracy when predicting labels and advanced metrics, to determine whether your model can make sufficiently accurate predictions for your data.

The section Evaluate your model's performance describes how to view and interpret the information on your model's Analyze page. The section Use advanced metrics in your analyses contains more detailed information about the Advanced metrics used to quantify your model’s accuracy.

You can also view more advanced information for specific model candidates, which are all of the model iterations that Canvas runs through while building your model. Based on the advanced metrics for a given model candidate, you can select a different candidate to be the default, or the version that is used for making predictions and deploying. For each model candidate, you can view the Advanced metrics information to help you decide which model candidate you’d like to select as the default. You can view this information by selecting the model candidate from the Model leaderboard. For more information, see View model candidates in the model leaderboard.

Canvas also provides the option to download a Jupyter notebook so that you can view and run the code used to build your model. This is useful if you’d like to make adjustments to the code or learn more about how your model was built. For more information, see Download a model notebook.

---

## Amazon SageMaker geospatial capabilities

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/geospatial.html

**Contents:**
- Amazon SageMaker geospatial capabilities
        - Important
        - Note
        - Why use SageMaker geospatial capabilities?
- How can I use SageMaker geospatial capabilities?
        - SageMaker AI has the following geospatial capabilities
- Are you a first-time user of SageMaker geospatial?
        - Topics

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. If prior to November 30, 2023 you created a Amazon SageMaker AI domain, Studio Classic remains the default experience. domains created after November 30, 2023 default to the new Studio experience.

Amazon SageMaker geospatial features and resources are only available in Studio Classic. To learn more about setting up a domain and getting started with Studio, see Getting started with Amazon SageMaker geospatial .

Amazon SageMaker geospatial capabilities makes it easier for data scientists and machine learning (ML) engineers to build, train, and deploy ML models faster using geospatial data. You have access to open-source and third-party data, processing, and visualization tools to make it more efficient to prepare geospatial data for ML. You can increase your productivity by using purpose-built algorithms and pre-trained ML models to speed up model building and training, and use built-in visualization tools to explore prediction outputs on an interactive map and then collaborate across teams on insights and results.

Currently, SageMaker geospatial capabilities are only supported in the US West (Oregon) Region.

If you don't see the SageMaker geospatial UI available in your current Studio Classic instance check to make sure you are currently in the US West (Oregon) Region.

You can use SageMaker geospatial capabilities to make predictions on geospatial data faster than do-it-yourself solutions. SageMaker geospatial capabilities make it easier to access geospatial data from your existing customer data lakes, open-source datasets, and other SageMaker geospatial data providers. SageMaker geospatial capabilities minimize the need for building custom infrastructure and data preprocessing functions by offering purpose-built algorithms for efficient data preparation, model training, and inference. You can also create and share custom visualizations and data with your company from Amazon SageMaker Studio Classic. SageMaker geospatial capabilities offer pre-trained models for common uses in agriculture, real estate, insurance, and financial services.

You can use SageMaker geospatial capabilities in two ways.

Through the SageMaker geospatial UI, as a part of Amazon SageMaker Studio Classic UI.

Through a Studio Classic notebook instance that uses the Geospatial 1.0 image.

Use a purpose built SageMaker geospatial image that supports both CPU and GP

*[Content truncated]*

---

## Sequence-to-Sequence Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/seq-2-seq.html

**Contents:**
- Sequence-to-Sequence Algorithm
        - Topics
- Input/Output Interface for the Sequence-to-Sequence Algorithm
- EC2 Instance Recommendation for the Sequence-to-Sequence Algorithm
- Sequence-to-Sequence Sample Notebooks

Amazon SageMaker AI Sequence to Sequence is a supervised learning algorithm where the input is a sequence of tokens (for example, text, audio) and the output generated is another sequence of tokens. Example applications include: machine translation (input a sentence from one language and predict what that sentence would be in another language), text summarization (input a longer string of words and predict a shorter string of words that is a summary), speech-to-text (audio clips converted into output sentences in tokens). Recently, problems in this domain have been successfully modeled with deep neural networks that show a significant performance boost over previous methodologies. Amazon SageMaker AI seq2seq uses Recurrent Neural Networks (RNNs) and Convolutional Neural Network (CNN) models with attention as encoder-decoder architectures.

Input/Output Interface for the Sequence-to-Sequence Algorithm

EC2 Instance Recommendation for the Sequence-to-Sequence Algorithm

Sequence-to-Sequence Sample Notebooks

How Sequence-to-Sequence Works

Sequence-to-Sequence Hyperparameters

Tune a Sequence-to-Sequence Model

SageMaker AI seq2seq expects data in RecordIO-Protobuf format. However, the tokens are expected as integers, not as floating points, as is usually the case.

A script to convert data from tokenized text files to the protobuf format is included in the seq2seq example notebook. In general, it packs the data into 32-bit integer tensors and generates the necessary vocabulary files, which are needed for metric calculation and inference.

After preprocessing is done, the algorithm can be invoked for training. The algorithm expects three channels:

train: It should contain the training data (for example, the train.rec file generated by the preprocessing script).

validation: It should contain the validation data (for example, the val.rec file generated by the preprocessing script).

vocab: It should contain two vocabulary files (vocab.src.json and vocab.trg.json)

If the algorithm doesn't find data in any of these three channels, training results in an error.

For hosted endpoints, inference supports two data formats. To perform inference using space separated text tokens, use the application/json format. Otherwise, use the recordio-protobuf format to work with the integer encoded data. Both modes support batching of input data. application/json format also allows you to visualize the attention matrix.

application/json: Expects the input in JSON format and 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
vocab.src.json
```

Example 2 (unknown):
```unknown
vocab.trg.json
```

Example 3 (unknown):
```unknown
application/json
```

Example 4 (unknown):
```unknown
recordio-protobuf
```

---

## Amazon SageMaker Feature Store resources

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-resources.html

**Contents:**
- Amazon SageMaker Feature Store resources
- Feature Store example notebooks and workshops
- Feature Store Python SDK and API

The following lists the available resources for Amazon SageMaker Feature Store users. For the Feature Store main page, see Amazon SageMaker Feature Store.

To get started using Amazon SageMaker Feature Store, you can choose from a variety of example Jupyter notebooks from the following table. If this is your first time using Feature Store, try out the Introduction to Feature Store notebook. To run any these notebooks, you must attach this policy to your IAM execution role: AmazonSageMakerFeatureStoreAccess.

See IAM Roles to access your role and attach this policy. For a walkthrough on how to view the policies attached to a role and how to add a policy to your role, see Adding policies to your IAM role.

The following table lists a variety of resources to help you get started with Feature Store. This table contains examples, instructions, and example notebooks to guide you in how to use Feature Store for the first time to specific use cases. The code in these resources use the SageMaker AI SDK for Python (Boto3).

Get started with Amazon SageMaker Feature Store in Read the Docs.

A list of example notebooks to introduce you to Feature Store and its features to help you get started.

Amazon SageMaker Feature Store guide in Read the Docs.

A Feature Store guide on how to set up, create a feature group, load data into a feature group, and how to use Feature Store in general.

Amazon SageMaker Feature Store end-to-end workshop in the aws-samples Github repository

An end-to-end Feature Store workshop.

Feature Store example notebooks in the SageMaker AI example notebooks repository.

Specific use case example notebooks for Feature Store.

Python Software Development Kit (SDK) and Application Programming Interface (API) are tools used for creating software applications. The Feature Store SDK for Python (Boto3) and API are listed in the following table.

Feature Store APIs in the Amazon SageMaker Python SDK Read the Docs

The Feature Store APIs in Read the Docs.

Feature Store Python SDK in the Amazon SageMaker Python SDK Github repository

The Feature Store Python SDK Github repository.

Feature Store Runtime operations and data types in the SDK for Python (Boto3) documentation

Feature Store Runtime client that contains all data plane API operations and data types for Feature Store.

Amazon SageMaker Feature Store Runtime in the Amazon SageMaker API Reference

Some feature group level actions supported by Feature Store. If the API operation or data type you ar

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerFeatureStoreAccess
```

Example 2 (unknown):
```unknown
aws-samples
```

---

## Transform data

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-transform.html

**Contents:**
- Transform data
- Join Datasets
        - Note
- Concatenate Datasets
        - To concatenate two datasets:
- Balance Data
        - Note
- Custom Transforms
        - Important
- Custom Formula

Amazon SageMaker Data Wrangler provides numerous ML data transforms to streamline cleaning and featurizing your data. Using the interactive data preparation tools in Data Wrangler, you can sample datasets of any size with a variety of sampling techniques and start exploring your data in a matter of minutes. After finalizing your data transforms on the sampled data, you can then scale the data flow to apply those transformations to the entire dataset.

When you add a transform, it adds a step to the data flow. Each transform you add modifies your dataset and produces a new dataframe. All subsequent transforms apply to the resulting dataframe.

Data Wrangler includes built-in transforms, which you can use to transform columns without any code. If you know how you want to prepare your data but don't know how to get started or which transforms to use, you can use the chat for data prep feature to interact conversationally with Data Wrangler and apply transforms using natural language. For more information, see Chat for data prep.

You can also add custom transformations using PySpark, Python (User-Defined Function), pandas, and PySpark SQL. Some transforms operate in place, while others create a new output column in your dataset.

You can apply transforms to multiple columns at once. For example, you can delete multiple columns in a single step.

You can apply the Process numeric and Handle missing transforms only to a single column.

Use this page to learn more about the built-in and custom transforms offered by Data Wrangler.

You can join datasets directly in your data flow. When you join two datasets, the resulting joined dataset appears in your flow. The following join types are supported by Data Wrangler.

Left outer – Include all rows from the left table. If the value for the column joined on a left table row does not match any right table row values, that row contains null values for all right table columns in the joined table.

Left anti – Include rows from the left table that do not contain values in the right table for the joined column.

Left semi – Include a single row from the left table for all identical rows that satisfy the criteria in the join statement. This excludes duplicate rows from the left table that match the criteria of the join.

Right outer – Include all rows from the right table. If the value for the joined column in a right table row does not match any left table row values, that row contains null values for all left table column

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
A
                    column
```

Example 2 (unknown):
```unknown
df.rename(columns={"A column": "A_column", "B column": "B_column"})
```

Example 3 (python):
```python
from pyspark.sql.functions import from_unixtime, to_date, date_format
df = df.withColumn('DATE_TIME', from_unixtime('TIMESTAMP'))
df = df.withColumn( 'EVENT_DATE', to_date('DATE_TIME')).withColumn(
'EVENT_TIME', date_format('DATE_TIME', 'HH:mm:ss'))
```

Example 4 (unknown):
```unknown
SELECT name, fare, pclass, survived FROM df
```

---

## 

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-update.html

---

## 

**URL:** https://docs.aws.amazon.com/sagemaker/

---

## LightGBM

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/lightgbm.html

**Contents:**
- LightGBM
- Amazon EC2 instance recommendation for the LightGBM algorithm
- LightGBM sample notebooks

LightGBM is a popular and efficient open-source implementation of the Gradient Boosting Decision Tree (GBDT) algorithm. GBDT is a supervised learning algorithm that attempts to accurately predict a target variable by combining an ensemble of estimates from a set of simpler and weaker models. LightGBM uses additional techniques to significantly improve the efficiency and scalability of conventional GBDT. This page includes information about Amazon EC2 instance recommendations and sample notebooks for LightGBM.

SageMaker AI LightGBM currently supports single-instance and multi-instance CPU training. For multi-instance CPU training (distributed training), specify an instance_count greater than 1 when you define your Estimator. For more information on distributed training with LightGBM, see Amazon SageMaker AI LightGBM Distributed training using Dask.

LightGBM is a memory-bound (as opposed to compute-bound) algorithm. So, a general-purpose compute instance (for example, M5) is a better choice than a compute-optimized instance (for example, C5). Further, we recommend that you have enough total memory in selected instances to hold the training data.

The following table outlines a variety of sample notebooks that address different use cases of Amazon SageMaker AI LightGBM algorithm.

Tabular classification with Amazon SageMaker AI LightGBM and CatBoost algorithm

This notebook demonstrates the use of the Amazon SageMaker AI LightGBM algorithm to train and host a tabular classification model.

Tabular regression with Amazon SageMaker AI LightGBM and CatBoost algorithm

This notebook demonstrates the use of the Amazon SageMaker AI LightGBM algorithm to train and host a tabular regression model.

Amazon SageMaker AI LightGBM Distributed training using Dask

This notebook demonstrates distributed training with the Amazon SageMaker AI LightGBM algorithm using the Dask framework.

For instructions on how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, choose the SageMaker AI Examples tab to see a list of all of the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

**Examples:**

Example 1 (unknown):
```unknown
instance_count
```

---

## Perform exploratory data analysis (EDA)

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-analyses.html

**Contents:**
- Perform exploratory data analysis (EDA)
        - Note
- Get insights on data and data quality
        - To create a Data Quality and Insights report
        - Note
        - Topics
  - Summary
  - Target column
  - Quick model
  - Feature summary

Data Wrangler includes built-in analyses that help you generate visualizations and data analyses in a few clicks. You can also create custom analyses using your own code.

You add an analysis to a dataframe by selecting a step in your data flow, and then choosing Add analysis. To access an analysis you've created, select the step that contains the analysis, and select the analysis.

Analyses are generated using a sample of up to 200,000 rows of your dataset, and you can configure the sample size. For more information about changing the sample size of your data flow, see Edit the data flow sampling configuration.

Analyses are optimized for data with 1000 or fewer columns. You may experience some latency when generating analyses for data with additional columns.

You can add the following analysis to a dataframe:

Data visualizations, including histograms and scatter plots.

A quick summary of your dataset, including number of entries, minimum and maximum values (for numeric data), and most and least frequent categories (for categorical data).

A quick model of the dataset, which can be used to generate an importance score for each feature.

A target leakage report, which you can use to determine if one or more features are strongly correlated with your target feature.

A custom visualization using your own code.

Use the following sections to learn more about these options.

Use the Data Quality and Insights Report to perform an analysis of the data that you've imported into Data Wrangler. We recommend that you create the report after you import your dataset. You can use the report to help you clean and process your data. It gives you information such as the number of missing values and the number of outliers. If you have issues with your data, such as target leakage or imbalance, the insights report can bring those issues to your attention.

Use the following procedure to create a Data Quality and Insights report. It assumes that you've already imported a dataset into your Data Wrangler flow.

Choose the ellipsis icon next to a node in your Data Wrangler flow.

Select Get data insights.

For Analysis type, select Data Quality and Insights Report.

For Analysis name, specify a name for the insights report.

For Problem type, specify Regression or Classification.

For Target column, specify the target column.

For Data size, specify one of the following:

Sampled dataset – Uses the interactive sample from your data flow, which can contain up to 200,000 rows

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
'Hello_word'
```

Example 2 (unknown):
```unknown
import altair as alt
df = df.iloc[:30]
df = df.rename(columns={"Age": "value"})
df = df.assign(count=df.groupby('value').value.transform('count'))
df = df[["value", "count"]]
base = alt.Chart(df)
bar = base.mark_bar().encode(x=alt.X('value', bin=True, axis=None), y=alt.Y('count'))
rule = base.mark_rule(color='red').encode(
    x='mean(value):Q',
    size=alt.value(5))
chart = bar + rule
```

Example 3 (unknown):
```unknown
import altair as alt

# Specify the number of top rows for plotting
rows_number = 1000
df = df.head(rows_number)
# You can also choose bottom rows or randomly sampled rows
# df = df.tail(rows_number)
# df = df.sample(rows_number)


chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        # Specify the column names for binning and number of bins for X and Y axis
        x=alt.X("col1:Q", bin=alt.Bin(maxbins=20)),
        y=alt.Y("col2:Q", bin=alt.Bin(maxbins=20)),
        size="count()",
    )
)

# :Q specifies that label column has quantitative type.
# For more details on Altair typ
...
```

---

## Generative AI assistance for solving ML problems in Canvas using Amazon Q Developer

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-q.html#canvas-q-capabilities

**Contents:**
- Generative AI assistance for solving ML problems in Canvas using Amazon Q Developer
        - Note
- How it works
        - Important
- Supported regions
- Amazon Q Developer capabilities available in Canvas
- Prerequisites
        - Note
- Getting started

While using Amazon SageMaker Canvas, you can chat with Amazon Q Developer in natural language to leverage generative AI and solve problems. Q Developer is an assistant that helps you translate your goals into machine learning (ML) tasks and describes each step of the ML workflow. Q Developer helps Canvas users reduce the amount of time, effort, and data science expertise required to leverage ML and make data-driven decisions for their organizations.

Through a conversation with Q Developer, you can initiate actions in Canvas such as preparing data, building an ML model, making predictions, and deploying a model. Q Developer makes suggestions for next steps and provides you with context as you complete each step. It also informs you of results; for example, Canvas can transform your dataset according to best practices, and Q Developer can list the transforms that were used and why.

Amazon Q Developer is available in SageMaker Canvas at no additional cost to both Amazon Q Developer Pro Tier and Free Tier users. However, standard charges apply for resources such as the SageMaker Canvas workspace instance and any resources used for building or deploying models. For more information about pricing, see Amazon SageMaker Canvas pricing.

Use of Amazon Q is licensed to you under MIT's 0 License and subject to the AWS Responsible AI Policy. When you use Q Developer from outside the US, Q Developer processes data across US regions. For more information, see Cross region inference in Amazon Q Developer.

Amazon Q Developer in SageMaker Canvas doesn't use user content to improve the service, regardless of whether you use the Free-tier or Pro-tier subscription. For service telemetry purposes, Q Developer might track your usage, such as the number of questions asked and whether recommendations were accepted or rejected. This telemetry data doesn't include personally identifiable information such as IP address.

Amazon Q Developer is a generative AI powered assistant available in SageMaker Canvas that you can query using natural language. Q Developer makes suggestions for each step of the machine learning workflow, explaining concepts and providing you with options and more details as needed. You can use Q Developer for help with regression, binary classification, and multi-class classification use cases.

For example, to predict customer churn, upload a dataset of historical customer churn information to Canvas through Q Developer. Q Developer suggests an appropriate ML

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
number of valid values
```

Example 2 (unknown):
```unknown
feature type
```

Example 3 (unknown):
```unknown
standard deviation
```

Example 4 (unknown):
```unknown
25th percentile
```

---

## DeleteRecord

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_feature_store_DeleteRecord.html

**Contents:**
- DeleteRecord
- Request Syntax
- URI Request Parameters
- Request Body
- Response Syntax
- Response Elements
- Errors
- See Also

Deletes a Record from a FeatureGroup in the OnlineStore. Feature Store supports both SoftDelete and HardDelete. For SoftDelete (default), feature columns are set to null and the record is no longer retrievable by GetRecord or BatchGetRecord. For HardDelete, the complete Record is removed from the OnlineStore. In both cases, Feature Store appends the deleted record marker to the OfflineStore. The deleted record marker is a record with the same RecordIdentifer as the original, but with is_deleted value set to True, EventTime set to the delete input EventTime, and other feature values set to null.

Note that the EventTime specified in DeleteRecord should be set later than the EventTime of the existing record in the OnlineStore for that RecordIdentifer. If it is not, the deletion does not occur:

For SoftDelete, the existing (not deleted) record remains in the OnlineStore, though the delete record marker is still written to the OfflineStore.

HardDelete returns EventTime: 400 ValidationException to indicate that the delete operation failed. No delete record marker is written to the OfflineStore.

When a record is deleted from the OnlineStore, the deleted record marker is appended to the OfflineStore. If you have the Iceberg table format enabled for your OfflineStore, you can remove all history of a record from the OfflineStore using Amazon Athena or Apache Spark. For information on how to hard delete a record from the OfflineStore with the Iceberg table format enabled, see Delete records from the offline store.

The request uses the following URI parameters.

The name of the deletion mode for deleting the record. By default, the deletion mode is set to SoftDelete.

Valid Values: SoftDelete | HardDelete

Timestamp indicating when the deletion event occurred. EventTime can be used to query data at a certain point in time.

Length Constraints: Maximum length of 358400.

The name or Amazon Resource Name (ARN) of the feature group to delete the record from.

Length Constraints: Minimum length of 1. Maximum length of 150.

Pattern: (arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:feature-group/)?([a-zA-Z0-9]([-_]*[a-zA-Z0-9]){0,63})

The value for the RecordIdentifier that uniquely identifies the record, in string format.

Length Constraints: Maximum length of 358400.

A list of stores from which you're deleting the record. By default, Feature Store deletes the record from all of the stores that you're using for the FeatureGroup.

Array Members: Minimum number of 1 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
FeatureGroup
```

Example 2 (unknown):
```unknown
OnlineStore
```

Example 3 (unknown):
```unknown
BatchGetRecord
```

Example 4 (unknown):
```unknown
OnlineStore
```

---

## BlazingText algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/blazingtext.html

**Contents:**
- BlazingText algorithm
        - Topics
- Input/Output Interface for the BlazingText Algorithm
  - Training and Validation Data Format
    - Training and Validation Data Format for the Word2Vec Algorithm
    - Training and Validation Data Format for the Text Classification Algorithm
      - Train with File Mode
        - Note
      - Train with Augmented Manifest Text Format
  - Model Artifacts and Inference

The Amazon SageMaker AI BlazingText algorithm provides highly optimized implementations of the Word2vec and text classification algorithms. The Word2vec algorithm is useful for many downstream natural language processing (NLP) tasks, such as sentiment analysis, named entity recognition, machine translation, etc. Text classification is an important task for applications that perform web searches, information retrieval, ranking, and document classification.

The Word2vec algorithm maps words to high-quality distributed vectors. The resulting vector representation of a word is called a word embedding. Words that are semantically similar correspond to vectors that are close together. That way, word embeddings capture the semantic relationships between words.

Many natural language processing (NLP) applications learn word embeddings by training on large collections of documents. These pretrained vector representations provide information about semantics and word distributions that typically improves the generalizability of other models that are later trained on a more limited amount of data. Most implementations of the Word2vec algorithm are not optimized for multi-core CPU architectures. This makes it difficult to scale to large datasets.

With the BlazingText algorithm, you can scale to large datasets easily. Similar to Word2vec, it provides the Skip-gram and continuous bag-of-words (CBOW) training architectures. BlazingText's implementation of the supervised multi-class, multi-label text classification algorithm extends the fastText text classifier to use GPU acceleration with custom CUDA kernels. You can train a model on more than a billion words in a couple of minutes using a multi-core CPU or a GPU. And, you achieve performance on par with the state-of-the-art deep learning text classification algorithms.

The BlazingText algorithm is not parallelizable. For more information on parameters related to training, see Docker Registry Paths for SageMaker Built-in Algorithms.

The SageMaker AI BlazingText algorithms provides the following features:

Accelerated training of the fastText text classifier on multi-core CPUs or a GPU and Word2Vec on GPUs using highly optimized CUDA kernels. For more information, see BlazingText: Scaling and Accelerating Word2Vec using Multiple GPUs.

Enriched Word Vectors with Subword Information by learning vector representations for character n-grams. This approach enables BlazingText to generate meaningful vectors for out-of-vocab

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
batch_skipgram
```

Example 2 (unknown):
```unknown
batch_skipgram
```

Example 3 (unknown):
```unknown
Batch Skip-gram
```

Example 4 (unknown):
```unknown
Batch Skip-gram
```

---

## CreateProcessingJob

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateProcessingJob.html#API_CreateProcessingJob_SeeAlso

**Contents:**
- CreateProcessingJob
- Request Syntax
- Request Parameters
        - Important
        - Important
- Response Syntax
- Response Elements
- Errors
- See Also

Creates a processing job.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Configures the processing job to run a specified Docker container image.

Type: AppSpecification object

The environment variables to set in the Docker container. Up to 100 key and values entries in the map are supported.

Do not include any security-sensitive information including account access IDs, secrets, or tokens in any environment fields. As part of the shared responsibility model, you are responsible for any potential exposure, unauthorized access, or compromise of your sensitive data if caused by security-sensitive information included in the request environment variable or plain text fields.

Type: String to string map

Map Entries: Minimum number of 0 items. Maximum number of 100 items.

Key Length Constraints: Minimum length of 0. Maximum length of 256.

Key Pattern: [a-zA-Z_][a-zA-Z0-9_]*

Value Length Constraints: Minimum length of 0. Maximum length of 256.

Value Pattern: [\S\s]*

Associates a SageMaker job as a trial component with an experiment and trial. Specified when you call the following APIs:

Type: ExperimentConfig object

Networking options for a processing job, such as whether to allow inbound and outbound network calls to and from processing containers, and the VPC subnets and security groups to use for VPC-enabled processing jobs.

Type: NetworkConfig object

An array of inputs configuring the data to download into the processing container.

Type: Array of ProcessingInput objects

Array Members: Minimum number of 0 items. Maximum number of 10 items.

The name of the processing job. The name must be unique within an AWS Region in the AWS account.

Length Constraints: Minimum length of 1. Maximum length of 63.

Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

Output configuration for the processing job.

Type: ProcessingOutputConfig object

Identifies the resources, ML compute instances, and ML storage volumes to deploy for a processing job. In distributed training, you specify more than one instance.

Type: ProcessingResources object

The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.

Length Constraints: Minimum length of 20. Maximum length of 2048.

Pattern: arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+

The time limit for how long the processing job is allowed to run.

Type: ProcessingSto

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
   "AppSpecification": {
      "ContainerArguments": [ "string" ],
      "ContainerEntrypoint": [ "string" ],
      "ImageUri": "string"
   },
   "Environment": {
      "string" : "string"
   },
   "ExperimentConfig": {
      "ExperimentName": "string",
      "RunName": "string",
      "TrialComponentDisplayName": "string",
      "TrialName": "string"
   },
   "NetworkConfig": {
      "EnableInterContainerTrafficEncryption": boolean,
      "EnableNetworkIsolation": boolean,
      "VpcConfig": {
         "SecurityGroupIds": [ "string" ],
         "Subnets": [ "string" ]
      }
   },
   "Proc
...
```

Example 2 (unknown):
```unknown
[a-zA-Z_][a-zA-Z0-9_]*
```

Example 3 (unknown):
```unknown
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

Example 4 (unknown):
```unknown
arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+
```

---

## TabTransformer

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/tabtransformer.html

**Contents:**
- TabTransformer
- Amazon EC2 instance recommendation for the TabTransformer algorithm
- TabTransformer sample notebooks

TabTransformer is a novel deep tabular data modeling architecture for supervised learning. The TabTransformer architecture is built on self-attention-based Transformers. The Transformer layers transform the embeddings of categorical features into robust contextual embeddings to achieve higher prediction accuracy. Furthermore, the contextual embeddings learned from TabTransformer are highly robust against both missing and noisy data features, and provide better interpretability. This page includes information about Amazon EC2 instance recommendations and sample notebooks for TabTransformer.

SageMaker AI TabTransformer supports single-instance CPU and single-instance GPU training. Despite higher per-instance costs, GPUs train more quickly, making them more cost effective. To take advantage of GPU training, specify the instance type as one of the GPU instances (for example, P3). SageMaker AI TabTransformer currently does not support multi-GPU training.

The following table outlines a variety of sample notebooks that address different use cases of Amazon SageMaker AI TabTransformer algorithm.

Tabular classification with Amazon SageMaker AI TabTransformer algorithm

This notebook demonstrates the use of the Amazon SageMaker AI TabTransformer algorithm to train and host a tabular classification model.

Tabular regression with Amazon SageMaker AI TabTransformer algorithm

This notebook demonstrates the use of the Amazon SageMaker AI TabTransformer algorithm to train and host a tabular regression model.

For instructions on how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, choose the SageMaker AI Examples tab to see a list of all of the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

---

## Policies

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-operate-console-ui-governance-policies.html

**Contents:**
- Policies
- Sharing idle compute resources examples
        - Topics

Amazon SageMaker HyperPod task governance simplifies how your Amazon EKS cluster resources are allocated and how tasks are prioritized. The following provides information on HyperPod EKS cluster policies. For information on how to set up task governance, see Task governance setup.

The policies are divided up into Compute prioritization and Compute allocation. The policy concepts below will be organized in the context of these policies.

Compute prioritization, or cluster policy, determines how idle compute is borrowed and how tasks are prioritized by teams.

Idle compute allocation defines how idle compute is allocated across teams. That is, how unused compute can be borrowed from teams. When choosing an Idle compute allocation, you can choose between:

First-come first-serve: When applied, teams are not prioritized against each other and each incoming task is equally likely to obtain over-quota resources. Tasks are prioritized based on order of submission. This means a user may be able to use 100% of the idle compute if they request it first.

Fair-share: When applied, teams borrow idle compute based on their assigned Fair-share weight. These weights are defined in Compute allocation. For more information on how this can be used, see Sharing idle compute resources examples.

Task prioritization defines how tasks are queued as compute becomes available. When choosing a Task prioritization, you can choose between:

First-come first-serve: When applied, tasks are queued in the order they are requested.

Task ranking: When applied, tasks are queued in the order defined by their prioritization. If this option is chosen, you must add priority classes along with the weights at which they should be prioritized. Tasks of the same priority class will be executed on a first-come first-serve basis. When enabled in Compute allocation, tasks are preempted from lower priority tasks by higher priority tasks within the team.

When data scientists submit jobs to the cluster, they use the priority class name in the YAML file. The priority class is in the format priority-class-name-priority. For an example, see Submit a job to SageMaker AI-managed queue and namespace.

Priority classes: These classes establish a relative priority for tasks when borrowing capacity. When a task is running using borrowed quota, it may be preempted by another task of higher priority than it, if no more capacity is available for the incoming task. If Preemption is enabled in the Compute allocati

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
priority-class-name-priority
```

Example 2 (unknown):
```unknown
priority-class-name
```

Example 3 (unknown):
```unknown
hyperpod-ns-team-name
```

Example 4 (unknown):
```unknown
ml.c5.2xlarge
```

---

## CreateFeatureGroup

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateFeatureGroup.html

**Contents:**
- CreateFeatureGroup
        - Important
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

Create a new FeatureGroup. A FeatureGroup is a group of Features defined in the FeatureStore to describe a Record.

The FeatureGroup defines the schema and features contained in the FeatureGroup. A FeatureGroup definition is composed of a list of Features, a RecordIdentifierFeatureName, an EventTimeFeatureName and configurations for its OnlineStore and OfflineStore. Check AWS service quotas to see the FeatureGroups quota for your AWS account.

Note that it can take approximately 10-15 minutes to provision an OnlineStore FeatureGroup with the InMemory StorageType.

You must include at least one of OnlineStoreConfig and OfflineStoreConfig to create a FeatureGroup.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

A free-form description of a FeatureGroup.

Length Constraints: Minimum length of 0. Maximum length of 128.

The name of the feature that stores the EventTime of a Record in a FeatureGroup.

An EventTime is a point in time when a new event occurs that corresponds to the creation or update of a Record in a FeatureGroup. All Records in the FeatureGroup must have a corresponding EventTime.

An EventTime can be a String or Fractional.

Fractional: EventTime feature values must be a Unix timestamp in seconds.

String: EventTime feature values must be an ISO-8601 string in the format. The following formats are supported yyyy-MM-dd'T'HH:mm:ssZ and yyyy-MM-dd'T'HH:mm:ss.SSSZ where yyyy, MM, and dd represent the year, month, and day respectively and HH, mm, ss, and if applicable, SSS represent the hour, month, second and milliseconds respsectively. 'T' and Z are constants.

Length Constraints: Minimum length of 1. Maximum length of 64.

Pattern: [a-zA-Z0-9]([-_]*[a-zA-Z0-9]){0,63}

A list of Feature names and types. Name and Type is compulsory per Feature.

Valid feature FeatureTypes are Integral, Fractional and String.

FeatureNames cannot be any of the following: is_deleted, write_time, api_invocation_time

You can create up to 2,500 FeatureDefinitions per FeatureGroup.

Type: Array of FeatureDefinition objects

Array Members: Minimum number of 1 item. Maximum number of 2500 items.

The name of the FeatureGroup. The name must be unique within an AWS Region in an AWS account.

Must start with an alphanumeric character.

Can only include alphanumeric characters, underscores, and hyphens. Spaces are not allowed.

Length Constraints: Minimum length of 1. Maximum

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
FeatureGroup
```

Example 2 (unknown):
```unknown
FeatureGroup
```

Example 3 (unknown):
```unknown
FeatureStore
```

Example 4 (unknown):
```unknown
FeatureGroup
```

---

## CreateDomain

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateDomain.html

**Contents:**
- CreateDomain
        - Important
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

Creates a Domain. A domain consists of an associated Amazon Elastic File System volume, a list of authorized users, and a variety of security, application, policy, and Amazon Virtual Private Cloud (VPC) configurations. Users within a domain can share notebook files and other artifacts with each other.

When a domain is created, an EFS volume is created for use by all of the users within the domain. Each user receives a private home directory within the EFS volume for notebooks, Git repositories, and data files.

SageMaker AI uses the AWS Key Management Service (AWS KMS) to encrypt the EFS volume attached to the domain with an AWS managed key by default. For more control, you can specify a customer managed key. For more information, see Protect Data at Rest Using Encryption.

All traffic between the domain and the Amazon EFS volume is through the specified VPC and subnets. For other traffic, you can specify the AppNetworkAccessType parameter. AppNetworkAccessType corresponds to the network access type that you choose when you onboard to the domain. The following options are available:

PublicInternetOnly - Non-EFS traffic goes through a VPC managed by Amazon SageMaker AI, which allows internet access. This is the default value.

VpcOnly - All traffic is through the specified VPC and subnets. Internet access is disabled by default. To allow internet access, you must specify a NAT gateway.

When internet access is disabled, you won't be able to run a Amazon SageMaker AI Studio notebook or to train or host models unless your VPC has an interface endpoint to the SageMaker AI API and runtime or a NAT gateway and your security groups allow outbound connections.

NFS traffic over TCP on port 2049 needs to be allowed in both inbound and outbound rules in order to launch a Amazon SageMaker AI Studio app successfully.

For more information, see Connect Amazon SageMaker AI Studio Notebooks to Resources in a VPC.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Specifies the VPC used for non-EFS traffic. The default value is PublicInternetOnly.

PublicInternetOnly - Non-EFS traffic is through a VPC managed by Amazon SageMaker AI, which allows direct internet access

VpcOnly - All traffic is through the specified VPC and subnets

Valid Values: PublicInternetOnly | VpcOnly

The entity that creates and manages the required security groups for inter-app communication in VPC

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AppNetworkAccessType
```

Example 2 (unknown):
```unknown
AppNetworkAccessType
```

Example 3 (unknown):
```unknown
PublicInternetOnly
```

Example 4 (unknown):
```unknown
{
   "AppNetworkAccessType": "string",
   "AppSecurityGroupManagement": "string",
   "AuthMode": "string",
   "DefaultSpaceSettings": {
      "CustomFileSystemConfigs": [
         { ... }
      ],
      "CustomPosixUserConfig": {
         "Gid": number,
         "Uid": number
      },
      "ExecutionRole": "string",
      "JupyterLabAppSettings": {
         "AppLifecycleManagement": {
            "IdleSettings": {
               "IdleTimeoutInMinutes": number,
               "LifecycleManagement": "string",
               "MaxIdleTimeoutInMinutes": number,
               "MinIdleTimeoutInMinu
...
```

---

## Model Registry Collections

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/modelcollections.html

**Contents:**
- Model Registry Collections
        - Topics

You can use Collections to group registered models that are related to each other and organize them in hierarchies to improve model discoverability at scale. With Collections, you can organize registered models that are associated with one another. For example, you could categorize your models based on the domain of the problem they solve as Collections titled NLP-models, CV-models, or Speech-recognition-models. To organize your registered models in a tree structure, you can nest Collections within each other. Any operations you perform on a Collection, such as create, read, update, or delete, will not alter your registered models. You can use the Amazon SageMaker Studio UI or the Python SDK to manage your Collections.

The Collections tab in the Model Registry displays a list of all the Collections in your account. The following sections describe how you can use options in the Collections tab to do the following:

Add Model Groups to a Collection

Move Model Groups between Collections

Remove Model Groups or Collections from other Collections

Any operation you perform on your Collections does not affect the integrity of the individual Model Groups they contain—the underlying Model Group artifacts in Amazon S3 and Amazon ECR are not modified.

While Collections provide greater flexibility in organizing your models, the internal representation imposes some constraints on the size of your hierarchy. For a summary of these constraints, see Constraints.

The following topics show you how to create and work with Collections in the Model Registry.

Set up prerequisite permissions

Add Model Groups to a Collection

Remove Model Groups or Collections from a Collection

Move a Model Group Between Collections

View a Model Group's Parent Collection

---

## Latent Dirichlet Allocation (LDA) Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/lda.html

**Contents:**
- Latent Dirichlet Allocation (LDA) Algorithm
        - Topics
- Choosing between Latent Dirichlet Allocation (LDA) and Neural Topic Model (NTM)
        - Topics
- Input/Output Interface for the LDA Algorithm
- EC2 Instance Recommendation for the LDA Algorithm
- LDA Sample Notebooks

The Amazon SageMaker AI Latent Dirichlet Allocation (LDA) algorithm is an unsupervised learning algorithm that attempts to describe a set of observations as a mixture of distinct categories. LDA is most commonly used to discover a user-specified number of topics shared by documents within a text corpus. Here each observation is a document, the features are the presence (or occurrence count) of each word, and the categories are the topics. Since the method is unsupervised, the topics are not specified up front, and are not guaranteed to align with how a human may naturally categorize documents. The topics are learned as a probability distribution over the words that occur in each document. Each document, in turn, is described as a mixture of topics.

The exact content of two documents with similar topic mixtures will not be the same. But overall, you would expect these documents to more frequently use a shared subset of words, than when compared with a document from a different topic mixture. This allows LDA to discover these word groups and use them to form topics. As an extremely simple example, given a set of documents where the only words that occur within them are: eat, sleep, play, meow, and bark, LDA might produce topics like the following:

You can infer that documents that are more likely to fall into Topic 1 are about cats (who are more likely to meow and sleep), and documents that fall into Topic 2 are about dogs (who prefer to play and bark). These topics can be found even though the words dog and cat never appear in any of the texts.

Choosing between Latent Dirichlet Allocation (LDA) and Neural Topic Model (NTM)

Input/Output Interface for the LDA Algorithm

EC2 Instance Recommendation for the LDA Algorithm

Topic models are commonly used to produce topics from corpuses that (1) coherently encapsulate semantic meaning and (2) describe documents well. As such, topic models aim to minimize perplexity and maximize topic coherence.

Perplexity is an intrinsic language modeling evaluation metric that measures the inverse of the geometric mean per-word likelihood in your test data. A lower perplexity score indicates better generalization performance. Research has shown that the likelihood computed per word often does not align to human judgement, and can be entirely non-correlated, thus topic coherence has been introduced. Each inferred topic from your model consists of words, and topic coherence is computed to the top N words for that particular to

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 2 (unknown):
```unknown
application/json
```

Example 3 (unknown):
```unknown
application/x-recordio-protobuf
```

Example 4 (unknown):
```unknown
application/json
```

---

## Release Notes

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-release-notes.html

**Contents:**
- Release Notes

Data Wrangler is regularly updated with new features and bug fixes. To upgrade the version of Data Wrangler you are using in Studio Classic, follow the instructions in Shut Down and Update Amazon SageMaker Studio Classic Apps.

You can now create a Data Quality and Insights report on your entire dataset. For more information, see Get Insights On Data and Data Quality.

You can now import your data from Salesforce Data Cloud. For more information, see Import data from Salesforce Data Cloud.

You can now get your data in a format that Amazon Personalize can interpret. For more information, see Map Columns for Amazon Personalize.

You can now use Hive to import your data from Amazon EMR. For more information, see Import data from Amazon EMR.

You can now export your Data Wrangler flow to an inference endpoint. For more information, see Export to an Inference Endpoint.

You can now use an interactive notebook widget for data preparation. For more information, see Use an Interactive Data Preparation Widget in an Amazon SageMaker Studio Classic Notebook to Get Data Insights.

You can now import data from SaaS platforms. For more information, see Import Data From Software as a Service (SaaS) Platforms.

You can now reuse data flows for different data sets. For more information, see Reusing Data Flows for Different Datasets.

You can now use Principal Component Analysis (PCA) as a transform. For more information, see Reduce Dimensionality within a Dataset.

You can now refit parameters in your Data Wrangler flow. For more information, see Export.

You can now deploy models from your Data Wrangler flow. For more information, see Automatically Train Models on Your Data Flow.

You can now set data retention periods in Athena. For more information, see Import data from Athena.

You can now use Amazon SageMaker Autopilot to train a model directly from your Data Wrangler flow. For more information, see Automatically Train Models on Your Data Flow.

You can now use additional m5 and r5 instances. For more information, see Instances.

You can now get a data quality report. For more information, see Get Insights On Data and Data Quality

You can now perform random sampling and stratified sampling. For more information, see Sampling.

You can now use Databricks as a data source. For more information, see Import data from Databricks (JDBC).

You can now export using destination nodes. For more information, see Export

You can import ORC and JSON files. For more information a

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Extract using regex
```

---

## Amazon SageMaker HyperPod

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod.html

**Contents:**
- Amazon SageMaker HyperPod
- AWS Regions supported by SageMaker HyperPod
        - Topics

SageMaker HyperPod helps you provision resilient clusters for running machine learning (ML) workloads and developing state-of-the-art models such as large language models (LLMs), diffusion models, and foundation models (FMs). It accelerates development of FMs by removing undifferentiated heavy-lifting involved in building and maintaining large-scale compute clusters powered by thousands of accelerators such as AWS Trainium and NVIDIA A100 and H100 Graphical Processing Units (GPUs). When accelerators fail, the resiliency features of SageMaker HyperPod monitor the cluster instances automatically detect and replace the faulty hardware on the fly so that you can focus on running ML workloads.

To get started, check Prerequisites for using SageMaker HyperPod, set up AWS Identity and Access Management for SageMaker HyperPod, and choose one of the following orchestrator options supported by SageMaker HyperPod.

Slurm support in SageMaker HyperPod

SageMaker HyperPod provides support for running machine learning workloads on resilient clusters by integrating with Slurm, an open-source workload manager. Slurm support in SageMaker HyperPod enables seamless cluster orchestration through Slurm cluster configuration, allowing you to set up head, login, and worker nodes on the SageMaker HyperPod clusters This integration also facilitates Slurm-based job scheduling for running ML workloads on the cluster, as well as direct access to cluster nodes for job scheduling. With HyperPod's lifecycle configuration support, you can customize the computing environment of the clusters to meet your specific requirements. Additionally, by leveraging the Amazon SageMaker AI distributed training libraries, you can optimize the clusters' performance on AWS computing and network resources. To learn more, see Orchestrating SageMaker HyperPod clusters with Slurm.

Amazon EKS support in SageMaker HyperPod

SageMaker HyperPod also integrates with Amazon EKS to enable large-scale training of foundation models on long-running and resilient compute clusters. This allows cluster admin users to provision HyperPod clusters and attach them to an EKS control plane, enabling dynamic capacity management, direct access to cluster instances, and resiliency capabilities. For data scientists, Amazon EKS support in HyperPod allows running containerized workloads for training foundation models, inference on the EKS cluster, and leveraging the job auto-resume capability for Kubeflow PyTorch training. The arch

*[Content truncated]*

---

## Fairness, model explainability and bias detection with SageMaker Clarify

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-configure-processing-jobs.html#clarify-fairness-and-explainability

**Contents:**
- Fairness, model explainability and bias detection with SageMaker Clarify
- What is fairness and model explainability for machine learning predictions?
  - Best practices to evaluate fairness and explainability in the ML lifecycle
  - Guide to the SageMaker AI explanations and bias documentation
- How SageMaker Clarify Processing Jobs Work
- Sample notebooks
  - Getting started
  - Special cases

You can use Amazon SageMaker Clarify to understand fairness and model explainability and to explain and detect bias in your models. You can configure an SageMaker Clarify processing job to compute bias metrics and feature attributions and generate reports for model explainability. SageMaker Clarify processing jobs are implemented using a specialized SageMaker Clarify container image. The following page describes how SageMaker Clarify works and how to get started with an analysis.

Machine learning (ML) models are helping make decisions in domains including financial services, healthcare, education, and human resources. Policymakers, regulators, and advocates have raised awareness about the ethical and policy challenges posed by ML and data-driven systems. Amazon SageMaker Clarify can help you understand why your ML model made a specific prediction and whether this bias impacts this prediction during training or inference. SageMaker Clarify also provides tools that can help you build less biased and more understandable machine learning models. SageMaker Clarify can also generate model governance reports that you can provide to risk and compliance teams and external regulators. With SageMaker Clarify, you can do the following:

Detect bias in and help explain your model predictions.

Identify types of bias in pre-training data.

Identify types of bias in post-training data that can emerge during training or when your model is in production.

SageMaker Clarify helps explain how your models make predictions using feature attributions. It can also monitor inference models that are in production for both bias and feature attribution drift. This information can help you in the following areas:

Regulatory – Policymakers and other regulators can have concerns about discriminatory impacts of decisions that use output from ML models. For example, an ML model may encode bias and influence an automated decision.

Business – Regulated domains may need reliable explanations for how ML models make predictions. Model explainability may be particularly important to industries that depend on reliability, safety, and compliance. These can include financial services, human resources, healthcare, and automated transportation. For example, lending applications may need to provide explanations about how ML models made certain predictions to loan officers, forecasters, and customers.

Data Science – Data scientists and ML engineers can debug and improve ML models when they can de

*[Content truncated]*

---

## Amazon SageMaker AI domain entities and statuses

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sm-domain.html

**Contents:**
- Amazon SageMaker AI domain entities and statuses
- Maintenance of applications
        - Topics

Amazon SageMaker AI domain supports SageMaker AI machine learning (ML) environments. A SageMaker AI domain is composed of the following entities and their associated status values. For onboarding steps to create a domain, see Amazon SageMaker AI domain overview.

Domain: A domain consists of the following.

An associated Amazon Elastic File System (Amazon EFS) volume.

A list of authorized users.

A variety of security, application, policy, and Amazon Virtual Private Cloud (Amazon VPC) configurations.

Users within a domain can share notebook files and other artifacts with each other. An account can have multiple domains. For more information about multiple domains, see Multiple domains overview.

User profile: A user profile represents a single user within a domain. It is the main way to reference a user for the purposes of sharing, reporting, and other user-oriented features. This entity is created when a user onboards to the Amazon SageMaker AI domain. For more information about user profiles, see Domain user profiles.

Shared space: A shared space consists of a shared JupyterServer application and shared directory. All users within the domain have access to the shared space. All user profiles in a domain have access to all shared spaces in the domain. For more information about shared spaces, see Collaboration with shared spaces.

App: An app represents an application that supports the reading and execution experience of the user’s notebooks, terminals, and consoles. The type of app can be JupyterServer, KernelGateway, RStudioServerPro, or RSession. A user may have multiple apps active simultaneously.

The following tables describe the status values for the domain, UserProfile, shared space, and App entities. Where applicable, they also give troubleshooting steps.

UserProfile status values

shared space status values

At least once every 90 days, SageMaker AI performs security and performance updates to the underlying software for Amazon SageMaker Studio Classic JupyterServer and KernelGateway, SageMaker Canvas, and Amazon SageMaker Data Wrangler applications. Some maintenance items, such as operating system upgrades, require that SageMaker AI takes your application offline for a short time during the maintenance window. Because this maintenance takes the application offline, you cannot perform any operations while the underlying software is being updated. When the maintenance activity is in progress, the state of the application transitions from InSe

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
UserProfile
```

Example 2 (unknown):
```unknown
shared space
```

Example 3 (unknown):
```unknown
DescribeDomain
```

Example 4 (unknown):
```unknown
FailureReason
```

---

## Amazon SageMaker Partner AI Apps overview

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/partner-apps.html

**Contents:**
- Amazon SageMaker Partner AI Apps overview
- How it works
- Integration with AWS services
- Supported types
        - Note

With Amazon SageMaker Partner AI Apps, users get access to generative AI and machine learning (ML) development applications built, published, and distributed by industry-leading application providers. Partner AI Apps are certified to run on SageMaker AI. With Partner AI Apps, users can accelerate and improve how they build solutions based on foundation models (FM) and classic ML models without compromising the security of their sensitive data. The data stays completely within their trusted security configuration and is never shared with a third party.

Partner AI Apps are full application stacks that include an Amazon Elastic Kubernetes Service cluster and an array of accompanying services that can include Application Load Balancer, Amazon Relational Database Service, Amazon Simple Storage Service buckets, Amazon Simple Queue Service queues, and Redis caches.

These service applications can be shared across all users in a SageMaker AI domain and are provisioned by an admin. After provisioning the application by purchasing a subscription through the AWS Marketplace, the admin can give users in the SageMaker AI domain permissions to access the Partner AI App directly from Amazon SageMaker Studio, Amazon SageMaker Unified Studio (preview), or using a pre-signed URL. For information about launching an application from Studio, see Launch Amazon SageMaker Studio.

Partner AI Apps offers the following benefits for administrators and users.

Administrators use the SageMaker AI console to browse, discover, select, and provision the Partner AI Apps for use by their data science and ML teams. After the Partner AI Apps are deployed, SageMaker AI runs them on service-managed AWS accounts. This significantly reduces the operational overhead associated with building and operating these applications, and contributes to the security and privacy of customer data.

Data scientists and ML developers can access Partner AI Apps from within their ML development environment in Amazon SageMaker Studio or Amazon SageMaker Unified Studio (preview). They can use the Partner AI Apps to analyze their data, experiments, and models created on SageMaker AI. This minimizes context switching and helps accelerate building foundation models and bringing new generative AI capabilities to market.

Partner AI Apps uses the existing AWS Identity and Access Management (IAM) configuration for authorization and authentication. As a result, users don’t need to provide separate credentials to access e

*[Content truncated]*

---

## Fairness, model explainability and bias detection with SageMaker Clarify

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-configure-processing-jobs.html

**Contents:**
- Fairness, model explainability and bias detection with SageMaker Clarify
- What is fairness and model explainability for machine learning predictions?
  - Best practices to evaluate fairness and explainability in the ML lifecycle
  - Guide to the SageMaker AI explanations and bias documentation
- How SageMaker Clarify Processing Jobs Work
- Sample notebooks
  - Getting started
  - Special cases

You can use Amazon SageMaker Clarify to understand fairness and model explainability and to explain and detect bias in your models. You can configure an SageMaker Clarify processing job to compute bias metrics and feature attributions and generate reports for model explainability. SageMaker Clarify processing jobs are implemented using a specialized SageMaker Clarify container image. The following page describes how SageMaker Clarify works and how to get started with an analysis.

Machine learning (ML) models are helping make decisions in domains including financial services, healthcare, education, and human resources. Policymakers, regulators, and advocates have raised awareness about the ethical and policy challenges posed by ML and data-driven systems. Amazon SageMaker Clarify can help you understand why your ML model made a specific prediction and whether this bias impacts this prediction during training or inference. SageMaker Clarify also provides tools that can help you build less biased and more understandable machine learning models. SageMaker Clarify can also generate model governance reports that you can provide to risk and compliance teams and external regulators. With SageMaker Clarify, you can do the following:

Detect bias in and help explain your model predictions.

Identify types of bias in pre-training data.

Identify types of bias in post-training data that can emerge during training or when your model is in production.

SageMaker Clarify helps explain how your models make predictions using feature attributions. It can also monitor inference models that are in production for both bias and feature attribution drift. This information can help you in the following areas:

Regulatory – Policymakers and other regulators can have concerns about discriminatory impacts of decisions that use output from ML models. For example, an ML model may encode bias and influence an automated decision.

Business – Regulated domains may need reliable explanations for how ML models make predictions. Model explainability may be particularly important to industries that depend on reliability, safety, and compliance. These can include financial services, human resources, healthcare, and automated transportation. For example, lending applications may need to provide explanations about how ML models made certain predictions to loan officers, forecasters, and customers.

Data Science – Data scientists and ML engineers can debug and improve ML models when they can de

*[Content truncated]*

---

## K-Nearest Neighbors (k-NN) Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/k-nearest-neighbors.html

**Contents:**
- K-Nearest Neighbors (k-NN) Algorithm
        - Topics
- Input/Output Interface for the k-NN Algorithm
- k-NN Sample Notebooks
- EC2 Instance Recommendation for the k-NN Algorithm

Amazon SageMaker AI k-nearest neighbors (k-NN) algorithm is an index-based algorithm. It uses a non-parametric method for classification or regression. For classification problems, the algorithm queries the k points that are closest to the sample point and returns the most frequently used label of their class as the predicted label. For regression problems, the algorithm queries the k closest points to the sample point and returns the average of their feature values as the predicted value.

Training with the k-NN algorithm has three steps: sampling, dimension reduction, and index building. Sampling reduces the size of the initial dataset so that it fits into memory. For dimension reduction, the algorithm decreases the feature dimension of the data to reduce the footprint of the k-NN model in memory and inference latency. We provide two methods of dimension reduction methods: random projection and the fast Johnson-Lindenstrauss transform. Typically, you use dimension reduction for high-dimensional (d >1000) datasets to avoid the “curse of dimensionality” that troubles the statistical analysis of data that becomes sparse as dimensionality increases. The main objective of k-NN's training is to construct the index. The index enables efficient lookups of distances between points whose values or class labels have not yet been determined and the k nearest points to use for inference.

Input/Output Interface for the k-NN Algorithm

k-NN Sample Notebooks

How the k-NN Algorithm Works

EC2 Instance Recommendation for the k-NN Algorithm

Data Formats for k-NN Training Input

k-NN Request and Response Formats

SageMaker AI k-NN supports train and test data channels.

Use a train channel for data that you want to sample and construct into the k-NN index.

Use a test channel to emit scores in log files. Scores are listed as one line per mini-batch: accuracy for classifier, mean-squared error (mse) for regressor for score.

For training inputs, k-NN supports text/csv and application/x-recordio-protobuf data formats. For input type text/csv, the first label_size columns are interpreted as the label vector for that row. You can use either File mode or Pipe mode to train models on data that is formatted as recordIO-wrapped-protobuf or as CSV.

For inference inputs, k-NN supports the application/json, application/x-recordio-protobuf, and text/csv data formats. The text/csv format accepts a label_size and encoding parameter. It assumes a label_size of 0 and a UTF-8 encoding.


*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application/x-recordio-protobuf
```

Example 2 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 3 (unknown):
```unknown
application/json
```

Example 4 (unknown):
```unknown
application/x-recordio-protobuf
```

---

## Export

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-data-export.html

**Contents:**
- Export
        - Important
- Export to Amazon S3
        - Note
        - Note
        - Note
        - Important
- Export to Pipelines
  - Use a Jupyter Notebook to Create a Pipeline
- Export to an Inference Endpoint

In your Data Wrangler flow, you can export some or all of the transformations that you've made to your data processing pipelines.

A Data Wrangler flow is the series of data preparation steps that you've performed on your data. In your data preparation, you perform one or more transformations to your data. Each transformation is done using a transform step. The flow has a series of nodes that represent the import of your data and the transformations that you've performed. For an example of nodes, see the following image.

The preceding image shows a Data Wrangler flow with two nodes. The Source - sampled node shows the data source from which you've imported your data. The Data types node indicates that Data Wrangler has performed a transformation to convert the dataset into a usable format.

Each transformation that you add to the Data Wrangler flow appears as an additional node. For information on the transforms that you can add, see Transform Data. The following image shows a Data Wrangler flow that has a Rename-column node to change the name of a column in a dataset.

You can export your data transformations to the following:

Amazon SageMaker Feature Store

We recommend that you use the IAM AmazonSageMakerFullAccess managed policy to grant AWS permission to use Data Wrangler. If you don't use the managed policy, you can use an IAM policy that gives Data Wrangler access to an Amazon S3 bucket. For more information on the policy, see Security and Permissions.

When you export your data flow, you're charged for the AWS resources that you use. You can use cost allocation tags to organize and manage the costs of those resources. You create these tags for your user-profile and Data Wrangler automatically applies them to the resources used to export the data flow. For more information, see Using Cost Allocation Tags.

Data Wrangler gives you the ability to export your data to a location within an Amazon S3 bucket. You can specify the location using one of the following methods:

Destination node – Where Data Wrangler stores the data after it has processed it.

Export to – Exports the data resulting from a transformation to Amazon S3.

Export data – For small datasets, can quickly export the data that you've transformed.

Use the following sections to learn more about each of these methods.

If you want to output a series of data processing steps that you've performed to Amazon S3, you create a destination node. A destination node tells Data Wrangler where to 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
AmazonSageMakerFullAccess
```

Example 2 (unknown):
```unknown
output_content_type
```

Example 3 (unknown):
```unknown
compression
```

Example 4 (unknown):
```unknown
num_partitions
```

---

## Amazon SageMaker Role Manager

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/role-manager.html

**Contents:**
- Amazon SageMaker Role Manager
        - Topics

Machine learning (ML) administrators striving for least-privilege permissions with Amazon SageMaker AI must account for a diversity of industry perspectives, including the unique least-privilege access needs required for personas such as data scientists, machine learning operation (MLOps) engineers, and more. Use Amazon SageMaker Role Manager to build and manage persona-based IAM roles for common machine learning needs directly through the Amazon SageMaker AI console.

Amazon SageMaker Role Manager provides 3 preconfigured role personas and predefined permissions for common ML activities. Explore the provided personas and their suggested policies, or create and maintain roles for personas unique to your business needs. If you require additional customization, specify networking and encryption permissions for Amazon Virtual Private Cloud resources and AWS Key Management Service encryption keys in Step 1. Enter role information of the Amazon SageMaker Role Manager.

Using the role manager (console)

Using the role manager (AWS CDK)

ML activity reference

Launch Studio Classic

---

## Random Cut Forest (RCF) Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/randomcutforest.html

**Contents:**
- Random Cut Forest (RCF) Algorithm
        - Topics
- Input/Output Interface for the RCF Algorithm
        - Note
- Instance Recommendations for the RCF Algorithm
- RCF Sample Notebooks

Amazon SageMaker AI Random Cut Forest (RCF) is an unsupervised algorithm for detecting anomalous data points within a data set. These are observations which diverge from otherwise well-structured or patterned data. Anomalies can manifest as unexpected spikes in time series data, breaks in periodicity, or unclassifiable data points. They are easy to describe in that, when viewed in a plot, they are often easily distinguishable from the "regular" data. Including these anomalies in a data set can drastically increase the complexity of a machine learning task since the "regular" data can often be described with a simple model.

With each data point, RCF associates an anomaly score. Low score values indicate that the data point is considered "normal." High values indicate the presence of an anomaly in the data. The definitions of "low" and "high" depend on the application but common practice suggests that scores beyond three standard deviations from the mean score are considered anomalous.

While there are many applications of anomaly detection algorithms to one-dimensional time series data such as traffic volume analysis or sound volume spike detection, RCF is designed to work with arbitrary-dimensional input. Amazon SageMaker AI RCF scales well with respect to number of features, data set size, and number of instances.

Input/Output Interface for the RCF Algorithm

Instance Recommendations for the RCF Algorithm

Amazon SageMaker AI Random Cut Forest supports the train and test data channels. The optional test channel is used to compute accuracy, precision, recall, and F1-score metrics on labeled data. Train and test data content types can be either application/x-recordio-protobuf or text/csv formats. For the test data, when using text/csv format, the content must be specified as text/csv;label_size=1 where the first column of each row represents the anomaly label: "1" for an anomalous data point and "0" for a normal data point. You can use either File mode or Pipe mode to train RCF models on data that is formatted as recordIO-wrapped-protobuf or as CSV

The train channel only supports S3DataDistributionType=ShardedByS3Key and the test channel only supports S3DataDistributionType=FullyReplicated. The following example specifies the S3 distribution type for the train channel using the Amazon SageMaker Python SDK.

The sagemaker.inputs.s3_input method was renamed to sagemaker.inputs.TrainingInput in SageMaker Python SDK v2.

To avoid common errors around executi

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application/x-recordio-protobuf
```

Example 2 (unknown):
```unknown
recordIO-wrapped-protobuf
```

Example 3 (unknown):
```unknown
S3DataDistributionType=ShardedByS3Key
```

Example 4 (unknown):
```unknown
S3DataDistributionType=FullyReplicated
```

---

## Walk Through a SageMaker AI MLOps Project Using Third-party Git Repos

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-walkthrough-3rdgit.html

**Contents:**
- Walk Through a SageMaker AI MLOps Project Using Third-party Git Repos
        - Important
        - Topics
- Step 1: Set up the GitHub connection
        - To set up the GitHub connection:
- Step 2: Create the Project
        - To create the SageMaker AI MLOps project
- Step 3: Make a Change in the Code
        - To make a code change
- Step 4: Approve the Model

As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The following section is specific to using the Studio Classic application. For information about using the updated Studio experience, see Amazon SageMaker Studio.

Studio Classic is still maintained for existing workloads but is no longer available for onboarding. You can only stop or delete existing Studio Classic applications and cannot create new ones. We recommend that you migrate your workload to the new Studio experience.

This walkthrough uses the template MLOps templates for model building, training, and deployment with third-party Git using CodePipeline to demonstrate how to use MLOps projects to create a CI/CD system to build, train, and deploy models.

To complete this walkthrough, you need:

An IAM or IAM Identity Center account to sign in to Studio Classic. For information, see Amazon SageMaker AI domain overview.

Permission to use SageMaker AI-provided project templates. For information, see Granting SageMaker Studio Permissions Required to Use Projects.

Basic familiarity with the Studio Classic user interface. For information, see Amazon SageMaker Studio Classic UI Overview.

Two empty GitHub repositories. You input these repositories into the project template, which will seed these repos with model build and deploy code.

Step 1: Set up the GitHub connection

Step 2: Create the Project

Step 3: Make a Change in the Code

Step 4: Approve the Model

(Optional) Step 5: Deploy the Model Version to Production

Step 6: Clean Up Resources

In this step, you connect to your GitHub repositories using an AWS CodeConnections connection. The SageMaker AI project uses this connection to access your source code repositories.

Log in to the CodePipeline console at https://console.aws.amazon.com/codepipeline/

Under Settings in the navigation pane, choose Connections.

Choose Create connection.

For Select a provider, select GitHub.

For Connection name, enter a name.

Choose Connect to GitHub.

If the AWS Connector GitHub app isn’t previously installed, choose Install new app.

This displays a list of all the GitHub personal accounts and organizations to which you have access.

Choose the account where you want to establish connectivity for use with SageMaker Projects and GitHub repositories.

You can optionally select your specific repositories or choose All repositories.

Choose Save. When the app is installed, you’re redirected to th

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
username/repository
                                    name
```

Example 2 (unknown):
```unknown
organization/repository
                                    name
```

Example 3 (unknown):
```unknown
username/repository
                                    name
```

Example 4 (unknown):
```unknown
organization/repository
                                    name
```

---

## Semantic Segmentation Algorithm

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/semantic-segmentation.html

**Contents:**
- Semantic Segmentation Algorithm
        - Topics
- Semantic Segmentation Sample Notebooks
- Input/Output Interface for the Semantic Segmentation Algorithm
  - How Training Works
  - Training with the Augmented Manifest Format
  - Incremental Training
  - Produce Inferences
- EC2 Instance Recommendation for the Semantic Segmentation Algorithm

The SageMaker AI semantic segmentation algorithm provides a fine-grained, pixel-level approach to developing computer vision applications. It tags every pixel in an image with a class label from a predefined set of classes. Tagging is fundamental for understanding scenes, which is critical to an increasing number of computer vision applications, such as self-driving vehicles, medical imaging diagnostics, and robot sensing.

For comparison, the SageMaker AI Image Classification - MXNet is a supervised learning algorithm that analyzes only whole images, classifying them into one of multiple output categories. The Object Detection - MXNet is a supervised learning algorithm that detects and classifies all instances of an object in an image. It indicates the location and scale of each object in the image with a rectangular bounding box.

Because the semantic segmentation algorithm classifies every pixel in an image, it also provides information about the shapes of the objects contained in the image. The segmentation output is represented as a grayscale image, called a segmentation mask. A segmentation mask is a grayscale image with the same shape as the input image.

The SageMaker AI semantic segmentation algorithm is built using the MXNet Gluon framework and the Gluon CV toolkit. It provides you with a choice of three built-in algorithms to train a deep neural network. You can use the Fully-Convolutional Network (FCN) algorithm , Pyramid Scene Parsing (PSP) algorithm, or DeepLabV3.

Each of the three algorithms has two distinct components:

The backbone (or encoder)—A network that produces reliable activation maps of features.

The decoder—A network that constructs the segmentation mask from the encoded activation maps.

You also have a choice of backbones for the FCN, PSP, and DeepLabV3 algorithms: ResNet50 or ResNet101. These backbones include pretrained artifacts that were originally trained on the ImageNet classification task. You can fine-tune these backbones for segmentation using your own data. Or, you can initialize and train these networks from scratch using only your own data. The decoders are never pretrained.

To deploy the trained model for inference, use the SageMaker AI hosting service. During inference, you can request the segmentation mask either as a PNG image or as a set of probabilities for each class for each pixel. You can use these masks as part of a larger pipeline that includes additional downstream image processing or other applicatio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
application/x-image
```

Example 2 (unknown):
```unknown
train_annotation
```

Example 3 (unknown):
```unknown
validation_annotation
```

Example 4 (unknown):
```unknown
label_map.json
```

---

## Throughput modes

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-throughput-mode.html

**Contents:**
- Throughput modes
        - Topics
- On-demand throughput mode
        - Important
- Provisioned throughput mode
        - Important
- Throughput mode metrics
- Throughput mode limits

Amazon SageMaker Feature Store provides two pricing models to choose from: on-demand (On-demand) and provisioned (Provisioned) throughput modes. On-demand works best for less predictable traffic, while Provisioned works best for consistent and predictable traffic.

You have the option to switch between On-demand and Provisioned throughput modes for a given feature group, to accommodate periods in which application traffic patterns are changing or less predictable. You can only update your feature group throughput mode to On-demand once in a 24 hour period. The throughput mode can be updated programmatically using the UpdateFeatureGroup API or through the console UI. For more information about using the console, see Using Amazon SageMaker Feature Store in the console.

You can use the Provisioned throughput mode with offline-only feature groups or feature groups with the Standard storage type. For other storage configurations, the On-demand throughput mode is used. For information about the online and offline storage configurations, see Online store and Offline store, respectively.

For more details about pricing, see Amazon SageMaker Pricing.

On-demand throughput mode

Provisioned throughput mode

Throughput mode metrics

Throughput mode limits

The On-demand (default) throughput mode works best when you are using feature groups with unknown workload, unpredictable application traffic, and you cannot forecast the capacity requirements.

The On-demand mode charges you for the reads and writes that your application performs on your feature groups. You do not need to specify how much read and write throughput you expect your application to perform because Feature Store instantly accommodates your workloads as they ramp up or down. You pay only for what you use, which is measured in ReadRequestsUnits and WriteRequestsUnits.

You can enable the On-demand throughput mode using the CreateFeatureGroup or UpdateFeatureGroup APIs or through the console UI. For more information about using the console UI, see Using Amazon SageMaker Feature Store in the console.

You can only update your feature group throughput mode to On-demand once in a 24 hour period.

The Provisioned throughput mode works best when you are using feature groups with predictable workloads and you can forecast the capacity requirements to control costs. This can make it more cost effective for certain workloads where you can anticipate throughput requirements in advance.

When you set a feature gro

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Provisioned
```

Example 2 (unknown):
```unknown
Provisioned
```

Example 3 (unknown):
```unknown
Provisioned
```

Example 4 (unknown):
```unknown
Provisioned
```

---

## DescribeDomain

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_DescribeDomain.html

**Contents:**
- DescribeDomain
- Request Syntax
- Request Parameters
- Response Syntax
- Response Elements
- Errors
- See Also

The description of the domain.

For information about the parameters that are common to all actions, see Common Parameters.

The request accepts the following data in JSON format.

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: d-(-*[a-z0-9]){1,61}

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

Specifies the VPC used for non-EFS traffic. The default value is PublicInternetOnly.

PublicInternetOnly - Non-EFS traffic is through a VPC managed by Amazon SageMaker AI, which allows direct internet access

VpcOnly - All traffic is through the specified VPC and subnets

Valid Values: PublicInternetOnly | VpcOnly

The entity that creates and manages the required security groups for inter-app communication in VPCOnly mode. Required when CreateDomain.AppNetworkAccessType is VPCOnly and DomainSettings.RStudioServerProDomainSettings.DomainExecutionRoleArn is provided.

Valid Values: Service | Customer

The domain's authentication mode.

Valid Values: SSO | IAM

The default settings for shared spaces that users create in the domain.

Type: DefaultSpaceSettings object

Settings which are applied to UserProfiles in this domain if settings are not explicitly specified in a given UserProfile.

Type: UserSettings object

The domain's Amazon Resource Name (ARN).

Length Constraints: Minimum length of 0. Maximum length of 256.

Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:domain/.*

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: d-(-*[a-z0-9]){1,61}

Length Constraints: Minimum length of 0. Maximum length of 63.

Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

A collection of Domain settings.

Type: DomainSettings object

Length Constraints: Minimum length of 0. Maximum length of 1024.

The ID of the Amazon Elastic File System managed by this Domain.

Length Constraints: Minimum length of 0. Maximum length of 32.

This parameter has been deprecated.

Length Constraints: Minimum length of 0. Maximum length of 2048.

Pattern: [a-zA-Z0-9:/_-]*

The AWS KMS customer managed key used to encrypt the EFS volume attached to the domain.

Length Constraints: Minimum length of 0. Maximum length of 2048.

Pattern: [a-zA-Z0-9:/_-]*

The last modified time.

The ID of the security group that authorizes traffic between the RSessionGateway apps and the RStudioServerPro app.

Length Constraints: Minimum length of 0. Maximum length of 32.

Patter

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{
   "DomainId": "string"
}
```

Example 2 (unknown):
```unknown
d-(-*[a-z0-9]){1,61}
```

Example 3 (unknown):
```unknown
{
   "AppNetworkAccessType": "string",
   "AppSecurityGroupManagement": "string",
   "AuthMode": "string",
   "CreationTime": number,
   "DefaultSpaceSettings": {
      "CustomFileSystemConfigs": [
         { ... }
      ],
      "CustomPosixUserConfig": {
         "Gid": number,
         "Uid": number
      },
      "ExecutionRole": "string",
      "JupyterLabAppSettings": {
         "AppLifecycleManagement": {
            "IdleSettings": {
               "IdleTimeoutInMinutes": number,
               "LifecycleManagement": "string",
               "MaxIdleTimeoutInMinutes": number,
         
...
```

Example 4 (unknown):
```unknown
PublicInternetOnly
```

---
