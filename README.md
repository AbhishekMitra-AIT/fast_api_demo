# Note Agent 📝

An AI-powered note-taking assistant that can read and write text files using natural language commands. Built with FastAPI, LangChain, and your choice of LLM provider.

## Features

- 🤖 Natural language interface for file operations
- 📄 Read and write text files
- 🌐 Web-based UI
- 🔌 REST API endpoint
- 🎯 Multiple LLM options (OpenAI, Anthropic Claude, Ollama)

## Prerequisites

- Python 3.9+
- One of the following:
  - OpenAI API key (paid)
  - Anthropic API key (paid)
  - Ollama installed locally (free)

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd fast_api_demo
```

2. **Create a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up your LLM provider**

### Option A: Using Ollama (Free, Local)

1. Install Ollama from [ollama.com](https://ollama.com)
2. Pull a model:
```bash
ollama pull llama3.2
```
3. Start Ollama:
```bash
ollama serve
```
4. Update `agent.py` to use Ollama (see configuration section)

### Option B: Using OpenAI

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```
3. Update `requirements.txt`:
```
langchain-openai
```

### Option C: Using Anthropic Claude

1. Get an API key from [console.anthropic.com](https://console.anthropic.com)
2. Create a `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
```
3. Update `requirements.txt`:
```
langchain-anthropic
```

## Project Structure

```
fast_api_demo/
├── agent.py           # AI agent logic with LangChain
├── main.py            # FastAPI application
├── templates/
│   └── index.html     # Web UI
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
└── README.md         # This file
```

## Configuration

### Using Different LLM Providers

Edit `agent.py` and change the import and initialization:

**For Ollama:**
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2", 
    temperature=0,
    base_url="http://localhost:11434"
)
```

**For OpenAI:**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
```

**For Anthropic:**
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0
)
```

## Usage

### Running Locally

1. **Start the server**
```bash
python main.py
```

2. **Access the web interface**
Open your browser and go to: `http://localhost:8000`

3. **Try some commands**
- "Write 'Hello World' to test.txt"
- "Read the contents of test.txt"
- "Create a shopping list in shopping.txt with milk, eggs, and bread"

### Using the API

**Endpoint:** `POST /agent`

**Request:**
```json
{
  "prompt": "Write 'Hello World' to test.txt"
}
```

**Response:**
```json
{
  "response": "Successfully wrote 11 characters to 'test.txt'."
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write Hello World to test.txt"}'
```

## Deployment

### Deploy to Railway

1. **Update `requirements.txt` for cloud deployment:**
```
fastapi
uvicorn
jinja2
langchain
langchain-anthropic  # or langchain-openai
langgraph
python-dotenv
requests
```

2. **Create `railway.toml`:**
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

3. **Update `main.py` to use environment PORT:**
```python
import os
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

4. **Deploy:**
- Push to GitHub
- Connect repository to Railway
- Add environment variables (ANTHROPIC_API_KEY or OPENAI_API_KEY)
- Deploy!

### Deploy to Vercel

1. **Create `vercel.json`:**
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. **Update `main.py`** to remove the `uvicorn.run()` line at the bottom

3. **Deploy:**
```bash
vercel
```

**Note:** File operations may be limited on Vercel due to read-only filesystem. Consider using cloud storage (S3, Google Cloud Storage) for production.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | If using Claude |
| `OLLAMA_BASE_URL` | Ollama server URL | If using remote Ollama |
| `PORT` | Server port (for deployment) | No (default: 8000) |

## Troubleshooting

### Ollama Connection Issues

**Error:** `No connection could be made`

**Solution:**
1. Check if Ollama is running:
```bash
Get-Process ollama  # Windows
ps aux | grep ollama  # Linux/Mac
```
2. Start Ollama:
```bash
ollama serve
```
3. Verify in browser: `http://localhost:11434`

### OpenAI Quota Exceeded

**Error:** `insufficient_quota`

**Solution:** Add credits at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)

### Model Not Found

**Error:** `model not found`

**Solution:**
- For Ollama: `ollama pull llama3.2`
- For OpenAI: Use `gpt-4o-mini` or `gpt-3.5-turbo`
- For Anthropic: Use `claude-3-5-sonnet-20241022`

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the Agent Directly

```bash
python agent.py
```

## Cost Estimates

| Provider | Cost | Speed | Quality |
|----------|------|-------|---------|
| **Ollama (Local)** | Free | Medium | Good |
| **OpenAI GPT-4o-mini** | ~$0.15/1M tokens | Fast | Excellent |
| **Anthropic Claude Sonnet** | ~$3/1M tokens | Fast | Excellent |

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Check the official documentation:
   - [LangChain Docs](https://python.langchain.com)
   - [FastAPI Docs](https://fastapi.tiangolo.com)
   - [Ollama Docs](https://ollama.com/docs)

## Acknowledgments

- Built with [LangChain](https://python.langchain.com)
- Powered by [FastAPI](https://fastapi.tiangolo.com)
- UI inspired by modern web design principles

---

Made with ❤️ using AI agents