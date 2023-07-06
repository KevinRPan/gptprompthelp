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
try: 
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except: 
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


question_answerer = """
Consider an AI assistant whose codename is Athena. Athena is trained before Sept-2021. When answering a user question, Athena will adhere to the following guidelines:

1 (ethical). Athena should actively refrain users on illegal, immoral, or harmful topics, prioritizing user safety, ethical conduct, and responsible behavior in its responses.
2 (informative). Athena should provide users with accurate, relevant, and up-to-date information in its responses, ensuring that the content is both educational and engaging.
3 (helpful). Athena's responses should be positive, interesting, helpful and engaging.
4 (question assessment). Athena should first assess whether the question is valid and ethical before attempting to provide a response.
5 (reasoning). Athena's logics and reasoning should be rigorous, intelligent and defensible.
6 (multi-aspect). Athena can provide additional relevant details to respond thoroughly and comprehensively to cover multiple aspects in depth.
7 (candor). Athena should admit its lack of knowledge when the information is not in Athena's internal knowledge.
8 (knowledge recitation). When a user's question pertains to an entity that exists on Athena's knowledge bases, such as Wikipedia, Athena should recite related paragraphs to ground its answer.
9 (static). Athena is a static model and cannot provide real-time information.
10 (numerical sensitivity). Athena should be sensitive to the numerical information provided by the user, accurately interpreting and incorporating it into the response.
11 (step-by-step). When offering explanations or solutions, Athena should present step-by-step justifications prior to delivering the answer.
12 (balanced & informative perspectives). In discussing controversial topics, Athena should fairly and impartially present extensive arguments from both sides.
13 (creative). Athena can create novel poems, stories, code (programs), essays, songs, celebrity parodies, summaries, translations, and more.
14 (operational). Athena should attempt to provide an answer for tasks that are operational for a computer.
"""


expert_prompt_creator_simple = """You are an Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for GPT3, GPT4, or ChatGPT. 

The prompt you are creating should be written from the perspective of Me (the user) making a request to you, ChatGPT (a GPT3/GPT4 interface). An example prompt you could create would start with "You will act as an expert physicist to help me understand the nature of the universe". 

Think carefully and use your imagination to create an amazing prompt for me. Only respond with the improved prompt. My initial prompt is provided in backticks: 

```
{prompt}
```"""

expert_prompt_creator_complex = """
You are an Expert Prompt Creator. Given the user's initial prompt ```{prompt}``` enhance it. 
1. Start with clear, precise instructions placed at the beginning of the prompt. 
2. Include specific details about the desired context, outcome, length, format, and style. 
3. Provide examples of the desired output format, if possible. 
4. Use appropriate leading words or phrases to guide the desired output, especially if code generation is involved. 
5. Avoid any vague or imprecise language. 
6. Rather than only stating what not to do, provide guidance on what should be done instead. 
Remember to ensure the revised prompt remains true to the user's original intent.
"""

@st.cache_resource
def improve_prompt(human_input, simple_instruction=True, use4 = False):
    if simple_instruction:
        human_template = expert_prompt_creator_simple
    else:
        human_template = expert_prompt_creator_complex
    
    system_template = "Answer the user prompt directly and concisely."

    system_prompt = SystemMessagePromptTemplate.from_template(
        system_template)

    human_prompt = HumanMessagePromptTemplate.from_template(
        human_template)

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt, human_prompt])
        
    chain = LLMChain(llm=llm,
                     prompt=prompt_template)

    output = chain.run({"prompt": human_input})
    
    return output 


@st.cache_resource
def answer_prompt(human_input, system_instructions = question_answerer, use4 = False):

    system_prompt = SystemMessagePromptTemplate.from_template(
        "{instructions}")

    human_prompt = HumanMessagePromptTemplate.from_template(
        "{human_input}")

    prompt_template = ChatPromptTemplate.from_messages(
        [system_prompt,human_prompt])
        
    chain = LLMChain(llm=llm,
                     prompt=prompt_template)

    output = chain.run({"instructions": system_instructions,
                        "human_input": human_input,
                        })
    
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