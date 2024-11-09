import streamlit as st
from langchain_ollama.llms import OllamaLLM
from autogen import ConversableAgent, UserProxyAgent

config_list = [
    {
        "model": "llama3.2",
        "base_url": "http://localhost:11434/v1",
        'api_key': 'ollama',
    },
]
llm_config={"config_list": config_list}

st.title("AI Travel Planner ChatBot")

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OllamaLLM(model="llama3.2", base_url="http://localhost:11434/")

zero_shot_agent = ConversableAgent(
    name="zero-shot-agent",
    system_message="You are helpul AI assistant",
    description="zero-shot-react-description",
    # tools=tools,
    llm_config=llm_config,
)

userproxy = UserProxyAgent(name="User",
    llm_config=llm_config,
    is_termination_msg=True,
    code_execution_config=False,
    human_input_mode="ALWAYS"   
)

if "ollama" not in st.session_state:
    st.session_state["ollama"] = "llama3.2"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message AI Aassistant?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.predict(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        # response = st.write_stream(userproxy.initiate_chat(zero_shot_agent))
    st.session_state.messages.append({"role": "assistant", "content": response})
