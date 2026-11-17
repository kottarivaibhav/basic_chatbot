from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv
import random
import re

load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
## Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

rules = {
    "greeting": {
        "patterns": [
            r"\b(hi|hello|hey|greetings)\b",
            r"\bgood (morning|afternoon|evening)\b",
        ],
        "responses": [
            "Hello! How can I help you today?",
            "Hi there! What's on your mind?",
            "Hey! Ask me anything.",
        ],
    },
    "hours": {
        "patterns": [
            r"\b(hours|open|close|timing|schedule)\b",
            r"\bwhen are you open\b",
        ],
        "responses": [
            "We are open Monday through Friday, from 9:00 AM to 5:00 PM.",
            "Our operating hours are 9 AM – 5 PM on weekdays.",
        ],
    },
    "pricing": {
        "patterns": [
            r"\b(price|pricing|cost|how much|plans)\b",
            r"\bsubscription\b",
        ],
        "responses": [
            "Our basic plan starts at $10/month, and our pro plan is $25/month.",
            "You can get started for free, or upgrade to Pro for $25/month.",
        ],
    },
    "thanks": {
        "patterns": [r"\b(thanks|thank you|appreciate it)\b"],
        "responses": [
            "You're welcome!",
            "Happy to help!",
            "Anytime! Let me know if you need anything else.",
        ],
    },
}

fallback_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "Sorry, I don't have an answer for that yet.",
    "Can you try asking about our hours, pricing, or services?",
]

## streamlit framework

st.title('Langchain Demo With Groq API')
input_text=st.text_input("Demo Pattern question you want to ask ")

def get_response(user_input):
  cleaned_input = user_input.lower().strip()

  # Check each intent and its patterns
  for intent, data in rules.items():
    for pattern in data["patterns"]:
      if re.search(pattern, cleaned_input):
        return random.choice(data["responses"])

  # Return a fallback if no rules match
  return random.choice(fallback_responses)

#llm=ChatGroq(model="openai/gpt-oss-120b",temperature=0.7,max_tokens=1000)
#output_parser=StrOutputParser()
#chain=prompt|llm|output_parser

if input_text:
    st.write(f"Bot: {get_response(input_text)}")