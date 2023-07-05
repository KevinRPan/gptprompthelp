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
import streamlit as st 
import guidance 

# Load environment variables
config = dotenv_values(".env")
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]


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

USE_4 = False

if USE_4:
    llm = llm4
    gmodel = gmodel4 
else: 
    llm = llm3 
    gmodel = gmodel3 

meta_prompt_1 = """

Given the user's initial prompt "{user prompt:""}" enhance it. 1. Start with clear, precise instructions placed at the beginning of the prompt. 2. Include specific details about the desired context, outcome, length, format, and style. 3. Provide examples of the desired output format, if possible. 4. Use appropriate leading words or phrases to guide the desired output, especially if code generation is involved. 5. Avoid any vague or imprecise language. 6. Rather than only stating what not to do, provide guidance on what should be done instead. Remember to ensure the revised prompt remains true to the user's original intent.

"""


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
        
    chain = LLMChain(llm=llm,
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
        
    chain = LLMChain(llm=llm,
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
    Name 3-5 world-class experts (past or present) who would be great at answering this?
    Don't answer the question yet.
    {{~/user}}

    {{#assistant~}}
    {{gen 'expert_names' temperature=0 max_tokens=300}}
    {{~/assistant}}

    {{#user~}}
    Great, now please answer the question as if these experts had collaborated in writing a joint anonymous answer. Do not mention that this was a combined effort from multiple experts, or that you cannot speak for them. Just answer the question as if you were a single expert.
    {{~/user}}

    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=1000}}
    {{~/assistant}}
    ''', llm=gmodel)

    expert_answer = experts(query=query)
    return expert_answer['answer']

def combine_answers(answers, initial_prompt, verbose = False):
    
    answers_string = 'Answer: ' + '\n\n Answer: '.join(answers)
    
    # st.write(answers_string)
    
    system_instructions = '''
    You are a helpful and terse assistant. Do not answer the question yourself. Instead, synthesize the answers into a single best answer.
    '''

    system_template = "{instructions}"

    system_prompt = SystemMessagePromptTemplate.from_template(
        system_template)

    human_template = """Please synthesize these following answers to the intitial question {initial_prompt} into a single best answer. A numbered or bulleted list would be preferred if relevant. Only answer the question, do not give other reminders or comments. Keep interesting details, remove filler instructions, unnecessary context, and reminders. 
    
    {answers_string}"""
    human_prompt = HumanMessagePromptTemplate.from_template(
        human_template)

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt,human_prompt])
        
    chain = LLMChain(llm=llm,
                     prompt=prompt_template)

    output = chain.run({"answers_string": answers_string,
                        "instructions": system_instructions,
                        "initial_prompt": initial_prompt})
    
    return output