
'''
Tool can be useful for the everyday person. [DONE]
If you want to win an argument, use the tool in order to craft responses [DONE]
Save time, make sure information is accurate [DONE]
OpenAI/Deepseek to collect information and conversate. [DONE]
Will use internal training data from LLM to cite sources [DONE]
(optional) look to connect other data sources [DONE]
User will interact with streamlit, selection boxes for length of arugment;  [DONE]
    (optional) rebuttals/counterclaims; debate/argument style; debate topic/question; etc.
'''

import streamlit as st
import json
from st_chat_message import message
from openai import OpenAI
import os
DEEPSEEK_API_KEY = os.getenv("OPENAI_API_KEY")
if not DEEPSEEK_API_KEY:
    st.error("DeepSeek API key not found. Please set the 'DEEPSEEK_API_KEY' environment variable.")
    st.stop() # Stop the app if no API key
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1" 
)

st.write("Welcome to ARGBOT")



type = st.selectbox("Please select the type of argument", ["Contention (create argument)", "Rebuttle (Argue against)"])
if (type == "Contention (create argument)"):
    with st.form("contentionInputs"):
        topic = st.text_area("Please enter the topic you want to debate / argue / talk about (include for / against): ")

        length = st.selectbox("Please enter the length of your arg", ["short (2-3sentences)", "medium(4 sentences)", "long (5-6 sentences)", "extra long (6-8 sentences)"])
        format = st.selectbox("Please enter ARG format", ["Claim Warrant Statistic Impact", "Topic Evidence Analysis"])
        citations = st.selectbox("Please enter citation format", ["MLA", "APA"])

        submitted = st.form_submit_button("Make an ARG")
        if submitted:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content" : f"""
                        You are a helpful assistant that will make an argument that's length is {length} about the topic {topic}.
                        Please use evidences online and return in {citations} citation format. Do not make up evidences.
                        Please write the argument in this format: {format}. For the evidence URL, cite the exact link to the evidence you provided. 
                        Avoid Latex and stricly format in Markdown
                    """}, 
                ],
                stream=False
            )

            st.write(response.choices[0].message.content)
elif (type == "Rebuttle (Argue against)"):
    with st.form("rebuttleInputs"):
        topic = st.text_area("Please enter the topic you want to debate / argue / talk about (include for / against): ")
        enemyEssay = st.text_area("Please include your opponent's argument. (You can type whole thing or summarize it)")
        
        length = st.selectbox("Please enter the length of your arg", ["short (2-3sentences)", "medium(4 sentences)", "long (5-6 sentences)", "extra long (6-8 sentences)"])
        format = st.selectbox("Please enter ARG format", ["Claim Warrant Statistic Impact", "Topic Evidence Analysis"])
        citations = st.selectbox("Please enter citation format", ["MLA", "APA"])

        submitted = st.form_submit_button("Make an Rebuttle")
        if submitted:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content" : f"""
                        You are a helpful assistant that will make a rebuttle that is {length} about the topic {topic}.
                        The other side's arguments are {enemyEssay}.
                        The rebuttle should find logic issues (self conflicting for instance), find evidence issues (impractical, outdated, not impact), find out why the other sides arguments are WRONG. 
                        Also when you are rebuttling the other side's argument, you should repeat and tell us what the other sides arguments that you are going to counter. 
                        Please use evidences online and return in {citations} citation format. Do not make up evidences.
                        Please write the argument in this format: {format}. For the evidence URL, cite the exact link to the evidence you provided. 
                        Avoid Latex and stricly format in Markdown
                    """}, 
                ],
                stream=False
            )

            st.write(response.choices[0].message.content)