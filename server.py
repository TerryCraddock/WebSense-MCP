#!/usr/bin/env python3
"""
WebMCP Server - A FastMCP-based Model Context Protocol server
Provides web search and other AI tools functionality
"""

import asyncio
import json
import re
from typing import Any, Dict, List

import aiohttp
from bs4 import BeautifulSoup

from mcp.server.fastmcp import FastMCP


# Create FastMCP server instance
mcp = FastMCP("WebMCP")


async def fetch_page_content(session: aiohttp.ClientSession, url: str, max_length: int = 2000) -> str:
    """Fetch and extract main content from a webpage"""
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return f"HTTP {response.status}"

            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                return "Non-HTML content"

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Try to find main content
            main_content = (
                soup.find('main') or
                soup.find('article') or
                soup.find('div', class_=re.compile(r'content|main|article')) or
                soup.body
            )

            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
            else:
                text = soup.get_text(separator=' ', strip=True)

            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()

            # Limit length
            if len(text) > max_length:
                text = text[:max_length] + "..."

            return text

    except Exception as e:
        return f"Content extraction failed: {str(e)}"


@mcp.tool()
async def web_search(
    query: str,
    limit: int = 5,
    include_content: bool = True
) -> Dict[str, Any]:
    """
    Search the web for information using DuckDuckGo

    Args:
        query: Search query string
        limit: Maximum number of results to return
        include_content: Whether to include page content in results

    Returns:
        Dictionary containing search results with metadata
    """

    # Create HTTP session for this request
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    ) as session:

        # Use DuckDuckGo for search (no API key required)
        search_url = "https://html.duckduckgo.com/html/"
        params = {
            'q': query,
            'kl': 'us-en'
        }

        try:
            async with session.get(search_url, params=params) as response:
                if response.status != 200:
                    return {"error": f"Search failed with status {response.status}"}

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                results = []
                result_divs = soup.find_all('div', class_='result')

                for i, result_div in enumerate(result_divs[:limit]):
                    if i >= limit:
                        break

                    # Extract title and URL
                    title_tag = result_div.find('a', class_='result__a')
                    snippet_tag = result_div.find('a', class_='result__snippet')

                    if not title_tag:
                        continue

                    title = title_tag.get_text(strip=True)
                    url = title_tag.get('href', '')

                    # Clean DuckDuckGo redirect URLs
                    if url.startswith('/l/?uddg='):
                        import urllib.parse
                        url = urllib.parse.unquote(url.split('uddg=')[1].split('&')[0])

                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

                    result_item = {
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    }

                    # Optionally fetch page content
                    if include_content and url:
                        try:
                            content = await fetch_page_content(session, url)
                            result_item["content"] = content
                        except Exception as e:
                            result_item["content"] = f"Content fetch failed: {str(e)}"

                    results.append(result_item)

                return {
                    "query": query,
                    "results_count": len(results),
                    "results": results
                }

        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}


@mcp.tool()
async def url_info(url: str) -> Dict[str, Any]:
    """
    Get information about a specific URL

    Args:
        url: URL to analyze

    Returns:
        Dictionary with URL metadata and content summary
    """

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    ) as session:

        try:
            async with session.head(url, allow_redirects=True) as response:
                headers = dict(response.headers)
                status = response.status
                final_url = str(response.url)

            content_info = {
                "url": final_url,
                "status_code": status,
                "content_type": headers.get('content-type', 'unknown'),
                "content_length": headers.get('content-length', 'unknown'),
                "server": headers.get('server', 'unknown'),
                "last_modified": headers.get('last-modified', 'unknown')
            }

            # Get content preview if it's HTML
            if 'text/html' in content_info["content_type"].lower():
                content = await fetch_page_content(session, final_url, max_length=500)
                content_info["content_preview"] = content

            return content_info

        except Exception as e:
            return {"error": f"URL analysis failed: {str(e)}"}


@mcp.resource("web://search/{query}")
async def search_resource(query: str) -> str:
    """
    Provide search results as a resource

    Args:
        query: Search query

    Returns:
        Formatted search results as text
    """
    return f"Search results for: {query}\n\nNote: Use the web_search tool for actual search functionality."


@mcp.prompt()
async def search_prompt(topic: str) -> str:
    """
    Create a search and analysis prompt

    Args:
        topic: Topic to search and analyze

    Returns:
        Formatted prompt for analysis
    """
    return f"""
Please search for information about "{topic}" and provide a comprehensive analysis.

Use the web_search tool to gather current information, then:
1. Summarize the key findings
2. Identify important trends or developments
3. Provide relevant context and implications
4. Suggest additional areas for investigation

Focus on recent and authoritative sources to ensure accuracy.
"""


if __name__ == "__main__":
    mcp.run()