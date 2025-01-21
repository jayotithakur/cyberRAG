from phi.tools.googlesearch import GoogleSearch
from phi.tools.duckduckgo import DuckDuckGo
from phi.agent import Agent


# Create the Web Agent to search for information
web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    tools=[GoogleSearch(), DuckDuckGo()],  # Using both GoogleSearch and DuckDuckGo tools
    instructions=[
        "Always include sources & provide full URLs for the sources",
        "Given a topic by the user, respond with the most relevant and recent information",
        "Search in both English and other relevant languages where applicable",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

# Now, perform the search and gather the information
# query = "what are cybersecurity threats?"
# web_agent.print_response(query, stream=True) 

web_agent.cli_app(stream=True)

