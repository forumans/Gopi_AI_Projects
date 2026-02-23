'''
Build a role based prompt to interact with OpenAI LLM.
Use LangChain to create a prompt template and invoke the LLM.
'''

import os, sys
from concurrent.futures import TimeoutError
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from global_util.gopi_util import get_llm

# temperature - controls the randomness of the output
# temperature = 0 - Strict
# temperature = 1 - Creative

#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="GEMINI_API_KEY")
#llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", openai_api_key=os.getenv("GOPI_OPENAI_API_KEY"))
llm = get_llm()

# This is a simple prompt template with 
# an expectation set to the LLM and the user prompt
def demo_simple_prompt():
    template_str = """
    You are a helpful assistant who always replies cheerfully and with emojis.
    Question: {user_prompt_input}
    Answer: 
    """

    prompt = PromptTemplate(
        input_variables=["user_prompt_input"],
        template=template_str
    )

    # Create a langchain expression language: prompt | llm | parser
    chain = prompt | llm | StrOutputParser()
    
    print("Calling LLM...")
            
    # Invoke the chain
    # The variable name "question_param" is used in the template
    # Then the actual question itself
    result = chain.invoke({"user_prompt_input": "What is the capital of France?"})
    
    print(result)


# This is a role based prompt template with 
# an expectation set to the LLM and the user prompt
def demo_role_based_prompt():
    chat_propt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a {role} who speaks in a {style} manner."),
            ("human", "{user_input}")
        ]
    )

    chain = chat_propt | llm | StrOutputParser()

    result = chain.invoke({"role": "Hindi Teacher", "style": "professional", 
        "user_input": "What are the benefits of Pyton programming language? Explain in 5 lines in Hindi language."})

    print(result)




if __name__ == "__main__":
    #demo_simple_prompt()
    demo_role_based_prompt()


