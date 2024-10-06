import warnings
from crewai import Crew
from personas import RSATitleAbstractGenerator, RSADetailWriter, SMEReviewer
from rsac_tasks import generate_title_abstract_task, generate_session_details_task, review_refine_task
from util import read_seed_file, save_output_to_log

warnings.filterwarnings('ignore')

# Read the seed input from the seed file
seed_abstract = read_seed_file("rsac_seed.txt")

# Define the Crew Workflow for RSA Abstract Writing
rsa_abstract_crew = Crew(
    agents=[
        RSATitleAbstractGenerator,  # Generates both title and abstract
        RSADetailWriter,            # Detail writer for session content
        SMEReviewer                 # SME reviewer for final refinement
    ],
    tasks=[
        generate_title_abstract_task,      # Generates both title and abstract
        generate_session_details_task,     # Develops detailed session description based on abstract
        review_refine_task                 # Final review and refinement based on SME feedback
    ],
    verbose=2
)

# Execute the Workflow with the Seed Abstract and Mission
result = rsa_abstract_crew.kickoff(inputs={"abstract": seed_abstract, "mission": "Create a compelling RSA Conference abstract."})

# Extract the individual components from the result
final_title = result.get("title", "No title generated")
final_abstract = result.get("abstract", "No abstract generated")
final_session_details = result.get("refined_details", "No session details generated")

# Create a consolidated final output
final_output = (
    f"### Final RSA Conference Submission\n\n"
    f"**Session Title:** {final_title}\n\n"
    f"**Abstract:**\n{final_abstract}\n\n"
    f"**Session Details:**\n{final_session_details}\n"
)

# Save the final consolidated output to a log file
output_file = save_output_to_log(final_output, log_dir="logs")
print(f"Final Output saved to: {output_file}")

# Print the final output for review
print(final_output)
