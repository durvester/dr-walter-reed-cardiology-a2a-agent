# Dr. Walter Reed's Interventional Cardiology A2A Agent
## Complete Implementation and Setup Guide

**Agent Specialization**: Interventional Cardiology  
**Target Users**: Healthcare providers, medical coordinators, specialist referrals  
**A2A Protocol Version**: 0.2.9  
**Implementation**: Official A2A SDK with full compliance  

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation and Setup](#installation-and-setup)
4. [Configuration](#configuration)
5. [Running the Agent](#running-the-agent)
6. [Testing and Validation](#testing-and-validation)
7. [A2A Protocol Compliance](#a2a-protocol-compliance)
8. [Medical Specialization](#medical-specialization)
9. [Security Features](#security-features)
10. [Troubleshooting](#troubleshooting)
11. [Architecture](#architecture)
12. [Development Notes](#development-notes)

---

## Overview

Dr. Walter Reed's Interventional Cardiology A2A Agent is a specialized healthcare AI agent designed to facilitate communication and coordination between healthcare providers regarding advanced cardiac procedures. The agent focuses on interventional cardiology services, providing professional medical information and care coordination.

### Key Features

- **Specialized Medical Expertise**: Interventional cardiology procedures, heart failure management, diagnostic services
- **A2A Protocol Compliance**: Full implementation using official Google A2A SDK v0.3.3
- **Professional Communication**: Healthcare provider-focused interactions with medical terminology
- **Security First**: Input validation, prompt injection protection, sensitive data filtering
- **No Hardcoded Values**: Complete configuration management via environment variables
- **Streaming Support**: Server-Sent Events (SSE) for real-time communication

### Medical Specializations

- **Angiography**: Diagnostic and interventional cardiac catheterization procedures
- **Angioplasty**: Balloon and stent procedures for coronary interventions
- **Heart Failure Management**: Comprehensive monitoring and optimization protocols
- **Ischemic Heart Disease**: CAD treatment and acute coronary syndrome management
- **Stroke Prevention**: Cardiovascular-related stroke risk management
- **Advanced Diagnostics**: Stress testing, ECG, 2D echocardiography

---

## Prerequisites

### System Requirements

- **Python**: 3.10 or higher (tested with Python 3.13.7)
- **Operating System**: macOS, Linux, or Windows
- **Memory**: Minimum 512MB RAM available
- **Network**: Internet connection for Claude API access

### Required Accounts and Keys

- **Anthropic Claude API Key**: Required for LLM integration
- **Fly.io Account**: Optional, for deployment (Phase 2)

### Development Tools (Recommended)

- Python virtual environment management (`venv` or `conda`)
- Code editor with Python support (VS Code, PyCharm, etc.)
- HTTP client for testing (curl, Postman, or similar)

---

## Installation and Setup

### Step 1: Project Setup

```bash
# Clone or create project directory
mkdir cardiology-agent
cd cardiology-agent

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify Python version (should be 3.10+)
python --version
```

### Step 2: Install Dependencies

```bash
# Install official A2A SDK with all necessary extras
pip install "a2a-sdk[http-server,telemetry,sql]"

# Install Claude API client
pip install anthropic

# Verify installations
pip list | grep -E "(a2a-sdk|anthropic)"
```

### Step 3: Project Files

The project should contain these files (all provided):

```
cardiology-agent/
├── __main__.py          # Main application entry point
├── agent_executor.py    # InterventionalCardiologyExecutor implementation
├── config.py           # Configuration management (no hardcoded values)
├── test_client.py      # A2A SDK test client
├── requirements.txt    # Dependencies specification
├── claude.md          # This documentation file
├── audit-trail.md     # Implementation audit trail
└── venv/              # Python virtual environment
```

### Step 4: Environment Configuration

Create a `.env` file or set environment variables:

```bash
# Required
export ANTHROPIC_API_KEY="your-claude-api-key-here"

# Optional (with defaults)
export PORT="9999"
export HOST="0.0.0.0"
export DEBUG="false"
export LOG_LEVEL="info"
export CLAUDE_MODEL="claude-3-5-sonnet-20241022"

# Advanced configuration (optional)
export AGENT_NAME="Dr. Walter Reed's Interventional Cardiology Assistant"
export PRACTICE_NAME="Dr. Walter Reed's Interventional Cardiology"
export MAX_MESSAGE_LENGTH="10000"
export ENABLE_INPUT_SANITIZATION="true"
```

---

## Configuration

The agent uses a comprehensive configuration management system with **no hardcoded values**. All settings are configurable via environment variables.

### Core Configuration Classes

#### `AgentConfig`
- **Agent identity and practice information**
- **Medical specializations and services**
- **Practice-specific details**

#### `ServerConfig`  
- **Network and protocol settings**
- **A2A compliance parameters**
- **Input/output mode specifications**

#### `ClaudeConfig`
- **Claude API integration settings**
- **Model selection and parameters**
- **System prompt configuration**

#### `SecurityConfig`
- **Input validation rules**
- **Security feature toggles**
- **Rate limiting settings**

### Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *Required* | Claude API key |
| `PORT` | `9999` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `AGENT_NAME` | Dr. Walter Reed's... | Agent identity |
| `CLAUDE_MODEL` | claude-3-5-sonnet... | Claude model version |
| `DEBUG` | `false` | Enable debug logging |
| `STREAMING_ENABLED` | `true` | Enable SSE streaming |
| `MAX_MESSAGE_LENGTH` | `10000` | Max input length |
| `ENABLE_INPUT_SANITIZATION` | `true` | Input validation |

### Advanced Configuration

#### Custom Medical Services

```bash
# Customize primary services (comma-separated)
export PRIMARY_SERVICES="Angiography procedures,Angioplasty interventions,Heart failure optimization"

# Customize diagnostic services
export DIAGNOSTIC_SERVICES="Stress testing,ECG monitoring,2D Echocardiography"

# Customize specialized procedures  
export SPECIALIZED_PROCEDURES="PCI procedures,Cardiac stenting,Complex lesion treatment"
```

#### Security Settings

```bash
# Input validation
export MAX_MESSAGE_LENGTH="15000"
export MAX_FILE_SIZE_MB="5"
export ALLOWED_FILE_TYPES="text/plain,text/markdown,application/pdf"

# Security features
export ENABLE_PROMPT_INJECTION_PROTECTION="true"
export ENABLE_INPUT_SANITIZATION="true"
export RATE_LIMIT_ENABLED="true"
export RATE_LIMIT_RPM="120"
```

---

## Running the Agent

### Local Development

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Set required environment variable
export ANTHROPIC_API_KEY="your-api-key"

# Start the agent
python __main__.py
```

**Expected Output:**
```
================================================================================
Dr. Walter Reed's Interventional Cardiology A2A Agent
================================================================================
Dr. Walter Reed's Interventional Cardiology Agent Configuration:
  Agent: Dr. Walter Reed's Interventional Cardiology Assistant
  Version: 1.0.0
  Server: 0.0.0.0:9999
  Claude Model: claude-3-5-sonnet-20241022
  Services: 5 primary, 4 diagnostic
  Security: Input validation=True
Starting server on 0.0.0.0:9999
Agent card will be available at: http://localhost:9999/.well-known/agent-card.json
A2A endpoint: http://localhost:9999/
```

### Verify Agent Card

```bash
# Test agent card accessibility
curl http://localhost:9999/.well-known/agent-card.json | jq '.'

# Expected: JSON with agent identity, skills, and capabilities
```

### Basic Communication Test

```bash
# Test basic A2A communication
curl -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Hello, what services do you offer?"}]
      }
    }
  }'
```

---

## Testing and Validation

### Automated Test Suite

The project includes a comprehensive test client:

```bash
# Run the complete test suite
python test_client.py
```

**Test Categories:**
1. **Basic Protocol Tests** - A2A compliance validation
2. **Agent Card Tests** - Discovery and metadata validation  
3. **Interventional Cardiology Knowledge** - Medical expertise validation
4. **Heart Failure Management** - Specialized knowledge testing
5. **Diagnostic Services** - Comprehensive service validation
6. **Multi-Turn Conversations** - Context management testing
7. **Security and Validation** - Input sanitization and protection
8. **Error Handling** - Edge case and error recovery testing

### Manual Testing Scenarios

#### Scenario 1: Interventional Consultation
```bash
# Test interventional cardiology knowledge
python -c "
import asyncio
from a2a.client import A2AClient

async def test():
    client = A2AClient.from_url('http://localhost:9999')
    response = await client.send_message_async('I need information about angioplasty procedures for my patient with complex coronary lesions.')
    print('Response:', response.content if hasattr(response, 'content') else response)

asyncio.run(test())
"
```

#### Scenario 2: Multi-turn Medical Consultation
```python
# Multi-turn conversation test
import asyncio
from a2a.client import A2AClient

async def multi_turn_test():
    client = A2AClient.from_url('http://localhost:9999')
    
    # Initial consultation
    response1 = await client.send_message_async(
        "I'm referring a patient for coronary angiography."
    )
    print("Response 1:", response1.content)
    
    # Follow-up with specifics
    response2 = await client.send_message_async(
        "The patient has diabetes and chronic kidney disease. What precautions should we consider?"
    )
    print("Response 2:", response2.content)

asyncio.run(multi_turn_test())
```

### A2A Inspector Integration

For comprehensive A2A protocol validation:

```bash
# Clone and set up A2A Inspector
git clone https://github.com/a2aproject/a2a-inspector
cd a2a-inspector
# Follow inspector setup instructions

# Point inspector to your agent
# URL: http://localhost:9999
# Test all A2A protocol methods and compliance
```

---

## A2A Protocol Compliance

### Supported A2A Methods

#### Core Methods (Required)
- ✅ **message/send** - Send message and get task snapshot
- ✅ **message/stream** - Send message with SSE streaming responses
- ✅ **tasks/get** - Retrieve task by ID with full history
- ✅ **tasks/cancel** - Cancel active task
- ✅ **tasks/resubscribe** - Resume SSE stream for existing task

#### Protocol Features
- ✅ **JSON-RPC 2.0** - Full specification compliance
- ✅ **Server-Sent Events** - Real-time streaming support
- ✅ **Task Lifecycle Management** - Complete state transitions
- ✅ **Agent Card Discovery** - Proper metadata publication
- ✅ **Error Handling** - A2A-specific error codes (-32001 to -32099)

#### Message Part Support
- ✅ **Text Parts** - Professional medical communication
- ✅ **File Parts** - Medical document handling (PDF, images, text)
- ✅ **Data Parts** - Structured medical data exchange

### Agent Card Specification

The agent publishes a complete A2A v0.2.9 compliant agent card:

```json
{
  "protocolVersion": "0.2.9",
  "name": "Dr. Walter Reed's Interventional Cardiology Assistant",
  "description": "AI assistant for Dr. Walter Reed's Interventional Cardiology Practice...",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "interventional_procedures",
      "name": "Interventional Cardiology Procedures",
      "description": "Coordinate and provide information about advanced interventional...",
      "tags": ["interventional", "angiography", "angioplasty", "stenting"],
      "examples": ["I need angiography information", "Schedule angioplasty consultation"]
    }
    // ... additional specialized skills
  ]
}
```

---

## Medical Specialization

### Clinical Focus Areas

#### 1. Interventional Procedures
- **Cardiac Catheterization**: Diagnostic and therapeutic procedures
- **Percutaneous Coronary Intervention (PCI)**: Advanced coronary interventions
- **Angioplasty**: Balloon angioplasty and stent placement
- **Complex Lesion Management**: Specialized intervention techniques

#### 2. Heart Failure Management  
- **Optimization Therapy**: Medical management protocols
- **Monitoring Programs**: Comprehensive patient monitoring
- **Advanced Therapies**: Latest treatment modalities
- **Multidisciplinary Coordination**: Team-based care approaches

#### 3. Ischemic Heart Disease
- **Acute Coronary Syndromes**: Emergency management protocols
- **Chronic CAD Management**: Long-term treatment strategies
- **Secondary Prevention**: Risk factor modification
- **Revascularization Planning**: Procedure selection and timing

#### 4. Stroke Prevention and Management
- **Cardiovascular Stroke Risk**: Assessment and modification
- **Anticoagulation Management**: Complex medication protocols
- **Acute Stroke Protocols**: Emergency response procedures
- **Secondary Prevention**: Long-term risk management

#### 5. Advanced Diagnostics
- **Exercise Stress Testing**: Functional cardiac assessment
- **Pharmacological Stress Testing**: Alternative diagnostic approaches
- **12-lead Electrocardiography**: Comprehensive ECG interpretation
- **2D Echocardiography**: Structural and functional imaging

### Communication Standards

#### Professional Medical Language
- Evidence-based information delivery
- Appropriate medical terminology
- Clear procedural explanations
- Risk assessment communication

#### Healthcare Provider Focus
- Provider-to-provider communication
- Medical coordination language
- Referral management protocols
- Care transition planning

#### Ethical Guidelines
- Professional boundary maintenance
- No direct patient medical advice
- Emphasis on clinical evaluation
- Referral requirement communication

---

## Security Features

### Input Validation and Sanitization

#### Message Length Limits
```python
# Configurable via environment
MAX_MESSAGE_LENGTH = 10000  # characters
MAX_FILE_SIZE_MB = 10       # megabytes
```

#### Content Filtering
- **Sensitive Data Detection**: Credit cards, SSN, passwords
- **Prompt Injection Protection**: Malicious instruction detection
- **File Type Validation**: Allowed MIME types only
- **Content Sanitization**: Input cleaning and validation

#### Security Patterns
```python
# Prompt injection detection
r'(ignore|forget|disregard).*(previous|above|instruction)'

# Sensitive data patterns  
r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'  # Credit cards
r'\b\d{3}-\d{2}-\d{4}\b'                        # SSN format
```

### Error Handling

#### Graceful Degradation
- API connection failures handled
- Invalid input gracefully processed
- Security violations properly blocked
- User-friendly error messages

#### Logging and Monitoring
```python
# Security event logging
logger.warning("Potential prompt injection attempt detected")
logger.warning("Sensitive data detected in message") 
logger.error(f"Claude API error: {str(e)}")
```

### Rate Limiting (Optional)
```bash
export RATE_LIMIT_ENABLED="true"
export RATE_LIMIT_RPM="120"  # requests per minute
```

---

## Troubleshooting

### Common Issues

#### 1. Claude API Key Issues
**Problem**: `ANTHROPIC_API_KEY environment variable is required`

**Solution**:
```bash
# Set the API key
export ANTHROPIC_API_KEY="your-actual-api-key"

# Verify it's set
echo $ANTHROPIC_API_KEY
```

#### 2. Import Errors
**Problem**: `ImportError: No module named 'a2a'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install "a2a-sdk[http-server,telemetry,sql]" anthropic

# Verify installation
pip list | grep a2a-sdk
```

#### 3. Port Already in Use
**Problem**: `Address already in use`

**Solution**:
```bash
# Use different port
export PORT="9998"

# Or find and kill existing process
lsof -ti:9999 | xargs kill -9
```

#### 4. Agent Card Not Accessible
**Problem**: `404 Not Found` for agent card

**Solution**:
```bash
# Check server is running
curl -I http://localhost:9999/

# Verify agent card endpoint
curl http://localhost:9999/.well-known/agent-card.json
```

#### 5. Claude API Errors
**Problem**: `Claude API error: Authentication failed`

**Solutions**:
- Verify API key is correct and active
- Check Claude API usage limits
- Ensure internet connectivity
- Check for Claude API service status

#### 6. Memory Issues
**Problem**: High memory usage or slow responses

**Solutions**:
```bash
# Reduce Claude token limits
export CLAUDE_MAX_TOKENS="1000"

# Reduce message length limits
export MAX_MESSAGE_LENGTH="5000"

# Enable debug logging to monitor
export DEBUG="true"
export LOG_LEVEL="debug"
```

### Debug Mode

Enable comprehensive debugging:

```bash
export DEBUG="true"
export LOG_LEVEL="debug"
python __main__.py
```

**Debug Output Includes**:
- Configuration validation details
- Claude API request/response info
- Security validation results
- Task execution timing
- Error stack traces

### Performance Monitoring

#### Response Time Monitoring
```python
# Built-in timing logs in debug mode
logger.debug(f"Generated response length: {len(response_text)} characters")
logger.debug(f"Generating response with {len(conversation_context)} context messages")
```

#### Health Check Endpoint
```bash
# Basic health check
curl http://localhost:9999/health

# Agent card availability check
curl -I http://localhost:9999/.well-known/agent-card.json
```

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    A2A Client Applications                     │
│                  (Inspector, Other Agents)                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │ A2A Protocol (JSON-RPC 2.0 + SSE)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Dr. Walter Reed's A2A Agent                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                A2AStarletteApplication                      │ │
│  │           (Official A2A SDK Framework)                     │ │
│  └─────────────────────┬───────────────────────────────────────┘ │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              DefaultRequestHandler                          │ │
│  │              (A2A SDK Component)                            │ │
│  └─────────────────────┬───────────────────────────────────────┘ │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │        InterventionalCardiologyExecutor                     │ │
│  │            (Custom Medical Logic)                           │ │
│  └─────────────────────┬───────────────────────────────────────┘ │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              ConfigManager                                  │ │
│  │           (No Hardcoded Values)                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Claude API Calls
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Anthropic Claude API                            │
│              (Medical Knowledge Base)                           │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### `A2AStarletteApplication` (SDK)
- HTTP server management
- A2A protocol implementation
- Request routing and validation
- SSE streaming support

#### `DefaultRequestHandler` (SDK)
- A2A method handling
- Task lifecycle management  
- Message parsing and validation
- Response formatting

#### `InterventionalCardiologyExecutor` (Custom)
- Medical domain expertise
- Claude API integration
- Security validation
- Professional communication

#### `ConfigManager` (Custom)
- Environment-based configuration
- No hardcoded values
- Validation and defaults
- Cross-component configuration

### Data Flow

1. **A2A Client** sends JSON-RPC request
2. **A2AStarletteApplication** receives and validates
3. **DefaultRequestHandler** processes A2A protocol
4. **InterventionalCardiologyExecutor** handles medical logic
5. **ConfigManager** provides configuration data
6. **Claude API** generates medical responses
7. **Response flows back** through same path
8. **SSE streaming** for real-time updates

### File Organization

```
cardiology-agent/
├── __main__.py              # Application entry point and A2A setup
├── agent_executor.py        # Medical domain logic and Claude integration
├── config.py               # Configuration management (no hardcoding)
├── test_client.py          # A2A protocol testing and validation
├── requirements.txt        # Dependencies specification  
├── claude.md              # Complete documentation (this file)
├── audit-trail.md         # Implementation audit trail
└── venv/                  # Python virtual environment
    └── ...                # A2A SDK and dependencies
```

---

## Development Notes

### Code Quality Standards

#### No Hardcoded Values Policy
- **All configuration** via environment variables
- **Default values** provided in configuration classes
- **Validation** for all configuration parameters
- **Clear documentation** for all environment variables

#### Medical Communication Standards
- **Professional terminology** appropriate for healthcare providers
- **Evidence-based information** delivery
- **Clear procedural explanations** with medical accuracy
- **Appropriate scope** limitations clearly communicated

#### Security First Approach
- **Input validation** for all user content
- **Prompt injection protection** against malicious instructions
- **Sensitive data filtering** to protect privacy
- **Comprehensive error handling** with user-friendly messages

#### A2A Protocol Compliance
- **Official SDK usage** for guaranteed compliance
- **All required methods** implemented and tested
- **Proper error codes** following A2A specification
- **Agent card compliance** with complete metadata

### Testing Strategy

#### Automated Testing
- **Protocol compliance** validation using A2A SDK client
- **Medical knowledge** testing with healthcare scenarios
- **Security validation** testing with malicious inputs
- **Multi-turn conversation** testing for context management

#### Manual Testing  
- **A2A Inspector** integration for comprehensive validation
- **Healthcare provider scenarios** for domain expertise validation
- **Edge case testing** for error handling verification
- **Performance testing** for response time optimization

#### Continuous Validation
- **Agent card accessibility** monitoring
- **Claude API integration** health checking
- **Security feature** effectiveness validation
- **Medical response quality** assessment

### Phase 2 Preparation

#### Planned Enhancements
- **MCP tool integration** for EHR access
- **Complex scheduling workflows** with real appointment systems
- **Enhanced conversation management** with persistent context
- **Production monitoring** and alerting systems
- **Fly.io deployment** with HTTPS and scaling

#### Architecture Considerations
- **Stateless design** for horizontal scaling
- **Plugin architecture** for tool integration
- **Configuration management** for multi-environment deployment
- **Monitoring and observability** for production operations

### Contributing Guidelines

#### Code Style
- **Type hints** for all function parameters and returns
- **Docstring documentation** for all classes and methods
- **Comprehensive logging** for debugging and monitoring
- **Error handling** with appropriate user messaging

#### Testing Requirements
- **All new features** must include automated tests
- **Security features** must include vulnerability testing
- **Medical knowledge** must be validated by healthcare experts
- **A2A compliance** must be verified with official tools

#### Documentation Standards
- **Configuration changes** must be documented in this file
- **API changes** must be reflected in agent card
- **Security implications** must be clearly documented
- **Audit trail** must be maintained for all changes

---

## Conclusion

Dr. Walter Reed's Interventional Cardiology A2A Agent represents a comprehensive implementation of the A2A protocol with specialized medical expertise. The agent provides professional healthcare communication capabilities while maintaining strict security standards and complete protocol compliance.

The implementation follows best practices for medical AI systems, enterprise security, and distributed agent architectures. All components are designed for production deployment with comprehensive configuration management, testing, and monitoring capabilities.

For technical support or development questions, refer to the audit trail documentation and the comprehensive test suite provided with this implementation.

---

**Last Updated**: 2025-08-31  
**A2A Protocol Version**: 0.2.9  
**A2A SDK Version**: 0.3.3  
**Python Version**: 3.13.7  
**Claude Model**: claude-3-5-sonnet-20241022