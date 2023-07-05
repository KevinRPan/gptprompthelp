import streamlit as st 
import pyperclip 
from functions import (
    improve_prompt,
    answer_prompt,
    expert_answer,
    combine_answers
)


st.set_page_config(
    page_title="GPT Prompt Help",
)

with st.sidebar:
    st.write("## GPT Prompt Help")
    
    st.write("This app helps you improve your GPT3/GPT4 prompts, and see the results of potental changes.")
    
    st.write("### How to use this app")
    st.write("Enter any prompt into the box. The app will answer that prompt as is (using GPT3.5), then suggest an improved verison of that prompt, and answer that improved prompt.")
    
    st.write("After the prompts have been answered, the app will combine the answers into a single answer, presented again at the top of the page.")
    
    st.markdown("---")
    st.write("#### Why use this app?")
    st.write("As Large Language Models become more prevalent, prompt engineering has become hot topic. **GPT Prompt Help** aims to provide everyone an easy way to experience the benefit of improved prompts, and to learn how to improve them for themselves.")
    
    st.write("#### Donation info")
    st.write("Generating answers costs money. If you enjoyed using this, please feel free share or to tip me on [PayPal](https://paypal.me/kevinrpan) or [Venmo](https://venmo.com/kevin-pan), or share any comments and feedback to hello@gptprompthelp.com. (I appreciate feedback!)")
    
user_input = st.text_input("Ask anything")

if user_input:
    new_prompt = improve_prompt(user_input)
    summary = st.container()
    
    # col1, col2, col3, col4 = st.columns([1,1,1,1])
    
    col1, col2 = st.columns([1,1])
    
    st.info("Original prompt: " + user_input)
    col1a,col1b = st.columns([1,1])
    
    st.info("Improved prompt: " + new_prompt)
    col2a,col2b = st.columns([1,1])
    
    
    with col1:
        with col1a:
            
            st.markdown("**Original input, Standard Answer**")
            a1=answer_prompt(user_input)
            st.write(a1)
            
            if st.button("Copy to clipboard",key='a1'):
                pyperclip.copy(a1)
                st.write("*Copied*")
        with col1b:
            
            st.markdown("**Original input, Expert Answer**")
            a2=expert_answer(user_input)
            st.write(a2)
            
            if st.button("Copy to clipboard",key='a2'):
                pyperclip.copy(a2)
                st.write("*Copied*")
            
    with col2: 
        with col2a: 
            st.markdown("**Improved prompt, Standard Answer**")
            a3=answer_prompt(new_prompt)
            st.write(answer_prompt(new_prompt))
            
            if st.button("Copy to clipboard",key='a3'):
                pyperclip.copy(a3)
                st.write("*Copied*")
                
        with col2b:
            st.markdown("**Improved prompt, Expert Answer**")
            a4=expert_answer(new_prompt)
            st.write(expert_answer(new_prompt))
            
            
            if st.button("Copy to clipboard",key='a4'):
                pyperclip.copy(a4)
                st.write("*Copied*")

    with summary:
        st.markdown("**Answer summary**")
        combined = combine_answers([a1,a2,a3,a4],
                                   user_input)
        st.write(combined)

        st.markdown("""---""") 
        if st.button("Copy to clipboard",key='combined'):
            pyperclip.copy(combined)
            st.write("*Copied*")