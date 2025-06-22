from fastmcp import Client, FastMCP
from flask import Flask, request

# our aim is to provide a Flask-based API that can be used to interact with the FastMCP server

def build_app(mcp: FastMCP) -> Flask:
    app = Flask(f"{mcp.name()}-api")

    @app.route("/tools", methods=["POST", "GET"])
    async def get_tools():
        async with Client(mcp) as client:
            tools = await client.list_tools()
            return tools
    
    @app.route("/tools/<tool_name>", methods=["POST"])
    async def run_tool(tool_name: str):
        async with Client(mcp) as client:
            tool = await client.get_tool(tool_name)
            if tool:
                return await client.call_tool(tool_name, arguments = request.get_json())
            
            return "Tool not found", 404
    
    return app