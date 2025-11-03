# Nvidia-Nemo - Other

**Pages:** 7

---

## NVIDIA NeMo Curator for Developers

**URL:** https://developer.nvidia.com/nemo-curator/

**Contents:**
- NVIDIA NeMo Curator for Developers
- How NVIDIA NeMo Curator Works
  - Text Data Processing
  - Synthetic Data Generation
  - Video Data Processing
  - Audio Data Processing
  - Image Data Processing
- Introductory Resources
  - Introductory Blog
  - Tutorials

NVIDIA NeMo™ Curator improves generative AI model accuracy by processing text, image, and video data at scale for training and customization. It also provides prebuilt pipelines for generating synthetic data to customize and evaluate generative AI systems.With NeMo Curator, part of the NVIDIA NeMo software suite for managing the AI agent lifecycle, developers can curate high-quality data and train highly accurate generative AI models for various industries, including finance, retail, manufacturing and telecommunications.NeMo Curator, along with NeMo microservices enables developers to create data flywheels and continuously optimize generative AI agents, enhancing the overall experience for end users.

DownloadDocumentationForum

NeMo Curator streamlines data-processing tasks, such as data downloading, extraction, cleaning, quality filtering, deduplication, and blending or shuffling, providing them as Pythonic APIs, making it easier for developers to build data-processing pipelines. High-quality data processed from NeMo Curator enables you to achieve higher accuracy with less data and faster model convergence, reducing training time. NeMo Curator supports the processing of text, image, and video modalities and can scale up to 100+ PB of data.NeMo Curator provides a customizable and modular interface, allowing you to select the building blocks for your data processing pipelines. Please refer to the architecture diagrams below to see how you can build data processing pipelines.

This architecture diagram shows the various features available for processing text. At a high level, a typical text processing pipeline begins with downloading data from public sources or private repositories and performing cleaning steps, such as fixing Unicode characters. Next, heuristic filters—such as word count—are applied, followed by deduplication, advanced quality filtering using classifier models for quality and domain, and finally, data blending.

NeMo Curator has a simple, easy-to-use set of tools that let you use pre-built synthetic data generation pipelines or build your own. Any model inference service that uses the OpenAI API is compatible with the synthetic data generation module, allowing you to generate your data from any model.NeMo Curator provides pre-built pipelines for several use cases to help you get started easily, including evaluating and customizing embedding models, prompt generation (open Q&A, closed Q&A, writing, math/coding), synthetic two-turn prompt ge

*[Content truncated]*

---

## NVIDIA Nemotron

**URL:** https://developer.nvidia.com/nemotron

**Contents:**
- NVIDIA Nemotron
- NVIDIA Nemotron Models
  - Nemotron Nano 2
  - Llama Nemotron Super 1.5
  - Llama Nemotron Ultra
  - Llama Nemotron Nano VL
  - Nemotron RAG
  - Nemotron Safety Guard
- NVIDIA Nemotron Datasets
  - Nemotron Pre- and Post-Training Dataset

NVIDIA Nemotron™ is a family of open models with open weights, training data, and recipes, delivering leading efficiency and accuracy for building specialized AI agents.

Explore ModelsForumFeature Voting

Nemotron models are transparent—the training data used for these models, as well as their weights, are open and available on Hugging Face for developers to evaluate before deploying them in production. The technical reports outlining the steps necessary to recreate these models are also freely available.Nemotron models show strong performance across agentic benchmarks, including scientific reasoning, advanced math, coding, function calling, instruction following, optical character recognition, retrieval-augmented generation (RAG), and more. The models can be further tuned with open tools for improving application-specific accuracy. Easily deploy model endpoints using open frameworks like vLLM, SGLang, and llama.cpp. Endpoints are also available as NVIDIA NIM™ microservices for easy deployment on any GPU-accelerated system. Nemotron reasoning models are optimized for various platforms:

Nano offers cost-efficiency at the edge.

Super balances accuracy and compute on a single GPU.

Ultra is designed for data center-scale deployments.

Additionally, these models provide up to 6x higher throughput, enabling agents to think faster and generate higher-accuracy response while lowering inference cost.

Up to 6x faster throughput over leading 8B open models

Up to 60% lower token generation with new thinking budget feature

Perfect for applications that require real-time responses

Suitable for edge and single consumer-grade GPU deployments

Demo Model on OpenRouter

Use the Model on Hugging Face

High in-class accuracy and throughputGreat for efficient deep research agentsSuitable for single data center GPU deployments

Demo Model on DeepInfra

Experience Model as NVIDIA NIM API

Use the Model on Hugging Face

Ideal for multi-agent enterprise workflows requiring highest accuracy, such as customer service automation, supply chain management, and IT security

Suitable for data center-scale deployments

Demo Model on OpenRouter

Use the Model on Hugging Face

Best-in-class vision language accuracyDesigned for document intelligence and information extraction

Suitable for single data center GPU deployments

Experience Model as NVIDIA NIM API

Use the Model Hugging Face

Industry-leading extraction, embedding, and reranking models

Best-in-class accuracy for text que

*[Content truncated]*

---

## NVIDIA NeMo Guardrails for Developers

**URL:** https://developer.nvidia.com/nemo-guardrails

**Contents:**
- NVIDIA NeMo Guardrails for Developers
- See NVIDIA NeMo Guardrails in Action
- How NVIDIA NeMo Guardrails Works
  - Introductory Blog
  - Deploy Guardrails Tutorial
  - Example Configurations
  - Customer Assistant Example
- Ways to Get Started With NVIDIA NeMo Guardrails
  - Download
  - Access

NVIDIA NeMo™ Guardrails is a scalable solution for orchestrating AI guardrails that keep agentic AI applications safe, reliable, and aligned. It allows you to define, orchestrate, and enforce guardrails for content safety, topic control, PII detection, RAG grounding, and jailbreak prevention—all with low latency and seamless integration. Extensible and customizable, it integrates with frameworks like LangChain, LangGraph, and LlamaIndex, supports multi-agent deployments, and leverages GPU acceleration for low-latency performance. NeMo Guardrails includes out-of-the-box NVIDIA Nemotron models packaged as NVIDIA NIM™ microservices and on Hugging Face—covering content safety, topic control, and jailbreak detection—alongside a growing ecosystem of AI safety models, rails, and observability tools. It’s part of the larger NVIDIA NeMo software suite for building, monitoring, and optimizing AI agents across their lifecycle.

Access SDKTry MicroserviceDocumentation

Enforce content safety, RAG grounding, and jailbreak prevention while building secure, compliant AI agents. This video demonstrates how NeMo Guardrails streamlines guardrail orchestration for safer, more reliable AI applications.

NeMo Guardrails provides components for building a robust, scalable guardrail solution for LLM applications and agents. It evaluates user inputs and model responses based on use-case-specific policies, providing an additional layer of safeguards beyond what’s natively available.

Programmable Policies: Supports customizable content moderation, PII detection, topic relevance, and jailbreak detection tailored to your industry and use case.

Effective Orchestration: Screens both user inputs and model outputs, effectively orchestrates multiple rails with the lowest latency.

Enterprise-Grade Support and Scale: Handle high volume and scale to multiple applications with enterprise-grade support.

Flow Management: Block, filter, or tailor next action or responses based on your requirements with flexible actions.

Simplify building trustworthy LLM apps with AI guardrails for safety, security, and control.

Run Inference with Parallel Rails using NeMo Guardrails microservice.

The configurations in this folder showcase various features of NeMo Guardrails, e.g., using a specific LLM, enabling streaming, and enabling fact-checking.

Learn how to integrate advanced content moderation, jailbreak detection, and topic control with NeMo Guardrails microservices.

Use the right tools and techn

*[Content truncated]*

---

## NVIDIA NeMo

**URL:** https://developer.nvidia.com/nemo-early-access

---

## NVIDIA Nemotron

**URL:** https://developer.nvidia.com/nemotron#section-nvidia-nemotron-models

**Contents:**
- NVIDIA Nemotron
- NVIDIA Nemotron Models
  - Nemotron Nano 2
  - Llama Nemotron Super 1.5
  - Llama Nemotron Ultra
  - Llama Nemotron Nano VL
  - Nemotron RAG
  - Nemotron Safety Guard
- NVIDIA Nemotron Datasets
  - Nemotron Pre- and Post-Training Dataset

NVIDIA Nemotron™ is a family of open models with open weights, training data, and recipes, delivering leading efficiency and accuracy for building specialized AI agents.

Explore ModelsForumFeature Voting

Nemotron models are transparent—the training data used for these models, as well as their weights, are open and available on Hugging Face for developers to evaluate before deploying them in production. The technical reports outlining the steps necessary to recreate these models are also freely available.Nemotron models show strong performance across agentic benchmarks, including scientific reasoning, advanced math, coding, function calling, instruction following, optical character recognition, retrieval-augmented generation (RAG), and more. The models can be further tuned with open tools for improving application-specific accuracy. Easily deploy model endpoints using open frameworks like vLLM, SGLang, and llama.cpp. Endpoints are also available as NVIDIA NIM™ microservices for easy deployment on any GPU-accelerated system. Nemotron reasoning models are optimized for various platforms:

Nano offers cost-efficiency at the edge.

Super balances accuracy and compute on a single GPU.

Ultra is designed for data center-scale deployments.

Additionally, these models provide up to 6x higher throughput, enabling agents to think faster and generate higher-accuracy response while lowering inference cost.

Up to 6x faster throughput over leading 8B open models

Up to 60% lower token generation with new thinking budget feature

Perfect for applications that require real-time responses

Suitable for edge and single consumer-grade GPU deployments

Demo Model on OpenRouter

Use the Model on Hugging Face

High in-class accuracy and throughputGreat for efficient deep research agentsSuitable for single data center GPU deployments

Demo Model on DeepInfra

Experience Model as NVIDIA NIM API

Use the Model on Hugging Face

Ideal for multi-agent enterprise workflows requiring highest accuracy, such as customer service automation, supply chain management, and IT security

Suitable for data center-scale deployments

Demo Model on OpenRouter

Use the Model on Hugging Face

Best-in-class vision language accuracyDesigned for document intelligence and information extraction

Suitable for single data center GPU deployments

Experience Model as NVIDIA NIM API

Use the Model Hugging Face

Industry-leading extraction, embedding, and reranking models

Best-in-class accuracy for text que

*[Content truncated]*

---

## NVIDIA NeMo Agent Toolkit

**URL:** https://developer.nvidia.com/nemo-agent-toolkit

**Contents:**
- NVIDIA NeMo Agent Toolkit
- See NeMo Agent Toolkit in Action
- How NeMo Agent Toolkit Works
  - Simplify Development
  - Accelerate Development and Improve Reliability
  - Streamline Agent Optimization
  - Accelerate Agent Responses
  - Increase Accuracy
  - Introductory Blog
  - Introductory Video

NVIDIA NeMo™ Agent Toolkit is an open-source AI framework for building, profiling, and optimizing agents and tools from any framework, enabling unified, cross-framework integration across connected AI agent systems. By exposing hidden bottlenecks and costs and optimizing the workflow, it helps enterprises scale agentic systems efficiently while maintaining reliability.

NeMo Agent Toolkit is part of the NVIDIA NeMo software suite for managing the AI agent lifecycle, providing telemetry, orchestration, and observability tools that accelerate development, uncover bottlenecks, and streamline performance across multi-agent systems.

Access GitHubDocumentationForum

Create Your Own AI Agent

Benchmarking and Optimizing AI Agents

How To Develop Teams of AI Agents

Optimize Your AI Agent Workflows

NVIDIA NeMo Agent Toolkit provides unified monitoring and optimization for AI agent systems, working across LangChain, CrewAI, and custom frameworks. It captures granular metrics on cross-agent coordination, tool usage efficiency, and computational costs, enabling data-driven optimizations through NVIDIA Accelerated Computing. It can be used to parallelize slow workflows, cache expensive operations, and maintain and evaluate system accuracy quickly. Compatible with OpenTelemetry and major agent frameworks, the toolkit reduces cloud spend and enhances performance while providing insights to scale from single agents to enterprise-grade digital workforces.NeMo Agent Toolkit supports the Model Context Protocol (MCP), enabling developers to use the toolkit to access tools served by remote MCP servers, or as a server to make their own tools available to others via MCP. This means agents built with the toolkit can easily use any tool registered in an MCP registry.

Experiment and prototype new agentic AI applications quickly and easily with the toolkit’s YAML configuration builder. With universal descriptors for agents, tools, and workflows, you can flexibly choose and connect agent frameworks best suited to each task in a workflow. Access a reusable collection of tools, pipelines, and agentic workflows to ease the development of agentic AI systems.

Build agentic systems with ease and repeatability. In the tool registry, access the best retrieval-augmented generation (RAG) architectures, workflows, and search tools available across your organization, or leverage the AI-Q NVIDIA Blueprint, built with NVIDIA NIM™ and NeMo. With the AI-Q blueprint, developers have an example t

*[Content truncated]*

---

## NVIDIA NeMo Curator for Developers

**URL:** https://developer.nvidia.com/nemo-curator

**Contents:**
- NVIDIA NeMo Curator for Developers
- How NVIDIA NeMo Curator Works
  - Text Data Processing
  - Synthetic Data Generation
  - Video Data Processing
  - Audio Data Processing
  - Image Data Processing
- Introductory Resources
  - Introductory Blog
  - Tutorials

NVIDIA NeMo™ Curator improves generative AI model accuracy by processing text, image, and video data at scale for training and customization. It also provides prebuilt pipelines for generating synthetic data to customize and evaluate generative AI systems.With NeMo Curator, part of the NVIDIA NeMo software suite for managing the AI agent lifecycle, developers can curate high-quality data and train highly accurate generative AI models for various industries, including finance, retail, manufacturing and telecommunications.NeMo Curator, along with NeMo microservices enables developers to create data flywheels and continuously optimize generative AI agents, enhancing the overall experience for end users.

DownloadDocumentationForum

NeMo Curator streamlines data-processing tasks, such as data downloading, extraction, cleaning, quality filtering, deduplication, and blending or shuffling, providing them as Pythonic APIs, making it easier for developers to build data-processing pipelines. High-quality data processed from NeMo Curator enables you to achieve higher accuracy with less data and faster model convergence, reducing training time. NeMo Curator supports the processing of text, image, and video modalities and can scale up to 100+ PB of data.NeMo Curator provides a customizable and modular interface, allowing you to select the building blocks for your data processing pipelines. Please refer to the architecture diagrams below to see how you can build data processing pipelines.

This architecture diagram shows the various features available for processing text. At a high level, a typical text processing pipeline begins with downloading data from public sources or private repositories and performing cleaning steps, such as fixing Unicode characters. Next, heuristic filters—such as word count—are applied, followed by deduplication, advanced quality filtering using classifier models for quality and domain, and finally, data blending.

NeMo Curator has a simple, easy-to-use set of tools that let you use pre-built synthetic data generation pipelines or build your own. Any model inference service that uses the OpenAI API is compatible with the synthetic data generation module, allowing you to generate your data from any model.NeMo Curator provides pre-built pipelines for several use cases to help you get started easily, including evaluating and customizing embedding models, prompt generation (open Q&A, closed Q&A, writing, math/coding), synthetic two-turn prompt ge

*[Content truncated]*

---
