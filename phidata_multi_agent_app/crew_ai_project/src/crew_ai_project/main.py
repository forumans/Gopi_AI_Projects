#!/usr/bin/env python
import sys
import warnings
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from crew_ai_project.crew import GopiCrewAiProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """

    input_str = input("Enter a stock symbol for analysis (e.g., AAPL, GOOGL, MSFT), or 'quit' to exit: ")

    if input_str.lower() == 'quit':
        print("Exiting...")
        return

    # Define the inputs for the crew
    inputs = {
        'topic': f'{input_str} Stock Growth Prediction',
        'current_year': str(datetime.now().year),
        'stock': input_str # Stock symbol to analyze
    }

    try:
        result = GopiCrewAiProject().crew().kickoff(inputs=inputs)
        print("Crew execution completed successfully.")
        
        # Generate Mermaid chart
        generate_mermaid_chart()
        print("Mermaid chart generated successfully.")
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        GopiCrewAiProject().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GopiCrewAiProject().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        GopiCrewAiProject().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = GopiCrewAiProject().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


def generate_chart_only():
    """
    Generate only the Mermaid chart without running the crew
    """
    generate_mermaid_chart()




def generate_mermaid_chart():
    """
    Generate a Mermaid chart showing the CrewAI workflow
    """
    mermaid_chart = """
```mermaid
graph TD
    A[User Input: Stock Symbol] --> B[Stock Price Analyst]
    B --> B1[Get Current Stock Price]
    B1 --> C[Stock News Analyst]
    C --> C1[Analyze Latest News]
    C1 --> D[Researcher]
    D --> D1[Predict Future Trends]
    D1 --> E[Reporting Analyst]
    E --> E1[Generate Final Report]
    E1 --> F[Output: report.md]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#f3e5f5
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#e8f5e8
```
"""
    
    # Save to file
    with open("crew_workflow.md", "w") as f:
        f.write("# CrewAI Workflow Chart\n\n")
        f.write(mermaid_chart)
    
    print("Mermaid chart saved to 'crew_workflow.md'")
    print("You can copy this chart to Mermaid-compatible tools like:")
    print("- GitHub markdown")
    print("- Mermaid Live Editor (https://mermaid.live)")
    print("- VS Code with Mermaid extension")





if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--chart":
        generate_chart_only()
    else:
        run()
