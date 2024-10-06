# personas.py

from crewai import Agent
from langchain_openai import ChatOpenAI
from duckduckgo_search import ddg  # Import DuckDuckGo search library

# Setup for the LLM
llm = ChatOpenAI(
    model="llama3.1:8b-instruct-q8_0",
    base_url="http://localhost:11434/v1",
    openai_api_key='NA'
)

# Define Agents with Search Capabilities
class WritingAgents:
    # Researcher Agent with DuckDuckGo Search Integration
    class Researcher(Agent):
        def __init__(self):
            super().__init__(
                role="Researcher",
                goal="Create a comprehensive research summary based on the provided topic using live search data.",
                backstory=(
                    "You are a research specialist with access to live search capabilities. "
                    "Your goal is to gather up-to-date information from the web using DuckDuckGo search and synthesize it "
                    "into a concise research summary."
                ),
                allow_delegation=False,
                verbose=True,
                llm=llm
            )

        # Custom search function
        def perform_search(self, query, max_results=5):
            """Uses DuckDuckGo to perform a live search and return results."""
            search_results = ddg(query, max_results=max_results)
            return search_results

        # Custom task execution to gather data and summarize
        def execute(self, task_description, inputs):
            """Override the default execute function to perform live search."""
            topic = inputs.get("topic", "")
            if not topic:
                return "No topic provided."

            # Perform the search and collect results
            search_query = f"{topic} site:scholar.google.com OR site:arxiv.org OR site:researchgate.net"
            search_results = self.perform_search(search_query)

            # Summarize the results
            research_summary = f"Research Summary for Topic: {topic}\n\n"
            for idx, result in enumerate(search_results):
                research_summary += f"{idx + 1}. Title: {result['title']}\n"
                research_summary += f"URL: {result['href']}\n"
                research_summary += f"Snippet: {result.get('body', 'No snippet available')}\n\n"

            return research_summary

    researcher = Researcher()

    # SME and Outliner Agents
    sme_1 = Agent(
        role="Subject Matter Expert 1",
        goal="Review the research summary and provide technical insights.",
        backstory=(
            "You are a subject matter expert specializing in AI Security. "
            "Your goal is to validate the research summary, ensuring it is accurate and complete."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    sme_2 = Agent(
        role="Subject Matter Expert 2",
        goal="Provide additional context and refine technical details in the research summary.",
        backstory=(
            "You are a secondary subject matter expert focused on adding depth to the research summary. "
            "Your goal is to highlight any missing elements and refine the technical content."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    outliner = Agent(
        role="Outliner",
        goal="Transform the research summary and SME inputs into a structured outline.",
        backstory=(
            "You are responsible for creating a clear and structured outline based on the research summary "
            "and SME feedback. Your outline should serve as a blueprint for abstract generation."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )
