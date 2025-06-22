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
                tools = await client.list_tools()
                # Convert each Tool object to dict
                return [tool.dict() if hasattr(tool, "dict") else tool.__dict__ for tool in tools]
        tools = asyncio.run(list_tools_async())
        return jsonify(tools)

    @app.route("/tools/<tool_name>", methods=["POST"])
    def run_tool(tool_name: str):
        async def run_tool_async(tool_name: str):
            async with Client(mcp) as client:
                result = await client.call_tool(tool_name, arguments=request.json.get("arguments", {}))
                # Convert result to dict if possible
                if hasattr(result, "dict"):
                    return result.dict()
                elif hasattr(result, "__dict__"):
                    return result.__dict__
                elif isinstance(result, (list, tuple)):
                    # Convert list/tuple of custom objects
                    return [
                        item.dict() if hasattr(item, "dict") else
                        item.__dict__ if hasattr(item, "__dict__") else item
                        for item in result
                    ]
                return result
        result = asyncio.run(run_tool_async(tool_name))
        return jsonify(result) if result is not None else ("Tool not found", 404)

    return app