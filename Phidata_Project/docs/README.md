# Phidata Project

A multi-agent AI system built with Phidata framework, featuring intelligent agents with various capabilities including web search, financial analysis, and conversational assistance.

## 🎯 Project Overview

This project demonstrates the implementation of AI agents using the Phidata framework, leveraging OpenAI's GPT models for intelligent conversations and task execution. The system is designed to be modular, scalable, and easy to extend with new agent capabilities.

## 🏗️ Project Structure

```
Phidata_Project/
├── docs/                          # Project documentation
│   └── README.md                   # This file
├── src/                           # Source code directory
│   ├── .env                       # Environment variables (git-ignored)
│   ├── basic.py                   # Basic agent implementation
│   └── phidata_multi_agents.py    # Multi-agent system (in development)
├── requirements.txt               # Python dependencies
└── .gitignore                    # Git ignore rules
```

## 🚀 Core Functionality

### **Basic Agent (`src/basic.py`)**
- **Agent Name**: Jarvis
- **Model**: GPT-4o (OpenAI)
- **Features**:
  - Conversational AI assistant
  - Markdown formatting support
  - Debug mode for detailed logging
  - Environment-based API key management
  - Interactive command-line interface

### **Multi-Agent System (`src/phidata_multi_agents.py`)**
- **Status**: In development
- **Purpose**: Extended multi-agent capabilities
- **Planned Features**:
  - Specialized agents for different tasks
  - Agent coordination and communication
  - Advanced tool integrations

## 🛠️ Technology Stack

### **Core Framework**
- **Phidata**: Agent orchestration and management
- **OpenAI**: GPT-4o language model
- **Python 3.10+**: Runtime environment

### **Data & Search**
- **DuckDuckGo Search**: Web search capabilities
- **YFinance**: Financial data integration
- **Newspaper4k**: News article extraction
- **LanceDB**: Vector database for embeddings
- **SQLAlchemy**: Database ORM

### **Development Tools**
- **Python-dotenv**: Environment variable management
- **Debug Mode**: Detailed logging and tracing

## 📋 Dependencies

```txt
phidata              # Core agent framework
openai               # OpenAI API integration
duckduckgo-search    # Web search functionality
yfinance            # Financial market data
newspaper4k         # News content extraction
python-dotenv       # Environment configuration
lancedb             # Vector database
sqlalchemy          # Database ORM
```

## 🔧 Setup & Installation

### **Prerequisites**
- Python 3.10 or higher
- OpenAI API key
- Git for version control

### **1. Clone Repository**
```bash
git clone <repository-url>
cd Phidata_Project
```

### **2. Create Virtual Environment**
```bash
# Create virtual environment
python -m venv .myenv_py_3_10

# Activate (Windows)
.myenv_py_3_10\Scripts\activate

# Activate (Linux/Mac)
source .myenv_py_3_10/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
```bash
# Create .env file in src/ directory
cd src
cp .env.example .env  # if template exists
# or create manually
```

**Environment Variables:**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎮 Usage

### **Run Basic Agent**
```bash
cd src
python basic.py
```

**Example Interaction:**
```
Hello, I am Jarvis. How can I help you?
> What's the weather like today?
[Jarvis responds with weather information]
```

### **Run Multi-Agent System**
```bash
cd src
python phidata_multi_agents.py
```
*(Note: Currently in development)*

## 🔍 Features & Capabilities

### **Current Features**
- ✅ **Conversational AI**: Natural language interactions
- ✅ **Markdown Support**: Formatted responses
- ✅ **Debug Mode**: Detailed logging for development
- ✅ **Environment Config**: Secure API key management
- ✅ **Modular Design**: Easy to extend and modify

### **Planned Features**
- 🔄 **Multi-Agent Coordination**: Multiple specialized agents
- 🔄 **Web Search Integration**: Real-time information retrieval
- 🔄 **Financial Analysis**: Stock market data and predictions
- 🔄 **News Processing**: Article summarization and analysis
- 🔄 **Vector Database**: Knowledge base and memory
- 🔄 **API Endpoints**: RESTful service integration

## 🧪 Development

### **Code Structure**
```python
# Basic agent creation
def create_basic_agent():
    agent = Agent(
        name="Jarvis",
        model=OpenAIChat(id="gpt-4o"),
        description="Helpful assistant",
        instructions=["Be concise and helpful"],
        markdown=True,
        debug=True
    )
    return agent
```

### **Best Practices**
- Use environment variables for API keys
- Enable debug mode during development
- Follow modular design patterns
- Implement proper error handling
- Document agent capabilities clearly

## 🔧 Configuration

### **Agent Settings**
- **Model**: GPT-4o (configurable)
- **Temperature**: Default OpenAI settings
- **Max Tokens**: Default OpenAI settings
- **Response Format**: Markdown enabled
- **Debug Mode**: Toggle for development/production

### **Environment Variables**
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API access token | ✅ Yes |

## 🚨 Troubleshooting

### **Common Issues**

#### **API Key Not Found**
```
Error: OPENAI_API_KEY not found
```
**Solution**: Ensure `.env` file exists in `src/` directory with valid API key

#### **Module Import Errors**
```
ModuleNotFoundError: No module named 'phi'
```
**Solution**: Activate virtual environment and install requirements

#### **Agent Not Responding**
```
Agent timeout or no response
```
**Solution**: Check network connection and API key validity

### **Debug Mode**
Enable detailed logging by setting `debug=True` in agent configuration.

## 📈 Roadmap

### **Phase 1: Foundation** ✅
- [x] Basic agent implementation
- [x] Environment configuration
- [x] Documentation setup

### **Phase 2: Multi-Agent System** 🔄
- [ ] Multi-agent coordination
- [ ] Tool integrations (search, finance, news)
- [ ] Agent communication protocols

### **Phase 3: Advanced Features** 📋
- [ ] Vector database integration
- [ ] API endpoints
- [ ] Web interface
- [ ] Performance optimization

### **Phase 4: Production** 📋
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Security hardening

## 🤝 Contributing

### **Development Workflow**
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

### **Code Style**
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Include type hints where appropriate

## 📞 Support

For questions, issues, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Create GitHub issue for bugs
4. Start discussion for feature requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: 2026-03-01  
**Version**: 1.0.0  
**Framework**: Phidata + OpenAI GPT-4o
