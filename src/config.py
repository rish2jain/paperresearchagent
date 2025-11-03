"""
Configuration Management
Centralized configuration with environment variable support and validation
"""

import os
from typing import Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class NIMConfig:
    """NIM service configuration"""
    reasoning_nim_url: str
    embedding_nim_url: str
    reasoning_timeout_total: int = 60
    reasoning_timeout_connect: int = 10
    reasoning_timeout_sock_read: int = 30
    embedding_timeout_total: int = 60
    embedding_timeout_connect: int = 10
    embedding_timeout_sock_read: int = 30


@dataclass
class PaperSourceConfig:
    """Configuration for paper source APIs"""
    # Free/public APIs
    semantic_scholar_api_key: Optional[str] = None
    crossref_mailto: str = "research-ops@example.com"
    
    # APIs requiring keys/subscriptions
    ieee_api_key: Optional[str] = None
    acm_api_key: Optional[str] = None
    springer_api_key: Optional[str] = None
    
    # Source enablement flags
    enable_arxiv: bool = True
    enable_pubmed: bool = True
    enable_semantic_scholar: bool = True
    enable_crossref: bool = True
    enable_ieee: bool = True
    enable_acm: bool = True
    enable_springer: bool = True
    
    @classmethod
    def from_env(cls) -> 'PaperSourceConfig':
        """Load configuration from environment variables"""
        return cls(
            semantic_scholar_api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY"),
            crossref_mailto=os.getenv("CROSSREF_MAILTO", "research-ops@example.com"),
            ieee_api_key=os.getenv("IEEE_API_KEY"),
            acm_api_key=os.getenv("ACM_API_KEY"),
            springer_api_key=os.getenv("SPRINGER_API_KEY"),
            enable_arxiv=os.getenv("ENABLE_ARXIV", "true").lower() == "true",
            enable_pubmed=os.getenv("ENABLE_PUBMED", "true").lower() == "true",
            enable_semantic_scholar=os.getenv("ENABLE_SEMANTIC_SCHOLAR", "true").lower() == "true",
            enable_crossref=os.getenv("ENABLE_CROSSREF", "true").lower() == "true",
            enable_ieee=os.getenv("ENABLE_IEEE", "false").lower() == "true",
            enable_acm=os.getenv("ENABLE_ACM", "false").lower() == "true",
            enable_springer=os.getenv("ENABLE_SPRINGER", "false").lower() == "true",
        )


@dataclass
class AgentConfig:
    """Agent system configuration"""
    relevance_threshold: float = 0.7
    clustering_eps: float = 0.3
    clustering_min_samples: int = 3
    synthesis_max_iterations: int = 2
    synthesis_quality_threshold: float = 0.8
    max_papers_per_search: int = 20
    max_concurrent_analyses: int = 5


@dataclass
class APIConfig:
    """API service configuration"""
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "info"
    cors_origins: list = None
    request_timeout: int = 300
    demo_mode: bool = False  # Enable demo mode with pre-cached results


@dataclass
class Config:
    """Main configuration object"""
    nim: NIMConfig
    agent: AgentConfig
    api: APIConfig
    paper_sources: PaperSourceConfig
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        # NIM Configuration
        reasoning_nim_url = os.getenv(
            "REASONING_NIM_URL",
            "http://reasoning-nim.research-ops.svc.cluster.local:8000"
        )
        embedding_nim_url = os.getenv(
            "EMBEDDING_NIM_URL",
            "http://embedding-nim.research-ops.svc.cluster.local:8001"
        )
        
        nim_config = NIMConfig(
            reasoning_nim_url=reasoning_nim_url,
            embedding_nim_url=embedding_nim_url,
            reasoning_timeout_total=int(os.getenv("REASONING_TIMEOUT_TOTAL", "60")),
            reasoning_timeout_connect=int(os.getenv("REASONING_TIMEOUT_CONNECT", "10")),
            reasoning_timeout_sock_read=int(os.getenv("REASONING_TIMEOUT_SOCK_READ", "30")),
            embedding_timeout_total=int(os.getenv("EMBEDDING_TIMEOUT_TOTAL", "60")),
            embedding_timeout_connect=int(os.getenv("EMBEDDING_TIMEOUT_CONNECT", "10")),
            embedding_timeout_sock_read=int(os.getenv("EMBEDDING_TIMEOUT_SOCK_READ", "30"))
        )
        
        # Agent Configuration
        agent_config = AgentConfig(
            relevance_threshold=float(os.getenv("RELEVANCE_THRESHOLD", "0.7")),
            clustering_eps=float(os.getenv("CLUSTERING_EPS", "0.3")),
            clustering_min_samples=int(os.getenv("CLUSTERING_MIN_SAMPLES", "3")),
            synthesis_max_iterations=int(os.getenv("SYNTHESIS_MAX_ITERATIONS", "2")),
            synthesis_quality_threshold=float(os.getenv("SYNTHESIS_QUALITY_THRESHOLD", "0.8")),
            max_papers_per_search=int(os.getenv("MAX_PAPERS_PER_SEARCH", "20")),
            max_concurrent_analyses=int(os.getenv("MAX_CONCURRENT_ANALYSES", "5"))
        )
        
        # API Configuration
        cors_origins_str = os.getenv("CORS_ORIGINS", "*")
        cors_origins = cors_origins_str.split(",") if cors_origins_str != "*" else ["*"]
        
        api_config = APIConfig(
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8080")),
            log_level=os.getenv("LOG_LEVEL", "info"),
            cors_origins=cors_origins,
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "300")),
            demo_mode=os.getenv("DEMO_MODE", "false").lower() == "true"
        )
        
        paper_source_config = PaperSourceConfig.from_env()
        
        config = cls(
            nim=nim_config,
            agent=agent_config,
            api=api_config,
            paper_sources=paper_source_config
        )
        
        logger.info("Configuration loaded from environment variables")
        return config
    
    def validate(self) -> bool:
        """Validate configuration values"""
        errors = []
        
        # Validate NIM URLs
        if not self.nim.reasoning_nim_url.startswith(("http://", "https://")):
            errors.append("REASONING_NIM_URL must start with http:// or https://")
        
        if not self.nim.embedding_nim_url.startswith(("http://", "https://")):
            errors.append("EMBEDDING_NIM_URL must start with http:// or https://")
        
        # Validate thresholds
        if not 0.0 <= self.agent.relevance_threshold <= 1.0:
            errors.append("RELEVANCE_THRESHOLD must be between 0.0 and 1.0")
        
        if not 0.0 <= self.agent.synthesis_quality_threshold <= 1.0:
            errors.append("SYNTHESIS_QUALITY_THRESHOLD must be between 0.0 and 1.0")
        
        # Validate clustering parameters
        if self.agent.clustering_eps <= 0:
            errors.append("CLUSTERING_EPS must be positive")
        
        if self.agent.clustering_min_samples < 1:
            errors.append("CLUSTERING_MIN_SAMPLES must be at least 1")
        
        if errors:
            for error in errors:
                logger.error(f"Configuration validation error: {error}")
            return False
        
        logger.info("Configuration validation passed")
        return True


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config.from_env()
        _config.validate()
    return _config


def reload_config() -> Config:
    """Reload configuration from environment"""
    global _config
    _config = Config.from_env()
    _config.validate()
    return _config

