from autogen import AssistantAgent, UserProxyAgent
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Setup API key. Add your own API key to config file or environment variable
config_list = [
    {
        "model": "llama3.2",
        "base_url": "http://localhost:11434/v1",
        'api_key': 'ollama',
    },
]

traveller = AssistantAgent(name="You: ",
                       max_consecutive_auto_reply=2,
                       system_message="You are a traveller exploring a new city. You are talking to travel assistant to get a optimal travel itinerary.",
                       llm_config={
                           "config_list": config_list,
                           "temperature": 1,
                       },
                       human_input_mode='ALWAYS')

travel_agent_sys_msg = """You are a one-day tour planning assistant that helps users create a comprehensive plan for exploring a city based on their preferences. The system should remember user preferences across the conversation to personalize future itinerary suggestions based on past interactions. 

As an professional travel assistant you must:
1. Ask the user for details such as the city to visit, available timings, budget, and interests (e.g., culture, adventure, food, shopping).
2. Ask for a starting point, such as their hotel or any other location. If the user does not provide a starting point, consider the starting point to be the first attraction itself. Include the distance and travel time from the starting point to the first attraction if a starting point is provided.
3. If the user is unsure about what places to visit or their preferences, suggest popular attractions based on the city, user interests, and budget.

Ask this questions in converstions one by one. And not bombard them with list of question. Ask only one question at a time.

Ask about dates and duration for which itinerary needs to be planned first.

Based on the user's preferences, you should generate an itinerary that includes 
the following details:
1. A list of places to visit,
2. the optimal sequence of visits,
3. transportation methods. 
"""
travel_agent = AssistantAgent(name="Travel Assisstant",
                     max_consecutive_auto_reply=2,
                     system_message=travel_agent_sys_msg,
                     llm_config={
                         "config_list": config_list,
                         "temperature": 1,
                     })

# traveller.initiate_chat(travel_agent, message="Hi! How can I assisit you today?")
chat_history = traveller.initiate_chat(travel_agent)


summary = ""
for message in chat_history.chat_history:
    summary += f"{message['role']}: {message['content']}\n"
    
summarier = AssistantAgent(name="Summary",
                     max_consecutive_auto_reply=1,
                     system_message="Based on the the conversation between user and travel agent, generate a travel itinerary that includes the following details: 1. A list of places to visit, 2. the optimal sequence of visits, 3. transportation methods. Include the distance and travel time from the starting point to the first attraction if a starting point is provided. Generate an optimized path based on the user's budget. If the budget allows for taxis, identify which segments can use taxis and adjust the itinerary accordingly to minimize travel time and maximize convenience. Make sure that the prices are accurate and realistic. Do not hard card anything. ",
                     llm_config={
                         "config_list": config_list,
                         "temperature": 1,
                     })