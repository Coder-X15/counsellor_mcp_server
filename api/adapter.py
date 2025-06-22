from fastmcp import Client, FastMCP
from flask import Flask, request

# our aim is to provide a Flask-based API that can be used to interact with the FastMCP server

def build_app(mcp: FastMCP) -> Flask:
    app = Flask(__name__)

    @app.route("/tools", methods=["POST", "GET"])
    def get_tools():
        client = Client(mcp)
        tools = client.list_tools()
        return tools

    @app.route("/tools/<tool_name>", methods=["POST"])
    def run_tool(tool_name: str):
        client = Client(mcp)
        tool = client.get_tool(tool_name)
        if tool:
            return client.call_tool(tool_name, arguments=request.get_json())
        return "Tool not found", 404

    return app