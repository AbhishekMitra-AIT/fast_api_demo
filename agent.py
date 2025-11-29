from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import requests

load_dotenv()

# Test Ollama connection
try:
    response = requests.get("http://localhost:11434")
    print(f"✓ Ollama is running: {response.text}")
except Exception as e:
    print(f"✗ Cannot connect to Ollama: {e}")
    print("Make sure Ollama is running with 'ollama serve'")
    exit(1)

@tool
def read_note(filepath: str) -> str:
    """Read the contents of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Contents of '{filepath}':\n{content}"
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_note(filepath: str, content: str) -> str:
    """Write content to a text file. This will overwrite the file if it exists."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{filepath}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"
    
    
TOOLS = [read_note, write_note]

# Using Ollama with a local model (FREE!)
try:
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0,
        base_url="http://localhost:11434"
    )
    print("✓ LLM initialized successfully")
except Exception as e:
    print(f"✗ Error initializing LLM: {e}")
    exit(1)

# Updated to use create_agent from langchain.agents (v1.0)
agent = create_agent(llm, TOOLS)


def run_agent(user_input: str) -> str:
    """Run the agent with a user query and return the response."""
    try:
        result = agent.invoke({
            "messages": [
                ("system", "You are a helpful note-taking assistant. "
                          "You can read and write text files to help users manage their notes. "
                          "Be concise and helpful."),
                ("user", user_input)
            ]
        })
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print(run_agent("hello how are you"))