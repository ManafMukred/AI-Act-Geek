import streamlit as st
import requests
URL = "http://backend:8000/"


def handle_userinput(user_question, answer):

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "content" in message.keys():
                st.markdown(message["content"])

    # Display user message in chat message container
    with st.chat_message("user", avatar="🔍"):
        st.markdown(user_question)
    with st.chat_message("Assistant", avatar="🤓"):
        st.markdown(answer)

    # Append the chatbot's response to the chat history
    st.session_state.chat_history = st.session_state.chat_history + \
        "You: \n" + user_question + "\n "
    st.session_state.chat_history = st.session_state.chat_history + \
        "Chatbot: \n" + answer + "\n"
    # append previous messages
    st.session_state.messages.append(
        {"role": "user",      "content": user_question})
    st.session_state.messages.append({"role": "Assistant", "content": answer})
    # Clear the user input
    st.session_state.user_input = ""


def main():

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = ''
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ''
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    # st.write(css, unsafe_allow_html=True)
    st.header("Ask The Nerd 🤓")
    user_question = st.chat_input("Ask a question about your documents:")

    with st.sidebar:
        result = {}
        st.subheader("Your documents")
        uploaded_files = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", type="pdf",
            accept_multiple_files=True)
        if uploaded_files:
            if st.button("Process"):
                with st.spinner("Processing"):
                    files = [("files", (file.name, file.getvalue(), file.type))
                             for file in uploaded_files]
                    requests.post(URL+"upload/", files=files, timeout=15)

    if user_question:
        # print(st.session_state.chat_history)
        chat_context = f"chat history: \n {st.session_state.chat_history}"
        full_text = chat_context + user_question
        reply = requests.post(
            URL+"ask", json={"question":  full_text}, timeout=15)
        result = reply.json()
        handle_userinput(user_question, result["answer"])


if __name__ == '__main__':
    main()
