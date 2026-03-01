
'''
Build a LangGraph to perform Web Search, Calculations, and Python code execution using tools.
'''

import os, sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_agent

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from global_util.gopi_util import get_llm

# Create OpenAI embeddings - Embeddings are used to convert text to vectors for semantic search
def create_openai_embeddings_model():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=my_openai_api_key)
    return embeddings


MY_SYSTEM_PROMPT = """
You are a helpful AI assistant with access to three tools:

1. **web_search** - Search the web for up-to-date information using DuckDuckGo.
2. **calculator** - Evaluate mathematical expressions (support standard math operators and functions like sqrt, sin, cos, log, pi, e). 
3. **python_repl** - Execute Python code and get results. Use this for tasks needing programming, data manipulation, or anything beyond simple math.
4. **get_current_datetime** - Get the current date and time in any timezone.
5. **convert_time** - Convert time from one timezone to another.

Guidelines:
- Pick the most appropriate tool for each sub-task.
- For math, prefer the calculator tool. For complex logic or multi-step calculations, use python_repl.
- For any latest news and other information, use web_search tool.
- For any programming related tasks, use python_repl tool.
- For any time related tasks, use get_current_datetime tool.
- For any time conversion tasks, use convert_time tool.
- If a tool fails, try an alternative approach or rephrase the task.
"""


# Create a calculator tool
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)

        print(f"Expression: {expression}, Result: {result}")

        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# Create a get_current_datetime tool
@tool
def get_current_datetime(timezone: str = "UTC") -> str:
    """Get current date and time in specified timezone."""
    from datetime import datetime
    import pytz
    
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Error getting time for {timezone}: {str(e)}"

# Create a convert_time tool
@tool
def convert_time(time_str: str, from_tz: str, to_tz: str) -> str:
    """Convert time from one timezone to another."""
    from datetime import datetime
    import pytz
    
    try:
        from_tz_obj = pytz.timezone(from_tz)
        to_tz_obj = pytz.timezone(to_tz)
        
        # Parse the time string (assuming format: 'YYYY-MM-DD HH:MM:SS')
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        time_obj = from_tz_obj.localize(time_obj)
        
        converted_time = time_obj.astimezone(to_tz_obj)
        return f"{time_str} {from_tz} = {converted_time.strftime('%Y-%m-%d %H:%M:%S %Z')} {to_tz}"
    except Exception as e:
        return f"Error converting time: {str(e)}"


# Create a search tool
# This tools is already built-in in langchain_community.tools
search_tool = DuckDuckGoSearchRun(name="web_search") 


# Create a Python REPL tool
python_tool = PythonREPLTool(name="python_repl")


# Create an agent instance
def create_agent_instance():
    llm = get_llm()
    tools = [calculator, search_tool, python_tool, get_current_datetime, convert_time]

    agent = create_agent(llm, tools, system_prompt=MY_SYSTEM_PROMPT)
    
    return agent

# Run the agent
def run_agent(agent, user_query: str) -> str:
    my_config = {"recursion_limit": 100}
    
    print(f"User query: {user_query}")

    # Invoke the agent with the user's query
    result = agent.invoke({"messages": [HumanMessage(content=user_query)]}, config=my_config)

    # Return the output from the result
    return result["messages"][-1].content

# Show menu
def show_menu():
    
    agent = create_agent_instance()

    while True:
        print("\n================================================")    
        print("1. Ask a question")
        print("2. Exit")
        choice = input("Choose an option (1-2): ")
        
        if choice == "1":
            user_query = input("Enter your question (Web Search, Run Python Code, Get Current Time, Convert Time): ")
            print("\nAgent is thinking... and will call the appropriate tools to answer your question....")
            result = run_agent(agent, user_query)
            print(result)
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 2.")

if __name__ == "__main__":
    show_menu()

