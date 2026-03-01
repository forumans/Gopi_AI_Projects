# Gopi AI Projects Documentation

## Project Overview

This repository contains a collection of AI-powered applications and utilities developed using modern Python frameworks, LangChain, and various AI/ML technologies.

## Project Structure

```
Gopi_AI_Projects/
├── global_setup/                 # Configuration and documentation
│   ├── requirements.txt          # Python dependencies
│   ├── commands.md             # Useful commands reference
│   └── PROJECT_DOCUMENTATION.md # This file
├── global_util/                # Shared utility functions
│   ├── gopi_util.py          # Core utilities (LLM, embeddings, Chroma DB)
│   └── .env                 # Environment variables (gitignored)
├── global_test_files/          # Test data files
│   ├── HR-Manual.pdf         # HR policy document for RAG demo
│   └── WeatherTable.pdf      # Weather data for table extraction demo
├── My_AI_Projects/            # Main AI applications
│   └── src/                 # Source code for AI projects
├── ResumeScreening/          # Resume processing applications
│   └── src/               # Source code for resume applications
│       ├── app.py           # Resume screening web app
│       └── gopi_resume_processor.py # Resume processing logic
├── Resumes/                  # Resume test data
├── chroma_db/               # Vector database storage
├── hr_policy_chroma_db/       # HR policy vector database
├── .venv/                   # Python virtual environment
├── .gradio/                 # Gradio temporary files
├── debug_path.py            # Path debugging utility
├── setup_paths.py           # Path setup utility
└── pyproject.toml           # Project configuration
```

## Applications

### 1. RAG HR Policies (`My_AI_Projects/src/RAG_HR_Policies.py`)
- **Purpose**: Retrieval-Augmented Generation system for HR policy queries
- **Technology**: LangChain, ChromaDB, Gradio, OpenAI
- **Features**:
  - PDF document processing and chunking
  - Vector storage and retrieval
  - Interactive web interface
  - Question-answering on HR policies

### 2. Finance LangGraph App (`My_AI_Projects/src/finance_langgraph_app.py`)
- **Purpose**: Financial assistant with expense tracking and budget management
- **Technology**: LangGraph, OpenAI
- **Features**:
  - Conversation flow management
  - Expense tracking
  - Budget calculations
  - Financial advice

### 3. LangGraph Test (`My_AI_Projects/src/langgraph1_test.py`)
- **Purpose**: Testing LangGraph capabilities with multiple tools
- **Technology**: LangGraph, various API integrations
- **Features**:
  - Web search integration
  - Python code execution
  - Time zone conversions
  - Tool orchestration

### 4. PDF Table Extraction (`My_AI_Projects/src/pdf_file_tabular_text.py`)
- **Purpose**: Extract tables from PDF documents
- **Technology**: pdfplumber, pandas
- **Features**:
  - Automatic table detection
  - Data frame conversion
  - Multi-page support

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Gopi_AI_Projects
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r global_setup/requirements.txt
   ```

4. **Environment Configuration**
   - Copy `global_util/.env.example` to `global_util/.env`
   - Add your OpenAI API key:
     ```
     GOPI_OPENAI_API_KEY=your_openai_api_key_here
     ```

## Usage

### Running Applications

1. **RAG HR Policies**
   ```bash
   python My_AI_Projects/src/RAG_HR_Policies.py
   ```
   - Access at: http://127.0.0.1:7860
   - Load HR policies and ask questions

2. **Finance Assistant**
   ```bash
   python My_AI_Projects/src/finance_langgraph_app.py
   ```

3. **LangGraph Test**
   ```bash
   python My_AI_Projects/src/langgraph1_test.py
   ```

4. **PDF Table Extraction**
   ```bash
   python My_AI_Projects/src/pdf_file_tabular_text.py
   ```

## Dependencies

### Core Libraries
- **LangChain**: LLM orchestration and chains
- **OpenAI**: GPT models and embeddings
- **ChromaDB**: Vector database for RAG
- **Gradio**: Web interface creation
- **pdfplumber**: PDF processing
- **pandas**: Data manipulation

### AI/ML Libraries
- `langchain-openai`: OpenAI integration
- `langchain-community`: Community integrations
- `langchain-google-genai`: Google AI integration
- `faiss-cpu`: Vector similarity search
- `google.generativeai`: Google AI models

### Document Processing
- `pypdf`: PDF text extraction
- `docx2txt`: Word document processing
- `pdfplumber`: PDF table extraction

### Web & Utilities
- `streamlit`: Alternative web framework
- `gradio`: Interactive interfaces
- `requests`: HTTP requests
- `duckduckgo-search`: Web search
- `ddgs`: DuckDuckGo search

## Configuration

### Environment Variables
- `GOPI_OPENAI_API_KEY`: OpenAI API key (required)

### File Paths
- Test files: `global_test_files/`
- Vector databases: `chroma_db/`, `hr_policy_chroma_db/`
- Utilities: `global_util/gopi_util.py`

## Development Guidelines

### Code Organization
- Shared utilities in `global_util/`
- Application-specific code in respective project folders
- Configuration in `global_setup/`
- Test data in `global_test_files/`

### Best Practices
1. Use relative paths for file references
2. Store sensitive data in environment variables
3. Follow PEP 8 style guidelines
4. Add comprehensive error handling
5. Document functions and classes

### Git Workflow
- Main branch: `main`
- Feature branches: `feature/feature-name`
- Commit format: `type: description`
- Ignore sensitive files via `.gitignore`

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   - Ensure virtual environment is activated
   - Install dependencies: `pip install -r global_setup/requirements.txt`

2. **API Key Errors**
   - Check `global_util/.env` file
   - Verify OpenAI API key is valid

3. **Path Issues**
   - Use relative paths from project root
   - Check file existence in `global_test_files/`

4. **Vector Database Issues**
   - Clear corrupted databases: delete `*_chroma_db/` folders
   - Re-run applications to rebuild databases

### Performance Optimization
- Use appropriate chunk sizes for document processing
- Cache embeddings when possible
- Optimize vector database settings
- Monitor API usage and costs

## Future Enhancements

### Planned Features
- [ ] Multi-modal AI capabilities
- [ ] Advanced RAG with multiple document types
- [ ] Real-time data processing
- [ ] User authentication and sessions
- [ ] Deployment configurations

### Technology Upgrades
- [ ] Migrate to latest LangChain versions
- [ ] Implement async processing
- [ ] Add monitoring and logging
- [ ] Container support (Docker)

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Update documentation
5. Submit pull request

## License

This project is for educational and development purposes. Please ensure compliance with API terms of service.

## Contact

For questions or support, refer to the project documentation or create an issue in the repository.

---

**Last Updated**: February 2026
**Version**: 1.0.0
