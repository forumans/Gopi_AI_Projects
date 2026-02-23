'''
This is a simple finance bot that can help users manage their expenses, 
calculate their budget, and get advice on saving money.
The bot uses LangGraph to manage the conversation flow.
It uses keywords to identify the intent of the user input.
'''

import re, json, sys, os
import logging
from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from gopi_util import get_llm, get_llm_response, extract_amount_from_text

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
llm = get_llm()

# ============= STATE TYPE =============
# BotState acts as a memory for the conversation
class BotState(TypedDict, total=False):
    user_input: str
    intent: Optional[str]  # expense | budget | advice | unknown
    data: Optional[Dict[str, Any]]  # data returned by LLM
    expenses: List[Dict[str, Any]]  # list of expenses
    hitl_flag: bool   # safety check flag


# ============= HELPERS =============
# This method parses the amount and category from the user input and returns them
def parse_amount_and_category(text: str):
    logging.info(f"Entering parse_amount_and_category with text: {text}")
    cleanText = text.replace(",", "") # Remove commas from the text and call it clearnText

    # Extract the amount from the text
    amount = extract_amount_from_text(cleanText)

    # Extract the category from the text
    text_lower = text.lower()  # Normalize to lowercase for better matching

    # Using sets {} instead of lists [] ensures no duplicates and faster lookups
    categories = {
        "food": {"food", "restaurant", "meal", "dinner", "lunch", "breakfast", "snack", "coffee", "tea", "drink"},
        "shopping": {"shopping", "buy", "purchase", "gift", "present"}, 
        "grocery": {"vegetable", "fruit", "grocery", "groceries", "pulse", "grains", "oil", "salt", "sugar", "rice", "wheat", "flour"},
        "rent": {"rent", "house", "flat", "apartment", "property", "rental"},
        "travel": {"travel", "holiday", "trip", "vacation", "flight", "hotel"}
    }

    category = "general"

    for cat, keywords in categories.items():
        # any() works efficiently with sets for checking multiple terms
        if any(word in text_lower for word in keywords):
            category = cat
            break

    logging.info(f"Exiting parse_amount_and_category with amount: {amount}, category: {category}\n")
    return amount, category


# This method checks if the user input has any keywords that are high risk
def is_high_risk(text: str) -> bool:
    logging.info(f"Entering is_high_risk with text: {text}")
    risk_keywords = [
        "retirement", "liquidate", "loan against", "pledge", "sell house", 
        "quit job", "all-in", "bet everything", "margin", "mortgage my", 
        "crypto all", "withdraw provident fund", "pf withdraw"
    ]
    
    for keyword in risk_keywords:
        if keyword in text.lower():  # Check if any risk keyword is present in the text
            logging.info(f"Exiting is_high_risk with result: True (found keyword: {keyword})")
            return True
    logging.info(f"Exiting is_high_risk with result: False\n")
    return False


# ============= NODES =============
# This method determines the intent of the user input
def node_intent(state: BotState) -> BotState:
    logging.info(f"Entering node_intent with state: {state}")
    text = state.get("user_input", "")
    tl = text.lower().strip()
    
    # 1) Safety check first
    state["hitl_flag"] = is_high_risk(tl)
    
    # 2) Keyword routing first (deterministic)
    if any(k in tl for k in ["budget", "summary", "total", "total spent", "total spend", "how much", "how much spent"]): 
        intent = "budget"
    elif any(k in tl for k in ["add", "spent", "expense", "expenses", "expense list", "expenses list", "rs", "inr", "$"]): 
        intent = "expense"
    elif any(k in tl for k in ["advice", "suggest", "tip", "plan", "how do i", "save for"]): 
        intent = "advice"
    else:
    # 3) Fallback to LLM (probabilistic) to understand user intent
        prompt = f"""
        Determine the intent of the following user query and return only one of the following intents:
        expense | budget | advice | unknown
        User Query: {text}
        """
        intent = get_llm_response(prompt)
    
    # Store intent in the state
    state["intent"] = intent
    logging.info(f"Exiting node_intent with intent: {intent}, hitl_flag: {state.get('hitl_flag')}\n")
    return state


# This method adds an expense to the expenses list
def node_expense(state: BotState) -> BotState:
    logging.info(f"Entering node_expense with state: {state}")
    text = state.get("user_input", "") # Get the user input from the state
    amount, category = parse_amount_and_category(text) # Parse the amount and category from the user input

    if amount is None:
        state["data"] = {"Please enter a valid amount"} # If amount is None, set the data to a dictionary with a message
        logging.info(f"Exiting node_expense with error: Invalid amount\n")
        return state

    state.setdefault("expenses", []).append({"amount": amount, "category": category}) # If amount is not None, append the amount and category to the expenses list
    state["data"] = f"Added expense: {amount} for {category}" # Set the data to a dictionary with a message

    logging.info(f"Exiting node_expense with added expense: {amount} for {category}\n")
    return state


# This method calculates the total expenses and the total expenses by category
def node_budget(state: BotState) -> BotState:
    logging.info(f"Entering node_budget with state: {state}")
    expenses = state.get("expenses", []) # Get the expenses list from the state

    total = sum(expense["amount"] for expense in expenses) if expenses else 0 # Calculate the total expenses if expenses list is not empty

    by_category: Dict[str, float] = {}
    for expense in expenses:
        category = expense["category"]
        by_category[category] = by_category.get(category, 0) + expense["amount"] # Calculate the total expenses by category

    state["data"] = json.dumps({"total_spent": total, "by_category": by_category}) # Set the data to a JSON string
    logging.info(f"Exiting node_budget with total: {total}, by_category: {by_category}\n")
    return state


# This method gives 3 short, friendly money saving tips
def node_advice(state: BotState) -> BotState:
    logging.info(f"Entering node_advice with state: {state}")
    text = state.get("user_input", "") # Get the user input from the state
    prompt = f"""Give exactly 3 short one sentence, user friendly money saving tips for the following user query (bulletted list of 1-3): {text}"""
    advice = get_llm_response(prompt)
    state["data"] = advice
    logging.info(f"Exiting node_advice with advice: {advice}\n")
    return state

# This method handles high risk transactions
def node_hitl(state: BotState) -> BotState:
    logging.info(f"Entering node_hitl with state: {state}")
    state["data"] = (
        "This looks like a high risk transaction. Please consult a financial advisor before proceeding."
        "I'll pause here until a human reviews your request."
    )
    logging.info(f"Exiting node_hitl with warning message\n")
    return state


# This method handles fallbacks
def node_fallback(state: BotState) -> BotState:
    logging.info(f"Entering node_fallback with state: {state}")
    state["data"] = "I can help with: expenses, budget, and advice."
    logging.info(f"Exiting node_fallback with help message\n")
    return state


# ============= ROUTER =============
def choose_next(state: BotState) -> str:
    logging.info(f"Entering choose_next with state: {state}")
    
    if state.get("hitl_flag"):
        logging.info(f"Exiting choose_next with route: hitl\n")
        return "hitl"
    
    intent = state.get("intent", "unknown")
    if intent == "expense": 
        logging.info(f"Exiting choose_next with route: expense\n")
        return "expense"
    elif intent == "budget": 
        logging.info(f"Exiting choose_next with route: budget\n")
        return "budget"
    elif intent == "advice": 
        logging.info(f"Exiting choose_next with route: advice\n")
        return "advice"
    else: 
        logging.info(f"Exiting choose_next with route: fallback\n")
        return "fallback"


# ============= BUILD GRAPH =============
builder = StateGraph(BotState)
builder.add_node("intent", node_intent)
builder.add_node("expense", node_expense)
builder.add_node("budget", node_budget)
builder.add_node("advice", node_advice)
builder.add_node("hitl", node_hitl)
builder.add_node("fallback", node_fallback)

builder.set_entry_point("intent")
builder.add_conditional_edges(
    "intent", 
    choose_next, 
    {"hitl": "hitl", "expense": "expense", "budget": "budget", "advice": "advice", "fallback": "fallback"}
)

graph = builder.compile()


# ============= RUN GRAPH (Interactive Chat Loop) =============
def run_chat():
    logging.info("Starting Personal Finance Bot")
    print("Personal Finance Bot (type 'exit' to quit)")
    state: BotState = {"expenses": [], "hitl_flag": False} # Initialize the state

    while True:
        user_input = input("Enter your spending details (Ex: I spent 1000 for house rent, What is my total expenses, Give me 3 money saving tips), or 'exit' to quit: \n").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            logging.info("User exited the chat")
            break

        state["user_input"] = user_input
        logging.info(f"Processing user input: {user_input}")
        
        out = graph.invoke(state) # Invoke the graph with the state and get the output
        print("Bot: ", out.get("data", "")) # Print the output
        logging.info(f"Bot response: {out.get('data', '')}")

        state = out # Update the state with the output

run_chat()

