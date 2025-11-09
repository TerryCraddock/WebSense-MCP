# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL INSTRUCTIONS - MCP TOOLS USAGE

**FORCED USAGE: ALWAYS use MCP tools for ANY complex task. No exceptions.**

### 1. Sequential Thinking Tool - 🚨 MANDATORY FOR EVERYTHING COMPLEX
**ABSOLUTE REQUIREMENT**: For ANY task that involves more than 3 steps, any decision-making, debugging, planning, or problem-solving, you MUST:
- Tool: `sequentialthinking_sequentialthinking`
- Trigger: **AUTOMATICALLY** before ANY complex work
- Use cases: Planning, debugging, architecture, API design, code refactoring, error analysis
- Process: Complete the thinking process BEFORE starting implementation
- NO EXCUSES: If you're working on anything complex, use this tool FIRST

### 2. Image Analysis Tool
- Tool: `zai-mcp-server_analyze_image`
- Use for: Screenshots, diagrams, mockups, visual content analysis
- Supports: Local files and remote URLs

### 3. Video Analysis Tool
- Tool: `zai-mcp-server_analyze_video`
- Use for: Video content, tutorials, demonstrations
- Supports: MP4, MOV, M4V formats

### 4. Web Search Tool
- Tool: `web-search-prime_webSearchPrime`
- Use for: Current information, documentation, recent resources
- Process: Use before built-in web search when available

### 5. Library Documentation Tool
- Tool: `context7_get-library-docs` (with `resolve-library-id` first)
- Use for: Programming library documentation
- Process: Resolve library ID first, then get documentation

## 🚨 ENFORCED MCP WORKFLOW

**Step 1**: **ALWAYS** start with sequential thinking for complex tasks
**Step 2**: Use additional MCP tools as needed for research and analysis
**Step 3**: Complete your thinking process BEFORE implementing
**Step 4**: Implement based on your sequential thinking results

### Examples of tasks that REQUIRE sequential thinking:
- ✅ Any API development or changes
- ✅ Database schema design or changes
- ✅ Error debugging and troubleshooting
- ✅ System architecture decisions
- ✅ Multi-step implementations
- ✅ Code refactoring
- ✅ Performance optimization
- ✅ Security considerations
- ✅ Any task involving multiple files/components

### When NOT to use sequential thinking:
- ❌ Simple file creation (basic scaffolding)
- ❌ Single line edits
- ❌ Reading existing files
- ❌ Simple environment checks
- ❌ Basic CLI commands

**VIOLATION**: Not using sequential thinking for complex tasks is a failure to follow instructions.

## 🚨 GIT WORKFLOW REQUIREMENTS

### Git Commands - ABSOLUTE RULES
**NEVER add descriptions to Bash tool calls for git operations**

**CORRECT Git Usage:**
```bash
git add .
git commit -m "Your commit message here"
git push
```

**FORBIDDEN Git Usage:**
- ❌ `description="Commit files"` parameter
- ❌ `description="Push to remote"` parameter
- ❌ Any description parameter in git commands
- ❌ Any personal notes or commentary in git commands

### Git Commit Messages
- Keep commit messages clear and descriptive
- Use conventional commit format when appropriate
- NO attribution lines or tool references
- Clean, professional commit history

**VIOLATION**: Adding descriptions to git commands is NOT acceptable.

## Project Overview

**WebMCP** is a Python-based Model Context Protocol (MCP) server project designed to create AI tools and integrations. The project transforms existing functionality into a fully working MCP server suitable for sharing on GitHub.

### Architecture

- **FastMCP Framework**: Uses decorator-based pattern for tool, resource, and prompt creation
- **Python MCP SDK**: Built on the `mcp` Python library (v1.21.0+)
- **Standard I/O Communication**: Communicates via stdio for Claude Desktop integration
- **Modular Design**: Separate tools for different capabilities (web search, Ollama integration, etc.)

### Key Components

- `mcpTest.py`: MCP client test script for external server integration
- Future server files: FastMCP-based server implementation
- `.claude/`: Claude Code configuration with MCP tool permissions

## Development Commands

### Running and Testing
```bash
# Run server in development mode with MCP Inspector
mcp dev server.py

# Direct server execution
python server.py
# or
mcp run server.py

# Test existing MCP client functionality
python mcpTest.py
```

### Claude Desktop Integration
```bash
# Install server for Claude Desktop
mcp install server.py

# Install with custom name
mcp install server.py --name "WebMCP Server"

# Install with environment variables
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
```

### Development Mode with Dependencies
```bash
# Add dependencies during development
mcp dev server.py --with pandas --with numpy

# Mount local code for live updates
mcp dev server.py --with-editable .
```

## MCP Server Development Patterns

### FastMCP Server Structure
```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("WebMCP")

# Define tools
@mcp.tool()
def my_tool(param: str) -> str:
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

### Server Lifespan Management
```python
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class AppContext:
    db_connection: Any

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    # Initialize resources
    conn = await connect_database()
    try:
        yield AppContext(db_connection=conn)
    finally:
        # Cleanup resources
        await conn.close()

mcp = FastMCP("WebMCP", lifespan=app_lifespan)
```

## Development Workflow

1. **Always start complex tasks with sequential thinking tool**
2. **Use MCP tools for research and analysis before coding**
3. **Test with MCP Inspector before Claude Desktop integration**
4. **Follow FastMCP patterns for tool/resource/prompt creation**
5. **Use lifespan management for resource initialization**
6. **Follow git command rules exactly - NO descriptions**

## Integration Points

### Ollama Integration
- Plan for Ollama API tools within MCP server structure
- Use FastMCP tools to expose LLM functionality
- Consider model management and prompt engineering tools

### External MCP Services
- Current `mcpTest.py` shows web search integration pattern
- Consider wrapping external services as MCP tools
- Maintain clean separation between client and server code