'''
Build a sequential chain of LLMs to generate a topic and then generate content based on the topic.
Use LangChain to create a prompt template and invoke the LLM.
'''

import os, sys
from concurrent.futures import TimeoutError
from google.genai.types import Content
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from global_util.gopi_util import get_llm


# temperature - controls the randomness of the output
# temperature = 0 - Strict
# temperature = 1 - Creative

#llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=os.getenv("GEMINI_API_KEY"))
#llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", openai_api_key=os.getenv("GOPI_OPENAI_API_KEY"))
llm = get_llm()

def demo_sequential_exec():
    subject_prompt = PromptTemplate.from_template("Generate a creative topic about {subject} in one sentence.") # It's like one agent
    content_prompt = PromptTemplate.from_template("Write a short paragraph about {topic}") # It's like another agent

    subject_runnable = subject_prompt | llm | StrOutputParser()
    content_runnable = content_prompt | llm | StrOutputParser()

    sequential_chain = (
        RunnablePassthrough() # A queue to hold the input
            .assign(topic=subject_runnable) # First the subject_runnable is executed and output is stored in the {topic} variable.
            .assign(content=content_runnable) # Sencond the content is generated using the topic
    )

    result = sequential_chain.invoke({"subject": "Artificial Intelligence"})
    
    print(result)
    

if __name__ == "__main__":
    #demo_simple_prompt()
    #demo_role_based_prompt()
    demo_sequential_exec()


