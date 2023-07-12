import streamlit as st 
import pyperclip 
from functions import (
    improve_prompt,
    answer_prompt,
    expert_answer,
    combine_answers,
    llm3
)

st.set_page_config(
    page_title="GPT Prompt Help",
)

with st.sidebar:
    st.write("# GPT Prompt Help")
    
    st.write("### A.k.a. Do you Need a Prompt Engineer?")
    
    st.write("This app helps you see potential improvements your GPT3/GPT4 prompts, and see the results of those potental changes.")
    
    st.write("### How to use this app")
    st.write("Enter any prompt into the box. The app will answer that prompt as is (using GPT3.5), then suggest an improved verison of that prompt, and answer that improved prompt.")
    
    st.write("After the prompts have been answered, the app will combine the answers into a single answer, presented again at the top of the page.")
    
    st.markdown("---")
    
    st.write("#### Why use this app?")
    st.write("As Large Language Models become more prevalent, prompt engineering has become hot topic. **GPT Prompt Help** aims to provide everyone an easy way to experience the benefit of improved prompts, and to learn how to improve them for themselves.")
    
    
    st.write("### What happens with what I enter?")
    st.write("The app uses popular prompt engineering prompts to iterate on the initial prompt, and then proceeds to answer those improved versions in addition to the initial version. All of these are temporary, what is entered and generated cannot be retrieved by anyone, they are not logged by this app nor by the model service.")
    
    st.write("#### Donation info")
    st.write("If you enjoyed using this, please feel free to share or to tip me to cover API costs on [PayPal](https://paypal.me/kevinrpan) or [Venmo](https://venmo.com/kevin-pan), or share any comments and feedback to hello@gptprompthelp.com. (I appreciate feedback!)")
    

# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.chains import LLMChain
# from langchain import PromptTemplate

if user_input := st.chat_input("Ask anything"):
    
    # st.chat_message("user").write(user_input)
    
    # with st.chat_message("assistant"):
    #     st_callback = StreamlitCallbackHandler(st.container())
    #     llm = llm3
    #     prompt = PromptTemplate.from_template("{prompt}")
    #     chain = LLMChain(llm=llm,
    #                         prompt=prompt)
    #     # response = agent.run(user_input, callbacks=[st_callback])
    #     response = chain.run(user_input, callbacks=[st_callback])
    #     st.write(response)
    
    
    st.info("**Original prompt:** " + user_input)

    st.markdown("**Original input**")
    
    a1=answer_prompt(user_input,system_instructions="")
    st.write(a1)
    
    if st.button("Copy to clipboard",key='a1'):
        pyperclip.copy(a1)
        st.write("*Copied*")
    
    st.markdown("---")
    new_prompt_simple = improve_prompt(user_input, simple_instruction=True, use4 = False)
    
    st.info("**Improved prompt:** " + new_prompt_simple)
    # col2a,col2b = st.columns([1,1])
    
    st.markdown("**Improved prompt**")
    a_simple=answer_prompt(new_prompt_simple)
    st.write(a_simple)
    
    if st.button("Copy to clipboard",key='a_simple'):
        pyperclip.copy(a_simple)
        st.write("*Copied*")
    
    
    st.markdown("---")
    new_prompt_complex = improve_prompt(user_input, simple_instruction=False, use4 = False)
    
    st.info("**Improved prompt:** " + new_prompt_complex)

    st.markdown("**Improved prompt**")
    a_complex=answer_prompt(new_prompt_complex)
    st.write(a_complex)
    
    if st.button("Copy to clipboard",key='a_comp'):
        pyperclip.copy(a_complex)
        st.write("*Copied*")
        
    st.markdown("""---""") 

    summary = st.container()
    with summary:
        st.markdown("**Answer summary**")
        combined = combine_answers([a1,a_simple,a_complex],
                                   user_input)
        st.write(combined)

        if st.button("Copy to clipboard",key='combined'):
            pyperclip.copy(combined)
            st.write("*Copied*")
            
        st.markdown("""---""") 