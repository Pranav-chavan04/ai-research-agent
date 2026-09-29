from pathlib import Path

import requests
from ddgs import DDGS
from dotenv import load_dotenv

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)


@tool
def web_search(query: str) -> str:
    """Search the web for information."""

    query = query.strip()

    if not query:
        return "Search query cannot be empty."

    try:
        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return "No search results found."

        output = []

        for result in results:
            output.append(
                f"Title: {result.get('title', 'Unknown')}\n"
                f"URL: {result.get('href', 'Unknown')}\n"
                f"Snippet: {result.get('body', 'No description')}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Web search failed: {e}"

@tool
def write_code(filename: str, code: str) -> str:
    """Write code to a file inside the workspace."""

    filename = filename.strip()

    if not filename:
        return "Filename cannot be empty."

    if not code.strip():
        return "Code cannot be empty."

    path = (WORKSPACE / filename).resolve()
    workspace_path = WORKSPACE.resolve()

    if not str(path).startswith(str(workspace_path)):
        return "Invalid filename."

    try:
        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            code,
            encoding="utf-8"
        )

        return (
            f"Successfully wrote {path}\n\n"
            f"```python\n{code}\n```"
        )

    except Exception as e:
        return f"Failed to write file: {e}"


@tool
def tell_joke(topic: str) -> str:
    """Fetch a random joke from an external API."""

    topic = topic.strip()

    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/jokes/random",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        setup = data.get("setup")
        punchline = data.get("punchline")

        if not setup or not punchline:
            return "The joke service returned an invalid joke."

        return f"{setup}\n\n{punchline}"

    except requests.RequestException as e:
        return f"Joke service failed: {e}"

    except Exception as e:
        return f"Unexpected joke error: {e}"


tools = [
    web_search,
    write_code,
    tell_joke
]

model_with_tools = model.bind_tools(tools)


class State(MessagesState):
    pass


def chatbot(state: State):
    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)

graph = StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chatbot")

graph.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph.add_edge("tools", "chatbot")

app = graph.compile()