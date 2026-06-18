import streamlit as st
import os
from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"

#generating email
def generate_email(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text.strip()

def screen():
    st.set_page_config(
        page_title="Email Generation Assistant",
        layout="centered"
    )
    
    st.title("Email Generation Assistant")
    st.write("Generate professional emails using Gemini AI.")

    #sidebar for api key
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
        )
        st.caption("Your key is used only for this session and is never stored.")

    #intent input
    intent = st.text_input(
        "Intent",
        placeholder="e.g., Follow up after meeting"
    )

    #key facts
    key_facts = st.text_area(
        "Key Facts (A few bullet points of information)",
        placeholder="""
        Meeting held on June 18
        Client requested updated proposal
        Need response by Friday""",
        height=150
    )

    #tone selection
    tone = st.selectbox(
        "Tone",
        [
            "Formal",
            "Casual",
            "Professional",
            "Friendly",
            "Empathetic",
            "Urgent",
            "Persuasive"
        ]
    )

    # Generate Button
    if st.button("Generate Email", use_container_width=True):
        if not intent.strip():
            st.warning("Please enter an intent.")
            return
        
        if not key_facts.strip():
            st.warning("Please enter at least one key fact.")
            return
        
        with st.spinner("Generating email..."):
            #st.write("This is youe email")
            try:
                email = generate_email("demo prompt", api_key)
            except Exception as e:
                st.error("Error:{e}")




if __name__ == "__main__":
    screen()