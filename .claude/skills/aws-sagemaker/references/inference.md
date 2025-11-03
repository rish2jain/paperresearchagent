# Aws-Sagemaker - Inference

**Pages:** 12

---

## Amazon SageMaker Inference Recommender

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/inference-recommender.html

**Contents:**
- Amazon SageMaker Inference Recommender
- How it Works
- How to Get Started
- Example notebooks

Amazon SageMaker Inference Recommender is a capability of Amazon SageMaker AI. It reduces the time required to get machine learning (ML) models in production by automating load testing and model tuning across SageMaker AI ML instances. You can use Inference Recommender to deploy your model to a real-time or serverless inference endpoint that delivers the best performance at the lowest cost. Inference Recommender helps you select the best instance type and configuration for your ML models and workloads. It considers factors like instance count, container parameters, model optimizations, max concurrency, and memory size.

Amazon SageMaker Inference Recommender only charges you for the instances used while your jobs are executing.

To use Amazon SageMaker Inference Recommender, you can either create a SageMaker AI model or register a model to the SageMaker Model Registry with your model artifacts. Use the AWS SDK for Python (Boto3) or the SageMaker AI console to run benchmarking jobs for different SageMaker AI endpoint configurations. Inference Recommender jobs help you collect and visualize metrics across performance and resource utilization to help you decide on which endpoint type and configuration to choose.

If you are a first-time user of Amazon SageMaker Inference Recommender, we recommend that you do the following:

Read through the Prerequisites for using Amazon SageMaker Inference Recommender section to make sure you have satisfied the requirements to use Amazon SageMaker Inference Recommender.

Read through the Recommendation jobs with Amazon SageMaker Inference Recommender section to launch your first Inference Recommender recommendation jobs.

Explore the introductory Amazon SageMaker Inference Recommender Jupyter notebook example, or review the example notebooks in the following section.

The following example Jupyter notebooks can help you with the workflows for multiple use cases in Inference Recommender:

If you want an introductory notebook that benchmarks a TensorFlow model, see the SageMaker Inference Recommender TensorFlow notebook.

If you want to benchmark a HuggingFace model, see the SageMaker Inference Recommender for HuggingFace notebook.

If you want to benchmark an XGBoost model, see the SageMaker Inference Recommender XGBoost notebook.

If you want to review CloudWatch metrics for your Inference Recommender jobs, see the SageMaker Inference Recommender CloudWatch metrics notebook.

---

## Deploy models for inference

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html

**Contents:**
- Deploy models for inference
- Choosing a feature
  - Use cases
  - Recommended features
  - Additional options

With Amazon SageMaker AI, you can start getting predictions, or inferences, from your trained machine learning models. SageMaker AI provides a broad selection of ML infrastructure and model deployment options to help meet all your ML inference needs. With SageMaker AI Inference, you can scale your model deployment, manage models more effectively in production, and reduce operational burden. SageMaker AI provides you with various inference options, such as real-time endpoints for getting low latency inference, serverless endpoints for fully managed infrastructure and auto-scaling, and asynchronous endpoints for batches of requests. By leveraging the appropriate inference option for your use case, you can ensure efficient model deployment and inference.

There are several use cases for deploying ML models with SageMaker AI. This section describes those use cases, as well as the SageMaker AI feature we recommend for each use case.

The following are the main uses cases for deploying ML models with SageMaker AI.

Use case 1: Deploy a machine learning model in a low-code or no-code environment. For beginners or those new to SageMaker AI, you can deploy pre-trained models using Amazon SageMaker JumpStart through the Amazon SageMaker Studio interface, without the need for complex configurations.

Use case 2: Use code to deploy machine learning models with more flexibility and control. Experienced ML practitioners can deploy their own models with customized settings for their application needs using the ModelBuilder class in the SageMaker AI Python SDK, which provides fine-grained control over various settings, such as instance types, network isolation, and resource allocation.

Use case 3: Deploy machine learning models at scale. For advanced users and organizations who want to manage models at scale in production, use the AWS SDK for Python (Boto3) and AWS CloudFormation along with your desired Infrastructure as Code (IaC) and CI/CD tools to provision resources and automate resource management.

The following table describes key considerations and tradeoffs for SageMaker AI features corresponding with each use case.

SageMaker AI provides different options for your inference use cases, giving you choice over the technical breadth and depth of your deployments:

Deploying a model to an endpoint. When deploying your model, consider the following options:

Real-time inference. Real-time inference is ideal for inference workloads where you have interactive, low late

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

---

## Amazon SageMaker Model Dashboard

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-dashboard.html

**Contents:**
- Amazon SageMaker Model Dashboard
- Model Dashboard elements

Amazon SageMaker Model Dashboard is a centralized portal, accessible from the SageMaker AI console, where you can view, search, and explore all of the models in your account. You can track which models are deployed for inference and if they are used in batch transform jobs or hosted on endpoints. If you set up monitors with Amazon SageMaker Model Monitor, you can also track the performance of your models as they make real-time predictions on live data. You can use the dashboard to find models that violate thresholds you set for data quality, model quality, bias and explainability. The dashboard’s comprehensive presentation of all your monitor results helps you quickly identify models that don’t have these metrics configured.

The Model Dashboard aggregates model-related information from several SageMaker AI features. In addition to the services provided in Model Monitor, you can view model cards, visualize workflow lineage, and track your endpoint performance. You no longer have to sort through logs, query in notebooks, or access other AWS services to collect the data you need. With a cohesive user experience and integration into existing services, SageMaker AI’s Model Dashboard provides an out-of-the-box model governance solution to help you ensure quality coverage across all your models.

To use the Model Dashboard, you should have one or more models in your account. You can train models using Amazon SageMaker AI or import models you've trained elsewhere. To create a model in SageMaker AI, you can use the CreateModel API. For more information, see CreateModel. You can also use SageMaker AI-provided ML environments, such as Amazon SageMaker Studio Classic, which provides project templates that set up model training and deployment for you. For information about how to get started with Studio Classic, see Amazon SageMaker Studio Classic.

While this is not a mandatory prerequisite, customers gain the most value out of the dashboard if they set up model monitoring jobs using SageMaker Model Monitor for models deployed to endpoints. For prerequisites and instructions on how to use SageMaker Model Monitor, see Data and model quality monitoring with Amazon SageMaker Model Monitor.

The Model Dashboard view extracts high-level details from each model to provide a comprehensive summary of every model in your account. If your model is deployed for inference, the dashboard helps you track the performance of your model and endpoint in real time.

Important details t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateModel
```

---

## Interpret results

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-interpreting-results.html

**Contents:**
- Interpret results
- List Executions
- Inspect a Specific Execution
- List Generated Reports
- Violations Report
        - Note

After you run a baseline processing job and obtained statistics and constraint for your dataset, you can execute monitoring jobs that calculate statistics and list any violations encountered relative to the baseline constraints. Amazon CloudWatch metrics are also reported in your account by default. For information on viewing the results of monitoring in Amazon SageMaker Studio, see Visualize results for real-time endpoints in Amazon SageMaker Studio.

The schedule starts monitoring jobs at the specified intervals. The following code lists the latest five executions. If you are running this code after creating the hourly schedule, the executions might be empty, and you might have to wait until you cross the hour boundary (in UTC) to see the executions start. The following code includes the logic for waiting.

In the previous step, you picked up the latest completed or failed scheduled execution. You can explore what went right or wrong. The terminal states are:

Completed – The monitoring execution completed and no issues were found in the violations report.

CompletedWithViolations – The execution completed, but constraint violations were detected.

Failed – The monitoring execution failed, possibly due to client error (for example, a role issues) or infrastructure issues. To identify the cause, see the FailureReason and ExitMessage.

Use the following code to list the generated reports.

If there are violations compared to the baseline, they are generated in the violations report. Use the following code to list the violations.

This applies only to datasets that contain tabular data. The following schema files specify the statistics calculated and the violations monitored for.

Output Files for Tabular Datasets

Contains columnar statistics for each feature in the dataset that is analyzed. See the schema of this file in the next topic.

This file is created only for data quality monitoring.

Contains a list of violations found in this current set of data as compared to the baseline statistics and constraints file specified in the baseline_constaints and baseline_statistics paths.

The Amazon SageMaker Model Monitor prebuilt container saves a set of Amazon CloudWatch metrics for each feature by default.

The container code can emit CloudWatch metrics in this location: /opt/ml/output/metrics/cloudwatch.

**Examples:**

Example 1 (unknown):
```unknown
mon_executions = my_default_monitor.list_executions()
print("We created a hourly schedule above and it will kick off executions ON the hour (plus 0 - 20 min buffer.\nWe will have to wait till we hit the hour...")

while len(mon_executions) == 0:
    print("Waiting for the 1st execution to happen...")
    time.sleep(60)
    mon_executions = my_default_monitor.list_executions()
```

Example 2 (unknown):
```unknown
CompletedWithViolations
```

Example 3 (unknown):
```unknown
FailureReason
```

Example 4 (unknown):
```unknown
ExitMessage
```

---

## Deploy models with Amazon SageMaker Serverless Inference

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html

**Contents:**
- Deploy models with Amazon SageMaker Serverless Inference
- How it works
        - Topics
  - Container support
  - Memory size
  - Concurrent invocations
        - Note
  - Minimizing cold starts
  - Feature exclusions
- Getting started

Amazon SageMaker Serverless Inference is a purpose-built inference option that enables you to deploy and scale ML models without configuring or managing any of the underlying infrastructure. On-demand Serverless Inference is ideal for workloads which have idle periods between traffic spurts and can tolerate cold starts. Serverless endpoints automatically launch compute resources and scale them in and out depending on traffic, eliminating the need to choose instance types or manage scaling policies. This takes away the undifferentiated heavy lifting of selecting and managing servers. Serverless Inference integrates with AWS Lambda to offer you high availability, built-in fault tolerance and automatic scaling. With a pay-per-use model, Serverless Inference is a cost-effective option if you have an infrequent or unpredictable traffic pattern. During times when there are no requests, Serverless Inference scales your endpoint down to 0, helping you to minimize your costs. For more information about pricing for on-demand Serverless Inference, see Amazon SageMaker Pricing.

Optionally, you can also use Provisioned Concurrency with Serverless Inference. Serverless Inference with provisioned concurrency is a cost-effective option when you have predictable bursts in your traffic. Provisioned Concurrency allows you to deploy models on serverless endpoints with predictable performance, and high scalability by keeping your endpoints warm. SageMaker AI ensures that for the number of Provisioned Concurrency that you allocate, the compute resources are initialized and ready to respond within milliseconds. For Serverless Inference with Provisioned Concurrency, you pay for the compute capacity used to process inference requests, billed by the millisecond, and the amount of data processed. You also pay for Provisioned Concurrency usage, based on the memory configured, duration provisioned, and the amount of concurrency enabled. For more information about pricing for Serverless Inference with Provisioned Concurrency, see Amazon SageMaker Pricing.

You can integrate Serverless Inference with your MLOps Pipelines to streamline your ML workflow, and you can use a serverless endpoint to host a model registered with Model Registry.

Serverless Inference is generally available in 21 AWS Regions: US East (N. Virginia), US East (Ohio), US West (N. California), US West (Oregon), Africa (Cape Town), Asia Pacific (Hong Kong), Asia Pacific (Mumbai), Asia Pacific (Tokyo), Asia Pacific (Se

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
OverheadLatency
```

Example 2 (unknown):
```unknown
ValidationError
```

---

## Model quality

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html

**Contents:**
- Model quality
        - Topics

Model quality monitoring jobs monitor the performance of a model by comparing the predictions that the model makes with the actual Ground Truth labels that the model attempts to predict. To do this, model quality monitoring merges data that is captured from real-time or batch inference with actual labels that you store in an Amazon S3 bucket, and then compares the predictions with the actual labels.

To measure model quality, model monitor uses metrics that depend on the ML problem type. For example, if your model is for a regression problem, one of the metrics evaluated is mean square error (mse). For information about all of the metrics used for the different ML problem types, see Model quality metrics and Amazon CloudWatch monitoring.

Model quality monitoring follows the same steps as data quality monitoring, but adds the additional step of merging the actual labels from Amazon S3 with the predictions captured from the real-time inference endpoint or batch transform job. To monitor model quality, follow these steps:

Enable data capture. This captures inference input and output from a real-time inference endpoint or batch transform job and stores the data in Amazon S3. For more information, see Data capture.

Create a baseline. In this step, you run a baseline job that compares predictions from the model with Ground Truth labels in a baseline dataset. The baseline job automatically creates baseline statistical rules and constraints that define thresholds against which the model performance is evaluated. For more information, see Create a model quality baseline.

Define and schedule model quality monitoring jobs. For specific information and code samples of model quality monitoring jobs, see Schedule model quality monitoring jobs. For general information about monitoring jobs, see Schedule monitoring jobs.

Ingest Ground Truth labels that model monitor merges with captured prediction data from a real-time inference endpoint or batch transform job. For more information, see Ingest Ground Truth labels and merge them with predictions.

Integrate model quality monitoring with Amazon CloudWatch. For more information, see Monitoring model quality metrics with CloudWatch.

Interpret the results of a monitoring job. For more information, see Interpret results.

Use SageMaker Studio to enable model quality monitoring and visualize results. For more information, see Visualize results for real-time endpoints in Amazon SageMaker Studio.

Create a model quality base

*[Content truncated]*

---

## Real-time inference

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html

**Contents:**
- Real-time inference
        - Topics

Real-time inference is ideal for inference workloads where you have real-time, interactive, low latency requirements. You can deploy your model to SageMaker AI hosting services and get an endpoint that can be used for inference. These endpoints are fully managed and support autoscaling (see Automatic scaling of Amazon SageMaker AI models).

Deploy models for real-time inference

Invoke models for real-time inference

Automatic scaling of Amazon SageMaker AI models

Instance storage volumes

Validation of models in production

Online explainability with SageMaker Clarify

Fine-tune models with adapter inference components

---

## Multi-model endpoints

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/multi-model-endpoints.html

**Contents:**
- Multi-model endpoints
        - Topics
- How multi-model endpoints work
        - Note
- Sample notebooks for multi-model endpoints

Multi-model endpoints provide a scalable and cost-effective solution to deploying large numbers of models. They use the same fleet of resources and a shared serving container to host all of your models. This reduces hosting costs by improving endpoint utilization compared with using single-model endpoints. It also reduces deployment overhead because Amazon SageMaker AI manages loading models in memory and scaling them based on the traffic patterns to your endpoint.

The following diagram shows how multi-model endpoints work compared to single-model endpoints.

Multi-model endpoints are ideal for hosting a large number of models that use the same ML framework on a shared serving container. If you have a mix of frequently and infrequently accessed models, a multi-model endpoint can efficiently serve this traffic with fewer resources and higher cost savings. Your application should be tolerant of occasional cold start-related latency penalties that occur when invoking infrequently used models.

Multi-model endpoints support hosting both CPU and GPU backed models. By using GPU backed models, you can lower your model deployment costs through increased usage of the endpoint and its underlying accelerated compute instances.

Multi-model endpoints also enable time-sharing of memory resources across your models. This works best when the models are fairly similar in size and invocation latency. When this is the case, multi-model endpoints can effectively use instances across all models. If you have models that have significantly higher transactions per second (TPS) or latency requirements, we recommend hosting them on dedicated endpoints.

You can use multi-model endpoints with the following features:

AWS PrivateLink and VPCs

Serial inference pipelines (but only one multi-model enabled container can be included in an inference pipeline)

You can use the AWS SDK for Python (Boto) or the SageMaker AI console to create a multi-model endpoint. For CPU backed multi-model endpoints, you can create your endpoint with custom-built containers by integrating the Multi Model Server library.

How multi-model endpoints work

Sample notebooks for multi-model endpoints

Supported algorithms, frameworks, and instances for multi-model endpoints

Instance recommendations for multi-model endpoint deployments

Create a Multi-Model Endpoint

Invoke a Multi-Model Endpoint

Build Your Own Container for SageMaker AI Multi-Model Endpoints

Multi-Model Endpoint Security

CloudWatch Metrics

*[Content truncated]*

---

## Data and model quality monitoring with Amazon SageMaker Model Monitor

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html#model-monitor-how-it-works

**Contents:**
- Data and model quality monitoring with Amazon SageMaker Model Monitor
        - Topics
- How Amazon SageMaker Model Monitor works
        - Notes
  - Model Monitor sample notebooks

Amazon SageMaker Model Monitor monitors the quality of Amazon SageMaker AI machine learning models in production. With Model Monitor, you can set up:

Continuous monitoring with a real-time endpoint.

Continuous monitoring with a batch transform job that runs regularly.

On-schedule monitoring for asynchronous batch transform jobs.

With Model Monitor, you can set alerts that notify you when there are deviations in the model quality. Early and proactive detection of these deviations lets you to take corrective actions. You can take actions like retraining models, auditing upstream systems, or fixing quality issues without having to monitor models manually or build additional tooling. You can use Model Monitor prebuilt monitoring capabilities that do not require coding. You also have the flexibility to monitor models by coding to provide custom analysis.

Model Monitor provides the following types of monitoring:

Data quality - Monitor drift in data quality.

Model quality - Monitor drift in model quality metrics, such as accuracy.

Bias drift for models in production - Monitor bias in your model's predictions.

Feature attribution drift for models in production - Monitor drift in feature attribution.

Monitoring a Model in Production

How Amazon SageMaker Model Monitor works

Bias drift for models in production

Feature attribution drift for models in production

Schedule monitoring jobs

Amazon SageMaker Model Monitor prebuilt container

Visualize results for real-time endpoints in Amazon SageMaker Studio

Amazon SageMaker Model Monitor automatically monitors machine learning (ML) models in production and notifies you when quality issues happen. Model Monitor uses rules to detect drift in your models and alerts you when it happens. The following figure shows how this process works in the case that your model is deployed to a real-time endpoint.

You can also use Model Monitor to monitor a batch transform job instead of a real-time endpoint. In this case, instead of receiving requests to an endpoint and tracking the predictions, Model Monitor monitors inference inputs and outputs. The following figure diagrams the process of monitoring a batch transform job.

To enable model monitoring, take the following steps. These steps follow the path of the data through the various data collection, monitoring, and analysis processes.

For a real-time endpoint, enable the endpoint to capture data from incoming requests to a trained ML model and the resulting model pre

*[Content truncated]*

---

## Asynchronous inference

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html

**Contents:**
- Asynchronous inference
- How It Works
        - Note
- How Do I Get Started?

Amazon SageMaker Asynchronous Inference is a capability in SageMaker AI that queues incoming requests and processes them asynchronously. This option is ideal for requests with large payload sizes (up to 1GB), long processing times (up to one hour), and near real-time latency requirements. Asynchronous Inference enables you to save on costs by autoscaling the instance count to zero when there are no requests to process, so you only pay when your endpoint is processing requests.

Creating an asynchronous inference endpoint is similar to creating real-time inference endpoints. You can use your existing SageMaker AI models and only need to specify the AsyncInferenceConfig object while creating your endpoint configuration with the EndpointConfig field in the CreateEndpointConfig API. The following diagram shows the architecture and workflow of Asynchronous Inference.

To invoke the endpoint, you need to place the request payload in Amazon S3. You also need to provide a pointer to this payload as a part of the InvokeEndpointAsync request. Upon invocation, SageMaker AI queues the request for processing and returns an identifier and output location as a response. Upon processing, SageMaker AI places the result in the Amazon S3 location. You can optionally choose to receive success or error notifications with Amazon SNS. For more information about how to set up asynchronous notifications, see Check prediction results.

The presence of an asynchronous inference configuration (AsyncInferenceConfig) object in the endpoint configuration implies that the endpoint can only receive asynchronous invocations.

If you are a first-time user of Amazon SageMaker Asynchronous Inference, we recommend that you do the following:

Read Asynchronous endpoint operations for information on how to create, invoke, update, and delete an asynchronous endpoint.

Explore the Asynchronous Inference example notebook in the aws/amazon-sagemaker-examples GitHub repository.

Note that if your endpoint uses any of the features listed in this Exclusions page, you cannot use Asynchronous Inference.

**Examples:**

Example 1 (unknown):
```unknown
AsyncInferenceConfig
```

Example 2 (unknown):
```unknown
EndpointConfig
```

Example 3 (unknown):
```unknown
CreateEndpointConfig
```

Example 4 (unknown):
```unknown
InvokeEndpointAsync
```

---

## Data and model quality monitoring with Amazon SageMaker Model Monitor

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html

**Contents:**
- Data and model quality monitoring with Amazon SageMaker Model Monitor
        - Topics
- How Amazon SageMaker Model Monitor works
        - Notes
  - Model Monitor sample notebooks

Amazon SageMaker Model Monitor monitors the quality of Amazon SageMaker AI machine learning models in production. With Model Monitor, you can set up:

Continuous monitoring with a real-time endpoint.

Continuous monitoring with a batch transform job that runs regularly.

On-schedule monitoring for asynchronous batch transform jobs.

With Model Monitor, you can set alerts that notify you when there are deviations in the model quality. Early and proactive detection of these deviations lets you to take corrective actions. You can take actions like retraining models, auditing upstream systems, or fixing quality issues without having to monitor models manually or build additional tooling. You can use Model Monitor prebuilt monitoring capabilities that do not require coding. You also have the flexibility to monitor models by coding to provide custom analysis.

Model Monitor provides the following types of monitoring:

Data quality - Monitor drift in data quality.

Model quality - Monitor drift in model quality metrics, such as accuracy.

Bias drift for models in production - Monitor bias in your model's predictions.

Feature attribution drift for models in production - Monitor drift in feature attribution.

Monitoring a Model in Production

How Amazon SageMaker Model Monitor works

Bias drift for models in production

Feature attribution drift for models in production

Schedule monitoring jobs

Amazon SageMaker Model Monitor prebuilt container

Visualize results for real-time endpoints in Amazon SageMaker Studio

Amazon SageMaker Model Monitor automatically monitors machine learning (ML) models in production and notifies you when quality issues happen. Model Monitor uses rules to detect drift in your models and alerts you when it happens. The following figure shows how this process works in the case that your model is deployed to a real-time endpoint.

You can also use Model Monitor to monitor a batch transform job instead of a real-time endpoint. In this case, instead of receiving requests to an endpoint and tracking the predictions, Model Monitor monitors inference inputs and outputs. The following figure diagrams the process of monitoring a batch transform job.

To enable model monitoring, take the following steps. These steps follow the path of the data through the various data collection, monitoring, and analysis processes.

For a real-time endpoint, enable the endpoint to capture data from incoming requests to a trained ML model and the resulting model pre

*[Content truncated]*

---

## Schedule monitoring jobs

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-scheduling.html

**Contents:**
- Schedule monitoring jobs
        - Example baseline assignments
        - Example schedule for recurring analysis
        - Example schedule for one-time analysis
        - Example schedule for a batch transform job

Amazon SageMaker Model Monitor provides you the ability to monitor the data collected from your real-time endpoints. You can monitor your data on a recurring schedule, or you can monitor it one time, immediately. You can create a monitoring schedule with the CreateMonitoringSchedule API.

With a monitoring schedule, SageMaker AI can start processing jobs to analyze the data collected during a given period. In the processing job, SageMaker AI compares the dataset for the current analysis with the baseline statistics and constraints that you provide. Then, SageMaker AI generate a violations report. In addition, CloudWatch metrics are emitted for each feature under analysis.

SageMaker AI provides a prebuilt container for performing analysis on tabular datasets. Alternatively, you could choose to bring your own container as outlined in the Support for Your Own Containers With Amazon SageMaker Model Monitor topic.

You can create a model monitoring schedule for your real-time endpoint or batch transform job. Use the baseline resources (constraints and statistics) to compare against the real-time traffic or batch job inputs.

In the following example, the training dataset used to train the model was uploaded to Amazon S3. If you already have it in Amazon S3, you can point to it directly.

If you are scheduling a model monitor for a real-time endpoint, use the baseline constraints and statistics to compare against real-time traffic. The following code snippet shows the general format you use to schedule a model monitor for a real-time endpoint. This example schedules the model monitor to run hourly.

You can also schedule the analysis to run once without recurring by passing arguments like the following to the create_monitoring_schedule method:

In these arguments, the schedule_cron_expression parameter schedules the analysis to run once, immediately, with the value CronExpressionGenerator.now(). For any schedule with this setting, the data_analysis_start_time and data_analysis_end_time parameters are required. These parameters set the start time and end time of an analysis window. Define these times as offsets that are relative to the current time, and use ISO 8601 duration format. In this example, the times -PT1H and -PT0H define a window between one hour in the past and the current time. With this schedule, the analysis evaluates only the data that was collected during the specified window.

The following code snippet shows the general format you use to sched

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
CreateMonitoringSchedule
```

Example 2 (unknown):
```unknown
# copy over the training dataset to Amazon S3 (if you already have it in Amazon S3, you could reuse it)
baseline_prefix = prefix + '/baselining'
baseline_data_prefix = baseline_prefix + '/data'
baseline_results_prefix = baseline_prefix + '/results'

baseline_data_uri = 's3://{}/{}'.format(bucket,baseline_data_prefix)
baseline_results_uri = 's3://{}/{}'.format(bucket, baseline_results_prefix)
print('Baseline data uri: {}'.format(baseline_data_uri))
print('Baseline results uri: {}'.format(baseline_results_uri))
```

Example 3 (unknown):
```unknown
training_data_file = open("test_data/training-dataset-with-header.csv", 'rb')
s3_key = os.path.join(baseline_prefix, 'data', 'training-dataset-with-header.csv')
boto3.Session().resource('s3').Bucket(bucket).Object(s3_key).upload_fileobj(training_data_file)
```

Example 4 (python):
```python
from sagemaker.model_monitor import CronExpressionGenerator
from time import gmtime, strftime

mon_schedule_name = 'my-model-monitor-schedule-' + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
my_default_monitor.create_monitoring_schedule(
    monitor_schedule_name=mon_schedule_name,
    endpoint_input=EndpointInput(
        endpoint_name=endpoint_name,
        destination="/opt/ml/processing/input/endpoint"
    ),
    post_analytics_processor_script=s3_code_postprocessor_uri,
    output_s3_uri=s3_report_path,
    statistics=my_default_monitor.baseline_statistics(),
    constraints=my_default_monitor
...
```

---
