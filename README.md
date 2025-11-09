# WebMCP 🌐

A Python-based Model Context Protocol (MCP) server that provides web search and URL analysis tools for AI assistants. Built with FastMCP framework for seamless integration with Claude Desktop and other MCP-compatible AI tools.

## 🚀 Features

- **🔍 Web Search**: DuckDuckGo-powered search with content extraction
- **📊 URL Analysis**: Metadata extraction and content preview
- **⚡ FastMCP Integration**: Decorator-based tool creation
- **🔧 No API Keys Required**: Uses free web search services
- **🛡️ Error Handling**: Graceful error responses and timeouts
- **📝 Type Safety**: Full type hints and validation

## 📋 Requirements

- Python 3.8+
- MCP Python SDK
- FastMCP Framework
- aiohttp & BeautifulSoup4

## 🛠️ Installation

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/yourusername/WebMCP.git
cd WebMCP
pip install -r requirements.txt
```

### 2. Install for Claude Desktop

```bash
# Install server for Claude Desktop
mcp install server.py

# Install with custom name
mcp install server.py --name "WebMCP Server"

# Install with environment variables
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
```

### 3. Development Mode

```bash
# Run with MCP Inspector for testing
mcp dev server.py

# Run with additional dependencies
mcp dev server.py --with pandas --with numpy

# Mount local code for live updates
mcp dev server.py --with-editable .
```

## 🎯 Available Tools

### `web_search`
Search the web using DuckDuckGo with optional content extraction.

**Parameters:**
- `query` (string, required): Search query
- `limit` (integer, optional): Max results (default: 5)
- `include_content` (boolean, optional): Fetch page content (default: true)

**Example:**
```python
result = await session.call_tool(
    "web_search",
    arguments={
        "query": "latest AI developments",
        "limit": 3,
        "include_content": True
    }
)
```

### `url_info`
Get metadata and content preview for any URL.

**Parameters:**
- `url` (string, required): URL to analyze

**Example:**
```python
result = await session.call_tool(
    "url_info",
    arguments={"url": "https://example.com"}
)
```

## 📁 Resources

- `web://search/{query}`: Search results as text resource

## 💬 Prompts

- `search_prompt`: Creates a comprehensive search and analysis prompt

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python mcpTest.py
```

This will:
1. List all available tools, resources, and prompts
2. Test web search functionality
3. Test URL analysis functionality

## 🔧 Development

### Project Structure

```
WebMCP/
├── server.py          # Main FastMCP server
├── mcpTest.py         # Test client
├── requirements.txt   # Python dependencies
├── README.md         # This file
├── .gitignore        # Git ignore rules
└── CLAUDE.md         # Claude Code instructions
```

### FastMCP Patterns

The server follows FastMCP best practices:

```python
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("WebMCP")

# Define tools
@mcp.tool()
async def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

# Define resources
@mcp.resource("data://{id}")
def get_data(id: str) -> str:
    """Get data resource"""
    return f"Data for {id}"

# Define prompts
@mcp.prompt()
def my_prompt(topic: str) -> str:
    """Create prompt"""
    return f"Analyze: {topic}"

if __name__ == "__main__":
    mcp.run()
```

## 🌟 Usage Examples

### Claude Desktop Integration

1. Install the server: `mcp install server.py`
2. Restart Claude Desktop
3. Use web search in conversations:
   - "Search for recent developments in quantum computing"
   - "Analyze this URL: https://example.com"
   - "Find information about renewable energy trends"

### Programmatic Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def search_web():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "web_search",
                arguments={"query": "Python programming", "limit": 5}
            )

            return result

# Run the search
results = asyncio.run(search_web())
```

## 🔒 Security & Privacy

- **No API Keys**: Uses DuckDuckGo (privacy-focused search)
- **Local Processing**: All content extraction happens locally
- **Configurable Timeouts**: Prevents hanging on slow websites
- **Error Handling**: Graceful failures don't crash the server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test: `python mcpTest.py`
4. Commit your changes: `git commit -m "Add feature"`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP framework
- [MCP Python SDK](https://github.com/modelcontextprotocol/servers) - Protocol implementation
- [DuckDuckGo](https://duckduckgo.com/) - Search functionality
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/WebMCP/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/WebMCP/discussions)
- 📧 **Questions**: Open a discussion or issue

---

**WebMCP** - Bringing the power of web search to AI assistants, one MCP tool at a time! 🚀