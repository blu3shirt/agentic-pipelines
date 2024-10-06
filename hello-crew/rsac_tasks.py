from crewai import Task
from personas import RSATitleAbstractGenerator, RSADetailWriter, SMEReviewer

# Define the Combined Title and Abstract Generation Task
generate_title_abstract_task = Task(
    description=(
        "### Task 1: Title and Abstract Generation\n"
        "1. **Title Generation**:\n"
        "    - Generate a compelling and concise title for the RSA Conference session.\n"
        "    - The title should reflect the main theme of the session and be attention-grabbing.\n"
        "    - Limit the title to 75 characters to ensure clarity and adherence to RSA guidelines.\n"
        "    - Emphasize a unique angle that relates specifically to AI security or risk management.\n\n"
        "2. **Abstract Generation**:\n"
        "    - Create a 400-character abstract that succinctly summarizes the session's purpose.\n"
        "    - Highlight key AI-specific risks and the solutions discussed in the session.\n"
        "    - Use direct, impactful language to convey what the audience will learn.\n"
        "    - Include a call-to-action if applicable to emphasize the value proposition of attending.\n\n"
        "3. **Audience Alignment**:\n"
        "    - Ensure that the title and abstract clearly state the value of the session for RSA attendees, such as CISOs, technical leaders, or industry strategists.\n"
        "    - Avoid overly technical jargon unless it adds significant value.\n\n"
        "4. **Consider RSA's Audience**:\n"
        "    - RSA attendees value cutting-edge insights, practical solutions, and real-world examples. Ensure the title and abstract cater to these priorities."
    ),
    expected_output=(
        "1. A session title with a maximum of 75 characters that captures the theme and interest of RSA attendees.\n"
        "2. A concise 400-character abstract that clearly summarizes the session’s focus, key learning points, "
        "and the value proposition for the audience."
    ),
    agent=RSATitleAbstractGenerator
)

# Define the Session Details Task
generate_session_details_task = Task(
    description=(
        "### Task 2: Session Detail Generation\n"
        "1. **Session Overview**:\n"
        "    - Develop a comprehensive session description that aligns with RSA guidelines and adheres to the 2,500-character limit.\n"
        "    - Introduce the topic by framing the importance of AI-driven identity and access management (IAM) in today’s cybersecurity landscape.\n\n"
        "2. **Problem Statement**:\n"
        "    - Clearly outline the problems organizations face with traditional IAM systems and the challenges introduced by evolving AI threats.\n"
        "    - Highlight why these challenges are significant and how they impact the industry.\n\n"
        "3. **Solution Framework**:\n"
        "    - Present the AI-driven solutions being covered, such as real-time risk assessment, automated compliance scanning, and intelligent threat detection.\n"
        "    - Explain how each solution helps mitigate identified risks and improves IAM effectiveness.\n\n"
        "4. **Real-World Case Studies**:\n"
        "    - Include at least two detailed case studies that showcase the practical application of these AI-driven IAM solutions.\n"
        "    - Make these case studies relatable to the audience (e.g., one case study on financial services and another on healthcare).\n\n"
        "5. **Actionable Recommendations**:\n"
        "    - Conclude the session details with actionable recommendations for attendees, including best practices, strategies, or frameworks that they can apply in their own organizations.\n"
        "    - Ensure recommendations are practical, specific, and aligned with RSA’s theme of advancing AI security.\n\n"
        "6. **Audience Engagement**:\n"
        "    - Suggest ways to engage the audience, such as Q&A sessions or interactive segments, to enhance the learning experience.\n"
        "    - Ensure the content encourages participation and discussion."
    ),
    expected_output=(
        "1. A comprehensive and well-organized session description, structured with an introduction, problem statement, solution overview, "
        "real-world examples, and clear actionable takeaways.\n"
        "2. A structured description that effectively engages RSA attendees and provides relevant, actionable insights."
    ),
    agent=RSADetailWriter
)

# Define the SME Review and Refinement Task
review_refine_task = Task(
    description=(
        "### Task 3: SME Review and Refinement\n"
        "1. **Review for Technical Accuracy**:\n"
        "    - Review the session details for accuracy regarding AI concepts, security threats, and IAM solutions.\n"
        "    - Validate technical points, especially those related to machine learning, anomaly detection, and risk mitigation.\n\n"
        "2. **Alignment with RSA Focus Areas**:\n"
        "    - Ensure that the session aligns with RSA’s focus on emerging threats, AI-driven security solutions, and advanced risk management.\n"
        "    - Verify that the content addresses pressing industry concerns, such as compliance and the need for advanced security frameworks.\n\n"
        "3. **Suggestions for Improvement**:\n"
        "    - Identify areas that require further elaboration, including adding more context or simplifying complex concepts for clarity.\n"
        "    - Suggest adding diagrams, flowcharts, or other visual aids where appropriate to enhance understanding.\n"
        "    - Provide specific recommendations for structuring content more logically or effectively.\n\n"
        "4. **Audience Engagement and Value**:\n"
        "    - Assess whether the session offers clear value to RSA attendees, including practical insights and takeaways.\n"
        "    - Ensure that the content has interactive elements to foster engagement and facilitate learning.\n\n"
        "5. **Final Refinement**:\n"
        "    - Based on the review, produce a final, polished version of the session details.\n"
        "    - Ensure that all recommendations are incorporated and that the final version meets RSA’s high standards for technical depth and audience engagement."
    ),
    expected_output=(
        "1. Annotated session details with detailed feedback and suggestions for refinement.\n"
        "2. Final refined session details that are polished, professional, and aligned with RSA themes, providing "
        "clear takeaways and interactive value for the target audience."
    ),
    agent=SMEReviewer
)
