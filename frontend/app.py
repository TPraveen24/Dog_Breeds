import streamlit as st
import requests
import uuid

# FastAPI Endpoint URL
API_URL = "http://backend:8000/ask/"

# Initialize session state for chat history & user ID
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Store past queries & responses
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())  # Generate a unique user ID

st.set_page_config(page_title="🐶 Chat with Dog Breed AI", layout="wide")
st.title("🐶 Dog Breed Chat Assistant")
st.markdown("Chat with AI about dog breeds!")

# Display Chat History as a Conversation
st.write("### 🗨️ Chat Window")
chat_container = st.container()
for chat in st.session_state.chat_history:
    with chat_container:
        st.markdown(f"👤 **You:** {chat['question']}")
        st.markdown(f"🤖 **AI:** {chat['response']}")

# User input
with st.form(key="chat_form", clear_on_submit=True):
    question = st.text_input("Type your message:", key="input_box")
    submit_button = st.form_submit_button("Send") 

#question = st.text_input("Type your message:", "",)

if submit_button and question.strip() :
        # Send request to FastAPI
        response = requests.post(API_URL, params={"question": question, "user_id": st.session_state.user_id})

        if response.status_code == 200:
            data = response.json()
            
            # Store in session history
            st.session_state.chat_history.append({"question": question, "response": data['answer']})
            
            # Rerun Streamlit to update chat
            st.rerun()
        else:
            st.error("❌ Error fetching response.")


st.markdown("---")
st.info(f"User ID: `{st.session_state.user_id}`")
