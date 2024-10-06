from crewai import Task
from personas import TopicParser, RSAResearcher, RSAOutliner, SME1, SME2

# Define the initial Topic Parsing task
parse_topic_task = Task(
    description=(
        "1. Analyze the seed abstract and extract key topics, focus areas, and main messages.\n"
        "2. Provide a structured output that includes topics, focus areas, and primary themes."
    ),
    expected_output="A structured list of topics, focus areas, and key messages from the abstract.",
    agent=TopicParser
)

# Define the initial research task based on extracted topics
generate_research_summary_task = Task(
    description=(
        "1. Use the parsed topics to conduct focused research on the provided topic.\n"
        "2. Summarize the key points, findings, and challenges in the research.\n"
        "3. Create a structured research summary that includes main findings and implications for RSA."
    ),
    expected_output="A detailed research summary covering the main findings and challenges of the topic.",
    agent=RSAResearcher
)

# Define the outline generation task based on research
generate_outline_task = Task(
    description=(
        "1. Create an initial outline based on the research summary.\n"
        "2. Ensure that the outline includes key sections and logical flow.\n"
        "3. Highlight the areas where SME feedback is required."
    ),
    expected_output="An initial structured outline covering all key research areas.",
    agent=RSAOutliner
)

# Define the SME 1 review task
sme_review_1_task = Task(
    description=(
        "1. Review the initial outline for technical accuracy and completeness.\n"
        "2. Provide insights on potential gaps or areas that need refinement.\n"
        "3. Ensure the outline aligns with research goals and mission context."
    ),
    expected_output="Annotated outline with technical feedback and suggestions.",
    agent=SME1
)

# Define the SME 2 review task
sme_review_2_task = Task(
    description=(
        "1. Review the refined outline incorporating SME 1 feedback.\n"
        "2. Add additional context or risk analysis perspectives where needed.\n"
        "3. Ensure that the outline covers all potential risks and mitigation strategies."
    ),
    expected_output="Final outline with cybersecurity risk analysis and SME 2 inputs.",
    agent=SME2
)

# Define the outline refinement task
refine_outline_task = Task(
    description=(
        "1. Refine the outline based on the feedback from SME 1 and SME 2.\n"
        "2. Adjust the structure to include all key points, supporting ideas, and details.\n"
        "3. Ensure that the hierarchical structure (I, A, i, (a), 1…) is followed."
    ),
    expected_output="A comprehensive outline with a hierarchical structure that incorporates all inputs.",
    agent=RSAOutliner
)
