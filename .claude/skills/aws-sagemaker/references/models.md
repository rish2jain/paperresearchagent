# Aws-Sagemaker - Models

**Pages:** 9

---

## AWS Managed Policies for Model Registry

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-model-registry.html

**Contents:**
- AWS Managed Policies for Model Registry
        - Topics
- AWS managed policy: AmazonSageMakerModelRegistryFullAccess
- Amazon SageMaker AI updates to Model Registry managed policies

These AWS managed policies adds permissions required to use Model Registry. The policies are available in your AWS account and are used by execution roles created from the Amazon SageMaker AI console.

AWS managed policy: AmazonSageMakerModelRegistryFullAccess

Amazon SageMaker AI updates to Model Registry managed policies

This AWS managed policy grants permissions needed to use all Model Registry features inside an Amazon SageMaker AI domain. This policy is attached to an execution role when configuring Model Registry settings to enable Model Registry permissions.

This policy includes the following permissions.

ecr – Allows principals to retrieve information, including metadata, about Amazon Elastic Container Registry (Amazon ECR) images.

iam – Allows principals to pass the execution role to the Amazon SageMaker AI service.

resource-groups – Allows principals to create, list, tag, and delete AWS Resource Groups.

s3 – Allows principals to retrieve objects from the Amazon Simple Storage Service (Amazon S3) buckets where model versions are stored. Retrievable objects are limited to those whose case-insensitive name contains the string "sagemaker".

sagemaker – Allows principals to catalog, manage, and deploy models using the SageMaker Model Registry.

kms – Allows only the SageMaker AI service principal to add a grant, generate data keys, decrypt, and read AWS KMS keys, and only keys that are tagged for "sagemaker" use.

View details about updates to AWS managed policies for Model Registry since this service began tracking these changes. For automatic alerts about changes to this page, subscribe to the RSS feed on the SageMaker AI Document history page.

AmazonSageMakerModelRegistryFullAccess - Update to an existing policy

Add kms:CreateGrant, kms:DescribeKey, kms:GenerateDataKey, and kms:Decrypt permissions.

AmazonSageMakerModelRegistryFullAccess - New policy

**Examples:**

Example 1 (unknown):
```unknown
resource-groups
```

Example 2 (unknown):
```unknown
"sagemaker"
```

Example 3 (json):
```json
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Sid": "AmazonSageMakerModelRegistrySageMakerReadPermission",
      "Effect": "Allow",
      "Action": [
        "sagemaker:DescribeAction",
        "sagemaker:DescribeInferenceRecommendationsJob",
        "sagemaker:DescribeModelPackage",
        "sagemaker:DescribeModelPackageGroup",
        "sagemaker:DescribePipeline",
        "sagemaker:DescribePipelineExecution",
        "sagemaker:ListAssociations",
        "sagemaker:ListArtifacts",
        "sagemaker:ListModelMetadata",
        "sagemaker:ListModelPackages",
        "sagemaker:SearchArtifacts"
      ]
    }
  ]
}
```

Example 4 (json):
```json
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Sid": "AmazonSageMakerModelRegistrySageMakerReadPermission",
      "Effect": "Allow",
      "Action": [
        "sagemaker:DescribeAction",
        "sagemaker:DescribeInferenceRecommendationsJob",
        "sagemaker:DescribeModelPackage",
        "sagemaker:DescribeModelPackageGroup",
        "sagemaker:DescribePipeline",
        "sagemaker:DescribePipelineExecution",
        "sagemaker:ListAssociations",
        "sagemaker:ListArtifacts",
        "sagemaker:ListModelMetadata",
        "sagemaker:ListModelPackages",
        "sagemaker:SearchArtifacts"
      ]
    }
  ]
}
```

---

## How custom models work

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-build-model.html

**Contents:**
- How custom models work

Use Amazon SageMaker Canvas to build a custom model on the dataset that you've imported. Use the model that you've built to make predictions on new data. SageMaker Canvas uses the information in the dataset to build up to 250 models and choose the one that performs the best.

When you begin building a model, Canvas automatically recommends one or more model types. Model types fall into one of the following categories:

Numeric prediction – This is known as regression in machine learning. Use the numeric prediction model type when you want to make predictions for numeric data. For example, you might want to predict the price of houses based on features such as the house’s square footage.

Categorical prediction – This is known as classification in machine learning. When you want to categorize data into groups, use the categorical prediction model types:

2 category prediction – Use the 2 category prediction model type (also known as binary classification in machine learning) when you have two categories that you want to predict for your data. For example, you might want to determine whether a customer is likely to churn.

3+ category prediction – Use the 3+ category prediction model type (also known as multi-class classification in machine learning) when you have three or more categories that you want to predict for your data. For example, you might want to predict a customer's loan status based on features such as previous payments.

Time series forecasting – Use time series forecasts when you want to make predictions over a period of time. For example, you might want to predict the number of items you’ll sell in the next quarter. For information about time series forecasts, see Time Series Forecasts in Amazon SageMaker Canvas.

Image prediction – Use the single-label image prediction model type (also known as single-label image classification in machine learning) when you want to assign labels to images. For example, you might want to classify different types of manufacturing defects in images of your product.

Text prediction – Use the multi-category text prediction model type (also known as multi-class text classification in machine learning) when you want to assign labels to passages of text. For example, you might have a dataset of customer reviews for a product, and you want to determine whether customers liked or disliked the product. You might have your model predict whether a given passage of text is Positive, Negative, or Neutral.

For a table of

*[Content truncated]*

---

## Automatic scaling of Amazon SageMaker AI models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html

**Contents:**
- Automatic scaling of Amazon SageMaker AI models
        - Topics

Amazon SageMaker AI supports automatic scaling (auto scaling) for your hosted models. Auto scaling dynamically adjusts the number of instances provisioned for a model in response to changes in your workload. When the workload increases, auto scaling brings more instances online. When the workload decreases, auto scaling removes unnecessary instances so that you don't pay for provisioned instances that you aren't using.

Auto scaling policy overview

Auto scaling prerequisites

Configure model auto scaling with the console

Define a scaling policy

Apply a scaling policy

Instructions for editing a scaling policy

Temporarily turn off scaling policies

Delete a scaling policy

Check the status of a scaling activity by describing scaling activities

Scale an endpoint to zero instances

Load testing your auto scaling configuration

Use AWS CloudFormation to create a scaling policy

Update endpoints that use auto scaling

Delete endpoints configured for auto scaling

---

## Model Registry Models, Model Versions, and Model Groups

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-models.html

**Contents:**
- Model Registry Models, Model Versions, and Model Groups
        - Topics

The SageMaker Model Registry is structured as several Model (Package) Groups with model packages in each group. These Model Groups can optionally be added to one or more Collections. Each model package in a Model Group corresponds to a trained model. The version of each model package is a numerical value that starts at 1 and is incremented with each new model package added to a Model Group. For example, if 5 model packages are added to a Model Group, the model package versions will be 1, 2, 3, 4, and 5.

A model package is the actual model that is registered into the Model Registry as a versioned entity. There are two types of model packages in SageMaker AI. One type is used in the AWS Marketplace, and the other is used in the Model Registry. Model packages used in the AWS Marketplace are not versionable entities and are not associated with Model Groups in the Model Registry. The Model Registry receives every new model that you retrain, gives it a version, and assigns it to a Model Group inside the Model Registry. The following image shows an example of a Model Group with 25 consecutively-versioned models. For more information about model packages used in the AWS Marketplace, see Algorithms and packages in the AWS Marketplace.

The model packages used in the Model Registry are versioned, and must be associated with a Model Group. The ARN of this model package type has the structure: 'arn:aws:sagemaker:region:account:model-package-group/version'

The following topics show you how to create and work with models, model versions, and Model Groups in the Model Registry.

Register a Model Version

View Model Groups and Versions

Update the Details of a Model Version

Compare Model Versions

View and Manage Model Group and Model Version Tags

Delete a Model Version

Staging Construct for your Model Lifecycle

Update the Approval Status of a Model

Deploy a Model from the Registry with Python

Deploy a Model in Studio

Cross-account discoverability

View the Deployment History of a Model

View model lineage details in Studio

**Examples:**

Example 1 (unknown):
```unknown
'arn:aws:sagemaker:region:account:model-package-group/version'
```

Example 2 (unknown):
```unknown
model-package-group
```

---

## Evaluating and comparing Amazon SageMaker JumpStart text classification models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-text-classification-evaluation.html

**Contents:**
- Evaluating and comparing Amazon SageMaker JumpStart text classification models
- Prerequisites
        - Topics

SageMaker AI JumpStart offers multiple text classification models that categorize text into predefined classes. These models handle tasks such as sentiment analysis, topic classification, and content moderation. Choosing the right model for production requires careful evaluation using key metrics including accuracy, F1-score, and Matthews Correlation Coefficient (MCC).

Deploy multiple text classification models (DistilBERT and BERT) from the JumpStart catalog.

Run comprehensive evaluations across balanced, skewed, and challenging datasets.

Interpret advanced metrics including Matthews Correlation Coefficient (MCC) and Area Under the Curve Receiver Operating Characteristic scores.

Make data-driven model selection decisions using systematic comparison frameworks.

Set up production deployments with auto-scaling and CloudWatch monitoring.

Download the complete evaluation framework: JumpStart Model Evaluation Package. The package includes pre-run results with sample outputs so you can preview the evaluation process and metrics before deploying models yourself.

Before you begin, make sure that you have the following:

AWS account with SageMaker AI permissions.

SageMaker AI Amazon SageMaker Studio access.

Basic Python knowledge.

Understanding of text classification concepts.

Time and cost: 45 minutes total time. Costs vary based on instance types and usage duration - see SageMaker AI Pricing for current rates.

This tutorial includes step-by-step cleanup instructions to help you remove all resources and avoid ongoing charges.

Set up your evaluation environment

Select and deploy text classification models

Evaluate and compare model performance

Interpret your results

Deploy your model at scale

---

## Feature attribution drift for models in production

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-monitor-feature-attribution-drift.html

**Contents:**
- Feature attribution drift for models in production
- Model Monitor Example Notebook
        - Topics

A drift in the distribution of live data for models in production can result in a corresponding drift in the feature attribution values, just as it could cause a drift in bias when monitoring bias metrics. Amazon SageMaker Clarify feature attribution monitoring helps data scientists and ML engineers monitor predictions for feature attribution drift on a regular basis. As the model is monitored, customers can view exportable reports and graphs detailing feature attributions in SageMaker Studio and configure alerts in Amazon CloudWatch to receive notifications if it is detected that the attribution values drift beyond a certain threshold.

To illustrate this with a specific situation, consider a hypothetical scenario for college admissions. Assume that we observe the following (aggregated) feature attribution values in the training data and in the live data:

College Admission Hypothetical Scenario

The change from training data to live data appears significant. The feature ranking has completely reversed. Similar to the bias drift, the feature attribution drifts might be caused by a change in the live data distribution and warrant a closer look into the model behavior on the live data. Again, the first step in these scenarios is to raise an alarm that a drift has happened.

We can detect the drift by comparing how the ranking of the individual features changed from training data to live data. In addition to being sensitive to changes in ranking order, we also want to be sensitive to the raw attribution score of the features. For instance, given two features that fall in the ranking by the same number of positions going from training to live data, we want to be more sensitive to the feature that had a higher attribution score in the training data. With these properties in mind, we use the Normalized Discounted Cumulative Gain (NDCG) score for comparing the feature attributions rankings of training and live data.

Specifically, assume we have the following:

F=[f1​,…,fm​] is the list of features sorted with respect to their attribution scores in the training data where m is the total number of features. For instance, in our case, F=[SAT Score, GPA, Class Rank].

a(f) is a function that returns the feature attribution score on the training data given a feature f. For example, a(SAT Score) = 0.70.

F′=[f′​1​, …, f′​m​] is the list of features sorted with respect to their attribution scores in the live data. For example, F′= [Class Rank, GPA, SAT Score].

Then, 

*[Content truncated]*

---

## Predictions with custom models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-make-predictions.html

**Contents:**
- Predictions with custom models

Use the custom model that you've built in SageMaker Canvas to make predictions for your data. The following sections show you how to make predictions for numeric and categorical prediction models, time series forecasts, image prediction models, and text prediction models.

Numeric and categorical prediction, image prediction, and text prediction custom models support making the following types of predictions for your data:

Single predictions — A Single prediction is when you only need to make one prediction. For example, you have one image or passage of text that you want to classify.

Batch predictions — A Batch prediction is when you’d like to make predictions for an entire dataset. You can make batch predictions for datasets that are 1 TB+. For example, you have a CSV file of customer reviews for which you’d like to predict the customer sentiment, or you have a folder of image files that you'd like to classify. You should make predictions with a dataset that matches your input dataset. Canvas provides you with the ability to do manual batch predictions, or you can configure automatic batch predictions that run whenever you update a dataset.

For each prediction or set of predictions, SageMaker Canvas returns the following:

The probability of the predicted value being correct

Choose one of the following workflows to make predictions with your custom model:

Batch predictions in SageMaker Canvas

Make single predictions

After generating predictions with your model, you can also do the following:

Update your model by adding versions. If you want to try to improve the prediction accuracy of your model, you can build new versions of your model. You can choose to clone your original model building configuration and dataset, or you can change your configuration and select a different dataset. After adding a new version, you can review and compare versions to choose the best one.

Register a model version in the SageMaker AI model registry. You can register versions of your model to the SageMaker Model Registry, which is a feature for tracking and managing the status of model versions and machine learning pipelines. A data scientist or MLOps team user with access to the SageMaker Model Registry can review your model versions and approve or reject them before deploying them to production.

Send your batch predictions to Quick Suite. In Quick Suite, you can build and publish dashboards with your batch prediction datasets. This can help you analyze and share 

*[Content truncated]*

---

## Understand options for evaluating large language models with SageMaker Clarify

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-foundation-model-evaluate.html

**Contents:**
- Understand options for evaluating large language models with SageMaker Clarify
        - Important
        - Topics

In order to use SageMaker Clarify Foundation Model Evaluations, you must upgrade to the new Studio experience. As of November 30, 2023, the previous Amazon SageMaker Studio experience is now named Amazon SageMaker Studio Classic. The foundation evaluation feature can only be used in the updated experience. For information about how to update Studio, see Migration from Amazon SageMaker Studio Classic. For information about using the Studio Classic application, see Amazon SageMaker Studio Classic.

Using Amazon SageMaker Clarify you can evaluate large language models (LLMs) by creating model evaluation jobs. A model evaluation job allows you to evaluate and compare model quality and responsibility metrics for text-based foundation models from JumpStart. Model evaluation jobs also support the use of JumpStart models that have already been deployed to an endpoint.

You can create a model evaluation job using three different approaches.

Create automated model evaluation jobs in Studio – Automatic model evaluation jobs allow you to quickly evaluate a model's ability to perform a task. You can either provide your own custom prompt dataset that you've tailored to a specific use case, or you can use an available built-in dataset.

Create a model evaluation jobs that use human workers in Studio – Model evaluation jobs that use human workers allow you to bring human input to the model evaluation process. They can be employees of your company or a group of subject-matter experts from your industry.

Create an automated model evaluation job using the fmeval library – Creating a job using the fmeval gives you the most fine-grained control over your model evaluation jobs. It also supports the use of LLMs outside of AWS or non-JumpStart based models from other services.

Model evaluation jobs support common use cases for LLMs such as text generation, text classification, question and answering, and text summarization.

Open-ended generation – The production of natural human responses to text that does not have a pre-defined structure.

Text summarization – The generation of a concise and condensed summary while retaining the meaning and key information that's contained in larger text.

Question answering – The generation of a relevant and accurate response to a prompt.

Classification – Assigning a category, such as a label or score, to text based on its content.

The following topics describe the available model evaluation tasks, and the kinds of metrics you can use. These tasks help you evaluate model performance and select appropriate metrics for your use case.

---

## Amazon SageMaker JumpStart Foundation Models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models.html

**Contents:**
- Amazon SageMaker JumpStart Foundation Models
        - Topics

Amazon SageMaker JumpStart offers state-of-the-art foundation models for use cases such as content writing, code generation, question answering, copywriting, summarization, classification, information retrieval, and more. Use JumpStart foundation models to build your own generative AI solutions and integrate custom solutions with additional SageMaker AI features. For more information, see Getting started with Amazon SageMaker JumpStart.

A foundation model is a large pre-trained model that is adaptable to many downstream tasks and often serves as the starting point for developing more specialized models. Examples of foundation models include LLaMa-3-70b, BLOOM 176B, FLAN-T5 XL, or GPT-J 6B, which are pre-trained on massive amounts of text data and can be fine-tuned for specific language tasks.

Amazon SageMaker JumpStart onboards and maintains publicly available foundation models for you to access, customize, and integrate into your machine learning lifecycles. For more information, see Publicly available foundation models. Amazon SageMaker JumpStart also includes proprietary foundation models from third-party providers. For more information, see Proprietary foundation models.

To get started exploring and experimenting with available models, see JumpStart foundation model usage. All foundation models are available to use programmatically with the SageMaker Python SDK. For more information, see Use foundation models with the SageMaker Python SDK.

For more information on considerations to make when choosing a model, see Model sources and license agreements.

For specifics about customization and fine-tuning foundation models, see Foundation model customization.

For more general information on foundation models, see the paper On the Opportunities and Risks of Foundation Models.

Available foundation models

JumpStart foundation model usage

Model sources and license agreements

Foundation model customization

Evaluate a text generation foundation model in Studio

---
