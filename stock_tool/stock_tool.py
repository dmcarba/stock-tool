"""Main entry point for MCP server and FastAPI app."""

import threading
from .app_server import start_api_server
from .mcp_server import start_mcp_server

def main():
    """Main function to start both FastAPI and MCP server."""
    print("Starting Stock Tool services...")
        
    # Start FastAPI in a separate thread
    api_thread = threading.Thread(target=start_api_server)
    api_thread.daemon = True
    api_thread.start()
    
    # Start MCP server in main thread
    start_mcp_server()

if __name__ == "__main__":
    main()