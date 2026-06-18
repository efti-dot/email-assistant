import streamlit as st
import os
from google import genai
from prompts import build_prompt
from dotenv import load_dotenv
from generator import generate_email

load_dotenv()

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
            value=os.getenv("GEMINI_API_KEY", "")
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
                email, prompt = generate_email(intent, key_facts, tone, api_key)
                st.session_state["generated_email"] = email
                st.session_state["last_prompt"] = prompt
            except Exception as e:
                st.error(f"Error:{e}")
                return
            
        if "generated_email" in st.session_state:
            st.subheader("Generated Email")
            st.text_area(
                "Result",
                value=st.session_state["generated_email"],
                height=300
            )
            with st.expander("View the prompt"):
                st.code(st.session_state["last_prompt"], language="text")




if __name__ == "__main__":
    screen()