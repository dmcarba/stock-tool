# mcp_test.py
import asyncio
from fastmcp.client import Client

async def main():
    try:
        async with Client("http://192.168.1.3:3001/mcp") as client:
            await client.ping()
            tools = await client.list_tools()
            print("Tools:", tools)
    except Exception as e:
        print("Error connecting to MCP server:", e)

asyncio.run(main())