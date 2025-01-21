from phi.agent import Agent,RunResponse
from phi.tools.email import EmailTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from pydantic import BaseModel, Field
from typing import List
import re


  

# Receiver and sender details
receiver_email = " "
# receiver_emails = os.getenv("RECEIVER_EMAILS", "").split(",")
sender_email = " "
sender_name = " "
sender_passkey = " "


# Initialize the EmailTools with necessary credentials
email_tool = EmailTools(
    receiver_email=receiver_email,
    sender_email=sender_email,
    sender_name=sender_name,
    sender_passkey=sender_passkey,
)

class URLResponse(BaseModel):
    status: str
    message: str
    urls: List[str]

# Create the Agent with HackerNews and EmailTools
news_agent = Agent(
    name="Hackernews Team",
    description="You are a news agent that helps users find the top news related to cybersecurity in canada",
    instructions =["Only include urls that are readable and reliable"],
    tools=[DuckDuckGo(news=True)],
    response_model=URLResponse,
    markdown=True,
)

summarize_agent = Agent(
    name="Summarize News",
    description="You are a news agent that summarizes the news",
    instructions=[
        "You will be provided with a list of URLs.",
        "Your task is to summarize the content of these articles concisely.",
        "Do not include titles or separate summaries for each article.",
        "For each article, provide a brief summary in 3-5 lines",
        "If you cannot access an article or encounter any issues, simply skip it without mentioning the error.",
        "If no summary is avaiable atleast add links as read more in the end",
        "Format the summary for each article as follows:",
        "1.",
        "2.",
        "3.",
    ],
    tools=[Newspaper4k(), email_tool],
    markdown=True,
)

def remove_markdown_formatting(text):
    # Remove bold formatting
    text = text.replace('**', '')
    # Remove italic formatting
    text = text.replace('*', '')
    # Remove heading formatting
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Add more replacements as needed for other markdown elements
    return text


def fetch_news():

    news_agent_response: RunResponse = news_agent.run("Get Top 10 latest stories url with http or https:")

    response_content = news_agent_response.content
    
    if response_content:
        try:
           
            # # Check if the response is not empty
            if not response_content:
                print("Error: No URLs found in the response.")
                return

            stories = response_content.urls

            urls = [url for url in stories]

            print("urls", urls)

            # # Use the extracted URLs in your summary agent
            summary_response = summarize_agent.run(f"Please summarize minimum 2 & maximum 5 stories from the urls and add a 'Read more' clickable link for each:\n\n" + "\n".join([f"- {url}" for url in urls]))
            
            print("Summary Response:", summary_response.content) 

            s_response = summary_response.content
        
            cleaned_summary = remove_markdown_formatting( s_response)
            
            email_body = cleaned_summary
            
            # Send the email
            email_tool.email_user(subject="Top Cybersecurity Stories Today", body=email_body)
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error processing the stories: {e}")
    else:
        print("Error: Unable to fetch the top stories.")


fetch_news()