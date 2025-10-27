import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class APIConfig:
    """Configuration for API settings"""
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_api_key: str = "ollama"
    model_name: str = "llama3.2"
    temperature: float = 0.2

@dataclass
class ScrapingConfig:
    """Configuration for RSS scraping settings"""
    per_blog_limit: int = 20
    request_timeout: int = 10
    retry_attempts: int = 3
    retry_delay: int = 1
    user_agent: str = "PersonalisedNewsfeed/1.0"

@dataclass
class FilteringConfig:
    """Configuration for article filtering settings"""
    relevance_threshold: float = 6.0
    max_articles_to_process: int = 100
    enable_deduplication: bool = True
    deduplication_threshold: float = 0.8

@dataclass
class OutputConfig:
    """Configuration for output settings"""
    output_directory: str = "output"
    markdown_filename: str = "relevant_articles.md"
    include_timestamp: bool = True
    sort_by_score: bool = True
    max_summary_length: int = 500

@dataclass
class PromptsConfig:
    """Configuration for prompt settings"""
    system_prompt: str = "You are a senior software developer who is very interested and developing my skills and knows that I am very interested in catching up with the latest tech news. Return only valid JSON exactly in the requested schema."
    user_prompt: str = "I am a junior software engineer who is very interested in keeping up with the latest tech trends and also learn new skills that I do not have. My company currently requires me to code in C# for backend and Typescript for frontend. I am interested in the latest AI developments, system design, software design and software development life cycle. Help me to sieve through the blogs and the summaries that I have provided and identify articles that will be helpful for me."

@dataclass
class TechBlogsConfig:
    """Configuration for tech blogs"""
    def __init__(self, blogs_dict: Dict[str, str] = None):
        if blogs_dict is None:
            blogs_dict = {
                "Netflix_tech_blog": "https://netflixtechblog.com/feed",
                "Stack_Overflow_blog": "https://stackoverflow.blog/feed"
            }
        self.blogs = blogs_dict

@dataclass
class FilesConfig:
    """Configuration for file paths"""
    cache_file: str = "feed_cache.json"

@dataclass
class Config:
    """Main configuration class"""
    api: APIConfig
    scraping: ScrapingConfig
    filtering: FilteringConfig
    output: OutputConfig
    prompts: PromptsConfig
    tech_blogs: TechBlogsConfig
    files: FilesConfig

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create Config instance from dictionary"""
        return cls(
            api=APIConfig(**config_dict.get('api', {})),
            scraping=ScrapingConfig(**config_dict.get('scraping', {})),
            filtering=FilteringConfig(**config_dict.get('filtering', {})),
            output=OutputConfig(**config_dict.get('output', {})),
            prompts=PromptsConfig(**config_dict.get('prompts', {})),
            tech_blogs=TechBlogsConfig(config_dict.get('tech_blogs', {})),
            files=FilesConfig(**config_dict.get('files', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Config instance to dictionary"""
        return {
            'api': asdict(self.api),
            'scraping': asdict(self.scraping),
            'filtering': asdict(self.filtering),
            'output': asdict(self.output),
            'prompts': asdict(self.prompts),
            'tech_blogs': self.tech_blogs.blogs,
            'files': asdict(self.files)
        }

class ConfigManager:
    """Manages configuration loading, validation, and access"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self._config: Optional[Config] = None

    def load_config(self) -> Config:
        """Load configuration from JSON file"""
        try:
            config_path = Path(self.config_file)
            
            if not config_path.exists():
                print(f"Config file {self.config_file} not found. Creating default config.")
                self._create_default_config()
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            self._config = Config.from_dict(config_dict)
            self._validate_config()
            print(f"Configuration loaded successfully from {self.config_file}")
            
            return self._config
            
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in config file: {e}")
            raise
        except Exception as e:
            print(f"Error loading configuration: {e}")
            raise

    def save_config(self, config: Config, filename: Optional[str] = None) -> None:
        """Save configuration to JSON file"""
        try:
            save_path = Path(filename) if filename else Path(self.config_file)
            
            # Ensure output directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"Configuration saved to {save_path}")
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
            raise

    def get_config(self) -> Config:
        """Get current configuration, loading if necessary"""
        if self._config is None:
            self._config = self.load_config()
        return self._config

    def reload_config(self) -> Config:
        """Reload configuration from file"""
        self._config = None
        return self.get_config()

    def _create_default_config(self) -> None:
        """Create default configuration file"""
        default_config = Config(
            api=APIConfig(),
            scraping=ScrapingConfig(),
            filtering=FilteringConfig(),
            output=OutputConfig(),
            prompts=PromptsConfig(),
            tech_blogs=TechBlogsConfig(),
            files=FilesConfig()
        )
        self.save_config(default_config)

    def _validate_config(self) -> None:
        """Validate configuration values"""
        if not self._config:
            return
        
        # Validate API config
        if self._config.api.temperature < 0 or self._config.api.temperature > 2:
            raise ValueError("API temperature must be between 0 and 2")
        
        if self._config.api.timeout <= 0:
            raise ValueError("API timeout must be positive")
        
        # Validate scraping config
        if self._config.scraping.per_blog_limit <= 0:
            raise ValueError("Per blog limit must be positive")
        
        if self._config.scraping.retry_attempts < 0:
            raise ValueError("Retry attempts cannot be negative")
        
        # Validate filtering config
        if not (0 <= self._config.filtering.relevance_threshold <= 10):
            raise ValueError("Relevance threshold must be between 0 and 10")
        
        if not (0 <= self._config.filtering.deduplication_threshold <= 1):
            raise ValueError("Deduplication threshold must be between 0 and 1")
        
        # Validate output config
        if self._config.output.max_summary_length <= 0:
            raise ValueError("Max summary length must be positive")
        
        print("Configuration validation passed")

# Global config manager instance
config_manager = ConfigManager()

def get_config() -> Config:
    """Get the global configuration instance"""
    return config_manager.get_config()

def reload_config() -> Config:
    """Reload the global configuration"""
    return config_manager.reload_config()
