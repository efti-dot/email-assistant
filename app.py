import streamlit as st
import os

def screen():
    st.set_page_config(
        page_title="Email Generation Assistant",
        layout="centered"
    )
    
    st.title("Email Generation Assistant")
    st.write("Generate professional emails using Gemini AI.")

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
    if st.button("Generate Email"):
        if not intent.strip():
            st.warning("Please enter an intent.")
        elif not key_facts.strip():
            st.warning("Please enter at least one key fact.")
        with st.spinner("Generating email..."):
            st.write("This is youe email")




if __name__ == "__main__":
    screen()