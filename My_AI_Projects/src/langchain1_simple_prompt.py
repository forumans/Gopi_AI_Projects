'''
Build a simple prompt to interact with OpenAI LLM.
Use LangChain to create a prompt template and invoke the LLM.
'''

import os, sys
from concurrent.futures import TimeoutError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#from langchain_google_genai import ChatGoogleGenerativeAI
# Add project root to Python path to find global_util
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from global_util.gopi_util import get_llm

# =======================================================================================
# temperature - controls the randomness of the output
# temperature = 0 - Strict
# temperature = 1 - Creative
# =======================================================================================

#llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", openai_api_key=os.getenv("GOPI_OPENAI_API_KEY"))
#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="GEMINI_API_KEY")
llm = get_llm()

# ========================= BEGIN: Simple Prompt =========================
def demo_basic_prompt():
    template_str = """
    You are a helpful assistant who always replies cheerfully and with emojis.
    Question: {question_param}
    Answer: 
    """

    prompt = PromptTemplate(
        input_variables=["question_param"],
        template=template_str
    )

    # Create a langchain expression language: prompt | llm | parser
    chain = prompt | llm | StrOutputParser()
    
    print("Calling LLM...")
    
    # Invoke the chain
    # The variable name "question_param" is used in the template
    # Then the actual question itself
    result = chain.invoke({"question_param": "What is the capital of France?"})
    
    print(result)

if __name__ == "__main__":
    demo_basic_prompt()


