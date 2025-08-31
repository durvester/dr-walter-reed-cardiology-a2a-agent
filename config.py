"""
Configuration Management for Dr. Walter Reed's Interventional Cardiology A2A Agent

This module provides centralized configuration management with no hardcoded values.
All configuration is sourced from environment variables with sensible defaults.

Requirements:
- No hardcoded values as mandated by user
- All settings configurable via environment variables
- Proper defaults for local development
- Clear documentation for all configuration options
"""

import os
from typing import Dict, List
from dataclasses import dataclass
from pathlib import Path

# Load .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print("ℹ️  No .env file found, using system environment variables")
except ImportError:
    print("ℹ️  python-dotenv not installed, using system environment variables only")

@dataclass
class AgentConfig:
    """Configuration for the A2A agent identity and capabilities"""
    
    # Agent Identity Configuration
    agent_name: str = os.getenv("AGENT_NAME", "Dr. Walter Reed's Interventional Cardiology Assistant")
    agent_description: str = os.getenv("AGENT_DESCRIPTION", 
        "AI assistant for Dr. Walter Reed's Interventional Cardiology Practice - "
        "specializing in advanced cardiac procedures, heart failure management, and "
        "comprehensive cardiovascular care coordination"
    )
    agent_version: str = os.getenv("AGENT_VERSION", "1.0.0")
    
    # Practice Specialization Configuration
    practice_name: str = os.getenv("PRACTICE_NAME", "Dr. Walter Reed's Interventional Cardiology")
    practice_location: str = os.getenv("PRACTICE_LOCATION", "")  # No default location
    
    # Interventional Cardiology Services Configuration
    primary_services: List[str] = None
    diagnostic_services: List[str] = None
    specialized_procedures: List[str] = None
    
    def __post_init__(self):
        """Initialize service lists from environment variables"""
        if self.primary_services is None:
            self.primary_services = self._get_list_from_env("PRIMARY_SERVICES", [
                "Angiography (diagnostic and interventional)",
                "Angioplasty procedures (balloon and stent)",
                "Heart failure management and optimization",
                "Ischemic heart disease treatment",
                "Stroke prevention and acute management"
            ])
        
        if self.diagnostic_services is None:
            self.diagnostic_services = self._get_list_from_env("DIAGNOSTIC_SERVICES", [
                "Stress testing (exercise and pharmacological)",
                "Electrocardiography (12-lead ECG)",
                "2D Echocardiography with Doppler",
                "Cardiac catheterization procedures"
            ])
        
        if self.specialized_procedures is None:
            self.specialized_procedures = self._get_list_from_env("SPECIALIZED_PROCEDURES", [
                "Percutaneous coronary interventions",
                "Cardiac stenting procedures",
                "Balloon angioplasty",
                "Acute myocardial infarction management",
                "Complex coronary lesion treatment"
            ])
    
    def _get_list_from_env(self, env_var: str, default: List[str]) -> List[str]:
        """Get a list from environment variable (comma-separated) or use default"""
        env_value = os.getenv(env_var)
        if env_value:
            return [item.strip() for item in env_value.split(",") if item.strip()]
        return default

@dataclass
class ServerConfig:
    """Configuration for the A2A server and network settings"""
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "9999"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "info")
    
    # A2A Protocol Configuration
    protocol_version: str = os.getenv("A2A_PROTOCOL_VERSION", "0.2.9")
    streaming_enabled: bool = os.getenv("STREAMING_ENABLED", "true").lower() == "true"
    push_notifications_enabled: bool = os.getenv("PUSH_NOTIFICATIONS_ENABLED", "false").lower() == "true"
    
    # Agent Card Configuration
    agent_card_path: str = os.getenv("AGENT_CARD_PATH", "/.well-known/agent-card.json")
    base_url: str = os.getenv("BASE_URL", f"http://localhost:{port}")
    
    # Input/Output Mode Configuration  
    default_input_modes: List[str] = None
    default_output_modes: List[str] = None
    
    def __post_init__(self):
        """Initialize mode lists from environment variables"""
        if self.default_input_modes is None:
            self.default_input_modes = self._get_list_from_env("DEFAULT_INPUT_MODES", [
                "text/plain",
                "application/json"
            ])
        
        if self.default_output_modes is None:
            self.default_output_modes = self._get_list_from_env("DEFAULT_OUTPUT_MODES", [
                "text/plain",
                "application/json"
            ])
    
    def _get_list_from_env(self, env_var: str, default: List[str]) -> List[str]:
        """Get a list from environment variable (comma-separated) or use default"""
        env_value = os.getenv(env_var)
        if env_value:
            return [item.strip() for item in env_value.split(",") if item.strip()]
        return default

@dataclass
class ClaudeConfig:
    """Configuration for Claude API integration"""
    
    # Claude API Configuration
    api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    max_tokens: int = int(os.getenv("CLAUDE_MAX_TOKENS", "1500"))
    temperature: float = float(os.getenv("CLAUDE_TEMPERATURE", "0.3"))
    
    # System Prompt Configuration (configurable but with medical default)
    system_prompt_template: str = os.getenv("SYSTEM_PROMPT_TEMPLATE", """
You are an AI agent representing {practice_name}.

You are a specialized medical assistant focused on interventional cardiology and provide professional medical information to healthcare agents and providers.

Your expertise covers:

PRIMARY SERVICES:
{primary_services}

DIAGNOSTIC CAPABILITIES:
{diagnostic_services}

SPECIALIZED PROCEDURES:
{specialized_procedures}

PROFESSIONAL GUIDELINES:
- Maintain the highest standards of medical professionalism
- Provide accurate, evidence-based information about procedures and protocols
- Coordinate care between healthcare providers and specialists
- Explain complex medical procedures in clear, professional language
- Always emphasize the importance of proper medical evaluation and referrals
- Never provide direct medical advice to patients - focus on provider coordination

IMPORTANT: You provide information and coordination services only. You cannot:
- Make medical diagnoses
- Prescribe treatments
- Schedule actual appointments (Phase 1 limitation)
- Access patient medical records
- Replace clinical judgment

Your responses should demonstrate deep knowledge of interventional cardiology while maintaining appropriate professional boundaries.
""".strip())
    
    def validate(self) -> bool:
        """Validate Claude configuration"""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return True

@dataclass  
class SecurityConfig:
    """Configuration for security and validation settings"""
    
    # Input Validation Configuration
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "10000"))
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    allowed_file_types: List[str] = None
    
    # Security Feature Configuration
    enable_input_sanitization: bool = os.getenv("ENABLE_INPUT_SANITIZATION", "true").lower() == "true"
    enable_prompt_injection_protection: bool = os.getenv("ENABLE_PROMPT_INJECTION_PROTECTION", "true").lower() == "true"
    
    # Rate Limiting Configuration
    rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
    rate_limit_requests_per_minute: int = int(os.getenv("RATE_LIMIT_RPM", "60"))
    
    def __post_init__(self):
        """Initialize allowed file types from environment"""
        if self.allowed_file_types is None:
            self.allowed_file_types = self._get_list_from_env("ALLOWED_FILE_TYPES", [
                "text/plain",
                "text/markdown", 
                "application/pdf",
                "image/png",
                "image/jpeg"
            ])
    
    def _get_list_from_env(self, env_var: str, default: List[str]) -> List[str]:
        """Get a list from environment variable (comma-separated) or use default"""
        env_value = os.getenv(env_var)
        if env_value:
            return [item.strip() for item in env_value.split(",") if item.strip()]
        return default

class ConfigManager:
    """Central configuration manager that coordinates all configuration aspects"""
    
    def __init__(self):
        self.agent = AgentConfig()
        self.server = ServerConfig()
        self.claude = ClaudeConfig()
        self.security = SecurityConfig()
        
        # Validate all configurations
        self._validate_all()
    
    def _validate_all(self):
        """Validate all configuration sections"""
        self.claude.validate()
        
        # Additional cross-configuration validation
        if self.server.port < 1024 or self.server.port > 65535:
            raise ValueError(f"Invalid port number: {self.server.port}")
        
        if self.claude.max_tokens < 100 or self.claude.max_tokens > 4096:
            raise ValueError(f"Invalid max_tokens: {self.claude.max_tokens}")
    
    def get_formatted_system_prompt(self) -> str:
        """Get the system prompt formatted with current configuration"""
        return self.claude.system_prompt_template.format(
            practice_name=self.agent.practice_name,
            primary_services="\n".join(f"- {service}" for service in self.agent.primary_services),
            diagnostic_services="\n".join(f"- {service}" for service in self.agent.diagnostic_services),  
            specialized_procedures="\n".join(f"- {procedure}" for procedure in self.agent.specialized_procedures)
        )
    
    def get_agent_card_data(self) -> Dict:
        """Generate agent card data from configuration"""
        return {
            "protocolVersion": self.server.protocol_version,
            "name": self.agent.agent_name,
            "description": self.agent.agent_description,
            "version": self.agent.agent_version,
            "url": self.server.base_url,
            "defaultInputModes": self.server.default_input_modes,
            "defaultOutputModes": self.server.default_output_modes,
            "capabilities": {
                "streaming": self.server.streaming_enabled,
                "pushNotifications": self.server.push_notifications_enabled
            }
        }
    
    def print_config_summary(self):
        """Print a summary of current configuration (for debugging)"""
        print(f"Dr. Walter Reed's Interventional Cardiology Agent Configuration:")
        print(f"  Agent: {self.agent.agent_name}")
        print(f"  Version: {self.agent.agent_version}")
        print(f"  Server: {self.server.host}:{self.server.port}")
        print(f"  Claude Model: {self.claude.model}")
        print(f"  Services: {len(self.agent.primary_services)} primary, {len(self.agent.diagnostic_services)} diagnostic")
        print(f"  Security: Input validation={self.security.enable_input_sanitization}")

# Global configuration instance
config = ConfigManager()