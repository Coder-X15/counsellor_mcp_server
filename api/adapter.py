import asyncio
from fastmcp import Client, FastMCP
from flask import Flask, request, jsonify

# our aim is to provide a Flask-based API that can be used to interact with the FastMCP server

def build_app(mcp: FastMCP) -> Flask:
    app = Flask(__name__)

    @app.route("/tools", methods=["POST", "GET"])
    def get_tools():
        async def list_tools_async():
            async with Client(mcp) as client:
                return await client.list_tools()
        tools = asyncio.run(list_tools_async())
        return jsonify(tools)

    @app.route("/tools/<tool_name>", methods=["POST"])
    def run_tool(tool_name: str):
        async def run_tool_async():
            async with Client(mcp) as client:
                tool = await client.get_tool(tool_name)
                if tool:
                    result = await client.call_tool(tool_name, arguments=request.get_json())
                    return result
                return None
        result = asyncio.run(run_tool_async())
        if result is not None:
            return jsonify(result)
        return "Tool not found", 404

    return app