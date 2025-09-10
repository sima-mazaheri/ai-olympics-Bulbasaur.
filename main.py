import os
import sys
import json

# Add the 'agents' folder to the system path to allow importing
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Now you can import your agents
from knowledge_agent import get_solution_proposal
from diagram_agent import create_solution_diagram

def mcp_server():
    """
    This is the main orchestration server.
    It takes client requirements, uses AI agents to generate a proposal,
    and creates a corresponding technical diagram.
    """
    print("Welcome to the Infostatus AI Solution Architect!")
    print("--------------------------------------------------")

    # Step 1: Gather Requirements (The user's input)
    client_requirements = input("Please describe the client's technical requirements: ")

    if not client_requirements:
        print("Requirements cannot be empty. Exiting.")
        return

    print("\nProcessing requirements with the Knowledge Agent...")

    # Step 2: Use the Knowledge Agent to get a proposal in JSON format
    try:
        solution_data = get_solution_proposal(client_requirements)
        print("\n--- Generated Proposal from Knowledge Agent ---")
        print(json.dumps(solution_data, indent=2))
    except Exception as e:
        print(f"Error getting proposal: {e}")
        return

    print("\nCreating a solution diagram with the Diagram Agent...")
    
    # Step 3: Use the Diagram Agent to create a visual
    diagram_created = create_solution_diagram(solution_data)
    
    if diagram_created:
        print("\nProcess complete. Your full proposal and diagram are ready!")
        print("You can find the diagram in the 'diagrams_output' folder.")
    else:
        print("\nProcess completed with errors. Diagram could not be created.")

# Run the server
if __name__ == "__main__":
    mcp_server()