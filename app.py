import streamlit as st 
from langchain.callbacks.streamlit import StreamlitCallbackHandler

st.set_page_config(
    page_title="GPT Prompt Help",
)

from functions import (
    improve_prompt,
    answer_prompt,
    combine_answers
)

sidebar_message = """
# GPT Prompt Help

### A.k.a. Do you Need a Prompt Engineer?
This app helps you see potential improvements of your GPT3/GPT4 prompts, and see the results of those changed prompts.

### What this app does:
1. Enter any prompt into the box. 
2. The app will answer that prompt, as is (using GPT3.5). 
3. Next, it will show an altered verison of the initial prompt. 
4. The app then also answers the new prompt.
5. Finally, it will summarize the answers and the difference. 

---
    
### Why use this app?
- As Large Language Models become more prevalent, prompt engineering has become hot topic. 
- **GPT Prompt Help** aims to provide everyone an easy way to experience the benefit of improved prompts.
- It also helps teach how we can improve prompts for ourselves.

### What are the prompts used?
The app is now available on [Github](https://github.com/KevinRPan/gptprompthelp).

"""

with st.sidebar:
    st.write(sidebar_message)
    

expander = st.expander("Tips")
expander.write("Try running any question on your mind. The app will try to answer it, and then improve the prompt to see if it can answer it better. For example, _help me understand prompt engineering_.")

if user_input := st.chat_input("Ask anything"):

    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        a1 = answer_prompt(user_input, callbacks=[st_callback], system_instructions="")

    st.markdown("---")

    st.info("**Improved prompt** \n\n The app will now try to improve your prompt.")
    with st.chat_message("user"):
        st_callback = StreamlitCallbackHandler(st.container())
        new_prompt_complex = improve_prompt(user_input, callbacks=[st_callback], simple_instruction=False, use4 = False)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        a_complex = answer_prompt(new_prompt_complex, callbacks=[st_callback])

    st.markdown("""---""") 
    with st.chat_message("user"):
        st.write("Describe the difference between these two answers and summarize them into a single answer.")

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        combined = combine_answers([a1,a_complex],
                                    user_input, 
                                    callbacks=[st_callback])

    st.markdown("""---""") 
