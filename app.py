import streamlit as st
import requests
import json
import time

url = "https://api.awanllm.com/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  'Authorization': "Bearer API_KEY"
}

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


# Streamed response emulator
def ask_awan(prompt):
    payload = json.dumps({
      "model": "Awanllm-Llama-3-8B-Dolfin",
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    response_json = json.loads(response.text) 

    for word in response_json["choices"][0]["message"]["content"].split():
        yield word + " "
        time.sleep(0.05)

# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(ask_awan(prompt))
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})
