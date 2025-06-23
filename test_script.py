# a test script using requests to run a tool in the server

import requests
import json


def test_get_tools():
    response = requests.get("https://counsellor-mcp-server.vercel.app/tools")
    assert response.status_code == 200, "Failed to get tools"
    tools = response.json()
    print(tools)
    assert isinstance(tools, list), "Tools should be a list"
    assert len(tools) > 0, "No tools found"

def test_get_state():
    response = requests.post(
        "https://counsellor-mcp-server.vercel.app/tools/getState",
        json={"arguments": None}  # or json={} if no arguments needed
    )
    assert response.status_code == 200, "Failed to get state"
    state = response.json()
    print(state)
    assert isinstance(state, list), "State should be a list"
    #assert "state" in state, "State key not found in response"
    #assert isinstance(state["state"], str), "State value should be a string"

def test_fetchConversation():
    response = requests.post("https://counsellor-mcp-server.vercel.app/tools/fetchConversationSnippets"
                             , json={"arguments": {'kwds': ['depression']}}
                             )
    assert response.status_code == 200, "Failed to fetch conversation snippets"
    conversation = response.json()
    print(conversation)
    assert isinstance(conversation, list), "Conversation should be a list"
    assert len(conversation) > 0, "No conversation snippets found"

def test_set_state():
    response = requests.post(
        "https://counsellor-mcp-server.vercel.app/tools/setState",
        json={"arguments": {"state": False}}  # replace with actual state value
    )
    assert response.status_code == 200, "Failed to set state"
    result = response.json()
    print(result)
    assert isinstance(result, list), "Result should be list"
    # assert "success" in result, "Success key not found in response"
    # assert result["success"] is True, "State was not set successfully"

if __name__ == "__main__":
    test_get_tools()
    test_get_state()
    test_set_state()
    # test_fetchConversation()
    print("Test passed!")