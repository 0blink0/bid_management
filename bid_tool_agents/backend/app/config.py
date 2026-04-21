"""
统一配置管理 - 支持多环境（开发/测试/生产）
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List, Dict, Any
from functools import lru_cache
import yaml
import os


class Environment:
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class DatabaseConfig(BaseSettings):
    """PostgreSQL数据库配置"""
    host: str = "localhost"
    port: int = 5432
    name: str = "bid_management"
    user: str = "postgres"
    password: str = "postgres"
    pool_size: int = 10
    max_overflow: int = 20

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class VectorDBConfig(BaseSettings):
    """向量数据库（Qdrant）配置"""
    host: str = "localhost"
    port: int = 6333
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    collection_name: str = "bid_documents"
    vector_size: int = 1024

    @property
    def url(self) -> str:
        if self.endpoint and self.endpoint.strip():
            return self.endpoint.strip()
        return f"http://{self.host}:{self.port}"


class GraphDBConfig(BaseSettings):
    """图数据库（Neo4j）配置"""
    host: str = "localhost"
    port: int = 7687
    name: str = "neo4j"
    user: str = "neo4j"
    password: str = "neo4j"

    @property
    def url(self) -> str:
        return f"bolt://{self.host}:{self.port}"


class RedisConfig(BaseSettings):
    """Redis配置"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    memory_ttl: Dict[str, int] = {
        "immediate": 60,
        "short_term": 3600,
        "session": 86400
    }

    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class LLMProviderConfig(BaseSettings):
    """LLM提供者配置"""
    provider: str = "ali_qwen"
    model: str = "qwen-max"
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 120
    retry_times: int = 3
    stream: bool = True


class LLMRoutingRule(BaseSettings):
    """LLM路由规则"""
    condition: str = ""
    target: str = ""
    priority: int = 0


class LLMConfig(BaseSettings):
    """LLM统一配置"""
    active: str = "ali_qwen"
    ali_qwen: Optional[LLMProviderConfig] = None
    private_qwen: Optional[LLMProviderConfig] = None
    private_deepseek: Optional[LLMProviderConfig] = None
    routing_enabled: bool = False
    routing_rules: List[LLMRoutingRule] = []


class StorageConfig(BaseSettings):
    """文件存储配置"""
    upload_dir: str = "./storage/uploads"
    parsed_dir: str = "./storage/parsed"
    report_dir: str = "./storage/reports"
    max_file_size: int = 500 * 1024 * 1024
    allowed_extensions: List[str] = [".pdf", ".docx", ".doc", ".jpg", ".png", ".zip"]


class AppConfig(BaseSettings):
    """应用配置"""
    app_name: str = "智能招投标审查平台"
    debug: bool = False
    environment: str = Environment.DEVELOPMENT
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = ["*"]
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"


class KnowledgeQueryConfig(BaseSettings):
    """知识检索接口配置。"""

    default_knowledge_type: str = "laws_regulations"
    default_limit: int = 10
    max_limit: int = 50


class Settings(BaseSettings):
    """统一配置类"""
    ENV: str = Field(default="development", alias="ENV")

    database: DatabaseConfig = DatabaseConfig()
    vector_db: VectorDBConfig = VectorDBConfig()
    graph_db: GraphDBConfig = GraphDBConfig()
    redis: RedisConfig = RedisConfig()
    llm: LLMConfig = LLMConfig()
    storage: StorageConfig = StorageConfig()
    app: AppConfig = AppConfig()
    knowledge_query: KnowledgeQueryConfig = KnowledgeQueryConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_config_from_yaml(env: str) -> Settings:
    """从YAML文件加载配置"""
    config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
    yaml_path = os.path.join(config_dir, f"{env}.yaml")

    if os.path.exists(yaml_path):
        with open(yaml_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            return Settings(**config_data)
    return Settings()


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    env = os.getenv("ENV", "development")
    return load_config_from_yaml(env)
