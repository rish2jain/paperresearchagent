# Aws-Sagemaker - Endpoints

**Pages:** 2

---

## Model deployment at the edge with SageMaker Edge Manager

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/edge.html

**Contents:**
- Model deployment at the edge with SageMaker Edge Manager
        - Warning
- Why Use Edge Manager?
- How Does it Work?
- How Do I Use SageMaker Edge Manager?

SageMaker Edge Manager is being discontinued on April 26th, 2024. For more information about continuing to deploy your models to edge devices, see SageMaker Edge Manager end of life.

Amazon SageMaker Edge Manager provides model management for edge devices so you can optimize, secure, monitor, and maintain machine learning models on fleets of edge devices such as smart cameras, robots, personal computers, and mobile devices.

Many machine learning (ML) use cases require running ML models on a fleet of edge devices, which allows you to get predictions in real-time, preserves the privacy of the end users, and lowers the cost of network connectivity. With the increasing availability of low-power edge hardware designed for ML, it is now possible to run multiple complex neural network models on edge devices.

However, operating ML models on edge devices is challenging, because devices, unlike cloud instances, have limited compute, memory, and connectivity. After the model is deployed, you need to continuously monitor the models, because model drift can cause the quality of model to decay overtime. Monitoring models across your device fleets is difficult because you need to write custom code to collect data samples from your device and recognize skew in predictions. In addition, models are often hard-coded into the application. To update the model, you must rebuild and update the entire application or device firmware, which can disrupt your operations.

With SageMaker Edge Manager, you can optimize, run, monitor, and update machine learning models across fleets of devices at the edge.

At a high level, there are five main components in the SageMaker Edge Manager workflow: compiling models with SageMaker Neo, packaging Neo-compiled models, deploying models to your devices, running models on the SageMaker AI inference engine (Edge Manager agent), and maintaining models on the devices.

SageMaker Edge Manager uses SageMaker Neo to optimize your models for the target hardware in one click, then to cryptographically sign your models before deployment. Using SageMaker Edge Manager, you can sample model input and output data from edge devices and send it to the cloud for monitoring and analysis, and view a dashboard that tracks and visually reports on the operation of the deployed models within the SageMaker AI console.

SageMaker Edge Manager extends capabilities that were previously only available in the cloud to the edge, so developers can continuously improve model

*[Content truncated]*

---

## Deploy your models to an endpoint

**URL:** https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-deploy-model.html

**Contents:**
- Deploy your models to an endpoint
- Permissions management
- Deploy a model
        - Note
        - Note

In Amazon SageMaker Canvas, you can deploy your models to an endpoint to make predictions. SageMaker AI provides the ML infrastructure for you to host your model on an endpoint with the compute instances that you choose. Then, you can invoke the endpoint (send a prediction request) and get a real-time prediction from your model. With this functionality, you can use your model in production to respond to incoming requests, and you can integrate your model with existing applications and workflows.

To get started, you should have a model that you'd like to deploy. You can deploy custom model versions that you've built, Amazon SageMaker JumpStart foundation models, and fine-tuned JumpStart foundation models. For more information about building a model in Canvas, see How custom models work. For more information about JumpStart foundation models in Canvas, see Generative AI foundation models in SageMaker Canvas.

Review the following Permissions management section, and then begin creating new deployments in the Deploy a model section.

By default, you have permissions to deploy models to SageMaker AI Hosting endpoints. SageMaker AI grants these permissions for all new and existing Canvas user profiles through the AmazonSageMakerCanvasFullAccess policy, which is attached to the AWS IAM execution role for the SageMaker AI domain that hosts your Canvas application.

If your Canvas administrator is setting up a new domain or user profile, when they're setting up the domain and following the prerequisite instructions in the Prerequisites for setting up Amazon SageMaker Canvas, SageMaker AI turns on the model deployment permissions through the Enable direct deployment of Canvas models option, which is enabled by default.

The Canvas administrator can manage model deployment permissions at the user profile level as well. For example, if the administrator doesn't want to grant model deployment permissions to all user profiles when setting up a domain, they can grant permissions to specific users after creating the domain.

The following procedure shows how to modify the model deployment permissions for a specific user profile:

Open the SageMaker AI console at https://console.aws.amazon.com/sagemaker/.

On the left navigation pane, choose Admin configurations.

Under Admin configurations, choose Domains.

From the list of domains, select the user profile’s domain.

On the Domain details page, select the User profiles tab.

Choose your User profile.

On the user profile

*[Content truncated]*

---
