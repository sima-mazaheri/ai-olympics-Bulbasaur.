from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, DynamoDB
from diagrams.aws.network import VPC
import os

def create_solution_diagram(solution_data, file_name="solution_diagram"):
    """
    Generates a technical diagram based on a list of services and connections.
    
    Args:
        solution_data (dict): A dictionary containing 'services' and 'connections'.
    """
    
    # Create the output folder if it doesn't exist
    output_dir = "diagrams_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with Diagram("Proposed Solution Architecture", show=False, filename=f"{output_dir}/{file_name}", direction="TB"):
            
            # Map of service names to their corresponding icons
            service_map = {
                "EC2": EC2,
                "Lambda": Lambda,
                "RDS": RDS,
                "DynamoDB": DynamoDB,
                "VPC": VPC
            }

            # Create service nodes based on the input data
            nodes = {}
            for service in solution_data.get('services', []):
                # Look up the icon from our map, defaulting to a generic icon if not found
                node_class = service_map.get(service, EC2)
                nodes[service] = node_class(service)

            # Create connections based on the input data
            for conn in solution_data.get('connections', []):
                source_service, target_service = conn
                if source_service in nodes and target_service in nodes:
                    nodes[source_service] >> nodes[target_service]

    except Exception as e:
        print(f"Error creating diagram: {e}")
        return False
        
    print(f"Diagram '{file_name}.png' created successfully in the '{output_dir}' folder.")
    return True

# This is a sample input to test the agent
if __name__ == "__main__":
    sample_solution = {
        "services": ["EC2", "RDS", "DynamoDB"],
        "connections": [
            ["EC2", "RDS"],
            ["EC2", "DynamoDB"]
        ]
    }
    create_solution_diagram(sample_solution)