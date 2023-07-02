import streamlit as st 
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values
import os 

import guidance 
import pyperclip 

# Load environment variables
config = dotenv_values(".env")
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

user_input = st.text_input("Ask anything")

llm4 = ChatOpenAI(model_name="gpt-4", 
                 temperature=0.7, 
                 request_timeout=240,
                 max_retries=4,
                 max_tokens=2000)

llm3 = ChatOpenAI(model_name="gpt-3.5-turbo", 
                 temperature=0.7, 
                 request_timeout=240,
                 max_retries=4,
                 max_tokens=2000)

gmodel4 = guidance.llms.OpenAI("gpt-4")

gmodel3 = guidance.llms.OpenAI("gpt-3.5-turbo")

@st.cache_resource
def improve_prompt(human_input, use4 = False):
    """_summary_

    Args:
        input (_type_): _description_
    """
    
    # prompt_creator = guidance(
    # """
    # {{#system~}}
    # You are a helpful and terse assistant.
    # {{~/system}}
    # {{#user~}}
    # I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for GPT3, GPT4, or ChatGPT. 

    # 1. The prompt we are creating should be written from the perspective of Me (the user) making a request to you, ChatGPT (a GPT3/GPT4 interface). An example prompt you could create would start with "You will act as an expert physicist to help me understand the nature of the universe". 

    # Think carefully and use your imagination to create 3 amazing prompts for me. My initial prompt is provided in backticks: 
    
    # ```
    # {{prompt}}
    # ```
    # {{~/user}}

    # {{#assistant~}}
    # Prompt: {{gen 'answer' temperature=0 max_tokens=500}}
    # {{~/assistant}}
    # """, llm = gmodel4
    # )
    # prompt_run = prompt_creator(
    #     prompt = human_input)
    
    # st.write(prompt_run)
    
    # st.write(prompt_run['answer'])
    # return prompt_run 

    system_instructions = "You are a helpful and terse assistant."
    system_template = "{instructions}"

    system_prompt = SystemMessagePromptTemplate.from_template(
        system_template)


    human_template = """I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for GPT3, GPT4, or ChatGPT. 

    1. The prompt we are creating should be written from the perspective of Me (the user) making a request to you, ChatGPT (a GPT3/GPT4 interface). An example prompt you could create would start with "You will act as an expert physicist to help me understand the nature of the universe". 

    Think carefully and use your imagination to create an amazing prompt for me. My initial prompt is provided in backticks: 
    
    ```
    {prompt}
    ```"""
    human_prompt = HumanMessagePromptTemplate.from_template(
        human_template)

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt, human_prompt])
        
    chain = LLMChain(llm=llm3,
                     prompt=prompt_template)

    output = chain.run({"prompt": human_input,
                        "instructions": system_instructions})
    
    return output 


@st.cache_resource
def answer_prompt(human_input, use4 = False):
    """_summary_

    Args:
        input (_type_): _description_
    """
    
    system_instructions = '''
    You are a helpful and terse assistant.
    '''

    system_template = "{instructions}"

    system_prompt = SystemMessagePromptTemplate.from_template(
        system_template)

    human_template = "{human_input}"
    human_prompt = HumanMessagePromptTemplate.from_template(
        human_template)

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt,human_prompt])
        
    chain = LLMChain(llm=llm4,
                     prompt=prompt_template)

    output = chain.run({"human_input": human_input,
                        "instructions": system_instructions})
    
    return output 

def expert_answer(query):
    # gpt4 = guidance.llms.OpenAI("gpt-4")

    experts = guidance('''
    {{#system~}}
    You are a helpful and terse assistant.
    {{~/system}}

    {{#user~}}
    I want a response to the following question:
    {{query}}
    Name 3 world-class experts (past or present) who would be great at answering this?
    Don't answer the question yet.
    {{~/user}}

    {{#assistant~}}
    {{gen 'expert_names' temperature=0 max_tokens=300}}
    {{~/assistant}}

    {{#user~}}
    Great, now please answer the question as if these experts had collaborated in writing a joint anonymous answer.
    {{~/user}}

    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}
    ''', llm=gmodel4)

    expert_answer = experts(query=query)
    return expert_answer['answer']

def combine_answers(answers, initial_prompt):
    
    answers_string = 'Answer: ' + '\n\n Answer: '.join(answers)
    
    system_instructions = '''
    You are a helpful and terse assistant.
    '''

    system_template = "{instructions}"

    system_prompt = SystemMessagePromptTemplate.from_template(
        system_template)

    human_template = """Please synthesize these following answers to the intitial question {initial_prompt} into a single best answer. Keep formatting if formatting is useful.   
    
    {answers_string}"""
    human_prompt = HumanMessagePromptTemplate.from_template(
        human_template)

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt,human_prompt])
        
    chain = LLMChain(llm=llm3,
                     prompt=prompt_template)

    output = chain.run({"answers_string": answers_string,
                        "instructions": system_instructions,
                        "initial_prompt": initial_prompt})
    
    return output

if user_input:
    new_prompt = improve_prompt(user_input)
    
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
            
            if st.button("Copy to clipboard",key=a1):
                pyperclip.copy(a1)
                st.write("*Copied*")
        with col1b:
            
            st.markdown("**Original input, Expert Answer**")
            a2=expert_answer(user_input)
            st.write(a2)
            
            if st.button("Copy to clipboard",key=a2):
                pyperclip.copy(a2)
                st.write("*Copied*")
            
    with col2: 
        with col2a: 
            st.markdown("**Improved prompt, Standard Answer**")
            a3=answer_prompt(new_prompt)
            st.write(answer_prompt(new_prompt))
            
            if st.button("Copy to clipboard",key=a3):
                pyperclip.copy(a3)
                st.write("*Copied*")
                
        with col2b:
            st.markdown("**Improved prompt, Expert Answer**")
            a4=expert_answer(new_prompt)
            st.write(expert_answer(new_prompt))
            
            
            if st.button("Copy to clipboard",key=a4):
                pyperclip.copy(a4)
                st.write("*Copied*")
            
    st.markdown("""---""") 
    
    st.markdown("**Answer summary**")
    combined = combine_answers([a1,a2,a3,a4],user_input)
    st.write(combined)

    if st.button("Copy to clipboard",key=combined):
        pyperclip.copy(combined)
        st.write("*Copied*")