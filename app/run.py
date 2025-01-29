# Import packages
import streamlit as st  
from langchain.agents import ConversationalChatAgent, AgentExecutor  
from langchain_community.callbacks import StreamlitCallbackHandler  
from langchain_openai import ChatOpenAI  
from langchain.memory import ConversationBufferMemory  
from langchain_community.chat_message_histories import StreamlitChatMessageHistory 
from langchain_community.tools import DuckDuckGoSearchRun  
import json
import requests
import warnings
warnings.filterwarnings('ignore')

# Page title
st.set_page_config(page_title = "Streamlit - GPT")

# Creating columns for page layout
# Defines the proportion of the columns
col1, col4 = st.columns([4, 1]) 

# Setting the first column to display the project title
with col1:
    st.title("Building and Deploying a Web Interface for Conversational Agent and Search with LangChain and LLM")

# Field for inputting the OpenAI API key
openai_api_key = st.sidebar.text_input("OpenAI API Key", type = "password")

# Initializing message history
# https://python.langchain.com/docs/integrations/memory/streamlit_chat_message_history/
msgs = StreamlitChatMessageHistory()

# Chat memory configuration
# https://python.langchain.com/docs/modules/memory/types/buffer/
memory = ConversationBufferMemory(chat_memory = msgs,
                                  return_messages = True,
                                  memory_key = "chat_history",
                                  output_key = "output")


# Check to clear message history or start conversation
if len(msgs.messages) == 0 or st.sidebar.button("Reset"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}

# Defining avatars for conversation participants
avatars = {"human": "user", "ai": "assistant"}

# Loop to display messages in chat
# Iterate over each message in the message history
for idx, msg in enumerate(msgs.messages):

    # Create a chat message with the avatar corresponding to the user type (human or AI)
    with st.chat_message(avatars[msg.type]):

        # Iterate over the stored steps for each message, if any
        for step in st.session_state.steps.get(str(idx), []):

            # If the current step throws an exception, skip to the next step
            if step[0].tool == "_Exception":
                continue


            # Create an expander for each tool used in the response, showing the input
            with st.expander(f"✅ **{step[0].tool}**: {step[0].tool_input}"):
                # Display the tool execution log
                st.write(step[0].log)

                # Display the result of the tool execution
                st.write(f"**{step[1]}**")

        # Exibe o conteúdo da mensagem no chat
        st.write(msg.content) 


# Input field for new user messages
if prompt := st.chat_input(placeholder = "Enter a question to get started!"):
    st.chat_message("user").write(prompt)

    # API key verification
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # OpenAI Language Model Configuration
    # https://python.langchain.com/docs/integrations/chat/openai/
    llm = ChatOpenAI(openai_api_key = openai_api_key, streaming = True)

    # Agent search engine configuration
    # https://api.python.langchain.com/en/latest/tools/langchain_community.tools.ddg_search.tool.DuckDuckGoSearchRun.html
    search_engine = [DuckDuckGoSearchRun(name = "Search")]

    # Creating a conversational agent with the search engine
    # https://api.python.langchain.com/en/latest/agents/langchain.agents.conversational_chat.base.ConversationalChatAgent.html
    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm = llm, tools = search_engine)
    
    # Executor for the agent, including memory and error handling
    # https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html
    executor = AgentExecutor.from_agent_and_tools(agent = chat_agent,
                                                  tools = search_engine,
                                                  memory = memory,
                                                  return_intermediate_steps = True,
                                                  handle_parsing_errors = True)
    
    # Displaying the assistant's response
    with st.chat_message("assistant"):
        # Callback to Streamlit
        # https://api.python.langchain.com/en/latest/callbacks/langchain_community.callbacks.streamlit.streamlit_callback_handler.StreamlitCallbackHandler.html
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts = False)
        response = executor(prompt, callbacks = [st_cb])
        st.write(response["output"])

        # Armazenamento dos passos intermediários
        st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"] 

# End