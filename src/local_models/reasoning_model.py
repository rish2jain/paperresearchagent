"""
Local Reasoning Model using llama.cpp with Metal GPU
Replaces NVIDIA Reasoning NIM for local execution
"""

import os
import logging
from typing import Optional, List, Dict
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import llama-cpp-python
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    logger.warning("llama-cpp-python not installed. Install with: pip install llama-cpp-python[metal]")

# Fallback to MLX if llama.cpp not available
try:
    from mlx_lm import load, generate
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False
    logger.warning("mlx-lm not installed. Install with: pip install mlx-lm")


class LocalReasoningModel:
    """
    Local reasoning model using llama.cpp with Metal backend
    Compatible with ReasoningNIMClient interface
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        n_ctx: int = 4096,
        n_gpu_layers: int = -1,
        use_mlx: bool = False
    ):
        """
        Initialize local reasoning model
        
        Args:
            model_path: Path to GGUF model file. If None, uses default location
            n_ctx: Context window size
            n_gpu_layers: Number of GPU layers (-1 = all)
            use_mlx: Use MLX instead of llama.cpp
        """
        # Expand user home directory if path contains ~
        if model_path:
            model_path = os.path.expanduser(model_path)
        self.model_path = model_path or self._get_default_model_path()
        # Ensure path is expanded even if from default
        self.model_path = os.path.expanduser(self.model_path)
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.use_mlx = use_mlx
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _get_default_model_path(self) -> str:
        """Get default model path"""
        home = Path.home()
        default_path = home / ".local" / "share" / "models" / "llama-3.1-8b-instruct-q4_K_M.gguf"
        
        # Check if model exists
        if default_path.exists():
            return str(default_path)
        
        # Alternative locations
        alt_paths = [
            home / "models" / "llama-3.1-8b-instruct-q4_K_M.gguf",
            Path("./models") / "llama-3.1-8b-instruct-q4_K_M.gguf",
        ]
        
        for path in alt_paths:
            if path.exists():
                return str(path)
        
        # Return default path (user will need to download model)
        logger.warning(f"Model not found at {default_path}. Please download the model.")
        return str(default_path)
    
    def _initialize_model(self):
        """Initialize the model"""
        if self.use_mlx and MLX_AVAILABLE:
            self._initialize_mlx()
        elif LLAMA_CPP_AVAILABLE:
            self._initialize_llama_cpp()
        else:
            raise RuntimeError(
                "No local model backend available. Install either:\n"
                "  - llama-cpp-python[metal]: pip install llama-cpp-python[metal]\n"
                "  - mlx-lm: pip install mlx-lm"
            )
    
    def _initialize_llama_cpp(self):
        """Initialize llama.cpp model"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}\n"
                f"Please download Llama 3.1 8B Instruct (Q4_K_M quantized) GGUF model"
            )
        
        logger.info(f"Loading llama.cpp model from {self.model_path}")
        
        try:
            self.model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.n_gpu_layers,  # Use Metal GPU
                n_ctx=self.n_ctx,
                verbose=False,
                n_threads=None,  # Auto-detect
            )
            logger.info("✅ Local reasoning model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _initialize_mlx(self):
        """Initialize MLX model"""
        model_name = "mlx-community/llama-3.1-8b-instruct"
        logger.info(f"Loading MLX model: {model_name}")
        
        try:
            self.model, self.tokenizer = load(model_name)
            logger.info("✅ MLX reasoning model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load MLX model: {e}")
            raise
    
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> str:
        """
        Generate completion matching NIM API interface
        
        Args:
            prompt: Input text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            stream: Whether to stream (not supported in local mode yet)
        
        Returns:
            Generated text completion
        """
        if stream:
            logger.warning("Streaming not yet supported in local mode, generating full response")
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        
        if self.use_mlx and MLX_AVAILABLE:
            result = await loop.run_in_executor(
                None,
                self._complete_mlx,
                prompt,
                max_tokens,
                temperature
            )
        else:
            result = await loop.run_in_executor(
                None,
                self._complete_llama_cpp,
                prompt,
                max_tokens,
                temperature,
                top_p
            )
        
        return result
    
    def _complete_llama_cpp(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_p: float
    ) -> str:
        """Generate completion using llama.cpp"""
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        response = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=False,
            stop=["<|end_of_text|>", "<|eot_id|>"]
        )
        
        return response['choices'][0]['text']
    
    def _complete_mlx(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Generate completion using MLX"""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not initialized")
        
        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=temperature
        )
        
        return response
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Chat-style interaction matching NIM API
        
        Args:
            messages: List of {"role": "user/assistant", "content": "text"}
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        
        Returns:
            Assistant's response
        """
        # Convert messages to prompt format
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt = "\n".join(prompt_parts) + "\nAssistant:"
        
        return await self.complete(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        # Cleanup if needed
        pass

