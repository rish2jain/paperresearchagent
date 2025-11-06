"""
AWS Integration Module
Provides deeper AWS integration with SageMaker, Lambda, and Bedrock
for enhanced AI capabilities and serverless processing.
"""

from typing import Dict, Any, Optional, List
import logging
import os
import json

# Optional AWS dependencies
try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
    boto3 = None

logger = logging.getLogger(__name__)


class AWSIntegration:
    """AWS service integration for enhanced capabilities"""
    
    def __init__(self):
        """Initialize AWS clients"""
        if not HAS_BOTO3:
            logger.warning("boto3 not available. AWS integration disabled.")
            self.enabled = False
            return
        
        self.enabled = True
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        # Initialize clients
        self.sagemaker_client = None
        self.lambda_client = None
        self.bedrock_client = None
        self.s3_client = None
        
        # Initialize if credentials available
        try:
            self._initialize_clients()
        except Exception as e:
            logger.warning(f"AWS client initialization failed: {e}")
            self.enabled = False
    
    def _initialize_clients(self):
        """Initialize AWS service clients"""
        if not HAS_BOTO3:
            return
        
        session = boto3.Session(region_name=self.region)
        
        # SageMaker Runtime client for model inference
        try:
            self.sagemaker_client = session.client('sagemaker-runtime')
            logger.info("SageMaker client initialized")
        except Exception as e:
            logger.warning(f"SageMaker client initialization failed: {e}")
        
        # Lambda client for serverless functions
        try:
            self.lambda_client = session.client('lambda')
            logger.info("Lambda client initialized")
        except Exception as e:
            logger.warning(f"Lambda client initialization failed: {e}")
        
        # Bedrock client for Amazon Bedrock models
        try:
            self.bedrock_client = session.client('bedrock-runtime', region_name=self.region)
            logger.info("Bedrock client initialized")
        except Exception as e:
            logger.warning(f"Bedrock client initialization failed: {e}")
        
        # S3 client for storage
        try:
            self.s3_client = session.client('s3')
            logger.info("S3 client initialized")
        except Exception as e:
            logger.warning(f"S3 client initialization failed: {e}")
    
    async def invoke_sagemaker_endpoint(
        self,
        endpoint_name: str,
        payload: Dict[str, Any],
        content_type: str = "application/json"
    ) -> Optional[Dict[str, Any]]:
        """
        Invoke a SageMaker endpoint for model inference
        
        Args:
            endpoint_name: Name of the SageMaker endpoint
            payload: Input data for the model
            content_type: Content type of the payload
            
        Returns:
            Model response or None if error
        """
        if not self.enabled or not self.sagemaker_client:
            logger.warning("SageMaker integration not available")
            return None
        
        try:
            import asyncio
            
            # Run in executor since boto3 is synchronous
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._invoke_sagemaker_sync,
                endpoint_name,
                payload,
                content_type
            )
            return response
        except Exception as e:
            logger.error(f"SageMaker invocation error: {e}")
            return None
    
    def _invoke_sagemaker_sync(
        self,
        endpoint_name: str,
        payload: Dict[str, Any],
        content_type: str
    ) -> Dict[str, Any]:
        """Synchronous SageMaker invocation"""
        body = json.dumps(payload).encode('utf-8')
        
        response = self.sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType=content_type,
            Body=body
        )
        
        result = json.loads(response['Body'].read().decode('utf-8'))
        return result
    
    async def invoke_lambda_function(
        self,
        function_name: str,
        payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Invoke an AWS Lambda function
        
        Args:
            function_name: Name of the Lambda function
            payload: Input payload
            
        Returns:
            Lambda response or None if error
        """
        if not self.enabled or not self.lambda_client:
            logger.warning("Lambda integration not available")
            return None
        
        try:
            import asyncio
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._invoke_lambda_sync,
                function_name,
                payload
            )
            return response
        except Exception as e:
            logger.error(f"Lambda invocation error: {e}")
            return None
    
    def _invoke_lambda_sync(
        self,
        function_name: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synchronous Lambda invocation"""
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        result = json.loads(response['Payload'].read().decode('utf-8'))
        return result
    
    async def invoke_bedrock_model(
        self,
        model_id: str,
        prompt: str,
        model_kwargs: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Invoke an Amazon Bedrock model
        
        Supports multiple model families:
        - Anthropic Claude: anthropic.claude-v2, anthropic.claude-3-sonnet-20240229, anthropic.claude-3-5-sonnet-20241022
        - Meta Llama: meta.llama3-8b-instruct-v1:0, meta.llama3-70b-instruct-v1:0
        - Amazon Titan: amazon.titan-text-express-v1, amazon.titan-text-lite-v1
        - AI21 Labs: ai21.j2-ultra-v1, ai21.j2-mid-v1
        - Cohere: cohere.command-text-v14, cohere.command-light-text-v14
        
        Args:
            model_id: Bedrock model ID
            prompt: Input prompt
            model_kwargs: Additional model parameters
            
        Returns:
            Model response text or None if error
        """
        if not self.enabled or not self.bedrock_client:
            logger.warning("Bedrock integration not available")
            return None
        
        try:
            import asyncio
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._invoke_bedrock_sync,
                model_id,
                prompt,
                model_kwargs or {}
            )
            return response
        except Exception as e:
            logger.error(f"Bedrock invocation error: {e}")
            return None
    
    def _invoke_bedrock_sync(
        self,
        model_id: str,
        prompt: str,
        model_kwargs: Dict[str, Any]
    ) -> str:
        """Synchronous Bedrock invocation with multi-model support"""
        # Determine model family and format request accordingly
        if model_id.startswith("anthropic.claude"):
            # Claude models (v2, v3, v3.5)
            if "claude-3" in model_id or "claude-3.5" in model_id:
                # Claude 3/3.5 format (messages API)
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": model_kwargs.get("max_tokens", 4096),
                    "temperature": model_kwargs.get("temperature", 0.7),
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            else:
                # Claude v2 format (text completion API - deprecated but still supported)
                body = {
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": model_kwargs.get("max_tokens", 1000),
                    "temperature": model_kwargs.get("temperature", 0.7)
                }
        elif model_id.startswith("meta.llama"):
            # Llama models
            body = {
                "prompt": prompt,
                "max_gen_len": model_kwargs.get("max_tokens", 512),
                "temperature": model_kwargs.get("temperature", 0.7),
                "top_p": model_kwargs.get("top_p", 0.9)
            }
        elif model_id.startswith("amazon.titan"):
            # Amazon Titan models
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": model_kwargs.get("max_tokens", 512),
                    "temperature": model_kwargs.get("temperature", 0.7),
                    "topP": model_kwargs.get("top_p", 0.9)
                }
            }
        elif model_id.startswith("ai21."):
            # AI21 Labs models
            body = {
                "prompt": prompt,
                "maxTokens": model_kwargs.get("max_tokens", 512),
                "temperature": model_kwargs.get("temperature", 0.7),
                "topP": model_kwargs.get("top_p", 0.9)
            }
        elif model_id.startswith("cohere."):
            # Cohere models
            body = {
                "prompt": prompt,
                "max_tokens": model_kwargs.get("max_tokens", 512),
                "temperature": model_kwargs.get("temperature", 0.7),
                "p": model_kwargs.get("top_p", 0.9)
            }
        else:
            # Default to Claude format (most common)
            logger.warning(f"Unknown model family for {model_id}, using Claude format")
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": model_kwargs.get("max_tokens", 1000),
                "temperature": model_kwargs.get("temperature", 0.7),
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        
        response = self.bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read().decode('utf-8'))
        
        # Parse response based on model family
        if model_id.startswith("anthropic.claude"):
            if "claude-3" in model_id or "claude-3.5" in model_id:
                # Claude 3/3.5 format
                return response_body.get('content', [{}])[0].get('text', '')
            else:
                # Claude v2 format
                return response_body.get('completion', '')
        elif model_id.startswith("meta.llama"):
            return response_body.get('generation', '')
        elif model_id.startswith("amazon.titan"):
            return response_body.get('results', [{}])[0].get('outputText', '')
        elif model_id.startswith("ai21."):
            return response_body.get('completions', [{}])[0].get('data', {}).get('text', '')
        elif model_id.startswith("cohere."):
            return response_body.get('generations', [{}])[0].get('text', '')
        else:
            # Default parsing
            return response_body.get('content', [{}])[0].get('text', '') if isinstance(response_body.get('content'), list) else response_body.get('text', '')
    
    async def store_result_in_s3(
        self,
        bucket_name: str,
        key: str,
        data: Any,
        content_type: str = "application/json"
    ) -> bool:
        """
        Store research result in S3
        
        Args:
            bucket_name: S3 bucket name
            key: S3 object key
            data: Data to store (dict will be JSON-encoded)
            content_type: Content type
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.s3_client:
            logger.warning("S3 integration not available")
            return False
        
        try:
            import asyncio
            
            if isinstance(data, dict):
                body = json.dumps(data).encode('utf-8')
            elif isinstance(data, str):
                body = data.encode('utf-8')
            else:
                body = data
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._store_s3_sync,
                bucket_name,
                key,
                body,
                content_type
            )
            return True
        except Exception as e:
            logger.error(f"S3 storage error: {e}")
            return False
    
    def _store_s3_sync(
        self,
        bucket_name: str,
        key: str,
        body: bytes,
        content_type: str
    ):
        """Synchronous S3 storage"""
        self.s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body,
            ContentType=content_type
        )
    
    async def trigger_research_lambda(
        self,
        query: str,
        max_papers: int = 10
    ) -> Optional[str]:
        """
        Trigger a Lambda function to run research asynchronously
        
        Args:
            query: Research query
            max_papers: Maximum papers to analyze
            
        Returns:
            Invocation ID or None if error
        """
        if not self.enabled or not self.lambda_client:
            return None
        
        lambda_function = os.getenv("RESEARCH_LAMBDA_FUNCTION", "research-ops-agent-trigger")
        
        import time
        
        payload = {
            "query": query,
            "max_papers": max_papers,
            "timestamp": str(int(time.time()))
        }
        
        try:
            import asyncio
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._invoke_lambda_async_sync,
                lambda_function,
                payload
            )
            return response
        except Exception as e:
            logger.error(f"Lambda trigger error: {e}")
            return None
    
    def _invoke_lambda_async_sync(
        self,
        function_name: str,
        payload: Dict[str, Any]
    ) -> str:
        """Invoke Lambda asynchronously"""
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='Event',  # Async
            Payload=json.dumps(payload)
        )
        return response.get('ResponseMetadata', {}).get('RequestId', '')


# Global AWS integration instance
_aws_integration: Optional[AWSIntegration] = None


def get_aws_integration() -> AWSIntegration:
    """Get global AWS integration instance"""
    global _aws_integration
    if _aws_integration is None:
        _aws_integration = AWSIntegration()
    return _aws_integration


async def use_bedrock_for_analysis(
    prompt: str,
    model_id: Optional[str] = None
) -> Optional[str]:
    """
    Use Amazon Bedrock for enhanced analysis
    
    Recommended models (2025):
    - anthropic.claude-3-5-sonnet-20241022 (best for analysis, recommended)
    - anthropic.claude-3-sonnet-20240229 (good balance)
    - anthropic.claude-v2 (legacy, but still works)
    - meta.llama3-70b-instruct-v1:0 (cost-effective)
    - amazon.titan-text-express-v1 (AWS native)
    
    Args:
        prompt: Analysis prompt
        model_id: Bedrock model ID (defaults to Claude 3.5 Sonnet if available)
        
    Returns:
        Analysis result or None
    """
    aws = get_aws_integration()
    if not aws.enabled:
        return None
    
    # Default to Claude 3.5 Sonnet (best for 2025), fallback to Claude v2
    if model_id is None:
        model_id = os.getenv(
            "BEDROCK_MODEL_ID",
            "anthropic.claude-3-5-sonnet-20241022"  # Latest Claude 3.5 (2025)
        )
    
    return await aws.invoke_bedrock_model(model_id, prompt)


async def use_sagemaker_for_inference(
    endpoint_name: str,
    payload: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Use SageMaker endpoint for model inference
    
    Args:
        endpoint_name: SageMaker endpoint name
        payload: Input payload
        
    Returns:
        Inference result or None
    """
    aws = get_aws_integration()
    if not aws.enabled:
        return None
    
    return await aws.invoke_sagemaker_endpoint(endpoint_name, payload)


async def store_research_result_s3(
    result: Dict[str, Any],
    query: str
) -> Optional[str]:
    """
    Store research result in S3 (or local file system fallback)
    
    Args:
        result: Research synthesis result
        query: Research query
        
    Returns:
        S3 object key (s3://...) or local file path (file://...) or None
    """
    import time
    from datetime import datetime
    import json
    from pathlib import Path
    
    bucket_name = os.getenv("RESEARCH_RESULTS_S3_BUCKET")
    
    # Generate storage key/path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    query_slug = query.lower().replace(" ", "_")[:50]
    key = f"research_results/{query_slug}_{timestamp}.json"
    
    # Try AWS S3 first if configured
    if bucket_name:
        aws = get_aws_integration()
        success = await aws.store_result_in_s3(bucket_name, key, result)
        
        if success:
            return f"s3://{bucket_name}/{key}"
    
    # Fallback to local file system storage
    try:
        # Create local storage directory
        local_storage_dir = Path(os.getenv("LOCAL_STORAGE_DIR", "~/.local/share/research-ops/results"))
        local_storage_dir = Path(local_storage_dir).expanduser()
        local_storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to local file
        local_file_path = local_storage_dir / f"{query_slug}_{timestamp}.json"
        with open(local_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Stored research result locally: {local_file_path}")
        return f"file://{local_file_path}"
    except Exception as e:
        logger.error(f"Local storage fallback failed: {e}")
        return None

