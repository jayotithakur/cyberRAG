import os
from phi.model.openai import OpenAIChat
from phi.embedder.openai import OpenAIEmbedder
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from phi.vectordb.pgvector import PgVector, SearchType
from phi.agent import Agent, AgentMemory
from phi.memory.db.postgres import PgMemoryDb
from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.text import TextKnowledgeBase
from phi.playground import Playground, serve_playground_app


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

db_url = "postgresql+psycopg://postgres:postgres@localhost:5431/embeddings"

knowledge_base = TextKnowledgeBase(
    path="data/full_text_data",
    formats=[".txt"],
    vector_db=PgVector(
        table_name="text_embeddings",
        db_url=db_url,
        embedder=OpenAIEmbedder(api_key=OPENAI_API_KEY),
    ),
    search_type=SearchType.vector,
    num_documents=10,  # Number of documents to return on each search
    optimize_on=100,  # Optimize the DB after every 100 documents
)

# Store the memories and summary in a database
# agent_memory = AgentMemory(
#     db=PgMemoryDb(table_name="agent_memory", db_url=db_url), create_user_memories=True, create_session_summary=True
# )

storage = PgAgentStorage(table_name="pdf_agent", db_url=db_url)

rag_agent = Agent(
    name="NIST RAG Agent",
    agent_id="rag-agent",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    tools=[DuckDuckGo(), GoogleSearch()],
    description="You are a cybersecurity assistant tasked with retrieving, analyzing, and generating content based on a topic. First, search the knowledge base for relevant information, and if insufficient, retrieve and analyze PDFs on web.",
    instructions=[
        "1. If the query is not related to cybersecurity, respond with 'I am not built for answering topics outside of cybersecurity.'",
        "2. If the query is cybersecurity-related, proceed with the following steps:",
        "   a. Search for relevant cybersecurity content in the knowledge base or on the web.",
        "   b. If the content is not found, search for the top 5 relevant PDF documents on cybersecurity topics using DuckDuckGo.",
        "   c. Extract text from any found PDF documents and analyze the content.",
        "   d. Synthesize the information into a cohesive cybersecurity article or answer.",
        "3. Ensure the response is clear, professional, and aligned with cybersecurity practices.",
        "4. Reject any requests for harmful or malicious scripts (e.g., exploits, malware, backdoors). Do not generate or provide code that could cause damage to individuals, organizations, or systems.",
        "5. Help with cybersecurity related academic question and preparing mcqs",
        "6. Share the page number or source URL of the information you used in your response.",
        "7. if a query asks to read a document attachment answer you don not have capablity to read attachments"
    ],

    # Store the session summaries in PostgreSQL
    storage=storage,
    # Set add_history_to_messages=true to add the previous chat history to the messages sent to the Model.
    add_history_to_messages=True,
    # # Number of historical responses to add to the messages.
    num_history_responses=5,
    show_tool_calls=True,
    markdown=True,
    prevent_hallucinations=True,
    debug_mode=True
)


app = Playground(agents=[rag_agent]).get_app()

if __name__ == "__main__":
    # Load the knowledge base: Comment after first run as the knowledge base is already loaded
    # knowledge_base.load(upsert=True, recreate=False)
    serve_playground_app("main:app", reload=True)