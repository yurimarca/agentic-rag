# Agentic RAG

An intelligent Retrieval-Augmented Generation (RAG) system built with [LangGraph](https://github.com/langgraph-dev/langgraph) that combines document retrieval with web search for comprehensive question answering.

## ✨ Features

- **Smart Document Retrieval**: Uses ChromaDB vector store for efficient similarity search
- **Intelligent Document Grading**: Evaluates document relevance before generation
- **Fallback Web Search**: Automatically searches the web when local documents are insufficient
- **LangGraph Workflow**: Implements a robust state-based graph workflow
- **OpenAI Integration**: Leverages OpenAI models for both grading and generation
- **Comprehensive Testing**: Includes unit tests for core functionality

## 🏗️ Architecture

![Graph Workflow](graph.png)

The system implements a sophisticated workflow with four main components:

### 🔍 Retrieve Node
- **Location**: `src/graph/nodes/retrieve.py`
- **Function**: Queries ChromaDB vector store using OpenAI embeddings
- **Input**: User question from graph state
- **Output**: Relevant document chunks

### 📊 Grade Documents Node
- **Location**: `src/graph/nodes/grade_documents.py`
- **Function**: Evaluates document relevance using LLM-based grading
- **Chain**: Uses `retrieval_grader` chain (`src/graph/chains/retrieval_grader.py`)
- **Output**: Binary relevance scores for each document

### 🌐 Web Search Node
- **Location**: `src/graph/nodes/web_search.py`
- **Function**: Performs web search using Tavily API when documents are insufficient
- **Trigger**: Activated when retrieved documents are deemed irrelevant
- **Integration**: Seamlessly adds web results to document pool

### 🤖 Generate Node
- **Location**: `src/graph/nodes/generate.py`
- **Function**: Generates comprehensive answers using retrieved and/or web-sourced content
- **Chain**: Uses `generation_chain` (`src/graph/chains/generation.py`)
- **Model**: OpenAI ChatGPT with specialized RAG prompting

## 🔄 Workflow Logic

1. **Start** → `RETRIEVE` node queries vector store
2. **Grade** → `GRADE_DOCUMENTS` evaluates document relevance
3. **Decision Point**:
   - **Sufficient documents** → Proceed to `GENERATE`
   - **Insufficient documents** → Route to `WEBSEARCH` then `GENERATE`
4. **End** → Return generated answer

The decision logic is handled by the `decide_to_generate` function in `src/graph/graph.py`.

## 📊 State Management

The workflow state is managed by `GraphState` class (`src/graph/state.py`) which tracks:
- User question
- Retrieved documents
- Web search results
- Generated answer
- Grading decisions

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Tavily API key (for web search)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd agentic-rag/agentic_rag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the `src/` directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   
   # Optional: LangSmith tracing
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   LANGCHAIN_API_KEY=your_langsmith_key
   LANGCHAIN_PROJECT=agentic-rag
   ```

### Data Ingestion

**Populate the vector store with documents:**
```bash
cd src
python ingestion.py
```

This script:
- Loads content from predefined URLs (Lilian Weng's blog posts on AI agents)
- Splits documents into 250-token chunks
- Creates ChromaDB vector store with OpenAI embeddings
- Persists data in `./.chroma` directory

## 🚀 Usage

### Basic Usage
```bash
cd src
python main.py
```

This runs the default question: "What is agent memory?"

### Custom Questions
Modify `src/main.py` to ask different questions:
```python
from graph.graph import app

result = app.invoke({"question": "Your custom question here"})
print(result)
```

### Programmatic Usage
```python
from dotenv import load_dotenv
load_dotenv()

from graph.graph import app

# Ask a question
response = app.invoke({
    "question": "What are the different types of agent memory?"
})

print("Answer:", response["generation"])
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
cd src
pytest graph/chains/tests/test_chains.py -v
```

Tests cover:
- Retrieval grader functionality
- Generation chain behavior
- Chain integration with mocked dependencies

## 📁 Project Structure

```
agentic_rag/
├── src/
│   ├── graph/
│   │   ├── chains/
│   │   │   ├── generation.py      # Answer generation chain
│   │   │   ├── retrieval_grader.py # Document relevance grader
│   │   │   └── tests/
│   │   │       └── test_chains.py  # Unit tests
│   │   ├── nodes/
│   │   │   ├── generate.py         # Generation node
│   │   │   ├── grade_documents.py  # Document grading node  
│   │   │   ├── retrieve.py         # Retrieval node
│   │   │   └── web_search.py       # Web search node
│   │   ├── consts.py              # Node name constants
│   │   ├── graph.py               # Main workflow definition
│   │   └── state.py               # State management
│   ├── ingestion.py               # Data ingestion script
│   ├── main.py                    # Entry point
│   └── .env                       # Environment variables
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── graph.png                     # Workflow visualization
```

## 🔧 Configuration

### Document Sources
Currently configured to ingest from Lilian Weng's AI blog posts. Modify URLs in `src/ingestion.py`:
```python
urls = [
    "https://your-domain.com/article1",
    "https://your-domain.com/article2",
    # Add more URLs as needed
]
```

### Chunk Size & Overlap
Adjust text splitting parameters in `src/ingestion.py`:
```python
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250,    # Tokens per chunk
    chunk_overlap=0    # Overlap between chunks
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langgraph-dev/langgraph) by LangChain
- Utilizes [ChromaDB](https://www.trychroma.com/) for vector storage
- Web search powered by [Tavily](https://tavily.com/)
- Inspired by research from [Lilian Weng's blog](https://lilianweng.github.io/)