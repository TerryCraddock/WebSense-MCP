#!/usr/bin/env python3
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_web_search(query, limit=5, include_content=True):
    """Test the web search using our WebMCP server"""

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "web_search",
                arguments={
                    "query": query,
                    "limit": limit,
                    "include_content": include_content
                }
            )

            return result

async def test_url_info(url):
    """Test the URL info tool using our WebMCP server"""

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "url_info",
                arguments={
                    "url": url
                }
            )

            return result

async def list_available_tools():
    """List all available tools from our WebMCP server"""

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools_result = await session.list_tools()

            # List resources
            resources_result = await session.list_resources()

            # List prompts
            prompts_result = await session.list_prompts()

            return {
                "tools": tools_result,
                "resources": resources_result,
                "prompts": prompts_result
            }

if __name__ == "__main__":
    print("=== WebMCP Server Test ===\n")

    # Test 1: List available tools
    print("1. Listing available tools, resources, and prompts...")
    try:
        server_info = asyncio.run(list_available_tools())

        print("\nAvailable Tools:")
        for tool in server_info["tools"].tools:
            print(f"  - {tool.name}: {tool.description}")

        print("\nAvailable Resources:")
        for resource in server_info["resources"].resources:
            print(f"  - {resource.uri}: {resource.name}")

        print("\nAvailable Prompts:")
        for prompt in server_info["prompts"].prompts:
            print(f"  - {prompt.name}: {prompt.description}")

    except Exception as e:
        print(f"Error listing server info: {e}")

    print("\n" + "="*50 + "\n")

    # Test 2: Web search
    print("2. Testing web search...")
    try:
        search_result = asyncio.run(test_web_search("advancements in robotics", limit=3, include_content=False))
        print("\n=== SEARCH RESULTS ===")

        # Extract the actual content from the CallToolResult object
        for item in search_result.content:
            if hasattr(item, 'text'):
                print(item.text)
            else:
                print(json.dumps(item.model_dump(), indent=2))

    except Exception as e:
        print(f"Error during search: {e}")

    print("\n" + "="*50 + "\n")

    # Test 3: URL info
    print("3. Testing URL info...")
    try:
        url_result = asyncio.run(test_url_info("https://www.python.org"))
        print("\n=== URL INFO RESULTS ===")

        # Extract the actual content from the CallToolResult object
        for item in url_result.content:
            if hasattr(item, 'text'):
                print(item.text)
            else:
                print(json.dumps(item.model_dump(), indent=2))

    except Exception as e:
        print(f"Error during URL info: {e}")

    print("\n=== Test Complete ===")