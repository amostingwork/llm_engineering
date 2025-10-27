# Personalised Newsfeed - Configuration Management

This document explains the simplified configuration management system for the personalised newsfeed application.

## Overview

The application uses a JSON-based configuration system that allows you to customize all aspects of the newsfeed without modifying code. The configuration is now simplified with direct prompt specification instead of granular user profile settings.

## Configuration File

The main configuration is stored in `config.json`. This file contains all settings organized into logical sections:

### API Configuration (`api`)
- `ollama_base_url`: Base URL for Ollama API (default: "http://localhost:11434/v1")
- `ollama_api_key`: API key for Ollama (default: "ollama")
- `model_name`: LLM model to use (default: "llama3.2")
- `temperature`: Model temperature for response generation (default: 0.2)
- `timeout`: Request timeout in seconds (default: 30)

### Scraping Configuration (`scraping`)
- `per_blog_limit`: Maximum articles to fetch per blog (default: 20)
- `request_timeout`: Timeout for RSS feed requests (default: 10)
- `retry_attempts`: Number of retry attempts for failed requests (default: 3)
- `retry_delay`: Delay between retry attempts in seconds (default: 1)
- `user_agent`: User agent string for requests (default: "PersonalisedNewsfeed/1.0")

### Filtering Configuration (`filtering`)
- `relevance_threshold`: Minimum relevance score for articles (default: 6.0)
- `max_articles_to_process`: Maximum articles to process in one batch (default: 100)
- `enable_deduplication`: Whether to remove duplicate articles (default: true)
- `deduplication_threshold`: Similarity threshold for deduplication (default: 0.8)

### Output Configuration (`output`)
- `output_directory`: Directory for output files (default: "output")
- `markdown_filename`: Name of the markdown output file (default: "relevant_articles.md")
- `include_timestamp`: Whether to include timestamp in filename (default: true)
- `sort_by_score`: Whether to sort articles by relevance score (default: true)
- `max_summary_length`: Maximum length for article summaries (default: 500)

### Prompts Configuration (`prompts`)
- `system_prompt`: Complete system prompt for the LLM
- `user_prompt`: Complete user prompt describing interests and requirements

### Tech Blogs Configuration (`tech_blogs`)
- Dictionary mapping blog names to RSS feed URLs
- Example:
  ```json
  "tech_blogs": {
    "Netflix_tech_blog": "https://netflixtechblog.com/feed",
    "Stack_Overflow_blog": "https://stackoverflow.blog/feed"
  }
  ```

### File Paths (`files`)
- `cache_file`: Path to cache file (default: "feed_cache.json")

## Usage

### Basic Usage
The application automatically loads configuration from `config.json` when started:

```python
from config_manager import get_config

config = get_config()
print(f"Using model: {config.api.model_name}")
print(f"System prompt: {config.prompts.system_prompt}")
```

### Custom Configuration
You can create custom configuration files:

```python
from config_manager import ConfigManager

# Load custom config
config_manager = ConfigManager("my_custom_config.json")
config = config_manager.load_config()
```

## Configuration Manager Features

### Validation
The configuration manager validates all settings to ensure they're within acceptable ranges:
- Temperature must be between 0 and 2
- Relevance threshold must be between 0 and 10
- Timeout values must be positive
- Deduplication threshold must be between 0 and 1

### Error Handling
- Graceful fallback to default values if configuration is invalid
- Detailed error messages for troubleshooting
- Automatic creation of default configuration if file doesn't exist

## Example Configuration

Here's a sample `config.json` for a senior developer interested in AI and system design:

```json
{
  "api": {
    "model_name": "llama3.1",
    "temperature": 0.1
  },
  "scraping": {
    "per_blog_limit": 50
  },
  "filtering": {
    "relevance_threshold": 7.0,
    "max_articles_to_process": 200
  },
  "prompts": {
    "system_prompt": "You are a senior software engineer with expertise in AI, machine learning, and distributed systems. You help identify the most relevant and cutting-edge articles for professional development.",
    "user_prompt": "I am a senior software engineer working on AI/ML systems and distributed architectures. I'm interested in articles about: machine learning advances, system design patterns, performance optimization, cloud architecture, and emerging technologies. Help me find articles that will advance my technical knowledge and keep me current with industry trends."
  },
  "tech_blogs": {
    "Netflix_tech_blog": "https://netflixtechblog.com/feed",
    "Stack_Overflow_blog": "https://stackoverflow.blog/feed",
    "Google_AI_blog": "https://ai.googleblog.com/feeds/posts/default",
    "AWS_blog": "https://aws.amazon.com/blogs/aws/feed/"
  }
}
```

## Migration from Old System

The new configuration system is backward compatible. If you don't have a `config.json` file, the system will:
1. Create a default configuration file
2. Use default values for all settings
3. Continue working as before

## Benefits

1. **No Code Changes**: Modify behavior without touching Python code
2. **Direct Prompt Control**: Specify exact prompts instead of building them from components
3. **Environment-Specific**: Different configs for development, staging, production
4. **Validation**: Automatic validation prevents configuration errors
5. **Simplicity**: Cleaner, more straightforward configuration structure
6. **Extensibility**: Easy to add new configuration options

## Troubleshooting

### Common Issues

1. **Invalid JSON**: Check your `config.json` syntax
2. **Missing Values**: The system will use defaults for missing values
3. **Permission Errors**: Ensure write permissions for output directories
4. **API Errors**: Verify Ollama is running and accessible

### Configuration Validation
The system will automatically validate your configuration and provide helpful error messages if there are issues with:
- Invalid temperature values
- Negative timeout values
- Invalid relevance thresholds
- Missing required fields
