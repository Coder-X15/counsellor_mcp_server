from fastmcp import FastMCP
import pandas as pd
from .adapter import build_app

# Create an MCP server instance named "Demo"
mcp = FastMCP("Demo", stateless_http=True, instructions="This is a demo server for mental health counseling conversations. Use the tools provided to fetch conversation snippets and control the music player widget.")

# loading resources
# 1. The dataset to fetch advice from
mental_health_df = pd.read_json("hf://datasets/Amod/mental_health_counseling_conversations/combined_dataset.json", lines=True)

# 2. The state of the music player widget
music_player_state = False

@mcp.tool()
def fetchConversationSnippets(kwds: list) -> str:
    # this too finds out those rows in `mental_health_df` that
    # contains the keywords in `kwds` and concatenates them to a larger text message and returns it.
    # The keywords must either be in the 'Context' column or in the 'Response' column for that row
    # to be included in the snippet.

    # step 1: figure out the indices
    indices = mental_health_df.apply(lambda row: any(keyword in str(row['Context']) or keyword in str(row['Response']) for keyword in kwds), axis=1)

    # step 2: filter out the rows in those indices and get the Response column alone
    filtered_df = mental_health_df[indices]['Response']

    # step 3: unite the snippets into a single text message and return
    return " ".join(filtered_df.values.tolist())



@mcp.tool()
def setState(state: bool) -> bool:
    # sets the state of the music player widget in the Streamlit frontend
    global music_player_state
    try:
        music_player_state = state
        return True # inidicates successful state setting
    except:
        return False # indicates unsuccessful state setting


@mcp.tool()
def getState() -> bool:
    # returns the state of the music player widget
     return music_player_state


app = build_app(mcp)

if __name__ == "__main__":
    # initialize and start the server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)