import os
from phi.agent import Agent
from phi.model.openai import OpenAIChat


# Load env variables
from dotenv import load_dotenv
load_dotenv()

def create_basic_agent():
    agent = Agent(
        name="Jarvis",
        model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
        description="Jarvis is a helpful assistant.",
        instructions=[
            "Be concise and helpful. Ask questions if you need clarification."
        ],
        markdown=True, # Enable markdown formatting in responses
        debug=True # Enable debug mode for detailed logging

    )

    return agent

if __name__ == "__main__":
    agent = create_basic_agent()
    user_input = input("Hello, I am Jarvis. How can I help you?")
    agent.print_response(user_input)
