from fastapi import FastAPI, HTTPException
from typing import Dict
from pydantic import BaseModel
import streamlit as st
import openai

app = FastAPI()

# The question generation function (from my Streamlit script)
def generate_question(language, concept, blooms_level, user_level):
    initialize_prompt = "You are an expert programming teacher."
    prompt = initialize_prompt + f"Give me a question on the topic : {concept} in the language : {language}. My current level is : {user_level} and my goal is to : {blooms_level}."

    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages=[
            {"role": "user", "content": prompt}
        ]   
    )
    question = response.choices[0].message  
    return question 

# The chat interaction function (from my Streamlit script)
def generate_ai_response(chat_history):
    prompt_to_summarize = "Give me a feedback on my recent responses using one of the three words\n 1. Not Accepted \n 2. Satisfactory \n 3. Proficient"
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines as well
        prompt=chat_history + prompt_to_summarize,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Model for input data
class QuestionRequest(BaseModel):
    language: str
    concept: str
    blooms_level: str
    user_level: str

# Model for chat data
class ChatRequest(BaseModel):
    chat_history: str
    latest_student_response: str

@app.post("/generate-question/")
def generate_question_api(question_request: QuestionRequest) -> Dict[str, str]:
    question = generate_question(
        question_request.language,
        question_request.concept,
        question_request.blooms_level,
        question_request.user_level
    )
    return {"question": question}

@app.post("/generate-ai-response/")
def generate_ai_response_api(chat_request: ChatRequest) -> Dict[str, str]:
    ai_response = generate_ai_response(
        chat_request.chat_history + f"\nStudent: {chat_request.latest_student_response}"
    )
    return {"ai_response": ai_response}
