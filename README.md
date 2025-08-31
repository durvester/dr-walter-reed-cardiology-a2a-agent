# Dr. Walter Reed's Interventional Cardiology A2A Agent

A specialized healthcare AI agent built on the Google A2A (Agent-to-Agent) protocol for interventional cardiology practice coordination and medical consultation.

## 🏥 **Overview**

This agent provides professional medical expertise and care coordination for:
- **Interventional Procedures**: Angiography, angioplasty, stenting, complex coronary interventions  
- **Heart Failure Management**: Optimization therapy, monitoring protocols, advanced treatments
- **Ischemic Heart Disease**: Acute coronary syndromes, chronic CAD, secondary prevention
- **Stroke Prevention**: Cardiovascular risk assessment, anticoagulation management
- **Cardiac Diagnostics**: Stress testing, ECG, echocardiography, catheterization

## 🚀 **Features**

- ✅ **Full A2A Protocol Compliance** - Built with official Google A2A SDK v0.3.3
- ✅ **Claude AI Integration** - Professional medical responses via Anthropic Claude
- ✅ **Streaming Support** - Real-time responses via Server-Sent Events
- ✅ **Security First** - Input validation, prompt injection protection
- ✅ **Zero Hardcoded Values** - Complete environment-based configuration
- ✅ **Professional Communication** - Healthcare provider-focused terminology

## 🛠️ **Quick Start**

### Prerequisites
- Python 3.10+ 
- Anthropic Claude API key
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cardiology-agent
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Run the agent**
   ```bash
   python __main__.py
   ```

The agent will start on `http://localhost:9999` with the agent card available at `http://localhost:9999/.well-known/agent-card.json`.

## 🔧 **Configuration**

All configuration is handled via environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *Required* | Your Claude API key |
| `PORT` | `9999` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `AGENT_NAME` | Dr. Walter Reed's... | Agent identity |
| `CLAUDE_MODEL` | claude-3-5-sonnet-20241022 | Claude model |
| `MAX_MESSAGE_LENGTH` | `10000` | Input length limit |

## 🧪 **Testing**

### Manual Testing
```bash
# Test agent card
curl http://localhost:9999/.well-known/agent-card.json | jq '.'

# Test basic communication
curl -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "message/send",
    "params": {
      "message": {
        "messageId": "test-msg",
        "role": "user",
        "parts": [{"kind": "text", "text": "What angioplasty procedures do you perform?"}]
      }
    }
  }'
```

### Test Streaming
```bash
curl -N -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "stream-test",
    "method": "message/stream",
    "params": {
      "message": {
        "messageId": "stream-msg",
        "role": "user",
        "parts": [{"kind": "text", "text": "Explain the complete angioplasty workflow."}]
      }
    }
  }'
```

### Using A2A Inspector
For comprehensive A2A protocol validation, use the [A2A Inspector](https://github.com/a2aproject/a2a-inspector):

1. Set up the inspector per its documentation
2. Connect to your agent at `http://localhost:9999`
3. Test all A2A methods and compliance

## 📋 **A2A Protocol Support**

### Core Methods
- ✅ `message/send` - Send message and get response
- ✅ `message/stream` - Send message with streaming response  
- ✅ `tasks/get` - Retrieve task information
- ✅ `tasks/cancel` - Cancel active tasks
- ✅ `tasks/resubscribe` - Resume streaming

### Agent Card
The agent publishes a complete A2A v0.3.0 compliant agent card with:
- **5 specialized skills** for interventional cardiology
- **Streaming capabilities** enabled
- **Professional metadata** and examples

## 🔒 **Security**

- **Input Validation**: Message length limits and content filtering
- **Prompt Injection Protection**: Detection of malicious instructions
- **Sensitive Data Filtering**: Credit cards, SSN, passwords blocked
- **Professional Boundaries**: Medical advice disclaimers and referral requirements

## 🏗️ **Architecture**

```
┌─────────────────────┐    A2A Protocol    ┌──────────────────────┐
│   A2A Clients       │ ◄─────────────────► │  Cardiology Agent    │
│ (Inspector, Other    │   JSON-RPC 2.0     │                      │
│  Agents)            │   + SSE Streaming   │  ┌─────────────────┐ │
└─────────────────────┘                     │  │ AgentExecutor   │ │
                                            │  │ (Medical Logic) │ │
                                            │  └─────────────────┘ │
                                            │          │           │
                                            │          ▼           │
                                            │  ┌─────────────────┐ │
                                            │  │ Claude API      │ │
                                            │  │ Integration     │ │
                                            │  └─────────────────┘ │
                                            └──────────────────────┘
```

## 📁 **Project Structure**

```
cardiology-agent/
├── __main__.py           # Application entry point and A2A setup
├── agent_executor.py     # Medical domain logic and Claude integration  
├── config.py            # Environment-based configuration management
├── test_client.py       # A2A protocol testing client
├── requirements.txt     # Python dependencies
├── .env.example         # Environment configuration template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── audit-trail.md      # Implementation audit trail
├── claude.md          # Complete technical documentation
└── venv/              # Python virtual environment (not in repo)
```

## 🩺 **Medical Specializations**

### Interventional Procedures
- Cardiac catheterization (diagnostic and therapeutic)
- Percutaneous coronary intervention (PCI)
- Balloon angioplasty and stent placement
- Complex lesion management

### Heart Failure Management
- Optimization therapy protocols
- Monitoring and assessment programs  
- Advanced treatment modalities
- Multidisciplinary care coordination

### Diagnostic Services  
- Exercise and pharmacological stress testing
- 12-lead electrocardiography interpretation
- 2D echocardiography with Doppler
- Cardiac catheterization procedures

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- Built with the [Google A2A SDK](https://github.com/a2aproject/a2a-sdk-python)
- Powered by [Anthropic Claude](https://www.anthropic.com/) for medical expertise
- Validated with [A2A Inspector](https://github.com/a2aproject/a2a-inspector)

## 📞 **Support**

For technical support or questions about this implementation:
- Review the comprehensive technical documentation in `claude.md`
- Check the implementation audit trail in `audit-trail.md`
- Use the A2A Inspector for protocol validation
- Submit issues via GitHub

---

**⚠️ Medical Disclaimer**: This agent is for healthcare provider coordination and informational purposes only. It does not provide direct patient medical advice. All medical decisions should be made by qualified healthcare professionals based on individual patient evaluation.