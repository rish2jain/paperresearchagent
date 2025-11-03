# Aws-Sagemaker - Training

**Pages:** 66

---

## Built-in SageMaker AI Algorithms for Computer Vision

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-vision.html

**Contents:**
- Built-in SageMaker AI Algorithms for Computer Vision

SageMaker AI provides image processing algorithms that are used for image classification, object detection, and computer vision.

Image Classification - MXNet—uses example data with answers (referred to as a supervised algorithm). Use this algorithm to classify images.

Image Classification - TensorFlow—uses pretrained TensorFlow Hub models to fine-tune for specific tasks (referred to as a supervised algorithm). Use this algorithm to classify images.

Object Detection - MXNet—detects and classifies objects in images using a single deep neural network. It is a supervised learning algorithm that takes images as input and identifies all instances of objects within the image scene.

Object Detection - TensorFlow—detects bounding boxes and object labels in an image. It is a supervised learning algorithm that supports transfer learning with available pretrained TensorFlow models.

Semantic Segmentation Algorithm—provides a fine-grained, pixel-level approach to developing computer vision applications.

---

## Data quality

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-quality.html

**Contents:**
- Data quality
        - Note
        - Topics

Data quality monitoring automatically monitors machine learning (ML) models in production and notifies you when data quality issues arise. ML models in production have to make predictions on real-life data that is not carefully curated like most training datasets. If the statistical nature of the data that your model receives while in production drifts away from the nature of the baseline data it was trained on, the model begins to lose accuracy in its predictions. Amazon SageMaker Model Monitor uses rules to detect data drift and alerts you when it happens. To monitor data quality, follow these steps:

Enable data capture. This captures inference input and output from a real-time inference endpoint or batch transform job and stores the data in Amazon S3. For more information, see Data capture.

Create a baseline. In this step, you run a baseline job that analyzes an input dataset that you provide. The baseline computes baseline schema constraints and statistics for each feature using Deequ, an open source library built on Apache Spark, which is used to measure data quality in large datasets. For more information, see Create a Baseline.

Define and schedule data quality monitoring jobs. For specific information and code samples of data quality monitoring jobs, see Schedule data quality monitoring jobs. For general information about monitoring jobs, see Schedule monitoring jobs.

Optionally use preprocessing and postprocessing scripts to transform the data coming out of your data quality analysis. For more information, see Preprocessing and Postprocessing.

View data quality metrics. For more information, see Schema for Statistics (statistics.json file).

Integrate data quality monitoring with Amazon CloudWatch. For more information, see CloudWatch Metrics.

Interpret the results of a monitoring job. For more information, see Interpret results.

Use SageMaker Studio to enable data quality monitoring and visualize results if you are using a real-time endpoint. For more information, see Visualize results for real-time endpoints in Amazon SageMaker Studio.

Model Monitor computes model metrics and statistics on tabular data only. For example, an image classification model that takes images as input and outputs a label based on that image can still be monitored. Model Monitor would be able to calculate metrics and statistics for the output, not the input.

Schedule data quality monitoring jobs

Schema for Statistics (statistics.json file)

Schema for Violations

*[Content truncated]*

---

## Automatic model tuning with SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html

**Contents:**
- Automatic model tuning with SageMaker AI
        - Topics

Amazon SageMaker AI automatic model tuning (AMT) finds the best version of a model by running many training jobs on your dataset. Amazon SageMaker AI automatic model tuning (AMT) is also known as hyperparameter tuning. To do this, AMT uses the algorithm and ranges of hyperparameters that you specify. It then chooses the hyperparameter values that creates a model that performs the best, as measured by a metric that you choose.

For example, running a binary classification problem on a marketing dataset. Your goal is to maximize the area under the curve (AUC) metric of the algorithm by training an XGBoost algorithm with Amazon SageMaker AI model. You want to find which values for the eta, alpha, min_child_weight, and max_depth hyperparameters that will train the best model. Specify a range of values for these hyperparameters. Then, SageMaker AI hyperparameter tuning searches within the ranges to find a combination that creates a training job that creates a model with the highest AUC. To conserve resources or meet a specific model quality expectation, set up completion criteria to stop tuning after the criteria have been met.

You can use SageMaker AI AMT with built-in algorithms, custom algorithms, or SageMaker AI pre-built containers for machine learning frameworks.

SageMaker AI AMT can use an Amazon EC2 Spot instance to optimize costs when running training jobs. For more information, see Managed Spot Training in Amazon SageMaker AI.

Before you start using hyperparameter tuning, you should have a well-defined machine learning problem, including the following:

An understanding of the type of algorithm that you need to train

A clear understanding of how you measure success

Prepare your dataset and algorithm so that they work in SageMaker AI and successfully run a training job at least once. For information about setting up and running a training job, see Guide to getting set up with Amazon SageMaker AI.

Understand the hyperparameter tuning strategies available in Amazon SageMaker AI

Define metrics and environment variables

Define Hyperparameter Ranges

Track and set completion criteria for your tuning job

Tune Multiple Algorithms with Hyperparameter Optimization to Find the Best Model

Example: Hyperparameter Tuning Job

Stop Training Jobs Early

Run a Warm Start Hyperparameter Tuning Job

Resource Limits for Automatic Model Tuning

Best Practices for Hyperparameter Tuning

**Examples:**

Example 1 (unknown):
```unknown
min_child_weight
```

---

## Recommendations for choosing the right data preparation tool in SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-prep.html#data-prep-choose-recommended

**Contents:**
- Recommendations for choosing the right data preparation tool in SageMaker AI
- Choose a feature
  - Use cases
  - Recommended features
  - Additional options

Data preparation in machine learning refers to the process of collecting, preprocessing, and organizing raw data to make it suitable for analysis and modeling. This step ensures that the data is in a format from which machine learning algorithms can effectively learn. Data preparation tasks may include handling missing values, removing outliers, scaling features, encoding categorical variables, assessing potential biases and taking steps to mitigate them, splitting data into training and testing sets, labeling, and other necessary transformations to optimize the quality and usability of the data for subsequent machine learning tasks.

There are 3 primary use cases for data preparation with Amazon SageMaker AI. Choose the use case that aligns with your requirements, and then refer to the corresponding recommended feature.

The following are the primary uses cases when performing data preparation for Machine Learning.

Use case 1: For those who prefer a visual interface, SageMaker AI provides ways to explore, prepare, and engineer features for model training through a point-and-click environment.

Use case 2: For users comfortable with coding who want more flexibility and control over data preparation, SageMaker AI integrates tools into its coding environments for exploration, transformations, and feature engineering.

Use case 3: For users focused on scalable data preparation, SageMaker AI offers serverless capabilities that leverage the Hadoop/Spark ecosystem for distributed processing of big data.

The following table outlines the key considerations and tradeoffs for the SageMaker AI features related to each data preparation use case for machine learning. To get started, identify the use case that aligns to your requirements and navigate to its recommended SageMaker AI feature.

Create data preparation pipelines

Perform data analysis

Transform data using built-in transforms

Use genAI-powered natural language instructions for data transforms

Optimized for tabular data tasks such as handling missing values, encoding categorical variables, and applying data transformations.

It may not be the optimal choice if your team already has expertise in Python, Spark, or other languages.

It might not be best suited if you need full flexibility to customize transformations to add complex business logic or require full control over your data processing environment.

This feature is designed for structured data residing in Amazon Redshift, Snowflake, Athena, or Ama

*[Content truncated]*

---

## Built-in algorithms and pretrained models in Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html#algorithms-built-in-text-analysis

**Contents:**
- Built-in algorithms and pretrained models in Amazon SageMaker
- Pre-trained models and solution templates
- Supervised learning
- Unsupervised learning
- Textual analysis
- Image processing
        - Topics

Amazon SageMaker provides a suite of built-in algorithms, pre-trained models, and pre-built solution templates to help data scientists and machine learning practitioners get started on training and deploying machine learning models quickly. For someone who is new to SageMaker, choosing the right algorithm for your particular use case can be a challenging task. The following table provides a quick cheat sheet that shows how you can start with an example problem or use case and find an appropriate built-in algorithm offered by SageMaker that is valid for that problem type. Additional guidance organized by learning paradigms (supervised and unsupervised) and important data domains (text and images) is provided in the sections following the table.

Table: Mapping use cases to built-in algorithms

Tabular Classification

Sentence Pair Classification

Named Entity Recognition

Instance Segmentation

Semantic Segmentation

Here a few examples out of the 15 problem types that can be addressed by the pre-trained models and pre-built solution templates provided by Amazon SageMaker JumpStart:

Question answering: chatbot that outputs an answer for a given question.

Text analysis: analyze texts from models specific to an industry domain such as finance.

Popular models, including Mobilenet, YOLO, Faster R-CNN, BERT, lightGBM, and CatBoost

For a list of pre-trained models available, see JumpStart Models.

For a list of pre-built solution templates available, see JumpStart Solutions.

Binary/multi-class classification

Predict if an item belongs to a category: an email spam filter

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Predict a numeric/continuous value: estimate the value of a house

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Time-series forecasting

Based on historical data for a behavior, predict future behavior: predict sales on a new product based on previous sales data.

Use the SageMaker AI DeepAR forecasting algorithm

Improve the data embeddings of the high-dimensional objects: identify duplicate support tickets or find the correct routing based on similarity of text in the tickets

Feature engineering: dimensionality reduction

Drop those columns from

*[Content truncated]*

---

## Docker containers for training and deploying models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers.html

**Contents:**
- Docker containers for training and deploying models
        - Topics
- Scenarios for Running Scripts, Training Algorithms, or Deploying Models with SageMaker AI
        - Topics
  - Use cases for using pre-built Docker containers with SageMaker AI
  - Use cases for extending a pre-built Docker container
  - Use case for building your own container
- Troubleshooting your Docker containers and deployments

Amazon SageMaker AI makes extensive use of Docker containers for build and runtime tasks. SageMaker AI provides pre-built Docker images for its built-in algorithms and the supported deep learning frameworks used for training and inference. Using containers, you can train machine learning algorithms and deploy models quickly and reliably at any scale. The topics in this section show how to deploy these containers for your own use cases. For information about how to bring your own containers for use with Amazon SageMaker Studio Classic, see Custom Images in Amazon SageMaker Studio Classic.

Scenarios for Running Scripts, Training Algorithms, or Deploying Models with SageMaker AI

Docker container basics

Pre-built SageMaker AI Docker images

Custom Docker containers with SageMaker AI

Container creation with your own algorithms and models

Examples and More Information: Use Your Own Algorithm or Model

Troubleshooting your Docker containers and deployments

Amazon SageMaker AI always uses Docker containers when running scripts, training algorithms, and deploying models. Your level of engagement with containers depends on your use case.

The following decision tree illustrates three main scenarios: Use cases for using pre-built Docker containers with SageMaker AI; Use cases for extending a pre-built Docker container; Use case for building your own container.

Use cases for using pre-built Docker containers with SageMaker AI

Use cases for extending a pre-built Docker container

Use case for building your own container

Consider the following use cases when using containers with SageMaker AI:

Pre-built SageMaker AI algorithm – Use the image that comes with the built-in algorithm. See Use Amazon SageMaker AI Built-in Algorithms or Pre-trained Models for more information.

Custom model with pre-built SageMaker AI container – If you train or deploy a custom model, but use a framework that has a pre-built SageMaker AI container including TensorFlow and PyTorch, choose one of the following options:

If you don't need a custom package, and the container already includes all required packages: Use the pre-built Docker image associated with your framework. For more information, see Pre-built SageMaker AI Docker images.

If you need a custom package installed into one of the pre-built containers: Confirm that the pre-built Docker image allows a requirements.txt file, or extend the pre-built container based on the following use cases.

The following are use cases for e

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
sudo service docker restart
```

Example 2 (unknown):
```unknown
~/.sagemaker/config.yaml
```

Example 3 (unknown):
```unknown
container_root
```

Example 4 (unknown):
```unknown
local:
  container_root: /home/ec2-user/SageMaker/temp
```

---

## Model Registration Deployment with Model Registry

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html

**Contents:**
- Model Registration Deployment with Model Registry

With the Amazon SageMaker Model Registry you can do the following:

Catalog models for production.

Manage model versions.

Associate metadata, such as training metrics, with a model.

View information from Amazon SageMaker Model Cards in your registered models.

View model lineage for traceability and reproducibility.

Define a staging construct that models can progress through for your model lifecycle.

Manage the approval status of a model.

Deploy models to production.

Automate model deployment with CI/CD.

Share models with other users.

Catalog models by creating SageMaker Model Registry Model (Package) Groups that contain different versions of a model. You can create a Model Group that tracks all of the models that you train to solve a particular problem. You can then register each model you train and the Model Registry adds it to the Model Group as a new model version. Lastly, you can create categories of Model Groups by further organizing them into SageMaker Model Registry Collections. A typical workflow might look like the following:

Create a Model Group.

Create an ML pipeline that trains a model. For information about SageMaker pipelines, see Pipelines actions.

For each run of the ML pipeline, create a model version that you register in the Model Group you created in the first step.

Add your Model Group into one or more Model Registry Collections.

For details about how to create and work with models, model versions, and Model Groups, see Model Registry Models, Model Versions, and Model Groups. Optionally, if you want to further group your Model Groups into Collections, see Model Registry Collections.

---

## Data labeling with a human-in-the-loop

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-label.html

**Contents:**
- Data labeling with a human-in-the-loop
        - Topics

To train a machine learning model, you need a large, high-quality, labeled dataset. You can label your data using Amazon SageMaker Ground Truth. Choose from one of the Ground Truth built-in task types or create your own custom labeling workflow. To improve the accuracy of your data labels and reduce the total cost of labeling your data, use Ground Truth enhanced data labeling features like automated data labeling and annotation consolidation.

Training data labeling using humans with Amazon SageMaker Ground Truth

Use Amazon SageMaker Ground Truth Plus to Label Data

Crowd HTML Elements Reference

Using Amazon Augmented AI for Human Review

---

## SageMaker Training and Inference Toolkits

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/amazon-sagemaker-toolkits.html

**Contents:**
- SageMaker Training and Inference Toolkits
- SageMaker AI Toolkits Containers Structure
- Single Versus Multiple Containers

The SageMaker Training and SageMaker AI Inference toolkits implement the functionality that you need to adapt your containers to run scripts, train algorithms, and deploy models on SageMaker AI. When installed, the library defines the following for users:

The locations for storing code and other resources.

The entry point that contains the code to run when the container is started. Your Dockerfile must copy the code that needs to be run into the location expected by a container that is compatible with SageMaker AI.

Other information that a container needs to manage deployments for training and inference.

When SageMaker AI trains a model, it creates the following file folder structure in the container's /opt/ml directory.

When you run a model training job, the SageMaker AI container uses the /opt/ml/input/ directory, which contains the JSON files that configure the hyperparameters for the algorithm and the network layout used for distributed training. The /opt/ml/input/ directory also contains files that specify the channels through which SageMaker AI accesses the data, which is stored in Amazon Simple Storage Service (Amazon S3). The SageMaker AI containers library places the scripts that the container will run in the /opt/ml/code/ directory. Your script should write the model generated by your algorithm to the /opt/ml/model/ directory. For more information, see Containers with custom training algorithms.

When you host a trained model on SageMaker AI to make inferences, you deploy the model to an HTTP endpoint. The model makes real-time predictions in response to inference requests. The container must contain a serving stack to process these requests.

In a hosting or batch transform container, the model files are located in the same folder to which they were written during training.

For more information, see Containers with custom inference code.

You can either provide separate Docker images for the training algorithm and inference code or you can use a single Docker image for both. When creating Docker images for use with SageMaker AI, consider the following:

Providing two Docker images can increase storage requirements and cost because common libraries might be duplicated.

In general, smaller containers start faster for both training and hosting. Models train faster and the hosting service can react to increases in traffic by automatically scaling more quickly.

You might be able to write an inference container that is significantly smaller th

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
/opt/ml
├── input
│   ├── config
│   │   ├── hyperparameters.json
│   │   └── resourceConfig.json
│   └── data
│       └── <channel_name>
│           └── <input data>
├── model
│
├── code
│
├── output
│
└── failure
```

Example 2 (unknown):
```unknown
/opt/ml/input/
```

Example 3 (unknown):
```unknown
/opt/ml/input/
```

Example 4 (unknown):
```unknown
/opt/ml/code/
```

---

## Reserve training plans for your training jobs or HyperPod clusters

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/reserve-capacity-with-training-plans.html

**Contents:**
- Reserve training plans for your training jobs or HyperPod clusters
- What are SageMaker training plans
        - Note
- Benefits of SageMaker training plans
- SageMaker training plans advance reservation and flexible start times
        - Note
- SageMaker training plans user workflow
        - Note
- Supported instance types, AWS Regions, and pricing
        - Note

Amazon SageMaker training plans is a capability that allows you to reserve and help maximize the use of GPU capacity for large-scale AI model training workloads. This feature provides access to highly sought-after instance types that cover a range of GPU-accelerated computing options, including the latest NVIDIA GPU technologies and AWS trainium chips. With SageMaker training plans, you can secure predictable access to these high-demand, high-performance computational resources within your specified timelines and budgets, without the need to manage underlying infrastructure. This flexibility is particularly valuable for organizations dealing with the challenges of acquiring and scheduling these oversubscribed compute instances for their mission-critical AI workloads.

SageMaker training plans allow you to reserve compute capacity tailored to your target resource needs, such as SageMaker training jobs or SageMaker HyperPod clusters. The service automatically handles the reservation, provisioning of accelerated compute resources, infrastructure setup, workload execution, and recovery from infrastructure failures.

SageMaker training plans consist of one or more Reserved Capacity blocks, each defined by the following parameters:

Specific instance type

Quantity of instances

Training plans are specific to their target resource (either SageMaker Training Job or SageMaker HyperPod) and cannot be interchanged.

Multiple Reserved Capacity blocks in a single training plan may be discontinuous. This means there can be gaps between the Reserved Capacity blocks.

SageMaker training plans offer the following benefits:

Predictable Access: Reserve GPU capacity for your machine learning workloads within specified time frames.

Cost Management: Plan and budget for large-scale training requirements in advance.

Automated Resource Management: SageMaker training plans handle the provisioning and management of infrastructure.

Flexibility: Create training plans for various resources, including SageMaker training jobs and SageMaker HyperPod clusters.

Fault Tolerance: Benefit from automatic recovery from infrastructure failures and workload migration across Availability Zones for SageMaker AI training jobs.

SageMaker training plans allow you to reserve compute capacity in advance, with flexible start times and durations.

Advance reservation: You can reserve a training plan up to 8 weeks (56 days) in advance of the start date.

Minimum lead time: SageMaker training plans of

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
p6e-gb200.36xlarge
```

Example 2 (unknown):
```unknown
insufficient-data
```

---

## Tutorials

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-recipes-tutorials.html

**Contents:**
- Tutorials

The following quick-start tutorials help you get started with using the recipes for training:

SageMaker HyperPod with Slurm Orchestration

HyperPod Slurm cluster pre-training tutorial (GPU)

Trainium Slurm cluster pre-training tutorial

HyperPod Slurm cluster PEFT-Lora tutorial (GPU)

HyperPod Slurm cluster DPO tutorial (GPU)

SageMaker HyperPod with K8s Orchestration

Kubernetes cluster pre-training tutorial (GPU)

Trainium SageMaker training jobs pre-training tutorial

SageMaker training jobs

SageMaker training jobs pre-training tutorial (GPU)

Trainium SageMaker training jobs pre-training tutorial

---

## Built-in SageMaker AI Algorithms for Text Data

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-text.html

**Contents:**
- Built-in SageMaker AI Algorithms for Text Data

SageMaker AI provides algorithms that are tailored to the analysis of textual documents used in natural language processing, document classification or summarization, topic modeling or classification, and language transcription or translation.

BlazingText algorithm—a highly optimized implementation of the Word2vec and text classification algorithms that scale to large datasets easily. It is useful for many downstream natural language processing (NLP) tasks.

Latent Dirichlet Allocation (LDA) Algorithm—an algorithm suitable for determining topics in a set of documents. It is an unsupervised algorithm, which means that it doesn't use example data with answers during training.

Neural Topic Model (NTM) Algorithm—another unsupervised technique for determining topics in a set of documents, using a neural network approach.

Object2Vec Algorithm—a general-purpose neural embedding algorithm that can be used for recommendation systems, document classification, and sentence embeddings.

Sequence-to-Sequence Algorithm—a supervised algorithm commonly used for neural machine translation.

Text Classification - TensorFlow—a supervised algorithm that supports transfer learning with available pretrained models for text classification.

---

## Built-in algorithms and pretrained models in Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html#algorithms-built-in-jumpstart

**Contents:**
- Built-in algorithms and pretrained models in Amazon SageMaker
- Pre-trained models and solution templates
- Supervised learning
- Unsupervised learning
- Textual analysis
- Image processing
        - Topics

Amazon SageMaker provides a suite of built-in algorithms, pre-trained models, and pre-built solution templates to help data scientists and machine learning practitioners get started on training and deploying machine learning models quickly. For someone who is new to SageMaker, choosing the right algorithm for your particular use case can be a challenging task. The following table provides a quick cheat sheet that shows how you can start with an example problem or use case and find an appropriate built-in algorithm offered by SageMaker that is valid for that problem type. Additional guidance organized by learning paradigms (supervised and unsupervised) and important data domains (text and images) is provided in the sections following the table.

Table: Mapping use cases to built-in algorithms

Tabular Classification

Sentence Pair Classification

Named Entity Recognition

Instance Segmentation

Semantic Segmentation

Here a few examples out of the 15 problem types that can be addressed by the pre-trained models and pre-built solution templates provided by Amazon SageMaker JumpStart:

Question answering: chatbot that outputs an answer for a given question.

Text analysis: analyze texts from models specific to an industry domain such as finance.

Popular models, including Mobilenet, YOLO, Faster R-CNN, BERT, lightGBM, and CatBoost

For a list of pre-trained models available, see JumpStart Models.

For a list of pre-built solution templates available, see JumpStart Solutions.

Binary/multi-class classification

Predict if an item belongs to a category: an email spam filter

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Predict a numeric/continuous value: estimate the value of a house

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Time-series forecasting

Based on historical data for a behavior, predict future behavior: predict sales on a new product based on previous sales data.

Use the SageMaker AI DeepAR forecasting algorithm

Improve the data embeddings of the high-dimensional objects: identify duplicate support tickets or find the correct routing based on similarity of text in the tickets

Feature engineering: dimensionality reduction

Drop those columns from

*[Content truncated]*

---

## BatchPutMetrics

**URL:** https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_metrics_BatchPutMetrics.html

**Contents:**
- BatchPutMetrics
- Request Syntax
- URI Request Parameters
- Request Body
- Response Syntax
- Response Elements
- Errors
- See Also

Used to ingest training metrics into SageMaker. These metrics can be visualized in SageMaker Studio.

The request does not use any URI parameters.

The request accepts the following data in JSON format.

A list of raw metric values to put.

Type: Array of RawMetricData objects

Array Members: Minimum number of 1 item. Maximum number of 10 items.

The name of the Trial Component to associate with the metrics. The Trial Component name must be entirely lowercase.

Length Constraints: Minimum length of 1. Maximum length of 120.

Pattern: ^[a-z0-9](-*[a-z0-9]){0,119}

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

Lists any errors that occur when inserting metric data.

Type: Array of BatchPutMetricsError objects

Array Members: Minimum number of 1 item. Maximum number of 10 items.

For information about the errors that are common to all actions, see Common Errors.

For more information about using this API in one of the language-specific AWS SDKs, see the following:

AWS Command Line Interface V2

AWS SDK for JavaScript V3

**Examples:**

Example 1 (unknown):
```unknown
PUT /BatchPutMetrics HTTP/1.1
Content-type: application/json

{
   "MetricData": [
      {
         "MetricName": "string",
         "Step": number,
         "Timestamp": number,
         "Value": number
      }
   ],
   "TrialComponentName": "string"
}
```

Example 2 (unknown):
```unknown
^[a-z0-9](-*[a-z0-9]){0,119}
```

Example 3 (unknown):
```unknown
HTTP/1.1 200
Content-type: application/json

{
   "Errors": [
      {
         "Code": "string",
         "MetricIndex": number
      }
   ]
}
```

---

## Default configurations

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/default-configurations.html

**Contents:**
- Default configurations
        - Topics

This section outlines the essential components and settings required to initiate and customize your Large Language Model (LLM) training processes using SageMaker HyperPod. This section covers the key repositories, configuration files, and recipe structures that form the foundation of your training jobs. Understanding these default configurations is crucial for effectively setting up and managing your LLM training workflows, whether you're using pre-defined recipes or customizing them to suit your specific needs.

General configuration

---

## Amazon SageMaker Training Compiler

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/training-compiler.html

**Contents:**
- Amazon SageMaker Training Compiler
        - Important
- What Is SageMaker Training Compiler?
- How It Works
        - Tip
        - Topics

Amazon Web Services (AWS) announces that there will be no new releases or versions of SageMaker Training Compiler. You can continue to utilize SageMaker Training Compiler through the existing AWS Deep Learning Containers (DLCs) for SageMaker Training. It is important to note that while the existing DLCs remain accessible, they will no longer receive patches or updates from AWS, in accordance with the AWS Deep Learning Containers Framework Support Policy.

Use Amazon SageMaker Training Compiler to train deep learning (DL) models faster on scalable GPU instances managed by SageMaker AI.

State-of-the-art deep learning (DL) models consist of complex multi-layered neural networks with billions of parameters that can take thousands of GPU hours to train. Optimizing such models on training infrastructure requires extensive knowledge of DL and systems engineering; this is challenging even for narrow use cases. Although there are open-source implementations of compilers that optimize the DL training process, they can lack the flexibility to integrate DL frameworks with some hardware such as GPU instances.

SageMaker Training Compiler is a capability of SageMaker AI that makes these hard-to-implement optimizations to reduce training time on GPU instances. The compiler optimizes DL models to accelerate training by more efficiently using SageMaker AI machine learning (ML) GPU instances. SageMaker Training Compiler is available at no additional charge within SageMaker AI and can help reduce total billable time as it accelerates training.

SageMaker Training Compiler is integrated into the AWS Deep Learning Containers (DLCs). Using the SageMaker Training Compiler–enabled AWS DLCs, you can compile and optimize training jobs on GPU instances with minimal changes to your code. Bring your deep learning models to SageMaker AI and enable SageMaker Training Compiler to accelerate the speed of your training job on SageMaker AI ML instances for accelerated computing.

SageMaker Training Compiler converts DL models from their high-level language representation to hardware-optimized instructions. Specifically, SageMaker Training Compiler applies graph-level optimizations, dataflow-level optimizations, and backend optimizations to produce an optimized model that efficiently uses hardware resources. As a result, you can train your models faster than when you train them without compilation.

It is a two-step process to activate SageMaker Training Compiler for your training job:

Bri

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
compiler_config=TrainingCompilerConfig()
```

Example 2 (unknown):
```unknown
learning_rate
```

Example 3 (unknown):
```unknown
learning_rate
```

Example 4 (unknown):
```unknown
estimator.fit()
```

---

## SageMaker HyperPod recipes

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-recipes.html

**Contents:**
- SageMaker HyperPod recipes
        - Topics

Amazon SageMaker HyperPod recipes are pre-configured training stacks provided by AWS to help you quickly start training and fine-tuning publicly available foundation models (FMs) from various model families such as Llama, Mistral, Mixtral, or DeepSeek. Recipes automate the end-to-end training loop, including loading datasets, applying distributed training techniques, and managing checkpoints for faster recovery from faults.

SageMaker HyperPod recipes are particularly beneficial for users who may not have deep machine learning expertise, as they abstract away much of the complexity involved in training large models.

You can run recipes within SageMaker HyperPod or as SageMaker training jobs.

The following tables are maintained in the SageMaker HyperPod GitHub repository and provide the most up-to-date information on the models supported for pre-training and fine-tuning, their respective recipes and launch scripts, supported instance types, and more.

For the most current list of supported models, recipes, and launch scripts for pre-training, see the pre-training table.

For the most current list of supported models, recipes, and launch scripts for fine-tuning, see the fine-tuning table.

For SageMaker HyperPod users, the automation of end-to-end training workflows comes from the integration of the training adapter with SageMaker HyperPod recipes. The training adapter is built on the NVIDIA NeMo framework and the Neuronx Distributed Training package. If you're familiar with using NeMo, the process of using the training adapter is the same. The training adapter runs the recipe on your cluster.

You can also train your own model by defining your own custom recipe.

To get started with a tutorial, see Tutorials.

Default configurations

Cluster-specific configurations

---

## Distributed computing with SageMaker AI best practices

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training-options.html

**Contents:**
- Distributed computing with SageMaker AI best practices
        - Topics
- Option 1: Use a SageMaker AI built-in algorithm that supports distributed training
- Option 2: Run a custom ML code in the SageMaker AI managed training or processing environment
  - If your ML code uses a deep learning framework
  - If your ML code involves tabular data processing
- Option 3: Write your own custom distributed training code
- Option 4: Launch multiple jobs in parallel or sequentially

This best practices page presents various flavors of distributed computing for machine learning (ML) jobs in general. The term distributed computing in this page encompasses distributed training for machine learning tasks and parallel computing for data processing, data generation, feature engineering, and reinforcement learning. In this page, we discuss about common challenges in distributed computing, and available options in SageMaker Training and SageMaker Processing. For additional reading materials about distributed computing, see What Is Distributed Computing?.

You can configure ML tasks to run in a distributed manner across multiple nodes (instances), accelerators (NVIDIA GPUs, AWS Trainium chips), and vCPU cores. By running distributed computation, you can achieve a variety of goals such as computing operations faster, handling large datasets, or training large ML models.

The following list covers common challenges that you might face when you run an ML training job at scale.

You need to make decisions on how to distribute computation depending on ML tasks, software libraries you want to use, and compute resources.

Not all ML tasks are straightforward to distribute. Also, not all ML libraries support distributed computation.

Distributed computation might not always result in a linear increase in compute efficiency. In particular, you need to identify if data I/O and inter-GPU communication have bottlenecks or cause overhead.

Distributed computation might disturb numerical processes and change model accuracy. Specifically to data-parallel neural network training, when you change the global batch size while scaling up to a larger compute cluster, you also need to adjust the learning rate accordingly.

SageMaker AI provides distributed training solutions to ease such challenges for various use cases. Choose one of the following options that best fits your use case.

Option 1: Use a SageMaker AI built-in algorithm that supports distributed training

Option 2: Run a custom ML code in the SageMaker AI managed training or processing environment

Option 3: Write your own custom distributed training code

Option 4: Launch multiple jobs in parallel or sequentially

SageMaker AI provides built-in algorithms that you can use out of the box through the SageMaker AI console or the SageMaker Python SDK. Using the built-in algorithms, you don’t need to spend time for code customization, understanding science behind the models, or running Docker on provision

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
tf.distribute
```

Example 2 (unknown):
```unknown
/opt/ml/input/config/resourceconfig.json
```

Example 3 (unknown):
```unknown
/opt/ml/config/resourceconfig.json
```

Example 4 (unknown):
```unknown
S3DataDistributionType=ShardedByS3Key
```

---

## Evaluate, explain, and detect bias in models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-explainability.html

**Contents:**
- Evaluate, explain, and detect bias in models
        - Topics

Amazon SageMaker AI offers features to improve your machine learning (ML) models by detecting potential bias and helping to explain the predictions that your models make from your tabular, computer vision, natural processing, or time series datasets. It helps you identify various types of bias in pre-training data and in post-training that can emerge during model training or when the model is in production. You can also evaluate a language model for model quality and responsibility metrics using foundation model evaluations.

The following topics give information about how to evaluate, explain, and detect bias with Amazon SageMaker AI.

Understand options for evaluating large language models with SageMaker Clarify

Evaluating and comparing Amazon SageMaker JumpStart text classification models

Fairness, model explainability and bias detection with SageMaker Clarify

SageMaker Clarify explainability with SageMaker AI Autopilot

---

## Train a Model with Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html

**Contents:**
- Train a Model with Amazon SageMaker
        - Tip
- Choosing a feature within Amazon SageMaker Training
  - Use cases
  - Recommended features
- Additional options

Amazon SageMaker Training is a fully managed machine learning (ML) service offered by SageMaker that helps you efficiently train a wide range of ML models at scale. The core of SageMaker AI jobs is the containerization of ML workloads and the capability of managing AWS compute resources. The SageMaker Training platform takes care of the heavy lifting associated with setting up and managing infrastructure for ML training workloads. With SageMaker Training, you can focus on developing, training, and fine-tuning your model. This page introduces three recommended ways to get started with training a model on SageMaker, followed by additional options you can consider.

For information about training foundation models for Generative AI, see Use SageMaker JumpStart foundation models in Amazon SageMaker Studio.

There are three main use cases for training ML models within SageMaker AI. This section describes those use cases, as well as the SageMaker AI features we recommend for each use case.

Whether you are training complex deep learning models or implementing smaller machine learning algorithms, SageMaker Training provides streamlined and cost-effective solutions that meet the requirements of your use cases.

The following are the main uses cases for training ML models within SageMaker AI.

Use case 1: Develop a machine learning model in a low-code or no-code environment.

Use case 2: Use code to develop machine learning models with more flexibility and control.

Use case 3: Develop machine learning models at scale with maximum flexibility and control.

The following table describes three common scenarios of training ML models and corresponding options to get started with SageMaker Training.

Bring your data and choose one of the built-in ML algorithms provided by SageMaker AI. Set up the model hyperparameters, output metrics, and basic infrastructure settings using the SageMaker Python SDK. The SageMaker Training platform helps provision the training infrastructure and resources.

Develop your own ML code and bring it as a script or a set of scripts to SageMaker AI. To learn more, see Distributed computing with SageMaker best practices. Additionally, you can bring your own Docker container. The SageMaker Training platform helps provision the training infrastructure and resources at scale based on your custom settings.

Low/no-code and UI-driven model development with quick experimentation with a training dataset. When you build a custom model an algorithm autom

*[Content truncated]*

---

## Built-in algorithms and pretrained models in Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html#algorithms-built-in-unsupervised-learning

**Contents:**
- Built-in algorithms and pretrained models in Amazon SageMaker
- Pre-trained models and solution templates
- Supervised learning
- Unsupervised learning
- Textual analysis
- Image processing
        - Topics

Amazon SageMaker provides a suite of built-in algorithms, pre-trained models, and pre-built solution templates to help data scientists and machine learning practitioners get started on training and deploying machine learning models quickly. For someone who is new to SageMaker, choosing the right algorithm for your particular use case can be a challenging task. The following table provides a quick cheat sheet that shows how you can start with an example problem or use case and find an appropriate built-in algorithm offered by SageMaker that is valid for that problem type. Additional guidance organized by learning paradigms (supervised and unsupervised) and important data domains (text and images) is provided in the sections following the table.

Table: Mapping use cases to built-in algorithms

Tabular Classification

Sentence Pair Classification

Named Entity Recognition

Instance Segmentation

Semantic Segmentation

Here a few examples out of the 15 problem types that can be addressed by the pre-trained models and pre-built solution templates provided by Amazon SageMaker JumpStart:

Question answering: chatbot that outputs an answer for a given question.

Text analysis: analyze texts from models specific to an industry domain such as finance.

Popular models, including Mobilenet, YOLO, Faster R-CNN, BERT, lightGBM, and CatBoost

For a list of pre-trained models available, see JumpStart Models.

For a list of pre-built solution templates available, see JumpStart Solutions.

Binary/multi-class classification

Predict if an item belongs to a category: an email spam filter

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Predict a numeric/continuous value: estimate the value of a house

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Time-series forecasting

Based on historical data for a behavior, predict future behavior: predict sales on a new product based on previous sales data.

Use the SageMaker AI DeepAR forecasting algorithm

Improve the data embeddings of the high-dimensional objects: identify duplicate support tickets or find the correct routing based on similarity of text in the tickets

Feature engineering: dimensionality reduction

Drop those columns from

*[Content truncated]*

---

## Image Classification - MXNet

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/image-classification.html

**Contents:**
- Image Classification - MXNet
        - Note
        - Topics
- Input/Output Interface for the Image Classification Algorithm
  - Train with RecordIO Format
  - Train with Image Format
        - Note
  - Train with Augmented Manifest Image Format
  - Incremental Training
  - Inference with the Image Classification Algorithm

The Amazon SageMaker image classification algorithm is a supervised learning algorithm that supports multi-label classification. It takes an image as input and outputs one or more labels assigned to that image. It uses a convolutional neural network that can be trained from scratch or trained using transfer learning when a large number of training images are not available

The recommended input format for the Amazon SageMaker AI image classification algorithms is Apache MXNet RecordIO. However, you can also use raw images in .jpg or .png format. Refer to this discussion for a broad overview of efficient data preparation and loading for machine learning systems.

To maintain better interoperability with existing deep learning frameworks, this differs from the protobuf data formats commonly used by other Amazon SageMaker AI algorithms.

For more information on convolutional networks, see:

Deep residual learning for image recognition Kaiming He, et al., 2016 IEEE Conference on Computer Vision and Pattern Recognition

ImageNet image database

Image classification with Gluon-CV and MXNet

Input/Output Interface for the Image Classification Algorithm

EC2 Instance Recommendation for the Image Classification Algorithm

Image Classification Sample Notebooks

How Image Classification Works

Image Classification Hyperparameters

Tune an Image Classification Model

The SageMaker AI Image Classification algorithm supports both RecordIO (application/x-recordio) and image (image/png, image/jpeg, and application/x-image) content types for training in file mode, and supports the RecordIO (application/x-recordio) content type for training in pipe mode. However, you can also train in pipe mode using the image files (image/png, image/jpeg, and application/x-image), without creating RecordIO files, by using the augmented manifest format.

Distributed training is supported for file mode and pipe mode. When using the RecordIO content type in pipe mode, you must set the S3DataDistributionType of the S3DataSource to FullyReplicated. The algorithm supports a fully replicated model where your data is copied onto each machine.

The algorithm supports image/png, image/jpeg, and application/x-image for inference.

If you use the RecordIO format for training, specify both train and validation channels as values for the InputDataConfig parameter of the CreateTrainingJob request. Specify one RecordIO (.rec) file in the train channel and one RecordIO file in the validation channel. Set t

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

## Unsupervised Built-in SageMaker AI Algorithms

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-unsupervised.html

**Contents:**
- Unsupervised Built-in SageMaker AI Algorithms

Amazon SageMaker AI provides several built-in algorithms that can be used for a variety of unsupervised learning tasks such as clustering, dimension reduction, pattern recognition, and anomaly detection.

IP Insights—learns the usage patterns for IPv4 addresses. It is designed to capture associations between IPv4 addresses and various entities, such as user IDs or account numbers.

K-Means Algorithm—finds discrete groupings within data, where members of a group are as similar as possible to one another and as different as possible from members of other groups.

Principal Component Analysis (PCA) Algorithm—reduces the dimensionality (number of features) within a dataset by projecting data points onto the first few principal components. The objective is to retain as much information or variation as possible. For mathematicians, principal components are eigenvectors of the data's covariance matrix.

Random Cut Forest (RCF) Algorithm—detects anomalous data points within a data set that diverge from otherwise well-structured or patterned data.

---

## Create an AutoML job to fine-tune text generation models using the API

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-create-experiment-finetune-llms.html

**Contents:**
- Create an AutoML job to fine-tune text generation models using the API
        - Note
        - Note
        - Note
- Prerequisites
- Required parameters
- Optional parameters

Large language models (LLMs) excel in multiple generative tasks, including text generation, summarization, completion, question answering, and more. Their performance can be attributed to their significant size and extensive training on diverse datasets and various tasks. However, specific domains, such as healthcare and financial services, may require customized fine-tuning to adapt to unique data and use cases. By tailoring their training to their particular domain, LLMs can improve their performance and provide more accurate outputs for targeted applications.

Autopilot offers the capability to fine-tune a selection of pre-trained generative text models. In particular, Autopilot supports the instruction-based fine tuning of a selection of general-purpose large language models (LLMs) powered by JumpStart.

The text generation models that support fine-tuning in Autopilot are currently accessible exclusively in Regions supported by SageMaker Canvas. See the documentation of SageMaker Canvas for the full list of its supported Regions.

Fine-tuning a pre-trained model requires a specific dataset of clear instructions that guide the model on how to generate output or behave for that task. The model learns from the dataset, adjusting its parameters to conform to the provided instructions. Instruction-based fine-tuning involves using labeled examples formatted as prompt-response pairs and phrased as instructions. For more information about fine-tuning, see Fine-tune a foundation model.

The following guidelines outline the process of creating an Amazon SageMaker Autopilot job as a pilot experiment to fine-tune text generation LLMs using the SageMaker API Reference.

Tasks such as text and image classification, time-series forecasting, and fine-tuning of large language models are exclusively available through the version 2 of the AutoML REST API. If your language of choice is Python, you can refer to AWS SDK for Python (Boto3) or the AutoMLV2 object of the Amazon SageMaker Python SDK directly.

Users who prefer the convenience of a user interface can use Amazon SageMaker Canvas to access pre-trained models and generative AI foundation models, or create custom models tailored for specific text, image classification, forecasting needs, or generative AI.

To create an Autopilot experiment programmatically for fine-tuning an LLM, you can call the CreateAutoMLJobV2 API in any language supported by Amazon SageMaker Autopilot or the AWS CLI.

For information about how 

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
AutoMLJobObjective
```

---

## Built-in SageMaker AI Algorithms for Tabular Data

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-tabular.html

**Contents:**
- Built-in SageMaker AI Algorithms for Tabular Data

Amazon SageMaker AI provides built-in algorithms that are tailored to the analysis of tabular data. Tabular data refers to any datasets that are organized in tables consisting of rows (observations) and columns (features). The built-in SageMaker AI algorithms for tabular data can be used for either classification or regression problems.

AutoGluon-Tabular—an open-source AutoML framework that succeeds by ensembling models and stacking them in multiple layers.

CatBoost—an implementation of the gradient-boosted trees algorithm that introduces ordered boosting and an innovative algorithm for processing categorical features.

Factorization Machines Algorithm—an extension of a linear model that is designed to economically capture interactions between features within high-dimensional sparse datasets.

K-Nearest Neighbors (k-NN) Algorithm—a non-parametric method that uses the k nearest labeled points to assign a label to a new data point for classification or a predicted target value from the average of the k nearest points for regression.

LightGBM—an implementation of the gradient-boosted trees algorithm that adds two novel techniques for improved efficiency and scalability: Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB).

Linear Learner Algorithm—learns a linear function for regression or a linear threshold function for classification.

TabTransformer—a novel deep tabular data modeling architecture built on self-attention-based Transformers.

XGBoost algorithm with Amazon SageMaker AI—an implementation of the gradient-boosted trees algorithm that combines an ensemble of estimates from a set of simpler and weaker models.

---

## Object Detection - TensorFlow

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/object-detection-tensorflow.html

**Contents:**
- Object Detection - TensorFlow
        - Topics
- Amazon EC2 instance recommendation for the Object Detection - TensorFlow algorithm
- Object Detection - TensorFlow sample notebooks

The Amazon SageMaker AI Object Detection - TensorFlow algorithm is a supervised learning algorithm that supports transfer learning with many pretrained models from the TensorFlow Model Garden. Use transfer learning to fine-tune one of the available pretrained models on your own dataset, even if a large amount of image data is not available. The object detection algorithm takes an image as input and outputs a list of bounding boxes. Training datasets must consist of images in .jpg, .jpeg, or .png format. This page includes information about Amazon EC2 instance recommendations and sample notebooks for Object Detection - TensorFlow.

How to use the SageMaker AI Object Detection - TensorFlow algorithm

Input and output interface for the Object Detection - TensorFlow algorithm

Amazon EC2 instance recommendation for the Object Detection - TensorFlow algorithm

Object Detection - TensorFlow sample notebooks

How Object Detection - TensorFlow Works

Object Detection - TensorFlow Hyperparameters

Tune an Object Detection - TensorFlow model

The Object Detection - TensorFlow algorithm supports all GPU instances for training, including:

We recommend GPU instances with more memory for training with large batch sizes. Both CPU (such as M5) and GPU (P2 or P3) instances can be used for inference. For a comprehensive list of SageMaker training and inference instances across AWS Regions, see Amazon SageMaker Pricing.

For more information about how to use the SageMaker AI Object Detection - TensorFlow algorithm for transfer learning on a custom dataset, see the Introduction to SageMaker TensorFlow - Object Detection notebook.

For instructions how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, select the SageMaker AI Examples tab to see a list of all the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

**Examples:**

Example 1 (unknown):
```unknown
ml.p2.xlarge
```

Example 2 (unknown):
```unknown
ml.p2.16xlarge
```

Example 3 (unknown):
```unknown
ml.p3.2xlarge
```

Example 4 (unknown):
```unknown
ml.p3.16xlarge
```

---

## Amazon SageMaker Debugger

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/train-debugger.html

**Contents:**
- Amazon SageMaker Debugger
- Amazon SageMaker Debugger features
        - Topics

Debug model output tensors from machine learning training jobs in real time and detect non-converging issues using Amazon SageMaker Debugger.

A machine learning (ML) training job can have problems such as overfitting, saturated activation functions, and vanishing gradients, which can compromise model performance.

SageMaker Debugger provides tools to debug training jobs and resolve such problems to improve the performance of your model. Debugger also offers tools to send alerts when training anomalies are found, take actions against the problems, and identify the root cause of them by visualizing collected metrics and tensors.

SageMaker Debugger supports the Apache MXNet, PyTorch, TensorFlow, and XGBoost frameworks. For more information about available frameworks and versions supported by SageMaker Debugger, see Supported frameworks and algorithms.

The high-level Debugger workflow is as follows:

Modify your training script with the sagemaker-debugger Python SDK if needed.

Configure a SageMaker training job with SageMaker Debugger.

Configure using the SageMaker AI Estimator API (for Python SDK).

Configure using the SageMaker AI CreateTrainingJob request (for Boto3 or CLI).

Configure custom training containers with SageMaker Debugger.

Start a training job and monitor training issues in real time.

List of Debugger built-in rules.

Get alerts and take prompt actions against the training issues.

Receive texts and emails and stop training jobs when training issues are found using Use Debugger built-in actions for rules.

Set up your own actions using Amazon CloudWatch Events and AWS Lambda.

Explore deep analysis of the training issues.

For debugging model output tensors, see Visualize Debugger Output Tensors in TensorBoard.

Fix the issues, consider the suggestions provided by Debugger, and repeat steps 1–5 until you optimize your model and achieve target accuracy.

The SageMaker Debugger developer guide walks you through the following topics.

Supported frameworks and algorithms

Amazon SageMaker Debugger architecture

Debugging training jobs using Amazon SageMaker Debugger

List of Debugger built-in rules

Creating custom rules using the Debugger client library

Use Debugger with custom training containers

Configure Debugger using SageMaker API

Amazon SageMaker Debugger references

**Examples:**

Example 1 (unknown):
```unknown
sagemaker-debugger
```

Example 2 (unknown):
```unknown
CreateTrainingJob
```

---

## Distributed training in Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training.html

**Contents:**
- Distributed training in Amazon SageMaker AI
        - Tip
- Distributed training concepts
  - Advanced concepts

SageMaker AI provides distributed training libraries and supports various distributed training options for deep learning tasks such as computer vision (CV) and natural language processing (NLP). With SageMaker AI’s distributed training libraries, you can run highly scalable and cost-effective custom data parallel and model parallel deep learning training jobs. You can also use other distributed training frameworks and packages such as PyTorch DistributedDataParallel (DDP), torchrun, MPI (mpirun), and parameter server. The following section gives information about fundamental distributed training concepts. Throughout the documentation, instructions and examples focus on how to set up the distributed training options for deep learning tasks using the SageMaker Python SDK.

To learn best practices for distributed computing of machine learning (ML) training and processing jobs in general, see Distributed computing with SageMaker AI best practices.

SageMaker AI’s distributed training libraries use the following distributed training terms and features.

Training Dataset: All of the data you use to train the model.

Global batch size: The number of records selected from the training dataset in each iteration to send to the GPUs in the cluster. This is the number of records over which the gradient is computed at each iteration. If data parallelism is used, it is equal to the total number of model replicas multiplied by the per-replica batch size: global batch size = (the number of model replicas) * (per-replica batch size). A single batch of global batch size is often referred to as the mini-batch in machine learning literature.

Per-replica batch size: When data parallelism is used, this is the number of records sent to each model replica. Each model replica performs a forward and backward pass with this batch to calculate weight updates. The resulting weight updates are synchronized (averaged) across all replicas before the next set of per-replica batches are processed.

Micro-batch: A subset of the mini-batch or, if hybrid model and data parallelism is used , it is a subset of the per-replica sized batch . When you use SageMaker AI’s distributed model parallelism library, each micro-batch is fed into the training pipeline one-by-one and follows an execution schedule defined by the library's runtime.

Epoch: One training cycle through the entire dataset. It is common to have multiple iterations per an epoch. The number of epochs you use in training is unique on

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
global batch size = (the number of model replicas) *
            (per-replica batch size)
```

---

## AWS managed policies for SageMaker training plans

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-training-plan.html

**Contents:**
- AWS managed policies for SageMaker training plans
        - Topics
- AWS managed policy: AmazonSageMakerTrainingPlanCreateAccess
- Amazon SageMaker AI updates to SageMaker training plans managed policies

This AWS managed policy grants permissions needed to create and manage Amazon SageMaker training plans and Reserved Capacity in SageMaker AI. The policy can be attached to IAM roles used for creating and managing training plans and reserved capacity within SageMaker AI including your SageMaker AI execution role.

AWS managed policy: AmazonSageMakerTrainingPlanCreateAccess

Amazon SageMaker AI updates to SageMaker training plans managed policies

This policy provides the necessary permissions to create, describe, search for, and list training plans in SageMaker AI. Additionally, it also allows adding tags to training plans and reserved capacity resources under specific conditions.

This policy includes the following permissions.

sagemaker – Create training plans and reserved capacity, permits adding tags to training plans and reserved capacity when the tagging action is specifically CreateTrainingPlan or CreateReservedCapacity, allows describing training plans, permits searching for training plan offerings and listing existing training plans on all resources.

View details about updates to AWS managed policies for Amazon SageMaker AI since this service began tracking these changes.

AmazonSageMakerTrainingPlanCreateAccess - updated policy

AmazonSageMakerTrainingPlanCreateAccess - New policy

**Examples:**

Example 1 (unknown):
```unknown
CreateTrainingPlan
```

Example 2 (unknown):
```unknown
CreateReservedCapacity
```

Example 3 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Sid": "CreateTrainingPlanPermissions",
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateTrainingPlan",
        "sagemaker:CreateReservedCapacity",
        "sagemaker:DescribeReservedCapacity"
      ],
      "Resource": [
        "arn:aws:sagemaker:*:*:training-plan/*",
        "arn:aws:sagemaker:*:*:reserved-capacity/*"
      ]
    },
    {
      "Sid": "AggTagsToTrainingPlanPermissions",
      "Effect": "Allow",
      "Action": [
        "sagemaker:AddTags"
      ],
      "Resource": [
        "arn:aws:sagemaker:*:*:
...
```

Example 4 (unknown):
```unknown
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Sid": "CreateTrainingPlanPermissions",
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateTrainingPlan",
        "sagemaker:CreateReservedCapacity",
        "sagemaker:DescribeReservedCapacity"
      ],
      "Resource": [
        "arn:aws:sagemaker:*:*:training-plan/*",
        "arn:aws:sagemaker:*:*:reserved-capacity/*"
      ]
    },
    {
      "Sid": "AggTagsToTrainingPlanPermissions",
      "Effect": "Allow",
      "Action": [
        "sagemaker:AddTags"
      ],
      "Resource": [
        "arn:aws:sagemaker:*:*:
...
```

---

## Create, store, and share features with Feature Store

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html

**Contents:**
- Create, store, and share features with Feature Store
- How Feature Store works
- Create feature groups
        - Important
- Find, discover, and share features
- Real-time inference for features stored in the online store
- Offline store for model training and batch inference
- Feature data ingestion
- Resilience in Feature Store

The machine learning (ML) development process includes extracting raw data, transforming it into features (meaningful inputs for your ML model). Those features are then stored in a serviceable way for data exploration, ML training, and ML inference. Amazon SageMaker Feature Store simplifies how you create, store, share, and manage features. This is done by providing feature store options and reducing repetitive data processing and curation work.

Among other things, with Feature Store you can:

Simplify feature processing, storing, retrieving, and sharing features for ML development across accounts or in an organization.

Track your feature processing code development, apply your feature processor to the raw data, and ingest your features into Feature Store in a consistent way. This reduces training-serving skew, a common issue in ML where the difference between performance during training and serving can impact the accuracy of your ML model.

Store your features and associated metadata in feature groups, so features can be easily discovered and reused. Feature groups are mutable and can evolve their schema after creation.

Create feature groups that can be configured to include an online or offline store, or both, to manage your features and automate how features are stored for your ML tasks.

The online store retains only the latest records for your features. This is primarily designed for supporting real-time predictions that need low millisecond latency reads and high throughput writes.

The offline store keeps all records for your features as a historical database. This is primarily intended for data exploration, model training, and batch predictions.

The following diagram shows how you can use Feature Store as part of your ML pipeline. Once you read in your raw data, you can use Feature Store to transform the raw data into features and ingest them into your feature group. The features can be ingested via streaming or batches to the feature group's online and offline stores. The features can then be served for data exploration, model training, and real-time or batch inference.

In Feature Store, features are stored in a collection called a feature group. You can visualize a feature group as a table in which each column is a feature, with a unique identifier for each row. In principle, a feature group is composed of features and values specific to each feature. A Record is a collection of values for features that correspond to a unique RecordIdentifie

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
RecordIdentifier
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

## Built-in SageMaker AI Algorithms for Time-Series Data

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-time-series.html

**Contents:**
- Built-in SageMaker AI Algorithms for Time-Series Data

SageMaker AI provides algorithms that are tailored to the analysis of time-series data for forecasting product demand, server loads, webpage requests, and more.

Use the SageMaker AI DeepAR forecasting algorithm—a supervised learning algorithm for forecasting scalar (one-dimensional) time series using recurrent neural networks (RNN).

---

## Built-in algorithms and pretrained models in Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html#algorithms-built-in-image-processing

**Contents:**
- Built-in algorithms and pretrained models in Amazon SageMaker
- Pre-trained models and solution templates
- Supervised learning
- Unsupervised learning
- Textual analysis
- Image processing
        - Topics

Amazon SageMaker provides a suite of built-in algorithms, pre-trained models, and pre-built solution templates to help data scientists and machine learning practitioners get started on training and deploying machine learning models quickly. For someone who is new to SageMaker, choosing the right algorithm for your particular use case can be a challenging task. The following table provides a quick cheat sheet that shows how you can start with an example problem or use case and find an appropriate built-in algorithm offered by SageMaker that is valid for that problem type. Additional guidance organized by learning paradigms (supervised and unsupervised) and important data domains (text and images) is provided in the sections following the table.

Table: Mapping use cases to built-in algorithms

Tabular Classification

Sentence Pair Classification

Named Entity Recognition

Instance Segmentation

Semantic Segmentation

Here a few examples out of the 15 problem types that can be addressed by the pre-trained models and pre-built solution templates provided by Amazon SageMaker JumpStart:

Question answering: chatbot that outputs an answer for a given question.

Text analysis: analyze texts from models specific to an industry domain such as finance.

Popular models, including Mobilenet, YOLO, Faster R-CNN, BERT, lightGBM, and CatBoost

For a list of pre-trained models available, see JumpStart Models.

For a list of pre-built solution templates available, see JumpStart Solutions.

Binary/multi-class classification

Predict if an item belongs to a category: an email spam filter

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Predict a numeric/continuous value: estimate the value of a house

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Time-series forecasting

Based on historical data for a behavior, predict future behavior: predict sales on a new product based on previous sales data.

Use the SageMaker AI DeepAR forecasting algorithm

Improve the data embeddings of the high-dimensional objects: identify duplicate support tickets or find the correct routing based on similarity of text in the tickets

Feature engineering: dimensionality reduction

Drop those columns from

*[Content truncated]*

---

## Reserve training plans for your training jobs or HyperPod clusters

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/reserve-capacity-with-training-plans.html#training-plans-target-resources

**Contents:**
- Reserve training plans for your training jobs or HyperPod clusters
- What are SageMaker training plans
        - Note
- Benefits of SageMaker training plans
- SageMaker training plans advance reservation and flexible start times
        - Note
- SageMaker training plans user workflow
        - Note
- Supported instance types, AWS Regions, and pricing
        - Note

Amazon SageMaker training plans is a capability that allows you to reserve and help maximize the use of GPU capacity for large-scale AI model training workloads. This feature provides access to highly sought-after instance types that cover a range of GPU-accelerated computing options, including the latest NVIDIA GPU technologies and AWS trainium chips. With SageMaker training plans, you can secure predictable access to these high-demand, high-performance computational resources within your specified timelines and budgets, without the need to manage underlying infrastructure. This flexibility is particularly valuable for organizations dealing with the challenges of acquiring and scheduling these oversubscribed compute instances for their mission-critical AI workloads.

SageMaker training plans allow you to reserve compute capacity tailored to your target resource needs, such as SageMaker training jobs or SageMaker HyperPod clusters. The service automatically handles the reservation, provisioning of accelerated compute resources, infrastructure setup, workload execution, and recovery from infrastructure failures.

SageMaker training plans consist of one or more Reserved Capacity blocks, each defined by the following parameters:

Specific instance type

Quantity of instances

Training plans are specific to their target resource (either SageMaker Training Job or SageMaker HyperPod) and cannot be interchanged.

Multiple Reserved Capacity blocks in a single training plan may be discontinuous. This means there can be gaps between the Reserved Capacity blocks.

SageMaker training plans offer the following benefits:

Predictable Access: Reserve GPU capacity for your machine learning workloads within specified time frames.

Cost Management: Plan and budget for large-scale training requirements in advance.

Automated Resource Management: SageMaker training plans handle the provisioning and management of infrastructure.

Flexibility: Create training plans for various resources, including SageMaker training jobs and SageMaker HyperPod clusters.

Fault Tolerance: Benefit from automatic recovery from infrastructure failures and workload migration across Availability Zones for SageMaker AI training jobs.

SageMaker training plans allow you to reserve compute capacity in advance, with flexible start times and durations.

Advance reservation: You can reserve a training plan up to 8 weeks (56 days) in advance of the start date.

Minimum lead time: SageMaker training plans of

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
p6e-gb200.36xlarge
```

Example 2 (unknown):
```unknown
insufficient-data
```

---

## Built-in algorithms and pretrained models in Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html

**Contents:**
- Built-in algorithms and pretrained models in Amazon SageMaker
- Pre-trained models and solution templates
- Supervised learning
- Unsupervised learning
- Textual analysis
- Image processing
        - Topics

Amazon SageMaker provides a suite of built-in algorithms, pre-trained models, and pre-built solution templates to help data scientists and machine learning practitioners get started on training and deploying machine learning models quickly. For someone who is new to SageMaker, choosing the right algorithm for your particular use case can be a challenging task. The following table provides a quick cheat sheet that shows how you can start with an example problem or use case and find an appropriate built-in algorithm offered by SageMaker that is valid for that problem type. Additional guidance organized by learning paradigms (supervised and unsupervised) and important data domains (text and images) is provided in the sections following the table.

Table: Mapping use cases to built-in algorithms

Tabular Classification

Sentence Pair Classification

Named Entity Recognition

Instance Segmentation

Semantic Segmentation

Here a few examples out of the 15 problem types that can be addressed by the pre-trained models and pre-built solution templates provided by Amazon SageMaker JumpStart:

Question answering: chatbot that outputs an answer for a given question.

Text analysis: analyze texts from models specific to an industry domain such as finance.

Popular models, including Mobilenet, YOLO, Faster R-CNN, BERT, lightGBM, and CatBoost

For a list of pre-trained models available, see JumpStart Models.

For a list of pre-built solution templates available, see JumpStart Solutions.

Binary/multi-class classification

Predict if an item belongs to a category: an email spam filter

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Predict a numeric/continuous value: estimate the value of a house

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Time-series forecasting

Based on historical data for a behavior, predict future behavior: predict sales on a new product based on previous sales data.

Use the SageMaker AI DeepAR forecasting algorithm

Improve the data embeddings of the high-dimensional objects: identify duplicate support tickets or find the correct routing based on similarity of text in the tickets

Feature engineering: dimensionality reduction

Drop those columns from

*[Content truncated]*

---

## Advanced settings

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/cluster-specific-configurations-advanced-settings.html

**Contents:**
- Advanced settings
- Use the SageMaker HyperPod adapter to create your own model

The SageMaker HyperPod recipe adapter is built on top of the Nvidia Nemo and Pytorch-lightning frameworks. If you've already used these frameworks, integrating your custom models or features into the SageMaker HyperPod recipe adapter is a similar process. In addition to modifying the recipe adapter, you can change your own pre-training or fine-tuning script. For guidance on writing your custom training script, see examples.

Within the recipe adapter, you can customize the following files in the following locations:

collections/data: Contains a module responsible for loading datasets. Currently, it only supports datasets from HuggingFace. If you have more advanced requirements, the code structure allows you to add custom data modules within the same folder.

collections/model: Includes the definitions of various language models. Currently, it supports common large language models like Llama, Mixtral, and Mistral. You have the flexibility to introduce your own model definitions within this folder.

collections/parts: This folder contains strategies for training models in a distributed manner. One example is the Fully Sharded Data Parallel (FSDP) strategy, which allows for sharding a large language model across multiple accelerators. Additionally, the strategies support various forms of model parallelism. You also have the option to introduce your own customized training strategies for model training.

utils: Contains various utilities aimed at facilitating the management of a training job. It serves as a repository where for your own tools. You can use your own tools for tasks such as troubleshooting or benchmarking. You can also add your own personalized PyTorch Lightning callbacks within this folder. You can use PyTorch Lightning callbacks to seamlessly integrate specific functionalities or operations into the training lifecycle.

conf: Contains the configuration schema definitions used for validating specific parameters in a training job. If you introduce new parameters or configurations, you can add your customized schema to this folder. You can use the customized schema to define the validation rules. You can validate data types, ranges, or any other parameter constraint. You can also define you own custom schema to validate the parameters.

**Examples:**

Example 1 (unknown):
```unknown
collections/data
```

Example 2 (unknown):
```unknown
collections/model
```

Example 3 (unknown):
```unknown
collections/parts
```

---

## Automatically Train Models on Your Data Flow

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-autopilot.html

**Contents:**
- Automatically Train Models on Your Data Flow
        - Important

You can use Amazon SageMaker Autopilot to automatically train, tune, and deploy models on the data that you've transformed in your data flow. Amazon SageMaker Autopilot can go through several algorithms and use the one that works best with your data. For more information about Amazon SageMaker Autopilot, see SageMaker Autopilot.

When you train and tune a model, Data Wrangler exports your data to an Amazon S3 location where Amazon SageMaker Autopilot can access it.

You can prepare and deploy a model by choosing a node in your Data Wrangler flow and choosing Export and Train in the data preview. You can use this method to view your dataset before you choose to train a model on it.

You can also train and deploy a model directly from your data flow.

The following procedure prepares and deploys a model from the data flow. For Data Wrangler flows with multi-row transforms, you can't use the transforms from the Data Wrangler flow when you're deploying the model. You can use the following procedure to process the data before you use it to perform inference.

To train and deploy a model directly from your data flow, do the following.

Choose the + next to the node containing the training data.

(Optional) Specify a AWS KMS key or ID. For more information about creating and controlling cryptographic keys to protect your data, see AWS Key Management Service.

Choose Export and train.

After Amazon SageMaker Autopilot trains the model on the data that Data Wrangler exported, specify a name for Experiment name.

Under Input data, choose Preview to verify that Data Wrangler properly exported your data to Amazon SageMaker Autopilot.

For Target, choose the target column.

(Optional) For S3 location under Output data, specify an Amazon S3 location other than the default location.

Choose Next: Training method.

Choose a training method. For more information, see Training modes.

(Optional) For Auto deploy endpoint, specify a name for the endpoint.

For Deployment option, choose a deployment method. You can choose to deploy with or without the transformations that you've made to your data.

You can't deploy an Amazon SageMaker Autopilot model with the transformations that you've made in your Data Wrangler flow. For more information about those transformations, see Export to an Inference Endpoint.

Choose Next: Review and create.

Choose Create experiment.

For more information about model training and deployment, see Create Regression or Classification Jobs for Tabular

*[Content truncated]*

---

## Task-Specific Models

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-models.html

**Contents:**
- Task-Specific Models

JumpStart supports task-specific models across fifteen of the most popular problem types. Of the supported problem types, Vision and NLP-related types total thirteen. There are eight problem types that support incremental training and fine-tuning. For more information about incremental training and hyper-parameter tuning, see SageMaker AI Automatic Model Tuning.​ JumpStart also supports four popular algorithms for tabular data modeling.

You can search and browse models from the JumpStart landing page in Studio or Studio Classic. When you select a model, the model detail page provides information about the model, and you can train and deploy your model in a few steps. The description section describes what you can do with the model, the expected types of inputs and outputs, and the data type needed for fine-tuning your model.

You can also programmatically utilize models with the SageMaker Python SDK. For a list of all available models, see the JumpStart Available Model Table.

The list of problem types and links to their example Jupyter notebooks are summarized in the following table.

Introduction to JumpStart - Image Classification

Introduction to JumpStart - Object Detection

Introduction to JumpStart - Semantic Segmentation

Introduction to JumpStart - Instance Segmentation

Introduction to JumpStart - Image Embedding

Introduction to JumpStart - Text Classification

Introduction to JumpStart - Sentence Pair Classification

Introduction to JumpStart – Question Answering

Introduction to JumpStart - Named Entity Recognition

Introduction to JumpStart - Text Summarization

Introduction to JumpStart - Text Generation

Introduction to JumpStart - Machine Translation

Introduction to JumpStart - Text Embedding

Introduction to JumpStart - Tabular Classification - LightGBM, CatBoost

Introduction to JumpStart - Tabular Classification - XGBoost, Linear Learner

Introduction to JumpStart - Tabular Classification - AutoGluon Learner

Introduction to JumpStart - Tabular Classification - TabTransformer Learner

Introduction to JumpStart - Tabular Regression - LightGBM, CatBoost

Introduction to JumpStart – Tabular Regression - XGBoost, Linear Learner

Introduction to JumpStart – Tabular Regression - AutoGluon Learner

Introduction to JumpStart – Tabular Regression - TabTransformer Learner

---

## Containers with custom training algorithms

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html

**Contents:**
- Containers with custom training algorithms
        - Topics

This section explains how Amazon SageMaker AI interacts with a Docker container that runs your custom training algorithm. Use this information to write training code and create a Docker image for your training algorithms.

How Amazon SageMaker AI Runs Your Training Image

How Amazon SageMaker AI Provides Training Information

Run Training with EFA

How Amazon SageMaker AI Signals Algorithm Success and Failure

How Amazon SageMaker AI Processes Training Output

---

## Custom Docker containers with SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers-adapt-your-own.html

**Contents:**
- Custom Docker containers with SageMaker AI
        - Topics
- Individual Framework Libraries

You can adapt an existing Docker image to work with SageMaker AI. You may need to use an existing, external Docker image with SageMaker AI when you have a container that satisfies feature or safety requirements that are not currently supported by a pre-built SageMaker AI image. There are two toolkits that allow you to bring your own container and adapt it to work with SageMaker AI:

SageMaker Training Toolkit – Use this toolkit for training models with SageMaker AI.

SageMaker AI Inference Toolkit – Use this toolkit for deploying models with SageMaker AI.

The following topics show how to adapt your existing image using the SageMaker Training and Inference toolkits:

Individual Framework Libraries

SageMaker Training and Inference Toolkits

Adapting your own training container

Adapt your own inference container for Amazon SageMaker AI

In addition to the SageMaker Training Toolkit and SageMaker AI Inference Toolkit, SageMaker AI also provides toolkits specialized for TensorFlow, MXNet, PyTorch, and Chainer. The following table provides links to the GitHub repositories that contain the source code for each framework and their respective serving toolkits. The instructions linked are for using the Python SDK to run training algorithms and host models on SageMaker AI. The functionality for these individual libraries is included in the SageMaker AI Training Toolkit and SageMaker AI Inference Toolkit.

SageMaker AI TensorFlow Training

SageMaker AI TensorFlow Serving

SageMaker AI MXNet Training

SageMaker AI MXNet Inference

SageMaker AI PyTorch Training

SageMaker AI PyTorch Inference

SageMaker AI Chainer SageMaker AI Containers

---

## Parameters for Built-in Algorithms

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/common-info-all-im-models.html

**Contents:**
- Parameters for Built-in Algorithms
        - Note
        - Topics

The following table lists parameters for each of the algorithms provided by Amazon SageMaker AI.

Algorithms that are parallelizable can be deployed on multiple compute instances for distributed training.

The following topics provide information about data formats, recommended Amazon EC2 instance types, and CloudWatch logs common to all of the built-in algorithms provided by Amazon SageMaker AI.

To look up the Docker image URIs of the built-in algorithms managed by SageMaker AI, see Docker Registry Paths and Example Code.

Common Data Formats for Training

Common data formats for inference

Instance Types for Built-in Algorithms

Logs for Built-in Algorithms

---

## Batch transform for inference with Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html

**Contents:**
- Batch transform for inference with Amazon SageMaker AI
        - Topics
- Use batch transform to get inferences from large datasets
        - Note
- Speed up a batch transform job
- Use batch transform to test production variants
- Batch transform sample notebooks

Use batch transform when you need to do the following:

Preprocess datasets to remove noise or bias that interferes with training or inference from your dataset.

Get inferences from large datasets.

Run inference when you don't need a persistent endpoint.

Associate input records with inferences to help with the interpretation of results.

To filter input data before performing inferences or to associate input records with inferences about those records, see Associate Prediction Results with Input Records. For example, you can filter input data to provide context for creating and interpreting reports about the output data.

Use batch transform to get inferences from large datasets

Speed up a batch transform job

Use batch transform to test production variants

Batch transform sample notebooks

Associate Prediction Results with Input Records

Storage in Batch Transform

Batch transform automatically manages the processing of large datasets within the limits of specified parameters. For example, having a dataset file, input1.csv, stored in an S3 bucket. The content of the input file might look like the following example.

When a batch transform job starts, SageMaker AI starts compute instances and distributes the inference or preprocessing workload between them. Batch Transform partitions the Amazon S3 objects in the input by key and maps Amazon S3 objects to instances. When you have multiple files, one instance might process input1.csv, and another instance might process the file named input2.csv. If you have one input file but initialize multiple compute instances, only one instance processes the input file. The rest of the instances are idle.

You can also split input files into mini-batches. For example, you might create a mini-batch from input1.csv by including only two of the records.

SageMaker AI processes each input file separately. It doesn't combine mini-batches from different input files to comply with the MaxPayloadInMB limit.

To split input files into mini-batches when you create a batch transform job, set the SplitType parameter value to Line. SageMaker AI uses the entire input file in a single request when:

SplitType is set to None.

An input file can't be split into mini-batches.

. Note that Batch Transform doesn't support CSV-formatted input that contains embedded newline characters. You can control the size of the mini-batches by using the BatchStrategy and MaxPayloadInMB parameters. MaxPayloadInMB must not be greater than 100 MB. If 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
Record1-Attribute1, Record1-Attribute2, Record1-Attribute3, ..., Record1-AttributeM
Record2-Attribute1, Record2-Attribute2, Record2-Attribute3, ..., Record2-AttributeM
Record3-Attribute1, Record3-Attribute2, Record3-Attribute3, ..., Record3-AttributeM
...
RecordN-Attribute1, RecordN-Attribute2, RecordN-Attribute3, ..., RecordN-AttributeM
```

Example 2 (unknown):
```unknown
Record3-Attribute1, Record3-Attribute2, Record3-Attribute3, ..., Record3-AttributeM
Record4-Attribute1, Record4-Attribute2, Record4-Attribute3, ..., Record4-AttributeM
```

Example 3 (unknown):
```unknown
MaxPayloadInMB
```

Example 4 (unknown):
```unknown
BatchStrategy
```

---

## Text Classification - TensorFlow

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/text-classification-tensorflow.html

**Contents:**
- Text Classification - TensorFlow
        - Topics
- Amazon EC2 instance recommendation for the Text Classification - TensorFlow algorithm
- Text Classification - TensorFlow sample notebooks

The Amazon SageMaker AI Text Classification - TensorFlow algorithm is a supervised learning algorithm that supports transfer learning with many pretrained models from the TensorFlow Hub. Use transfer learning to fine-tune one of the available pretrained models on your own dataset, even if a large amount of text data is not available. The text classification algorithm takes a text string as input and outputs a probability for each of the class labels. Training datasets must be in CSV format. This page includes information about Amazon EC2 instance recommendations and sample notebooks for Text Classification - TensorFlow.

How to use the SageMaker AI Text Classification - TensorFlow algorithm

Input and output interface for the Text Classification - TensorFlow algorithm

Amazon EC2 instance recommendation for the Text Classification - TensorFlow algorithm

Text Classification - TensorFlow sample notebooks

How Text Classification - TensorFlow Works

TensorFlow Hub Models

Text Classification - TensorFlow Hyperparameters

Tune a Text Classification - TensorFlow model

The Text Classification - TensorFlow algorithm supports all CPU and GPU instances for training, including:

We recommend GPU instances with more memory for training with large batch sizes. Both CPU (such as M5) and GPU (P2, P3, G4dn, or G5) instances can be used for inference. For a comprehensive list of SageMaker training and inference instances across AWS Regions, see Amazon SageMaker Pricing.

For more information about how to use the SageMaker AI Text Classification - TensorFlow algorithm for transfer learning on a custom dataset, see the Introduction to JumpStart - Text Classification notebook.

For instructions how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, select the SageMaker AI Examples tab to see a list of all the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

**Examples:**

Example 1 (unknown):
```unknown
ml.p2.xlarge
```

Example 2 (unknown):
```unknown
ml.p2.16xlarge
```

Example 3 (unknown):
```unknown
ml.p3.2xlarge
```

Example 4 (unknown):
```unknown
ml.p3.16xlarge
```

---

## Data capture

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-capture.html

**Contents:**
- Data capture

To log the inputs to your endpoint and the inference outputs from your deployed model to Amazon S3, you can enable a feature called Data Capture. Data Capture is commonly used to record information that can be used for training, debugging, and monitoring. Amazon SageMaker Model Monitor automatically parses this captured data and compares metrics from this data with a baseline that you create for the model. For more information about Model Monitor see Data and model quality monitoring with Amazon SageMaker Model Monitor.

You can implement Data Capture for both real-time and batch model-monitor modes using the AWS SDK for Python (Boto) or the SageMaker Python SDK. For a real-time endpoint, you will specify your Data Capture configuration when you create your endpoint. Due to the persistent nature of your real-time endpoint, you can configure additional options to turn data capturing on or off at certain times, or change the sampling frequency. You can also choose to encrypt your inference data.

For a batch transform job, you can enable Data Capture if you want to run on-schedule model monitoring or continuous model-monitoring for regular, periodic batch transform jobs. You will specify your Data Capture configuration when you create your batch transform job. Within this configuration, you have the option to turn on encryption or generate the inference ID with your output, which helps you match your captured data to Ground Truth data.

---

## Recommendations for choosing the right data preparation tool in SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-prep.html

**Contents:**
- Recommendations for choosing the right data preparation tool in SageMaker AI
- Choose a feature
  - Use cases
  - Recommended features
  - Additional options

Data preparation in machine learning refers to the process of collecting, preprocessing, and organizing raw data to make it suitable for analysis and modeling. This step ensures that the data is in a format from which machine learning algorithms can effectively learn. Data preparation tasks may include handling missing values, removing outliers, scaling features, encoding categorical variables, assessing potential biases and taking steps to mitigate them, splitting data into training and testing sets, labeling, and other necessary transformations to optimize the quality and usability of the data for subsequent machine learning tasks.

There are 3 primary use cases for data preparation with Amazon SageMaker AI. Choose the use case that aligns with your requirements, and then refer to the corresponding recommended feature.

The following are the primary uses cases when performing data preparation for Machine Learning.

Use case 1: For those who prefer a visual interface, SageMaker AI provides ways to explore, prepare, and engineer features for model training through a point-and-click environment.

Use case 2: For users comfortable with coding who want more flexibility and control over data preparation, SageMaker AI integrates tools into its coding environments for exploration, transformations, and feature engineering.

Use case 3: For users focused on scalable data preparation, SageMaker AI offers serverless capabilities that leverage the Hadoop/Spark ecosystem for distributed processing of big data.

The following table outlines the key considerations and tradeoffs for the SageMaker AI features related to each data preparation use case for machine learning. To get started, identify the use case that aligns to your requirements and navigate to its recommended SageMaker AI feature.

Create data preparation pipelines

Perform data analysis

Transform data using built-in transforms

Use genAI-powered natural language instructions for data transforms

Optimized for tabular data tasks such as handling missing values, encoding categorical variables, and applying data transformations.

It may not be the optimal choice if your team already has expertise in Python, Spark, or other languages.

It might not be best suited if you need full flexibility to customize transformations to add complex business logic or require full control over your data processing environment.

This feature is designed for structured data residing in Amazon Redshift, Snowflake, Athena, or Ama

*[Content truncated]*

---

## Reserve training plans for your training jobs or HyperPod clusters

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/reserve-capacity-with-training-plans.html#training-plans-supported-instances-and-regions

**Contents:**
- Reserve training plans for your training jobs or HyperPod clusters
- What are SageMaker training plans
        - Note
- Benefits of SageMaker training plans
- SageMaker training plans advance reservation and flexible start times
        - Note
- SageMaker training plans user workflow
        - Note
- Supported instance types, AWS Regions, and pricing
        - Note

Amazon SageMaker training plans is a capability that allows you to reserve and help maximize the use of GPU capacity for large-scale AI model training workloads. This feature provides access to highly sought-after instance types that cover a range of GPU-accelerated computing options, including the latest NVIDIA GPU technologies and AWS trainium chips. With SageMaker training plans, you can secure predictable access to these high-demand, high-performance computational resources within your specified timelines and budgets, without the need to manage underlying infrastructure. This flexibility is particularly valuable for organizations dealing with the challenges of acquiring and scheduling these oversubscribed compute instances for their mission-critical AI workloads.

SageMaker training plans allow you to reserve compute capacity tailored to your target resource needs, such as SageMaker training jobs or SageMaker HyperPod clusters. The service automatically handles the reservation, provisioning of accelerated compute resources, infrastructure setup, workload execution, and recovery from infrastructure failures.

SageMaker training plans consist of one or more Reserved Capacity blocks, each defined by the following parameters:

Specific instance type

Quantity of instances

Training plans are specific to their target resource (either SageMaker Training Job or SageMaker HyperPod) and cannot be interchanged.

Multiple Reserved Capacity blocks in a single training plan may be discontinuous. This means there can be gaps between the Reserved Capacity blocks.

SageMaker training plans offer the following benefits:

Predictable Access: Reserve GPU capacity for your machine learning workloads within specified time frames.

Cost Management: Plan and budget for large-scale training requirements in advance.

Automated Resource Management: SageMaker training plans handle the provisioning and management of infrastructure.

Flexibility: Create training plans for various resources, including SageMaker training jobs and SageMaker HyperPod clusters.

Fault Tolerance: Benefit from automatic recovery from infrastructure failures and workload migration across Availability Zones for SageMaker AI training jobs.

SageMaker training plans allow you to reserve compute capacity in advance, with flexible start times and durations.

Advance reservation: You can reserve a training plan up to 8 weeks (56 days) in advance of the start date.

Minimum lead time: SageMaker training plans of

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
p6e-gb200.36xlarge
```

Example 2 (unknown):
```unknown
insufficient-data
```

---

## AutoGluon-Tabular

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/autogluon-tabular.html

**Contents:**
- AutoGluon-Tabular
- Amazon EC2 instance recommendation for the AutoGluon-Tabular algorithm
- AutoGluon-Tabular sample notebooks

AutoGluon-Tabular is a popular open-source AutoML framework that trains highly accurate machine learning models on an unprocessed tabular dataset. Unlike existing AutoML frameworks that primarily focus on model and hyperparameter selection, AutoGluon-Tabular succeeds by ensembling multiple models and stacking them in multiple layers. This page includes information about Amazon EC2 instance recommendations and sample notebooks for AutoGluon-Tabular.

SageMaker AI AutoGluon-Tabular supports single-instance CPU and single-instance GPU training. Despite higher per-instance costs, GPUs train more quickly, making them more cost effective. To take advantage of GPU training, specify the instance type as one of the GPU instances (for example, P3). SageMaker AI AutoGluon-Tabular currently does not support multi-GPU training.

The following table outlines a variety of sample notebooks that address different use cases of Amazon SageMaker AI AutoGluon-Tabular algorithm.

Tabular classification with Amazon SageMaker AI AutoGluon-Tabular algorithm

This notebook demonstrates the use of the Amazon SageMaker AI AutoGluon-Tabular algorithm to train and host a tabular classification model.

Tabular regression with Amazon SageMaker AI AutoGluon-Tabular algorithm

This notebook demonstrates the use of the Amazon SageMaker AI AutoGluon-Tabular algorithm to train and host a tabular regression model.

For instructions on how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, choose the SageMaker AI Examples tab to see a list of all of the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

---

## Running training jobs on a heterogeneous cluster

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/train-heterogeneous-cluster.html

**Contents:**
- Running training jobs on a heterogeneous cluster
        - Note
        - Note
        - Topics

Using the heterogeneous cluster feature of SageMaker Training, you can run a training job with multiple types of ML instances for a better resource scaling and utilization for different ML training tasks and purposes. For example, if your training job on a cluster with GPU instances suffers low GPU utilization and CPU bottleneck problems due to CPU-intensive tasks, using a heterogeneous cluster can help offload CPU-intensive tasks by adding more cost-efficient CPU instance groups, resolve such bottleneck problems, and achieve a better GPU utilization.

This feature is available in the SageMaker Python SDK v2.98.0 and later.

This feature is available through the SageMaker AI PyTorch and TensorFlow framework estimator classes. Supported frameworks are PyTorch v1.10 or later and TensorFlow v2.6 or later.

See also the blog Improve price performance of your model training using Amazon SageMaker AI heterogeneous clusters.

Configure a training job with a heterogeneous cluster in Amazon SageMaker AI

Run distributed training on a heterogeneous cluster in Amazon SageMaker AI

Modify your training script to assign instance groups

---

## Distributed computing with SageMaker AI best practices

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training-options.html#distributed-training-options-2

**Contents:**
- Distributed computing with SageMaker AI best practices
        - Topics
- Option 1: Use a SageMaker AI built-in algorithm that supports distributed training
- Option 2: Run a custom ML code in the SageMaker AI managed training or processing environment
  - If your ML code uses a deep learning framework
  - If your ML code involves tabular data processing
- Option 3: Write your own custom distributed training code
- Option 4: Launch multiple jobs in parallel or sequentially

This best practices page presents various flavors of distributed computing for machine learning (ML) jobs in general. The term distributed computing in this page encompasses distributed training for machine learning tasks and parallel computing for data processing, data generation, feature engineering, and reinforcement learning. In this page, we discuss about common challenges in distributed computing, and available options in SageMaker Training and SageMaker Processing. For additional reading materials about distributed computing, see What Is Distributed Computing?.

You can configure ML tasks to run in a distributed manner across multiple nodes (instances), accelerators (NVIDIA GPUs, AWS Trainium chips), and vCPU cores. By running distributed computation, you can achieve a variety of goals such as computing operations faster, handling large datasets, or training large ML models.

The following list covers common challenges that you might face when you run an ML training job at scale.

You need to make decisions on how to distribute computation depending on ML tasks, software libraries you want to use, and compute resources.

Not all ML tasks are straightforward to distribute. Also, not all ML libraries support distributed computation.

Distributed computation might not always result in a linear increase in compute efficiency. In particular, you need to identify if data I/O and inter-GPU communication have bottlenecks or cause overhead.

Distributed computation might disturb numerical processes and change model accuracy. Specifically to data-parallel neural network training, when you change the global batch size while scaling up to a larger compute cluster, you also need to adjust the learning rate accordingly.

SageMaker AI provides distributed training solutions to ease such challenges for various use cases. Choose one of the following options that best fits your use case.

Option 1: Use a SageMaker AI built-in algorithm that supports distributed training

Option 2: Run a custom ML code in the SageMaker AI managed training or processing environment

Option 3: Write your own custom distributed training code

Option 4: Launch multiple jobs in parallel or sequentially

SageMaker AI provides built-in algorithms that you can use out of the box through the SageMaker AI console or the SageMaker Python SDK. Using the built-in algorithms, you don’t need to spend time for code customization, understanding science behind the models, or running Docker on provision

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
tf.distribute
```

Example 2 (unknown):
```unknown
/opt/ml/input/config/resourceconfig.json
```

Example 3 (unknown):
```unknown
/opt/ml/config/resourceconfig.json
```

Example 4 (unknown):
```unknown
S3DataDistributionType=ShardedByS3Key
```

---

## Managed Spot Training in Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html

**Contents:**
- Managed Spot Training in Amazon SageMaker AI
        - Note

Amazon SageMaker AI makes it easy to train machine learning models using managed Amazon EC2 Spot instances. Managed spot training can optimize the cost of training models up to 90% over on-demand instances. SageMaker AI manages the Spot interruptions on your behalf.

Managed Spot Training uses Amazon EC2 Spot instance to run training jobs instead of on-demand instances. You can specify which training jobs use spot instances and a stopping condition that specifies how long SageMaker AI waits for a job to run using Amazon EC2 Spot instances. Metrics and logs generated during training runs are available in CloudWatch.

Amazon SageMaker AI automatic model tuning, also known as hyperparameter tuning, can use managed spot training. For more information on automatic model tuning, see Automatic model tuning with SageMaker AI.

Spot instances can be interrupted, causing jobs to take longer to start or finish. You can configure your managed spot training job to use checkpoints. SageMaker AI copies checkpoint data from a local path to Amazon S3. When the job is restarted, SageMaker AI copies the data from Amazon S3 back into the local path. The training job can then resume from the last checkpoint instead of restarting. For more information about checkpointing, see Checkpoints in Amazon SageMaker AI.

Unless your training job will complete quickly, we recommend you use checkpointing with managed spot training. SageMaker AI built-in algorithms and marketplace algorithms that do not checkpoint are currently limited to a MaxWaitTimeInSeconds of 3600 seconds (60 minutes).

To use managed spot training, create a training job. Set EnableManagedSpotTraining to True and specify the MaxWaitTimeInSeconds. MaxWaitTimeInSeconds must be larger than MaxRuntimeInSeconds. For more information about creating a training job, see DescribeTrainingJob.

You can calculate the savings from using managed spot training using the formula (1 - (BillableTimeInSeconds / TrainingTimeInSeconds)) * 100. For example, if BillableTimeInSeconds is 100 and TrainingTimeInSeconds is 500, this means that your training job ran for 500 seconds, but you were billed for only 100 seconds. Your savings is (1 - (100 / 500)) * 100 = 80%.

To learn how to run training jobs on Amazon SageMaker AI spot instances and how managed spot training works and reduces the billable time, see the following example notebooks:

Managed Spot Training with TensorFlow

Managed Spot Training with PyTorch

Managed Spot Training with X

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
MaxWaitTimeInSeconds
```

Example 2 (unknown):
```unknown
EnableManagedSpotTraining
```

Example 3 (unknown):
```unknown
MaxWaitTimeInSeconds
```

Example 4 (unknown):
```unknown
MaxWaitTimeInSeconds
```

---

## Define a pipeline

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/define-pipeline.html

**Contents:**
- Define a pipeline
        - Note
        - Topics
  - Create a Processing step
  - Create a Training step
  - Create a model package with a Register model step
  - Deploy the model to an endpoint with a Deploy model (endpoint) step
  - Define the Pipeline parameters
  - Save Pipeline
  - Prerequisites

To orchestrate your workflows with Amazon SageMaker Pipelines, you must generate a directed acyclic graph (DAG) in the form of a JSON pipeline definition. The DAG specifies the different steps involved in your ML process, such as data preprocessing, model training, model evaluation, and model deployment, as well as the dependencies and flow of data between these steps. The following topic shows you how to generate a pipeline definition.

You can generate your JSON pipeline definition using either the SageMaker Python SDK or the visual drag-and-drop Pipeline Designer feature in Amazon SageMaker Studio. The following image is a representation of the pipeline DAG that you create in this tutorial:

The pipeline that you define in the following sections solves a regression problem to determine the age of an abalone based on its physical measurements. For a runnable Jupyter notebook that includes the content in this tutorial, see Orchestrating Jobs with Amazon SageMaker Model Building Pipelines.

You can reference the model location as a property of the training step, as shown in the end-to-end example CustomerChurn pipeline in Github.

The following walkthrough guides you through the steps to create a barebones pipeline using the drag-and-drop Pipeline Designer. If you need to pause or end your Pipeline editing session in the visual designer at any time, click on the Export option. This allows you to download the current definition of your Pipeline to your local environment. Later, when you want to resume the Pipeline editing process, you can import the same JSON definition file into the visual designer.

To create a data processing job step, do the following:

Open the Studio console by following the instructions in Launch Amazon SageMaker Studio.

In the left navigation pane, select Pipelines.

In the left sidebar, choose Process data and drag it to the canvas.

In the canvas, choose the Process data step you added.

To add an input dataset, choose Add under Data (input) in the right sidebar and select a dataset.

To add a location to save output datasets, choose Add under Data (output) in the right sidebar and navigate to the destination.

Complete the remaining fields in the right sidebar. For information about the fields in these tabs, see sagemaker.workflow.steps.ProcessingStep.

To set up a model training step, do the following:

In the left sidebar, choose Train model and drag it to the canvas.

In the canvas, choose the Train model step you added.

To 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<your-role-arn>
```

Example 2 (unknown):
```unknown
{
    "Version":"2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "iam:PassRole"
            ],
            "Resource": "arn:aws:iam::111122223333:role/role-name"
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
                "iam:GetRole",
                "iam:PassRole"
            ],
            "Resource": "arn:aws:iam::111122223333:role/role-name"
        }
    ]
}
```

Example 4 (unknown):
```unknown
111122223333
```

---

## CloudWatch Logs for Amazon SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/logging-cloudwatch.html

**Contents:**
- CloudWatch Logs for Amazon SageMaker AI
        - Note

To help you debug your compilation jobs, processing jobs, training jobs, endpoints, transform jobs, notebook instances, and notebook instance lifecycle configurations, anything an algorithm container, a model container, or a notebook instance lifecycle configuration sends to stdout or stderr is also sent to Amazon CloudWatch Logs. In addition to debugging, you can use these for progress analysis.

By default, log data is stored in CloudWatch Logs indefinitely. However, you can configure how long to store log data in a log group. For information, see Change Log Data Retention in CloudWatch Logs in the Amazon CloudWatch Logs User Guide.

The following table lists all of the logs provided by Amazon SageMaker AI.

[compilation-job-name]

[production-variant-name]/[instance-id]

(For Asynchronous Inference endpoints) [production-variant-name]/[instance-id]/data-log

(For Inference Pipelines) [production-variant-name]/[instance-id]/[container-name provided in SageMaker AI model]

aws/sagemaker/groundtruth/worker-activity/[requester-AWS-Id]-[region]/[timestamp]

[inference-recommendations-job-name]/execution

[inference-recommendations-job-name]/CompilationJob/[compilation-job-name]

[inference-recommendations-job-name]/Endpoint/[endpoint-name]

[notebook-instance-name]/[LifecycleConfigHook]

[notebook-instance-name]/jupyter.log

[processing-job-name]/[hostname]-[epoch_timestamp]

[domain-id]/[user-profile-name]/[app-type]/[app-name]

[domain-id]/domain-shared/rstudioserverpro/default

[training-job-name]/algo-[instance-number-in-cluster]-[epoch_timestamp]

[transform-job-name]/[instance-id]-[epoch_timestamp]

[transform-job-name]/[instance-id]-[epoch_timestamp]/data-log

[transform-job-name]/[instance-id]-[epoch_timestamp]/[container-name provided in SageMaker AI model] (For Inference Pipelines)

1. The /aws/sagemaker/NotebookInstances/[LifecycleConfigHook] log stream is created when you create a notebook instance with a lifecycle configuration. For more information, see Customization of a SageMaker notebook instance using an LCC script.

2. For Inference Pipelines, if you don't provide container names, the platform uses **container-1, container-2**, and so on, corresponding to the order provided in the SageMaker AI model.

For more information about logging events with CloudWatch logging, see What is Amazon CloudWatch Logs? in the Amazon CloudWatch User Guide.

**Examples:**

Example 1 (unknown):
```unknown
/aws/sagemaker/CompilationJobs
```

Example 2 (unknown):
```unknown
[compilation-job-name]
```

Example 3 (unknown):
```unknown
/aws/sagemaker/Endpoints/[EndpointName]
```

Example 4 (unknown):
```unknown
[production-variant-name]/[instance-id]
```

---

## View SageMaker training plans quotas using the AWS management console

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/training-plan-quotas.html

**Contents:**
- View SageMaker training plans quotas using the AWS management console
        - Important

For pricing information about SageMaker training plans, see the Amazon SageMaker Pricing page. Navigate to the Amazon SageMaker HyperPod flexible training plans section under On-Demand Pricing. Choose your desired Region to view available instance types and their corresponding prices.

Make sure that your Training Jobs or HyperPod service quotas allow a maximum number of instances per instance type that exceeds the number of instances specified in your plan.

You can view the current quotas and limits for SageMaker training plans using the AWS Management Console.

To search for a specific quota value:

Open the Service Quotas console.

In the left navigation pane, choose AWS services.

From the AWS services list, search for and select Amazon SageMaker AI.

In the Service quotas list, you can see the service quota name, applied value (if it's available), AWS default quota, and whether the quota value is adjustable.

To find specific quotas, you can use the search bar at the top of the Service quotas list. Type the Limit Name of the quota you are searching for. For example, to find the quota for the number of training plans per region, you would type training-plan-total_count in the search bar.

The following table outlines the quota limit names for SageMaker training plans.

If you need higher limits for your SageMaker training plans, you may be able to request a quota increase. The ability to increase a quota depends on whether it's adjustable, which you can see in the Service quotas console.

To request a quota increase:

Navigate to the specific quota in the Service quotas console.

If the quota is adjustable, you can request a quota increase at either the account level or resource level based on the value listed in the Adjustability column.

For Increase quota value, enter the new value. The new value must be greater than the current value.

Quota increase requests are subject to review and approval by AWS. To view any pending or recently resolved requests in the console, navigate to the Request history tab from the service's details page, or choose Dashboard from the navigation pane. For pending requests, choose the status of the request to open the request receipt. The initial status of a request is Pending. After the status changes to Quota requested, you see the case number with AWS Support. Choose the case number to open the ticket for your request.

To learn more about requesting a quota increase in general, see Requesting a quota increase in the 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
training-plan-total_count
```

Example 2 (unknown):
```unknown
Quota requested
```

---

## SageMaker AI Managed Warm Pools

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/train-warm-pools.html

**Contents:**
- SageMaker AI Managed Warm Pools
        - Important
        - Topics
- How it works
        - Topics
  - Warm pool lifecycle
  - Warm pool creation
  - Matching training jobs
  - Maximum warm pool duration
  - Using persistent cache

SageMaker AI managed warm pools let you retain and reuse provisioned infrastructure after the completion of a training job to reduce latency for repetitive workloads, such as iterative experimentation or running many jobs consecutively. Subsequent training jobs that match specified parameters run on the retained warm pool infrastructure, which speeds up start times by reducing the time spent provisioning resources.

SageMaker AI managed warm pools are a billable resource. For more information, see Billing.

Request a warm pool quota increase

Use SageMaker AI managed warm pools

To use SageMaker AI managed warm pools and reduce latency between similar consecutive training jobs, create a training job that specifies a KeepAlivePeriodInSeconds value in its ResourceConfig. This value represents the duration of time in seconds to retain configured resources in a warm pool for subsequent training jobs. If you need to run several training jobs using similar configurations, you can further reduce latency and billable time by using a dedicated persistent cache directory to store and re-use your information in a different job.

Matching training jobs

Maximum warm pool duration

Using persistent cache

Create an initial training job with a KeepAlivePeriodInSeconds value greater than 0. When you run this first training job, this “cold-starts” a cluster with typical startup times.

When the first training job completes, the provisioned resources are kept alive in a warm pool for the period specified in the KeepAlivePeriodInSeconds value. As long as the cluster is healthy and the warm pool is within the specified KeepAlivePeriodInSeconds, then the warm pool status is Available.

The warm pool stays Available until it either identifies a matching training job for reuse or it exceeds the specified KeepAlivePeriodInSeconds and is terminated. The maximum length of time allowed for the KeepAlivePeriodInSeconds is 3600 seconds (60 minutes). If the warm pool status is Terminated, then this is the end of the warm pool lifecycle.

If the warm pool identifies a second training job with matching specifications such as instance count or instance type, then the warm pool moves from the first training job to the second training job for reuse. The status of the first training job warm pool becomes Reused. This is the end of the warm pool lifecycle for the first training job.

The status of the second training job that reused the warm pool becomes InUse. After the second training job 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
KeepAlivePeriodInSeconds
```

Example 2 (unknown):
```unknown
ResourceConfig
```

Example 3 (unknown):
```unknown
KeepAlivePeriodInSeconds
```

Example 4 (unknown):
```unknown
KeepAlivePeriodInSeconds
```

---

## Built-in algorithms and pretrained models in Amazon SageMaker

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html#algorithms-built-in-supervised-learning

**Contents:**
- Built-in algorithms and pretrained models in Amazon SageMaker
- Pre-trained models and solution templates
- Supervised learning
- Unsupervised learning
- Textual analysis
- Image processing
        - Topics

Amazon SageMaker provides a suite of built-in algorithms, pre-trained models, and pre-built solution templates to help data scientists and machine learning practitioners get started on training and deploying machine learning models quickly. For someone who is new to SageMaker, choosing the right algorithm for your particular use case can be a challenging task. The following table provides a quick cheat sheet that shows how you can start with an example problem or use case and find an appropriate built-in algorithm offered by SageMaker that is valid for that problem type. Additional guidance organized by learning paradigms (supervised and unsupervised) and important data domains (text and images) is provided in the sections following the table.

Table: Mapping use cases to built-in algorithms

Tabular Classification

Sentence Pair Classification

Named Entity Recognition

Instance Segmentation

Semantic Segmentation

Here a few examples out of the 15 problem types that can be addressed by the pre-trained models and pre-built solution templates provided by Amazon SageMaker JumpStart:

Question answering: chatbot that outputs an answer for a given question.

Text analysis: analyze texts from models specific to an industry domain such as finance.

Popular models, including Mobilenet, YOLO, Faster R-CNN, BERT, lightGBM, and CatBoost

For a list of pre-trained models available, see JumpStart Models.

For a list of pre-built solution templates available, see JumpStart Solutions.

Binary/multi-class classification

Predict if an item belongs to a category: an email spam filter

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Predict a numeric/continuous value: estimate the value of a house

AutoGluon-Tabular, CatBoost, Factorization Machines Algorithm, K-Nearest Neighbors (k-NN) Algorithm, LightGBM, Linear Learner Algorithm, TabTransformer, XGBoost algorithm with Amazon SageMaker AI

Time-series forecasting

Based on historical data for a behavior, predict future behavior: predict sales on a new product based on previous sales data.

Use the SageMaker AI DeepAR forecasting algorithm

Improve the data embeddings of the high-dimensional objects: identify duplicate support tickets or find the correct routing based on similarity of text in the tickets

Feature engineering: dimensionality reduction

Drop those columns from

*[Content truncated]*

---

## Recommendations for choosing the right data preparation tool in SageMaker AI

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/data-prep.html#data-prep-choose-use-cases

**Contents:**
- Recommendations for choosing the right data preparation tool in SageMaker AI
- Choose a feature
  - Use cases
  - Recommended features
  - Additional options

Data preparation in machine learning refers to the process of collecting, preprocessing, and organizing raw data to make it suitable for analysis and modeling. This step ensures that the data is in a format from which machine learning algorithms can effectively learn. Data preparation tasks may include handling missing values, removing outliers, scaling features, encoding categorical variables, assessing potential biases and taking steps to mitigate them, splitting data into training and testing sets, labeling, and other necessary transformations to optimize the quality and usability of the data for subsequent machine learning tasks.

There are 3 primary use cases for data preparation with Amazon SageMaker AI. Choose the use case that aligns with your requirements, and then refer to the corresponding recommended feature.

The following are the primary uses cases when performing data preparation for Machine Learning.

Use case 1: For those who prefer a visual interface, SageMaker AI provides ways to explore, prepare, and engineer features for model training through a point-and-click environment.

Use case 2: For users comfortable with coding who want more flexibility and control over data preparation, SageMaker AI integrates tools into its coding environments for exploration, transformations, and feature engineering.

Use case 3: For users focused on scalable data preparation, SageMaker AI offers serverless capabilities that leverage the Hadoop/Spark ecosystem for distributed processing of big data.

The following table outlines the key considerations and tradeoffs for the SageMaker AI features related to each data preparation use case for machine learning. To get started, identify the use case that aligns to your requirements and navigate to its recommended SageMaker AI feature.

Create data preparation pipelines

Perform data analysis

Transform data using built-in transforms

Use genAI-powered natural language instructions for data transforms

Optimized for tabular data tasks such as handling missing values, encoding categorical variables, and applying data transformations.

It may not be the optimal choice if your team already has expertise in Python, Spark, or other languages.

It might not be best suited if you need full flexibility to customize transformations to add complex business logic or require full control over your data processing environment.

This feature is designed for structured data residing in Amazon Redshift, Snowflake, Athena, or Ama

*[Content truncated]*

---

## Cluster-specific configurations

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/cluster-specific-configurations.html

**Contents:**
- Cluster-specific configurations
        - Topics

SageMaker HyperPod offers flexibility in running training jobs across different cluster environments. Each environment has its own configuration requirements and setup process. This section outlines the steps and configurations needed for running training jobs in SageMaker HyperPod Slurm, SageMaker HyperPod k8s, and SageMaker training jobs. Understanding these configurations is crucial for effectively leveraging the power of distributed training in your chosen environment.

You can use a recipe in the following cluster environments:

SageMaker HyperPod Slurm Orchestration

SageMaker HyperPod Amazon Elastic Kubernetes Service Orchestration

SageMaker training jobs

To launch a training job in a cluster, set and install the corresponding cluster configuration and environment.

Running a training job on HyperPod Slurm

Running a training job on HyperPod k8s

Running a SageMaker training job

---

## Feature Store storage configurations

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-storage-configurations.html

**Contents:**
- Feature Store storage configurations
        - Topics

Amazon SageMaker Feature Store consists of an online store and an offline store. The online store enables real-time lookup of features for inference, while the offline store contains historical data for model training and batch inference. When creating a feature group, you have the option of enabling either the online store, offline store, or both. When you enable both, they sync to avoid discrepancies between training and serving data. For more information about the online and offline stores and other Feature Store concepts, see Feature Store concepts.

The following topics discuss online store storage types and offline store table formats.

---

## Image Classification - TensorFlow

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/image-classification-tensorflow.html

**Contents:**
- Image Classification - TensorFlow
        - Topics
- Amazon EC2 instance recommendation for the Image Classification - TensorFlow algorithm
- Image Classification - TensorFlow sample notebooks

The Amazon SageMaker Image Classification - TensorFlow algorithm is a supervised learning algorithm that supports transfer learning with many pretrained models from the TensorFlow Hub. Use transfer learning to fine-tune one of the available pretrained models on your own dataset, even if a large amount of image data is not available. The image classification algorithm takes an image as input and outputs a probability for each provided class label. Training datasets must consist of images in .jpg, .jpeg, or .png format. This page includes information about Amazon EC2 instance recommendations and sample notebooks for Image Classification - TensorFlow.

How to use the SageMaker Image Classification - TensorFlow algorithm

Input and output interface for the Image Classification - TensorFlow algorithm

Amazon EC2 instance recommendation for the Image Classification - TensorFlow algorithm

Image Classification - TensorFlow sample notebooks

How Image Classification - TensorFlow Works

TensorFlow Hub Models

Image Classification - TensorFlow Hyperparameters

Tune an Image Classification - TensorFlow model

The Image Classification - TensorFlow algorithm supports all CPU and GPU instances for training, including:

We recommend GPU instances with more memory for training with large batch sizes. Both CPU (such as M5) and GPU (P2, P3, G4dn, or G5) instances can be used for inference.

For more information about how to use the SageMaker Image Classification - TensorFlow algorithm for transfer learning on a custom dataset, see the Introduction to SageMaker TensorFlow - Image Classification notebook.

For instructions how to create and access Jupyter notebook instances that you can use to run the example in SageMaker AI, see Amazon SageMaker notebook instances. After you have created a notebook instance and opened it, select the SageMaker AI Examples tab to see a list of all the SageMaker AI samples. To open a notebook, choose its Use tab and choose Create copy.

**Examples:**

Example 1 (unknown):
```unknown
ml.p2.xlarge
```

Example 2 (unknown):
```unknown
ml.p2.16xlarge
```

Example 3 (unknown):
```unknown
ml.p3.2xlarge
```

Example 4 (unknown):
```unknown
ml.p3.16xlarge
```

---

## Profile and optimize computational performance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/train-profile-computational-performance.html

**Contents:**
- Profile and optimize computational performance
        - Topics

When training state-of-the-art deep learning models that rapidly grow in size, scaling the training job of such models to a large GPU cluster and identifying computational performance issues from billions and trillions of operations and communications in every iteration of the gradient descent process become a challenge.

SageMaker AI provides profiling tools to visualize and diagnose such complex computation issues arising from running training jobs on AWS cloud computing resources. There are two profiling options that SageMaker AI offers: Amazon SageMaker Profiler and a resource utilzation monitor in Amazon SageMaker Studio Classic. See the following introductions of the two functionalities to gain quick insights and learn which one to use depending on your needs.

Amazon SageMaker Profiler

Amazon SageMaker Profiler is a profiling capability of SageMaker AI with which you can deep dive into compute resources provisioned while training deep learning models, and gain visibility into operation-level details. SageMaker Profiler provides Python modules for adding annotations throughout PyTorch or TensorFlow training scripts and activating SageMaker Profiler. You can access the modules through the SageMaker Python SDK and AWS Deep Learning Containers.

With SageMaker Profiler, you can track all activities on CPUs and GPUs, such as CPU and GPU utilizations, kernel runs on GPUs, kernel launches on CPUs, sync operations, memory operations across CPUs and GPUs, latencies between kernel launches and corresponding runs, and data transfer between CPUs and GPUs.

SageMaker Profiler also offers a user interface (UI) that visualizes the profile, a statistical summary of profiled events, and the timeline of a training job for tracking and understanding the time relationship of the events between GPUs and CPUs.

To learn more about SageMaker Profiler, see Amazon SageMaker Profiler.

Monitoring AWS compute resources in Amazon SageMaker Studio Classic

SageMaker AI also provides a user interface in Studio Classic for monitoring resource utilization at high level, but with more granularity compared to the default utilization metrics collected from SageMaker AI to CloudWatch.

For any training job you run in SageMaker AI using the SageMaker Python SDK, SageMaker AI starts profiling basic resource utilization metrics, such as CPU utilization, GPU utilization, GPU memory utilization, network, and I/O wait time. It collects these resource utilization metrics every 500 milliseco

*[Content truncated]*

---

## Bias drift for models in production

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-monitor-bias-drift.html

**Contents:**
- Bias drift for models in production
- Model Monitor Sample Notebook
        - Topics

Amazon SageMaker Clarify bias monitoring helps data scientists and ML engineers monitor predictions for bias on a regular basis. As the model is monitored, customers can view exportable reports and graphs detailing bias in SageMaker Studio and configure alerts in Amazon CloudWatch to receive notifications if bias beyond a certain threshold is detected. Bias can be introduced or exacerbated in deployed ML models when the training data differs from the data that the model sees during deployment (that is, the live data). These kinds of changes in the live data distribution might be temporary (for example, due to some short-lived, real-world events) or permanent. In either case, it might be important to detect these changes. For example, the outputs of a model for predicting home prices can become biased if the mortgage rates used to train the model differ from current, real-world mortgage rates. With bias detection capabilities in Model Monitor, when SageMaker AI detects bias beyond a certain threshold, it automatically generates metrics that you can view in SageMaker Studio and through Amazon CloudWatch alerts.

In general, measuring bias only during the train-and-deploy phase might not be sufficient. It is possible that after the model has been deployed, the distribution of the data that the deployed model sees (that is, the live data) is different from data distribution in the training dataset. This change might introduce bias in a model over time. The change in the live data distribution might be temporary (for example, due to some short-lived behavior like the holiday season) or permanent. In either case, it might be important to detect these changes and take steps to reduce the bias when appropriate.

To detect these changes, SageMaker Clarify provides functionality to monitor the bias metrics of a deployed model continuously and raise automated alerts if the metrics exceed a threshold. For example, consider the DPPL bias metric. Specify an allowed range of values A=(amin​,amax​), for instance an interval of (-0.1, 0.1), that DPPL should belong to during deployment. Any deviation from this range should raise a bias detected alert. With SageMaker Clarify, you can perform these checks at regular intervals.

For example, you can set the frequency of the checks to 2 days. This means that SageMaker Clarify computes the DPPL metric on data collected during a 2-day window. In this example, Dwin​ is the data that the model processed during last 2-day window. An

*[Content truncated]*

---

## MLOps Automation With SageMaker Projects

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html

**Contents:**
- MLOps Automation With SageMaker Projects
        - Topics

Create end-to-end ML solutions with CI/CD by using SageMaker Projects.

Use SageMaker Projects to create a MLOps solution to orchestrate and manage:

Building custom images for processing, training, and inference

Data preparation and feature engineering

Monitoring and updating models

What is a SageMaker AI Project?

Granting SageMaker Studio Permissions Required to Use Projects

Create a MLOps Project using Amazon SageMaker Studio or Studio Classic

MLOps Project Templates

View Project Resources

Update a MLOps Project in Amazon SageMaker Studio or Studio Classic

Delete a MLOps Project using Amazon SageMaker Studio or Studio Classic

Walk Through a SageMaker AI MLOps Project Using Third-party Git Repos

---

## Use Amazon SageMaker Ground Truth Plus to Label Data

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/gtp.html

**Contents:**
- Use Amazon SageMaker Ground Truth Plus to Label Data
        - Why use SageMaker Ground Truth Plus?
        - Important
        - How does SageMaker Ground Truth Plus work?
        - How do I use SageMaker Ground Truth Plus?

Amazon SageMaker Ground Truth Plus is a turnkey data labeling service that uses an expert workforce to deliver high-quality annotations quickly and reduces costs by up to 40%. Using SageMaker Ground Truth Plus, data scientists and business managers, such as data operations managers and program managers, can create high-quality training datasets without having to build labeling applications and manage labeling workforces on their own. You can get started with Amazon SageMaker Ground Truth Plus by uploading data along with the labeling requirements in Amazon S3.

To train a machine learning (ML) model, data scientists need large, high-quality, labeled datasets. As ML adoption grows, labeling needs increase. This forces data scientists to spend weeks on building data labeling workflows and managing a data labeling workforce. Unfortunately, this slows down innovation and increases cost. To ensure data scientists can spend their time building, training, and deploying ML models, data scientists typically task other in-house teams consisting of data operations managers and program managers to produce high-quality training datasets. However, these teams typically don't have access to skills required to deliver high-quality training datasets, which affects ML results. As a result, you look for a data labeling partner that can help them create high-quality training datasets at scale without consuming their in-house resources.

When you upload the data, SageMaker Ground Truth Plus sets up the data labeling workflows and operates them on your behalf. From there, an expert workforce trained on a varierty of machine learning (ML) tasks performs data labeling. SageMaker Ground Truth Plus currently offers two types of expert workforce: an Amazon employed workforce and a curated list of third-party vendors. SageMaker Ground Truth Plus provides you with the flexibility to choose the labeling workforce. AWS experts select the best labeling workforce based on your project requirements. For example, if you need people proficient in labeling audio files, specify that in the guidelines provided to SageMaker Ground Truth Plus, and the service automatically selects labelers with those skills.

SageMaker Ground Truth Plus does not support PHI, PCI or FedRAMP certified data, and you should not provide this data to SageMaker Ground Truth Plus.

There are five main components to a workflow.

Creating a project team

Accessing the project portal to monitor progress of training datasets

*[Content truncated]*

---

## Debugging and improving model performance

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/train-debug-and-improve-model-performance.html

**Contents:**
- Debugging and improving model performance
        - Topics

The essence of training machine learning models, deep learning neural networks, transformer models is in achieving stable model convergence, and as such, state-of-the-art models have millions, billions, or trillions of model parameters. The number of operations to update the gigantic number of model parameters during each iteration can easily become astronomical. To identify model convergence issues, it is important to be able to access the model parameters, activations, and gradients computed during optimization processes.

Amazon SageMaker AI provides two debugging tools to help identify such convergence issues and gain visibility into your models.

Amazon SageMaker AI with TensorBoard

To offer greater compatibility with the open-source community tools within the SageMaker AI Training platform, SageMaker AI hosts TensorBoard as an application in SageMaker AI domain. You can bring your training jobs to SageMaker AI and keep using the TensorBoard summary writer to collect the model output tensors. Because TensorBoard is implemented into SageMaker AI domain, it also gives you more options to manage user profiles under the SageMaker AI domain in your AWS account, and provides fine control over the user profiles by granting access to specific actions and resources. To learn more, see TensorBoard in Amazon SageMaker AI.

Amazon SageMaker Debugger

Amazon SageMaker Debugger is a capability of SageMaker AI that provides tools to register hooks to callbacks to extract model output tensors and save them in Amazon Simple Storage Service. It provides built-in rules for detecting model convergence issues, such as overfitting, saturated activation functions, vanishing gradients, and more. You can also set up the built-in rules with Amazon CloudWatch Events and AWS Lambda for taking automated actions against detected issues, and set up Amazon Simple Notification Service to receive email or text notifications. To learn more, see Amazon SageMaker Debugger.

TensorBoard in Amazon SageMaker AI

Amazon SageMaker Debugger

Access a training container through AWS Systems Manager for remote debugging

Release notes for debugging capabilities of Amazon SageMaker AI

---

## Types of Algorithms

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html

**Contents:**
- Types of Algorithms
        - Topics
- Choose an algorithm implementation
        - Topics
  - Use a built-in algorithm
  - Use script mode in a supported framework
  - Use a custom Docker image
- Problem types for the basic machine learning paradigms
        - Topics
  - Supervised learning

Machine learning can help you accomplish empirical tasks that require some sort of inductive inference. This task involves induction as it uses data to train algorithms to make generalizable inferences. This means that the algorithms can make statistically reliable predictions or decisions, or complete other tasks when applied to new data that was not used to train them.

To help you select the best algorithm for your task, we classify these tasks on various levels of abstraction. At the highest level of abstraction, machine learning attempts to find patterns or relationships between features or less structured items, such as text in a data set. Pattern recognition techniques can be classified into distinct machine learning paradigms, each of which address specific problem types. There are currently three basic paradigms for machine learning used to address various problem types:

Unsupervised learning

Reinforcement learning

The types of problems that each learning paradigm can address are identified by considering the inferences (or predictions, decisions, or other tasks) you want to make from the type of data that you have or could collect. Machine learning paradigms use algorithmic methods to address their various problem types. The algorithms provide recipes for solving these problems.

However, many algorithms, such as neural networks, can be deployed with different learning paradigms and on different types of problems. Multiple algorithms can also address a specific problem type. Some algorithms are more generally applicable and others are quite specific for certain kinds of objectives and data. So the mapping between machine learning algorithms and problem types is many-to-many. Also, there are various implementation options available for algorithms.

The following sections provide guidance concerning implementation options, machine learning paradigms, and algorithms appropriate for different problem types.

Choose an algorithm implementation

Problem types for the basic machine learning paradigms

Built-in algorithms and pretrained models in Amazon SageMaker

Use Reinforcement Learning with Amazon SageMaker AI

After choosing an algorithm, you must decide which implementation of it you want to use. Amazon SageMaker AI supports three implementation options that require increasing levels of effort.

Pre-trained models require the least effort and are models ready to deploy or to fine-tune and deploy using SageMaker JumpStart.

Built-in algorithms r

*[Content truncated]*

---

## Training data labeling using humans with Amazon SageMaker Ground Truth

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html

**Contents:**
- Training data labeling using humans with Amazon SageMaker Ground Truth
- Are You a First-time User of Ground Truth?

To train a machine learning model, you need a large, high-quality, labeled dataset. Ground Truth helps you build high-quality training datasets for your machine learning models. With Ground Truth, you can use workers from either Amazon Mechanical Turk, a vendor company that you choose, or an internal, private workforce along with machine learning to enable you to create a labeled dataset. You can use the labeled dataset output from Ground Truth to train your own models. You can also use the output as a training dataset for an Amazon SageMaker AI model.

Depending on your ML application, you can choose from one of the Ground Truth built-in task types to have workers generate specific types of labels for your data. You can also build a custom labeling workflow to provide your own UI and tools to workers labeling your data. To learn more about the Ground Truth built in task types, see Built-in Task Types. To learn how to create a custom labeling workflow, see Custom labeling workflows.

In order to automate labeling your training dataset, you can optionally use automated data labeling, a Ground Truth process that uses machine learning to decide which data needs to be labeled by humans. Automated data labeling may reduce the labeling time and manual effort required. For more information, see Automate data labeling. To create a custom labeling workflow, see Custom labeling workflows.

Use either pre-built or custom tools to assign the labeling tasks for your training dataset. A labeling UI template is a webpage that Ground Truth uses to present tasks and instructions to your workers. The SageMaker AI console provides built-in templates for labeling data. You can use these templates to get started , or you can build your own tasks and instructions by using our HTML 2.0 components. For more information, see Custom labeling workflows.

Use the workforce of your choice to label your dataset. You can choose your workforce from:

The Amazon Mechanical Turk workforce of over 500,000 independent contractors worldwide.

A private workforce that you create from your employees or contractors for handling data within your organization.

A vendor company that you can find in the AWS Marketplace that specializes in data labeling services.

For more information, see Workforces.

You store your datasets in Amazon S3 buckets. The buckets contain three things: The data to be labeled, an input manifest file that Ground Truth uses to read the data files, and an output manifest fil

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
/aws/sagemaker/LabelingJobs
```

---

## AWS managed policies for Amazon SageMaker HyperPod

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-hyperpod.html

**Contents:**
- AWS managed policies for Amazon SageMaker HyperPod
        - Topics
- Amazon SageMaker AI updates to SageMaker HyperPod managed policies

The following AWS managed policies add permissions required to use Amazon SageMaker HyperPod. The policies are available in your AWS account and are used by execution roles created from the SageMaker AI console or the HyperPod service-linked role.

AWS managed policy: AmazonSageMakerHyperPodTrainingOperatorAccess

AWS managed policy: AmazonSageMakerHyperPodObservabilityAdminAccess

AWS managed policy: AmazonSageMakerHyperPodServiceRolePolicy

AWS managed policy: AmazonSageMakerClusterInstanceRolePolicy

Amazon SageMaker AI updates to SageMaker HyperPod managed policies

View details about updates to AWS managed policies for SageMaker HyperPod since this service began tracking these changes. For automatic alerts about changes to this page, subscribe to the RSS feed on the SageMaker AI Document history page.

AmazonSageMakerHyperPodTrainingOperatorAccess - New policy

AmazonSageMakerHyperPodObservabilityAdminAccess - Updated policy

Updated the policy to fix the role scope-down to include the service-role prefix. Also added permissions for eks:DeletePodIdentityAssociation and eks:UpdatePodIdentityAssociation that are required for end-to-end administrative actions.

AmazonSageMakerHyperPodObservabilityAdminAccess - New policy

AmazonSageMakerHyperPodServiceRolePolicy - New policy

AmazonSageMakerClusterInstanceRolePolicy - New policy

**Examples:**

Example 1 (unknown):
```unknown
service-role
```

Example 2 (unknown):
```unknown
eks:DeletePodIdentityAssociation
```

Example 3 (unknown):
```unknown
eks:UpdatePodIdentityAssociation
```

---
