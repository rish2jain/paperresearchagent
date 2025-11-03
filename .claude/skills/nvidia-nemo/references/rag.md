# Nvidia-Nemo - Rag

**Pages:** 3

---

## Generative AI

**URL:** https://developer.nvidia.com/nemo

**Contents:**
- How Generative AI Works
- Explore Generative AI Tools and Technologies
  - NVIDIA Nemotron
  - NVIDIA Cosmos
  - NVIDIA NIM
  - NVIDIA Dynamo
  - NVIDIA TensorRT
  - AI-Q NVIDIA Blueprint
  - NVIDIA AI Blueprints
  - NVIDIA Riva

Generative AI models learn by recognizing patterns and structures within massive datasets of text, code, images, audio, video, and other data. These models use neural networks, often transformer networks, to process the information. Developers can then leverage the models to generate new content, enhance existing content, or create entirely new AI-powered applications. Retrieval-augmented generation (RAG) takes this further by integrating external knowledge sources, enabling AI to retrieve and synthesize up-to-date and contextually relevant information. This approach improves accuracy and can be used for tasks like creating realistic images from text descriptions, generating musical compositions, or building intelligent AI chatbots that can engage in human-like conversations.

NVIDIA Nemotron™ is a family of most open and efficient multimodal models, with open datasets and recipes for building agentic AI.

NVIDIA Cosmos™ is a platform of state-of-the-art generative world foundation models and data processing pipelines that accelerate the development of highly performant physical AI systems, such as robots and self-driving cars.

NVIDIA NIM™ is a set of easy-to-use microservices designed to accelerate the deployment of generative AI models across any cloud or data center.

NVIDIA Dynamo is an open-source, low-latency inference framework for serving generative AI models in distributed environments. It scales inference workloads across large GPU fleets with optimized resource scheduling, memory management, and data transfer, and it supports all major AI inference backends.

NVIDIA TensorRT™ is an ecosystem of APIs for high-performance deep learning inference. TensorRT includes an inference runtime and model optimizations that deliver low latency and high throughput for production applications.

AI-Q is an NVIDIA AI Blueprint for building AI agents that can access, query, and act on business knowledge using tools like advanced RAG and reasoning models. They transform enterprise data into an accessible, actionable resource.

NVIDIA AI Blueprints are comprehensive reference workflows that accelerate AI application development and deployment. They feature NVIDIA acceleration libraries, SDKs, and microservices for AI agents, digital twins, and more.

NVIDIA Riva is a GPU-accelerated multilingual speech and translation AI SDK for building and deploying fully customizable, real-time conversational AI pipelines.

NVIDIA NeMo™ Data Designer generates high-quality, domain-specific synthetic data and annotations to accelerate model training and evaluation.

---

## NVIDIA NeMo Evaluator for Developers

**URL:** https://developer.nvidia.com/nemo-evaluator

**Contents:**
- NVIDIA NeMo Evaluator for Developers
- NVIDIA NeMo Evaluator Key Features
- SDK
- Microservice
- How NVIDIA NeMo Microservices Evaluator Works
- Introductory Resources
  - Introductory Blog
  - Tutorial Notebook
  - Introductory Webinar
  - How-To Blog

NVIDIA NeMo™ Evaluator is a scalable solution for evaluating generative AI applications—including large language models (LLMs), retrieval-augmented generation (RAG) pipelines, and AI agents—available as both an open-source SDK for experimentation and a cloud-native microservice for automated, enterprise-grade workflows. NeMo Evaluator SDK supports over 100 built-in academic benchmarks and an easy-to-follow process for adding customizable metrics via open-source contribution. In addition to academic benchmarks, NeMo Evaluator microservice provides LLM-as-a-judge scoring, RAG, and agent metrics that make it easy to assess and optimize models across environments. NeMo Evaluator is a part of the NVIDIA NeMo™ software suite for building, monitoring, and optimizing AI agents across their lifecycle at enterprise scale.

Access SDK Quickstart Download MicroserviceDocumentation

NeMo Evaluator is built on a single-core engine that powers both the open-source SDK and the enterprise-ready microservice.

An open-source SDK for running academic benchmarks with reproducibility and scale. Built on the nemo-evaluator core and launcher, it provides code-native access for experimentation on LLMs, embeddings, and reranking models.

Reproducible by default: Captures configs, seeds, and software provenance for auditable, repeatable results.

Comprehensive benchmarks: Over 100 academic benchmarks across leading harnesses and modalities, continuously updated.

Python-native and ready to run: Configs and containers deliver results directly in notebooks or scripts.

Flexible and scalable: Run locally with Docker or scale out to Slurm clusters.

An enterprise-grade, cloud-native REST API that automates scalable evaluation pipelines. Teams can submit jobs, configure parameters, and monitor results centrally—ideal for CI/CD integration and production-ready generative AI operations workflows.

Automates scalable evaluation pipelines with a simple REST API.

Abstracts complexity: Submit “jobs,” configure parameters, and monitor results centrally.

NeMo Evaluator microservice allows a user to run various evaluation jobs for agentic AI applications through a REST API. Evaluation flows enabled include: academic benchmarking, agentic and RAG metrics, and LLM-as-a-judge. A user can also tune their judge model via the prompt optimization feature.

Read how the NeMo Evaluator microservice simplifies end-to-end evaluation of generative AI systems.

Explore tutorials designed to help you evalua

*[Content truncated]*

---

## NVIDIA NeMo Evaluator for Developers

**URL:** https://developer.nvidia.com/nemo-evaluator/

**Contents:**
- NVIDIA NeMo Evaluator for Developers
- NVIDIA NeMo Evaluator Key Features
- SDK
- Microservice
- How NVIDIA NeMo Microservices Evaluator Works
- Introductory Resources
  - Introductory Blog
  - Tutorial Notebook
  - Introductory Webinar
  - How-To Blog

NVIDIA NeMo™ Evaluator is a scalable solution for evaluating generative AI applications—including large language models (LLMs), retrieval-augmented generation (RAG) pipelines, and AI agents—available as both an open-source SDK for experimentation and a cloud-native microservice for automated, enterprise-grade workflows. NeMo Evaluator SDK supports over 100 built-in academic benchmarks and an easy-to-follow process for adding customizable metrics via open-source contribution. In addition to academic benchmarks, NeMo Evaluator microservice provides LLM-as-a-judge scoring, RAG, and agent metrics that make it easy to assess and optimize models across environments. NeMo Evaluator is a part of the NVIDIA NeMo™ software suite for building, monitoring, and optimizing AI agents across their lifecycle at enterprise scale.

Access SDK Quickstart Download MicroserviceDocumentation

NeMo Evaluator is built on a single-core engine that powers both the open-source SDK and the enterprise-ready microservice.

An open-source SDK for running academic benchmarks with reproducibility and scale. Built on the nemo-evaluator core and launcher, it provides code-native access for experimentation on LLMs, embeddings, and reranking models.

Reproducible by default: Captures configs, seeds, and software provenance for auditable, repeatable results.

Comprehensive benchmarks: Over 100 academic benchmarks across leading harnesses and modalities, continuously updated.

Python-native and ready to run: Configs and containers deliver results directly in notebooks or scripts.

Flexible and scalable: Run locally with Docker or scale out to Slurm clusters.

An enterprise-grade, cloud-native REST API that automates scalable evaluation pipelines. Teams can submit jobs, configure parameters, and monitor results centrally—ideal for CI/CD integration and production-ready generative AI operations workflows.

Automates scalable evaluation pipelines with a simple REST API.

Abstracts complexity: Submit “jobs,” configure parameters, and monitor results centrally.

NeMo Evaluator microservice allows a user to run various evaluation jobs for agentic AI applications through a REST API. Evaluation flows enabled include: academic benchmarking, agentic and RAG metrics, and LLM-as-a-judge. A user can also tune their judge model via the prompt optimization feature.

Read how the NeMo Evaluator microservice simplifies end-to-end evaluation of generative AI systems.

Explore tutorials designed to help you evalua

*[Content truncated]*

---
