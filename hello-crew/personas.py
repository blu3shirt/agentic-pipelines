from crewai import Agent
from langchain_openai import ChatOpenAI

# Setup for the LLM
llm = ChatOpenAI(
    model="llama3.2:1b-instruct-q8_0",  # Replace with your preferred model
    base_url="http://localhost:11434/v1",
    openai_api_key='NA'
)

# Define Agents for the Simplified RSA Abstract Pipeline
class RSAAgents:
    # Combined Title and Abstract Generator Agent
    class RSATitleAbstractGenerator(Agent):
        def __init__(self):
            super().__init__(
                role="RSAC Title and Abstract Generator",
                goal="Create compelling titles and concise abstracts that clearly communicate the session’s value.",
                backstory="You specialize in crafting impactful titles and abstracts for technical sessions, focusing on clarity and engagement.",
                allow_delegation=False,
                verbose=True,
                llm=llm
            )

        def execute(self, task_description, context=None):
            abstract = context.get("abstract", "")
            mission = context.get("mission", "")
            if not abstract or not mission:
                raise ValueError("Missing required context for title and abstract generation.")
            
            # Generate dynamic content based on abstract and mission
            title = f"AI-Driven Identity Protection: {mission}"
            abstract_output = (
                f"In an era of evolving digital threats, organizations must go beyond traditional IAM strategies. "
                f"This session, '{title}', will reveal how AI-powered IAM solutions enable real-time risk assessment, "
                f"automated compliance scanning, and intelligent threat detection to protect identities and data. "
                f"Attendees will learn actionable strategies to strengthen IAM through AI innovation."
            )
            return {"title": title, "abstract": abstract_output}

    # Detail Writer Agent
    class RSADetailWriter(Agent):
        def __init__(self):
            super().__init__(
                role="RSAC Detail Writer",
                goal="Develop comprehensive session details that include actionable takeaways and align with RSA guidelines.",
                backstory="You create session details that resonate with technical and business leaders, using real-world examples and case studies.",
                allow_delegation=False,
                verbose=True,
                llm=llm
            )

        def execute(self, task_description, context=None):
            title = context.get("title", "")
            abstract = context.get("abstract", "")
            if not title or not abstract:
                raise ValueError("Missing title or abstract for session detail generation.")

            # Develop dynamic session details using the title and abstract
            session_details = (
                f"**Session Title:** {title}\n\n"
                f"**Abstract Overview:**\n{abstract}\n\n"
                "**Problem Statement:**\n"
                "The rapid adoption of AI in IAM has brought new challenges, including real-time risk assessment, compliance management, and "
                "threat detection. Without robust AI-powered tools, traditional IAM solutions are becoming ineffective against evolving threats.\n\n"
                "**Key Discussion Points:**\n"
                "- **Understanding AI-Specific IAM Challenges**: How AI introduces both new risks and opportunities in IAM.\n"
                "- **AI-Driven Real-Time Risk Assessment**: Implementing dynamic, context-aware risk assessment in IAM systems.\n"
                "- **Automated Compliance Management**: Using AI to automate compliance checks and streamline auditing.\n"
                "- **Threat Detection in IAM Systems**: Leveraging AI for anomaly detection and real-time response.\n\n"
                "This session will feature technical deep dives and real-world case studies from leading organizations that have successfully "
                "integrated AI into their IAM strategies."
            )

            return {"session_details": session_details}

    # SME Reviewer Agent
    class SMEReviewer(Agent):
        def __init__(self):
            super().__init__(
                role="SME Reviewer",
                goal="Review and refine the session details based on RSA standards and audience expectations.",
                backstory="You have extensive experience presenting at RSA and validating technical content for accuracy.",
                allow_delegation=False,
                verbose=True,
                llm=llm
            )

        def execute(self, task_description, context=None):
            session_details = context.get("session_details", "")
            if not session_details:
                raise ValueError("Missing session details for SME review.")

            # Provide specific suggestions for improvement
            suggestions = []
            if "compliance management" not in session_details:
                suggestions.append("Expand on how AI improves compliance management, particularly in regulated industries like finance and healthcare.")
            if "real-world case studies" not in session_details:
                suggestions.append("Include specific case studies demonstrating AI success in IAM.")

            # Incorporate feedback into session details
            refined_details = session_details
            for suggestion in suggestions:
                refined_details += f"\n\n**Suggested Improvement:** {suggestion}"

            return {"refined_details": refined_details}

# Instantiate agents
RSATitleAbstractGenerator = RSAAgents.RSATitleAbstractGenerator()
RSADetailWriter = RSAAgents.RSADetailWriter()
SMEReviewer = RSAAgents.SMEReviewer()
